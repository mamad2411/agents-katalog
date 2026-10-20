---
name: managing-fauna
description: |
  Use when working with Fauna — fauna database management via the fauna CLI and
  Fauna API. Covers databases, collections, indexes, functions, keys, and query
  execution. Use when managing Fauna databases or reviewing document-relational
  data.
connection_type: fauna
preload: false
---

# Managing Fauna

Manage Fauna databases using the `fauna` CLI and Fauna API.

## MANDATORY: Discovery-First Pattern

**Always discover available resources before performing analysis.**

### Phase 1: Discovery

```bash
#!/bin/bash

echo "=== Databases ==="
fauna list-databases 2>/dev/null | head -20 || \
curl -s "https://db.fauna.com" \
    -H "Authorization: Bearer $FAUNA_SECRET" \
    -H "Content-Type: application/json" \
    -d '{"query": "Database.all().map(db => { name: db.name, coll: db.coll })"}' | jq '.data[]' | head -20

echo ""
echo "=== Collections ==="
fauna eval "Collection.all().map(c => { name: c.name, count: c.count() })" 2>/dev/null | head -20 || \
curl -s "https://db.fauna.com" \
    -H "Authorization: Bearer $FAUNA_SECRET" \
    -H "Content-Type: application/json" \
    -d '{"query": "Collection.all().map(c => { name: c.name })"}' | jq '.data[]' | head -20

echo ""
echo "=== Functions ==="
fauna eval "Function.all().map(f => { name: f.name, role: f.role })" 2>/dev/null | head -10 || \
curl -s "https://db.fauna.com" \
    -H "Authorization: Bearer $FAUNA_SECRET" \
    -H "Content-Type: application/json" \
    -d '{"query": "Function.all().map(f => { name: f.name })"}' | jq '.data[]' | head -10

echo ""
echo "=== Keys ==="
fauna eval "Key.all().map(k => { id: k.id, role: k.role })" 2>/dev/null | head -10
```

### Phase 2: Analysis

```bash
#!/bin/bash

DB_NAME="${1:-}"

echo "=== Collection Details ==="
fauna eval "Collection.all().map(c => { name: c.name, indexes: c.indexes().map(i => i.name), history_days: c.history_days, document_ttls: c.document_ttls })" ${DB_NAME:+--database "$DB_NAME"} 2>/dev/null | head -30 || \
curl -s "https://db.fauna.com" \
    -H "Authorization: Bearer $FAUNA_SECRET" \
    -H "Content-Type: application/json" \
    -d '{"query": "Collection.all().map(c => { name: c.name })"}' | jq '.data' | head -20

echo ""
echo "=== Index Details ==="
fauna eval "Collection.all().flatMap(c => c.indexes().map(i => { collection: c.name, index: i.name, terms: i.terms, values: i.values }))" ${DB_NAME:+--database "$DB_NAME"} 2>/dev/null | head -20

echo ""
echo "=== Sample Record Counts ==="
fauna eval "Collection.all().take(10).map(c => { name: c.name, count: c.count() })" ${DB_NAME:+--database "$DB_NAME"} 2>/dev/null | head -10

echo ""
echo "=== Access Providers ==="
fauna eval "AccessProvider.all().map(ap => { name: ap.name, issuer: ap.issuer })" ${DB_NAME:+--database "$DB_NAME"} 2>/dev/null | head -10

echo ""
echo "=== Schema Status ==="
fauna schema status ${DB_NAME:+--database "$DB_NAME"} 2>/dev/null | head -10
```

## Output Format

```
COLLECTION    INDEXES    COUNT     HISTORY_DAYS
users         3          12450     30
orders        2          89340     30
products      4          5620      30
```

## Safety Rules
- Use read-only queries: `*.all()`, `*.count()`, schema introspection
- Never run `delete`, `create`, `update` mutations without explicit user confirmation
- FQL queries should be read-only
- Limit output with `| head -N` to stay under 50 lines

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

