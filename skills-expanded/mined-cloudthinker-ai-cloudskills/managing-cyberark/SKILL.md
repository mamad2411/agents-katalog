---
name: managing-cyberark
description: |
  Use when working with Cyberark — cyberArk privileged access management for
  safe management, privileged account discovery, session monitoring, credential
  rotation status, and security audit. Covers Vault, PVWA, PSM, and CyberArk
  Privilege Cloud. Read this skill before any CyberArk operations — it enforces
  discovery-first patterns and strict read-only safety rules.
connection_type: cyberark
preload: false
---

# CyberArk Management Skill

Safely read and audit CyberArk — the privileged access management platform.

## MANDATORY: Discovery-First Pattern

**Always discover safes, platforms, and account categories before accessing specific credentials. Never guess safe names or account IDs.**

### Phase 1: Discovery

```bash
#!/bin/bash

cyberark_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: $CYBERARK_SESSION_TOKEN" \
         -H "Content-Type: application/json" \
         "${CYBERARK_BASE_URL}/PasswordVault/api/${endpoint}"
}

# Authenticate first
cyberark_auth() {
    CYBERARK_SESSION_TOKEN=$(curl -s -X POST \
        -H "Content-Type: application/json" \
        -d "{\"username\":\"$CYBERARK_USER\",\"password\":\"$CYBERARK_PASS\"}" \
        "${CYBERARK_BASE_URL}/PasswordVault/api/auth/cyberark/logon" | tr -d '"')
}

echo "=== Server Info ==="
cyberark_api "ServerWebServices.svc/rest/server" 2>/dev/null | jq '.' || echo "Server info endpoint may vary by version"

echo ""
echo "=== Safes ==="
cyberark_api "Safes?limit=25" | jq -r '.value[]? | "\(.SafeUrlId)\t\(.SafeName)\t\(.Description // "N/A")\tMembers:\(.NumberOfDaysRetention // "N/A")"' | column -t

echo ""
echo "=== Platforms ==="
cyberark_api "Platforms" | jq -r '.Platforms[]? | "\(.PlatformID)\t\(.Name)\t\(.Active)"' | column -t

echo ""
echo "=== Account Summary ==="
cyberark_api "Accounts?limit=1" | jq '.count // .Total // "N/A"'
```

**Phase 1 outputs:** Safe list, platform inventory, account summary — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess safe names** — always list safes in Phase 1
- **NEVER assume account IDs** — always search accounts first
- **NEVER fabricate platform names** — always list platforms
- **ONLY read and list** — never retrieve passwords, create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: GET requests only — `Safes`, `Accounts`, `Platforms`, `LiveSessions`, `Recordings`
- **NEVER retrieve passwords**: Never call `Accounts/{id}/Password/Retrieve` unless explicitly requested
- **MASK sensitive data**: Redact all credential values, secret keys, and certificate contents
- **FORBIDDEN without explicit request**: Password retrieval, account creation/deletion, safe modifications, credential rotation triggers
- **NEVER display passwords in output**: Even if retrieved, mask with `*** REDACTED ***`

## Core Helper Functions

```bash
#!/bin/bash

cyberark_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: $CYBERARK_SESSION_TOKEN" \
         -H "Content-Type: application/json" \
         "${CYBERARK_BASE_URL}/PasswordVault/api/${endpoint}"
}

# Search accounts with safe filtering
search_accounts() {
    local search="$1"
    local safe="${2:-}"
    local filter=""
    [ -n "$safe" ] && filter="&filter=safeName eq ${safe}"
    cyberark_api "Accounts?search=${search}&limit=20${filter}"
}

# Paginated fetch
cyberark_paginated() {
    local endpoint="$1"
    local max_results="${2:-200}"
    local offset=0
    local limit=50

    while [ $offset -lt $max_results ]; do
        local sep="?"
        [[ "$endpoint" == *"?"* ]] && sep="&"
        result=$(cyberark_api "${endpoint}${sep}limit=${limit}&offset=${offset}")
        echo "$result" | jq '.value // .Accounts // []' 2>/dev/null
        count=$(echo "$result" | jq '.value // .Accounts // [] | length' 2>/dev/null)
        [ "${count:-0}" -lt "$limit" ] && break
        offset=$((offset + limit))
    done
}
```

## Common Operations

### Safe Management & Members

```bash
#!/bin/bash
SAFE_NAME="${1:?Safe name required — discover via Phase 1}"

echo "=== Safe Details: $SAFE_NAME ==="
cyberark_api "Safes/${SAFE_NAME}" | jq '{
    safe_name: .SafeName,
    description: .Description,
    location: .Location,
    managing_cpm: .ManagingCPM,
    number_of_versions: .NumberOfVersionsRetention,
    number_of_days: .NumberOfDaysRetention,
    olac_enabled: .OLACEnabled,
    creation_time: .CreationTime
}'

echo ""
echo "=== Safe Members ==="
cyberark_api "Safes/${SAFE_NAME}/Members" | jq -r '.value[]? | {
    name: .MemberName,
    type: .MemberType,
    permissions: {
        use_accounts: .Permissions.UseAccounts,
        retrieve_accounts: .Permissions.RetrieveAccounts,
        list_accounts: .Permissions.ListAccounts,
        manage_safe: .Permissions.ManageSafe,
        manage_safe_members: .Permissions.ManageSafeMembers,
        view_audit_log: .Permissions.ViewAuditLog
    }
}'
```

### Account Discovery & Search

```bash
#!/bin/bash
SEARCH="${1:?Search term required (account name, address, or username)}"

echo "=== Account Search: $SEARCH ==="
cyberark_api "Accounts?search=${SEARCH}&limit=20" | jq -r '.value[]? | {
    id: .id,
    name: .name,
    address: .address,
    username: .userName,
    safe: .safeName,
    platform_id: .platformId,
    secret_type: .secretType,
    secret_management: {
        automatic: .secretManagement.automaticManagementEnabled,
        last_modified: .secretManagement.lastModifiedTime,
        last_reconciled: .secretManagement.lastReconciledTime,
        last_verified: .secretManagement.lastVerifiedTime,
        status: .secretManagement.status
    },
    created_time: .createdTime
}'

echo ""
echo "=== Accounts by Platform ==="
cyberark_api "Accounts?limit=100" | jq -r '[.value[]? | .platformId] | group_by(.) | map({platform: .[0], count: length}) | sort_by(-.count) | .[] | "\(.platform)\t\(.count)"' | column -t
```

### Session Monitoring

```bash
#!/bin/bash
echo "=== Active PSM Sessions ==="
cyberark_api "LiveSessions?limit=20" | jq -r '.LiveSessions[]? | {
    session_id: .SessionID,
    user: .User,
    target_user: .AccountUserName,
    target_address: .RemoteMachine,
    from_ip: .FromIP,
    protocol: .Protocol,
    start_time: .Start,
    duration: .Duration,
    risk_score: .RiskScore
}'

echo ""
echo "=== Recent Session Recordings ==="
cyberark_api "Recordings?limit=20&Sort=Start&SortDirection=desc" | jq -r '.Recordings[]? | "\(.SessionID)\t\(.User)\t\(.AccountUserName)\t\(.RemoteMachine)\t\(.Start)\t\(.Duration)s"' | column -t

echo ""
echo "=== High-Risk Sessions ==="
cyberark_api "LiveSessions?limit=50" | jq -r '.LiveSessions[]? | select(.RiskScore > 50) | "\(.SessionID)\t\(.User)\t\(.RiskScore)\t\(.RemoteMachine)"' | column -t
```

### Credential Rotation Status

```bash
#!/bin/bash
echo "=== CPM Status — Recent Rotation Activity ==="
cyberark_api "Accounts?limit=50" | jq -r '.value[]? | select(.secretManagement.automaticManagementEnabled == true) | {
    name: .name,
    safe: .safeName,
    last_modified: .secretManagement.lastModifiedTime,
    last_verified: .secretManagement.lastVerifiedTime,
    status: .secretManagement.status
}'

echo ""
echo "=== Accounts with Failed Rotation ==="
cyberark_api "Accounts?limit=100" | jq -r '.value[]? | select(.secretManagement.status != "success" and .secretManagement.status != null) | "\(.name)\t\(.safeName)\t\(.secretManagement.status)"' | column -t

echo ""
echo "=== Accounts Not Rotated (>90 days) ==="
THRESHOLD=$(date -u -v-90d +%s 2>/dev/null || date -u -d '90 days ago' +%s)
cyberark_api "Accounts?limit=100" | jq -r --arg t "$THRESHOLD" '.value[]? | select(.secretManagement.lastModifiedTime < ($t | tonumber)) | "\(.name)\t\(.safeName)\t\(.secretManagement.lastModifiedTime | todate)"' | column -t 2>/dev/null
```

### Security Audit

```bash
#!/bin/bash
echo "=== Safe Permissions Audit ==="
cyberark_api "Safes?limit=50" | jq -r '.value[]?.SafeUrlId' | while read safe; do
    echo "--- Safe: $safe ---"
    cyberark_api "Safes/${safe}/Members" | jq -r '.value[]? | select(.Permissions.RetrieveAccounts == true) | "  RETRIEVE access: \(.MemberName) (\(.MemberType))"'
done | head -40

echo ""
echo "=== Accounts with Manual Management ==="
cyberark_api "Accounts?limit=100" | jq -r '.value[]? | select(.secretManagement.automaticManagementEnabled == false) | "\(.name)\t\(.safeName)\t\(.address)\tManual management"' | column -t | head -20
```

## Output Format

Present results as a structured report:
```
Managing Cyberark Report
════════════════════════
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

- **Authentication methods**: PVWA supports CyberArk, LDAP, RADIUS, and SAML auth — endpoint path differs (`auth/cyberark/logon` vs `auth/ldap/logon`)
- **Session token expiry**: Tokens expire after inactivity (default 20 min) — re-authenticate if getting 401
- **API versions**: Self-hosted (PVWA) and Privilege Cloud have different API base URLs and some endpoint differences
- **Safe URL encoding**: Safe names with spaces must be URL-encoded — use `SafeUrlId` instead of `SafeName` in paths
- **CPM dependency**: Automatic credential rotation requires CPM to be running and configured — check CPM status separately
- **Password retrieval auditing**: Every password retrieval is logged — even read-only access to passwords creates audit entries
- **Dual control**: Some safes require dual-control approval before password retrieval — API calls will return pending status
- **PSM vs direct access**: Session recordings are only available for PSM-proxied connections — direct connections are not recorded
