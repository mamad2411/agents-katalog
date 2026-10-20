---
name: managing-fusionauth
description: |
  Use when working with Fusionauth — fusionAuth identity platform management for
  tenant configuration, application setup, theme customization, webhook
  configuration, user management, and audit log review. Covers login flows,
  passwordless auth, identity providers, and multi-tenant architecture. Read
  this skill before any FusionAuth operations — it enforces discovery-first
  patterns and strict read-only safety rules.
connection_type: fusionauth
preload: false
---

# FusionAuth Management Skill

Safely read and audit FusionAuth — the developer-focused identity and access management platform.

## MANDATORY: Discovery-First Pattern

**Always discover tenants, applications, and identity providers before performing targeted queries. Never guess tenant or application IDs.**

### Phase 1: Discovery

```bash
#!/bin/bash

fa_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: $FUSIONAUTH_API_KEY" \
         -H "Content-Type: application/json" \
         "${FUSIONAUTH_URL}/api/${endpoint}"
}

echo "=== FusionAuth Status ==="
curl -s "${FUSIONAUTH_URL}/api/status" | jq '.'

echo ""
echo "=== Tenants ==="
fa_api "tenant" | jq -r '.tenants[] | "\(.id)\t\(.name)\t\(.configured)"' | column -t

echo ""
echo "=== Applications ==="
fa_api "application" | jq -r '.applications[] | "\(.id)\t\(.name)\t\(.active)\t\(.tenantId)"' | column -t

echo ""
echo "=== Identity Providers ==="
fa_api "identity-provider" | jq -r '.identityProviders[]? | "\(.id)\t\(.name)\t\(.type)\t\(.enabled)"' | column -t

echo ""
echo "=== Themes ==="
fa_api "theme" | jq -r '.themes[]? | "\(.id)\t\(.name)\t\(.insertInstant)"' | column -t

echo ""
echo "=== Webhooks ==="
fa_api "webhook" | jq -r '.webhooks[]? | "\(.id)\t\(.url)\t\(.global)\tEvents: \(.eventsEnabled | keys | length)"' | column -t
```

**Phase 1 outputs:** Tenant list, applications, identity providers, themes, webhooks — only reference these in subsequent operations.

## Anti-Hallucination Rules

- **NEVER guess tenant or application IDs** — always discover in Phase 1
- **NEVER assume identity provider names** — always list first
- **NEVER fabricate theme or webhook IDs** — always list before querying
- **ONLY read and list** — never create, update, or delete without explicit request

## Safety Rules

- **READ-ONLY by default**: GET requests only — tenants, applications, users, themes, webhooks, audit logs
- **MASK sensitive data**: Redact API keys, client secrets, HMAC secrets, and user passwords
- **FORBIDDEN without explicit request**: POST/PUT/DELETE to tenants, applications, users; key generation; password changes
- **NEVER print API keys**: Always redact key values in output

## Core Helper Functions

```bash
#!/bin/bash

fa_api() {
    local endpoint="$1"
    local method="${2:-GET}"
    curl -s -X "$method" \
         -H "Authorization: $FUSIONAUTH_API_KEY" \
         -H "Content-Type: application/json" \
         "${FUSIONAUTH_URL}/api/${endpoint}"
}

# Search users
fa_search_users() {
    local query="$1"
    local max="${2:-25}"
    curl -s -X POST \
         -H "Authorization: $FUSIONAUTH_API_KEY" \
         -H "Content-Type: application/json" \
         -d "{\"search\":{\"queryString\":\"${query}\",\"numberOfResults\":${max}}}" \
         "${FUSIONAUTH_URL}/api/user/search"
}

# Tenant-scoped API call
fa_api_tenant() {
    local tenant_id="$1"
    local endpoint="$2"
    curl -s -H "Authorization: $FUSIONAUTH_API_KEY" \
         -H "X-FusionAuth-TenantId: $tenant_id" \
         -H "Content-Type: application/json" \
         "${FUSIONAUTH_URL}/api/${endpoint}"
}
```

## Common Operations

### Tenant Configuration

```bash
#!/bin/bash
TENANT_ID="${1:?Tenant ID required — discover via Phase 1}"

echo "=== Tenant Details ==="
fa_api "tenant/${TENANT_ID}" | jq '.tenant | {
    id: .id,
    name: .name,
    configured: .configured,
    issuer: .issuer,
    login_config: {
        require_authentication: .loginConfiguration.requireAuthentication
    },
    email_config: {
        host: .emailConfiguration.host,
        port: .emailConfiguration.port,
        security: .emailConfiguration.security,
        verification_required: .emailConfiguration.verifyEmail
    },
    jwt_config: {
        access_token_ttl: .jwtConfiguration.timeToLiveInSeconds,
        refresh_token_ttl: .jwtConfiguration.refreshTokenTimeToLiveInMinutes,
        refresh_token_usage: .jwtConfiguration.refreshTokenUsagePolicy
    },
    password_validation: .passwordValidationRules,
    rate_limit: .rateLimitConfiguration
}'

echo ""
echo "=== Tenant MFA Configuration ==="
fa_api "tenant/${TENANT_ID}" | jq '.tenant.multiFactorConfiguration'

echo ""
echo "=== External Identifier Config ==="
fa_api "tenant/${TENANT_ID}" | jq '.tenant.externalIdentifierConfiguration | {
    authorization_grant_timeout: .authorizationGrantIdTimeToLiveInSeconds,
    change_password_timeout: .changePasswordIdTimeToLiveInSeconds,
    email_verification_timeout: .emailVerificationIdTimeToLiveInSeconds,
    setup_password_timeout: .setupPasswordIdTimeToLiveInSeconds
}'
```

### Application Configuration

```bash
#!/bin/bash
APP_ID="${1:?Application ID required — discover via Phase 1}"

echo "=== Application Details ==="
fa_api "application/${APP_ID}" | jq '.application | {
    id: .id,
    name: .name,
    active: .active,
    tenant_id: .tenantId,
    verification_strategy: .verificationStrategy,
    oauth_config: {
        client_id: .oauthConfiguration.clientId,
        client_secret: "*** REDACTED ***",
        authorized_origins: .oauthConfiguration.authorizedOriginURLs,
        authorized_redirects: .oauthConfiguration.authorizedRedirectURLs,
        logout_url: .oauthConfiguration.logoutURL,
        enabled_grants: .oauthConfiguration.enabledGrants,
        require_pkce: .oauthConfiguration.requireClientAuthentication
    },
    registration_config: .registrationConfiguration,
    login_config: .loginConfiguration
}'

echo ""
echo "=== Application Roles ==="
fa_api "application/${APP_ID}" | jq -r '.application.roles[]? | "\(.id)\t\(.name)\t\(.description // "N/A")\tDefault:\(.isDefault)\tSuper:\(.isSuperRole)"' | column -t
```

### Theme Management

```bash
#!/bin/bash
echo "=== All Themes ==="
fa_api "theme" | jq -r '.themes[] | {
    id: .id,
    name: .name,
    default: (.defaultMessages != null),
    insert_instant: .insertInstant,
    last_update: .lastUpdateInstant
}'

THEME_ID="${1:-}"
if [ -n "$THEME_ID" ]; then
    echo ""
    echo "=== Theme Templates: $THEME_ID ==="
    fa_api "theme/${THEME_ID}" | jq '.theme | {
        name: .name,
        has_stylesheet: (.stylesheet != null and .stylesheet != ""),
        templates: (to_entries | map(select(.key | test("^(oauth|email|account)"))) | map(.key) | sort)
    }'
fi
```

### Webhook Configuration

```bash
#!/bin/bash
echo "=== All Webhooks ==="
fa_api "webhook" | jq -r '.webhooks[] | {
    id: .id,
    url: .url,
    global: .global,
    connect_timeout: .connectTimeout,
    read_timeout: .readTimeout,
    ssl_certificate: (if .sslCertificate then "configured" else "none" end),
    events_enabled: (.eventsEnabled | to_entries | map(select(.value == true)) | map(.key))
}'

echo ""
echo "=== Webhook Event Summary ==="
fa_api "webhook" | jq -r '.webhooks[] | "\(.url)\tEvents: \(.eventsEnabled | to_entries | map(select(.value == true)) | length)"' | column -t
```

### User Management & Audit

```bash
#!/bin/bash
SEARCH="${1:?Search term required}"

echo "=== User Search: $SEARCH ==="
fa_search_users "$SEARCH" | jq -r '.users[]? | {
    id: .id,
    email: .email,
    username: .username,
    name: "\(.firstName // "") \(.lastName // "")",
    active: .active,
    verified: .verified,
    two_factor_enabled: (.twoFactor.methods | length > 0),
    insert_instant: .insertInstant,
    last_login: .lastLoginInstant,
    registrations: [.registrations[]? | {app_id: .applicationId, roles: .roles}]
}'

echo ""
echo "=== Audit Log (recent 20) ==="
fa_api "system/audit-log?numberOfResults=20&sortField=insertInstant&sortOrder=desc" | jq -r '.auditLogs[]? | "\(.insertInstant)\t\(.user.email // .user.loginId // "system")\t\(.reason)\t\(.data.attributes // "N/A")"' | column -t

echo ""
echo "=== Login Records ==="
fa_api "system/login-record/export?limit=20" 2>/dev/null | jq -r '.loginRecords[]? | "\(.instant)\t\(.userId)\t\(.applicationId)\t\(.ipAddress)"' | column -t || echo "Login records endpoint may vary by version"
```

## Output Format

Present results as a structured report:
```
Managing Fusionauth Report
══════════════════════════
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

- **API key scope**: API keys can be tenant-scoped or global — tenant-scoped keys return 401 for other tenants
- **Multi-tenant header**: Use `X-FusionAuth-TenantId` header to scope requests to a specific tenant
- **User search syntax**: Search uses Elasticsearch query string syntax — special characters must be escaped
- **Theme inheritance**: Custom themes inherit from the default theme — missing templates fall back to default
- **Webhook retry**: Failed webhooks are retried with exponential backoff — check webhook event logs for delivery status
- **Application roles vs groups**: Roles are per-application; groups are global to tenant — use roles for app-specific authorization
- **JWT signing keys**: Each application can have its own signing key — verify key configuration per app
- **Lambda functions**: FusionAuth uses Lambdas (JavaScript functions) for token customization — review Lambda code for security
