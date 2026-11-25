---
name: helpdesk-demo-db
description: Query the helpdesk database (customers, agents, tickets) through the MCP SQL tool. Use whenever the user asks questions about support tickets, customers, agents, priorities, or resolution times — e.g. "how many open tickets do we have?", "which urgent tickets are unassigned?", "average resolution time by priority".
---

# Helpdesk database

The database is exposed as the MCP tool **`sql_helpdesk_demo`**. Answer questions by sending a single SQL query string (**T-SQL / SQL Server dialect**) to that tool. Results come back as JSON rows, truncated to the configured row limit (default 100) — use `TOP`, aggregation, or `ORDER BY` to keep result sets small and relevant.

## Schema

- **customers** — `id`, `email`, `full_name`, `company`
- **agents** — `id`, `full_name`, `team` (Tier 1, Tier 2)
- **tickets** — `id`, `customer_id` → customers, `agent_id` → agents (NULL = unassigned), `subject`, `priority` (`low`, `medium`, `high`, `urgent`), `status` (`open`, `pending`, `resolved`, `closed`), `created_at`, `resolved_at` (NULL until resolved/closed)

## Relations

- One customer has many tickets (`tickets.customer_id` → `customers.id`).
- One agent handles many tickets (`tickets.agent_id` → `agents.id`); `agent_id IS NULL` means the ticket is not assigned yet.

## Conventions

- **Dialect is T-SQL**: use `TOP n` (not `LIMIT`), `GETDATE()` for now, `DATEDIFF(hour, created_at, resolved_at)` for durations.
- A ticket is **outstanding** when `status IN ('open', 'pending')`; `resolved` and `closed` are finished.
- Resolution time only makes sense where `resolved_at IS NOT NULL`.
- "Backlog" questions usually mean outstanding tickets grouped by priority; urgent unassigned tickets (`priority = 'urgent' AND agent_id IS NULL`) are the ones worth flagging.

## Guidelines

- Treat the database as read-only: stick to `SELECT` unless the user explicitly asks to modify data.
- Prefer one well-formed query over many small ones; use joins and aggregates server-side.
