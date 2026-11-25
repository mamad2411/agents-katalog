---
name: mcp-shrimp-execution-loop
description: >-
  Execute Shrimp tasks in order: load state, respect dependencies, implement,
  verify_task, update status. Use after task-planning-shrimp or when resuming
  in_progress/pending tasks (/next). Not for same-session-only Plan Mode work.
compatibility: Requires Shrimp Task Manager MCP; pairs with task-planning-shrimp for planning.
allowed-tools: MCP(*) Bash(*) Read Write StrReplace
---

# mcp-shrimp-execution-loop

Runs the **execute → verify → update** cycle against Shrimp's persistent task store. Planning new epics belongs in **task-planning-shrimp**; same-session-only work belongs in **Plan Mode**.

## Activation gate

Activate when:

- Shrimp tasks already exist (`list_tasks` shows `in_progress` or `pending`), or
- `split_tasks` just created a graph and user wants execution, or
- `/next` selected a Shrimp-backed next task.

Skip when:

- No Shrimp MCP available — use Agent + Plan Mode instead.
- User is in **ASK** mode (read-only; no `execute_task` / file edits).
- Task is a one-shot change with no Shrimp `taskId`.

## Resume protocol (`/next`, new chat)

1. `list_tasks(status: "in_progress")` — if any, **resume first** (`get_task_detail` → `execute_task`).
2. Else `list_tasks(status: "pending")` — pick first task whose `dependencies` are all **completed** (check names against completed list).
3. If global volume has unrelated tasks, filter by epic keywords in task name / `globalAnalysisResult` (see **task-planning-shrimp** global-volume warning).

## Execution loop (one task at a time)

Shrimp expects **one task per cycle** unless user requests continuous mode.

```
┌─────────────────────────────────────┐
│ 1. get_task_detail(taskId)          │
│ 2. execute_task(taskId)             │  ← follow returned guidance; NOT "done" yet
│ 3. Implement in repo (minimal diff) │
│ 4. Verify (tests/lint/run)          │
│ 5. verify_task(taskId, score, summary) │  score ≥80 → auto-completes
│ 6. If score <80: fix → re-verify    │
└─────────────────────────────────────┘
         │
         ▼
   Next pending with satisfied deps, or stop
```

### Step details

**`execute_task`** — returns instructional guidance only. You must still edit files and run verification. Never mark done immediately after the tool call.

**`verify_task`** — requires `score` (0–100) and `summary` (≥30 chars). Use `verificationCriteria` from `get_task_detail`. Score **≥80** completes the task in Shrimp.

**`update_task`** — use mid-flight for notes, `relatedFiles`, or dependency fixes; completed tasks allow only summary + relatedFiles.

**Blocked dependencies** — do not skip silently. Either complete prerequisites first or ask user to reprioritize / `update_task` dependencies.

## Pairing with other tooling

| Phase | Tool |
|-------|------|
| Stuck on failure | `debugger` subagent + `troubleshooting-rca` |
| Tests failing | `test-runner` |
| Security-sensitive task | `security-auditor` before `verify_task` |
| Epic complete | `verifier` subagent, then optional `/save_memory` |

After epic completion: propose `/save_memory` with outcome — do not auto-save.

## Continuous mode

Only if user explicitly asks ("continuous", "ciągły", "all remaining tasks"):

- Loop pending tasks in dependency order.
- Stop on: failing `verify_task` (<80), ambiguity, destructive ops needing confirmation, or blocker outside scope.

## Global volume discipline

Same as planning skill: one `shrimp_data` volume for all projects. When executing, confirm tasks belong to **this** repo/epic before changing code. If mixed backlog, ask user which task ID to run.

## Output (each cycle)

```text
Shrimp: <task name> (<taskId>) — <status after verify>
Done: <1 line>
Next: <task name + taskId | "none — epic complete">
Verify: <command run + result>
```

Final epic summary: counts completed/skipped, link to memory save prompt if useful.

## Anti-patterns

- Using Shrimp to re-plan what Plan Mode already approved in the same session.
- `clearAllTasks` mid-execution without user consent.
- Parallel `execute_task` on dependent tasks.
- Claiming task complete without `verify_task` or repo verification.
