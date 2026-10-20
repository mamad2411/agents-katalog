---
name: base-uri-csp
description: >
  Content-Security-Policy base-uri directive for owned web apps: restricting
  document base URL hijacking, combining with default-src/script-src, reporting,
  and testing <base> injection. Use when hardening CSP or fixing open base-uri —
  not for bypassing third-party CSPs without authorization.
---

# CSP `base-uri` Directive

## Scope And Authorization

- **In scope:** Web applications you own or are authorized to harden.
- **Out of scope:** Exploiting base tag injection on third-party sites.
- CSP changes can break relative URL resolution — test staging thoroughly.
- Pair broader XSS defense with `xss-cross-site-scripting`; use `code-quality-standards` for header code.

## When To Use

- Setting or reviewing `Content-Security-Policy` headers/meta.
- Findings: missing `base-uri` allowing attacker-controlled `<base href>`.
- Apps that use relative script/style/form URLs.
- Deploying CSP report-only first for `base-uri` violations.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full XSS methodology | `xss-cross-site-scripting` |
| General security headers (nginx) | `nginx-security-headers` |
| CAPTCHA / bot controls | bot/WAF skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Directive | Role |
| --- | --- |
| `base-uri` | Allowed base URLs for the document (limits `<base>`) |
| `default-src` | Fallback for many fetches — **does not** replace `base-uri` |
| `script-src` | Script sources; still needed separately |
| `form-action` | Form submit targets (related navigation hardening) |
| Tooling | Browser devtools, securityheaders scanners, CSP evaluators, unit tests for headers |

## Workflow

### 1. Confirm scope and success criteria

1. App URLs, CSP delivery (header vs meta), CDNs, authorization.
2. Success: `base-uri 'self'` (or explicit allowlist); injected `<base>` does not redirect relative fetches off-site.
3. No broken assets from legitimate base tags if any.

### 2. Inventory current CSP

```bash
curl -sI https://app.example.local/ | rg -i 'content-security-policy'
# Search templates for <base
rg -n "<base" --glob '*.{html,tsx,jsx,vue,ejs,hbs}'
```

1. Note report-uri/report-to endpoints.
2. List environments (some miss headers behind CDN).
3. Check meta CSP conflicting with header CSP.

### 3. Baseline risk

1. Without `base-uri`, injected `<base href="https://evil.example/">` can make relative script/image/form URLs load from attacker origin (depending on other directives and markup).
2. Map pages using relative URLs heavily.
3. Record any intentional cross-origin base (rare).

### 4. Apply `base-uri`

**Recommended starting point:**

```http
Content-Security-Policy: default-src 'self'; script-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'
```

```nginx
add_header Content-Security-Policy "default-src 'self'; base-uri 'self'; object-src 'none'" always;
```

```python
# Flask example
@app.after_request
def csp(resp):
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; base-uri 'self'; object-src 'none'"
    )
    return resp
```

1. Prefer header over `<meta>` for defense consistency.
2. Use report-only first:

```http
Content-Security-Policy-Report-Only: base-uri 'self'
```

3. If multi-host app, allowlist explicit bases: `base-uri 'self' https://cdn.example.com` (only if required).
4. Combine with auto-escaping and input validation — CSP is depth-in-defense.

### 5. Verify with evidence

```bash
curl -sI https://staging.example/ | rg -i content-security-policy
```

1. Browser test: inject `<base href="https://example.com/">` in a lab page under CSP — relative loads should violate policy / not rebind unexpectedly.
2. Functional test: login, assets, forms still work.
3. Collect violation reports for false positives.

### 6. Observe and harden

1. Monitor CSP reports for `base-uri` violations.
2. CDN/header duplication: ensure edge doesn’t strip CSP.
3. Periodic review alongside `script-src` nonce/hash migrations.

### 7. Hand off

1. Document final CSP string per environment.
2. Owners for report triage.
3. Note intentional exceptions with expiry.

## Related Directives

| Directive | Complements `base-uri` by |
| --- | --- |
| `form-action` | Limiting where forms submit |
| `navigate-to` | (where supported) navigation targets |
| `script-src` | Blocking foreign scripts even if URL rewritten |
| `default-src` | Broad fetch fallback |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Policy | `base-uri 'self'` | Omitting `base-uri` entirely |
| Rollout | Report-Only → enforce | Enforce untested on prod Friday |
| Allowlist | Explicit rare hosts | `base-uri *` |
| Delivery | HTTP header | Only meta, easily injected away in some cases |
| XSS | CSP + encoding | CSP alone as XSS “fix” |

## Output Checklist

- [ ] Current CSP and `<base>` usage inventoried
- [ ] `base-uri` directive designed
- [ ] Report-Only validation done if needed
- [ ] Enforced CSP deployed to target envs
- [ ] Functional regression passed
- [ ] Attack lab check documented
- [ ] Reporting/monitoring considered
- [ ] `code-quality-standards` applied to header code

## Rules

- Authorized apps only.
- `base-uri` is mandatory in modern CSP baselines.
- Test before enforce.
- Do not use `*` for `base-uri`.
- CSP complements, not replaces, output encoding.
