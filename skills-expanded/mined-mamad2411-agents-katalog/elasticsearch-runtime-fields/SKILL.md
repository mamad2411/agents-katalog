---
name: elasticsearch-runtime-fields
description: >
  Elasticsearch runtime fields cost and safety on owned clusters: when to use
  runtime vs indexed fields, Painless scripts, mapping runtime sections, query
  performance tradeoffs, and security of field definitions. Use when runtime
  fields, schema-on-read, or expensive scripted fields in Kibana/ES. Not a full
  ILM or cluster auth guide.
---

# Elasticsearch Runtime Fields

## Scope And Authorization

- **In scope:** mappings, templates, and queries on ES/OpenSearch clusters you own.
- **Out of scope:** Injecting runtime scripts into third-party clusters.
- Runtime fields execute at query time—they can amplify CPU cost across shards.
- Script source may expose business logic; control who can update mappings.
- Redact PII in example documents and script snippets shared externally.

## When To Use

- Prototyping a field without reindexing (schema-on-read).
- Short-lived derived fields for investigations in Kibana.
- Evaluating whether a runtime field should be promoted to indexed for production SLOs.
- Auditing mappings for heavy `runtime` Painless that runs on every hit.
- Shadowing or overriding fields carefully without breaking consumers.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Query timeouts/breakers generally | `elasticsearch-query-dsl-safety` |
| Auth/TLS/anonymous | `elasticsearch-security-basics` |
| Retention / ILM | `elasticsearch-ilm-security` |
| Ingest pipeline design broadly | ingest/data pipeline skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Cost model | Runtime = CPU per doc touched; indexed = disk + index time |
| Use cases | Rare fields, experiments, temporary SOC views |
| Avoid | High-QPS product search path on multi-GB scans |
| Scripts | Simple grok/emit; no unbounded loops |
| Governance | Mapping changes via template PR, not ad-hoc prod Kibana only |
| Security | Limit `manage` on indices; script allowlists |

## Workflow

### 1. Confirm scope and success criteria

1. Query patterns that need the field (filters, aggs, display-only).
2. Success: correct values on sample docs; p95 query cost acceptable vs indexed alternative.

### 2. Inventory runtime usage

```bash
curl -sS -u "$ES_USER:$ES_PASS" "$ES/my-index/_mapping?pretty" | head -n 200
# Search templates / Kibana saved objects may define runtime fields ad hoc
curl -sS -u "$ES_USER:$ES_PASS" "$ES/my-index/_search" -H 'Content-Type: application/json' -d '{
  "size": 0,
  "query": { "match_all": {} }
}'
```

1. List indices with `runtime` sections in mappings.
2. Find application queries that pass `runtime_mappings` in the search body.

### 3. Baseline cost

1. Profile a representative query with and without the runtime field (stage).
2. Note docs examined, shard time, and circuit breaker proximity.
3. Estimate QPS that will use the field in production.

### 4. Define runtime fields carefully

```json
PUT my-index/_mapping
{
  "runtime": {
    "http.status_class": {
      "type": "keyword",
      "script": {
        "source": "if (doc['http.response.status_code'].size()==0) return; emit(doc['http.response.status_code'].value / 100 + 'xx')"
      }
    }
  }
}
```

```json
// Query-time only (does not persist in mapping)
POST my-index/_search
{
  "runtime_mappings": {
    "price_with_tax": {
      "type": "double",
      "script": {
        "source": "emit(doc['price'].value * 1.2)"
      }
    }
  },
  "query": {
    "range": { "price_with_tax": { "gt": 100 } }
  }
}
```

1. Prefer **keyword/long** runtime types over complex objects.
2. Guard empty doc values (`size()==0`) to avoid script exceptions.
3. Do not parse multi-MB `_source` strings on every query if an ingest field would do.

### 5. Promote or reject

| Signal | Action |
| --- | --- |
| Field used in hot filters/aggs at high QPS | Reindex / ingest pipeline → indexed field |
| Occasional dashboard column | Keep runtime; document owner |
| Script grows complex | Move to ingest or app-side |
| Multi-tenant field exposes others' data | Fix script + security; add tests |

1. For production product paths, default to indexed fields computed at write time.
2. Runtime is a bridge, not a permanent substitute for mapping design.

### 6. Verify with evidence

```bash
# Profile API (version-dependent) or compare took times
curl -sS -u "$ES_USER:$ES_PASS" "$ES/my-index/_search" -H 'Content-Type: application/json' -d '{
  "size": 10,
  "query": { "term": { "http.status_class": "2xx" } }
}'
```

1. Validate correctness on edge docs (missing fields, unexpected types).
2. Confirm role restrictions: users without manage cannot install cluster-wide dangerous scripts if policy requires.
3. Load-test the worst-case index pattern (e.g. `logs-*` with wide time range).

### 7. Hand off

1. Document each permanent runtime field: owner, reason, revisit date.
2. Alert if mapping changes introduce new runtime scripts in prod templates.
3. Prefer data streams + templates so runtime definitions are code-reviewed.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Experiment | Query-time runtime for 1 day SOC hunt | Unreviewed runtime on all log indices forever |
| Hot path | Indexed field for checkout search | Painless tax calc on every product query |
| Scripts | Tiny emit with null checks | Nested loops over `_source` arrays |
| Governance | Template PR | Each analyst invents fields in Kibana only |
| Security | Least-privilege manage | All users edit mappings |

## Output Checklist

- [ ] Runtime fields inventoried per hot index
- [ ] Cost baseline vs indexed alternative
- [ ] Null-safe scripts and limited types
- [ ] Promotion/reject decision documented
- [ ] Load evidence for production-like QPS
- [ ] Mapping ownership and review path set
- [ ] Residual CPU risk noted

## Rules

- Owned clusters only.
- Treat query-time scripts as production code—review and test them.
- Do not “fix” outages by removing timeouts; fix field strategy.
- Prefer ingest/indexed fields for high-QPS paths.
- Coordinate with `elasticsearch-query-dsl-safety` for cluster-wide query limits.
