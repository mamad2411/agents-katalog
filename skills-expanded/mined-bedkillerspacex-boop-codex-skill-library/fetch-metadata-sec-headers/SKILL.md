---
name: fetch-metadata-sec-headers
description: >
  Assess and implement Fetch Metadata request headers (Sec-Fetch-Site, Sec-Fetch-Mode,
  Sec-Fetch-Dest, Sec-Fetch-User) for CSRF mitigation and server-side policy checks.
  Use when auditing missing Sec-Fetch validation on cookie-authenticated endpoints,
  documenting header semantics, building reject-cross-site or navigation allowlists,
  or verifying browser-sent metadata on owned apps and authorized assessments.
---

# Fetch Metadata Sec Headers

## Scope And Authorization

- **In scope:** owned applications and authorized security assessments.
- **Out of scope:** attacking third-party sites or forging headers against systems without permission.
- Prefer logging/metrics before hard enforcement in production.
- Redact cookies and tokens from header dumps.
- Pair code changes with `code-quality-standards`.

## When To Use

- Explaining or auditing **Sec-Fetch-*** header presence and values.
- Implementing server checks that read Site/Mode/Dest/User.
- CSRF defense-in-depth alongside tokens and SameSite cookies.
- Differentiating same-origin vs same-site vs cross-site request classes.
- Companion to isolation policy design (`fetch-metadata-isolation`).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full Resource Isolation Policy rollout design | `fetch-metadata-isolation` |
| CSP `form-action` | `form-action-csp` |
| CORS configuration | CORS skill in catalog |
| Session fixation | `session-fixation-management` |
| Implementation quality baseline | `code-quality-standards` |

## Header reference

| Header | Values (common) | Meaning |
| --- | --- | --- |
| `Sec-Fetch-Site` | `same-origin`, `same-site`, `cross-site`, `none` | Relationship between initiator and target |
| `Sec-Fetch-Mode` | `navigate`, `cors`, `no-cors`, `same-origin`, `websocket` | Request mode algorithm |
| `Sec-Fetch-Dest` | `document`, `empty`, `image`, `script`, `worker`, … | Request destination |
| `Sec-Fetch-User` | `?1` or absent | User activation for navigation |

### Site value guide

| Value | Interpretation |
| --- | --- |
| `same-origin` | Scheme/host/port match |
| `same-site` | Schemeful same-site (e.g. subdomains) but not same-origin |
| `cross-site` | Different site |
| `none` | User-driven navigation / no fetch initiator context (e.g. address bar) |

## Workflow

### 1. Confirm scope and success criteria

1. Identify cookie-authenticated routes and whether non-browser clients share them.
2. Success: documented header matrix; dangerous cross-site state changes blocked or ticketed; tests assert header logic.
3. Record browser support assumptions (modern Chromium/Firefox/Safari behavior differs slightly over time—re-verify).

### 2. Inventory headers in real traffic

1. Capture legitimate SPA XHR, form POST, img CSRF-style, and top-level GET.
2. Table the four headers per scenario.
3. Note any reverse proxy stripping `Sec-*` headers (must not strip).

```bash
# Browser DevTools → Network → Request Headers
# Or mitmproxy/Burp on owned lab traffic
curl -sS -D - -o /dev/null "https://app.example/" -H "Cookie: session=lab"
# curl will NOT send Sec-Fetch-* like a browser; use browser or automated browser tests
```

### 3. Baseline CSRF exposure

1. Without tokens, can cross-site POST mutate state? Record proof in lab.
2. Check `SameSite` cookie attribute and Origin/Referer checks if present.
3. List endpoints missing both CSRF token and Sec-Fetch checks.

### 4. Implement header-aware checks

```python
def is_potentially_dangerous_cross_site(method: str, h: dict) -> bool:
    if method in ("GET", "HEAD", "OPTIONS"):
        return False
    site = h.get("sec-fetch-site", "")
    if site in ("cross-site",):
        return True
    # Optional strictness: treat same-site as dangerous for admin APIs
    if site == "same-site" and method in ("POST", "PUT", "PATCH", "DELETE"):
        return True
    return False


def allow_top_level_get(h: dict) -> bool:
    return (
        h.get("sec-fetch-mode") == "navigate"
        and h.get("sec-fetch-dest") == "document"
    )
```

```go
// Go net/http sketch
func secFetchSite(r *http.Request) string {
    return r.Header.Get("Sec-Fetch-Site")
}
```

1. **Do not** treat absence of headers as proof of safety—legacy and non-browser clients omit them.
2. For browser-only cookie sessions: deny dangerous cross-site when headers present; require CSRF token or secondary auth when headers absent.
3. Ensure proxies preserve `Sec-Fetch-*` (some CDNs need explicit allow).

### 5. Verify with evidence

```javascript
// Playwright/Puppeteer idea: real browser sends Sec-Fetch-*
// await page.goto(attacker);
// submit form to victim; expect 403
```

| Scenario | Expect Sec-Fetch-Site | Policy intent |
| --- | --- | --- |
| SPA fetch same origin | `same-origin` | Allow |
| `<form>` from evil.tld | `cross-site` | Deny mutating |
| User opens link | `none` or cross-site + navigate | Allow GET document |
| Subdomain app.a.com → a.com | often `same-site` | Deny if strict admin |

1. Unit-test pure functions with header fixtures.
2. Integration-test with a real browser, not only curl.

### 6. Observe and harden

1. Log (sampled) Site/Mode/Dest on 403s for policy tuning.
2. Alert if proxy suddenly drops all Sec-Fetch headers (all empty).
3. Re-test after browser major versions.

### 7. Hand off

1. Deliver header semantics table + policy code references.
2. Cross-link `fetch-metadata-isolation` for full RIP rollout.
3. Apply `code-quality-standards` for middleware.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Validation | Real browser tests | Only curl with forged Sec-Fetch as “browser proof” |
| CSRF | Tokens + Sec-Fetch + SameSite | Sec-Fetch alone, drop tokens |
| Proxies | Preserve Sec-* | Strip unknown headers globally |
| Missing headers | Explicit policy | Silent allow of everything without headers |
| Documentation | Per-route matrix | “We use Sec-Fetch” with no values |

## Output Checklist

- [ ] Routes and cookie use inventoried
- [ ] Header matrix for major scenarios captured
- [ ] Proxy preservation verified
- [ ] Server checks implemented or findings filed
- [ ] Browser-based cross-site deny evidenced
- [ ] Missing-header behavior documented
- [ ] Monitoring for policy 403s
- [ ] Neighbor skills linked (isolation, CSP form-action)
- [ ] `code-quality-standards` applied if code shipped

## Rules

- Authorized testing only.
- Headers are browser-set forbidden headers—clients should not be able to set them in the browser; still validate logic carefully in tests.
- Prefer defense-in-depth with CSRF tokens.
- Keep this skill focused on Sec-Fetch-* semantics and checks; broader isolation rollout lives in `fetch-metadata-isolation`.
