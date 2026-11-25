---
name: clear-site-data-api
description: >
  Use the Clear-Site-Data response header to wipe cookies, storage, and cache on logout,
  account switch, or session revoke. Use when implementing thorough client state clearing
  for web apps you own — complements server-side session invalidation; not a substitute
  for HttpOnly cookie logout or CSRF fixes alone.
---

# Clear-Site-Data API

## Scope And Authorization

- **In scope:** first-party web apps you own; authorized security hardening.
- **Out of scope:** forcing clearance on third-party sites; using header to disrupt users maliciously.
- Test in staging: aggressive cache clear can increase origin load after mass logout.
- Redact session identifiers from HAR captures used as evidence.
- Pair with `cookie-security-flags` and `code-quality-standards`.

## When To Use

- Logout / “sign out everywhere” / account switcher must clear **client** residue.
- Shared device / kiosk flows need strong wipe of storage + cache.
- Fixing incomplete logout (tokens left in `localStorage`, Cache Storage, service workers).
- Tokens: Clear-Site-Data, cookies, storage, cache, executionContexts, logout.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Cookie Secure/HttpOnly/SameSite design | `cookie-security-flags` |
| Cookie prefixes `__Host-` / `__Secure-` | `cookie-prefix-host-secure` |
| CHIPS / Partitioned cookies | `cookie-partitioned-chips` |
| Client Hints privacy | `clear-client-hints` |
| Server session store revoke | session / auth skill |
| Service worker update strategy alone | web platform / PWA skill |

## Header Directives

| Directive | Clears | Notes |
| --- | --- | --- |
| `"cookies"` | Cookies for origin (and sometimes related) | Does not replace `Set-Cookie` expiry on response carefully — still invalidate server-side |
| `"storage"` | localStorage, sessionStorage, IndexedDB, Cache Storage, etc. | Broad; may log users out of same-site subapps |
| `"cache"` | HTTP cache for origin | Can spike traffic after deploy/logout storms |
| `"executionContexts"` | Reload browsing contexts | Aggressive UX; use deliberately |
| `"*"` | All supported types | Nuclear option; test thoroughly |

Syntax (response header):

```http
Clear-Site-Data: "cookies", "storage", "cache"
```

## Workflow

### 1. Confirm scope and success criteria

1. App origins (apex + www + API subdomain), auth model (cookie vs bearer in storage).
2. Success: after logout response, client has no usable access token/session material; server rejects old session.
3. Map same-site apps that **share** cookies/storage and would be wiped together.

### 2. Inventory client state

1. Cookies: names, Domain/Path, HttpOnly, lifetime.
2. Web storage keys (tokens, user prefs, offline queues).
3. Cache Storage / service worker caches; shared workers.
4. Third-party embeds that might depend on storage (usually should not hold your session).

```bash
# After implementing, verify header present on logout response:
curl -sD - -o /dev/null -X POST https://app.example.com/logout \
  -H "Cookie: session=REDACTED" | rg -i "clear-site-data|set-cookie"
```

### 3. Baseline incomplete logout

1. Login → DevTools Application panel snapshot.
2. Logout without Clear-Site-Data → note residual keys/tokens.
3. Confirm server session invalidation path exists (must not rely on header alone).

### 4. Implement Clear-Site-Data

**Logout response pattern:**

```http
HTTP/1.1 204 No Content
Clear-Site-Data: "cookies", "storage"
Set-Cookie: session=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; Secure; SameSite=Lax
Cache-Control: no-store
```

**Server sketch (Express-like):**

```javascript
app.post("/logout", auth, async (req, res) => {
  await sessions.revoke(req.sessionId); // server-side first
  res.setHeader("Clear-Site-Data", '"cookies", "storage"');
  res.clearCookie("session", { path: "/", secure: true, httpOnly: true, sameSite: "lax" });
  res.status(204).end();
});
```

1. Prefer explicit directive list over `"*"` until tested.
2. Send only on **authenticated** logout/account-switch responses (not every 200).
3. For multi-subdomain auth, understand cookie Domain scope; you may need logout on each host or careful cookie design.
4. SPA: still clear in-memory stores; header does not reset JS variables already loaded — reload or navigate after logout.
5. Optionally include `"cache"` if sensitive content could remain in HTTP cache (auth’d documents).

### 5. Verify with evidence

1. Automated browser test: login → set localStorage token → logout → assert storage empty and cookie gone.
2. Replay old session cookie → 401.
3. Check BFCache/back button does not resurrect authenticated views (`Cache-Control: no-store` on sensitive pages).
4. Account switch: user A → clear → user B must not see A’s IndexedDB rows.

### 6. Observe and harden

1. Monitor logout error rates and origin traffic after enabling `"cache"`.
2. Support tickets: “prefs wiped” — separate **preference** keys from auth keys if product requires softer clear.
3. Document interaction with service workers (may need `clients.claim` / unregister strategy).

### 7. Hand off

1. Runbook: logout, global revoke, compromised session.
2. Security notes: Clear-Site-Data is **best effort** per browser support — always server-invalidate.
3. Apply `code-quality-standards` to auth handlers.

## Browser / Ops Notes

| Topic | Detail |
| --- | --- |
| Support | Major browsers support common directives; test target UA matrix |
| HTTPS | Typically secure contexts |
| Wildcard | `"*"` expands to all known types for that browser |
| CDN | Ensure edge does not strip Clear-Site-Data on logout paths |
| Reporting | No standard report-only mode — use staging |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Order | Server revoke + header + expire cookie | Header only |
| Scope | Directives matched to auth storage | `"*"` on every navigation |
| SPA | Force navigation/reload after logout | Leave in-memory token |
| Multi-app | Document shared parent domain impact | Surprise wipe of sibling product |
| Evidence | Automated storage assertions | Manual “looks logged out” |

## Output Checklist

- [ ] Origins and auth storage inventory complete
- [ ] Server-side session revoke implemented
- [ ] Clear-Site-Data directives chosen and documented
- [ ] Cookie expiry aligned on logout response
- [ ] Browser tests for storage/cookie/cache residual
- [ ] Account switch / shared device scenario verified
- [ ] CDN preserves header on logout
- [ ] SW/cache interaction reviewed
- [ ] Residual browser support gaps noted

## Rules

- Owned apps only; always pair with server-side invalidation.
- Do not use mass Clear-Site-Data as a substitute for fixing XSS token theft root causes alone — fix XSS too.
- Prefer reversible staged rollout of `"cache"` directive.
- Focus this skill on **Clear-Site-Data**; cookie flag design and CSP remain separate.
