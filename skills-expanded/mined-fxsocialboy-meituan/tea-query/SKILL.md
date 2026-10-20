---
name: tea-query
description: Query TEA report information and data, including dashboards, reports, and report data. Use when the user mentions TEA, TEA dashboards, TEA reports, wants to list dashboards or query report data from TEA. Also trigger when the user provides a TEA URL or mentions querying DataFinder reports.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# TEA Query Skill

Query TEA-next (DataOpen) report information and data.

> **When to Use**: List dashboards, query report details, get report data from the TEA-next platform. Useful for checking dashboard contents, inspecting reports, and retrieving report data across regions.

## Quick Start

```bash
# List all dashboards for a project
gdpa-cli run tea-query --session-id "$SESSION_ID" --input '{
  "action": "list_dashboards",
  "region": "sg",
  "project_id": 12345
}'

# Get dashboard details
gdpa-cli run tea-query --session-id "$SESSION_ID" --input '{
  "action": "get_dashboard",
  "region": "sg",
  "project_id": 12345,
  "dashboard_id": "abc123"
}'

# List reports in a dashboard
gdpa-cli run tea-query --session-id "$SESSION_ID" --input '{
  "action": "list_reports",
  "region": "sg",
  "project_id": 12345,
  "dashboard_id": "abc123"
}'

# Query report data (core API)
gdpa-cli run tea-query --session-id "$SESSION_ID" --input '{
  "action": "query_report",
  "region": "sg",
  "project_id": 12345,
  "report_id": "rpt_456",
  "global_filter": {},
  "profile_filters": [],
  "skip_period_indexes": []
}'

# Get report info within a dashboard (without data)
gdpa-cli run tea-query --session-id "$SESSION_ID" --input '{
  "action": "get_report_in_dashboard",
  "region": "sg",
  "project_id": 12345,
  "dashboard_id": "abc123",
  "report_id": "rpt_456"
}'
```

## Supported Actions

### `list_dashboards`

List all dashboards the user has access to under a project.

**Required parameters**
- `action`: `list_dashboards`
- `region`: `cn` or `sg`
- `project_id`: TEA-next project ID (integer)

### `get_dashboard`

Get details of a specific dashboard.

**Required parameters**
- `action`: `get_dashboard`
- `region`: `cn` or `sg`
- `project_id`: TEA-next project ID
- `dashboard_id`: Dashboard ID (string)

### `list_reports`

List all reports/charts in a dashboard.

**Required parameters**
- `action`: `list_reports`
- `region`: `cn` or `sg`
- `project_id`: TEA-next project ID
- `dashboard_id`: Dashboard ID

### `query_report`

Query report information and data. This is the core interface for retrieving actual report data.

**Required parameters**
- `action`: `query_report`
- `region`: `cn` or `sg`
- `project_id`: TEA-next project ID
- `report_id`: Report ID (string)

**Optional parameters**
- `global_filter`: Global filter object (default: `{}`)
- `profile_filters`: User attribute filters (default: `[]`)
- `skip_period_indexes`: Time period indexes to skip (default: `[]`)
- `period`: Time range specification
- `param_filters`: Parameter filters
- `property_logic`: Property logic operator
- `replace_info`: Replace info for dynamic parameters

### `get_report_in_dashboard`

Get report info within a dashboard context (metadata only, no data).

**Required parameters**
- `action`: `get_report_in_dashboard`
- `region`: `cn` or `sg`
- `project_id`: TEA-next project ID
- `dashboard_id`: Dashboard ID
- `report_id`: Report ID

## Typical Workflow

When a user wants to query report data from TEA-next, follow this order:

1. Use `list_dashboards` to find available dashboards for the project
2. Use `list_reports` to see what reports/charts are in the dashboard
3. Use `query_report` to get the actual report data with desired filters

If the user already knows the `report_id`, skip directly to `query_report`.

## Region Mapping

| Region | DataOpen app management (view AppID / AppSecret) | API base |
|--------|--------------------------------------------------|----------|
| `cn` | [data.bytedance.net](https://data.bytedance.net/dataopen/tea-next/app) | `data.bytedance.net` |
| `sg` | [tea-captain.tiktok-row.net](https://tea-captain.tiktok-row.net/dataopen/tea-next/app) | `tea-captain.tiktok-row.net` |

## Rate Limits

All APIs share the same limits:
- QPS: 5
- Timeout: 300,000ms (5 minutes)
- Daily call limit: 100,000

## Required Authentication Setup

TEA-next uses DataOpen application credentials (`app_id` and `app_secret`) for authentication.

When credentials are missing, explain that TEA credentials are not configured for the region, tell the user to get `app_id` and `app_secret` from the **region-specific** DataOpen application page, then guide them to run:

```bash
gdpa-cli tea credential set --region <region>
```

This command interactively prompts for `app_id` and `app_secret` and saves them locally.

Additional credential commands:

```bash
# Show credential file path
gdpa-cli tea credential path

# Check whether a region is configured
gdpa-cli tea credential get --region sg

# Non-interactive usage
gdpa-cli tea credential set --region sg --app-id <app_id> --app-secret <app_secret>
```

To get the credentials, open the app page for your region and copy **AppID** and **AppSecret** from the application details (create an app and apply for the "看板&图表" permission package if needed):

- **CN**: [https://data.bytedance.net/dataopen/tea-next/app](https://data.bytedance.net/dataopen/tea-next/app)
- **SG**: [https://tea-captain.tiktok-row.net/dataopen/tea-next/app](https://tea-captain.tiktok-row.net/dataopen/tea-next/app)

If credentials are missing, the agent response may include structured onboarding fields such as `setup_required`, `credential_page_url`, and `next_command`. Prefer those fields when explaining the next step (same pattern as Aeolus).

If the CLI reports missing credentials, the recommended guidance is:
1. Explain that TEA credentials are not configured for the requested region
2. Point the user to the DataOpen application page for that region (use `credential_page_url` when present)
3. Tell them to run `gdpa-cli tea credential set --region <region>`
4. After setup, rerun the original request

## Notes

- `region` is required for every action
- `project_id` corresponds to the TEA-next project/application, visible in the TEA-next URL
- `dashboard_id` and `report_id` can be discovered via `list_dashboards` and `list_reports`
- The `query_report` API may have slow response times for complex reports (up to 5 minutes)
- If credentials are missing, the agent will return structured `setup_required` fields
