---
name: grill-with-docs
description: Grill the user about a plan or design and record decisions and domain terms in the project's docs as they settle. Use when the user says "grill with docs" or wants a design interview that leaves a written record.
disable-model-invocation: true
---

# Grill with docs

Adapted from Matt Pocock's `grilling` and `domain-modeling` skills (MIT,
github.com/mattpocock/skills).

Run the `grill-me` skill. While it runs, write down each answer the user confirms **as it
settles**, not in a batch at the end: a session can be cut off at any point.

Read `AGENTS.md` first. If it sets where decisions, terms, or plans live, their budgets,
or the rules for writing them, follow it. The defaults below apply where it doesn't.

## Decisions → `DECISIONS.md`

The test for an entry: **without it, would a new agent plausibly do the opposite, or
spend real time finding out why?** If not, don't write it. Include what was rejected and
why: that's the part an agent would otherwise retry.

Counts:

- "SQLite, not Postgres: one user and nothing to operate. Rejected: Postgres, because
  running a server isn't worth it at this scale." (a trade-off)
- "No offline mode for now." (an explicit no)
- "User data stays in the EU region; the contract requires it." (a constraint the code
  can't show)

Doesn't count: equivalent library picks, renames, formatting, bug fixes, and anything the
code or a commit message already explains. A parameter's value is a comment next to the
parameter, unless it is coupled to other limits a new agent would break. A rule a test
enforces keeps its entry when the reason would be re-argued; the test preserves the
behavior, not why it was chosen.

Entry format, newest at the bottom:

```markdown
## YYYY-MM-DD: <decision in a few words>

<What was decided and why.> Rejected: <alternative> because <reason>.
```

An index entry is at most five lines. If a decision needs more, the index keeps a
two-line summary and the rest goes in `docs/decisions/NNN-slug.md`. Create `DECISIONS.md`
the first time there is an entry. When a decision is reversed, replace the old entry's
body with "Superseded by <date entry>" and keep its heading, so the rejected path stays
visible. Two entries must never disagree without one saying it's superseded.

## Terms → `GLOSSARY.md`

Only when a term is specific to this project and has been, or would easily be, confused:
the user and the code disagree, two words name one thing, or one word names two things.
Challenge it in the grilling ("you said X, the code calls it Y; which is it?"), then write
it.

```markdown
**Term**: what it is, in one or two sentences. _Avoid_: other words for it.
```

No implementation details, no general programming concepts. Create `GLOSSARY.md` the
first time there is a term.

## Direction → `ROADMAP.md`

If the grilling changes the project goal, what "done" means, or what comes next, update
`ROADMAP.md` in place. Don't append a history; the old version is in git.

## Shape → `ARCHITECTURE.md`

If the grilling settles a module boundary or a rule about what must not call what, put it
on the architecture page. One page; if it exists, edit it in place.
