# Wiring de-ai into cto-filter and communication-filter

Both filters live in their own repository, `muratkeremozcan/cto-filter`, and are installed into the same skill and agent discovery directories as `de-ai`:

- `skills/cto-filter/SKILL.md`
- `agents/communication-filter.md`

Neither filter vendors a copy of `de-ai`.
They read it through the installed path below, so `de-ai` has to be installed for either filter to run its voice layer.

## What the wiring is

`cto-filter` ends with this layer, after the executive gates, signal placement, and its own filter-specific voice checks:

```markdown
## De-AI pass

After the gates pass and before returning the draft, run the `de-ai` skill over the text.
Load `~/.claude/skills/de-ai/references/ai-tells.md` and
`~/.claude/skills/de-ai/references/murat-voice.md` and apply all four passes: tells, bloat,
voice, line structure. Those two files own the dash, antithesis, slogan, label-colon,
blockquote, and formatting rules, so this skill does not restate them.

Two things this filter has gotten wrong before, so check them explicitly on the way out:
- Tightening a soft offer must not introduce calendar-bot phrasing. "happy to pair if useful"
  became "want to grab 30 minutes this week?" and that was worse. See tell 5.
- The draft must come back at the writer's length or shorter, unless missing evidence requires
  a compact addition. This filter adds structure; structure is not a licence to add lines.

Fold the tells found into the gate results as one line with the count. Any unfixed tell makes
the verdict REVISE.
```

Its inline voice-pass list keeps only the checks `ai-tells.md` does not cover: owner naming, `guess`/`hope`/`should`, peer-message length, and unsupported claims.
The tell rules live in `ai-tells.md` alone, so a change there reaches both filters.

`communication-filter` preloads `cto-filter` through its `skills:` frontmatter and inherits the layer.
Its output contract adds one section:

```markdown
Report the de-AI pass as its own section: the count of tells removed, and the three most
significant ones by name (e.g. "3 removed: dash connector, label-colon opener, scheduling phrase").
Return the final text as plain text with no blockquote gutter.
```

## Why the de-AI pass runs last

The positioning gates rewrite sentences to satisfy Priorities and Approval Boundary, and rewrites reintroduce tells.
A de-AI pass running first would be undone.

The known failure of that filter gets a named check on the way out: on 2026-08-13 it tightened a soft offer ("happy to pair if useful") into calendar-bot phrasing ("want to grab 30 minutes this week?").
Tightening is exactly when that register gets introduced.
