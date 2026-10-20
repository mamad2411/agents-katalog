---
name: auth0-actions-security
description: >
  Auth0 Actions security for owned tenants: Login/MFA/credentials-exchange flows,
  secrets handling, least-privilege Management API usage, redirect/callback safety,
  deny/allow logic, and logging without leaking tokens. Use when writing or reviewing
  Auth0 Actions/Hooks migrations — not for attacking third-party Auth0 tenants.
---

# Auth0 Actions Security

## Scope And Authorization

- **In scope:** Auth0 tenants, Applications, and Actions you administer or assess with authorization.
- **Out of scope:** Credential stuffing, tenant takeover, or abusing others’ Auth0 configurations.
- Actions run in Auth0’s pipeline with access to event user data — treat code as production auth logic.
- Store secrets only in Action Secrets UI / IaC secret vars; never hardcode.
- Pair with `secrets-management-hygiene` and `code-quality-standards`.

## When To Use

- Implementing post-login enrichment, MFA gates, allowlists, or claims customization.
- Reviewing Actions for SSRF via redirects, open redirects, or unsafe `fetch`.
- Migrating Rules/Hooks to Actions securely.
- Adding Management API calls from Actions with minimal scopes.
- Debugging login failures introduced by Action exceptions.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Generic OAuth/OIDC app integration | OAuth skills / API auth |
| Full ATO methodology | `account-takeover-methodology` (authorized) |
| SAML enterprise IdP | `saml-sso-basics` |
| Password reset Host header issues | `password-reset-poisoning` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Trigger | Typical use | Risk focus |
| --- | --- | --- |
| Login / Post-Login | claims, MFA, blocks | deny correctness, redirects |
| Pre-User Registration | validation | injection into metadata |
| Post-User Registration | provisioning | privileged API calls |
| Credentials Exchange | M2M customization | excessive claims/scopes |
| Password / ID token etc. | specialized | token content leakage |

| Control | Guidance |
| --- | --- |
| Secrets | Action secrets; rotate; least number |
| Network | Allowlisted external URLs only |
| Fail mode | Fail closed for authz decisions when dependency errors |
| Logs | No access tokens, refresh tokens, passwords, raw secrets |

## Workflow

### 1. Confirm scope and success criteria

1. Record tenant, env (dev/prod), Application types (SPA/native/M2M), Action triggers.
2. Success: unauthorized users blocked; secrets not in code; external calls timeout; no PII over-logging; login still works for legit users.
3. Map break-glass: disable Action or tenant admin access.

### 2. Inventory Actions and secrets

1. List Actions bound to flows (Auth0 Dashboard → Actions → Flows).
2. Export Action code to Git if org uses Deploy CLI / Terraform.
3. Inventory secrets names (not values) and Management API grants.

```bash
# If Auth0 Deploy CLI configured (owned tenant)
a0deploy export --format yaml --output_folder ./auth0-export
```

### 3. Baseline

1. Capture login success rate and Action error metrics before change.
2. Unit-test critical deny/allow decisions with sample `event` fixtures.
3. Note external dependencies (risk APIs, HRIS, feature flags).

### 4. Apply secure Action patterns

**Post-login allowlist / deny (sketch):**

```js
/**
 * Handler that runs after user authentication.
 * @param {Event} event
 * @param {PostLoginAPI} api
 */
exports.onExecutePostLogin = async (event, api) => {
  const email = event.user.email || "";
  const domain = email.split("@")[1]?.toLowerCase();
  const allowed = (event.secrets.ALLOWED_DOMAINS || "").split(",").map((s) => s.trim());

  if (!domain || !allowed.includes(domain)) {
    api.access.deny("access_denied", "User is not allowed.");
    return;
  }

  // Custom claims — use namespaced URLs
  api.idToken.setCustomClaim("https://example.com/role", event.user.app_metadata?.role || "user");
  api.accessToken.setCustomClaim("https://example.com/role", event.user.app_metadata?.role || "user");
};
```

**Secrets & fetch hygiene**

```js
const controller = new AbortController();
const t = setTimeout(() => controller.abort(), 2000);
try {
  const res = await fetch(event.secrets.RISK_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${event.secrets.RISK_TOKEN}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ user_id: event.user.user_id }),
    signal: controller.signal,
  });
  if (!res.ok) {
    api.access.deny("access_denied", "Risk check failed.");
    return;
  }
} catch (_) {
  api.access.deny("access_denied", "Risk check unavailable."); // fail closed for high-risk apps
  return;
} finally {
  clearTimeout(t);
}
```

1. Prefer fail **closed** for security checks; fail open only with explicit risk acceptance.
2. Validate redirect URLs against allowlists if using `api.redirect`.
3. Management API: dedicated M2M app, minimal scopes (`read:users` not `update:users` if only reading).
4. Avoid logging `event.request` wholesale — may include PII and tokens.
5. Do not trust client-supplied metadata for authorization without server-side verification.

**Claims**

1. Namespace custom claims (`https://your-domain/claim`).
2. Keep tokens small; put authorization details in RBAC/permissions where possible.
3. Never put secrets in ID/access tokens.

### 5. Verify with evidence

1. Login as allowed domain user → success; claims present.
2. Login as disallowed → denied with generic message.
3. Rotate secret → Action still works via dashboard secret, not code.
4. Simulate risk API timeout → expected deny/allow per policy.
5. Confirm logs in Monitoring free of tokens.

```bash
# OIDC smoke (owned app)
curl -sS -X POST "https://$TENANT/oauth/token" -d "grant_type=..." # use test client only
```

### 6. Observe and harden

1. Monitor Action failure rate and login error codes.
2. Alert on sudden deny spikes (misconfig) or drop to zero denies (Action unbound).
3. Quarterly review: unused secrets, over-scoped M2M apps, dead Actions.

### 7. Hand off

1. Document Action order in flow diagram.
2. CODEOWNERS for Action source; change control for prod tenant.
3. Runbook: disable Action quickly if lockout.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secrets | Action secrets + rotation | Hardcoded API keys |
| Failures | Timeout + fail closed | Unbounded fetch, fail open silently |
| Claims | Namespaced, minimal | Secrets in tokens |
| Redirects | Allowlisted URLs | User-controlled redirect_uri in Action |
| Logs | Redacted | console.log(event) |
| Mgmt API | Least scopes | Global client secret in Action |

## Output Checklist

- [ ] Tenant/apps/triggers/authorization recorded
- [ ] Actions inventoried; secrets not in source
- [ ] Deny/allow logic tested with fixtures
- [ ] External calls timed out; fail mode documented
- [ ] Claims namespaced; no secrets in tokens
- [ ] Management API scopes minimal
- [ ] Logging redaction verified
- [ ] Monitoring/alerts considered
- [ ] `code-quality-standards` applied to Action code

## Rules

- Owned tenants only; Actions are production auth code.
- Fail closed for authorization-critical checks unless explicitly waived.
- Never log passwords, OTPs, or tokens.
- Prefer Auth0 RBAC/permissions over ad-hoc unchecked metadata.
- Focus on Actions security; broader ATO and protocol attacks use dedicated authorized skills.
