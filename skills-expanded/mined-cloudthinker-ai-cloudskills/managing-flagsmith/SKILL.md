---
name: managing-flagsmith
description: |
  Use when working with Flagsmith — flagsmith feature flag and remote config
  management, user segments, A/B testing, and environment management. Covers
  flag listing, identity overrides, segment rules, change requests, and audit
  logging. Use when managing feature flags, configuring user segments, reviewing
  identity overrides, or auditing flag changes in Flagsmith.
connection_type: flagsmith
preload: false
---

# Flagsmith Management Skill

Manage and analyze feature flags, segments, identities, and environments in Flagsmith.

## API Conventions

### Authentication
All API calls use the `Authorization: Api-Key $FLAGSMITH_API_KEY` header (admin key). Never hardcode tokens.

### Base URL
`$FLAGSMITH_URL/api/v1` (cloud: `https://api.flagsmith.com/api/v1`, or self-hosted)

### Core Helper Function

```bash
#!/bin/bash

FLAGSMITH_BASE="${FLAGSMITH_URL:-https://api.flagsmith.com}"

fs_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Api-Key $FLAGSMITH_API_KEY" \
            -H "Content-Type: application/json" \
            "${FLAGSMITH_BASE}/api/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Api-Key $FLAGSMITH_API_KEY" \
            -H "Content-Type: application/json" \
            "${FLAGSMITH_BASE}/api/v1${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- Never dump full API responses

## Discovery Phase

### List Projects and Environments

```bash
#!/bin/bash
echo "=== Projects ==="
fs_api GET "/projects/" \
    | jq -r '.[] | "\(.id)\t\(.name)\t\(.environments | length) envs"' | column -t

echo ""
PROJECT_ID="${1:?Project ID required}"
echo "=== Environments ==="
fs_api GET "/environments/?project=${PROJECT_ID}" \
    | jq -r '.results[] | "\(.api_key[0:12])...\t\(.name)"' | column -t
```

### List Feature Flags

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Features ==="
fs_api GET "/projects/${PROJECT_ID}/features/?page_size=25" \
    | jq -r '.results[] | "\(.type)\t\(.name)\t\(.default_enabled)\t\(.is_archived)"' | column -t

echo ""
echo "=== Feature Summary ==="
fs_api GET "/projects/${PROJECT_ID}/features/?page_size=100" \
    | jq '{total: .count, archived: ([.results[] | select(.is_archived)] | length), by_type: (.results | group_by(.type) | map({(.[0].type): length}) | add)}'
```

## Analysis Phase

### Flag States by Environment

```bash
#!/bin/bash
ENVIRONMENT_KEY="${1:?Environment API key required}"

echo "=== Feature States ==="
curl -s -H "X-Environment-Key: ${ENVIRONMENT_KEY}" \
    "${FLAGSMITH_BASE}/api/v1/flags/" \
    | jq -r '.[] | "\(.feature.name)\tenabled:\(.enabled)\tvalue:\(.feature_state_value // "null")"' \
    | column -t | head -25
```

### Audit Log

```bash
#!/bin/bash
PROJECT_ID="${1:?Project ID required}"

echo "=== Recent Changes ==="
fs_api GET "/projects/${PROJECT_ID}/audit/?page_size=20" \
    | jq -r '.results[] | "\(.created_date[0:16])\t\(.author.email // "system")\t\(.log[0:60])"' \
    | column -t

echo ""
echo "=== Segments ==="
fs_api GET "/projects/${PROJECT_ID}/segments/?page_size=15" \
    | jq -r '.results[] | "\(.name)\t\(.rules | length) rules"' | column -t
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- Show summaries before details

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
- **Two auth modes**: Admin API uses `Api-Key` header; client SDK uses `X-Environment-Key` header
- **Self-hosted vs cloud**: Base URL varies -- always use `$FLAGSMITH_URL` env variable
- **Feature types**: `STANDARD` (boolean flags) and `MULTIVARIATE` (multiple values with percentage weights)
- **Identity overrides**: Per-user flag overrides take precedence over segment and default rules
- **Pagination**: Uses Django-style pagination with `page_size` and `page` parameters
- **Change requests**: Approval workflows available for production flag changes
