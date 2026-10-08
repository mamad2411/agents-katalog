---
name: nrev-fix
description: Diagnose and fix failing nRev workflows — when a run errors, a node shows config errors, validation fails, rows fail silently (completed status but empty/errored data), an edit_workflow operation is refused, an API call returns 4xx/5xx, or auth/connection problems block a build. Maps symptoms to root cause to fix. Load whenever something doesn't work as expected.
---

# Troubleshooting

Diagnose in this order — **execution status → node output rows → node settings
→ parent output**. Most failures are schema mismatches between adjacent nodes,
not the node you're looking at. The single most important habit: **a
`completed` node status does NOT mean the rows succeeded** — always read
`get_node_output` and check each row's `error` field.

## Silent failures (the dangerous ones)

| Symptom | Cause | Fix |
|---|---|---|
| Node `completed`, 0 output rows | Upstream filter removed everything, or input was empty in test mode | `get_node_output` on the PARENT; check filter conditions; confirm seed table has rows |
| Run "succeeded" but terminal Slack/Sheets/CRM node didn't act | A mid-pipeline node emitted 0 rows, starving everything downstream — `get_execution` lists these under `zero_row_nodes` with a `warnings` note | Inspect the named node's config/output; do NOT recommend or launch a live run until the test run produces rows end to end |
| Node `completed`, every row has an `error` value | Per-row failure (Pipedream/nrev_tables especially) — not surfaced at node level | Read the `error` column; usually a bad `{{template}}` or missing connection |
| `{{column}}` renders literally / empty | Column doesn't exist upstream, or name mismatch (case, snake_case) | `get_node_output` on parent to see actual column names; fix the reference |
| Numeric comparison always false | Template resolved to a string ("5" vs 5) | Cast to number in an upstream Magic Node before comparing |
| Dropdown value rejected at runtime | Used a label instead of the option `value` | `describe_node` / `get_field_options`; pass `value`, put the label in `labels` |
| `get_node_preview` returns 0 rows unexpectedly | `limit` > 100 (silently zero) | Keep page size ≤ 100; use `download_node_output` for whole sets |

## Validation errors (before/after a run)

| Symptom | Cause | Fix |
|---|---|---|
| `node_config_error` on a node | Required setting unset or wrong shape | `get_workflow(view="node")` to read it; reconfigure with `update_node_settings`; reshape per the node-settings skill |
| Magic Node: "Input should be a valid dictionary or instance of CodeSection" | Code written as a bare string / empty list instead of the nested `code_section` envelope | Set the code via `update_node_settings(settings={"code": "..."})` — the tool builds the right shape (node-settings skill → Magic Node) |
| Magic Node: "Missing a field - instructions_and_ref" | Input references stored top-level instead of nested in the group | Wire the df1..dfN input edges (`edit_workflow`) — references are auto-maintained in the nested location; re-`validate_workflow` |
| `magic_reference_warnings` | Magic Node references an edge id that no longer exists (parent removed/rewired) | Re-add the input edge, or remove the stale reference by re-wiring; `validate_workflow` to confirm |
| `unconfigured_warnings` (advisory) | A downstream node has no settings at all (e.g. a Filter with no condition) — runs without a config error but silently passes/drops every row | Configure the node (`update_node_settings`), or confirm it genuinely needs none before running |
| `workflow_config_error` set | Graph-level problem (no start node, disconnected node, missing listener) | Ensure ≥1 start node; wire orphans; check `is_runable` |
| `is_runable: false` | Workflow not yet valid to run | Resolve all node + workflow errors first |

## edit_workflow refusals (OperationError)

These are intentional — the message names the rule and the escape. Don't fight
them; follow the remediation.

| Message gist | Why | What to do |
|---|---|---|
| "refusing a second `_default` edge" | Single-input rule | Use a Magic Node (df1…df5) to join; or `remove_edge` first to replace |
| "cannot be a workflow start node" | Action-only type as a root | Put a data source as the root and wire this downstream; `force_root=true` only for a genuine catalog edge case |
| "workflow already has a listener" | One-listener rule | `is_listener=false` (plain start node) or `force_demote_listener=true` |
| "Scheduler with is_listener=false" | Start node that never fires | Leave the Scheduler as listener for cron; use a real source for one-off runs |
| "missing required key" | Operation missing a field | Check the op shape in the edit_workflow docstring / workflow-examples skill |

## API errors (APIError: HTTP <status> from <url>)

| Status | Likely cause | Fix |
|---|---|---|
| 401 / "Not authenticated" | session missing or expired | `get_auth_status`; if unset/expired, call `auth_login` to re-sign-in (it opens the user's browser, then auto-refreshes). Don't ask the user for tokens or environments. |
| 403 | Token valid but not authorized for that tenant/resource | Confirm the resource belongs to the JWT's tenant |
| 404 on an UNVERIFIED endpoint | Wrapper path/shape not yet exercised against prod (plays summon, abort, variables, table delete) | Capture the real request from the web app's network tab and align the wrapper in `api.py`/`tables_api.py` |
| 405 on `delete_table` | Delete endpoint "not yet live" in this environment | Expected; surface to user — deletion unavailable for now |
| 413 | Full-workflow PUT too large | Should not happen via tools (per-node PUT for edge changes); if it does, the change was misclassified as structural |
| 422 | Bad body/params (e.g. limit > 100, wrong field shape) | Check caps (catalog/preview ≤100); reshape body; for input_data runs, verify the manual-trigger body key |
| 5xx | Platform-side | Retry; if persistent, capture and report |

## Connection / app problems

- App-backed node fails only **at run time**, not build time → confirm with
  `list_connections` BEFORE designing around the node. If missing, ask the user
  to connect the app in the platform UI.
- A teammate's connection may work for some apps (Gmail, Sheets) but fail for
  others (Google Calendar) — prefer the user's own connection_id.

## When you're stuck

1. `get_execution(execution_id)` → which node, what error.
2. `get_node_output` on the failing node AND its parent — compare columns.
3. `get_workflow(view="node", node_id=…)` → read the exact settings.
4. `describe_node` → re-confirm field names and option values you may have
   guessed.
5. Fix with `update_node_settings`; re-run with `run_node` + `prior_execution_id`;
   re-inspect. Change one thing at a time.
