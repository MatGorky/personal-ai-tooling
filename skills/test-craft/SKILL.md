---
name: test-craft
description: How to write tests that protect real behavior and survive refactoring, how to work test-first, and how to set up or take over a project's testing approach. Use whenever writing, changing, or reviewing tests, doing TDD, setting up testing in a new project, or picking up a project whose tests are missing or unreliable.
---

# Test craft

The goal: **protect meaningful behavior with tests that give reliable feedback, survive
internal refactoring, and are cheap enough to run often.** Judge every test by the
confidence it buys for its cost, not by a quota of test types or a coverage number. This
is the idea behind Kent C. Dodds' Testing Trophy, and it applies to backends as much as
frontends.

**The project comes first.** Read the Testing section of `AGENTS.md` before writing any
test. Where it disagrees with this skill, the project wins.

## Rules

1. **Test behavior through a stable interface.** Assert what a caller can observe:
   returned values, stored changes, emitted events, visible UI. Don't assert on private
   methods or incidental call order, unless the order is the behavior (releasing a held
   key, committing before publishing).
2. **Pick the smallest scope that catches the real failure.** A calculation gets a
   focused test. A database transaction needs a real database. A login journey needs a
   browser. Don't push everything through HTTP just to call it integration.
3. **Keep your own collaborating code real.** Replace a dependency when you need control
   over time, failures, cost, or external effects, not because you don't own it: a real
   disposable database, but a controlled clock. When a substitute stands in for something
   real, check the real integration separately where it matters, and say that the fake
   doesn't prove it.
4. **Spend tests on risk.** Important rules, boundaries, failure handling, and past bugs
   first. No test-per-class, no coverage targets. Before writing a test, name the mistake
   it would catch.
5. **Keep the loop dependable.** Tests are independent. Time and randomness are
   controlled, data is isolated, and a failure message says what broke. Keep a fast
   suite for development and slower checks for integration confidence.
6. **Expected values come from the requirement**, or from an example checked
   independently, never from running the code. Never change an expectation, skip a test,
   or delete one just to get to green. If the test is wrong, say why before changing it.

Frontend default: mostly tests that render components and drive them the way a user
does, focused tests for tricky logic, and a few end-to-end tests of critical journeys.
Backend default: behavior tests through the application against a disposable database,
focused tests for complex logic, and a few checks of the deployed wiring.

## Test-first loop

1. Write one test for the next behavior.
2. Run it and **watch it fail for the intended reason**. A test that fails on an import
   error, or passes immediately, proves nothing yet.
3. Write the least code that makes it pass.
4. Refactor with the tests green. Tests that break during a refactor that kept behavior
   intact are testing implementation; fix them per rule 1.

Trigger a new test with a new behavior, not with a new class or method.

## Setting up a new project

Write the Testing section of `AGENTS.md` (`project-init` calls for it):

```markdown
## Testing

<The interfaces tests go through. What runs against real dependencies, what is faked
and why. The commands for the fast suite and the slower checks. What must be checked
by hand or live, because tests can't reach it.>
```

Keep it to project specifics. Don't copy these rules into it.

## Taking over an existing project

Don't start by rewriting tests or by writing new code.

1. **Map what exists.** Run the suite. Note what passes, what fails, what's skipped,
   what's flaky, and what each part actually protects. Note which important behaviors
   have no tests.
2. **Pin current behavior before changing it.** Around the code you're about to touch,
   add *characterization tests* (Michael Feathers' term): tests that record what the code
   does today, so a change can't silently alter it. Label them as recording current
   behavior, not as a statement of what's correct. Behavior that looks like a bug gets
   listed for the user, not pinned as the spec.
3. **Write the Testing section** with what you learned, then work test-first from there.

## Reporting

When you say something works, say what verified it: which suite, and whether it ran
against real dependencies or substitutes. Anything that only a fake or a recording has
shown goes in Resume here under Unverified.
