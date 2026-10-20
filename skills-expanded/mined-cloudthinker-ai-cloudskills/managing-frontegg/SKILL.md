---
name: managing-frontegg
description: |
  Use when working with Frontegg — frontegg authentication and user management
  platform covering users, tenants, roles, permissions, SSO, and audit logs. Use
  when analyzing tenant health, monitoring user authentication, reviewing role
  assignments, managing Frontegg tenants and users, or auditing access control
  configurations.
connection_type: frontegg
preload: false
---

# Frontegg Management Skill

Manage and analyze Frontegg authentication resources including users, tenants, roles, and audit logs.

## API Conventions

### Authentication
API calls require vendor token obtained via client credentials, injected automatically.

### Base URL
`https://api.frontegg.com`

### Core Helper Function

```bash
#!/bin/bash

frontegg_api() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"

    if [ -n "$data" ]; then
        curl -s -X "$method" \
            -H "Authorization: Bearer $FRONTEGG_VENDOR_TOKEN" \
            -H "Content-Type: application/json" \
            "https://api.frontegg.com${endpoint}" \
            -d "$data"
    else
        curl -s -X "$method" \
            -H "Authorization: Bearer $FRONTEGG_VENDOR_TOKEN" \
            "https://api.frontegg.com${endpoint}"
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
echo "=== Tenants ==="
frontegg_api GET "/tenants/resources/tenants/v1?_limit=20" \
    | jq -r '.[] | "\(.tenantId[0:16])\t\(.name)\t\(.createdAt[0:10])"' \
    | column -t | head -20

echo ""
echo "=== Users (recent) ==="
frontegg_api GET "/identity/resources/users/v2?_limit=20&_sortBy=createdAt&_order=desc" \
    | jq -r '.items[] | "\(.id[0:16])\t\(.email)\t\(.verified)\t\(.createdAt[0:10])"' \
    | column -t | head -20

echo ""
echo "=== Roles ==="
frontegg_api GET "/identity/resources/roles/v1" \
    | jq -r '.[] | "\(.id[0:16])\t\(.name)\t\(.key)\t\(.permissions | length) perms"' \
    | head -15

echo ""
echo "=== Permissions ==="
frontegg_api GET "/identity/resources/permissions/v1" \
    | jq -r '.[] | "\(.key)\t\(.name)\t\(.categoryId // "none")"' | head -15
```

## Phase 2: Analysis

### Tenant Health

```bash
#!/bin/bash
echo "=== Tenant User Distribution ==="
frontegg_api GET "/tenants/resources/tenants/v1?_limit=50" \
    | jq -r '.[].tenantId' | while read tid; do
    COUNT=$(frontegg_api GET "/identity/resources/users/v1?_limit=1&tenantId=$tid" | jq '.totalItems // 0')
    echo "$tid: $COUNT users"
done | sort -t: -k2 -rn | head -15

echo ""
echo "=== Users Without Verified Email ==="
frontegg_api GET "/identity/resources/users/v2?_limit=50&verified=false" \
    | jq -r '.items[] | "\(.id[0:16])\t\(.email)\t\(.createdAt[0:10])"' | head -10
```

### Access Control Audit

```bash
#!/bin/bash
echo "=== Role Assignment Summary ==="
frontegg_api GET "/identity/resources/users/v2?_limit=100" \
    | jq -r '[.items[].roles[].name] | group_by(.) | map({(.[0]): length}) | add'

echo ""
echo "=== SSO Configurations ==="
frontegg_api GET "/team/resources/sso/v1/configurations" \
    | jq -r '.[] | "\(.id[0:16])\t\(.type)\t\(.enabled)\t\(.domain)"' | head -10

echo ""
echo "=== Audit Logs (recent) ==="
frontegg_api GET "/audits/resources/audits/v1?_limit=20&_sortBy=createdAt&_order=desc" \
    | jq -r '.items[] | "\(.createdAt[0:16])\t\(.action)\t\(.user.email // "system")\t\(.severity)"' \
    | head -15
```

## Output Format

```
=== Frontegg Environment ===
Tenants: <n>  Users: <n>  Roles: <n>

--- Tenant Health ---
Largest: <name> (<n> users)
Unverified Users: <n>

--- Access Control ---
Roles: <n>  Permissions: <n>
SSO Configs: <n>

--- Audit (recent) ---
<timestamp>  <action>  <user>  <severity>
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
- **Vendor token**: Must authenticate with client ID/secret to get vendor token first
- **Pagination**: Use `_limit`, `_offset`, `_sortBy`, `_order` query params
- **Tenant scoping**: Most user endpoints can filter by `tenantId` parameter
- **Rate limits**: 100 requests/minute for management endpoints
