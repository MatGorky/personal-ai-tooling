---
name: project-init
description: Set up a project's working docs (AGENTS.md, ROADMAP.md, and DECISIONS.md when needed) so any agent can pick up the work without the history being retold. Use when starting a new project, or when an existing project has no clear direction or its state lives in the README or in chat.
---

# Project init

Sets up the small doc set every project of mine uses. The test it has to pass: **a fresh
agent, reading only these files, continues the work correctly without me retelling the
project's history.**

The doc set:

| File | What earns a place there |
| --- | --- |
| `AGENTS.md` | Commands, constraints the code can't show, and the rules for reading and updating the other docs. Every agent loads it. |
| `CLAUDE.md` | One line, `@AGENTS.md`, so Claude Code loads the same file. |
| `ROADMAP.md` | The goal and when it's done, Resume here, Now / Next / Later, Not doing. |
| `DECISIONS.md` | Only when there is a decision worth keeping. Created then, not up front. |

Nothing else up front. No glossary, ADR folder, plan files, or contributing guide until
something needs them; `grill-with-docs` and `checkpoint` create them when they do.

**Merge, never reset.** The templates below are for files that don't exist yet. When a
file exists, merge into it: keep working instructions, imports, and references. Running
init again on a project that already has these docs must not reset its roadmap, Resume
here, or decisions. Instructions that only one agent understands can stay in that agent's
own file (`CLAUDE.md`, `.cursor/rules`, ...) next to the `@AGENTS.md` import.

## 1. Read before asking

Read the README, the manifest (`pyproject.toml`, `package.json`, ...), any existing
`AGENTS.md` / `CLAUDE.md`, the docs folder, and `git log`. Derive the commands (setup,
run, test, lint), the layout, and the constraints. Never ask for something on disk.

## 2. Pin the goal

The goal is the part that can't be derived, and the part projects drift without. Use the
`grill-me` format (numbered questions in chat, each with your recommended answer) and
lead with a draft built from what you read.

Don't finish until both are concrete:

- **Goal**: what the project is for, in two or three sentences, including why.
- **Done when**: an observable condition. "Farms for an hour unattended and reports
  EXP/hour" is concrete; "a working bot" is not.

Also settle what's explicitly **not** being done. That list is what stops drift.

## 3. Find where state already lives

In an existing project, status, next steps, and decisions are usually scattered in the
README, an old `CLAUDE.md`, or plan files. List what you found and where it should move:

- Status and next steps → `ROADMAP.md`.
- Decisions with their reasons → `DECISIONS.md`, when losing the reason would plausibly
  cause repeated investigation, an unwanted change, or the same argument again.
- How to use the project stays in the README.

Show the user the list before moving anything out of an existing file.

## 4. Write the files

`AGENTS.md`:

```markdown
# <Project>

<One line: what this is.> Goal, current state and next step: `ROADMAP.md`.

## Commands

<setup, run, test, lint: exact commands>

## Constraints

<Rules the code can't show. Omit the section if there are none.>

## Testing

<The boundaries tests go through, what runs against real dependencies, what gets faked
and why, and which checks give confidence before calling something done.>

## Working on this project

- Start by reading **Resume here** in `ROADMAP.md` and the entry headings in
  `DECISIONS.md`. Before changing anything a heading covers, read that entry; don't retry
  a rejected approach without saying so.
- Write things down when they happen, not at the end: a settled decision goes in
  `DECISIONS.md`; a new blocker or an unverified claim goes in Resume here.
- Before stopping, rewrite Resume here so the next agent knows the next concrete action.
- **Decisions** are worth recording when losing the reason would cause repeated
  investigation, an unwanted change, or the same argument again. Not for equivalent
  library picks, renames, routine bug fixes, or anything the code or a commit message
  already explains. Format: `## YYYY-MM-DD: <decision>`, then what and why, then
  `Rejected: <alternative> because <reason>.` Past a paragraph, an entry moves to
  `docs/decisions/NNN-slug.md` and leaves a one-line pointer.
- **Plans** go in `docs/plans/<slug>.md`, and only when asked for or when the work can't
  be tracked in Now plus Resume here. When the work is done, record any decision it
  produced and delete the plan.
```

`ROADMAP.md`:

```markdown
# Roadmap

## Goal

<two or three sentences, including why>

**Done when:** <observable condition>

## Resume here

_Updated YYYY-MM-DD_

- **Next:** <one concrete action>
- **Blocked:** <what, and on what; or "nothing">
- **Unverified:** <claims made but not yet tested>

## Now

## Next

## Later

## Not doing
```

Keep Now / Next / Later as short lists of outcomes, not tasks. Get today's date at runtime.

If a `CLAUDE.md` with content already exists, move what applies to every agent into
`AGENTS.md`, keep anything Claude-specific, and add `@AGENTS.md` at the top.

The Testing section is project-specific: derive it from the existing tests and settle
the gaps in the grilling. Follow `test-craft` for how to write it, and its
"Taking over an existing project" steps when the tests are missing or unreliable.

## 5. Self-check

Re-read only the new files and write in chat what an agent would do next and what it
would get wrong. Fix the docs for anything it would get wrong. This only catches obvious
gaps; the real test is the first handoff to a fresh session, so say that in the report.

Then report what was written, what moved out of which file, and anything left as an open
question. Don't commit unless asked.
