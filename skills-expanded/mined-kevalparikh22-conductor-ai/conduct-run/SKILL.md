---
name: conduct-run
description: "Execute a whole plan with worker LLMs in one call (tasks in parallel by their depends, merged and verified by conductor-ai), then review"
argument-hint: "<plan-file> [from-task-id]"
disable-model-invocation: true
allowed-tools: "Read, Edit, Bash(conductor-ai:*), Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git log:*), Bash(git merge:*), Bash(git stash push:*), Bash(git stash list), Bash(git switch -c:*)"
---

You are the controller (see `.conductor-ai/ORCHESTRATOR.md`). Execute `the arguments the user gave` (from the given task id, if one is given).

**One call does the plan.** Keep your turns few: each turn costs time and quota.

1. `conductor-ai plan check <plan>`. Fix every ✗ task and every `!` warning in the plan first (a contradiction there becomes a wrong test).
2. Make sure the checkout is clean (`git status`): commit or stash your own changes. Then run it **in the foreground**, with the longest timeout your shell tool allows (Claude Code: 600000 ms); it prints one summary when it is done. Don't start it in the background and then poll or `sleep` for it: a wait loop can outlast the batch by many minutes (seen in B2: the batch took 98 s, the loop 20 min). If it outlasts your timeout, `conductor-ai runs` shows what finished:
   `conductor-ai batch --plan <plan> --all`
   (from a given task id: `conductor-ai batch --plan <plan> --tasks <that id and the ones after it> --merge`). conductor-ai starts every worker task as soon as the tasks it depends on are merged, each in its own worktree on a different provider; checks each one (verify, acceptance checks, scope); merges each one that passed into this branch and runs verify on the merged code; gives slow tasks a second attempt and runs reviews off the critical path. Controller tasks and tasks already `status: done` are listed and left to you. Add `--priority speed` only if the user asked for speed over tokens (`save` for the opposite).
3. Read the batch summary once. Per task:
   - **✓ and merged:** nothing to do: conductor-ai already set `status: done` in the plan and committed it. Read its `review:` line if there is one: triage each finding yourself (they are advisory) and fix the real ones (small ones yourself, larger ones with `conductor-ai run fix "<finding>"`).
   - **✗, ⚠ or ? (not merged):** `conductor-ai retry <id> --note "<what to fix>"` (same worker, same worktree; `--provider <other>` to hand it on), review `conductor-ai diff conductor-ai/<id>`, then `git merge --no-ff conductor-ai/<id>`, `conductor-ai worktree rm <id>`, and set `status: done` for it. Start over only when the work is unusable. Then run the tasks that waited on it: `conductor-ai batch --plan <plan> --all` again (done tasks are skipped).
   - **NOT MERGED: conflict:** resolve it yourself (`git merge --no-ff <branch>`), or retry that task now that the others are merged.
   - **verify FAILED on the merged code:** the batch stopped there. Fix it yourself (small) or with `conductor-ai run fix`, or undo the merge as the line says, then run `--all` again.
   - **not started:** it waited on a task that didn't merge; it runs on the next `--all`.
4. Do the controller tasks yourself.

While running:
- Keep your context small: read the summaries, `report.md` and `conductor-ai diff`, never `report.full.md` or run logs.
- **Stop and ask** if a task needs a design decision the plan doesn't cover, a worker leaves its scope twice, or verify fails for reasons outside the task.
- If every task failed with exit 3 (everything rate-limited), stop, update `HANDOFF.md`, and report what is left.

When all tasks are done:
1. Review only when something calls for it: a task ended partial, out of scope or handed on, a `review:` line had findings you did not fix, or the plan asks for one. Then `conductor-ai run review --plan <plan>` (background), triage, fix, commit. When every task passed and merged the first time, skip it and say "no extra review: every task passed its checks".
2. `conductor-ai worktree` should list nothing; remove leftovers.
3. Summarise in a few lines: tasks per provider, merged, review findings, leftovers. Update `HANDOFF.md` only if something is left for later (one edit, no commit of its own). When everything merged, there is no other bookkeeping to do: keep your turns to a minimum.
