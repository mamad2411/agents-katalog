---
name: entra-conditional-access
description: >
  Microsoft Entra Conditional Access for owned tenants: MFA grants, platform and
  location conditions, compliant device, session controls, report-only rollout,
  and break-glass exclusions. Use when CA policies, require MFA, block legacy
  auth, or risk-based access—not app consent policies alone.
---

# Entra Conditional Access

## Scope And Authorization

- **In scope:** Entra ID tenants you administer with change control.
- **Out of scope:** Applying policies to tenants without authorization.
- Misconfigured CA can lock out the organization—always protect break-glass accounts **before** broad enforcement.
- Use **report-only** then pilot then on.
- Redact user UPNs in external reports when required.

## When To Use

- Requiring MFA for all users or admins.
- Blocking legacy authentication.
- Requiring compliant/hybrid joined devices for sensitive apps.
- Location-based or insider risk signals (with licensing).
- Session controls (sign-in frequency, app enforced restrictions).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| OAuth app consent lockdown | `entra-app-consent-policies` |
| SAML SSO issues | `saml-sso-basics` |
| Password reset poisoning | `password-reset-poisoning` |
| Secrets program | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Assignments | Users/groups/apps; exclude break-glass |
| Cloud apps | Prefer all + exclude only with justification |
| Conditions | Client apps (legacy), locations, platforms, risk |
| Grant | MFA, compliant device, password change, block |
| Session | Sign-in frequency, persistent browser, CAE |
| Rollout | Report-only → pilot group → all |

## Workflow

### 1. Confirm scope and success criteria

1. Tenant, licensing (P1/P2 features), admin owners.
2. Success: MFA enforced for target personas; legacy auth blocked; zero unintended global lockout.

### 2. Protect break-glass **first**

1. At least two cloud-only emergency accounts with long random passwords in offline vault.
2. **Exclude** them from all CA policies (or dedicated policy that still logs).
3. Monitor every sign-in of break-glass accounts (alert).

### 3. Inventory existing CA

```powershell
Connect-MgGraph -Scopes "Policy.Read.All"
Get-MgIdentityConditionalAccessPolicy | Select-Object Id, DisplayName, State
```

1. Export policy JSON for backup.
2. Note conflicts (multiple policies grant vs block).

### 4. Baseline with report-only

1. Create policies in **report-only** mode.
2. Review Insights / log analytics: would-block counts by app.
3. Fix app compatibility (legacy protocols, service accounts).

### 5. Implement core policies (examples)

| Policy | Intent |
| --- | --- |
| MFA for all users | Grant: require MFA; all apps |
| MFA for admins | Stronger: phishing-resistant if available |
| Block legacy auth | Condition client apps: other clients → Block |
| Compliant device for sensitive | Office 365 / admin portals |
| Block high risk sign-in | Identity protection signals (if licensed) |

1. Prefer named groups for pilots (`CA-Pilot-Users`).
2. Service accounts: move to managed identities / cert auth; exclude sparingly with expiry.
3. Document every exclusion with owner + review date.

### 6. Enforce and verify

1. Flip pilot to **On**; validate MFA enrollment capacity.
2. Expand to all users during change window.
3. Test: standard user without MFA challenged; legacy auth blocked; break-glass still works from documented procedure.

```powershell
# Sign-in logs review (portal or Graph) for failures after enforcement
# WhatIf tools / CA insights for specific user scenarios
```

### 7. Hand off

1. Runbook: user MFA lockout, device compliance fail, travel scenarios.
2. Continuous access evaluation considerations for session revocation.
3. Quarterly policy review; remove dead exclusions.
4. Coordinate consent policies for OAuth risk.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Break-glass | Excluded + monitored | No emergency account |
| Rollout | Report-only → pilot → all | Enforce all users day one |
| Legacy auth | Blocked | Left open for “printers forever” |
| Exclusions | Ticketed + expiry | Entire company excluded |
| Admins | Phishing-resistant MFA | SMS only forever |

## Output Checklist

- [ ] Break-glass accounts ready and excluded
- [ ] Policy backup exported
- [ ] Report-only insights reviewed
- [ ] Core MFA + legacy block policies on for target scope
- [ ] Exclusions documented with owners
- [ ] Test evidence for allow/challenge/block
- [ ] Support runbooks published
- [ ] Residual risk and review date noted

## Rules

- Never enforce broad CA without break-glass.
- Report-only first for major changes.
- Minimize standing exclusions.
- Pair with app consent policies for OAuth threats.
- Authorized tenant admins only.
