---
name: fetch-metadata-isolation
description: >
  Design and enforce Resource Isolation Policies using Fetch Metadata (Sec-Fetch-Site,
  Sec-Fetch-Mode, Sec-Fetch-Dest, Sec-Fetch-User) to block cross-site state-changing
  and sensitive resource loads. Use when implementing reject-cross-site defaults,
  top-level navigation allowlists, isolating cookie-authenticated endpoints, or
  reviewing CSRF and XS-Leak adjacent controls on owned web applications.
---

# Fetch Metadata Isolation

## Scope And Authorization

- **In scope:** web apps you own or are authorized to harden/audit.
- **Out of scope:** bypassing another site’s isolation policies without authorization.
- Roll out in report-only/log mode before hard deny on production.
- Redact session cookies and tokens from policy logs and tickets.
- Pair middleware changes with `code-quality-standards`.

## When To Use

- Building a **Resource Isolation Policy (RIP)** or “reject cross-site by default.”
- Protecting cookie-authenticated JSON/HTML endpoints from cross-site `fetch`/`form` abuse.
- Allowing only safe top-level navigations (`Sec-Fetch-Mode: navigate`, `Sec-Fetch-User: ?1`) where needed.
- Complementing CSRF tokens when browsers send Sec-Fetch-* reliably.
- Differentiating isolation policy design from raw header inventory work.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Header dictionary / Sec-Fetch field meanings deep dive | `fetch-metadata-sec-headers` |
| Classic CSRF tokens only | web CSRF skill / session skills in catalog |
| CSP form-action | `form-action-csp` |
| CORS misconfiguration | CORS primary skill in catalog |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Header | Isolation use |
| --- | --- |
| `Sec-Fetch-Site` | `same-origin` / `same-site` / `cross-site` / `none` |
| `Sec-Fetch-Mode` | `cors` / `no-cors` / `navigate` / `same-origin` / `websocket` |
| `Sec-Fetch-Dest` | `document` / `empty` / `image` / `script` / … |
| `Sec-Fetch-User` | `?1` if user-activated navigation |

| Policy pattern | Typical rule |
| --- | --- |
| State-changing API | Reject if `Sec-Fetch-Site` is `cross-site` (and often `same-site` if strict) |
| Top-level GET document | Allow `navigate` + `document` even if cross-site (link clicks) when product requires |
| Embed isolation | Reject cross-site loads of sensitive `document` in frames if not intended |
| Missing headers | Legacy clients: fail-open log vs fail-closed for browser-only APIs |

## Workflow

### 1. Confirm scope and success criteria

1. List endpoints: cookie session APIs, OAuth callbacks, file downloads, embeddable widgets.
2. Success: cross-site POST to `/api/*` denied; normal same-origin SPA XHR allowed; marketing links to public pages still work if required.
3. Decide missing-header policy (browsers without Sec-Fetch-*).

### 2. Inventory

1. Map routes that trust cookies without CSRF token.
2. Sample live traffic for Sec-Fetch-* distributions (same-origin vs cross-site).
3. Note mobile apps / non-browser API clients that share cookie domains (prefer token auth instead).

```bash
# From access logs or a lab proxy — look for Sec-Fetch-Site values on state-changing routes
# Example nginx log format must include request headers if you log them
```

### 3. Baseline attacks (authorized)

1. Cross-site form POST and `fetch(..., credentials: 'include')` against a lab endpoint.
2. Top-level GET navigation to confirm product still works.
3. Capture before/after status codes.

### 4. Implement isolation middleware

```python
# Illustrative ASGI/WSGI-style check for cookie-authenticated mutating requests
SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}

def isolation_ok(method: str, headers: dict) -> bool:
    site = headers.get("sec-fetch-site", "")
    mode = headers.get("sec-fetch-mode", "")
    dest = headers.get("sec-fetch-dest", "")
    user = headers.get("sec-fetch-user", "")

    # Non-browser or very old browser: policy choice — here require header on HTML form posts
    if not site:
        return method in SAFE_METHODS  # or allow if Authorization bearer present

    if site in ("same-origin", "none"):
        return True

    # Allow user-driven top-level navigations (link open)
    if mode == "navigate" and dest == "document" and method in SAFE_METHODS:
        return True

    # Optional: allow same-site subdomains carefully
    if site == "same-site" and method in SAFE_METHODS:
        return True

    # Default deny cross-site (and uncaught cases)
    return False
```

```javascript
// Express-style
function resourceIsolation(req, res, next) {
  if (isolation_ok(req.method, req.headers)) return next();
  return res.status(403).send("Cross-site request blocked");
}
```

1. Prefer **deny cross-site** on `/api/` and session JSON; keep public static assets unrestricted as needed.
2. Log first (shadow mode): header values + decision without blocking.
3. Combine with `SameSite` cookies; isolation is defense-in-depth, not sole control.
4. Document exceptions (payment webhooks should use signatures, not cookies).

### 5. Verify with evidence

```html
<!-- Attacker page lab: should fail against isolated API -->
<form method="POST" action="https://app.example/api/transfer">
  <input name="amount" value="1" />
</form>
<script>document.forms[0].submit()</script>
```

```bash
# Simulate headers (servers may trust these only from real browsers — still useful in unit tests)
curl -sS -o /dev/null -w "%{http_code}\n" -X POST "https://app.example/api/transfer" \
  -H "Cookie: session=test" \
  -H "Sec-Fetch-Site: cross-site" \
  -H "Sec-Fetch-Mode: no-cors" \
  -H "Sec-Fetch-Dest: empty"
# Expect 403 after enforce
```

1. SPA same-origin fetch still 200.
2. OAuth external redirects still complete (top-level navigate).
3. Embed/widget cases explicitly tested if product needs cross-site.

### 6. Observe and harden

1. Metrics: isolation_block_total by path and Sec-Fetch-Site.
2. Alert on sudden block spikes after deploy (broken legit flows).
3. Review exceptions quarterly; remove temporary fail-open.

### 7. Hand off

1. Publish policy table: path prefix → rule → missing-header behavior.
2. Link CSRF token status; note clients that should migrate to bearer tokens.
3. Apply `code-quality-standards` for middleware.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Default | Cross-site deny on cookie APIs | Only CSRF token on some forms |
| Navigation | Explicit navigate allowlist | Blocking all cross-site GET documents blindly if product needs links |
| Rollout | Shadow → enforce | Hard deny Friday on prod with no metrics |
| Clients | Separate token auth for mobile | Mobile app broken, so disable isolation globally |
| Headers | Trust browser-provided in real browsers; unit-test logic | Trust client-supplied Sec-Fetch in non-browser without care |
| Scope | Policy per path class | One global rule for static + API + webhooks |

## Output Checklist

- [ ] Endpoint classes inventoried (API, document, webhook, embed)
- [ ] Shadow-mode logs reviewed
- [ ] Isolation middleware rules documented
- [ ] Cross-site deny evidenced; same-origin allow evidenced
- [ ] Top-level navigation cases tested
- [ ] Missing-header policy decided
- [ ] Metrics/alerts for blocks
- [ ] Exceptions owner + expiry
- [ ] `code-quality-standards` applied

## Rules

- Owned apps only; authorized assessments only.
- Isolation complements CSRF tokens, Origin checks, and SameSite—do not drop tokens solely because Sec-Fetch exists.
- Webhooks and non-browser clients must not depend on cookie + Sec-Fetch alone.
- Prefer path-scoped policies over one brittle global filter.
- For field-level header reference and CSRF-focused header audits, also use `fetch-metadata-sec-headers`.
