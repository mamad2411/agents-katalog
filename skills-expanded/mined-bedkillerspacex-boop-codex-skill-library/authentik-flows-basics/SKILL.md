---
name: authentik-flows-basics
description: >
  Authentik identity flows for owned IdP deployments: authentication/authorization/
  enrollment/recovery flows, stages, policies, bindings, and blueprints. Use when
  designing or debugging Authentik login MFA enrollment or access policies — not for
  attacking public Authentik instances you do not operate.
---

# Authentik Flows Basics

## Scope And Authorization

- **In scope:** Authentik instances, applications, and flows you administer under authorization.
- **Out of scope:** Credential attacks or flow abuse against third-party Authentik.
- Flows control account lifecycle — test in non-prod; keep emergency admin recovery path.
- Protect blueprint exports; they may contain internal URLs and policy logic (usually not secrets, but still sensitive).
- Pair with `secrets-management-hygiene` for client secrets; `code-quality-standards` for IaC.

## When To Use

- Building or customizing identification → authentication → MFA → user_login flows.
- Adding enrollment, invitation, or password recovery flows.
- Binding policies (expression, reputation, geo) to stages.
- Debugging redirect loops, failed MFA, or wrong application launch URL.
- Exporting/importing blueprints for GitOps.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Auth0 Actions | `auth0-actions-security` |
| SAML SSO assessment | `saml-sso-basics` |
| Generic OAuth app security | OAuth/API auth skills |
| Linux host hardening for the VM | OS hardening skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Object | Role |
| --- | --- |
| Flow | Ordered stages for a purpose (authentication, enrollment, …) |
| Stage | Unit step (identification, password, authenticator validation, …) |
| Policy | Binding that allows/denies or selects stage paths |
| Binding | Attaches policy/stage to flow with order |
| Application + Provider | What user launches after auth (OAuth2/SAML/Proxy/LDAP) |
| Outpost | Reverse proxy / LDAP / RADIUS edge components |

## Common Flow Types

| Designation (typical) | Purpose |
| --- | --- |
| `default-authentication-flow` | Login |
| `default-invalidation-flow` | Logout |
| Enrollment flows | Self-service or invite user creation |
| Recovery flows | Password reset / account recovery |
| Authorization flows | Consent / access checks for apps |

Exact slugs vary by install — always inspect your instance.

## Workflow

### 1. Confirm scope and success criteria

1. Record Authentik version, install method (compose/k8s), domains, SSO apps.
2. Success: users complete login+MFA; unauthorized denied; recovery works for legit users only; admin break-glass documented.
3. Note branded domains and TLS termination.

### 2. Inventory flows and bindings

```bash
# UI: Admin → Flows & Stages → Flows
# API (token with care)
curl -sS -H "Authorization: Bearer $AUTHENTIK_TOKEN" \
  "$AUTHENTIK_URL/api/v3/flows/instances/" | jq '.results[].slug'
```

1. List stages per authentication flow in order.
2. List policies bound to each stage (expression policies especially).
3. Map Applications → Providers → authentication flow override.

### 3. Baseline

1. Export blueprints or screenshots of flow diagrams before change.
2. Capture failing user journeys (HAR redacted).
3. Confirm MFA enrollment state for pilot users.

### 4. Design and modify flows

**Typical authentication chain**

```text
Identification → Password (or source) → MFA validation → User login → (optional) redirect to app
```

**Stage guidance**

| Stage | Tips |
| --- | --- |
| Identification | Prefer email/username policy; captcha/reputation if exposed |
| Password | Rate limits; lockout policies |
| Authenticator validate | TOTP/WebAuthn; allow recovery carefully |
| User write / prompt | Minimize writable fields on login path |
| Consent | Show scopes clearly for OAuth |

**Expression policy sketch (conceptual)**

```python
# Authentik expression policy — allow only corporate email domains
return request.context["prompt_data"].get("email", "").endswith("@example.com")
```

1. Keep expressions small and unit-testable with policy tester.
2. Deny by default for admin apps; separate flow for privileged access.
3. Recovery flow: single-use tokens, short TTL, notify on email change.
4. Enrollment: invitation-only for internal IdP when possible.

**Outposts / proxy providers**

1. Ensure outpost tokens rotated; least network exposure.
2. Forward-auth applications inherit flow security — still enforce app-level authz.

### 5. Verify with evidence

1. Happy path: password + MFA → app launches.
2. Bad password → generic error, rate limited.
3. User without MFA when required → enrollment or deny per policy.
4. Recovery email for unknown user does not account-enumerate if org requires anti-enum (align messages).
5. OAuth app: authorization code flow succeeds; wrong redirect_uri fails.

```bash
# Health
curl -fsS "$AUTHENTIK_URL/-/health/live/"
```

### 6. Observe and harden

1. Events: failed logins, policy denies, MFA failures.
2. Alert on spikes; review suspicious recovery attempts.
3. Keep Authentik and outposts updated; review release notes for flow stage changes.

### 7. Hand off

1. Flow diagram + stage list in runbook.
2. Blueprint Git repo with review; no secrets in blueprints.
3. Break-glass local admin procedure offline.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Login flow | MFA for privileged apps | password-only for admin |
| Policies | explicit allow domains | empty bindings wide open |
| Recovery | short TTL, notify user | long-lived tokens, silent |
| Enrollment | invite-only internal | open registration on Internet IdP |
| Changes | blueprint PR + pilot | live-edit prod only |
| Logs | event review | no monitoring |

## Output Checklist

- [ ] Instance version, domains, apps, authorization recorded
- [ ] Flows/stages/policies inventoried
- [ ] Baseline export taken
- [ ] Authentication + MFA path verified
- [ ] Enrollment/recovery reviewed for abuse cases
- [ ] Application-provider-flow mapping correct
- [ ] Events/monitoring considered
- [ ] Blueprints/Git ownership set
- [ ] Break-glass admin documented
- [ ] `code-quality-standards` applied if IaC shipped

## Rules

- Owned IdP only; flows are security-critical.
- Prefer MFA and invite-only enrollment for internal deployments.
- Test recovery carefully to avoid account takeover paths.
- Keep emergency admin access offline-documented.
- Focus on Authentik flows; SAML/OAuth protocol deep-dives in neighbor skills.
