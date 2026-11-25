---
name: orbiads-reporting
description: Use for GAM reporting and analytics — delivery and inventory reports, availability forecasts, delivery-status checks, and PQL queries — through OrbiAds MCP actions or their orbiads CLI equivalents. Examples: "run a delivery report", "forecast availability for this line item", "check delivery status". Catalogue reads are free; each report run or export costs 0.5 credit.
version: 1.0.0
author: OrbiAds
license: MIT
metadata:
  group: reporting
  tags: [orbiads, gam, adops, reporting, forecast]
  related_skills: [orbiads]
  parent_mcp_tools:
    - mcm
    - pql
    - preview
    - reporting
  action_count: 40
  cli_coverage: partial
  read_only: false
user-invocable: false
---

<!--
  ⚠️ GENERATED ARTIFACT — generation source lives in the private OrbiAds monorepo.
  Do not hand-edit; open an issue or PR against documentation/examples instead.
-->

# OrbiAds GAM — Reporting, Forecasting & Delivery Analytics

_Run delivery and inventory reports, check prospective or standalone availability forecasts, and execute PQL queries._

**Mode:** mixed (read + write) · **Tools included:** 4 · **Total actions:** 40 · **CLI coverage:** partial (36/40 actions)

Parent MCP tools: `mcm`, `pql`, `preview`, `reporting`.

## Surfaces

OrbiAds exposes the same backend through two surfaces; **MCP is the default**. A subset of actions also has a CLI command (`cli_coverage: partial` — 36/40 actions here). Per-action availability (MCP command vs `orbiads <command>` vs `MCP-only`) is listed in [`references/actions.md`](references/actions.md).

**Rule:** if an action is marked `MCP-only` in that table, fall back to the MCP surface (or the web app) for it — never improvise a raw REST call or shell around the CLI.

## CLI usage

```bash
pip install orbiads-cli
orbiads auth status --json     # verify you are authenticated first
orbiads network info --json    # confirm the active tenant / network
```

- Always pass `--json` so the agent parses structured output, never scraped text.
- **CLI gap → fall back to MCP for that action; never shell out around the CLI.**

## Safety Contract

- **Most reads are free; writes and heavy reads cost credits** (e.g. a report run or export costs 0.5 credit). Call free reads liberally for state discovery before any mutation.
- **preview → confirm → execute.** Every write runs once with `dry_run=true` (or no `confirmation_token`) to return a preview + token + cost, then again with the same payload + `confirmation_token`. Get explicit user consent between the two calls.
- **Never bypass `billing_guard`** and never reuse a stale token — payload drift returns `IDEMPOTENCY_KEY_MISMATCH`; refresh the preview.
- **Never invent identifiers.** Do not guess a `tenantId` / `networkCode` / advertiser / order id — resolve them from the session or a read first.
- **At most 2 write retries**, then stop and report.
- **Never leak raw SOAP/REST traces** to the user — surface the structured `error` object instead.
- These rules apply identically on the MCP and CLI surfaces — a CLI write (`orbiads ... create/deploy`) needs the same preview + explicit user confirmation as an MCP write.

## Reporting grammar — get it right on the first try

### Date ranges

- Relative window: pass `dateRangeType` (aliases accepted: `date_range_type`, `dateRange`, `date_range`) with one of: `LAST_MONTH` (default), `LAST_WEEK`, `LAST_7_DAYS`, `LAST_30_DAYS`, `YESTERDAY`, `TODAY`, `CURRENT_MONTH`, `CURRENT_QUARTER`, `LAST_3_MONTHS`, `LAST_YEAR`.
- Custom window: `dateRangeType: "FIXED"` + `startDate` + `endDate` (YYYY-MM-DD).
- Exception: `fetch_inventory_report` has no relative-range param — pass `startDate`/`endDate` only (omit both for LAST_MONTH).
- `get_report_date_ranges`, `get_report_dimensions`, `get_report_metrics` are free (0 credit) — call them for the exact catalogue before composing a report.

### Dimension × metric compatibility (GAM-side)

GAM rejects some dimension/metric combinations at submission with `REPORT_ERROR_CONSTRAINTS_INCOMPATIBILITY` ("The report is invalid as specified and needs to be modified") **without naming the offending pair**. Live-observed examples: `VIDEO_AD_BREAK_TYPE_NAME` combined with `OPERATING_SYSTEM_CATEGORY_NAME` or `DEVICE_CATEGORY_NAME`; `INVENTORY_FORMAT_NAME` with fill-rate metrics.

When a report is rejected:

1. Credits are refunded automatically — a rejected submission never bills.
2. Retry with `expandedCompatibility: true` to relax GAM's field-pairing checks.
3. Still rejected → split into single-dimension reports and join the rows client-side (dimension values are stable join keys).

## Full action catalogue

Full action catalogue (costs, write flags, confirmation tokens, CLI equivalents): read [`references/actions.md`](references/actions.md).

## Routing back to the orchestrator

This sub-skill is `user-invocable: false`. The `orbiads` orchestrator ([`../orbiads/SKILL.md`](../orbiads/SKILL.md)) routes intents — and the MCP-vs-CLI surface choice — to these tools based on its routing table. If you load this file directly, you bypass the orchestrator's context intake — re-route through the orchestrator unless you already know exactly which action to call.
