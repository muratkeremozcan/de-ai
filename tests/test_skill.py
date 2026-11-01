"""The de-ai skill's frontmatter, references and house rules, plus fixtures proving each check fails when it should."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from skill_checks import (
    dash_problems,
    frontmatter_problems,
    line_structure_problems,
    reference_problems,
    skill_markdown_files,
)

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "de-ai"
SKILL_MD = SKILL_DIR / "SKILL.md"

# ai-tells.md quotes the banned constructions as examples, so the dash check skips it,
# and its blockquotes are lists of example fragments, so the line check skips those.
EXAMPLE_FILES = {SKILL_DIR / "references" / "ai-tells.md"}
SKILL_FILES = skill_markdown_files(SKILL_DIR)
AUTHORED_FILES = [*SKILL_FILES, ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md"))]

VALID_FRONTMATTER = "---\nname: de-ai\ndescription: Strips AI tells.\n---\n\n# de-ai\n"


class SkillFileTests(unittest.TestCase):
    def test_frontmatter(self):
        self.assertEqual(frontmatter_problems(SKILL_MD.read_text(), SKILL_DIR.name), [])

    def test_references(self):
        self.assertEqual(reference_problems(SKILL_DIR), [])

    def test_no_dash_clause_connectors(self):
        for path in AUTHORED_FILES:
            if path not in EXAMPLE_FILES:
                with self.subTest(file=path.name):
                    self.assertEqual(dash_problems(path.read_text()), [])

    def test_one_sentence_per_line(self):
        for path in AUTHORED_FILES:
            with self.subTest(file=path.name):
                problems = line_structure_problems(path.read_text(), check_quotes=path not in EXAMPLE_FILES)
                self.assertEqual(problems, [])


class FrontmatterFixtureTests(unittest.TestCase):
    def test_valid_frontmatter_passes(self):
        self.assertEqual(frontmatter_problems(VALID_FRONTMATTER, "de-ai"), [])

    def test_failures(self):
        cases = {
            "missing block": "# de-ai\n",
            "invalid yaml": '---\nname: de-ai\ndescription: "unclosed\n---\n',
            "not a mapping": "---\n- de-ai\n---\n",
            "missing description": "---\nname: de-ai\n---\n",
            "empty block scalar": "---\nname: de-ai\ndescription: |\n---\n",
            "non-string name": "---\nname: 7\ndescription: x\n---\n",
            "wrong name": "---\nname: other\ndescription: x\n---\n",
            "long description": f"---\nname: de-ai\ndescription: {'x' * 1025}\n---\n",
            "angle bracket": "---\nname: de-ai\ndescription: use <this>\n---\n",
        }
        for label, text in cases.items():
            with self.subTest(case=label):
                self.assertNotEqual(frontmatter_problems(text, "de-ai"), [])


class DashFixtureTests(unittest.TestCase):
    def test_compound_words_and_list_markers_pass(self):
        text = (
            VALID_FRONTMATTER
            + "- A long-term fix.\n1. A well-tuned gate.\nSee pages 3–5.\nRun `ls - x`.\n| a | - |\n```\nx - y\n```\n"
            + "~~~\nx - y\n~~~\n"
            + "\n    x - y\n"
        )
        self.assertEqual(dash_problems(text), [])

    def test_failures(self):
        cases = {
            "em dash in prose": "It works — mostly.\n",
            "spaced hyphen in prose": "It works - mostly.\n",
            "spaced en dash": "It works – mostly.\n",
            "double hyphen": "It works -- mostly.\n",
            "em dash in quote": "> It works — mostly.\n",
            "em dash after a nested fence": "````markdown\n```python\nx = 1\n````\nThis works — mostly.\n",
            "em dash in heading": "## Setup — quick\n",
            "em dash in list item": "- It works — mostly.\n",
            "description": "---\nname: de-ai\ndescription: Strips tells — fast.\n---\n",
        }
        for label, text in cases.items():
            with self.subTest(case=label):
                self.assertNotEqual(dash_problems(text), [])


class LineStructureFixtureTests(unittest.TestCase):
    def test_valid_structure_passes(self):
        text = (
            "One sentence here.\n"
            "A long sentence breaks after a comma,\n"
            "and continues here.\n"
            "Use `gh pr view. Then` as a literal.\n"
            "See e.g. the docs.\n"
            "Ask J. Smith for help.\n"
            "Follow the U.S. Treasury guidance.\n"
            "It handles files, links, etc. and then exits.\n"
            "Use \\` to escape a backtick.\n"
            "1) First step\n"
            "2) Second step\n"
            "\n"
            "````markdown\n```python\nTwo sentences. In a nested fence.\n````\n"
            "~~~\nTwo sentences. In a tilde fence.\n~~~\n"
            "> ```python\n> x = `y\n> ```\n"
            "\n"
            "    Two sentences. In indented code.\n"
            "- A short list item\n"
            "- Another one\n"
            "\n"
            "A hard break  \n"
            "continues.\n"
            "```\nTwo sentences. In a fence.\n```\n"
            "| Two sentences. In a table. |\n"
        )
        self.assertEqual(line_structure_problems(text), [])

    def test_failures(self):
        cases = {
            "two sentences on a line": "This is one sentence. This is a second sentence.\n",
            "wrapped mid-clause": "This sentence wraps in the\nmiddle of a clause.\n",
            "wrapped quote": "> This quote wraps in the\n> middle of a clause.\n",
            "two sentences in a quote": "> First sentence. Second sentence.\n",
            "split inline code": "Run `gh pr view.\nThen continue`.\n",
            "wrapped list item": "- This item wraps in the\n  middle of a clause.\n",
            "two sentences in a numbered item": "1. First sentence. Second sentence.\n",
            "lowercase second sentence": "first sentence. second sentence.\n",
            "numeric second sentence": "We support 3.11. 3.13 is next.\n",
            "etc ending a sentence": "It handles files, links, etc. Then it exits.\n",
            "acronym ending a sentence": "This runs in the U.S. Then it stops.\n",
            "prose after a nested fence": "````markdown\n```python\nx = 1\n````\nOne. Two.\n",
        }
        for label, text in cases.items():
            with self.subTest(case=label):
                self.assertNotEqual(line_structure_problems(text), [])


class ReferenceFixtureTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.skill = self.tmp / "skills" / "de-ai"
        shutil.copytree(SKILL_DIR, self.skill)
        (self.tmp / "README.md").write_text("outside the skill\n")

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def append(self, line):
        skill_md = self.skill / "SKILL.md"
        skill_md.write_text(skill_md.read_text() + line + "\n")

    def test_copy_passes(self):
        self.assertEqual(reference_problems(self.skill), [])

    def test_missing_inline_reference(self):
        self.append("Read `references/missing.md`.")
        self.assertNotEqual(reference_problems(self.skill), [])

    def test_missing_markdown_link(self):
        self.append("Read [extra guidance](references/missing.md).")
        self.assertNotEqual(reference_problems(self.skill), [])

    def test_unreachable_reference(self):
        (self.skill / "references" / "orphan.md").write_text("# Orphan\n")
        self.assertNotEqual(reference_problems(self.skill), [])

    def test_nested_reference_resolves(self):
        (self.skill / "references" / "extra").mkdir()
        (self.skill / "references" / "extra" / "more.md").write_text("# More\n")
        self.append("Read [more](references/extra/more.md).")
        self.assertEqual(reference_problems(self.skill), [])

    def test_missing_sibling_reference(self):
        voice = self.skill / "references" / "murat-voice.md"
        voice.write_text(voice.read_text().replace("`pr-descriptions.md`", "`missing.md`"))
        self.assertNotEqual(reference_problems(self.skill), [])

    def test_other_repository_paths_are_skipped(self):
        self.append("The filter lives at `skills/cto-filter/SKILL.md`.")
        self.assertEqual(reference_problems(self.skill), [])

    def test_installed_paths_for_every_root(self):
        for root in (".claude", ".agents", ".codex", ".gemini/config"):
            for relative in ("../../README.md", "references/missing.md"):
                with self.subTest(root=root, path=relative):
                    skill_md = self.skill / "SKILL.md"
                    original = skill_md.read_text()
                    self.append(f"Read `~/{root}/skills/de-ai/{relative}`.")
                    self.assertNotEqual(reference_problems(self.skill), [])
                    skill_md.write_text(original)

    def test_nested_reference_files_get_house_rule_checks(self):
        nested = self.skill / "references" / "nested-probe" / "bad.md"
        nested.parent.mkdir()
        nested.write_text("This works — mostly. Another sentence.\n")
        self.assertIn(nested, skill_markdown_files(self.skill))
        self.assertNotEqual(dash_problems(nested.read_text()), [])
        self.assertNotEqual(line_structure_problems(nested.read_text()), [])


class InstallScriptTests(unittest.TestCase):
    ROOTS = (".claude/skills", ".agents/skills", ".codex/skills", ".gemini/config/skills")

    def setUp(self):
        self.home = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.home)

    def run_install(self):
        env = {**os.environ, "HOME": str(self.home)}
        script = ROOT / "scripts" / "install.sh"
        return subprocess.run(["bash", str(script)], env=env, capture_output=True, text=True)

    def test_fresh_home_gets_all_four_links(self):
        self.assertEqual(self.run_install().returncode, 0)
        for root in self.ROOTS:
            with self.subTest(root=root):
                self.assertEqual((self.home / root / "de-ai").resolve(), SKILL_DIR.resolve())

    def test_existing_symlink_is_replaced_in_place(self):
        old = self.home / "old-skill"
        old.mkdir()
        (self.home / ".claude/skills").mkdir(parents=True)
        (self.home / ".claude/skills/de-ai").symlink_to(old)
        self.assertEqual(self.run_install().returncode, 0)
        self.assertEqual((self.home / ".claude/skills/de-ai").resolve(), SKILL_DIR.resolve())
        self.assertEqual(list(old.iterdir()), [])

    def test_real_directory_refuses_without_writing(self):
        (self.home / ".codex/skills/de-ai").mkdir(parents=True)
        result = self.run_install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refusing", result.stderr)
        for root in self.ROOTS:
            with self.subTest(root=root):
                self.assertFalse((self.home / root / "de-ai").is_symlink())


if __name__ == "__main__":
    unittest.main()
