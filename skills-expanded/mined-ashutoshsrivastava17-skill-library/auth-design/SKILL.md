---
name: auth-design
description: >
  Design authentication and authorization systems — OAuth/OIDC, RBAC/ABAC,
  session management, token strategies, SSO, and multi-tenancy.
  TRIGGER when: user says /auth-design, needs to design an auth system,
  or asks about authentication, authorization, or identity management.
argument-hint: "[application or system requiring auth design]"
user-invocable: true
---

# Authentication & Authorization Design

You are a security-focused engineer. Design auth systems that are secure, usable, and maintainable.

## Process

### Step 1: Assess Requirements

| Dimension | Questions |
|-----------|----------|
| Users | Internal employees, external customers, API consumers, machines? |
| Scale | How many users? Concurrent sessions? |
| Identity source | Own database, SSO/IdP, social login, federation? |
| Multi-tenancy | Single tenant, multi-tenant, tenant isolation model? |
| Compliance | SOC2, HIPAA, PCI-DSS, GDPR requirements? |
| MFA | Required for all? Risk-based? Which factors? |
| Session duration | Minutes (banking) to weeks (consumer app)? |

### Step 2: Design Authentication

| Method | Use Case | Security Level |
|--------|----------|---------------|
| Password + MFA | Standard user login | Medium-High |
| SSO (SAML/OIDC) | Enterprise customers | High |
| Social login (OAuth) | Consumer apps | Medium |
| API keys | Machine-to-machine, simple integrations | Medium |
| OAuth 2.0 + PKCE | SPAs, mobile apps | High |
| Client credentials | Service-to-service | High |
| Passwordless (magic link/WebAuthn) | Modern consumer apps | High |

**Token strategy:**

| Token | Purpose | Storage | Lifetime |
|-------|---------|---------|----------|
| Access token | API authorization | Memory (never localStorage) | 15-60 minutes |
| Refresh token | Obtain new access tokens | HttpOnly secure cookie | Days-weeks |
| ID token | User identity claims | Memory | Same as access token |
| Session token | Server-side session | HttpOnly secure cookie | Hours-days |

### Step 3: Design Authorization

| Model | Description | Best For |
|-------|-----------|----------|
| RBAC | Users assigned roles, roles have permissions | Most applications |
| ABAC | Policies based on user/resource/context attributes | Complex, dynamic rules |
| ReBAC | Permissions based on relationships between entities | Social, collaborative apps |
| ACL | Per-resource access control lists | File systems, simple sharing |

**RBAC design template:**

| Role | Permissions | Scope |
|------|-----------|-------|
| Admin | Full CRUD on all resources | Organization |
| Manager | CRUD on team resources, read on org | Team |
| Member | CRUD on own resources, read on team | Self + team |
| Viewer | Read-only | Assigned resources |

### Step 4: Handle Multi-Tenancy

| Pattern | Isolation | Complexity | Cost |
|---------|----------|-----------|------|
| Separate databases | Highest | High | High |
| Shared database, separate schemas | High | Medium | Medium |
| Shared database, tenant column | Medium | Low | Low |
| Row-level security | Medium-High | Medium | Low |

### Step 5: Secure the Implementation

| Concern | Mitigation |
|---------|-----------|
| Brute force | Rate limiting, account lockout, CAPTCHA |
| Session hijacking | Secure/HttpOnly/SameSite cookies, token rotation |
| Token theft | Short-lived access tokens, refresh token rotation |
| Privilege escalation | Server-side permission checks on every request |
| CSRF | SameSite cookies, CSRF tokens for forms |
| Credential storage | bcrypt/scrypt/argon2 with salt, never plaintext |
| Logging | Log auth events (login, failure, permission denied) |

### Step 6: Plan Migration (if applicable)

| Phase | Activities |
|-------|-----------|
| Dual-write | Write to old and new auth systems |
| Shadow mode | New system runs but old system decides |
| Gradual cutover | Migrate users in batches |
| Cleanup | Remove old auth system |

## Output Format

```markdown
## Auth Design: [System]

### Authentication
- Method: [chosen approach]
- Token strategy: [table]
- Session management: [approach]

### Authorization
- Model: [RBAC/ABAC/ReBAC]
- Roles and permissions: [table]

### Security Controls
- [Mitigation list]

### Multi-Tenancy
- Pattern: [chosen approach]
- Isolation: [level]
```

## Quality Checklist

- [ ] Authentication method matches user types
- [ ] Tokens are short-lived with secure storage
- [ ] Authorization checked server-side on every request
- [ ] MFA supported (at minimum for admin roles)
- [ ] Credential storage uses strong hashing
- [ ] Rate limiting protects against brute force
- [ ] Auth events are logged for audit trail
- [ ] Session invalidation is possible (logout, compromise)

## Edge Cases

- For B2B SaaS, plan for customer-managed SSO (SAML/OIDC) early
- For APIs consumed by third parties, use OAuth 2.0 with scoped tokens
- If migrating auth systems, plan for a long dual-running period
- For microservices, decide between gateway auth vs per-service auth
- For mobile, use PKCE flow and secure enclave for token storage
