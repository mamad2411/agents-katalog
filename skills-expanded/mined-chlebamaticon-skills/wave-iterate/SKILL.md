---
name: wave-iterate
description: >-
  Evaluate, resume, and execute the next actionable planned Wave from .waves/.
  Use when the user asks to run, resume, reassess, or continue a Wave after
  planning with wave.
---

# Wave iterate

Use this skill only after `/wave` has written task briefs. It owns execution and lifecycle management; `/wave` owns only planning.

## 1. Reconcile the Wave board

Read all `.waves/<topic>-<wave-no>/*.md` task briefs. Select the earliest Wave that is not fully merged. For each task, use its `Status:`, `PR:`, and `Quality:` fields, then verify referenced PRs, quality checks, and labels against GitHub. Update the task brief atomically whenever its lifecycle changes:

- `planned` — no worker or PR yet
- `in-progress` — worker or branch exists, but no PR yet
- `open` — PR URL recorded
- `merged` — PR is merged
- `halted` — PR has `needs-human`, `needs-decision`, or `blocked`

If no task briefs exist, stop and direct the user to run `/wave` first. If every task is merged, show the completed board and stop.

For the selected Wave, report a concise status: each task ID, title, Kind, Status, PR (when present), Quality, and halt labels. Do not reassign, relaunch, or duplicate a task with an open or in-progress PR. If a task's evidence is ambiguous, ask the user before changing it.

## 2. Handle the current gate

- Any `halted` task: report its PR URL and labels, then stop.
- An `open` task with a failed quality gate or requested changes: assign only that task to a repair worker. It fixes, pushes, and then runs `/validate` on the same PR.
- An `open` task whose quality gates are still pending: continue watching; do not treat it as ready to merge.
- An `open` task with all quality gates passing and no halt label: leave it awaiting merge.
- A Wave with open or in-progress tasks: do not start its remaining planned tasks until the user explicitly asks to launch them; never start a later Wave.
- A Wave whose tasks are all merged: select the next planned Wave and repeat reconciliation.

## 3. Choose models for planned tasks

For the selected Wave's `planned` tasks only, ask the user once for model choices. Default every `implementation` task to Composer 2.5. If there are `research` tasks, ask which model to use: GPT Luna, Terra, Sol, or a custom choice. Write the selected display name to each task's `Model:` field.

Choose one available execution runtime for the entire Wave. Map each chosen display name to an exact model ID available in that runtime. Never invent or substitute a model ID; if a requested model is unavailable, report the available choices and wait.

## 4. Summarize and obtain consent

Before creating worktrees, launching workers, or making GitHub changes, show the user the current Wave's launch plan. Include every planned task's ID, title, Kind, selected Model, one-line scope, base SHA, and the fact that it receives an isolated branch, worktree, and PR. Also list open or merged tasks excluded from this dispatch and any dependencies reserved for later Waves.

Ask for explicit consent with these choices: **Launch planned tasks**, **Revise the breakdown**, or **Cancel**. Do not execute unless the user selects **Launch planned tasks**. On a revision, update the task briefs and repeat model selection when scope or Kind changed. On cancellation, retain the briefs and stop.

## 5. Dispatch and record results

Confirm the source checkout is clean before creating isolated worktrees. If it is dirty, report the blocking files and wait for the user to choose commit, stash, or discard.

Use one execution runtime per Wave. In Cursor Multitask, create one Git worktree and branch per dispatched task, then launch one background `generalPurpose` task per worktree in one message. Otherwise, if the Pi subagent runtime is exposed, launch one asynchronous workflow with one isolated worker per task. Each worker receives its task brief's absolute path, assigned worktree path, base SHA, and authority to implement, commit, push, and open exactly one PR; it must not access sibling briefs or later Waves.

When a worker opens a PR, record its URL in `PR:`, set `Status: open`, and preserve its handoff evidence. If it returns without a PR, set `Status: in-progress` and resume only that task on a later `/wave-iterate`. Do not start a later Wave until every current-Wave PR is merged.

## 6. Watch quality gates, repair, and advance

Run `/validate` for every open Wave PR. Then watch every PR's complete GitHub quality gate, including CI/CD checks that report a GitHub check run or commit status, required branch-protection or ruleset checks, required reviews, merge conflicts, draft state, and halt labels. Use the PR's check-rollup and mergeability state, not a single check name. Keep watching pending checks until they complete; record one of `Quality: pending`, `Quality: passing`, or `Quality: failing` in the task brief.

Do not advance to another Wave until every task in the current Wave is `merged`, and every one of its PRs reached `Quality: passing` before merge. A failed, cancelled, stale, missing-required, or skipped-required check is failing unless the repository's protection rules explicitly accept it. For a failed quality gate or requested change, dispatch a repair only for that PR, then repeat validation and the full quality watch. Mark tasks `halted` and stop for halt labels. Mark tasks `merged` only after GitHub confirms their merge.

External quality systems that do not publish a GitHub check, commit status, deployment status, or PR review cannot be watched automatically. List them as unresolved gates and ask the user for evidence before proceeding.

When all tasks in the current Wave are merged, update their briefs, then select and evaluate the next planned Wave. Before dispatching its planned tasks, repeat model selection, the launch summary, and explicit consent.
