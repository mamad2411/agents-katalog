---
name: wingman-mcp
description: Add persistent, interactive task plan management to your agent. Wingman tracks plans and tasks across a long conversation — Claude creates plans, ticks tasks after completing work, and a live panel renders inline in the chat. Install the MCP server first, then use these tools to manage plans and tasks throughout any multi-step workflow.
license: MIT
---

# Wingman MCP — Persistent Plan & Task Management

## Install

```bash
pip install wingman-mcp
```

Then add to your MCP host config and restart. See https://github.com/adeoluwaadesina/wingman-mcp for host-specific setup (Claude Desktop, Cursor, VS Code).

## When to use

- The user is working on a multi-step goal that spans more than one turn
- You need to track what's been done, what's in progress, and what's pending
- You want to break down a complex task before starting, then work through it systematically
- You're orchestrating sub-tasks and need durable state across agent calls

## Tools

| Tool | Purpose |
|------|---------|
| `create_plan(name, tasks[])` | Create a named plan with optional initial tasks |
| `show_plan(plan_name)` | Render the interactive panel inline in chat |
| `show_plans()` | Render a clickable plan picker (all plans with task counts) |
| `get_plan(plan_name)` | Return plan state as formatted text — no panel |
| `add_task(plan_name, content)` | Append a single task |
| `add_tasks(plan_name, tasks[])` | Append multiple tasks in one call |
| `tick_task(plan_name, task_id)` | Mark a task done after completing work |
| `update_task_status(plan_name, task_id, status)` | Set status: `pending` / `in_progress` / `done` / `blocked` |
| `rename_plan(current_name, new_name)` | Rename a plan |
| `reorder_tasks(plan_name, ordered_ids[])` | Reorder tasks by ID list |
| `list_plans()` | List all plans with task counts |
| `delete_plan(plan_name)` | Delete a plan and all its tasks |

## Key patterns

**Always call `show_plan` after creating or modifying a plan** so the user sees the updated panel.

**Call `tick_task` automatically** when you finish work on a task — don't wait for the user to click the checkbox.

**Use `add_tasks` (plural) when populating from conversation** — one tool call, multiple tasks, single transaction.

**Use `update_task_status` with `in_progress`** before starting a task so the panel reflects what you're currently working on.

**Use `show_plans` with no arguments** when the user hasn't specified a plan name — lets them pick from the panel rather than typing.

## Orchestration pattern

Wingman is stateful plan infrastructure. An orchestrator agent can call Wingman tools as coordination primitives across a multi-agent workflow:

```
1. create_plan("Research sprint", [])
2. add_tasks(plan_name, [task_a, task_b, task_c])
3. update_task_status(plan_name, task_1_id, "in_progress")
   → delegate task_a to sub-agent
4. tick_task(plan_name, task_1_id)  ← sub-agent reports done
5. show_plan(plan_name)             ← updated panel reflects progress
```

Plans persist in local SQLite — state survives agent restarts and new conversations.

## Notes

- Plans are identified by name (unique, up to 64 chars). Alphanumeric + space, hyphen, underscore, apostrophe, period, colon, parentheses allowed.
- Task IDs are per-plan sequential (1..N display). Use `get_plan` to inspect current IDs before calling `tick_task` or `reorder_tasks`.
- The interactive panel renders in Claude Desktop and MCPJam (MCP Apps / SEP-1865). Cursor and VS Code receive clean text fallback — all tools still work.
- No telemetry. No network calls. Local SQLite only.
