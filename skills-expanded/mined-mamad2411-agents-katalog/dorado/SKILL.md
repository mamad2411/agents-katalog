---
name: dorado
description: Query Dorado (DataLeap) projects, batch tasks, temporary SQL executions, project yarn queues, and queue resources. Use when the user mentions Dorado, DataLeap, batch dorado tasks, dorado temporary query SQL, dorado project id lookup, dorado task lookup, dorado queue lookup, or wants to inspect a Dorado task in cn/sg/gcp/va/boe/boei18n or a configured custom region.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Dorado Agent

Query Dorado project/task metadata and run temporary SQL with the business-facing actions exposed by this repo.

## Debug SQL Prerequisite

`debug_sql_exec` / `debug_sql_status` / `debug_sql_result` / `debug_sql_history` require a saved Dorado temporary-query task as the execution carrier.

- Create path: `Dorado 项目 > 临时查询 > 新建查询`
- After creating it, switch the execution engine to `Spark` on the page if needed, then configure `dc` / `cluster` / `queue` and click save
- The task only needs to be created once; later debug SQL executions inherit its saved `dc` / `cluster` / `queue`
- You can read `task_id` from the page URL: `/query/<task_id>`
- Example: `.../query/123456789?project=cn_2059` means `task_id=123456789`

This repo does not use `.dorado.env`. Instead, you can persist per-region defaults in `~/.gdp_config/dorado_defaults.yaml`:

```yaml
regions:
  cn:
    default_task_id: 125033930
    default_project_id: 2059
```

When `debug_sql_*` input omits `task_id` or `project_id`, explicit input wins; otherwise the agent reads the region default from this file.

## Quick Start

```bash
# List projects
gdpa-cli run dorado --session-id "$SESSION_ID" --input '{
  "action": "list_projects",
  "region": "cn",
  "page": 1,
  "page_size": 20
}'

# Get one task
gdpa-cli run dorado --session-id "$SESSION_ID" --input '{
  "action": "get_task",
  "region": "boei18n",
  "task_id": 100274211
}'

# Execute debug SQL on an existing temporary-query carrier task
gdpa-cli run dorado --session-id "$SESSION_ID" --input '{
  "action": "debug_sql_exec",
  "region": "boei18n",
  "task_id": 100274211,
  "project_id": 458,
  "sql": "SELECT count(*) FROM db.table"
}'
```

## Supported Actions

Read / inspect:

- `list_projects`
- `list_tasks`
- `search_tasks`
- `get_task`
- `get_queue_resource`
- `list_project_yarn_queues`
- `debug_sql_status`
- `debug_sql_result`
- `debug_sql_exec`

## Common Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `action` | string | Yes | Dorado action name |
| `region` | string | No | Dorado region. Default: `cn` |
| `project_id` | int | Depends | Needed by project-scoped actions |
| `task_id` | int | Depends | Needed by task-scoped actions |
| `folder_id` | int | Depends | Required by `search_tasks` |

## Action Notes

- `search_tasks`: Dorado batch search requires `folder_id`; if you do not know it, get it from the Dorado page URL or ask the task owner.
- `list_tasks`: when `task_id` is absent, the agent lists tasks from the project's searchable root folder.
- `debug_sql_exec`: requires an existing Dorado temporary-query task as the execution carrier.
- `list_project_yarn_queues`: defaults `username` to the current login user when available.
- `get_queue_resource`: accepts comma-separated strings or arrays for `clusters` and `queues`.
- For `debug_sql_*`, if `task_id` / `project_id` are absent, the agent first tries `~/.gdp_config/dorado_defaults.yaml`.

## Regions

Builtin regions:

- `cn`
- `sg`
- `gcp`
- `va`
- `boe`
- `boei18n`

Custom regions follow this repo's own config convention under `~/.gdp_config/dorado_regions.yaml`. This skill does not use `.dorado.env`.
