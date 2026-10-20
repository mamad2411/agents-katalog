---
name: noibu-analytics
description: Noibu ecommerce analytics on Opsphere — routing (querying-noibu-data), Store Pulse text snapshots, issues, and session/page KPIs. Use when the user asks about conversion, store health, checkout errors, Noibu domains, or "how is the store doing".
---

# Noibu analytics (Opsphere)

Use **Opsphere MCP** `noibu_*` tools on the remote gateway. Noibu is **not** configured via `ops_configure_integration` — the tenant links **one** OAuth connection in **Admin → Integrations → Noibu** (`noibu_link_start` / `noibu_link_status`, `scope: tenant`).

**Explicit opt-out is authoritative.** If the user refused Opsphere for this task, do not call Noibu tools indirectly.

## Before any data call

1. Call `noibu_link_status`. Proceed only when `linked: true` and `scope: tenant`. If `linked: false` or `expires_at` is soon/past, a tenant admin must reconnect in Admin — QA automations fail loudly when the link is stale (same-day token expiry is normal; refresh happens on data calls when possible).
2. Confirm `noibu_domains_list` (or another `noibu_*` data tool) appears in `tools/list` — module `noibu` must be enabled for the workspace **profile** in use (Cursor automation → **cursor** profile; Admin Connect → **web** profile).
3. Read **`references/querying-noibu-data-routing.md`** — same routing semantics as Noibu's [querying-noibu-data](https://github.com/Noibu/ai-plugin/blob/main/src/skills/querying-noibu-data/SKILL.md), with Opsphere tool names.
4. Read **`references/opsphere-broker-tools.md`** — JSON under **`input`**, optional top-level **`rationale`** and **`preset: checkout`** on `noibu_issues_search`.
5. Read **`references/opsphere-broker-aliases.md`** when calling diagnosis, trends, session lookup, or grouped page visits (Opsphere vs upstream argument names).
6. For **weekly checkout Slack jobs**, the full run prompt is **not** in this repo — maintain it in Cursor Automation. Public contract: **`references/weekly-checkout-health-automation.md`** and **`references/noibu-console-links-automation.md`** (`noibuConsoleLinks`, `issueUrl` in Slack).

Field-level measure docs remain on Noibu's GitHub (`references/sessions.md`, `references/page-visits.md`, `references/errors.md`, … under [ai-plugin](https://github.com/Noibu/ai-plugin/tree/main/src/skills/querying-noibu-data/references)).

## Intent routing

| User intent | Follow |
|-------------|--------|
| Conversion, revenue, AOV, traffic sources, cohorts, funnels (counts) | `querying-noibu-data` routing → usually `noibu_sessions_search` |
| Per-page traffic, web vitals, scroll/clicks, landing/exit | `noibu_page_visits` |
| **Store health**, "how's the store", daily snapshot, pulse | **`references/store-pulse-opsphere.md`** (text-first; no Cowork widgets) |
| Errors / bugs / issues (explicit) | `noibu_issues_search` with **`preset: checkout`** for payment/cart/checkout lists; `noibu_issue_get` for drill-down |
| AI issue explanation | `noibu_error_diagnosis_get` — Opsphere **`errorIds`** (broker → upstream `issueIds`) |
| Issue volume over time | `noibu_error_trends_get` — `domainId` + `issueId`/`issueIds` + optional `days` (broker sets intervals) |
| Top sessions for an issue | `noibu_issue_session_highlights_get` |
| Single session drill-down | `noibu_sessions_lookup` — nested `periodOptions.dateTimeRange` + `queryInput` |
| Domain / company scope | `noibu_domains_list`, `noibu_domain_get` — always `{ "input": { "name": "<hostname>" } }`, `noibu_company_get` |

Lead with **analytics** unless the user explicitly asks about errors.

## Store Pulse on Opsphere

When the user wants an at-a-glance **last 24h** health read (same intent as Noibu's [store-pulse](https://github.com/Noibu/ai-plugin/blob/main/src/skills/store-pulse/SKILL.md)):

1. Open **`references/store-pulse-opsphere.md`** and execute that workflow.
2. Use measure definitions from Noibu's [core-kpis](https://github.com/Noibu/ai-plugin/blob/main/src/skills/store-pulse/references/blocks/core-kpis.md) and [purchase-funnel](https://github.com/Noibu/ai-plugin/blob/main/src/skills/store-pulse/references/blocks/purchase-funnel.md) blocks inside `noibu_sessions_search`.
3. Present a short prose summary (KPI row + funnel steps + one investigative follow-up). **Do not** call `show_widget`, `create_artifact`, `list_artifacts`, or schedule tools — they are not brokered.

## Cursor Automation guardrails

For a scheduled Cursor background run, use only the existing atomic `noibu_*` tools; there is no Opsphere Noibu macro in this release.

1. Call `ops_execution_budget` once at the start, once after the KPI phase, and once after the issues phase when the tool is advertised. At the start, require the authoritative response to report `workload_type: automation`, `classification.entitlement_valid: true`, and `classification.run_session_valid: true`; otherwise stop and report incorrect Automation MCP configuration. Do not poll it before every call.
2. Use a fixed plan of at most 48 Noibu data calls for the complete run. Do not start a phase unless the reported remaining budget covers that phase's declared maximum.
3. Retry an invalid Noibu query at most once after correcting its arguments from the bundled references. Do not rediscover schemas during the run.
4. If any denial reports `terminal_for_run=true`, stop immediately and produce the best partial report from evidence already collected. Do not wait for reset or open a replacement session.
5. Do not search repositories, memory, unrelated resources, or other tenants to complete the report.

## Opsphere vs official Noibu MCP

Full allowlist and JSON examples: **`references/opsphere-broker-tools.md`**. Broker-only rewrites: **`references/opsphere-broker-aliases.md`**.

Upstream arguments belong under **`input`**. Siblings on the Opsphere tool: **`rationale`** (always) and **`preset: checkout`** on `noibu_issues_search` when the user wants checkout/payment issue lists.

## Console links in reports

After **`noibu_domain_get`**, **`noibu_issues_search`**, or **`noibu_issue_get`**, use `structuredContent.data.noibuConsoleLinks` and row-level **`issueUrl`** when present. See **`references/noibu-console-links-automation.md`**. Do not fabricate `console.noibu.com` issue paths.

## Out of scope (Opsphere allowlist)

Writes, AB tests, replays, platform logs, visualizations (`noibu_visualize_page_visits`), feedback, releases, and Cowork UI are **not** brokered. Say so clearly and point to the official Noibu MCP or Noibu Console when the user asks for those capabilities.

## Report

- State domain name and UUID used, time window (UTC), and sibling-domain checks when conversion looked zero.
- Separate live tool results from inference.
- If tools return GraphQL or validation errors, quote the gateway message; fix args using `references/opsphere-broker-tools.md` and **`references/opsphere-broker-aliases.md`** before retrying (one correction retry in automations).
- For issues in Slack or markdown reports, link with upstream **`issueUrl`** or **`noibuConsoleLinks`** — never fabricate console issue paths.
