---
name: meego-query
description: Search and query Meego work items across projects — find stories, issues, bugs, or tasks by user, keyword, or ID. Use whenever the user wants to find Meego tasks, look up work items, search for stories or issues, check task status, or needs to find work items for association. Also trigger when the user mentions Meego and wants to query or search. Supports cross-project search and filtering by type, time range, and keyword.
---

> ⚠️ **You MUST create a session_id first before running any `gdpa-cli run` command.**
>
> **session_id 传递**：在使用 `gdpa-cli run` 下的命令前，**必须先创建 Session**。
> 1. 创建 Session: `gdpa-cli create-session`（返回 session_id）
> 2. 在 `gdpa-cli run` 的所有命令中通过 `--session-id` 参数传递：
>    - `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`
>    - `gdpa-cli run devflow list --session-id <session_id> --psm xxx`
>    - `gdpa-cli run apply-mcp --session-id <session_id> --psm xxx --sa xxx`
> ⚠️ 不传递 --session-id 会报错。请确保在同一会话的所有调用中使用相同的 session_id。

# Meego Query Agent

Search Meego work items across projects for task association using `WorkItemFilterAcrossProject` API.

> **When to use**: When you need to find existing Meego tasks/stories/issues to associate, search a user's work items, or look up specific work item details.

## Quick Start

### Search user's recent stories (recommended)

```bash
gdpa-cli run meego-query --input '{
  "work_item_type_key": "story",
  "page_size": 20,
  "updated_at_start": "4380h"
}'
```

> `email` 可省略，会自动通过 `gdpa-cli login` 的登录信息获取用户名并拼接 `@bytedance.com`。也可以显式指定：`"email": "yourname@bytedance.com"`。

### Search by keyword

```bash
gdpa-cli run meego-query --input '{
  "work_item_name": "gdpa",
  "updated_at_start": "4380h"
}'
```

### Query by specific ID

```bash
gdpa-cli run meego-query --input '{
  "work_item_ids": "[6742176517]"
}'
```

## Input Parameters

### Optional (auto-fetched)

| Parameter | Type | Description |
|-----------|------|-------------|
| `email` | string | User's ByteDance email. If not provided, auto-fetched via `gdpa-cli login` info (username + `@bytedance.com`). You can also use `user_jwt` skill (`gdpa-cli login -u cn`) to get username and append `@bytedance.com` |

### Optional (Recommended)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `updated_at_start` | string | none | ⚠️ **RECOMMENDED**. Time range filter, Go duration format. Use `"4380h"` (~6 months). Without this returns ALL items |
| `work_item_type_key` | string | `"story"` | Work item type: `story`, `issue`, `project`, `sprint`, `chart`, `sub_task` |
| `work_item_name` | string | none | Fuzzy keyword search on work item name |

### Optional

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_keys` | string | all projects | JSON array of project keys, e.g. `"[\"64e70ccaf56b8dff0331bc7e\"]"` |
| `work_item_ids` | string | none | JSON array of work item IDs, e.g. `"[6742176517]"` |
| `page_size` | int | 20 | Results per page |
| `page_num` | int | 1 | Page number |

## Output Format

```json
{
  "success": true,
  "data": {
    "total": 8,
    "page_num": 1,
    "page_size": 5,
    "items": [
      {
        "id": 6788756641,
        "name": "work item name",
        "project_key": "64e70ccaf56b8dff0331bc7e",
        "simple_name": "ttarch",
        "work_item_type_key": "story",
        "status": {
          "state_key": "end",
          "is_archived": false,
          "is_initial": false
        },
        "created_by": "7114917577608003586",
        "updated_by": "7114917577608003586",
        "created_at": 1761891808217,
        "updated_at": 1764838316441
      }
    ]
  }
}
```

## Examples

### Example 1: Search user's recent stories (auto email)

```bash
gdpa-cli run meego-query --input '{"work_item_type_key":"story","page_size":5,"updated_at_start":"4380h"}'
```

**Response:** Returns 8 items with work item details (id, name, project, status, timestamps).

### Example 2: Search by keyword

```bash
gdpa-cli run meego-query --input '{"work_item_name":"gdpa","page_size":10,"updated_at_start":"4380h"}'
```

**Response:** Returns 3 filtered items matching "gdpa" keyword.

### Example 3: Query by specific work item ID

```bash
gdpa-cli run meego-query --input '{"work_item_ids":"[6742176517]"}'
```

**Response:** Returns exactly 1 item with the matching ID.

### Example 4: Explicit email

```bash
gdpa-cli run meego-query --input '{"email":"yourname@bytedance.com","work_item_type_key":"story","updated_at_start":"4380h"}'
```

## Parameter Testing Summary

| Parameter | Required | Test Result |
|-----------|----------|-------------|
| `email` | No (auto-fetched) | Without → auto-fetched from login info. If login unavailable → error |
| `work_item_type_key` | No | Without → defaults to "story", same results |
| `updated_at_start` | **RECOMMENDED** | Without → 112 items (all). With "4380h" → 8 items (recent 6 months) |
| `work_item_name` | No | "gdpa" → filtered from 8 to 3 results |
| `project_keys` | No | Limits to specific project(s) |
| `work_item_ids` | No | Exact ID lookup, returns 1 result |
| `page_size` / `page_num` | No | Pagination works correctly |

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Plugin Token Must Have User Key (20039)` | Missing `email` and auto-fetch failed | Provide valid ByteDance email or run `gdpa-cli login` |
| `success: true, total: 0` | No matching items | Broaden search: remove `work_item_name`, extend `updated_at_start`, try different `work_item_type_key` |
