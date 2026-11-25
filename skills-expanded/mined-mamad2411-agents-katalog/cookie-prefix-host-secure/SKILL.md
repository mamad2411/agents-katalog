---
name: cookie-prefix-host-secure
description: >
  Use cookie name prefixes __Host- and __Secure- correctly with Secure, Path, and
  Domain constraints to stop cookie injection from weaker scopes. Use for owned web
  auth and CSRF cookies — pair with cookie-security-flags for full flag matrix;
  CHIPS is cookie-partitioned-chips.
---

# Cookie Prefixes `__Host-` and `__Secure-`

## Scope And Authorization

- **In scope:** apps you own setting cookies over HTTPS.
- **Out of scope:** attacking cookie jar on third-party sites without authorization.
- Breaking Domain/Path incorrectly can log everyone out — stage rollouts.
- Pair with `cookie-security-flags` as the broader skill.

## When To Use

- Hardening session/CSRF cookies against **cookie tossing** / domain-scope injection.
- Setting host-only cookies that must not be shared with subdomains.
- Tokens: `__Host-`, `__Secure-`, cookie prefix, host-only, cookie injection.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full Secure/HttpOnly/SameSite matrix | `cookie-security-flags` |
| Partitioned third-party embeds | `cookie-partitioned-chips` |
| Consent Mode | `cookie-consent-mode-ops` |
| Clear-Site-Data | `clear-site-data-api` |

## Prefix Rules (browsers enforce)

| Prefix | Required | Forbidden |
| --- | --- | --- |
| `__Host-` | `Secure`; `Path=/` | `Domain` attribute (host-only) |
| `__Secure-` | `Secure` | (Domain allowed if needed) |

If requirements fail, browser **rejects** the `Set-Cookie`.

## Workflow

### 1. Confirm cookie roles

1. Session cookie: prefer `__Host-` when single host serves app.
2. CSRF cookie readable by JS: may be `__Host-` + not HttpOnly if double-submit pattern needs it (prefer header tokens when possible).
3. Multi-subdomain SSO cookie: `__Host-` **won’t work** across subdomains — use `__Secure-` + careful Domain **or** redesign to token gateway.

### 2. Inventory current Set-Cookie

```bash
curl -sI -c - https://app.example.com/login | rg -i set-cookie
# Look for Domain=; Path=; Secure; names without prefixes
```

### 3. Apply prefixes

**Session on exact host:**

```http
Set-Cookie: __Host-session=...; Secure; HttpOnly; Path=/; SameSite=Lax
```

**Secure but shared parent domain (avoid if possible):**

```http
Set-Cookie: __Secure-session=...; Secure; HttpOnly; Path=/; Domain=example.com; SameSite=Lax
```

1. Rename is a **hard cut** — plan dual-read during migration or forced re-login.
2. Ensure all code reads new cookie name (`__Host-session` not `session`).

### 4. Server framework examples

```javascript
// Express
res.cookie("__Host-session", token, {
  secure: true,
  httpOnly: true,
  path: "/",
  sameSite: "lax",
  // do NOT set domain for __Host-
});
```

```python
# Starlette/FastAPI style
response.set_cookie(
    key="__Host-session",
    value=token,
    secure=True,
    httponly=True,
    path="/",
    samesite="lax",
)
```

### 5. Verify

1. Login response contains correctly spelled prefix and flags.
2. Intentionally broken cookie (Domain set with `__Host-`) is rejected — confirm app doesn’t set that.
3. Subdomain `evil.example.com` cannot set `__Host-` cookie for `app.example.com` host-only jar rules (document threat).
4. App functions after rename; logout clears `__Host-session`.

### 6. Migrate safely

1. Deploy readers accepting old and new names briefly.
2. Issue only new name; expire old.
3. Monitor auth failure rate.

### 7. Hand off

1. Cookie table: name, prefix, domain, path, flags, owner.
2. Threat note: why `__Host-` chosen (anti cookie injection).
3. Cross-link full flags skill for SameSite edge cases.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Host-only app | `__Host-session` | Bare `session` with `Domain=.example.com` |
| HTTPS | Always Secure | Prefix over HTTP (rejected) |
| Path | `/` for `__Host-` | `__Host-` with `Path=/app` (invalid) |
| Migration | Dual-read plan | Silent rename outage |
| SSO | Conscious Domain design | Forcing `__Host-` across many subdomains |

## Output Checklist

- [ ] Cookie roles and host topology mapped
- [ ] Prefix chosen per cookie (`__Host-` vs `__Secure-`)
- [ ] Set-Cookie meets prefix requirements
- [ ] Application reads new names
- [ ] Migration/re-login plan executed
- [ ] Logout clears prefixed cookies
- [ ] Verification with curl/DevTools done
- [ ] Residual subdomain SSO risks documented

## Rules

- Owned apps only; stage renames.
- Browser rejects invalid prefixed cookies — test explicitly.
- Prefer `__Host-` for single-host auth when possible.
- Prefix skill complements, does not replace, full `cookie-security-flags`.
