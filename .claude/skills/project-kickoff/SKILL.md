---
name: project-kickoff
description: Interview the user, then write a finished kickoff prompt for a new project or a new phase of an existing one into outputs/. Use when the user is starting a project, entering a new phase (planning, design, implementation, review), or asks for a kickoff prompt, project spec, or "a prompt to start X".
---

# project-kickoff

Interview the user, then fill [`prompts/project-kickoff.md`](../../../prompts/project-kickoff.md)
and write the result to `outputs/YYYY-MM-DD-<slug>-<phase>.md`. The output is a
**paste-ready first message** for a new project or phase — not a document about the
project, not a plan for it.

Read the template before starting. It is the source of truth for the output shape; if it
has changed, the template wins over the layout in this file.

## Hard rules

1. **Never ask what you can find out.** If a repo, `STATE.md`, `AGENTS.md`, README, or
   package manifest is in reach, read it first. Questions about things on disk waste the
   interview.
2. **Only ask what forks the output.** The template's own rule — "assume rather than ask
   unless the answer changes the shape of the work" — governs the interview too. Everything
   else: draft it, let the user correct it. Confirming a draft is cheaper than composing
   from scratch, and the user is a better editor than author of their own spec.
3. **Never invent a fact.** Any number, deadline, volume, or budget the user doesn't have
   goes into the prompt as `UNKNOWN`, exactly as the template asks. A plausible-looking
   invented number is the single worst failure mode of this skill.
4. **One page, hard.** The prompt body stays under ~500 words. Over that you are padding,
   and the template says so. Cut the weakest section rather than tightening everything.
5. **Nothing the model would do anyway.** No "write clean code", "be thorough", "use best
   practices". If deleting a line changes nothing about what comes back, delete it.
6. **No hedging in the instructions.** Hedging belongs in the interview; the prompt gives
   decisions. "Decide, don't hand me options" applies to how you write it, too.

## Workflow

### 1. Orient before asking

Establish whether this is a **new project** or a **new phase** of something existing.
For an existing thing, read what's there — `STATE.md` first if it exists, then `AGENTS.md`,
README, and the manifest — and derive stack, conventions, and what the last phase left
unfinished. Come to the interview already knowing these.

### 2. Interview — three rounds, no more

Use `AskUserQuestion` for anything with discrete answers; batch questions into one call
rather than trickling them out. Keep it to three rounds. Stop early if you have enough.

**Round 1 — the pitch.** The two things you cannot derive:

- Which phase: planning / design / implementation / review.
- What are we building, and **why now**? Push for the real motivation — the business case,
  the constraint being escaped, the thing being learned. Vagueness here is the single
  biggest predictor of a useless prompt, because *why* is what lets the model make the
  hundred calls the prompt never specifies. If the answer is generic ("it'd be useful"),
  ask once more, concretely: what breaks or stays broken if this doesn't exist?

**Round 2 — the forks.** Now be specific, and lead with your own analysis:

- **The classification that forks the design.** Name the one decision that changes
  everything downstream — local-first vs. hosted, batch vs. streaming, single-user vs.
  multi-tenant, library vs. service. Propose the answer with your reasoning and ask the
  user to confirm or overturn it. Do not hand them a menu.
- **Load-bearing facts.** List what you believe the work hinges on numerically — scale,
  volume, latency budget, data size, cost ceiling — and ask which they actually have.
  Whatever they don't have becomes `UNKNOWN` in the prompt.
- **Constraints.** State what you inferred (stack, existing conventions) and ask only for
  what you can't see: budget, timeline, who else touches this, what it has to become later.

**Round 3 — the edges.** Usually one batched call:

- What's explicitly out of scope for this phase.
- Which files the phase should produce — draft the list yourself, ask for corrections.
- Who could veto this later: legal, security, data handling, approvals or quotas with long
  lead times. Prompt with concrete candidates rather than asking open-endedly; the user
  hasn't thought about the quota either.

### 3. Draft the case against

Write this yourself — the user just spent three rounds arguing for the project and is the
wrong person to argue against it. Price the boring alternative fairly (buy it, do it
manually, don't build it) and state the conditions under which not building is correct.
It goes in the prompt whether or not the user likes it.

### 4. Apply the conditional add-ons

Decide these from what you already learned. Don't ask.

| If the interview showed | Add to the prompt |
| --- | --- |
| Work spans multiple sessions | "Read `STATE.md` first, rewrite it last." Nothing more. |
| Genuinely parallel subtasks | Exclusive file write-access per agent; decompose by artifact, never by topic |
| User is new to the domain | "Teach me as you go — sequenced by what unblocks the work soonest." |
| This gets defended to someone | The case-against becomes mandatory and goes near the top |

### 5. Pre-flight, then write

Check the draft against the template's own list — phase boundary stated, the *why* is
there, load-bearing facts supplied or marked `UNKNOWN`, output files named, no hedging,
nothing the model would do anyway — and fix what fails **before** writing the file, not
after.

Write to `outputs/YYYY-MM-DD-<slug>-<phase>.md`. Get the date at runtime
(`date +%Y-%m-%d`); never guess it. Create `outputs/` if it doesn't exist. `<slug>` is
2–3 kebab-case words.

### 6. Report back

In chat, not in the file: where it was written, every assumption you made and what breaks
if it's wrong, and each fact left `UNKNOWN` with what it blocks. If a `UNKNOWN` would make
the first deliverable invented rather than derived, say so plainly — that's the user's cue
to go find the number before pasting.

## Format contract

The file is two blocks separated by `---`. Everything above the separator is the prompt
and must survive a select-all-and-paste with no editing: no preamble, no "here's your
prompt", no meta-commentary, no `<<>>` placeholders left behind.

```markdown
We're in the <phase> phase.
Out of scope right now: <what it shouldn't touch yet>.

**Role:** <role to assume>

**Goal:** <what we're building, 2–3 sentences>

**Why:** <the real motivation>

**Constraints:** <budget, stack, timeline, skill, what this becomes later>

**Facts the work depends on:** <numbers and inputs; UNKNOWN where absent>
<the classification that forks the design — committed to and justified>

**Output:** <files to produce, one line of purpose each — names, not schemas>

**How to work:** Decide, don't hand me options — record rejected alternatives and what
it'd cost to reverse them. Assume rather than ask unless the answer changes the shape of
the work; log what you assumed and what breaks if it's wrong. Mark any number you can't
derive as an estimate, with its basis.

**Cover these or I'll get burned later:** <the vetoes: legal, security, data handling,
long-lead approvals and quotas>

**Include the case against this.** <the boring alternative priced fairly; when "don't
build it" is right>

<conditional add-ons from step 4, if any>

---

## Interview notes

<assumptions made and what breaks if wrong; UNKNOWNs and what they block; alternatives
the user rejected and why>
```

The **How to work** block is copied verbatim from the template — it is already correct and
tuning it per project is how it rots.

## Notes

- Acceptance criteria, decision records, session state, and conventions belong in the new
  project's repo, not in this prompt. If the user wants `AGENTS.md`, `STATE.md`, or ADR
  skeletons, generate them directly into the new project — the template points at a
  `project-kickoff-prompt-template.md` for these, which does not currently exist.
- Keep `AGENTS.md` short when you do write one: build and test commands, project layout,
  what's off-limits. Detail goes in referenced files, loaded on demand.
