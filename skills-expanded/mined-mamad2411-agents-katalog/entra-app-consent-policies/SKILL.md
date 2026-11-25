---
name: entra-app-consent-policies
description: >
  Microsoft Entra ID (Azure AD) app consent policies for owned tenants: user
  consent restrictions, admin consent workflows, permission classifications,
  app governance, and blocking risky OAuth consent phishing. Use when
  oauth2PermissionGrants, admin consent, verified publishers, or consent
  policies—not Conditional Access alone (see entra-conditional-access).
---

# Entra App Consent Policies

## Scope And Authorization

- **In scope:** Entra tenants your organization owns; changes via approved identity admins.
- **Out of scope:** Altering another tenant’s consent settings; simulating consent phishing against real users without authorization.
- Consent grants can expose mail/files—treat reviews as high privilege.
- Prefer pilot groups before tenant-wide consent lockdown.
- Pair with `entra-conditional-access` and `secrets-management-hygiene` for app secrets.

## When To Use

- Stopping users from granting high-risk Graph permissions to any app.
- Implementing admin consent request workflow.
- Reviewing existing OAuth grants after a consent-phishing incident.
- Classifying permissions (low vs high impact) for policy.
- Governing multi-tenant apps and publisher verification requirements.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Conditional Access / MFA grants | `entra-conditional-access` |
| SAML SSO app review | `saml-sso-basics` |
| Generic OAuth app security | OAuth skills in catalog |
| Secrets for app registrations | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| User consent | Disable or limit to verified publishers + low-risk perms |
| Admin consent | Workflow with reviewers; audit trail |
| Grants | Inventory `oauth2PermissionGrants` / app role assignments |
| Classification | Mark Mail.ReadWrite, Files.ReadWrite.All as high risk |
| Detection | Alerts on new high-privilege grants |
| Break-glass | Emergency admin path documented |

## Workflow

### 1. Confirm scope and success criteria

1. Tenant ID, current consent configuration, identity governance owners.
2. Success: users cannot consent high-risk perms; admins review via workflow; stale grants cleaned.

### 2. Inventory current consent posture

```powershell
# Microsoft Graph / Microsoft.Graph PowerShell examples (authorized admin)
Connect-MgGraph -Scopes "Policy.Read.All","Application.Read.All","DelegatedPermissionGrant.Read.All"
Get-MgPolicyAuthorizationPolicy | Format-List
Get-MgOauth2PermissionGrant -All | Select-Object Id, ClientId, Scope, ConsentType | Select-Object -First 50
```

1. Portal: Enterprise applications → Consent and permissions.
2. List apps with `Directory.ReadWrite.All`, `Mail.Read`, full_access_as_app, etc.

### 3. Baseline risk

| Finding | Risk |
| --- | --- |
| Users can consent to any permission | Consent phishing |
| No admin consent workflow | Shadow IT friction / unsafe workarounds |
| Orphaned grants to unused apps | Persistent access |
| Multi-tenant apps without publisher verify | Higher abuse likelihood |

### 4. Apply policies

1. **Disable user consent** or allow only **selected permissions** from **verified publishers**.
2. Enable **admin consent requests** with designated reviewers and expiry for requests.
3. Use **permission classifications** (low impact allowlist for user consent if partially enabled).
4. Require assignment for enterprise apps where appropriate (`user assignment required`).
5. Prefer **app roles** / least Graph scopes for first-party apps you develop.

```text
# Policy intent (configure via portal or Graph authorizationPolicy / permissionGrantPolicies)
- defaultUserRolePermissions.permissionGrantPoliciesAssigned → limited policies
- Admin consent workflow: ON
- Risk-based: block legacy auth separately via CA
```

### 5. Clean and monitor grants

1. Revoke grants for unused or untrusted clients after owner notification.
2. Alert on new grants with high-privilege scopes (SIEM / Entra recommendations / Defender for Cloud Apps).
3. Review service principals created from multi-tenant apps weekly during lockdown.

### 6. Verify with evidence

1. Standard user attempts to consent to a high-risk lab app → blocked / admin request created.
2. Admin request path succeeds for approved app.
3. Export before/after grant counts and policy screenshots (redact secrets).

### 7. Hand off

1. Runbook for app owners requesting Graph permissions.
2. Quarterly access review of OAuth grants.
3. Coordinate with CA policies for location/risk on admin reviewers.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| User consent | Off or low-risk only | Any user, any Graph scope |
| Review | Admin workflow + SLA | Slack “please click accept” |
| Grants | Periodic revoke | Eternal Mail.Read for abandoned app |
| First-party apps | Least scopes | `.default` with huge surface |
| Evidence | Test user blocked | Policy toggle without test |

## Output Checklist

- [ ] Current authorization/consent policy recorded
- [ ] High-privilege grants inventoried
- [ ] User consent restricted
- [ ] Admin consent workflow enabled with reviewers
- [ ] Test evidence of block + request path
- [ ] Monitoring for new risky grants
- [ ] App owner request process documented
- [ ] Residual risk noted

## Rules

- Tenant admin authorization required for changes.
- Do not phish real users to “test consent.”
- Least privilege Graph scopes for internal apps.
- Pair with Conditional Access for admin accounts.
- Document break-glass for emergency app enablement.
