---
name: argos-dashboard
description: Manage Argos custom dashboards — list / get / save / delete dashboards by id, or quickly build a multi-metric dashboard from a list of metric names. Use whenever the user wants to browse their dashboards, create / update / delete an Argos custom dashboard, set up a metrics dashboard for a service, or fetch the JSON of an existing dashboard. Also trigger when the user mentions Argos dashboard, 自定义看板, dashboard URL, list dashboards, 我的看板, or wants to wrap a few metric names into a quick monitoring view.
---

> **session_id 传递**：若本次任务需要在多次 `gdpa-cli run` 之间串联 workflow 状态、日志或上下文，请复用同一个 `session_id`。如果当前 skill / Agent 已经提供了 `session_id`，**请直接复用，不要新建**。
>
> - **已有时优先复用**：不要重复执行 `create-session`。
> - **没有时再创建**：执行 `gdpa-cli create-session`。
> - **后续调用**：可以显式传 `--session-id <session_id>`，例如 `gdpa-cli run <agent> --session-id <session_id> --input '{...}'`。
> - **适用场景**：Base Workflow、BITS Dev Workflow、post-coding-verify 及其他依赖 Session 工作目录的场景需要持续复用；普通单次查询通常可以不传。

# Argos-Dashboard Agent

Manage Argos custom dashboards across CN / I18N / TTP / BOE control planes — the same dashboards backed by the Web editor at `cloud.tiktok-row.net/argos/dashboard/...` (I18N) and `cloud.bytedance.net/argos/dashboard/...` (CN).

> **When to Use**: Build a quick metrics dashboard for one or more metric names, fetch / save / delete an existing dashboard by id, or apply edits captured via `get_dashboard` round-trip.

> **IMPORTANT Safety Rules**:
> 1. **MUST follow two-phase workflow for writes**: For `save_dashboard` / `delete_dashboard` / `build_simple_dashboard`, always run preview first (without `confirm`), show the result to the user, and wait for explicit user approval before re-running with `"confirm": true`. NEVER skip the preview phase.
> 2. **NEVER change the target region**: Only operate on the exact `vregion` the user requested. If a region fails (timeout, network error), report the error — do NOT silently switch.
> 3. **NEVER auto-retry with different parameters**: If a call fails, report the failure and let the user decide. Do NOT silently switch id, name, or body content.
> 4. **Owner scope only**: This skill authenticates via the current `gdpa-cli login` user JWT — it works only for dashboards the caller can edit in the Web UI. Cross-team writes are out of scope.
> 5. **For partial updates, ALWAYS pass `"auto_merge": true`** (or use the get → edit → save round-trip). Argos's save endpoint is a **full replacement**: any field omitted from the body falls back to server defaults, which silently blanks panels (e.g. `enable_show_data` defaults to `false`, so the panel stops querying data). See [Updating an Existing Dashboard Safely](#updating-an-existing-dashboard-safely) below.
> 6. **When the user gives metric names for `build_simple_dashboard`, run the `metrics` skill first** to confirm the metric exists and inspect its tags. Show the discovered tag set to the user before proceeding — this catches typos and gives the user a chance to add `psm`/tag filters that the simple builder otherwise leaves empty. See [Pre-flight Tag Inspection](#pre-flight-tag-inspection-with-metrics).

> **session_id（推荐带上）**：`--session-id` 技术上可省略，但**推荐一律带上**，把同一轮多次调用串到同一个 session 里便于回溯与日志关联。首次跑 `export SID=${SID:-$(gdpa-cli create-session)}`，后续命令统一用 `--session-id "$SID"`。

## Quick Start

```bash
# 1. List the dashboards I own (read)
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"list_dashboards", "vregion":"sg"
}'
# Optional filters: search/folder/view/page/size/sort_by/sort_desc
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"list_dashboards", "vregion":"sg",
  "search":"skill", "view":"my", "folder":"GDPA", "page":1, "size":20
}'

# 2. Get an existing dashboard by id (read)
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"get_dashboard", "vregion":"sg", "id":"69e8a8b02adb5e60a7ddaabb"
}'

# 3. Build a simple multi-metric dashboard — MUST be two-phase
# Phase 1: preview (no confirm)
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"build_simple_dashboard", "vregion":"sg",
  "name":"GDPA Skill 实时看板",
  "metrics":[
    "gdp.event_collector.agent.execution.rate",
    "gdp.event_collector.agent.execution.timer.avg"
  ],
  "level":"P2",
  "folder":"GDPA"
}'
# >>> Show data.preview to the user, wait for explicit confirmation <<<

# Phase 2: ONLY after user confirms
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"build_simple_dashboard", "vregion":"sg",
  "name":"GDPA Skill 实时看板",
  "metrics":[
    "gdp.event_collector.agent.execution.rate",
    "gdp.event_collector.agent.execution.timer.avg"
  ],
  "level":"P2",
  "folder":"GDPA",
  "confirm": true
}'

# 3. Save (create or update) a dashboard from a full body — same two-phase pattern
# When body.dashboard.id is empty/missing -> create. When present -> update.
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"save_dashboard", "vregion":"sg",
  "body": { "meta": {"name":"...","level":"P2","region":"sg","..."}, "dashboard":{"panels":[...]} }
}'   # preview, then re-run with "confirm": true

# 3b. Safe partial update: change only a couple of fields without losing the rest
#     auto_merge=true makes the agent GET the existing dashboard, deep-merge
#     your patch on top, and save the merged body. Preview shows the FINAL
#     merged body so you can sanity-check before confirming.
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"save_dashboard", "vregion":"sg",
  "auto_merge": true,
  "body": {
    "dashboard": { "id": "<dashboard-id>" },
    "meta":      { "name": "renamed dashboard" }
  }
}'   # preview (already merged), then re-run with "confirm": true

# 4. Delete a dashboard by id — two-phase
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"delete_dashboard", "vregion":"sg", "id":"<dashboard-id>"
}'   # preview, then re-run with "confirm": true
```

## Actions

| Action | Scope | Endpoint |
|---|---|---|
| `list_dashboards` | read | `POST /monitor_data/custom/home/dashboards` |
| `get_dashboard` | read | `GET /monitor_data/custom/dashboards/{id}` |
| `save_dashboard` | **write (two-phase)** | `POST /monitor_data/custom/dashboards` |
| `delete_dashboard` | **write (two-phase)** | `DELETE /monitor_data/custom/dashboards/{id}` |
| `build_simple_dashboard` | **write (two-phase)** | `POST /monitor_data/custom/dashboards` |

## Input Parameters

### Required per action

| Action | Required |
|---|---|
| `list_dashboards` | `action`, `vregion` (all filters optional) |
| `get_dashboard` / `delete_dashboard` | `action`, `vregion`, `id` |
| `save_dashboard` | `action`, `vregion`, `body` (or `dashboard_body`) |
| `build_simple_dashboard` | `action`, `vregion`, `name`, `metrics` (string array, ≥1) |

### Common

| Parameter | Type | Description |
|---|---|---|
| `vregion` | string | `cn` / `china-east` / `sg` / `us` / `ttp` / `euttp` / `boe` (aliases) or full name. See VRegion table |
| `id` | string | Dashboard id (24-char hex token from the Web URL) |
| `body` / `dashboard_body` | object \| string | Full save payload `{meta, dashboard, commit_message?}`. Accepts typed map or raw JSON string |
| `confirm` | bool | **Must be literal `true`** for writes to execute. Strings `"true"` / `1` / `"yes"` are ignored on purpose |
| `auto_merge` | bool | (`save_dashboard` only) When `true` and `body.dashboard.id` is set, agent does a **GET → deep-merge → save** round-trip so missing fields in your patch are preserved from the current server-side body. Strongly recommended for any partial update. Ignored on create flows (no `dashboard.id`). |

### `list_dashboards` filters

| Parameter | Type | Description |
|---|---|---|
| `search` | string | Optional keyword filter (matches name/description on the server side) |
| `view` | string | `my` (default) / `all` / `stared`. `my` = dashboards where the caller is owner/editor |
| `folder` | string | Optional folder name filter |
| `page` | int | Page number, 1-indexed (default `1`) |
| `size` | int | Page size (default `20`, capped at `200`) |
| `sort_by` | string | Optional sort key (e.g. `name`, `updated_at`) — server default is `name` |
| `sort_desc` | bool | Optional sort direction. Only forwarded when set; server default is `true` |

### `build_simple_dashboard` shorthand

| Parameter | Type | Description |
|---|---|---|
| `name` | string | Dashboard title |
| `metrics` | []string \| comma-separated string | One panel per metric, stacked vertically |
| `level` | string | `P0` / `P1` / `P2` (default `P2`). Argos rejects other values |
| `folder` | string | Optional folder name |
| `description` | string | Optional dashboard description |
| `psm` | string | Optional pre-fill for query `psm` filter |
| `time_from` / `time_to` | string | Default `now-1h` / `now` |
| `commit_message` | string | Optional commit message attached to this save |

### Diagnostics

| Parameter | Type | Notes |
|---|---|---|
| `debug` | bool | Log outgoing HTTP body and raw envelope to stderr |

## Output Format

Top level always: `{success, action, vregion, data?, error?}`.

### `list_dashboards`
```json
{
  "count": 2,
  "dashboards": [
    {
      "id": "69e8be70...",
      "name": "GDPA Skill Test Dashboard (api)",
      "description": "created by api test",
      "folder": "GDPA",
      "level": "P2",
      "creator": "laihongquan",
      "updated_at": 1776860784,
      "stared": false,
      "is_editor": true,
      "is_viewer": true,
      "is_admin": true,
      "url": "https://cloud.tiktok-row.net/argos/dashboard/69e8be70..."
    }
  ],
  "page_info": { "page": 1, "size": 20, "by": "name", "desc": true, "total": 2 }
}
```

### `get_dashboard`
```json
{
  "id": "69e8a8b0...",
  "url": "https://cloud.tiktok-row.net/argos/dashboard/69e8a8b0...",
  "name": "GDPA Skill 实时看板",
  "dashboard": { "meta": {...}, "dashboard": {"panels":[...]} }
}
```

### `save_dashboard` / `build_simple_dashboard` — confirmed
```json
{
  "id": "69e8a8b0...",
  "url": "https://cloud.tiktok-row.net/argos/dashboard/69e8a8b0...",
  "detail": { /* server-returned body, may include the full saved dashboard */ }
}
```

### `delete_dashboard` — confirmed
```json
{ "id": "<deleted-id>", "detail": {} }
```

### Write actions — preview (no `confirm`)
```json
{
  "requires_confirmation": true,
  "hint": "Re-run the same call with \"confirm\": true to execute this write.",
  "preview": {
    "action": "...",
    "method": "POST (create)|POST (update)|DELETE",
    "endpoint": "/monitor_data/custom/dashboards[/{id}]",
    "vregion": "...",
    "body": { /* full body that will be sent */ },
    "id": "..."
  }
}
```

## Two-Phase Workflow for Writes (MANDATORY)

**Every `save_dashboard` / `delete_dashboard` / `build_simple_dashboard` call must go through both phases. NEVER skip Phase 1.**

1. **Phase 1 — Preview** (no `confirm` or `confirm=false`): Agent assembles the body it *would* send (or the id it *would* delete) but does NOT call the server. `data.requires_confirmation=true` and `data.preview` carry the full plan. **Show `data.preview` to the user and wait for explicit approval.**
2. **Phase 2 — Execute** (`"confirm": true`): Same input plus `confirm: true`. Agent re-validates and calls the server. Returns the new/target id plus a Web editor URL.

**Update vs create** is decided by `body.dashboard.id`: missing/empty → create, present → update. The preview labels the method as `POST (create)` or `POST (update)` accordingly.

## Updating an Existing Dashboard Safely

Argos's `POST /monitor_data/custom/dashboards` is a **full-body replacement**, not a JSON Merge Patch. **Any field you omit from the body falls back to the server's default value.** For panel-display fields the defaults are mostly `false` / empty, which silently breaks panels — most notably:

| Field | Server default when missing | Effect |
|---|---|---|
| `enable_show_data` | `false` | Panel stops querying / drawing data — looks empty |
| `is_percent` | `false` | Percentage rendering off |
| `is_thresholds` | `false` | Threshold lines disappear |
| `gauge_upper_bound` | `0` | Gauge upper bound resets |
| `tooltip_mode` | `""` | Tooltip rendering reverts to base mode |

You have two safe ways to avoid this:

### Option A (preferred): `"auto_merge": true`
Pass `auto_merge: true` on `save_dashboard`. The agent will:
1. `GET` the current dashboard body referenced by `body.dashboard.id`
2. Deep-merge your patch on top (patch wins for any overlapping key, server-side fields preserved for everything you didn't send; **arrays are wholesale-replaced** so to edit panels send the full panels array)
3. Use the merged body for both the preview AND the eventual save

The preview output sets `data.preview.auto_merged: true` so the user can see the merge happened, and the final body in `data.preview.body` is exactly what will be sent.

### Option B: Manual round-trip (always safe)
Use the `get_dashboard` → local edit → `save_dashboard` pattern explicitly. This gives you maximum control if you need to selectively delete keys (which `auto_merge` cannot express).

```bash
# Step 1 — fetch full body
gdpa-cli run argos-dashboard --session-id "$SID" --input '{
  "action":"get_dashboard","vregion":"sg","id":"<id>"
}' > /tmp/dash.json

# Step 2 — edit /tmp/dash.json locally (data.dashboard is the {meta, dashboard:{...}} envelope)
# Step 3 — save the full edited body
gdpa-cli run argos-dashboard --session-id "$SID" --input "$(jq -cn \
  --argjson body "$(jq '.data.dashboard' /tmp/dash.json)" \
  '{action:"save_dashboard", vregion:"sg", body: $body}')"
# preview, then confirm
```

> **Heuristic**: if the user is updating an existing dashboard (any time `body.dashboard.id` is present in their patch and they only sent a subset of fields), default to `auto_merge: true`. Skip it ONLY when the user explicitly wants to reset fields to server defaults.

## Pre-flight Tag Inspection (with `metrics`)

`build_simple_dashboard` is fast but minimal — every panel is a graph with empty tag filters and a single `psm` slot. Before building, **inspect the metric's actual tag set with the `metrics` skill** so you (and the user) know:

- whether the metric exists in the target region at all
- which tag keys are available (so the user can decide which ones to filter on)
- typical tag values (e.g. is `psm` always present? are there per-region tags?)

```bash
# Discover available tag keys for a metric (does NOT pull data, cheap)
gdpa-cli run metrics --session-id "$SID" --input '{
  "action":"suggest_tagk",
  "metric_name":"gdp.event_collector.agent.execution.rate",
  "vregion":"Singapore-Central"
}'
```

If the call returns nothing, the metric name is wrong or not yet reported in that region — surface that to the user before building a dashboard that will look empty. If tags surface a meaningful `psm`, pass it through to `build_simple_dashboard` via the `psm` parameter so panels start out filtered to the right service.

## Panel Render Cheatsheet (lessons learned)

When you assemble or hand-edit panels (either through `build_simple_dashboard` or by patching `body.dashboard.panels` for `save_dashboard`), the Argos editor JSON has a few non-obvious fields whose absence makes a panel render as an empty placeholder even though `enable_show_data:true` and the metric clearly has data:

| Field | Required value | Why it matters |
|---|---|---|
| `panels[].id` | 24-hex string (UUID-shaped) | Empty → frontend skips the per-panel data fetch entirely |
| `panels[].queries[].key` | 24-hex string | Same as above — per-query identifier the renderer uses |
| `panels[].aggrs` | `["min","max","avg"]` (or any subset that matches your `aggr`) | Without `aggrs` no series lines are drawn even though data is fetched |
| `panels[].queries[].disabled` | **`true`** | Counter-intuitive: in Argos UI semantics `disabled:true` ≡ "committed query"; `disabled:false` keeps the query in scratchpad mode and the data toggle defaults to OFF (greyed-out eye icon) |
| `panels[].mode` | `"markdown"` | Description-editor mode; the editor always writes it |
| `panels[].content` | `""` | Description-editor body |
| `panels[].enable_composition` / `enable_data_point` / `graph_stack` | `false` (explicit) | Server defaults are fine, but making them explicit prevents future schema regressions |

`build_simple_dashboard` already bakes all of the above into every panel it generates (see `buildMetricPanel` in `agent.go`). When you write your own dashboard JSON or merge in panels from elsewhere, copy the working panel shape — comparing against a UI-built reference dashboard is the fastest way to catch missing fields.

## VRegion Mapping

| VRegion | Aliases | Dashboard Gateway | JWT Site |
|---|---|---|---|
| `China-North` | `cn`, `china` | `aiops-argos.byted.org` | CN |
| `China-East` | `china-east` | `aiops-argos.byted.org` | CN |
| `Singapore-Central` | `sg`, `singapore`, `i18n` | `aiops-argos-sg.tiktok-row.org` | I18N |
| `US-East` | `us`, `useast` | `aiops-argos-us.tiktok-row.org` | I18N |
| `US-TTP` / `US-TTP2` | `usttp`, `ttp` / `usttp2` | `aiops-argos-us.tiktok-row.org` | TTP |
| `EU-TTP` / `EU-TTP2` | `euttp` / `euttp2` | `aiops-argos-sg.tiktok-row.org` | I18N |
| `China-BOE` | `boe`, `cn-boe` | `aiops-argos.boe.byted.org` | BOE |

> `meta.region` in the body is set automatically by `build_simple_dashboard` to the short code (`cn` / `sg` / `us` / `boe`) matching the chosen vregion. When passing your own `body`, set this field to match the gateway or the editor will reject the save with `region mismatch`.

## Auth

User JWT via `gdpa-cli login`，按 vregion 自动选 CN / i18n / ttp / boe site。所有读/写都走这条路径。**仅支持 owner 自己看板的操作**；非 owner 写入不在 skill 范围内。

JWT 失效或 site 不匹配时报 `authentication failed` 或 `getKeyLookupFunc: not support region`，重新 `gdpa-cli login` 即可。

## Error Handling

### Agent-side errors

| Error | Cause | Solution |
|---|---|---|
| `action is required` | Missing `action` | Set one of the 4 supported actions |
| `id is required for <action>` | `id` missing for get/delete | Pass `id` |
| `body ... is required` / `dashboard body is not valid JSON` | Missing/malformed body for save | Pass a valid `body` object or JSON string, or use `build_simple_dashboard` |
| `name is required` / `metrics is required` | Missing required input for `build_simple_dashboard` | Pass `name` and a non-empty `metrics` array |
| `view must be one of my/all/stared` | Invalid `view` for `list_dashboards` | Use `my`, `all`, or `stared` |
| `level must be one of P0/P1/P2` | Invalid `level` | Use `P0`, `P1`, or `P2` (Argos limit) |
| `unsupported vregion "..."` | Unknown vregion | Use a value from the VRegion table |
| `authentication failed` | JWT cache invalid/missing | Re-run `gdpa-cli login` |
| `requires_confirmation: true` in data | First write call without `confirm` | Show `data.preview` to user, then re-run with `"confirm": true` |

### Server-side business errors

Errors surface as `argos_dashboard API error (code=N): <message>` and the CLI tags them with an errcode category (AUTH-000 / API-001..004 / API-003).

| Symptom in `error_message` | Likely cause | Action |
|---|---|---|
| `need user jwt` / `unauthenticated` | Missing or expired JWT | Re-run `gdpa-cli login` |
| `getKeyLookupFunc: not support region: <r>` | JWT site doesn't match the gateway | Verify the chosen `vregion` matches the JWT site you've logged into |
| `dashboard level must be one of P0, P1, P2` | Invalid `level` (e.g. `P3`) | Use `P0`, `P1`, or `P2` |
| `region mismatch` | `meta.region` in body disagrees with gateway region | Align `meta.region` with the gateway short code (`cn`/`sg`/`us`/`boe`) |
| HTTP 404 on get/delete | Dashboard id doesn't exist or has been deleted | Verify the id from the editor URL |
| Dashboard saves OK but **panels render empty** in the UI | Two common causes: (1) save body omitted display fields (`enable_show_data`, `is_percent`, etc.) → server reset them to defaults (Argos save is full-replacement); (2) panel JSON is missing render-critical fields (`panels[].id`, `queries[].key`, `aggrs`, or has `queries[].disabled:false` instead of `true`) | For (1): re-run `save_dashboard` with `"auto_merge": true`. For (2): see the [Panel Render Cheatsheet](#panel-render-cheatsheet-lessons-learned) and either let `build_simple_dashboard` build the panels, or copy the missing fields from a working UI-built reference panel |
| `auto_merge: failed to fetch existing dashboard ...` | The `dashboard.id` in your patch doesn't exist or the GET hit an upstream error | Verify the id (try `get_dashboard` standalone). For a brand-new dashboard, drop `auto_merge` (it auto-skips when no id is present anyway) |

## Notes

- **Reads vs writes**: `list_dashboards` and `get_dashboard` run immediately; the other three actions require Phase 1 preview + Phase 2 confirm. Never skip Phase 1.
- **`body`** is forwarded verbatim to Argos so the skill tracks server-side schema evolution automatically — pull a known-good dashboard via `get_dashboard`, edit, then `save_dashboard` to apply.
- **Partial updates**: Argos save is full-replacement, so a patch-style body would normally wipe untouched fields. Use `"auto_merge": true` to make `save_dashboard` do a GET → deep-merge → save round-trip (recommended). See [Updating an Existing Dashboard Safely](#updating-an-existing-dashboard-safely).
- **`build_simple_dashboard`** is a convenience for the common case (a few metric names, one panel each, default layout). It bakes in every field the Argos editor relies on to render data immediately — display flags (`enable_show_data:true`, `is_percent:true`, `is_thresholds:true`, `gauge_upper_bound:100`, `tooltip_mode:"all"`), aggregation lines (`aggrs:["min","max","avg"]`), per-panel/query 24-hex IDs, and the counter-intuitive `queries[].disabled:true` "committed query" flag. See [Panel Render Cheatsheet](#panel-render-cheatsheet-lessons-learned) before hand-building panels.
- **Tag pre-flight**: when the user gives metric names, run `metrics suggest_tagk` first to confirm the metric exists and surface available tag keys. See [Pre-flight Tag Inspection](#pre-flight-tag-inspection-with-metrics).
- **Dashboard URL**: every successful read/write returns `data.url` so the user can open the dashboard in the Web editor directly.
- **Debug**: pass `"debug": true` to log the outgoing HTTP body on stderr — useful when the server rejects a payload field.
