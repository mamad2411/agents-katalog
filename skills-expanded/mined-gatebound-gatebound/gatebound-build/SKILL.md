---
name: gatebound-build
description: Build the tasks in spec/04-tasks.md behind the gates — by default this session implements each task and `jobs complete` runs its gates; on request (--backend, execution=worker) workers run the tasks and failures are redelegated up to the retry budget. The gates decide pass or fail, then hand off to verify. Korean triggers — "빌드 시작해줘", "작업 실행해줘", "태스크 자동으로 만들어줘", "워커로 돌려줘". English triggers — "build it", "run the tasks", "execute the task list", "run the tasks on workers". NOT for coding outside the task list or past the gates, and NOT for judging whether the result is done — that is /gatebound:verify.
user-invocable: false
---

# gatebound-build

Invoke `/gatebound:build`, passing any task ids the user named as the argument.

Do not implement tasks from this file. `plugin/commands/build.md` is the
execution instruction; this file only routes to it.

Two things the command enforces and this shim must not undercut: under
`execution: worker` the main session never edits a task's files while its job
runs (under the default `host` it implements them and `jobs complete` judges),
and nobody's own report decides a verdict. The gates decide.

Under a host without slash commands (Codex), `/gatebound:build` does not exist:
read `commands/build.md` two directories above this skill's folder and follow
it, applying `policy/codex.md` from the same plugin.
