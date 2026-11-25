---
name: oriflux
description: Oriflux — cookieless web + product + API analytics over your own Oriflux instance. Use when the user wants to see traffic, visitors, sessions, bounce rate, geographic breakdowns, or API health (request volume, error rates, latency) for a Sponge Theory product, or run a typed metric query. All access goes through the oriflux MCP tools; the instance URL and read key come from the plugin configuration (never hardcode a key).
---

# Oriflux — analytics in Claude Code

You have access to **Oriflux** by **Sponge Theory**: a self-hosted, cookieless,
multi-tenant analytics platform unifying **web analytics + product analytics +
API analytics**. The MCP server is declared in this plugin's `.mcp.json` and
authenticated over HTTPS with the Oriflux instance URL and a **read-scoped API
key** (`ofx_read_…`) the user entered when enabling the plugin (Claude Code
native configuration). **No credential is baked into this plugin** and no key
ever appears in tool arguments — the transport adds the `Authorization: Bearer`
header for you.

The MCP surface is **read-only**: every tool is the same REST endpoint the
dashboard uses, compiled through Oriflux's typed metric/dimension registry, so
answers can never drift from the UI. A read key cannot write.

## Core concepts

- **Project** — a product / property being measured (e.g. AudiGEO, NeoRAG,
  sponge-theory.ai). Everything is scoped to a project, identified by its slug.
- **Metric registry** — metrics and dimensions are a hand-maintained, typed
  registry (not free-form SQL). A `query_metrics` validation error lists the
  available metric/dimension names, so a bad call self-repairs.
- **Period** — a `{start, end}` window. Multi-day visitor totals are **visit-days**
  (Oriflux rotates the visitor hash daily for privacy, PRD §9) — the tools say so
  in their responses; report them as visit-days, not unique people.

## Available tools (read-only, live today)

1. **`list_projects`** — projects (products) visible to the key's organization.
   Start here when the target project is unknown or ambiguous.
2. **`get_overview`** — headline numbers for a project over a period: visitors,
   pageviews, sessions, bounce rate, session duration, API requests, error rates,
   p95.
3. **`query_metrics`** — the typed query object (`metric, dimensions, filters,
   granularity, period, compare_to`), identical schema to `POST /api/v1/query`.
   Returns rows **and** the executed SQL for auditability. Use for anything beyond
   the overview: time series, breakdowns by dimension, comparisons.
4. **`get_geo_breakdown`** — geographic distribution for a project (country /
   region / city level) for a metric over a period, sorted.
5. **`get_api_health`** — API request volume, 4xx/5xx rates, p50/p95/p99 latency,
   and top endpoints for a project over a period.

## Typical workflow

1. **Identify the project.** If it's not obvious, call `list_projects` and pick
   the matching slug (or ask when genuinely ambiguous).
2. **Frame the question.** For a quick health read, `get_overview`. For "where is
   traffic from", `get_geo_breakdown`. For "how is the API doing", `get_api_health`.
   For anything custom (a specific metric over time, a breakdown by a dimension,
   or a comparison to a prior period), `query_metrics`.
3. **Cite the numbers.** When you report figures, ground them in what the tool
   returned; for `query_metrics`, the response includes the executed SQL — mention
   it when auditability matters. Never invent numbers Oriflux didn't return.

## Guidance

- This is a **read-only** analytics surface — there is nothing destructive to
  confirm. If a user asks to change data, explain that the plugin's read key
  cannot write.
- Prefer `get_overview` / `get_geo_breakdown` / `get_api_health` for their
  respective shaped answers; reach for `query_metrics` when you need a metric,
  dimension, granularity or comparison those don't cover.
- If a `query_metrics` call is rejected, read the returned list of valid
  metric/dimension names and retry with a correct one rather than guessing.
- Some advanced tools (funnels, retention, insights, alerts, natural-language
  "ask Oriflux") are part of the Oriflux roadmap and may not yet be available on
  a given instance — if a tool call returns not-found / not-implemented, fall
  back to the read-only tools above.

## Privacy

Oriflux is cookieless and GDPR-first by design; all data stays within the user's
own Oriflux instance and AI never sees raw events, only aggregates. The read key
is stored in Claude Code's native `userConfig` (masked, system keychain) and is
sent only to that instance over HTTPS.
