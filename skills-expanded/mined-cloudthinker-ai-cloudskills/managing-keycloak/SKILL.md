---
name: managing-keycloak
description: |
  Use when working with Keycloak — keycloak identity and access management for
  realm administration, client configuration, user federation, role mapping,
  session analysis, and authentication flow review. Covers OpenID Connect, SAML,
  LDAP federation, and identity brokering. Read this skill before any Keycloak
  operations — it enforces discovery-first patterns and strict read-only safety
  rules.
connection_type: keycloak
preload: false
---

# Keycloak Management Skill

Safely read and audit Keycloak — the open-source identity and access management server.

## MANDATORY: Discovery-First Pattern

**Always discover realms, clients, and identity providers before targeted queries. Never guess realm names or client IDs.**

### Phase 1: Discovery

```bash
#!/bin/bash

kc_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: Bearer $KC_ACCESS_TOKEN" \
         -H "Content-Type: application/json" \
         "${KC_BASE_URL}/admin/realms/${KC_REALM:-master}/${endpoint}"
}

kc_token() {
    curl -s -X POST \
         "${KC_BASE_URL}/realms/${KC_REALM:-master}/protocol/openid-connect/token" \
         -d "client_id=${KC_CLIENT_ID:-admin-cli}" \
         -d "username=$KC_ADMIN_USER" \
         -d "password=$KC_ADMIN_PASS" \
         -d "grant_type=password" | jq -r '.access_token'
}

echo "=== Server Info ==="
curl -s -H "Authorization: Bearer $KC_ACCESS_TOKEN" \
     "${KC_BASE_URL}/admin/serverinfo" | jq '{
    system_info: .systemInfo | {version: .version, server_time: .serverTime, uptime: .uptime},
    providers: (.providers | keys | length),
    themes: .themes | keys
}' 2>/dev/null || echo "Server info not accessible"

echo ""
echo "=== Available Realms ==="
curl -s -H "Authorization: Bearer $KC_ACCESS_TOKEN" \
     "${KC_BASE_URL}/admin/realms" | jq -r '.[] | "\(.realm)\t\(.enabled)\tUsers: \(.users // "N/A")"' | column -t

echo ""
echo "=== Clients in Realm ==="
kc_api "clients?first=0&max=30" | jq -r '.[] | "\(.id)\t\(.clientId)\t\(.enabled)\t\(.protocol)"' | column -t

echo ""
echo "=== Identity Providers ==="
kc_api "identity-provider/instances" | jq -r '.[] | "\(.alias)\t\(.providerId)\t\(.enabled)"' | column -t
```

**Phase 1 outputs:** Realm list, client inventory, identity providers — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess realm names** — always list realms in Phase 1
- **NEVER assume client IDs** — always list clients first
- **NEVER fabricate role names** — always query realm or client roles
- **ONLY read and list** — never create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: GET requests only — `clients`, `users`, `roles`, `groups`, `identity-provider`
- **MASK sensitive data**: Redact client secrets, user credentials, and LDAP bind passwords
- **FORBIDDEN without explicit request**: POST/PUT/DELETE to realms, clients, users; credential resets
- **NEVER print secrets**: Always use `*** REDACTED ***` for client secrets and LDAP passwords

## Core Helper Functions

```bash
#!/bin/bash

kc_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: Bearer $KC_ACCESS_TOKEN" \
         -H "Content-Type: application/json" \
         "${KC_BASE_URL}/admin/realms/${KC_REALM:-master}/${endpoint}"
}

# Paginated fetch
kc_api_paginated() {
    local endpoint="$1"
    local max_results="${2:-100}"
    local batch_size=50
    local first=0

    while [ $first -lt $max_results ]; do
        local separator="?"
        [[ "$endpoint" == *"?"* ]] && separator="&"
        result=$(kc_api "${endpoint}${separator}first=${first}&max=${batch_size}")
        count=$(echo "$result" | jq '. | length')
        echo "$result" | jq '.[]'
        [ "$count" -lt "$batch_size" ] && break
        first=$((first + batch_size))
    done
}
```

## Common Operations

### Realm Configuration Review

```bash
#!/bin/bash
REALM="${1:-$KC_REALM}"

echo "=== Realm: $REALM ==="
kc_api "" | jq '{
    realm: .realm,
    enabled: .enabled,
    registration_allowed: .registrationAllowed,
    login_with_email: .loginWithEmailAllowed,
    duplicate_emails: .duplicateEmailsAllowed,
    verify_email: .verifyEmail,
    brute_force_protected: .bruteForceProtected,
    max_failure_wait: .maxFailureWaitSeconds,
    ssl_required: .sslRequired,
    access_token_lifespan: .accessTokenLifespan,
    sso_session_idle: .ssoSessionIdleTimeout,
    sso_session_max: .ssoSessionMaxLifespan,
    default_roles: .defaultRoles
}'

echo ""
echo "=== Authentication Flows ==="
kc_api "authentication/flows" | jq -r '.[] | "\(.id)\t\(.alias)\t\(.builtIn)"' | column -t

echo ""
echo "=== Required Actions ==="
kc_api "authentication/required-actions" | jq -r '.[] | "\(.alias)\t\(.name)\t\(.enabled)\tDefault: \(.defaultAction)"' | column -t
```

### Client Configuration

```bash
#!/bin/bash
CLIENT_ID="${1:?Client UUID required — discover via Phase 1}"

echo "=== Client Details ==="
kc_api "clients/${CLIENT_ID}" | jq '{
    clientId: .clientId,
    name: .name,
    enabled: .enabled,
    protocol: .protocol,
    public_client: .publicClient,
    service_accounts_enabled: .serviceAccountsEnabled,
    authorization_enabled: .authorizationServicesEnabled,
    redirect_uris: .redirectUris,
    web_origins: .webOrigins,
    base_url: .baseUrl,
    root_url: .rootUrl,
    secret: "*** REDACTED ***"
}'

echo ""
echo "=== Client Roles ==="
kc_api "clients/${CLIENT_ID}/roles" | jq -r '.[] | "\(.id)\t\(.name)\t\(.description // "N/A")"' | column -t

echo ""
echo "=== Client Scopes ==="
kc_api "clients/${CLIENT_ID}/default-client-scopes" | jq -r '.[] | "\(.id)\t\(.name)\t\(.protocol)"' | column -t
```

### User Federation & LDAP

```bash
#!/bin/bash
echo "=== User Federation Providers ==="
kc_api "components?type=org.keycloak.storage.UserStorageProvider" | jq -r '.[] | {
    id: .id,
    name: .name,
    provider_type: .providerId,
    enabled: (.config.enabled[0] // "true"),
    vendor: (.config.vendor[0] // "N/A"),
    connection_url: (.config.connectionUrl[0] // "N/A"),
    bind_dn: (.config.bindDn[0] // "N/A"),
    bind_credential: "*** REDACTED ***",
    users_dn: (.config.usersDn[0] // "N/A"),
    sync_period: (.config.fullSyncPeriod[0] // "N/A"),
    changed_sync_period: (.config.changedSyncPeriod[0] // "N/A")
}'

echo ""
echo "=== LDAP Mappers ==="
kc_api "components?type=org.keycloak.storage.UserStorageProvider" | jq -r '.[0].id' | while read fed_id; do
    [ "$fed_id" != "null" ] && kc_api "components?parent=${fed_id}&type=org.keycloak.storage.ldap.mappers.LDAPStorageMapper" | jq -r '.[] | "\(.name)\t\(.providerId)\t\(.config.ldapAttribute[0] // "N/A")"' | column -t
done
```

### Role Mapping & Session Analysis

```bash
#!/bin/bash
echo "=== Realm Roles ==="
kc_api "roles?first=0&max=50" | jq -r '.[] | "\(.id)\t\(.name)\t\(.composite)\t\(.description // "N/A")"' | column -t

echo ""
echo "=== Active Sessions ==="
kc_api "client-session-stats" | jq -r '.[] | "\(.clientId)\tActive: \(.active)"' | column -t

echo ""
echo "=== Users with Admin Roles ==="
kc_api "roles/admin/users?first=0&max=20" 2>/dev/null | jq -r '.[] | "\(.id)\t\(.username)\t\(.email // "N/A")"' | column -t || echo "No admin role or insufficient permissions"
```

### Event & Audit Logs

```bash
#!/bin/bash
echo "=== Recent Login Events ==="
kc_api "events?first=0&max=30&type=LOGIN,LOGIN_ERROR" | jq -r '.[] | {
    time: .time,
    type: .type,
    user: .userId,
    client: .clientId,
    ip: .ipAddress,
    error: (.error // "none"),
    details: .details
}'

echo ""
echo "=== Admin Events ==="
kc_api "admin-events?first=0&max=20" | jq -r '.[] | "\(.time)\t\(.operationType)\t\(.resourceType)\t\(.resourcePath)"' | column -t

echo ""
echo "=== Event Configuration ==="
kc_api "events/config" | jq '{
    events_enabled: .eventsEnabled,
    admin_events_enabled: .adminEventsEnabled,
    admin_events_details: .adminEventsDetailsEnabled,
    event_types: .enabledEventTypes,
    expiration: .eventsExpiration
}'
```

## Output Format

Present results as a structured report:
```
Managing Keycloak Report
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

- **Token expiry**: Admin tokens expire quickly (default 60s) — refresh before each batch of operations
- **Realm context**: All API calls are realm-scoped — always verify `KC_REALM` is set correctly
- **Client ID vs UUID**: `clientId` is the human-readable name; the UUID `id` is needed for API paths
- **Built-in vs custom flows**: Modifying built-in authentication flows can break login — always check `.builtIn` flag
- **LDAP sync timing**: Full sync can be resource-intensive — check `fullSyncPeriod` before triggering manual sync
- **Session invalidation**: Clearing sessions affects all users in a realm — never clear without explicit request
- **Protocol mappers**: OIDC and SAML have different mapper types — check client protocol before reviewing mappers
- **Composite roles**: A role can contain other roles — always check `.composite` flag to understand effective permissions
