"""Checks the test suite runs against the skill files, written as functions so fixtures can exercise them."""

import re
from pathlib import Path

import yaml

LIST_MARKER = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")
CLAUSE_END = re.compile(r"""[.,;:?!][*_`"')\]]*$""")
SENTENCE_END = re.compile(r"""[.?!][*_"')\]]*\s+(?=[\w"'*\[])""")
INITIAL = re.compile(r"(?:^|[\s(])[A-Z]\.$")
DOTTED_ABBREVIATION = re.compile(r"(?:^|[\s(])(?:[A-Za-z]\.)+[A-Za-z]\.$")
SENTENCE_STARTERS = {
    "A",
    "An",
    "And",
    "But",
    "I",
    "It",
    "Its",
    "So",
    "That",
    "The",
    "Then",
    "These",
    "This",
    "We",
    "You",
}
TITLE_ABBREVIATION = re.compile(r"\b(?:vs|cf|No|Dr|Mr|Ms)\.$")
TRAILING_ABBREVIATION = re.compile(r"\betc\.$")
DASH_CONNECTOR = re.compile(r"—| – | -{1,2} ")
CODE_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
BACKTICKED_MD = re.compile(r"`([\w./~-]+\.md)`")
LINKED_MD = re.compile(r"\]\(([^)\s#]+\.md)(?:#[^)]*)?\)")
INSTALLED_PATH = re.compile(r"~/\.(?:claude|agents|codex|gemini/config)/skills/de-ai/([^`\s)]+)")


def skill_markdown_files(skill_dir):
    """SKILL.md and every markdown file under references/, nested folders included."""
    skill_dir = Path(skill_dir)
    return [skill_dir / "SKILL.md", *sorted((skill_dir / "references").rglob("*.md"))]


def parse_frontmatter(text):
    """Return the frontmatter mapping, or raise ValueError naming what is wrong with it."""
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError("file must open with a --- frontmatter block")
    try:
        fields = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise ValueError(f"frontmatter is invalid YAML: {error}") from error
    if not isinstance(fields, dict):
        raise ValueError("frontmatter must be a mapping")
    for key in ("name", "description"):
        if not isinstance(fields.get(key), str) or not fields[key].strip():
            raise ValueError(f"frontmatter needs a non-empty string {key!r}")
    return fields


def frontmatter_problems(text, directory_name):
    try:
        fields = parse_frontmatter(text)
    except ValueError as error:
        return [str(error)]
    problems = []
    if fields["name"] != directory_name:
        problems.append(f"name {fields['name']!r} does not match directory {directory_name!r}")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", fields["name"]):
        problems.append("name must be 1 to 64 lowercase letters, digits or hyphens")
    if len(fields["description"]) > 1024:
        problems.append("description is longer than 1024 characters")
    if re.search(r"[<>]", fields["description"]):
        problems.append("description contains an angle bracket")
    return problems


def strip_code_spans(line):
    """Replace inline code spans with a placeholder; return None when a span is left open."""
    out, index = [], 0
    while index < len(line):
        char = line[index]
        if char == "\\" and line[index + 1 : index + 2] == "`":
            out.append("`")
            index += 2
            continue
        if char != "`":
            out.append(char)
            index += 1
            continue
        run = len(line[index:]) - len(line[index:].lstrip("`"))
        fence = "`" * run
        close = index + run
        while True:
            close = line.find(fence, close)
            if close == -1:
                return None
            after = close + run
            if after < len(line) and line[after] == "`":
                close = after + len(line[after:]) - len(line[after:].lstrip("`"))
                continue
            break
        out.append("CODE")
        index = close + run
    return "".join(out)


def markdown_lines(text):
    """Yield (number, kind, line) for every line outside frontmatter and code.

    kind is "heading", "table", "quote", "prose" or "blank".
    Code is a fenced block, at top level or inside a blockquote, or an indented block after a blank line
    outside a list. A fence closes only on its opening character repeated at least as many times.
    """
    lines = text.splitlines()
    in_frontmatter = bool(lines) and lines[0] == "---"
    fence = None
    previous_blank = True
    in_list = False
    for number, line in enumerate(lines, start=1):
        if in_frontmatter:
            if number > 1 and line == "---":
                in_frontmatter = False
            continue
        unquoted = re.sub(r"^ {0,3}(?:>\s?)+", "", line)
        match = CODE_FENCE.match(unquoted)
        if fence is None and match and not (match.group(1)[0] == "`" and "`" in match.group(2)):
            fence = match.group(1)
            previous_blank = False
            if not line.startswith((" ", "\t")):
                in_list = False
            continue
        if fence is not None:
            closing = match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence)
            if closing and not match.group(2).strip():
                fence = None
            continue
        stripped = line.strip()
        indented_code = previous_blank and not in_list and re.match(r"^(?: {4}|\t)", line) and stripped
        if indented_code:
            continue
        if not stripped or stripped == "---":
            previous_blank = True
            yield number, "blank", line
            continue
        previous_blank = False
        if LIST_MARKER.match(line):
            in_list = True
        elif not line.startswith((" ", "\t")):
            in_list = False
        if stripped.startswith("#"):
            yield number, "heading", line
        elif stripped.startswith("|"):
            yield number, "table", line
        elif stripped.startswith(">"):
            yield number, "quote", line
        else:
            yield number, "prose", line


def dash_problems(text):
    """Dash clause connectors in prose, quotes and headings, plus the frontmatter description."""
    problems = []
    try:
        description = parse_frontmatter(text)["description"]
    except ValueError:
        description = ""
    if DASH_CONNECTOR.search(description):
        problems.append("description: dash clause connector")
    for number, kind, line in markdown_lines(text):
        if kind in ("blank", "table"):
            continue
        body = LIST_MARKER.sub("", line.lstrip("> ").lstrip("#").strip())
        body = strip_code_spans(body) or body
        if DASH_CONNECTOR.search(body):
            problems.append(f"line {number}: dash clause connector: {line}")
    return problems


def sentence_count(text):
    """Count sentences on one line, allowing initials, dotted abbreviations and mid-sentence etc."""
    count = 1
    for boundary in SENTENCE_END.finditer(text):
        before = text[: boundary.start() + 1]
        following = text[boundary.end()]
        next_word = re.match(r"[\w']+", text[boundary.end() :])
        if INITIAL.search(before) or TITLE_ABBREVIATION.search(before):
            continue
        if DOTTED_ABBREVIATION.search(before) and not (next_word and next_word.group(0) in SENTENCE_STARTERS):
            continue
        if TRAILING_ABBREVIATION.search(before) and following.islower():
            continue
        count += 1
    return count


def line_structure_problems(text, check_quotes=True):
    """One sentence per line, breaks after punctuation, and no inline code span split across lines.

    check_quotes=False skips blockquotes, for files whose quotes are lists of example fragments.
    """
    problems = []
    checked = ("prose", "quote") if check_quotes else ("prose",)
    entries = [(n, k, line) for n, k, line in markdown_lines(text) if k in ("prose", "quote", "blank", "heading")]
    for position, (number, kind, line) in enumerate(entries):
        if kind not in checked:
            continue
        body = re.sub(r"^\s*>\s?", "", line) if kind == "quote" else line
        body = LIST_MARKER.sub("", body)
        spanless = strip_code_spans(body)
        if spanless is None:
            problems.append(f"line {number}: inline code span left open: {line}")
            continue
        if sentence_count(spanless.strip()) > 1:
            problems.append(f"line {number}: more than one sentence: {line}")
        if line.endswith("  "):
            continue
        following = entries[position + 1] if position + 1 < len(entries) else None
        continues = (
            following is not None
            and following[0] == number + 1
            and following[1] == kind
            and not LIST_MARKER.match(re.sub(r"^\s*>\s?", "", following[2]))
        )
        if continues and not CLAUSE_END.search(body.rstrip()):
            problems.append(f"line {number}: wrapped mid-clause: {line}")
    return problems


def resolve_reference(token, containing_file, skill_dir):
    """Resolve a named markdown file, or return None when it names a path outside this skill's layout.

    `references/...` resolves from the skill root, a bare file name from its own folder, the
    skill root or `references/`, and any other folder path belongs to another repository.
    """
    if token.startswith("references/"):
        return [(skill_dir / token).resolve()]
    if "/" in token:
        return None
    return [(folder / token).resolve() for folder in (containing_file.parent, skill_dir, skill_dir / "references")]


def named_references(path, skill_dir):
    text = path.read_text()
    for token in [*BACKTICKED_MD.findall(text), *LINKED_MD.findall(text)]:
        if token.startswith("~/") or "://" in token:
            continue
        candidates = resolve_reference(token, path, skill_dir)
        if candidates is not None:
            yield token, candidates


def reference_problems(skill_dir):
    """Named references that do not exist, references SKILL.md cannot reach, installed paths that escape."""
    skill_dir = Path(skill_dir).resolve()
    skill_md, *references = skill_markdown_files(skill_dir)
    problems = []
    for path in [skill_md, *references]:
        for token, candidates in named_references(path, skill_dir):
            if not any(c.is_relative_to(skill_dir) and c.is_file() for c in candidates):
                problems.append(f"{path.name}: missing reference {token}")
        for relative in INSTALLED_PATH.findall(path.read_text()):
            target = (skill_dir / relative).resolve()
            if not target.is_relative_to(skill_dir) or not target.is_file():
                problems.append(f"{path.name}: installed path escapes or is missing: {relative}")
    reachable = {c for token, candidates in named_references(skill_md, skill_dir) for c in candidates}
    for reference in references:
        if reference.resolve() not in reachable:
            problems.append(f"SKILL.md does not reach {reference.relative_to(skill_dir)}")
    return problems
