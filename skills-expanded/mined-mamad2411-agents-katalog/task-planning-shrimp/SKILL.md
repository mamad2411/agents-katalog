---
name: task-planning-shrimp
description: >-
  Plan and split work with Shrimp Task Manager MCP when backlog must persist
  across sessions and tasks have explicit dependencies. Skip for same-session
  planning (use Plan Mode). Requires shrimp-task-manager MCP + Docker volume.
compatibility: Requires Shrimp Task Manager MCP (`shrimp-task-manager`) reachable; data in Docker volume `shrimp_data`.
allowed-tools: MCP(*)
metadata:
  intent: Shrimp = operational state between sessions, not a Plan Mode duplicate.
---

# task-planning-shrimp

Shrimp holds a **persistent task graph** (status, dependencies, verification criteria) outside chat context. It does **not** replace Cursor **Plan Mode** for interactive planning in the current session.

## Shrimp vs Plan Mode

| Need | Use |
|------|-----|
| Agree on approach before coding **this session** | **Plan Mode** + `plan-as-contract` |
| Resume work **after new chat / next day** | **Shrimp** (`list_tasks` → `in_progress` / `pending`) |
| 1–3 simple steps, done today | **Plan Mode** or Issues — not Shrimp |
| Several related tasks with **A blocks B** | **Shrimp** (`dependencies` in `split_tasks`) |
| Per-repo backlog on many projects | **Issues / Linear** — see global-volume warning below |

**CoVe** validates the plan whether Plan Mode or Shrimp produced it.

## Activation gate (anti-noise)

Activate **only when both** are true:

1. **Cross-session continuity** — work will continue in a later chat or after context limits.
2. **Structured backlog** — multiple tasks with explicit `dependencies`, not a single atomic change.

Also activate when user explicitly asks for Shrimp, or `/next` / `/retro` already has Shrimp tasks for this effort.

**Skip** when:

- Single command, short Q&A, or bugfix in one session → `troubleshooting-rca` / Agent.
- Planning that ends in the same session → **Plan Mode** only (do not `split_tasks` for duplicate plan).
- Backlog belongs in issue tracker (GitHub/Linear) and won't be resumed via Shrimp.

## Global volume warning (this setup)

In `~/.cursor/mcp.json`, Shrimp uses **one** Docker volume (`shrimp_data`) for **all** workspaces — not per git repo.

Before `split_tasks` on a new effort:

1. `list_tasks` — note unrelated `pending` / `in_progress` from other projects.
2. If switching project context: use `updateMode: clearAllTasks` (backs up first) **or** `append` only when continuing the same epic.
3. State in one line which project/epic the new tasks belong to (task names or `globalAnalysisResult`).

## Shrimp granularity (follow MCP, not arbitrary splits)

`split_tasks` expects **coarse** subtasks (from tool schema):

- Each subtask: completable in ~**1–2 working days** (8–16 h), single technical domain.
- Per split: **≤10** subtasks (prefer batches of 6–8).
- Task tree depth: **≤3** levels.
- Do **not** split into dozens of 30-minute micro-tasks — that fights the tool design.

For fine-grained same-session steps, use Plan Mode checkboxes instead.

## Procedure

### 1) Discover existing state
```
list_tasks(status: "in_progress")
list_tasks(status: "pending")
```
If continuing: `get_task_detail` on the active task; set `existingTasksReference: true` in `plan_task`.

### 2) Plan (no code changes)
```
plan_task(description, requirements, existingTasksReference?)
```
Optional refinement: `analyze_task`, `reflect_task`, `research_mode` for complex/unknown domains.

### 3) Split into graph
```
split_tasks(updateMode, tasksRaw, globalAnalysisResult?)
```

Each task object must include:

| Field | Required |
|-------|----------|
| `name` | Short, unique (dependencies reference **exact name**) |
| `description` | Goal + acceptance |
| `implementationGuide` | High-level steps / pseudocode |
| `verificationCriteria` | How to verify |
| `dependencies` | `[]` or `["Prerequisite task name"]` |
| `relatedFiles` | Paths + `TO_MODIFY` / `REFERENCE` / `CREATE` when known |

`updateMode`:

| Mode | When |
|------|------|
| `clearAllTasks` | New epic; unrelated pending work exists (default per tool) |
| `append` | Add tasks to current epic |
| `selective` | Rename/update matched tasks |
| `overwrite` | Replace unfinished; keep completed |

### 4) Hand off to execution
Return: task IDs (from `list_tasks`), **next executable task** (deps satisfied), and activate **mcp-shrimp-execution-loop**.

Do **not** call `execute_task` in planning-only mode (Shrimp TaskPlanner vs TaskExecutor separation).

## Dependency rules

- Dependencies are **task names** (strings), not IDs, in `split_tasks`.
- Before recommending `execute_task`, confirm prerequisite tasks are **completed** via `list_tasks` / `get_task_detail`.
- If execution fails with dependency conflict: complete or `update_task` dependencies, then retry.
- **UNCERTAIN:** whether server hard-blocks `execute_task` when deps are open — always verify in `list_tasks` first.

## Alternatives when Shrimp is wrong tool

| Situation | Prefer |
|-----------|--------|
| Same-session plan + implement | Plan Mode → Agent |
| Per-repo issues, PRs, assignees | GitHub / Linear MCP |
| Lessons learned, not task queue | Neo4j memory (`/save_memory`) |
| `/next` with empty Shrimp | git WIP → memory → issues |

## Output

- Epic summary (1–2 sentences)
- `globalAnalysisResult` echo if set
- Table: task name | status | blocked by | taskId
- **Next task** to run (with `taskId`) + which skill: `mcp-shrimp-execution-loop`
