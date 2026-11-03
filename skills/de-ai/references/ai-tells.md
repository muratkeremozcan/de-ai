# AI tells: the ban list

Each entry is the construction, why it reads as generated, and what to write instead.
The first six are Murat's own recorded corrections and carry the most weight; the rest are the general tells that show up in any model's prose.

---

## 1. Dash as a clause connector

**Banned:** joining two clauses with `—` or with a spaced `-`.

> Config drift is the real cost — every service re-solves it.

**Fix:** colon when the second clause explains the first, semicolon when both stand alone, otherwise two sentences.

> Config drift is the real cost: every service re-solves it.

Hyphens inside real compound words are fine (long-term, well-tuned).
A bare `-` as a table's "no value" placeholder is fine.
Arrows in status lines are fine (`75% → 83.8%`).

**This one does not survive a rewrite.**
After any edit pass, grep the output for `—` and for ` - ` again before calling it done.

---

## 2. Negation-then-correction antithesis

**Banned:** any sentence where one clause exists only so it can be rejected.
Wording varies; the shape is what gives it away.
Every one of these is the same construction:

> That's not management, it's architecture.
> That's architecture, never management.
> It isn't because the tests are slow. It's because the runner is held.
> **Routes past the menu, not the skill.**
> This is visible now, rather than theoretical.
> We're fixing the model instead of arguing about blame.
> Config is owned in one place, no longer scattered per service.
> We want correctness here, over raw speed.

**The test, applied to every sentence:** does a clause name something only to deny it?
If yes, the sentence gets rewritten.
The connector word is irrelevant to that test.

Surface forms, for grepping.
Treat the list as incomplete; a form missing from it is still banned when the shape matches.

`not X, it's Y` · `it's not X, it's Y` · `X, not Y` · `X, never Y` · `always X, never Y` · `X rather than Y` · `X instead of Y` · `X as opposed to Y` · `X over Y` · `X, no longer Y` · `far from X, it's Y` · `anything but X` · the same pair split by a full stop (`That's architecture. Never management.`)

**Fix:** delete the rejected half and keep the affirmative.
Then reread what is left.
If the affirmative only made sense against the thing you deleted, rebuild the sentence from the underlying fact.

> That's architecture.
> The runner is held for the whole job.
> **Skips the menu, keeps the activation.**
> Now we're watching it happen.
> We're fixing the model.
> Config is owned in one place.

### Swapping the connector is not a fix

His correction, 2026-08-25: "We did 'It is x, not y', now it's replacing that with 'never'.
So lame."
A pass had turned `X, not Y` into `X, never Y` and scored itself clean, because the banned string was gone.
The construction was untouched.
Escalating to a stronger negation reads worse than the original: emphatic denial of a claim nobody made is exactly the register a model produces.

The rejected clause gets deleted.
**If the edited sentence still contains Y in any form, the edit failed.**
Rewriting `not` as `never`, `rather than`, `over`, `no longer`, or as a full stop leaves the same sentence wearing a different word.

A contrast survives only when both halves are concrete and load-bearing: a checklist's actual pass/fail state, a real before/after with numbers, a decision record naming the option that was turned down and why.
If the negated half restates something the surrounding sentence already said, cut it.

This is the single highest-frequency tell in long documents.
`rather than` and `instead of` are the two most likely to survive a manual read, and `never` is the one most likely to be introduced *by* the fix pass itself.
One ~160-line doc came out with roughly 20 instances of the `not/it's` form alone.
**After the tells pass, grep separately for** `not`, `never`, `rather than`, `instead of`, `as opposed to`, `no longer`.
A check for "not" and "but" alone misses the family.

---

## 3. Label-colon opener

**Banned:** opening a sentence, paragraph, or message with a short noun-phrase label plus a colon that announces what is coming.

> Bottom line: the gate passes now.
> Why it exists: the runner was being held.
> Quick thing worth flagging: two tests are flaky.

**Fix:** start with the content.

> The gate passes now.
> The runner was being held.
> Two tests are flaky.

---

## 4. Slogan sentence

**Banned:** the clipped aphoristic mic-drop line.
His words: "this, I don't speak like this."

> Config's the pole.
> Speed is a feature.
> The gate is the contract.

**Fix:** write the full sentence a person would actually type in a hurry.

> Config is what everything else waits on.

If the line would work printed on a poster, rewrite it.

---

## 5. Corporate scheduling register

**Banned:** anything that sounds like a calendar bot offering to meet.

> Want to grab 30 minutes this week?
> Let's sync on this.
> Happy to hop on a call.
> Does that work for you?

**Fix:** offer it the way he'd type it.

> happy to pair on this whenever works
> lmk if you want to jam on it
> I'll take the migration, ping me if you want to walk through the rest

Never a specific-duration-plus-question-mark unless he asked for one.
This tends to get introduced *by* a filter pass that was tightening something soft, so check for it again after any tightening.

---

## 6. Self-narration and framing paragraphs

**Banned:** a paragraph or opener whose only job is to tell the reader how to feel about the facts that follow, or to claim a track record.

> Everything below is one coherent plan, not five disconnected projects.
> I've done this exact kind of migration before:
> A few things before this goes to the director:
> This demonstrates strategic thinking across the org.

**Fix:** cut it.
Lead with the fact and let the reader draw the conclusion.

> Six services migrated in February under one epic.

Before adding any framing sentence, ask whether it contains a fact the reader does not already have.
If not, it goes.

---

## 7. Tell vocabulary

Use the plain word when it preserves the meaning.
Keep literal technical terms, identifiers, and quoted wording accurate, including a word listed here when it has a precise domain meaning.
The left column is what a model reaches for; the right is what a person says.

| Model word | Say |
|---|---|
| leverage | use |
| utilize | use |
| delve into | look at |
| robust | solid, or a number |
| seamless | works, no setup |
| comprehensive | complete, or drop it |
| landscape, realm, space | the actual noun |
| underscore, highlight | show |
| testament to | evidence of, or drop it |
| pivotal, crucial, vital | important, or drop it |
| navigate (a problem) | handle, deal with |
| foster, cultivate | build, grow |
| streamline | simplify, cut steps |
| holistic | whole, or drop it |
| in today's fast-paced world | drop the whole clause |
| it's worth noting that | drop it, state the note |
| importantly, notably, critically | drop it |
| that said, that being said | but, or a new sentence |
| at the end of the day | drop it |
| game-changer, unlock, supercharge | say what it does |
| ensure | make sure |
| facilitate | help, let |
| myriad, plethora | many, or the count |
| serves as, stands as | is |
| boasts | has |
| in order to | to |
| due to the fact that | because |
| significantly, dramatically, remarkably | the measured change, or drop it |

Same rule for the jargon register: a short sentence made of spec vocabulary is not simple.
"JavaScript loses digits above 2^53" is the target.
"The numeric value domain is enforced in two layers" is the failure.

---

## 8. Rule-of-three padding

**Banned:** the reflexive three-item list where two items or one carry the meaning.

> faster, cheaper, and more reliable
> It simplifies onboarding, reduces errors, and improves confidence.

**Fix:** keep the items that are actually true and load-bearing.
Two is usually the real number.

> 6x less runner time, and the flake went away

---

## 9. "Not only... but also" and its cousins

**Banned:** `not only X but also Y`, `X while simultaneously Y`, `both X and Y alike`, `more than just X`.

**Fix:** two facts, two clauses, no scaffold.

---

## 10. The closing summary paragraph

**Banned:** a final paragraph that restates what the reader just read, or ties the work back to a wider theme, or lists everything still open elsewhere.

> In summary, this change improves reliability across the board and sets us up well for the next phase of the rollout.

**Fix:** stop at the last real fact.
If nothing needs the reader, the sentence is "nothing to do."

---

## 11. Formatting tells

- **Bold on every other phrase.**
  Bold the number and the verdict; leave the rest plain.
- **Emoji bullets** and decorative section icons in professional writing.
- **A heading for every two sentences.**
  Headings are for things a reader will scan back to.
- **Perfectly parallel bullets of identical length.**
  Real notes are uneven.
- **A table where three bullets would do**, or prose where a table would do.
- **Hard-wrapped lines that split a sentence mid-clause.**
  Models wrap to a character budget; people break lines where sentences end.
  One sentence per line; when a sentence must break, the break lands after punctuation (period, comma, semicolon, colon).
  Same rule inside code comments.
  Never reflow code, table rows, URLs, or frontmatter to enforce it.
- **Blockquote gutters (`> `) on text meant to be copy-pasted.**
  Plain text, always.

---

## 12. Hedge stacking

**Banned:** `may potentially`, `could possibly help to`, `it seems likely that`, `generally speaking, in most cases`.

**Fix:** one hedge maximum, and only when the uncertainty is real and changes what the reader does.
Otherwise state it flat.
If you don't know, say you don't know.

---

## 13. Unsupported authority and significance

**Banned:** vague authority such as "experts agree" or "research shows" without an identifiable source, and claims such as "a milestone" with no stated consequence.
Trailing phrases such as "showcasing our commitment" often add a claim the preceding fact cannot support.

**Fix:** keep the observed fact and its supported consequence.
Name and link a source already available, or flag the evidence gap separately.
Keep a trailing phrase when it states a real condition or result, such as "preventing duplicate writes" when the mechanism supports that claim.

---

## 14. Synonym cycling and abstract metaphors

**Banned:** renaming one thing across a paragraph to avoid repetition, or dressing up an ordinary action with an abstract metaphor.
Calling one check a "gate", a "ratchet", and a "guardrail" makes the reader work out whether there are three checks.

**Fix:** use one name for each thing and the real symbol, flag, or command when it matters.
Use "move" for moving code and "shared library" for a library described as a "substrate".
Keep established domain terms such as a mathematical vector or a test harness when they identify the thing accurately.

---

## 15. False ranges

**Banned:** "from X to Y" when the endpoints imply a scale or progression that the facts do not establish.

**Fix:** name the actual items or scope.
Keep real ranges, including dates, versions, measured values, and a genuine sequence of steps.

---

## 16. Chatbot pleasantries and flattery

**Banned:** reflexive openers such as "certainly", flattery such as "great question", exaggerated agreement, and generic closers such as "I hope this helps".

**Fix:** begin with the answer and end with the last useful fact or action.
Keep a specific thanks, acknowledgment of impact, or real offer when it serves the relationship.
Tell 5 covers the wording of that offer.

---

## 17. Over-compression

**Banned:** dropping articles, verbs, or conditions until the reader has to decode the line.

> Parser rejects bad date → exit 2, no write.

**Fix:** keep a complete sentence with the behavior intact.

> The parser rejects an invalid date, exits with code 2, and writes nothing.

Compact status lines with clear before-and-after values remain useful, as tell 1 describes.
In explanations and instructions, spell out the relationship and keep the words that make it unambiguous.
