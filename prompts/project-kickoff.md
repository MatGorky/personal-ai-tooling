# Project Kickoff Template
 
Fill the `<<>>` blanks. Delete anything that doesn't apply. If it's longer than a
page, you're padding.
 
---
 
We're in the `<<planning | design | implementation | review>>` phase.
Out of scope right now: `<<what you don't want it doing yet>>`.
 
**Role:** `<<Role for you to assume>>`

**Goal:** `<<what we're building, 2–3 sentences>>`
 
**Why:** `<<the real motivation — business case, constraint you're escaping,
learning goal. This is what lets you make sensible calls on the hundred things I
didn't think to specify.>>`
 
**Constraints:** `<<budget, stack, timeline, team skill, what this has to become
later>>`
 
**Facts the work depends on:** `<<the numbers or inputs without which any output
is invented. Mark UNKNOWN where you don't have them.>>`
`<<the one classification that forks the whole design — commit to it and justify
it before designing anything>>`
 
**Output:** `<<list the files you want. Names and one-line purposes. Not
schemas.>>`
 
**How to work:** Decide, don't hand me options — record rejected alternatives and
what it'd cost to reverse them. Assume rather than ask unless the answer changes
the shape of the work; log what you assumed and what breaks if it's wrong. Mark
any number you can't derive as an estimate, with its basis.
 
**Cover these or I'll get burned later:** `<<what would a team you haven't talked
to yet veto? legal, security, data handling, approvals and quotas with long lead
times>>`
 
**Include the case against this.** `<<what's the boring alternative, priced
fairly? under what conditions is the right answer "don't build it"?>>`
 
---
 
## Add only if
 
| Situation | Add |
|---|---|
| Spans multiple sessions | "Read `STATE.md` first, rewrite it last." Nothing more. |
| Genuinely parallel subtasks | Assign each agent exclusive write access to specific files. Never two agents on one file. Decompose by artifact, not by topic. |
| You're new to the domain | "Teach me as you go — sequenced, ordered by what unblocks the work soonest." |
| You'll defend this to someone | The case-against becomes mandatory, not optional. |
 
## Belongs in the repo, not the prompt
 
Acceptance criteria, decision records, session state, conventions. These are
artifacts you maintain — the prompt points at them. Keep `AGENTS.md` short:
build and test commands, project layout, what's off-limits. Detail goes in
referenced files, loaded on demand.
 
Skeletons for `AGENTS.md`, `STATE.md`, and ADRs are in
`project-kickoff-prompt-template.md`.
 
## Pre-flight
 
- [ ] Phase boundary stated
- [ ] The *why* is there
- [ ] Load-bearing facts supplied or marked `UNKNOWN`
- [ ] Output files named
- [ ] No hedging in the instructions (save it for the questions)
- [ ] Nothing included that the model would do anyway