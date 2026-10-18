---
name: project-init
description: Set up a project's working docs (AGENTS.md, ROADMAP.md, ARCHITECTURE.md, and DECISIONS.md when needed) so any agent can pick up the work without the history being retold. Use when starting a new project, or when an existing project has no clear direction or its state lives in the README or in chat.
---

# Project init

Sets up the small doc set every project of mine uses. The test it has to pass: **a fresh
agent, reading only these files, continues the work correctly without me retelling the
project's history.**

The doc set:

| File | What earns a place there | Budget |
| --- | --- | --- |
| `AGENTS.md` | Commands, constraints the code can't show, the testing approach, where patterns live, and the rules for reading and updating the other docs. Every agent loads it. | under 80 lines |
| `CLAUDE.md` | One line, `@AGENTS.md`, so Claude Code loads the same file. | 1 line |
| `ROADMAP.md` | The goal and when it's done, Resume here, Now / Next / Later, Not doing. | Resume here under 20 lines |
| `ARCHITECTURE.md` | Module map, data flow, and what must not call what. Written once there is code to map. | one page |
| `DECISIONS.md` | Only when there is a decision worth keeping. Created then, not up front. | prune past about 25 entries; 5 lines each |

Nothing else up front. No glossary, ADR folder, plan files, run logs, or contributing
guide until something needs them; `grill-with-docs` and `checkpoint` create them when
they do.

A budget is a trigger to prune, not a quota: what survives is decided by the rules, never
by the count. A doc far over its budget is not read, so it stops being true. Detail
always lives in the file a line points at.

**Merge, never reset.** The templates below are for files that don't exist yet. When a
file exists, merge into it: keep working instructions, imports, and references. Running
init again on a project that already has these docs must not reset its roadmap, Resume
here, or decisions. Instructions that only one agent understands can stay in that agent's
own file (`CLAUDE.md`, `.cursor/rules`, ...) next to the `@AGENTS.md` import.

## 1. Read before asking

Read the README, the manifest (`pyproject.toml`, `package.json`, ...), any existing
`AGENTS.md` / `CLAUDE.md`, the docs folder, and `git log`. Derive the commands (setup,
run, test, lint), the layout, the module boundaries, and the constraints. Never ask for
something on disk.

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
- Decisions with their reasons → `DECISIONS.md`, when a new agent without the entry would
  plausibly do the opposite or spend real time finding out why.
- Module descriptions and diagrams → `ARCHITECTURE.md`.
- How to use the project stays in the README.

Show the user the list before moving anything out of an existing file.

## 4. Write the files

`AGENTS.md`:

```markdown
# <Project>

<One line: what this is.> Goal, current state and next step: `ROADMAP.md`. Module map
and boundaries: `ARCHITECTURE.md`.

## Commands

<setup, run, test, lint: exact commands>

## Constraints

<Rules the code can't show. Omit the section if there are none.>

## Testing

<The boundaries tests go through, what runs against real dependencies, what gets faked
and why, and which checks give confidence before calling something done.>

## Patterns

<One line per pattern, naming the file and the aspect to copy: "A new CLI command
follows `probe` in `src/cli.py` for its dry-run default and countdown." Naming the
aspect keeps unrelated quirks from spreading. Never paste code here; it drifts from the
code within weeks, and the canonical file can't drift from itself. Omit the section
until there is a file clean enough to copy.>

## Working on this project

- Start by reading **Resume here** in `ROADMAP.md` and the entry headings in
  `DECISIONS.md`. Before changing anything a heading covers, read that entry; don't retry
  a rejected approach without saying so.
- Write things down when they happen, not at the end: a settled decision goes in
  `DECISIONS.md`; a new blocker or an unverified claim goes in Resume here.
- Before stopping, rewrite Resume here from scratch so the next agent knows the next
  concrete action. It stays under 20 lines. Evidence (run IDs, measurements, counters,
  commands to rerun) goes in `docs/runs/<YYYY-MM-DD>.md`, linked once, never repeated.
  One writer: in a multi-agent run only the orchestrator rewrites Resume here; workers
  put their findings in the run log and report them.
- **Decisions**: record one when a new agent without the entry would plausibly do the
  opposite, or spend real time finding out why. Not for equivalent library picks,
  renames, bug fixes, or anything the code or a commit message already explains. A
  parameter's value is a comment next to the parameter, unless it is coupled to other
  limits a new agent would break. Format: `## YYYY-MM-DD: <decision>`, then what and
  why, then `Rejected: <alternative> because <reason>.` At most five lines; past that, a
  two-line summary here and the rest in `docs/decisions/NNN-slug.md`. A changed decision
  is rewritten, not amended; when two entries disagree, the newer governs and the older
  is marked superseded.
- **Plans** go in `docs/plans/<slug>.md`, and only when asked for or when the work can't
  be tracked in Now plus Resume here. A plan may hold the acceptance examples,
  exclusions, and failure cases agreed before implementation; tests are written from
  them. When the work is done, record any decision it produced and delete the plan.
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
- **Unverified:** <claims made but not yet tested, one line each>

## Now

## Next

## Later

## Not doing
```

Keep Now / Next / Later as short lists of outcomes, not tasks. Get today's date at runtime.

`ARCHITECTURE.md`, for a project that has code; for a new project, write it once the
first modules exist:

```markdown
# Architecture

<The data flow in one line or a small diagram: capture → perception → decision → input.>

## Modules

- `src/<module>/`: <what it owns, one line>

## Boundaries

- <what must not call what, and why, one line each>
```

One page, hard. If it needs more, the modules are too many for one page and the extra
goes in a README next to the module it describes. It describes what exists; an intended
change belongs in the roadmap or a plan, not here.

If a `CLAUDE.md` with content already exists, move what applies to every agent into
`AGENTS.md`, keep anything Claude-specific, and add `@AGENTS.md` at the top.

The Testing section is project-specific: derive it from the existing tests and settle
the gaps in the grilling. Follow `test-craft` for how to write it, and its
"Taking over an existing project" steps when the tests are missing or unreliable.

The Patterns section names files, never code. Point only at a file clean enough to copy
from; if the best example of a pattern is messy, say there is none yet rather than
pointing at it.

## 5. Self-check

Re-read only the new files and write in chat what an agent would do next and what it
would get wrong. Fix the docs for anything it would get wrong. This only catches obvious
gaps; the real test is the first handoff to a fresh session, so say that in the report.

Then report what was written, what moved out of which file, and anything left as an open
question. Don't commit unless asked.
