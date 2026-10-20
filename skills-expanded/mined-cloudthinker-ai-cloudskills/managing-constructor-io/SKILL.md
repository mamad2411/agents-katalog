---
name: managing-constructor-io
description: |
  Use when working with Constructor Io — constructor.io product search and
  discovery platform management including catalog sync, search configuration,
  autosuggest, browse, recommendations, quizzes, and A/B testing. Covers catalog
  health, search performance, conversion tracking, and personalization
  effectiveness.
connection_type: constructor-io
preload: false
---

# Constructor.io Management Skill

Monitor and manage Constructor.io product discovery and search platform.

## MANDATORY: Discovery-First Pattern

**Always discover catalog status and search configuration before querying analytics.**

### Phase 1: Discovery

```bash
#!/bin/bash
CIO_API="https://ac.cnstrc.com"
CIO_MGMT="https://api.constructor.io/v2"
AUTH="Authorization: Basic $(echo -n "${CONSTRUCTOR_API_TOKEN}:" | base64)"

echo "=== Catalog Status ==="
curl -s -H "$AUTH" "$CIO_MGMT/catalogs" | \
  jq -r '.catalogs[] | "\(.name) | Items: \(.item_count) | Last Sync: \(.last_sync_at)"' 2>/dev/null || echo "Check catalog via dashboard"

echo ""
echo "=== Sections ==="
curl -s -H "$AUTH" "$CIO_MGMT/sections" | \
  jq -r '.sections[] | "\(.name) | Display: \(.display_name) | Items: \(.item_count)"' 2>/dev/null

echo ""
echo "=== Search Configuration ==="
curl -s -H "$AUTH" "$CIO_MGMT/search_configurations" | \
  jq -r '.[] | "\(.name) | Enabled: \(.enabled) | Filters: \(.filter_count // "N/A")"' 2>/dev/null || echo "Check search config via dashboard"

echo ""
echo "=== Recommendation Pods ==="
curl -s -H "$AUTH" "$CIO_MGMT/recommendation_pods" | \
  jq -r '.pods[] | "\(.pod_id) | Type: \(.strategy) | Active: \(.active)"' 2>/dev/null || echo "Check recommendation pods via dashboard"

echo ""
echo "=== Search Health Check ==="
curl -s "$CIO_API/autocomplete/${CONSTRUCTOR_SEARCH_KEY}?query=test&num_results=1" | \
  jq -r '"Autosuggest API: \(if .sections then "OK" else "Error" end)"'
```

**Phase 1 outputs:** Catalog status, sections, search config, recommendation pods

### Phase 2: Analysis

```bash
#!/bin/bash
echo "=== Search Performance Test ==="
curl -s "$CIO_API/search/${CONSTRUCTOR_SEARCH_KEY}?query=shirt&num_results=5&section=Products" | \
  jq -r '"Results: \(.response.total_num_results)\nFacets: \(.response.facets | length)\nSort Options: \(.response.sort_options | length)\nLatency: \(.request.processing_time_ms // "N/A")ms"'

echo ""
echo "=== Autocomplete Test ==="
curl -s "$CIO_API/autocomplete/${CONSTRUCTOR_SEARCH_KEY}?query=sh&num_results=5" | \
  jq -r '.sections | to_entries[] | "\(.key): \(.value | length) suggestions"'

echo ""
echo "=== Browse Performance ==="
curl -s "$CIO_API/browse/${CONSTRUCTOR_SEARCH_KEY}/group_id/all?num_results=1" | \
  jq -r '"Browse Results: \(.response.total_num_results // "N/A")\nGroups: \(.response.groups | length // "N/A")"' 2>/dev/null

echo ""
echo "=== A/B Tests ==="
curl -s -H "$AUTH" "$CIO_MGMT/ab_tests" | \
  jq -r '.ab_tests[] | "\(.name) | Status: \(.status) | Start: \(.start_date) | End: \(.end_date)"' 2>/dev/null || echo "Check A/B tests via dashboard"

echo ""
echo "=== Quizzes ==="
curl -s -H "$AUTH" "$CIO_MGMT/quizzes" | \
  jq -r '.quizzes[] | "\(.quiz_id) | Name: \(.name) | Active: \(.active)"' 2>/dev/null || echo "No quizzes configured"
```

## Output Format

```
CONSTRUCTOR.IO STATUS
=====================
Catalog: {items} items | Last Sync: {time}
Sections: {count}
Search API: {status} ({latency}ms)
Autosuggest: {status}
Recommendation Pods: {active}/{total}
A/B Tests: {active}/{total}
Quizzes: {count}
Issues: {list_of_warnings}
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

## Common Pitfalls

- **API key vs Token**: Search key for client-side queries; API token for management
- **Catalog sync**: Full syncs can take time — use delta updates for large catalogs
- **Sections**: Products vs Content vs custom sections — query the right section
- **Personalization**: Requires behavioral tracking SDK integration to work effectively
