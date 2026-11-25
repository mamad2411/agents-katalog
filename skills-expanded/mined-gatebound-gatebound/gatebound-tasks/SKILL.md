---
name: gatebound-tasks
description: Break an existing spec into vertical-slice tasks with non-overlapping write scopes, dependency rounds, and a gate command each. Korean triggers — "작업 나눠줘", "태스크로 쪼개줘", "할 일 목록 만들어줘", "작업 분해해줘". English triggers — "break this into tasks", "split the work", "make a task list from the spec", "decompose into work items". NOT for executing the tasks — that is /gatebound:build — and NOT for writing the spec itself.
user-invocable: false
---

# gatebound-tasks

Invoke `/gatebound:tasks` with any constraints the user mentioned as the
argument.

Do not decompose anything here. `plugin/commands/tasks.md` is the execution
instruction; this file only routes to it.

The command requires `spec/01-prd.md` to exist. If it does not, route to
`/gatebound:interview` first.

Under a host without slash commands (Codex), `/gatebound:tasks` does not exist:
read `commands/tasks.md` two directories above this skill's folder and follow
it, applying `policy/codex.md` from the same plugin.
