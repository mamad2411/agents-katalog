---
name: plan-and-usage
description: Show Opsphere plan, trial, daily usage, execution budget, Personal Workspace, Work Context, and integrations. Use for plan/usage/limits/upgrade, ops_my_usage, or ops_execution_budget.
---

# Plan and usage

## Tool

First check the current MCP `tools/list`.

- If **`ops_my_usage`** is present, call it with no parameters.
- If the user specifically asks about investigation capacity or reset time and
  **`ops_execution_budget`** is present, call it with no parameters after
  `ops_my_usage`. It is available to eligible Team and Enterprise workspaces.
- If it is absent, do not call it and do not infer that Opsphere or the active
  workspace is disconnected. Explain that plan/usage is a Connection Hub or
  self-service control-plane capability and is not exposed by this direct
  corporate-workspace session. Operational provider tools advertised in the
  current list can still work normally.
- Do not invent plan, quota, Personal Workspace, Work Context, or integration
  status from the tool's absence. If `ops_list_integrations` is present, it may be
  used separately for live integration status; otherwise tell the user that an
  administrator or a Connection Hub login is needed for account-level details.

Good fallback:

> This direct workspace session does not expose the self-service plan/usage tool.
> That does not disable the workspace's operational integrations; I can still use
> the provider tools currently advertised. For account-level plan and quota
> details, use your Opsphere Connection Hub session or ask the workspace admin.

## Catalog and workspace measurements

Report `catalog.announcedToolCount` separately from workspace configured tools,
enabled modules, configured providers and plan eligibility. The stable public
catalog is not an authorization list. Usage and subscription remain Hub-level;
operational configuration belongs to the active workspace, not the Hub. Unknown
availability must stay unknown, not become zero or "not configured". When
`catalog.mode` is `stable`, switching workspace needs no catalog reconnection.

## Response presentation (mandatory)

**Never** paste the raw MCP tool envelope (`content`, `type`, JSON-RPC, or a `json` code block of the full tool result).

1. Read the markdown inside the tool's `text` field.
2. Reply in **natural language** with short sections.
3. Use bullets or a compact table — not a code fence unless the user explicitly asks for raw JSON.

### Present these concepts separately

| Section | How to phrase |
|---------|----------------|
| Connection | Opsphere **connected** |
| Plan | e.g. Community (trial days if present) |
| Personal Workspace | Included automatically; say **Active** only when selected |
| Work Context | Configured / not configured — optional provider notes |
| External workspaces | Community: included Personal Workspace; additional links need upgrade. **Org invite:** same email + Developer+ may already show in `ops_accounts_list` — mention when user asks about a company invitation. |
| Integrations | Count / list next actions (Connect AWS, Datadog, …) if zero |
| Daily / monthly usage | From tool text |
| Current execution budget | From `ops_execution_budget`: workload, per-run calls/cost/macros/retries, automation daily runs/calls/cost, and reset times; keep separate from subscription usage |

### Good example

> You're **connected** on **Community** (trial ends 16 Aug 2026 — 30 days left).
>
> **Personal Workspace:** Active  
> **Work context:** Not configured — add details about the systems you usually work with anytime.  
> **Additional workspaces:** Your Personal Workspace is included; linking more requires Developer or higher.
>
> **Today:** 10 / 100 tool calls (resets midnight UTC).  
> **Integrations:** none yet — say _"Configure my Datadog"_ when ready.
>
> Need more capacity or external workspaces? See [opsphere.io/pricing](https://opsphere.io/pricing).

### Bad example (do not do this)

- Dumping raw MCP JSON
- Saying **"31 MCP tools enabled"** / **"20 MCP tools enabled"** / inventing a public tool count
- Implying Work Context "not configured" means Personal Workspace is broken
- Showing "0/0" external links without the upgrade explanation

## After presenting usage

- If the user asks about a **company invitation**, call `ops_accounts_list` — org workspace may already be linked (same email + Developer+). Otherwise point to upgrade or **`link-account`**.
- If Work Context is not configured, optionally offer `set-work-context` (does not block tools).
- If integrations are 0, offer `configure-integration` for providers allowed on the plan.
- On Community, do not promise Developer features unless plan status shows Developer is active.
- If the user asks to enable K8s / ArgoCD / macros on Community: those are outside Community — point to pricing.
