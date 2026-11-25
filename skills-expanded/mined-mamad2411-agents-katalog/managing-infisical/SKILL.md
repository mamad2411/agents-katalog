---
name: managing-infisical
description: |
  Use when working with Infisical — infisical secrets management, environment
  configuration, access control, secret versioning, and audit logging. Covers
  project and workspace management, secret syncing across environments, access
  policies, secret rotation, and integration status. Use when managing secrets
  across environments, auditing secret access, comparing environment configs, or
  reviewing secret history in Infisical.
connection_type: infisical
preload: false
---

# Infisical Management Skill

Manage and analyze secrets, projects, environments, and access controls in Infisical.

## API Conventions

### Authentication
All API calls use the `Authorization: Bearer $INFISICAL_API_KEY` header. Never hardcode tokens.

### Base URL
`$INFISICAL_URL/api/v3` (cloud: `https://app.infisical.com/api/v3`, or self-hosted)

### Core Helper Function

```bash
#!/bin/bash

INFISICAL_BASE="${INFISICAL_URL:-https://app.infisical.com}"

inf_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $INFISICAL_API_KEY" \
            -H "Content-Type: application/json" \
            "${INFISICAL_BASE}/api/v3${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $INFISICAL_API_KEY" \
            -H "Content-Type: application/json" \
            "${INFISICAL_BASE}/api/v3${endpoint}"
    fi
}
```

## Output Rules
- **TOKEN EFFICIENCY**: Extract only needed fields with `jq`
- Target <=50 lines per script output
- **NEVER** output secret values -- only output secret keys and metadata
- Never dump full API responses

## Discovery Phase

### List Workspaces and Environments

```bash
#!/bin/bash
echo "=== Workspaces ==="
inf_api GET "/workspaces" \
    | jq -r '.workspaces[] | "\(.id[0:12])\t\(.name)\t\(.environments | length) envs"' | column -t

echo ""
WORKSPACE_ID="${1:?Workspace ID required}"
echo "=== Environments ==="
inf_api GET "/workspaces/${WORKSPACE_ID}" \
    | jq -r '.workspace.environments[] | "\(.slug)\t\(.name)"' | column -t
```

### List Secret Keys

```bash
#!/bin/bash
WORKSPACE_ID="${1:?Workspace ID required}"
ENV="${2:-dev}"

echo "=== Secret Keys (names only, ${ENV}) ==="
inf_api GET "/secrets?workspaceId=${WORKSPACE_ID}&environment=${ENV}" \
    | jq -r '.secrets[] | "\(.secretKey)\t\(.type)\t\(.version)"' | column -t | head -25
```

## Analysis Phase

### Config Comparison

```bash
#!/bin/bash
WORKSPACE_ID="${1:?Workspace ID required}"

echo "=== Key Count by Environment ==="
inf_api GET "/workspaces/${WORKSPACE_ID}" | jq -r '.workspace.environments[].slug' | while read -r env; do
    count=$(inf_api GET "/secrets?workspaceId=${WORKSPACE_ID}&environment=${env}" | jq '.secrets | length')
    echo "${env}\t${count} keys"
done | column -t

echo ""
echo "=== Keys Missing in Production ==="
DEV_KEYS=$(inf_api GET "/secrets?workspaceId=${WORKSPACE_ID}&environment=dev" | jq -r '.secrets[].secretKey' | sort)
PROD_KEYS=$(inf_api GET "/secrets?workspaceId=${WORKSPACE_ID}&environment=prod" | jq -r '.secrets[].secretKey' | sort)
comm -23 <(echo "$DEV_KEYS") <(echo "$PROD_KEYS") | head -15
```

### Audit Log

```bash
#!/bin/bash
WORKSPACE_ID="${1:?Workspace ID required}"

echo "=== Recent Activity ==="
inf_api GET "/audit-logs?workspaceId=${WORKSPACE_ID}&limit=20" \
    | jq -r '.auditLogs[] | "\(.createdAt[0:16])\t\(.actor.name // "system")\t\(.event.type)\t\(.event.metadata.secretKey // "")"' \
    | column -t

echo ""
echo "=== Integrations ==="
inf_api GET "/integrations?workspaceId=${WORKSPACE_ID}" \
    | jq -r '.integrations[] | "\(.integration)\t\(.environment)\t\(.isActive)"' | column -t
```

## Output Format
- Use tab-separated columns with `column -t`
- Limit lists to 15-25 items
- NEVER display secret values -- only key names and metadata
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
- **Never expose values**: Only display secret key names, never actual values
- **Workspace scoping**: Most endpoints require `workspaceId` parameter
- **Environment slugs**: Use environment slugs (dev, staging, prod) not display names
- **Secret versioning**: Secrets are versioned -- check version number for change tracking
- **Self-hosted vs cloud**: Base URL differs -- always use `$INFISICAL_URL` env variable
- **Folders**: Secrets can be organized in folders -- use `secretPath` parameter
