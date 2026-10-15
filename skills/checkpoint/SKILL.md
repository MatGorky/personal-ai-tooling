---
name: checkpoint
description: Reconcile a project's docs with what actually happened in this session (Resume here, roadmap, decisions, plans), so the next agent can continue. Use when the user says "checkpoint", is wrapping up or switching agents, or after a decision, blocker, or milestone.
---

# Checkpoint

Brings the roadmap, decisions, and any plan files in line with the session. It
reconciles; it is not the only time docs get written. `AGENTS.md` already tells agents to
record decisions and blockers as they happen, because sessions get cut off.

Read `AGENTS.md` first. If it sets where the roadmap, decisions, terms, or plans live, or
the rules for writing them, follow it. The defaults are `ROADMAP.md`, `DECISIONS.md`, `GLOSSARY.md`, and
`docs/plans/`. If the project has no roadmap at all, stop and suggest `project-init`.

## 1. Gather

Read the roadmap, the decisions file if it exists, and any plans. Then look at what
happened: this conversation, `git status`, `git diff`, and `git log` since the date on
Resume here. Base everything on what happened, not on what was planned.

## 2. Rewrite Resume here

Rewrite the whole section and update its date. Each line must be concrete enough that a
fresh agent can act without asking:

- **Next**: one action. "Working on auth" fails. "Callback works locally; add a test for
  expired tokens in `tests/test_auth.py`" passes.
- **Blocked**: what, and what it waits on. "Nothing" is fine.
- **Unverified**: claims made but not tested. If something was observed once on one
  machine, say so. Remove a line only when it's been verified or no longer matters.

## 3. Move the roadmap

Move items between Now / Next / Later to match reality, and remove finished ones. If the
work drifted from the Goal or touched something in Not doing, say so to the user instead
of quietly editing the Goal.

## 4. Record decisions

Record a decision when losing its reason would plausibly cause repeated investigation, an
unwanted change, or the same argument again. Include what was rejected and why: that's the
part an agent would otherwise retry. Keep entries proportional: one line for a small
choice, a paragraph for a big one.

Counts:

- "SQLite, not Postgres: one user and nothing to operate. Rejected: Postgres, because
  running a server isn't worth it at this scale." (a trade-off)
- "No multi-monitor support for now." (an explicit no)
- "Screenshots never leave the machine; OCR runs locally." (a constraint the code can't
  show)

Doesn't count: picking between equivalent libraries, renames, formatting, routine bug
fixes, or anything the code or a commit message already explains.

```markdown
## YYYY-MM-DD: <decision in a few words>

<What and why.> Rejected: <alternative> because <reason>.
```

Mark an overturned entry "Superseded by <date entry>"; don't delete it. Create the
decisions file on the first entry. If an entry outgrows a paragraph, move it to
`docs/decisions/NNN-slug.md` and leave a one-line entry pointing at it.

If a project-specific term was confused twice this session, add it to the glossary
(create it then): `**Term**: what it is. _Avoid_: other words for it.`

## 5. Close or update plans

For each plan: if the work is done, close it; if it's still going, update it. A plan must
not contradict Resume here. A plan nobody asked for, for work that fits in Now plus
Resume here, gets folded into the roadmap and closed.

## 6. Delete safely

Before removing a finished roadmap item, a closed plan, or any doc section, check that
nothing unique is lost. Git only keeps what was committed: if the content never made it
into a commit (`git log -- <path>` shows nothing, or the file is untracked), move anything
still useful (a decision, a gotcha, a result) to its permanent place first.

Don't delete a section just because nobody read it recently. Delete what is obsolete or
duplicated; keep what would be expensive to rediscover, like a recovery procedure needed
twice a year.

## 7. Check for drift

If the session changed commands, setup, constraints, or how things are tested, update
`AGENTS.md` and the README to match. Keep `AGENTS.md` short; detail goes in the file it
points at.

## 8. Report

In chat: the new Resume here, decisions added, plans closed, anything moved before a
deletion, and anything you noticed but didn't change. Don't commit unless asked.
