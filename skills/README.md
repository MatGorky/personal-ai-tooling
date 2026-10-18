# skills/

Skills meant to be used from any project and any agent, not just this repo. Each folder
is linked into Claude Code's and Codex's user-level skills folders, so edits here take
effect everywhere immediately.

| Skill | Use |
| --- | --- |
| [`project-init`](project-init/SKILL.md) | Set up `AGENTS.md`, `ROADMAP.md`, `ARCHITECTURE.md` and, when needed, `DECISIONS.md` in a project |
| [`checkpoint`](checkpoint/SKILL.md) | Reconcile those docs with what a session actually did, and prune them back inside their budgets |
| [`grill-me`](grill-me/SKILL.md) | Interview me until a plan has no silent assumptions |
| [`grill-with-docs`](grill-with-docs/SKILL.md) | The same, recording decisions and terms as they settle |
| [`test-craft`](test-craft/SKILL.md) | Write reliable tests, work test-first, set up or take over a project's testing |

Link them on a new machine (PowerShell):

```powershell
foreach ($s in 'grill-me','grill-with-docs','project-init','checkpoint','test-craft') {
  foreach ($agent in '.claude','.codex') {
    New-Item -ItemType Junction -Path "$env:USERPROFILE\$agent\skills\$s" -Target "$PWD\skills\$s"
  }
}
```
