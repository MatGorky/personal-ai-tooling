---
name: grill-me
description: Grill the user relentlessly about a plan, decision, or idea until there is a shared understanding. Use when the user says "grill me" or wants to stress-test their thinking.
disable-model-invocation: true
---

# Grill me

Adapted from Matt Pocock's `grilling` skill (MIT, github.com/mattpocock/skills).

Interview the user until there is enough shared understanding for the next useful step.
Map the topic as a **design tree**: every decision branches into the decisions that hang
off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are
already settled. Each round, ask the **few most consequential** frontier questions (about
five at most), numbered, each with your recommended answer. Then wait for the answers.

Ask in chat, as text. Do not use form or multiple-choice question tools.

```
**Q1. <question title>**: <question body, with the real options if there are any>

➡️ <your recommended answer and the one reason it wins>

**Q2. ...**
```

Word each question so "yes" accepts your recommendation.

Each round reshapes the tree: settled decisions push the frontier outward. Recompute it
and ask the next round. A question that depends on another question still open in this
round belongs to a later round.

Finding **facts** is your job, never the user's. If a question needs a fact from the
repo, the filesystem, or a tool, look it up (or send a subagent) instead of asking. Only
the questions downstream of a pending lookup wait for it.

**Decisions that shape the work are the user's**: goals, scope, trade-offs they'd care
about. Routine technical choices are yours: make them, and list them as assumptions in the
next round so the user can overturn one.

Push on vagueness. "It'd be useful" or "make it better" is not an answer; ask once more,
concretely: what stays broken if this doesn't happen, and how will we know it's done?

Stop when the next useful step is clear, not when every branch is exhausted. End with a
short list: decisions made, assumptions you made, and questions deliberately deferred.
Recording an answer the user confirmed is fine at any point; starting implementation
waits until the user confirms the final list.
