---
name: captcha-enterprise-integration
description: >
  Integrate enterprise CAPTCHA/bot challenge vendors on owned apps: site keys, server
  verify APIs, score thresholds, action names, CSP/iframe requirements, secrets management,
  fail modes, and mobile/API patterns. Use when reCAPTCHA Enterprise, hCaptcha Enterprise,
  Turnstile, or similar server-side verification wiring — not for abusing third-party sites.
---

# Captcha Enterprise Integration

## Scope And Authorization

- **In scope:** Your applications, keys, and cloud projects for CAPTCHA/bot vendors.
- **Out of scope:** Using your keys to gate third-party sites without rights; fraud operations.
- Protect **secret keys** like production credentials.
- Pair with `captcha-accessibility-balance`, `captcha-bypass-research` (authorized tests), bot-management skills.

## When To Use

- Adding or migrating to enterprise CAPTCHA / managed challenge products.
- Implementing server-side `siteverify` / Assessment APIs correctly.
- Tuning score thresholds and action-based challenges.
- Wiring CSP, domains allowlists, and multi-env keys (dev/stage/prod).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Accessibility balance | `captcha-accessibility-balance` |
| Authorized bypass testing | `captcha-bypass-research` |
| Multi-signal fusion | `bot-management-signal-fusion` |
| Rate limits | rate-limit skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Piece | Role |
| --- | --- |
| Site key | Public; embedded in client |
| Secret / API key | Server only; verify assessments |
| Action | Named event (`login`, `signup`) for binding |
| Score / pass | Vendor risk signal; threshold policy yours |
| Domain allowlist | Vendor console restricts key use |
| CSP | `frame-src` / `script-src` for vendor |

## Workflow

### 1. Confirm scope and success criteria

1. Surfaces, vendor choice, compliance (data residency), mobile needs.
2. Success: server verify mandatory; secrets in secret manager; thresholds documented; staging tests pass; a11y path exists.
3. Decide fail-open vs fail-closed on vendor outage per surface risk.

### 2. Provision keys and projects

1. Create separate keys per environment.
2. Restrict domains/package names in vendor console.
3. Store secrets in Vault/AWS SM/GCP SM — never frontend env `NEXT_PUBLIC_SECRET`.
4. IAM least privilege for assessment APIs (GCP service accounts, etc.).

### 3. Client integration

```html
<!-- Conceptual widget load; follow current vendor docs -->
<script src="https://vendor.example/api.js" async defer></script>
<div class="challenge" data-sitekey="SITE_KEY" data-action="login"></div>
```

```js
// Obtain token for action, send to your backend only over HTTPS
const token = await vendor.execute('SITE_KEY', { action: 'login' });
await fetch('/api/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ user, password, captchaToken: token })
});
```

1. Update CSP allowlists minimally for vendor scripts/frames.
2. Do not trust client-side “success” callbacks alone.
3. Ensure keyboard/AT considerations (`captcha-accessibility-balance`).

### 4. Server verification (mandatory)

```python
# Conceptual verify — use official SDK when available
def verify_captcha(token: str, action: str, remote_ip: str | None) -> None:
    resp = vendor_assess(token=token, secret=SECRET, expected_action=action, ip=remote_ip)
    if not resp.ok:
        raise PermissionError("captcha_failed")
    if resp.action != action:
        raise PermissionError("captcha_action_mismatch")
    if resp.score < THRESHOLD:  # for score-based products
        raise PermissionError("captcha_low_score")
    # optional: persist token id for one-time use
    mark_used(resp.token_id)
```

**Requirements:**

1. Verify on **every** protected server route (web + mobile BFF).
2. Check action/hostname claims when vendor provides them.
3. Enforce one-time use if tokens can be replayed.
4. Timeouts on vendor HTTP; defined fail mode.
5. Metrics: `captcha_verify_total{result}`.

### 5. Thresholds and policy

| Surface | Typical policy sketch |
| --- | --- |
| Login | Score ≥ X or challenge; lockout + rate limit |
| Signup | Stricter threshold |
| Low-risk browse | Invisible / no challenge |
| Admin | Prefer stronger MFA over CAPTCHA alone |

1. Document scores and review quarterly (distribution drift).
2. Combine with rate limits and bot signals — CAPTCHA is not sufficient alone.
3. Logging: store reason codes; avoid logging full tokens.

### 6. Verify integration

```bash
# Staging tests
# - missing token → 400/403
# - garbage token → reject
# - valid token → allow once; replay → reject if one-time
curl -s -X POST https://staging.example/api/login -d '{"captchaToken":""}' 
```

1. Domain mismatch: token from wrong site key fails.
2. Load test vendor latency impact on login p99.
3. Run authorized control tests from `captcha-bypass-research` checklist.
4. AT smoke on widget.

### 7. Hand off

1. Runbook: rotate secrets; vendor outage mode; threshold change process.
2. Dashboard verify fail rates and vendor errors.
3. Apply `code-quality-standards`; secret scan CI for leaked site secrets.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Secret | Server secret manager | Secret in mobile app binary |
| Verify | Always server-side | Client `if (token) ok` |
| Keys | Per-env + domain allowlist | One global key all envs |
| Replay | One-time store | Accept same token N times |
| Outage | Documented degrade + limits | Silent allow all |
| Policy | CAPTCHA + rate limit + MFA | CAPTCHA only forever |

## Output Checklist

- [ ] Vendor project/keys per env provisioned
- [ ] Secrets stored server-side only
- [ ] Client widget + CSP configured
- [ ] Server verify on all protected routes
- [ ] Action/hostname/score checks applied
- [ ] One-time / TTL policy implemented
- [ ] Fail mode documented and tested
- [ ] Metrics/alerts live
- [ ] A11y alternative path linked
- [ ] Authorized bypass checklist retested
- [ ] `code-quality-standards` applied

## Rules

- Server verification with protected secrets is mandatory.
- Separate environments and restrict key domains.
- CAPTCHA complements rate limits and auth — does not replace them.
- Authorized apps only.
- Accessibility and control testing have dedicated skills — use them.
