---
name: checkpoint
description: Reconcile a project's docs with what actually happened in this session (Resume here, roadmap, decisions, plans), keep them inside their size budgets, and prune what has grown past them, so the next agent can continue. Use when the user says "checkpoint", is wrapping up or switching agents, or after a decision, blocker, or milestone.
---

# Checkpoint

Brings the roadmap, decisions, architecture page, and any plan files in line with the
session, and keeps them inside their budgets. It reconciles; it is not the only time
docs get written. `AGENTS.md` already tells agents to record decisions and blockers as
they happen, because sessions get cut off.

Read `AGENTS.md` first. If it sets where the docs live, their budgets, or the rules for
writing them, follow it. The defaults:

| Doc | Default location | Budget |
| --- | --- | --- |
| Roadmap | `ROADMAP.md` | Resume here under 20 lines; Now, Next, Later a few lines each |
| Decisions index | `DECISIONS.md` | prune past about 25 entries; an entry at most 5 lines |
| Decision detail | `docs/decisions/NNN-slug.md` | one page |
| Architecture | `ARCHITECTURE.md` | one page |
| Evidence | `docs/runs/<YYYY-MM-DD>.md` | no budget; it's a log |
| Plans | `docs/plans/<slug>.md` | deleted when the work ships |
| Glossary | `GLOSSARY.md` | terms that were actually confused |

A budget is a trigger to prune, not a quota: what survives is decided by the tests in
steps 4 and 5, never by the count, and reasoning that still governs is never shortened
just to fit. A doc far over its budget is not read, so it stops being true. If the
project has no roadmap at all, stop and suggest `project-init`.

## 1. Gather

Read the roadmap, the decisions index, the architecture page, and any plans. Then look at
what happened: this conversation, `git status`, `git diff`, and `git log` since the date
on Resume here. Base everything on what happened, not on what was planned.

## 2. Rewrite Resume here

Rewrite the whole section from scratch and update its date. Patching lines into the old
text is how it grows past its budget. Each line must be concrete enough that a fresh
agent can act without asking:

- **Next**: one action. "Working on auth" fails. "Callback works locally; add a test for
  expired tokens in `tests/test_auth.py`" passes.
- **Blocked**: what, and what it waits on. "Nothing" is fine.
- **Unverified**: claims made but not tested, one line each. If something was observed
  once on one machine, say so. Remove a line only when it's been verified or no longer
  matters.

Evidence stays out of Resume here: run IDs, measurements, counters, tables, and commands
to rerun go in the day's run log under `docs/runs/`, and Resume here links it once and
states the conclusion. "Live OCR verified at level 27 (run log, 2026-10-16)" is a Resume
here line; the 57 passes and 6 failures behind it are run-log lines.

One writer. In a multi-agent run, only the orchestrator, or the one session the user is
talking to, rewrites Resume here. Workers append their findings and evidence to the run
log and report them; they don't edit the roadmap. Several writers produce competing
accounts of what matters next.

## 3. Move the roadmap

Move items between Now / Next / Later to match reality, and remove finished ones. If the
work drifted from the Goal or touched something in Not doing, say so to the user instead
of quietly editing the Goal.

## 4. Record decisions

The test for an entry: **without it, would a new agent plausibly do the opposite, or
spend real time finding out why?** If not, it's a changelog line, and git already has it.
Include what was rejected and why: that's the part an agent would otherwise retry.

Counts:

- "SQLite, not Postgres: one user and nothing to operate. Rejected: Postgres, because
  running a server isn't worth it at this scale." (a trade-off)
- "No multi-monitor support for now." (an explicit no)
- "Screenshots never leave the machine; OCR runs locally." (a constraint the code can't
  show)

Doesn't count: equivalent library picks, renames, formatting, bug fixes, and anything the
code or a commit message already explains.

Two cases that look like they don't count but can: a parameter's value goes in a comment
next to the parameter, but its entry stays when the value is coupled to other limits a
new agent would break (a frame rate tied to hold timing and processing cost). A rule a
test enforces keeps its entry when the reason would be re-argued, because the test
preserves the behavior, not why it was chosen; the entry names the test.

```markdown
## YYYY-MM-DD: <decision in a few words>

<What and why.> Rejected: <alternative> because <reason>.
```

An index entry is at most five lines. If a decision needs more, the index keeps a
two-line summary and the rest goes in `docs/decisions/NNN-slug.md`. Create the index on
the first entry.

An entry states the decision as it stands now. When a decision changes, rewrite the entry
instead of appending "refined" or "amended" notes; git has the old text. When a decision
is reversed, replace the old entry's body with "Superseded by <date entry>" and keep its
heading, so the rejected path stays visible.

If a project-specific term was confused twice this session, add it to the glossary
(create it then): `**Term**: what it is. _Avoid_: other words for it.`

## 5. Prune

Do this whenever a doc is over its budget, and at least every few sessions. For the
decisions index, in order:

1. Resolve conflicts first. When two entries disagree, the newer governs: rewrite the
   older to what still holds, or replace its body with "Superseded by <date entry>". An
   agent must never have to work out which statement is current. This matters more
   than any line count.
2. Apply the test in step 4 to every entry. Entries that fail it are deleted; a bare
   parameter value becomes a comment next to the parameter.
3. Merge entries that are one decision told in pieces, under the newest date.
4. Shorten entries over five lines by moving the detail to `docs/decisions/`, never by
   cutting the reasoning.

Resume here over budget gets rewritten per step 2, with the evidence moved to the run
log. Now, Next, and Later over budget get their task-level items folded into one outcome
each. A glossary term is deleted only when the project no longer uses it; a term nobody
confuses anymore may be the reason nobody does.

Say in the report what was pruned and where it went, so the user can object.

## 6. Close or update plans

For each plan: if the work is done, close it; if it's still going, update it. A plan must
not contradict Resume here. A plan nobody asked for, for work that fits in Now plus
Resume here, gets folded into the roadmap and closed. A plan that holds acceptance
examples, exclusions, and failure cases agreed before implementation closes once the
tests written from them pass.

## 7. Delete safely

Before removing a finished roadmap item, a closed plan, a pruned entry, or any doc
section, check that nothing unique is lost. Git only keeps what was committed: if the
file is untracked, or `git status -- <path>` shows staged or unstaged changes, its
current contents are not in any commit. Move anything still useful (a decision, a gotcha,
a result) to its permanent place first.

Don't delete a section just because nobody read it recently. Delete what is obsolete,
duplicated, or fails the step 4 test; keep what would be expensive to rediscover, like a
recovery procedure needed twice a year.

## 8. Check for drift

- If the session changed commands, setup, constraints, or how things are tested, update
  `AGENTS.md` and the README to match. Keep `AGENTS.md` short; detail goes in the file it
  points at.
- If a module was added, split, or removed, or a boundary changed, update the
  architecture page. It stays one page.
- If a canonical file named under Patterns in `AGENTS.md` was changed, check it is still
  clean enough to copy from. If it isn't, point at a better one or say there is none.

## 9. Report

In chat: the new Resume here, decisions added, what was pruned and where it went, plans
closed, anything moved before a deletion, and anything you noticed but didn't change.
Don't commit unless asked.
