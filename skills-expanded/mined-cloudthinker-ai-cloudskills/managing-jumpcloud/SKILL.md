---
name: managing-jumpcloud
description: |
  Use when working with Jumpcloud — jumpCloud directory platform management for
  user and system management, SSO application configuration, device policy
  enforcement, group management, and audit event review. Covers LDAP, RADIUS,
  SSO apps, MDM policies, and system agent status. Read this skill before any
  JumpCloud operations — it enforces discovery-first patterns and strict
  read-only safety rules.
connection_type: jumpcloud
preload: false
---

# JumpCloud Management Skill

Safely read and audit JumpCloud — the open directory platform for identity, access, and device management.

## MANDATORY: Discovery-First Pattern

**Always discover the organization, user directories, and system inventory before performing targeted queries. Never guess user IDs or system IDs.**

### Phase 1: Discovery

```bash
#!/bin/bash

jc_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "x-api-key: $JUMPCLOUD_API_KEY" \
         -H "Content-Type: application/json" \
         "https://console.jumpcloud.com/api/${endpoint}"
}

jc_api_v2() {
    local endpoint="$1"
    curl -s -H "x-api-key: $JUMPCLOUD_API_KEY" \
         -H "Content-Type: application/json" \
         "https://console.jumpcloud.com/api/v2/${endpoint}"
}

echo "=== Organization Info ==="
jc_api "organizations" | jq '.[0] | {
    id: .id,
    display_name: .displayName,
    logo_url: .logoUrl,
    created: .created,
    account_locked: .accountLocked
}'

echo ""
echo "=== User Count ==="
jc_api "systemusers?limit=1" | jq '.totalCount'

echo ""
echo "=== Systems Count ==="
jc_api "systems?limit=1" | jq '.totalCount'

echo ""
echo "=== SSO Applications ==="
jc_api_v2 "applications?limit=20" | jq -r '.[] | "\(.id)\t\(.displayLabel)\t\(.ssoUrl // "N/A")"' | column -t

echo ""
echo "=== User Groups ==="
jc_api_v2 "usergroups?limit=20" | jq -r '.[] | "\(.id)\t\(.name)\t\(.type)"' | column -t

echo ""
echo "=== System Groups ==="
jc_api_v2 "systemgroups?limit=20" | jq -r '.[] | "\(.id)\t\(.name)\t\(.type)"' | column -t
```

**Phase 1 outputs:** Org info, user/system counts, app and group inventories — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess user or system IDs** — always search or list first
- **NEVER assume application names** — always list applications in Phase 1
- **NEVER fabricate group names** — always list user/system groups
- **ONLY read and list** — never create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: GET requests only — `systemusers`, `systems`, `applications`, `usergroups`, `events`
- **MASK sensitive data**: Redact SSH keys, recovery codes, and TOTP seeds
- **FORBIDDEN without explicit request**: POST/PUT/DELETE to users, systems, apps; password resets; MFA resets
- **NEVER print API keys or secrets**: Always redact in output

## Core Helper Functions

```bash
#!/bin/bash

jc_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "x-api-key: $JUMPCLOUD_API_KEY" \
         -H "Content-Type: application/json" \
         "https://console.jumpcloud.com/api/${endpoint}"
}

jc_api_v2() {
    local endpoint="$1"
    curl -s -H "x-api-key: $JUMPCLOUD_API_KEY" \
         -H "Content-Type: application/json" \
         "https://console.jumpcloud.com/api/v2/${endpoint}"
}

# Paginated fetch
jc_paginated() {
    local endpoint="$1"
    local max_results="${2:-200}"
    local skip=0
    local limit=100

    while [ $skip -lt $max_results ]; do
        local sep="?"
        [[ "$endpoint" == *"?"* ]] && sep="&"
        result=$(jc_api "${endpoint}${sep}limit=${limit}&skip=${skip}")
        echo "$result" | jq '.results // .[]' 2>/dev/null
        count=$(echo "$result" | jq '.results // . | length' 2>/dev/null)
        [ "${count:-0}" -lt "$limit" ] && break
        skip=$((skip + limit))
    done
}
```

## Common Operations

### User Management

```bash
#!/bin/bash
SEARCH="${1:?Search term required (email or username)}"

echo "=== User Search: $SEARCH ==="
jc_api "systemusers?filter=email%3A\$regex%3A${SEARCH}&limit=10" | jq -r '.results[] | {
    id: .id,
    username: .username,
    email: .email,
    name: "\(.firstname) \(.lastname)",
    activated: .activated,
    suspended: .suspended,
    state: .state,
    mfa_enabled: .mfa.configured,
    totp_enabled: .totp_enabled,
    created: .created,
    password_expiration: .password_expiration,
    external_source: (.externalSourceType // "local")
}'

echo ""
echo "=== User Group Memberships ==="
USER_ID=$(jc_api "systemusers?filter=email%3A\$regex%3A${SEARCH}&limit=1" | jq -r '.results[0].id')
jc_api_v2 "users/${USER_ID}/memberof" | jq -r '.[] | "\(.id)\t\(.name)\t\(.type)"' | column -t
```

### SSO Application Configuration

```bash
#!/bin/bash
echo "=== All SSO Applications ==="
jc_api_v2 "applications?limit=50" | jq -r '.[] | {
    id: .id,
    name: .displayLabel,
    sso_url: .ssoUrl,
    beta: .beta,
    organization: .organization
}'

echo ""
APP_ID="${1:-}"
if [ -n "$APP_ID" ]; then
    echo "=== Application Details: $APP_ID ==="
    jc_api_v2 "applications/${APP_ID}" | jq '{
        id: .id,
        display_label: .displayLabel,
        sso_url: .ssoUrl,
        learn_more: .learnMore,
        database_attributes: .databaseAttributes
    }'

    echo ""
    echo "=== Users Assigned to App ==="
    jc_api_v2 "applications/${APP_ID}/associations?targets=user" | jq -r '.[] | "\(.to.id)\t\(.to.type)"' | column -t
fi
```

### Device & System Management

```bash
#!/bin/bash
echo "=== Systems Overview ==="
jc_api "systems?limit=20" | jq -r '.results[] | {
    id: .id,
    display_name: .displayName,
    hostname: .hostname,
    os: .os,
    version: .version,
    agent_version: .agentVersion,
    active: .active,
    allow_ssh_password: .allowSshPasswordAuthentication,
    allow_multi_factor: .allowMultiFactorAuthentication,
    last_contact: .lastContact,
    created: .created
}'

echo ""
echo "=== Systems by OS ==="
jc_api "systems?limit=200" | jq -r '[.results[] | .os] | group_by(.) | map({os: .[0], count: length}) | sort_by(-.count) | .[] | "\(.os)\t\(.count)"' | column -t

echo ""
echo "=== Inactive Systems (no contact >30 days) ==="
THRESHOLD=$(date -u -v-30d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '30 days ago' +%Y-%m-%dT%H:%M:%SZ)
jc_api "systems?limit=100" | jq -r --arg t "$THRESHOLD" '.results[] | select(.lastContact < $t) | "\(.displayName)\t\(.hostname)\t\(.lastContact)"' | column -t
```

### Policy Enforcement Review

```bash
#!/bin/bash
echo "=== Policies ==="
jc_api_v2 "policies?limit=30" | jq -r '.[] | "\(.id)\t\(.name)\t\(.template.name // "custom")"' | column -t

echo ""
echo "=== Policy Details ==="
POLICY_ID="${1:-}"
if [ -n "$POLICY_ID" ]; then
    jc_api_v2 "policies/${POLICY_ID}" | jq '{
        id: .id,
        name: .name,
        template: .template.name,
        values: .values
    }'

    echo ""
    echo "=== Systems Bound to Policy ==="
    jc_api_v2 "policies/${POLICY_ID}/associations?targets=system" | jq -r '.[] | "\(.to.id)\t\(.to.type)"' | column -t
fi

echo ""
echo "=== RADIUS Servers ==="
jc_api "radiusservers?limit=10" | jq -r '.results[]? | "\(.id)\t\(.name)\t\(.networkSourceIp)"' | column -t
```

### Audit Event Review

```bash
#!/bin/bash
SINCE="${1:-$(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ)}"

echo "=== Directory Insights Events (since $SINCE) ==="
curl -s -X POST \
     -H "x-api-key: $JUMPCLOUD_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{\"service\": [\"directory\"], \"start_time\": \"${SINCE}\", \"limit\": 30}" \
     "https://api.jumpcloud.com/insights/directory/v1/events" | jq -r '.[] | {
    timestamp: .timestamp,
    event_type: .event_type,
    initiated_by: (.initiated_by.email // .initiated_by.type // "system"),
    resource: (.resource.email // .resource.hostname // .resource.id // "N/A"),
    success: .success
}'

echo ""
echo "=== SSO Authentication Events ==="
curl -s -X POST \
     -H "x-api-key: $JUMPCLOUD_API_KEY" \
     -H "Content-Type: application/json" \
     -d "{\"service\": [\"sso\"], \"start_time\": \"${SINCE}\", \"limit\": 20}" \
     "https://api.jumpcloud.com/insights/directory/v1/events" | jq -r '.[] | "\(.timestamp)\t\(.event_type)\t\(.initiated_by.email // "N/A")\t\(.success)"' | column -t
```

## Output Format

Present results as a structured report:
```
Managing Jumpcloud Report
═════════════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **API v1 vs v2**: User and system CRUD uses v1 (`/api/`); groups, policies, and associations use v2 (`/api/v2/`) — using wrong version returns 404
- **Multi-tenant orgs**: API key is org-scoped — ensure correct org context for multi-tenant setups
- **System agent status**: `active: true` only means agent is installed, not recently connected — check `lastContact` for actual status
- **LDAP vs Cloud**: JumpCloud can be both LDAP directory and cloud SSO — user source affects which attributes are available
- **Directory Insights API**: Uses POST with body params (not GET) — different from standard REST patterns
- **Rate limits**: API rate limits are per-org (typically 100 req/10s) — batch requests when listing large directories
- **Filter syntax**: v1 uses MongoDB-style filters (`$regex`, `$eq`) — v2 uses different query parameter format
- **Pagination**: v1 uses `skip`/`limit`; v2 uses `limit` with cursor — do not mix pagination styles
