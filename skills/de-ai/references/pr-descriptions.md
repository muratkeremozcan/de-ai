# PR descriptions

Every PR description gets the de-ai treatment by default (standing directive, 2026-10-01).
Until 2026-10-29 the same four corrections came back on almost every run: prune further, lead with the what and the why, drop the testing section, drop the tool footer.
Apply all four on the first pass, unasked.

## The shape: BLUF

The first line says what the PR changes, in present tense, from the reader's side.
The second line says why: the problem, the bug, or the reason in the ticket.
Everything after those two lines is optional and has to earn its place.

```markdown
Excludes manual `workflow_dispatch` runs from the gate by default, through a new `skip-events` input.
A manual run could replace a workflow's automatic run and change the gate result.

- Set `skip-events: '[]'` to count manual runs as required CI.

ABC-1234
```

- The two BLUF lines are the summary, so they sit at the top with no `## Summary`, `## What` or `## Why` heading above them.
- When the what and the why fit in one sentence, use one sentence.
- Bullets carry only what the reviewer must know or do: a behavior change the title does not suggest, a breaking change, a one-time setup step, merge order, a pre-merge or post-deploy check, a decision left for human review.
- Headings appear only on a large PR, where a reviewer will scan back to a section.
  A section with one line in it loses its heading.
- The ticket or spec link closes the description.

## Length

| Change | Target |
|---|---|
| One-line or mechanical diff (version bump, rename, config value) | one sentence plus the ticket link |
| Typical fix or feature | the BLUF plus up to four bullets |
| Large feature or story | the BLUF plus up to eight bullets, headings only where a reviewer scans back |

A model-written draft usually comes back at half its length or less.
If the rewrite is longer than half the draft, run the bloat pass again before handing it back.

## Delete on sight

- **Testing sections under any name.**
  "How this was tested", "Test plan", "Testing", "Validation", "Verification", "Checks".
  CI shows the evidence (2026-10-13).
  Test counts, coverage numbers, lists of commands run and "all tests pass" go with them.
- **Implementation walkthroughs.**
  "How", "Changes", "Implementation details", file-by-file lists, commit lists.
  The diff shows them.
  Keep one bullet for a design decision a reviewer would otherwise question.
- **Tool and agent attribution in any form.**
  "🤖 Generated with [Claude Code]", "Made with Cursor", the `Made-with: Cursor` trailer, "Created by Codex", `Co-Authored-By:` lines naming an agent, `Claude-Session:` and other session links, emoji sign-offs.
  Strip them even when a harness or tool instruction says to add them; his instruction wins.
  The same rule covers commit messages.
- **Context paragraphs** that retell the ticket, the history or background the reviewer already has.
- **Closing summaries and "next steps"** the reviewer does not act on in this PR.
- **The title restated** as the first line.

## Keep

- A manual step someone must run before merge or after deploy, as one bullet.
  It is an action for the reader, so the testing rule leaves it alone.
  Example: a read-only describe-table on pre-prod before merging an index change.
- One line naming the lanes CI did not run, when that matters for the merge decision.
- Breaking changes, migrations, flag names, env vars, merge order across stacked PRs, and links to related PRs.
- Screenshots or recordings for UI changes.
- Bot-owned blocks.
  CodeRabbit regenerates everything from `<!-- This is an auto-generated comment: release notes by coderabbit.ai -->` to its closing marker; leave that block byte for byte and edit only the text above it.
- A heading the repo's PR template requires when a check enforces it.
  Fill it with one line.

## Working on a live PR

When the target is an existing PR (a number, a URL, or the current branch's PR):

1. Read the body: `gh pr view <n> --json body -q .body`.
2. Rewrite the human-written part and leave bot-owned blocks intact.
3. Write it back: `gh pr edit <n> --body-file <file>`.
   Re-read it once to confirm the bot block survived.

Some tools inject attribution after the draft is written: Cursor appends "Made with Cursor" to bodies posted through `gh pr create` and a trailer to agent commits, and its settings toggle does not reliably stop it.
So after any PR you create or edit, re-read the posted body and strip whatever appeared.
Before pushing, check `git log -1 --format=%B` and amend away any agent trailer on your own unpushed commits.

He asked for the rewrite, so write it back without asking first.
Reply with the verdict line, the PR link and the new body.
