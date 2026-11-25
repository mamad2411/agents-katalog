---
name: managing-descope
description: |
  Use when working with Descope — descope authentication and identity management
  platform covering users, tenants, access keys, flows, and audit logs. Use when
  analyzing user authentication patterns, monitoring tenant health, reviewing
  access key usage, managing Descope flows and roles, or auditing login
  activity.
connection_type: descope
preload: false
---

# Descope Management Skill

Manage and analyze Descope authentication resources including users, tenants, and audit trails.

## API Conventions

### Authentication
All API calls use Bearer project ID and management key, injected automatically.

### Base URL
`https://api.descope.com/v1`

### Core Helper Function

```bash
#!/bin/bash

descope_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $DESCOPE_PROJECT_ID:$DESCOPE_MANAGEMENT_KEY" \
            -H "Content-Type: application/json" \
            "https://api.descope.com/v1${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $DESCOPE_PROJECT_ID:$DESCOPE_MANAGEMENT_KEY" \
            "https://api.descope.com/v1${endpoint}"
    fi
}
```

## Output Rules
- Target ≤50 lines per script output
- Use `jq` to extract only needed fields
- Never dump full API responses

## Phase 1: Discovery

```bash
#!/bin/bash
echo "=== Users (recent) ==="
descope_api POST "/mgmt/user/search" '{"limit": 20}' \
    | jq -r '.users[] | "\(.userId[0:16])\t\(.email // "no-email")\t\(.status)\t\(.createdTime | . / 1000 | strftime("%Y-%m-%d"))"' \
    | column -t | head -20

echo ""
echo "=== Tenants ==="
descope_api GET "/mgmt/tenant/all" \
    | jq -r '.tenants[] | "\(.id[0:16])\t\(.name)\t\(.selfProvisioningDomains | join(",") | .[0:40])"' \
    | head -15

echo ""
echo "=== Roles ==="
descope_api GET "/mgmt/role/all" \
    | jq -r '.roles[] | "\(.name)\t\(.description[0:50] // "")"' | head -15

echo ""
echo "=== Access Keys ==="
descope_api POST "/mgmt/accesskey/search" '{"limit": 20}' \
    | jq -r '.keys[] | "\(.id[0:16])\t\(.name)\t\(.status)\t\(.createdTime | . / 1000 | strftime("%Y-%m-%d"))"' \
    | head -10
```

## Phase 2: Analysis

### Authentication Health

```bash
#!/bin/bash
echo "=== User Status Breakdown ==="
descope_api POST "/mgmt/user/search" '{"limit": 200}' \
    | jq -r '.users[] | .status' | sort | uniq -c | sort -rn

echo ""
echo "=== Users by Auth Method ==="
descope_api POST "/mgmt/user/search" '{"limit": 200}' \
    | jq '{
        with_email: [.users[] | select(.verifiedEmail == true)] | length,
        with_phone: [.users[] | select(.verifiedPhone == true)] | length,
        with_sso: [.users[] | select(.ssoAppIds | length > 0)] | length
    }'

echo ""
echo "=== Audit Log (recent) ==="
descope_api POST "/mgmt/audit/search" '{"limit": 20}' \
    | jq -r '.audits[] | "\(.occurred[0:16])\t\(.action)\t\(.userId[0:16] // "system")\t\(.type)"' \
    | head -15
```

### Tenant Analytics

```bash
#!/bin/bash
echo "=== Tenant User Distribution ==="
descope_api GET "/mgmt/tenant/all" \
    | jq -r '.tenants[].id' | while read tid; do
    COUNT=$(descope_api POST "/mgmt/user/search" "{\"limit\": 1, \"tenantIds\": [\"$tid\"]}" | jq '.total // 0')
    echo "$tid: $COUNT users"
done | sort -t: -k2 -rn | head -15

echo ""
echo "=== Disabled Users ==="
descope_api POST "/mgmt/user/search" '{"limit": 50, "statuses": ["disabled"]}' \
    | jq -r '.users[] | "\(.userId[0:16])\t\(.email // "no-email")\t\(.createdTime | . / 1000 | strftime("%Y-%m-%d"))"' \
    | head -10
```

## Output Format

```
=== Descope Project: <id> ===
Total Users: <n>  Tenants: <n>  Roles: <n>

--- Auth Health ---
Verified Email: <n>  Verified Phone: <n>  SSO: <n>

--- User Status ---
enabled: <n>  disabled: <n>  invited: <n>

--- Audit (recent) ---
<timestamp>  <action>  <user>
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
- **Search endpoints are POST**: User and audit search use POST with JSON body
- **Timestamps**: Descope uses Unix milliseconds — divide by 1000 for dates
- **Management key**: Required for all management API endpoints; different from project ID
- **Rate limits**: 100 requests/minute for management endpoints
