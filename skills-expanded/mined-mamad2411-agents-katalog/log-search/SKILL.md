---
name: log-search
description: Run a typed, time-bounded log search against Elasticsearch — refuses unbounded scans, aggregates by trace id / status / route, returns a short evidence packet.
---

# log-search

> A bounded, defensible Elasticsearch query for incident or PRD investigation. Output is the matching log count, top buckets, and a 10-sample evidence packet — never a raw 10k-row dump.

> **MCP binding (read before any tool call):** resolve which server backs `elastic` from `${POLYMATH_PLUGIN_DATA:-$HOME/.polymath/data}/polymath-core/project-context.json` `mcpResolution.elastic` — when `source` is `host`, the CURRENT host agent's own `elastic` MCP server is ALREADY registered: use its tools (`toolPrefix` gives the naming) and do NOT register or start a polymath copy. A server registered in a DIFFERENT agent is never a substitute. When `source` is `plugin`, the plugin-shipped `.mcp.json` server backs this skill. When `none`, credentials are unconfigured: ask the user to configure them or degrade gracefully. See the `polymath-core:mcp-bridge` skill.

## When to use

- An incident points at "logs say X" and you need the count, the buckets, and a small sample.
- A PRD asks "how often does Y happen in prod" — needs an aggregation, not a dump.
- A regression hunt across multiple services with a shared `trace.id`.

## Inputs

- Index pattern (required) — e.g. `logs-prod-*`. Refuse `*` (full-cluster scan).
- Time range (required) — explicit `gte` + `lte` ISO-8601 timestamps. Default `now-1h` only if no range provided AND `--allow-default-range` is set.
- Query (required) — KQL/Lucene string OR an Elastic Query DSL JSON body.
- Aggregations (optional) — bucket fields (e.g. `service.name`, `http.response.status_code`, `trace.id`).

## Procedure

1. **Validate the index pattern.** Refuse `*`, `*-*`, or anything with no leading namespace. Cluster-wide scans cost money and surface PII from unrelated indices.
2. **Validate the time range.** `gte` is required. Refuse "no time range" unless the caller explicitly opts in with `--allow-default-range`.
3. **Build the request.** Use `_search` with `track_total_hits=10000` (cap), `size=10` (sample), and `aggs` for the requested buckets. Set `terminate_after` to cap shard-side work.
4. **Run the search.** Capture `took`, `total.value`, `total.relation`. If `relation = "gte"`, the count is approximate — surface honestly.
5. **Bucket and sample.** Top 10 buckets per agg; first 10 hits sorted by `@timestamp desc`. Redact common PII fields (`user.email`, `client.ip`, `http.request.headers.authorization`) before printing.
6. **Cross-index hint.** If `trace.id` appears in hits, suggest joining against `traces-*` (Honeycomb / Tempo / OTLP indices) for the upstream trace.

## Output

```text
log-search

Index:      logs-prod-refund-*
Time:       2026-05-23T14:00Z → 2026-05-23T14:30Z
Query:      service.name:"refund-api" AND http.response.status_code >= 500
Took:       412ms
Matches:    2,041  (exact)

Top buckets
  http.response.status_code:
    502: 1,890
    500: 134
    504: 17
  trace.id (top 5):
    7a8b9c..: 412
    1b2c3d..: 89
    ...

Sample (10 most recent)
  @timestamp                  status  trace.id     message (redacted)
  2026-05-23T14:29:58.412Z    502     7a8b9c       "upstream timeout from refund-worker"
  2026-05-23T14:29:57.110Z    502     7a8b9c       "circuit-breaker open: refund-worker"
  ...

Cross-index hint:
  Top trace.id 7a8b9c appears 412×; consider `traces-prod-*` lookup
  via polymath-observability:trace-investigate.
```

## Quality bar

- Index pattern explicit, never `*`.
- Time range explicit; default-range opt-in only.
- Total relation honest (exact vs. approximate).
- PII fields redacted before printing.
- Sample capped at 10, never a full dump.

## Anti-patterns to avoid

- `index: '*'` cluster-wide scans. Slow + cross-tenant PII risk.
- "Last 24h" defaults without opt-in. Most incident windows are minutes; 24h defaults bury the signal.
- Returning raw hits without redaction. Logs frequently carry headers + PII.
- Treating `total.relation = "gte"` as exact. The number is a lower bound when relation is `gte`.

