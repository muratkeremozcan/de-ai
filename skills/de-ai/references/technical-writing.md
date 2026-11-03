# Technical writing

Keep technical prose usable after the voice edit.
The reader must understand the behavior, condition, or action on the first read.
The carve-outs in `SKILL.md` and the PR contract in `pr-descriptions.md` still govern scope and output.

## Keep the meaning exact

- Use the actual names from the artifact or codebase for symbols, files, flags, commands, and UI controls.
  Repeat the same name for the same thing.
- Name the actor when the source establishes it and responsibility matters.
  Keep passive voice when the actor is unknown or irrelevant.
- Put a prerequisite or warning before the action it governs.
  Preserve the difference between a recommendation, a requirement, and a possibility.
- Place "only" beside the word or action it limits.
  Make the grouping of "and" and "or" explicit when more than one reading is possible.
- Give "it", "this", "they", and "which" a clear referent.
  Repeat the noun when two things could fit.
- Break up noun stacks and sentences that require rereading.
  Keep articles, verbs, and connecting words that carry the relationship.
- Write an instruction as a direct command with one action per sentence.
  Retain exact command syntax, output, and error text.
- Cut "simply", "easy", and "just" when they dismiss the reader's difficulty.
  Explain an unfamiliar acronym when this audience needs it.

## Match the document to the reader's task

For documentation, identify the purpose of the section being edited.
A README can contain several purposes in separate sections; preserve the requested scope of the edit.

| Purpose | What the reader needs |
|---|---|
| Tutorial | A concrete thing to build, ordered steps, and visible results along the way. |
| How-to | A task to complete, prerequisites, actions, and relevant branches. |
| Reference | Exact names, behavior, defaults, limits, and errors in a predictable order. |
| Explanation | A bounded why question, constraints, and supported trade-offs. |

Keep background out of a procedure when a short link supplies it.
In an RFC, distinguish the current behavior, proposal, and unresolved decision.
Use the source's actual values; flag missing defaults or expected results without inventing them.
For a PR description, apply the sentence checks and keep the BLUF and length rules in `pr-descriptions.md`.
For a message, apply the sentence checks and keep the audience's message length.

## Keep the layout useful

Use numbered steps when order matters and bullets for independent items.
Use sentence case for new headings and label tasks with an action.
Give links descriptive text that identifies their destination.
Keep code, paths, and identifiers in code font.
Preserve code fences, generated blocks, and existing conventions; a prose edit cannot change their contents to satisfy a style preference.
