---
name: marketer-dashboard
description: >
  Show live strategies, metrics, links, and campaigns via Link Platform MCP tools.
  Triggers: dashboard, metrics, overview, show dashboard, show metrics.
---

# Marketer Dashboard Skill

## Overview

Fetches all marketing data via Link Platform MCP tools (MCP is the only entry point — your server handles all auth and Link Platform calls) and displays a clean dashboard.

## When To Use

- "Show me the dashboard"
- "What strategies are live?"
- "Show my metrics"
- "Give me an overview"

## Prerequisites

- `USER_PAT` and `LINK_PLATFORM_HANDLE` env vars set

## Procedure

### Step 1: Fetch All Data via MCP Tools

Call in parallel:

```
agent_list_proposals({ handle: "<LINK_PLATFORM_HANDLE>", status: "live" })
agent_list_proposals({ handle: "<LINK_PLATFORM_HANDLE>", status: "draft" })
analytics_get({ handle: "<LINK_PLATFORM_HANDLE>" })
links_list({ handle: "<LINK_PLATFORM_HANDLE>" })
links_list({ handle: "<LINK_PLATFORM_HANDLE>" })
```

### Step 2: Display CLI Dashboard

```
==================================================
  MARKETING DASHBOARD — <handle>.10x.in
  Updated: <timestamp>
==================================================

STRATEGIES
  Live: <n>   Draft: <n>   Archived: <n>

LIVE STRATEGIES
  +------------------------+----------+--------+------------+
  | Name                   | Page     | Clicks | Conv. Rate |
  +------------------------+----------+--------+------------+
  | Summer Sale            | /summer  |  1,240 |   7.2%     |
  +------------------------+----------+--------+------------+

TOP PERFORMER: "<name>" — <rate>% conversion

LINKS    Total: <n>

PAGES    Total: <n>  Published: <n>  Draft: <n>
==================================================
```

### Step 3 (Optional): HTML Preview

If user wants a browser view, use `agent_start_run` to generate a dashboard HTML preview on the server.

## Suggested Next Actions

| Observation | Run |
|-------------|-----|
| Low conversion rate | `/lp-optimize` or `/lp-abtest` |
| Need an audit | `system_audit_events` or `/lp-audit` |
| No live strategies | `agent_create_proposal` (needs `idempotencyKey` + `strategyId`) + `landing-page` |
