---
name: managing-azure-entra
description: |
  Use when working with Azure Entra — azure Entra ID (formerly Azure AD)
  management for user lifecycle, app registrations, service principals,
  conditional access policies, sign-in log analysis, and directory role
  assignments. Covers B2B guest users, enterprise applications, and security
  configuration review. Read this skill before any Entra ID operations — it
  enforces discovery-first patterns and strict read-only safety rules.
connection_type: azure
preload: false
---

# Azure Entra ID Management Skill

Safely read and audit Azure Entra ID — Microsoft's cloud identity and access management service.

## MANDATORY: Discovery-First Pattern

**Always discover tenant configuration, directory objects, and registered apps before performing targeted queries. Never guess object IDs or app registration names.**

### Phase 1: Discovery

```bash
#!/bin/bash

graph_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer $GRAPH_ACCESS_TOKEN" \
         -H "Content-Type: application/json" \
         "https://graph.microsoft.com/v1.0/${endpoint}"
}

echo "=== Tenant Info ==="
graph_api "organization" | jq '.value[0] | {
    id: .id,
    display_name: .displayName,
    tenant_type: .tenantType,
    verified_domains: [.verifiedDomains[] | .name],
    created: .createdDateTime
}'

echo ""
echo "=== Directory Statistics ==="
echo "Users: $(graph_api 'users/$count' -H 'ConsistencyLevel: eventual' 2>/dev/null || echo 'N/A')"
echo "Groups: $(graph_api 'groups/$count' -H 'ConsistencyLevel: eventual' 2>/dev/null || echo 'N/A')"
echo "Applications: $(graph_api 'applications/$count' -H 'ConsistencyLevel: eventual' 2>/dev/null || echo 'N/A')"

echo ""
echo "=== App Registrations (first 20) ==="
graph_api "applications?\$top=20&\$select=id,displayName,appId,createdDateTime,signInAudience" | jq -r '.value[] | "\(.appId)\t\(.displayName)\t\(.signInAudience)"' | column -t

echo ""
echo "=== Conditional Access Policies ==="
graph_api "identity/conditionalAccess/policies" | jq -r '.value[] | "\(.id)\t\(.displayName)\t\(.state)"' | column -t
```

**Phase 1 outputs:** Tenant info, app registrations, conditional access policies — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess object IDs or UPNs** — always search via `$filter` or `$search`
- **NEVER assume app registration names** — always list in Phase 1
- **NEVER fabricate role names** — always query directory roles
- **ONLY read and list** — never create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: GET requests only via Microsoft Graph API
- **MASK sensitive data**: Redact app secrets, user passwords, and certificate thumbprints
- **FORBIDDEN without explicit request**: POST/PATCH/DELETE to users, apps, policies; credential operations
- **NEVER print secrets or certificates**: Always redact sensitive credential material

## Core Helper Functions

```bash
#!/bin/bash

graph_api() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer $GRAPH_ACCESS_TOKEN" \
         -H "Content-Type: application/json" \
         "https://graph.microsoft.com/v1.0/${endpoint}"
}

graph_api_beta() {
    local endpoint="$1"
    curl -s -H "Authorization: Bearer $GRAPH_ACCESS_TOKEN" \
         -H "Content-Type: application/json" \
         "https://graph.microsoft.com/beta/${endpoint}"
}

# Paginated fetch following @odata.nextLink
graph_paginated() {
    local url="https://graph.microsoft.com/v1.0/$1"
    local max_pages="${2:-5}"
    local page=0

    while [ -n "$url" ] && [ $page -lt $max_pages ]; do
        result=$(curl -s -H "Authorization: Bearer $GRAPH_ACCESS_TOKEN" "$url")
        echo "$result" | jq '.value[]' 2>/dev/null
        url=$(echo "$result" | jq -r '.["@odata.nextLink"] // empty')
        page=$((page + 1))
    done
}
```

## Common Operations

### User Management & Search

```bash
#!/bin/bash
SEARCH="${1:?Search term required (email, name, or UPN)}"

echo "=== User Search: $SEARCH ==="
graph_api "users?\$filter=startswith(displayName,'${SEARCH}') or startswith(mail,'${SEARCH}') or startswith(userPrincipalName,'${SEARCH}')&\$select=id,displayName,mail,userPrincipalName,accountEnabled,createdDateTime,lastSignInDateTime,userType" | jq -r '.value[] | {
    id: .id,
    display_name: .displayName,
    upn: .userPrincipalName,
    mail: .mail,
    enabled: .accountEnabled,
    user_type: .userType,
    created: .createdDateTime
}'

echo ""
echo "=== Guest Users ==="
graph_api "users?\$filter=userType eq 'Guest'&\$top=20&\$select=displayName,mail,userPrincipalName,createdDateTime" | jq -r '.value[] | "\(.displayName)\t\(.mail)\t\(.createdDateTime)"' | column -t
```

### App Registration & Service Principal Review

```bash
#!/bin/bash
APP_ID="${1:?App ID (client ID) required — discover via Phase 1}"

echo "=== App Registration Details ==="
graph_api "applications?\$filter=appId eq '${APP_ID}'" | jq '.value[0] | {
    id: .id,
    display_name: .displayName,
    app_id: .appId,
    sign_in_audience: .signInAudience,
    created: .createdDateTime,
    redirect_uris: .web.redirectUris,
    api_permissions: [.requiredResourceAccess[] | {resource: .resourceAppId, permissions: [.resourceAccess[] | .id]}],
    credential_count: ((.passwordCredentials | length) + (.keyCredentials | length)),
    credentials_expiry: [.passwordCredentials[] | {name: .displayName, expiry: .endDateTime}]
}'

echo ""
echo "=== Service Principal ==="
graph_api "servicePrincipals?\$filter=appId eq '${APP_ID}'" | jq '.value[0] | {
    id: .id,
    display_name: .displayName,
    enabled: .accountEnabled,
    app_role_assignment_required: .appRoleAssignmentRequired,
    service_principal_type: .servicePrincipalType
}'

echo ""
echo "=== App Role Assignments ==="
SP_ID=$(graph_api "servicePrincipals?\$filter=appId eq '${APP_ID}'" | jq -r '.value[0].id')
graph_api "servicePrincipals/${SP_ID}/appRoleAssignedTo" | jq -r '.value[] | "\(.principalDisplayName)\t\(.principalType)\t\(.appRoleId)"' | column -t
```

### Conditional Access Policy Analysis

```bash
#!/bin/bash
echo "=== All Conditional Access Policies ==="
graph_api "identity/conditionalAccess/policies" | jq -r '.value[] | {
    id: .id,
    name: .displayName,
    state: .state,
    created: .createdDateTime,
    conditions: {
        users_include: .conditions.users.includeUsers,
        users_exclude: .conditions.users.excludeUsers,
        apps_include: .conditions.applications.includeApplications,
        platforms: .conditions.platforms,
        locations: .conditions.locations,
        risk_levels: .conditions.signInRiskLevels
    },
    grant_controls: .grantControls,
    session_controls: .sessionControls
}'

echo ""
echo "=== Policies in Report-Only Mode ==="
graph_api "identity/conditionalAccess/policies" | jq -r '.value[] | select(.state == "enabledForReportingButNotEnforced") | "\(.displayName)\t\(.state)"' | column -t

echo ""
echo "=== Named Locations ==="
graph_api "identity/conditionalAccess/namedLocations" | jq -r '.value[] | "\(.displayName)\t\(.["@odata.type"])\t\(.isTrusted // "N/A")"' | column -t
```

### Sign-In Log Analysis

```bash
#!/bin/bash
echo "=== Recent Sign-In Logs (last 50) ==="
graph_api_beta "auditLogs/signIns?\$top=50&\$orderby=createdDateTime desc" | jq -r '.value[] | {
    date: .createdDateTime,
    user: .userDisplayName,
    app: .appDisplayName,
    status: .status.errorCode,
    failure_reason: (.status.failureReason // "Success"),
    ip: .ipAddress,
    location: "\(.location.city // "N/A"), \(.location.countryOrRegion // "N/A")",
    device: .deviceDetail.operatingSystem,
    mfa_required: (.authenticationRequirement // "N/A")
}'

echo ""
echo "=== Failed Sign-Ins ==="
graph_api_beta "auditLogs/signIns?\$filter=status/errorCode ne 0&\$top=20&\$orderby=createdDateTime desc" | jq -r '.value[] | "\(.createdDateTime)\t\(.userDisplayName)\t\(.status.failureReason)\t\(.ipAddress)"' | column -t

echo ""
echo "=== Risky Users ==="
graph_api "identityProtection/riskyUsers?\$top=20" | jq -r '.value[] | "\(.userDisplayName)\t\(.riskLevel)\t\(.riskState)\t\(.riskLastUpdatedDateTime)"' | column -t 2>/dev/null || echo "Identity Protection not available or insufficient permissions"
```

### Directory Role Assignments

```bash
#!/bin/bash
echo "=== Activated Directory Roles ==="
graph_api "directoryRoles" | jq -r '.value[] | "\(.id)\t\(.displayName)\t\(.description)"' | column -t

echo ""
echo "=== Global Administrator Members ==="
GA_ROLE_ID=$(graph_api "directoryRoles?\$filter=displayName eq 'Global Administrator'" | jq -r '.value[0].id')
graph_api "directoryRoles/${GA_ROLE_ID}/members" | jq -r '.value[] | "\(.displayName)\t\(.userPrincipalName // .appDisplayName)\t\(.["@odata.type"])"' | column -t

echo ""
echo "=== All Privileged Role Assignments ==="
for role in "Global Administrator" "Privileged Role Administrator" "User Administrator" "Application Administrator"; do
    ROLE_ID=$(graph_api "directoryRoles?\$filter=displayName eq '${role}'" | jq -r '.value[0].id // empty')
    if [ -n "$ROLE_ID" ]; then
        count=$(graph_api "directoryRoles/${ROLE_ID}/members" | jq '.value | length')
        echo "${role}: ${count} members"
    fi
done
```

## Output Format

Present results as a structured report:
```
Managing Azure Entra Report
═══════════════════════════
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

- **Graph API versions**: v1.0 is stable; beta has more features but may change — use beta only for sign-in logs and risky users
- **Token scopes**: Graph tokens need specific scopes (e.g., `Directory.Read.All`, `AuditLog.Read.All`) — 403 means missing scope, not wrong credentials
- **$count requires header**: Using `$count` requires `ConsistencyLevel: eventual` header
- **Sign-in log retention**: 7 days for free tier, 30 days for P1/P2 — export to Log Analytics for longer retention
- **Conditional access evaluation**: Policies with state `enabledForReportingButNotEnforced` are report-only — they log but do not block
- **App vs Service Principal**: App registration is the template; service principal is the instance in a tenant — both need review
- **Guest user UPNs**: Guest users have mangled UPNs like `user_company.com#EXT#@tenant.onmicrosoft.com` — search by mail instead
- **Pagination**: Graph API returns max 999 items per page — always follow `@odata.nextLink` for complete results
