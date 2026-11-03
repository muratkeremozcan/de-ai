# de-ai

A skill that strips AI tells from writing, prunes it hard and rewrites it in Murat's voice.
PR descriptions get a BLUF of the what and the why, no testing section and no tool attribution.

- `skills/de-ai/SKILL.md`: the entrypoint, with its carve-outs, four passes and output contract.
- `skills/de-ai/references/ai-tells.md`: the ban list of words, sentence shapes, structure and formatting.
- `skills/de-ai/references/murat-voice.md`: his recorded corrections and the shape to write in.
- `skills/de-ai/references/technical-writing.md`: technical clarity checks and documentation purposes, loaded for technical prose.
- `skills/de-ai/references/pr-descriptions.md`: PR description and commit message rules.
- `skills/de-ai/references/integration.md`: how `cto-filter` and `communication-filter` call this skill as their voice layer.
- `skills/de-ai/evals/triggers.json`: trigger queries for future evaluation; these are separate from the contract tests.
- `scripts/install.sh`: links the skill into each host's discovery folder.
- `docs/source-provenance.md`: where the skill came from.
- `docs/upstream-comparison.md`: the Unslop and technical-writing comparison and adoption decisions.

## Install

`scripts/install.sh` links the skill into the Claude, Agents, Codex and Gemini discovery folders under `$HOME`.
It checks all four destinations first and writes nothing when any of them is a real file or directory.
It then replaces existing symlinks, creates missing folders, and exits nonzero on any failure:

```bash
bash scripts/install.sh
```

## Tests

```bash
uv run --with pyyaml python -B -m unittest discover -s tests -v
```

The tests parse the frontmatter as YAML and check it against host limits.
They check that every reference the skill names exists inside the skill and that `SKILL.md` reaches each one.
They check the skill's own files against two of its rules: no dash clause connectors, and one sentence per line.
`ai-tells.md` quotes the banned forms as examples, so the dash check skips it and the line check skips its blockquotes.
Each check also runs against fixtures it must reject.
`scripts/install.sh` runs against temporary home folders: a fresh one, one with an old symlink, and one with a real directory in the way.
