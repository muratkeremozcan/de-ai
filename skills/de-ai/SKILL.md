---
name: de-ai
description: Strip AI tells from writing, prune it hard and rewrite it in Murat's voice. PR descriptions get a BLUF of the what and the why, no testing section and no tool attribution. Fires on "de-ai this", "de-AI it", "de-ai the PR", "does this sound AI", "make this sound human", "murat-ify this", or before posting any PR description or sending any human-facing text. Also runs as the voice layer inside cto-filter and communication-filter.
---

# de-ai

Take any draft, remove what makes it read as machine-written, and put it back in Murat's actual register.
Two jobs, in this order: kill the tells, then cut the bloat.
A third job runs at the layout level: lines break where sentences end.

## Step 0: check the carve-outs first

When either of these is true, open the reply with `SKIP` and name the carve-out.

- **The reader is another LLM.**
  Handoff briefs, prompts, agent instructions, machine-to-machine specs.
  The audience does not register an AI tell, so cleaning it is wasted work.
  His call, 2026-08-03: "doesn't matter, those are handoffs to other LLMs."
  Say so in one line and stop.
- **He wrote it himself and it is a public post.**
  LinkedIn, X, blog comments.
  He leaves rough edges in on purpose so it does not read as generated.
  Fix only what is genuinely **broken** (a missing space, a doubled word, a factual overclaim).
  Grammar slips and informal style are his; leave them out of the list and out of the post.
  After the verdict line, list each broken span with its fix, one line each, then give the full post with only those spans changed.

One more limit applies everywhere: **a draft he wrote is the spec.**
If he hands you his own text and asks for a specific change, change only that.
Do not restructure, do not add a line, do not reorder the close.

A PR description is human-facing even though bots read it too, so neither carve-out covers it.

## Step 1: read the references

Load these before editing anything.

- `references/ai-tells.md`: the universal ban list of words, sentence shapes, structure, and formatting.
- `references/murat-voice.md`: his own recorded corrections, and the positive shape to write in.
- `references/pr-descriptions.md`, when the text is a PR description or a commit message.
  Its shape, length targets and delete list override the general targets in `murat-voice.md`.

## Step 2: four passes over the text

Run them separately.
A single combined read misses things; the antithesis rule in particular has survived two "careful" drafting passes and needed a dedicated re-read both times.

1. **Tells pass.**
   Grep the draft for every banned construction in `ai-tells.md`.
   Dashes as clause connectors, the antithesis in every connector form ("not", "never", "rather than", "instead of", "over", "no longer"), label-colon openers, slogan lines, scheduling phrases, the tell vocabulary.
   Fix each one in place.
   Every antithesis fix **deletes the rejected clause**.
   A reworded connector counts as unfixed, and "never" is the swap that keeps getting shipped as if it were a repair.
2. **Bloat pass.**
   Cut anything the reader already knows, any sentence that asserts significance without showing it, any closing roundup, any caveat that does not change what the reader does next.
   Then run the delete test on every line that is left: would the reader miss it?
   If not, it goes.
   When he wrote the draft, the target is his length or shorter.
   When a model wrote it, expect half the length or less; a rewrite longer than that means the pass stopped early, so run it again.
   He had to follow nearly every run with "prune further" until 2026-10-29.
   The first version you hand back is the pruned one.
3. **Voice pass.**
   Simplify vocabulary as well as length.
   A short sentence made of jargon is still wrong.
   The test is whether it survives being said out loud at a whiteboard.
4. **Line-structure pass.**
   One complete sentence per line; never wrap mid-clause to hit a line length.
   When a sentence must break, break after punctuation (period, comma, semicolon, colon) so every line ends on the mark and no line opens mid-thought.
   Applies to prose and to code comments alike.
   Never reflow code inside fences, table rows, URLs, or frontmatter, and leave markdown hard breaks (two trailing spaces) intact.
   No pass changes text inside a code fence, its comments included; when a fenced comment has a tell, mention it in the reply and leave the fence as it is.
   Rendered markdown looks the same either way; what changes is the diff and where a review comment lands.

On any draft longer than a page, run pass 1 a second time at the end.
Rewrites reintroduce the dash and the antithesis; that has happened three times on record.
On the second pass, read every sentence you edited in pass 1 and check the rejected half is gone from the page; a stronger negation in its place counts as unfixed.

## Step 3: hand it back

- **Plain text.**
  No `> ` blockquote gutter; he has to strip it by hand before pasting.
- **PR descriptions and commit messages go inside one ```` ```markdown ```` fence**, so the raw markdown copies intact.
  When the target is a live PR, write it back yourself as `pr-descriptions.md` describes.
- **The delta only.**
  If the conversation is already in flight, give the new part alone.
  Assume everything earlier already went out.
- **Then a short list of what you cut**, three bullets max, one line each.
  Skip it if nothing interesting was cut.

## Verdict line

Open the reply with one of these, then the rewritten text.

- `CLEAN`: no tells found, nothing worth cutting.
- `FIXED (n)`: n tells removed, rewrite below.
- `SKIP`: a carve-out applies; name which one.
  A public post then gets its fixes and the full post, as Step 0 says.

## Running as a layer inside another filter

`cto-filter` and `communication-filter` call this as their voice layer.
When invoked that way, skip the verdict line and return the fixed text plus the list of tells found, so the calling filter can fold it into its own verdict.
See `references/integration.md`.
