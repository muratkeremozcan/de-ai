# Unslop and technical-writing comparison

Compared on 2026-11-03 against the de-ai and cto-filter checkouts.
The [skills.rest listing](https://skills.rest/skill/unslop-poteto) points to `poteto/noodle`.
Lauren Tan's pstack plugin also publishes Unslop and technical-writing in `cursor/plugins`.
Its [plugin manifest](https://github.com/cursor/plugins/blob/ae5650febf4320793844c12c4adaa937f417f8da/pstack/.cursor-plugin/plugin.json) names Lauren Tan as the author.

## Source snapshots

Both repositories were cloned and their skill files read locally.
Links below pin the exact revisions inspected.

| Source | Revision | Local clone |
|---|---|---|
| [Original Unslop](https://github.com/poteto/noodle/blob/82d2921c52370f23f29086de81ccfb600939c037/.agents/skills/unslop/SKILL.md) | `82d2921c52370f23f29086de81ccfb600939c037` | `/tmp/de-ai-unslop-noodle-20261103` |
| [pstack Unslop](https://github.com/cursor/plugins/blob/ae5650febf4320793844c12c4adaa937f417f8da/pstack/skills/unslop/SKILL.md) | `ae5650febf4320793844c12c4adaa937f417f8da` | `/tmp/de-ai-poteto-pstack-20261103` |
| [pstack technical-writing](https://github.com/cursor/plugins/blob/ae5650febf4320793844c12c4adaa937f417f8da/pstack/skills/technical-writing/SKILL.md) | `ae5650febf4320793844c12c4adaa937f417f8da` | The same sparse clone, with `pstack` checked out. |

These are distinct versions of Unslop.
The noodle version has an explicit section about adding personality.
The pstack version adds concrete checks for abstract metaphors, active voice, dense sentences, and over-compression.
Technical-writing adds document purposes and sentence rules drawn from Diátaxis, Google developer style, Simplified Technical English, and Global English.
This comparison concerns those skills' instructions; it makes no claim of compliance with those external standards.

## Coverage before this change

| Area | Upstream coverage | Existing de-ai or cto-filter coverage | Change |
|---|---|---|---|
| Dashes, antithesis, filler, hedges, formatting | Both Unslop versions cover these. | de-ai already has stronger antithesis checks, four passes, and recorded corrections. | Retain the existing rules and extend the vocabulary examples. |
| Meaning and personality | noodle asks for opinions, first person, rhythm, and some mess. | de-ai preserves Murat's rough public posts and specific edits; factual fidelity is less explicit. | Keep supported opinions and rhythm; explicitly protect facts, uncertainty, and the writer's experience. |
| Unsupported authority | Both Unslop versions call out unnamed experts and reports. | cto-filter traces evidence; de-ai has general overclaim and filler checks. | Add a named tell and keep unresolved evidence gaps visible in cto-filter after editing. |
| Trailing significance claims | Both flag decorative phrases ending in an ing form. | de-ai cuts unsupported significance without naming this shape. | Distinguish a supported consequence from an unsupported interpretation. |
| Synonym cycling | Both use a single name for a single thing. | Plain vocabulary is covered; consistent names are implicit. | Add a check for renamed concepts and preserve actual technical identifiers. |
| False ranges | Both flag endpoints with no meaningful scale. | No explicit check. | Add the check with exceptions for genuine ranges and sequences. |
| Chatbot language | Both flag canned agreement and pleasantries. | Scheduling language and framing are covered. | Add direct checks for flattery and generic conversational closers. |
| Abstract jargon | pstack Unslop adds a specific metaphor rule. | de-ai rejects jargon broadly. | Name the failure while keeping accurate domain terms. |
| Over-compression | pstack Unslop protects full sentences and grammatical structure. | de-ai strongly targets half-length rewrites and endorses compact status lines. | Protect conditions, articles, verbs, and actions; keep clear numeric status lines. |
| Technical ambiguity | Technical-writing checks actors, modifiers, pronouns, noun stacks, and terminology. | cto-filter checks ownership; de-ai mainly checks voice and layout. | Add a conditional technical reference and load its sentence checks from cto-filter. |
| Documentation purpose | Technical-writing distinguishes tutorials, how-to guides, reference, and explanation. | No document-purpose guidance. | Apply purpose per section during an edit, including a mixed-purpose README. |
| PRs and integration | Technical-writing includes PRs and commits in its scope. | de-ai has specific BLUF, pruning, bot-block, attribution, and live-edit rules; cto-filter has evidence and ownership gates. | Retain these contracts and check that voice edits preserve the decision and completion state. |

## Adoption decisions

The new technical reference loads for technical prose.
Its documentation modes apply to documentation sections; chat messages retain the audience's existing length targets.
PR descriptions retain the dedicated BLUF contract, and the public-post and LLM carve-outs remain in force.
Trigger scope stays the same.
The de-ai description uses the standard "Use when" wording, with its existing phrases and contexts preserved.
The trigger queries in `skills/de-ai/evals/triggers.json` record positive cases and near misses for a future evaluation.

Several upstream choices conflict with the existing contracts or need narrower application:

- Murat permits colons and semicolons as clause connectors; his dash rule remains authoritative.
- His informal peer voice and compact numeric status lines are recorded preferences, so a universal idiom or arrow ban would erase useful voice.
- Code fences and bot-owned blocks are protected; upstream tab indentation and quote normalization cannot justify changing them.
- The noodle advice to add opinions and mess needs an authorship boundary because an editor could invent experiences or mistakes.
- Strict whole-document separation of documentation modes would turn a README edit into a restructure; section-level purpose preserves the requested scope.
- Sentence length is a readability judgment; mandatory word limits could split a condition from its consequence.
- Legitimate technical terms and meaningful ing phrases stay when they describe the mechanism accurately.

## Apply the rules to this repo

The old de-ai instruction required another pruning pass whenever a model-written rewrite exceeded half the draft's length.
It now treats half-length as a target and explicitly preserves facts, qualifications, and necessary instructions.
That closes the conflict between aggressive pruning and the new over-compression check.

The filter previously checked tells after its gates without explicitly checking whether that rewrite changed a decision or completion claim.
It now compares conditions, ownership, uncertainty, completion states, and the requested decision after the voice pass.
The shared technical reference supplies the same sentence rules to both skills.

For example, the sentence "If the source is uncertain, the rewrite may keep that uncertainty" must retain both the condition and the possibility.
A shorter sentence that promises certainty would change the claim.
An unsupported "experts agree" claim needs an evidence gap; a named source can be added only when it is available.

Repository contract tests check loading, references, house style, installation, and filter integration.
They do not measure rewrite quality, and no comparative model benchmark was run for this change.

## Loading cost and validation

The entry grew from 1,454 to 1,569 tokens, measured with Toolsmith's token counter.
Its description is 445 characters.
The technical-writing reference adds 587 tokens when technical prose needs it.
The existing pass explanations and correction history could move into a reference if reducing the entry's loading cost becomes a separate task.
These remain standalone skills with no new runtime dependency on pstack or BMad.

The repository checks pass: 22 de-ai tests, 13 cto-filter tests with the companion installed, Ruff, shellcheck for de-ai's installer, and whitespace checks.
Both skill entries pass Toolsmith's frontmatter check.
The generic BMad path scanner flags installed companion paths and the integration document's cross-repository example.
Those paths are part of the existing standalone integration contract; the repository tests validate that their targets exist.
All four installed host links resolve to the edited checkouts, including the new technical reference and license notice.

## Attribution

Both upstream repositories license this material under MIT, copyright 2026 Lauren Tan.
The license notice ships inside the skill in [NOTICE](../skills/de-ai/NOTICE).
The additions adapt selected ideas into de-ai's existing voice and filter contracts.
