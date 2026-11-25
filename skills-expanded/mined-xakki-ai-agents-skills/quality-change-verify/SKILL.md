---
name: quality-change-verify
description: 'Run and report a final, post-repair or pre-completion validation pass with exact commands, exit codes and limits, discovering the project''s sanctioned checks. Use before declaring work done or after a repair. RU: проверка перед завершением, итоговая валидация, качество.'
---

# Change verification

Use for a requested final or post-repair validation pass, or before declaring a task done. Establish the actual project, candidate, current inputs, authorized scope and applicable required gates. Record relevant branch and revision, staged and unstaged changes, and untracked deliverables before and after; ordinary Git diff checks do not include untracked files. For final verification do not stage, unstage, repair or start services unless separately authorized.

Discover the project's sanctioned checks from `AGENTS.md`, project guidance, Make targets, manifests and scripts, CI workflows and saved project instructions; use their entrypoints and working directory. Do not guess a command, target or test filter and do not run a first-use questionnaire. Scope checks to the task-owned diff; use required Make/container gates when project instructions require them, otherwise documented project-native runners. Broader regression checks are justified by project requirements or material blast radius, without routine confirmation. Use only authorized, documented environment setup; never install ad-hoc dependencies or bypass sanctioned runners.

Inspect a command's side effects before calling a pass read-only: tests may start services, modify generated files or shared state. A read-only authorization does not authorize edits, index changes, service startup, mutation or deployment. Run only permitted checks, state any missing authorization or environment blocker, and do not perform a repair in an independent read-only review.

Record each exact command, working directory, exit status, meaningful totals and failures. Green means exit status `0` and no new warnings under the project's policy. A launched or timed-out process is not a completed gate; track its actual completion when supported. Avoid concurrent tests that share mutable state. Separate earlier evidence from checks on the present candidate and label unrun, blocked, failed and passed checks; never imply broader coverage than measured. For long-running, shared-state or runtime checks use [verification modes](references/verification-modes.md).

For a repair, verify the original failure with focused checks where feasible, then required broader gates and proportionate integration checks where shared state or ordering matters; do not automatically require every suite. Classify direct, baseline and environment failures separately. A wrong invocation or working directory is an operator error, not a product result. Do not infer a root cause without evidence. If a check is red and fixing is authorized and in scope, fix the root cause and rerun.

Never make a check pass by: skipping or disabling lint/type checks; marking tests skipped, `xfail` or commented out without a real, stated reason; `--no-verify`; silencing failures with `|| true` or discarded stderr; substituting a native runner for a required Make/container gate; or inventing a targeted filter to avoid a sanctioned gate. Do not run a whole suite by default when a sanctioned focused check suffices.

Report the candidate, commands and outcomes, counts and failures, worktree effects, untested scope and blockers. A passing subset is not the whole gate. Distinguish self-check from independently authorized review; for defect and mutation evidence see `quality-change-review`. Passing checks is not authorization to publish, merge or deploy: those need valid action-specific authorization covering the target and all required gates, and are never inferred from a green check.
