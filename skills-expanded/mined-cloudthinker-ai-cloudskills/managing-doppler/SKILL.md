---
name: managing-doppler
description: |
  Use when working with Doppler — doppler secrets management, environment
  configuration, project organization, and access control. Covers secret
  syncing, config comparison across environments, activity logs, service token
  management, and integration status. Use when managing secrets across
  environments, auditing config changes, comparing environment configs, or
  reviewing access permissions in Doppler.
connection_type: doppler
preload: false
---

# Doppler Management Skill

Manage and analyze secrets, projects, environments, and access controls in Doppler.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $DOPPLER_API_KEY` header. Never hardcode tokens.

### Base URL
`https://api.doppler.com/v3`

### Core Helper Function

```bash
#!/bin/bash

doppler_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $DOPPLER_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.doppler.com/v3${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $DOPPLER_API_KEY" \
            -H "Content-Type: application/json" \
            "https://api.doppler.com/v3${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- **NEVER** output secret values -- only output secret names/keys
- Never dump full API responses

## Discovery Phase

### List Projects and Environments

```bash
#!/bin/bash
echo "=== Projects ==="
doppler_api GET "/projects" \
    | jq -r '.projects[] | "\(.slug)\t\(.name)\t\(.created_at[0:16])"' | column -t

echo ""
echo "=== Environments (per project) ==="
PROJECT="${1:?Project slug required}"
doppler_api GET "/environments?project=${PROJECT}" \
    | jq -r '.environments[] | "\(.slug)\t\(.name)"' | column -t
```

### List Configs

```bash
#!/bin/bash
PROJECT="${1:?Project slug required}"

echo "=== Configs ==="
doppler_api GET "/configs?project=${PROJECT}" \
    | jq -r '.configs[] | "\(.name)\t\(.environment)\t\(.locked)"' | column -t

echo ""
echo "=== Secret Names (keys only) ==="
CONFIG="${2:-dev}"
doppler_api GET "/secrets?project=${PROJECT}&config=${CONFIG}" \
    | jq -r '.secrets | keys[]' | head -25
```

## Analysis Phase

### Config Comparison

```bash
#!/bin/bash
PROJECT="${1:?Project slug required}"

echo "=== Key Count by Config ==="
for config in dev staging production; do
    count=$(doppler_api GET "/secrets?project=${PROJECT}&config=${config}" | jq '.secrets | keys | length')
    echo "${config}\t${count} keys"
done | column -t

echo ""
echo "=== Keys Missing in Production ==="
DEV_KEYS=$(doppler_api GET "/secrets?project=${PROJECT}&config=dev" | jq -r '.secrets | keys[]' | sort)
PROD_KEYS=$(doppler_api GET "/secrets?project=${PROJECT}&config=production" | jq -r '.secrets | keys[]' | sort)
comm -23 <(echo "$DEV_KEYS") <(echo "$PROD_KEYS") | head -15
```

### Activity Log

```bash
#!/bin/bash
PROJECT="${1:?Project slug required}"

echo "=== Recent Activity ==="
doppler_api GET "/logs?project=${PROJECT}&per_page=20" \
    | jq -r '.logs[] | "\(.created_at[0:16])\t\(.user.name // "service")\t\(.action)\t\(.config // "N/A")"' \
    | column -t

echo ""
echo "=== Service Tokens ==="
CONFIG="${2:-production}"
doppler_api GET "/configs/config/tokens?project=${PROJECT}&config=${CONFIG}" \
    | jq -r '.tokens[] | "\(.name)\t\(.created_at[0:16])\t\(.expires_at[0:16] // "never")"' | column -t
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- NEVER display secret values -- only key names
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
- **Never expose values**: Only display secret names/keys, never actual values
- **Config hierarchy**: Configs inherit from environments (dev, staging, production) with branch configs
- **Project + config scoping**: Most endpoints require both `project` and `config` parameters
- **Service tokens vs API keys**: Service tokens are scoped to a single config; API keys have broader access
- **Rate limits**: 240 requests per minute
- **Pagination**: Use `per_page` and `page` parameters
