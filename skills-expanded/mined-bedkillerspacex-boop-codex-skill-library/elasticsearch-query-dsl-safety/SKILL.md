---
name: elasticsearch-query-dsl-safety
description: >
  Avoid expensive or abusive Elasticsearch Query DSL on owned clusters: timeouts,
  circuit breakers, search limits, script controls, deep pagination hazards, and
  role-level query restrictions. Use when ES queries cause heap pressure, wildcard
  leading stars, costly aggs, or search thread pool rejections. Not a general
  cluster TLS guide (see elasticsearch-security-basics).
---

# Elasticsearch Query DSL Safety

## Scope And Authorization

- **In scope:** Query patterns, client code, and cluster settings on ES/OpenSearch you operate.
- **Out of scope:** Crafting resource-exhaustion queries against third-party clusters.
- Expensive queries can take down shared clusters—test limits in non-prod first.
- Redact query bodies that contain personal data when pasting into tickets.
- Pair application query builders with `code-quality-standards`.

## When To Use

- Cluster instability correlated with search thread pool rejections or circuit breakers.
- Users/API clients sending unbounded `match_all`, deep `from`/`size`, or leading-wildcard queries.
- Enabling or tuning `search.default_allow_partial_results`, request timeouts, and max windows.
- Restricting scripts (`script.allowed_types`, painless contexts) and expensive aggs.
- Designing safe query builders for product search.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Auth/TLS/anonymous access | `elasticsearch-security-basics` |
| ILM/retention security | `elasticsearch-ilm-security` |
| Runtime field cost design | `elasticsearch-runtime-fields` |
| App input validation (Echo/etc.) | framework bind skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Timeouts | Client + `timeout` on search; cancel stuck requests |
| Breakers | Respect parent/request/fielddata breakers; fix queries not only raise limits |
| Pagination | Prefer `search_after` / PIT over huge `from` |
| Wildcards | Avoid leading `*foo`; constrain analyzed fields |
| Scripts | Disable inline dynamic scripts if unused; allowlist stored scripts |
| Authz | Role query templates / DLS so tenants cannot scan all docs |

## Workflow

### 1. Confirm scope and success criteria

1. Identify offending indices, clients, and time windows of pressure.
2. Success: p95 search latency and reject rates within SLO; no single query can unbounded-scan.

### 2. Inventory hot queries and settings

```bash
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_nodes/stats/indices/search?pretty" | head
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_cat/thread_pool/search?v"
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_cluster/settings?include_defaults=true&flat_settings=true&pretty" \
  | head -n 5
# Slow log (if enabled) / task management
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_tasks?detailed=true&actions=*search*&pretty" | head
```

1. Enable or review index search slow logs for outliers.
2. List application query templates (Kibana, backend builders).

### 3. Baseline bad patterns

| Pattern | Risk | Safer alternative |
| --- | --- | --- |
| `{"query":{"match_all":{}}}` + large size | Heap / IO | Filter required fields; default time range |
| `from: 100000` | Deep pagination cost | `search_after` + sort + PIT |
| `*suffix` wildcard | Expensive | ngram/search_as_you_type or reverse field |
| Unbounded `terms` agg | Memory | `size` cap; composite agg |
| Inline scripts per doc | CPU | Precompute fields at index time |
| Wildcard indices `*` | Cross-tenant | Explicit index/alias allowlist |

### 4. Apply cluster and role guardrails

```json
PUT _cluster/settings
{
  "persistent": {
    "search.max_buckets": 65535,
    "script.allowed_types": "stored",
    "script.allowed_contexts": "ingest,score"
  }
}
```

```json
PUT _security/role/app_search
{
  "indices": [{
    "names": ["products"],
    "privileges": ["read"],
    "query": {
      "term": { "tenant_id": "{{_user.metadata.tenant_id}}" }
    }
  }]
}
```

1. Set application defaults: `size` max (e.g. 100), mandatory time filter on log indices.
2. Configure HTTP client timeouts and max retries carefully (avoid thundering herds).
3. Prefer filter context and keyword fields for exact match.

### 5. Fix application Query DSL

```json
// Prefer bounded range + search_after
{
  "size": 50,
  "timeout": "5s",
  "query": {
    "bool": {
      "filter": [
        { "term": { "tenant_id": "T1" } },
        { "range": { "@timestamp": { "gte": "now-7d" } } }
      ],
      "must": [{ "match": { "title": "adapter" } }]
    }
  },
  "sort": [{ "@timestamp": "desc" }, { "_shard_doc": "asc" }]
}
```

1. Validate user-supplied sort fields against an allowlist (prevents script sort abuse).
2. Cap aggregation `size` and cardinality fields.
3. For multi-tenant SaaS, enforce tenant filter server-side—never trust client-only filters.

### 6. Verify with evidence

```bash
# Should fail or be limited when size too large (app-side) or when breaker trips
curl -sS -u "$ES_USER:$ES_PASS" "$ES/products/_search" -H 'Content-Type: application/json' -d '{
  "size": 50,
  "timeout": "2s",
  "query": { "match": { "title": "test" } }
}'
curl -sS -u "$ES_USER:$ES_PASS" "$ES/_nodes/stats/breaker?pretty" | head
```

1. Load-test representative queries in stage with production-like data volume.
2. Confirm thread pool rejections drop after fixes.
3. Document remaining allowed expensive admin queries (break-glass role only).

### 7. Hand off

1. Runbook: identify heavy search tasks and cancel with `_tasks/_cancel`.
2. Alerts on search reject rate, breaker trips, and slow log volume.
3. Code review checklist for new query builders.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Pagination | `search_after` + PIT | `from: 50000` |
| Tenant isolation | Role DLS / server filter | Client passes optional tenant_id |
| Scripts | Stored allowlisted | Arbitrary inline painless from users |
| Timeouts | 2–10s user search | No timeout, wait forever |
| Wildcards | Suffix with indexed field | Leading `*` on analyzed text |

## Output Checklist

- [ ] Hot queries and thread pool stats baselined
- [ ] Dangerous DSL patterns inventoried in app code
- [ ] Timeouts, size caps, agg caps applied
- [ ] Script policy tightened if scripts unused
- [ ] Tenant/role query restrictions verified
- [ ] Stage load evidence for fixed queries
- [ ] Alerts for rejects/breakers
- [ ] Residual risk documented

## Rules

- Authorized clusters only; do not DoS shared environments “as a test” without a window.
- Prefer fixing queries over raising every circuit breaker limit.
- Never log full queries containing secrets.
- Route auth/TLS work to `elasticsearch-security-basics`.
