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

Read `AGENTS.md` first. If it sets where decisions, terms, or plans live, or the rules for
writing them, follow it. The defaults below apply where it doesn't.

## Decisions → `DECISIONS.md`

Record a decision when losing its reason would plausibly cause repeated investigation, an
unwanted change, or the same argument again. Keep each entry proportional: one line for a
small choice, a paragraph for a big one.

Counts:

- "SQLite, not Postgres: one user and nothing to operate. Rejected: Postgres, because
  running a server isn't worth it at this scale." (a trade-off)
- "No multi-monitor support for now." (an explicit no)
- "Screenshots never leave the machine; OCR runs locally." (a constraint the code can't
  show)

Doesn't count: picking between equivalent libraries, renames, formatting, routine bug
fixes, or anything the code or a commit message already explains.

Entry format, newest at the bottom:

```markdown
## YYYY-MM-DD: <decision in a few words>

<What was decided and why.> Rejected: <alternative> because <reason>.
```

Create `DECISIONS.md` the first time there is an entry. If an entry outgrows a paragraph,
move it to `docs/decisions/NNN-slug.md` and leave a one-line entry pointing at it. When a
decision is overturned, edit the old entry to say "Superseded by <date entry>" rather than
deleting it, so the rejected path stays visible.

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
