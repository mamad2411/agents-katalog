---
name: managing-algolia
description: |
  Use when working with Algolia — algolia index management, search relevance
  tuning, analytics review, and configuration optimization. Covers index
  settings, ranking criteria, faceting configuration, synonyms, rules, API key
  management, and usage quotas. Read this skill before any Algolia operations.
connection_type: algolia
preload: false
---

# Algolia Management Skill

Monitor, analyze, and optimize Algolia search indices safely.

## MANDATORY: Discovery-First Pattern

**Always list indices and check usage before any search or config operations. Never assume index names or attribute configurations.**

### Phase 1: Discovery

```bash
#!/bin/bash

ALGOLIA_APP="${ALGOLIA_APP_ID}"
ALGOLIA_KEY="${ALGOLIA_ADMIN_API_KEY}"

algolia_get() {
    curl -s -H "X-Algolia-API-Key: $ALGOLIA_KEY" \
         -H "X-Algolia-Application-Id: $ALGOLIA_APP" \
         "https://$ALGOLIA_APP-dsn.algolia.net$1"
}

echo "=== List Indices ==="
algolia_get "/1/indexes" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for idx in data.get('items', []):
    print(f\"Index: {idx['name']} | Entries: {idx.get('entries',0)} | Size: {idx.get('dataSize',0)//1024}KB | Updated: {idx.get('updatedAt','?')}\")
" 2>/dev/null

echo ""
echo "=== API Key Status ==="
algolia_get "/1/keys" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Total keys: {len(data.get('keys', []))}\")
for k in data.get('keys', [])[:5]:
    print(f\"  Key ...{k['value'][-6:]}: ACL={k.get('acl',[])} | Indices={k.get('indexes',['*'])}\")
" 2>/dev/null

echo ""
echo "=== Usage Logs ==="
algolia_get "/1/logs?length=5&type=all" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for l in data.get('logs', []):
    print(f\"  {l.get('timestamp','?')} | {l.get('method','?')} {l.get('url','?')} | {l.get('answer_code','?')} | {l.get('processing_time_ms','?')}ms\")
" 2>/dev/null
```

**Phase 1 outputs:** Index list with entry counts and sizes, API key inventory, recent API logs.

### Phase 2: Analysis

```bash
#!/bin/bash

ALGOLIA_APP="${ALGOLIA_APP_ID}"
ALGOLIA_KEY="${ALGOLIA_ADMIN_API_KEY}"
INDEX="${1:-my_index}"

algolia_get() {
    curl -s -H "X-Algolia-API-Key: $ALGOLIA_KEY" \
         -H "X-Algolia-Application-Id: $ALGOLIA_APP" \
         "https://$ALGOLIA_APP-dsn.algolia.net$1"
}

echo "=== Index Settings: $INDEX ==="
algolia_get "/1/indexes/$INDEX/settings" | python3 -c "
import sys, json
s = json.load(sys.stdin)
print(f\"Searchable attrs: {s.get('searchableAttributes','*')}\")
print(f\"Ranking: {s.get('ranking',[])}\")
print(f\"Facets: {s.get('attributesForFaceting',[])}\")
print(f\"Custom ranking: {s.get('customRanking',[])}\")
print(f\"Replicas: {s.get('replicas',[])}\")
print(f\"Unretrievable: {s.get('unretrievableAttributes',[])}\")
" 2>/dev/null

echo ""
echo "=== Synonyms ==="
algolia_get "/1/indexes/$INDEX/synonyms/search" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Total synonyms: {data.get('nbHits',0)}\")
for s in data.get('hits', [])[:5]:
    print(f\"  {s.get('objectID','?')}: type={s.get('type','?')} synonyms={s.get('synonyms',s.get('word','?'))}\")
" 2>/dev/null

echo ""
echo "=== Rules ==="
algolia_get "/1/indexes/$INDEX/rules/search" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"Total rules: {data.get('nbHits',0)}\")
for r in data.get('hits', [])[:5]:
    print(f\"  {r.get('objectID','?')}: condition={r.get('condition',{}).get('pattern','?')}\")
" 2>/dev/null
```

## Output Format

```
ALGOLIA ANALYSIS
================
App ID: [app_id] | Indices: [count]
Total Records: [sum] | Total Size: [sum]

ISSUES FOUND:
- [issue with affected index]

RECOMMENDATIONS:
- [actionable recommendation]
```

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

