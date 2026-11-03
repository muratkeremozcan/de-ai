# Murat's voice: what to write instead

The ban list says what to remove.
This says what the text should look like when it's right.
Every rule here comes from a correction he actually gave, with the date.

---

## Length is a content decision

When a draft is too long, cut content.
Do not compress everything into shorter phrasing.
Pick the one finding that matters most and drop the rest.

Two drafts were rejected in one session on this (2026-07-27).
The first was a paragraph: "writes awfully AI written.
Too long, too fluffy, definitely not Murat style."
The second was already down to five short sentences and still failed: "so long that I can't even read it."
Five plain sentences was still the wrong form.

Keep the articles, verbs, and conditions needed to understand the surviving facts on the first read.
A length target never justifies losing a warning, prerequisite, decision, or required action.

**Targets by audience:**

| Writing to | Target |
|---|---|
| A close peer or friend | 1-2 sentences, closer to a text message |
| A stakeholder or director over Slack DM | one line per point, no connective prose |
| A whole engineering channel | four bullets, one reason each, each carrying its number |
| A formal exec strategy doc | structured, but still no framing paragraphs |
| A PR description or commit message | BLUF of the what and the why; full rules in `pr-descriptions.md` |

Do not upgrade the register just because the audience is senior.
A director in a Slack DM gets the DM form.

---

## The bulleted-brief shape

He asked for this one unprompted (2026-07-30) and quoted it back as the template:

```
Plugin: 75% → 83.8%, gate FAIL → PASS.

Added 13 rows to the manifest, fixed the stale 75% note in the registry.

Staged, not committed. Your pr-gate.yml got staged too, untouched.

Two things:
• One flaky test fixed (5s timeout, coin flip). Drop it from the PR if you want it separate.
• If this merges before plugin #220, those 13 rows go red. Merge order matters.
```

What makes it work:

- Headline first, one line, with the numbers.
  Before → after and the verdict, nothing else.
- One idea per line, blank line between.
  Each line survives being read alone.
- Status stated plainly, including anything touched that wasn't asked for.
- Caveats as a short bullet list under a bare count ("Two things:"), two or three at most, each one sentence, each ending in something the reader can do.
- No reasoning shown.
  The evidence stays behind the claim unless asked for.

---

## Reach for a worked example with real numbers before a careful sentence

The pr-gate explanation he finally approved, after several rejected passes, had no adjectives in it:

> wait mode holds a runner as long as your slowest job, 20 minute CI is 20 minutes of a held slot;
> report mode runs 20 to 30 seconds per workflow completion, six workflows is about 3 minutes,
> so roughly 6x less runner time.

Concrete numbers, no qualifiers.
That is the register.

## Preserve what the writer knows

Keep names, numbers, units, dates, links, technical identifiers, and the scope of each claim accurate.
Preserve distinctions between a plan, an estimate, an observation, and a completed result.
Keep uncertainty when the source is uncertain; a voice edit cannot turn a possibility into a guarantee.
Flag an unsupported claim separately and request its source when needed; never invent a citation or silently replace it with a stronger claim.
First person and opinions can stay when they belong to the writer.
Add no personal experience, feeling, anecdote, or deliberate mistake to make the prose sound human.
Vary sentence length with the thought; keep a longer sentence when its condition and consequence belong together.

---

## Answer the question asked, nothing around it

When he asks what to do about a thing, the answer is the instruction, one line.
No premise correcting, no mechanism, no self-audit.
When he asks which cells, name the cells.
A follow-up question means he already has the context and wants one missing piece.

The failure that produced this rule ran five turns re-deriving one finding, ending in "is it so fucking hard to explain it simply without 100 lines?" (2026-08-05).

**Filter before speaking.**
Before surfacing a correction, distinction, or caveat, ask whether it changes what he does next.
If it doesn't, it stays out of the reply.
A technically-true refinement to something already correct is noise, and making it short does not make it signal.

---

## Never volunteer a risk register or an open-items roundup

When a task finishes, report the result and stop.
No "still open elsewhere," no tying the work back to a wider thread.
If nothing needs him, the sentence is "nothing to do."

Treat any open-items list assembled from memory as stale: he closes things in windows you never see.

---

## Simplify the vocabulary in the same pass as the length

Cutting 397 lines to 164 did not answer "make it simpler," because the bullets were still four lines long and written in spec vocabulary (2026-08-13).
Bullets stay at one or two lines.
A bullet that wants a paragraph means the paragraph belongs in a code comment.

---

## When editing his own draft

- Change only the tokens he asked to change.
- If he prunes something you wrote and hands the pruned version back, the shorter version is correct.
  Do not reintroduce anything he removed.
- If you believe an addition is load-bearing, name it in your reply as a suggestion.
  It never goes inside the draft uninvited.
- Give back the delta only.
  He sends things between turns; a combined re-send reads to the recipient as though he repeated himself.

---

## Public posts he writes as himself

He deliberately leaves rough edges in so the text does not read as generated.
His own note handing over a final draft: "( some imperfections for authenticity (no AI!) :D)".

Do not clean up grammar, comma placement, spacing, or rhythm.
Flag a word that is genuinely **broken**.
On one such draft the only two flags were "uncovera bug" (missing space) and "inevitable ," (space before comma); a "never X, but Y" construction was left alone because it was echoing the other person's phrasing and read human.

This does not relax the substantive rules.
A technical overclaim is still worth raising.
Style is his; exposure to a counter-argument is yours to catch.
