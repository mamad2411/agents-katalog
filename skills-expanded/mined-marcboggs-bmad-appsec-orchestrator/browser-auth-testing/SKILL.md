---
name: browser-auth-testing
description: "Browser-based authentication testing and interactive web application vulnerability discovery using Playwright MCP. Use when targets require login flows, multi-step form submissions, JavaScript-heavy SPAs, OAuth/SAML browser redirects, CSRF token harvesting, cookie manipulation, session management testing, or any workflow that requires maintaining browser state. Handles: login sequence automation, authenticated scanning, session fixation testing, cookie attribute inspection, localStorage/sessionStorage secrets, DOM-based XSS validation, CSP bypass via browser context, clickjacking frame testing, OAuth redirect interception, MFA flow interaction."
---

## BROWSER-BASED AUTHENTICATION & INTERACTIVE TESTING

> Use Playwright MCP tools when the target requires real browser interaction — SPAs, login flows, OAuth redirects, DOM XSS confirmation, or session state that curl/Burp can't maintain.

### When to Use Playwright (vs Burp/curl)

| Scenario | Use Playwright | Use Burp/curl |
|---|---|---|
| Target is JS SPA (React/Angular/Vue) | ✓ | ✗ |
| Login requires CAPTCHA interaction | ✓ | ✗ |
| Need to maintain session across redirects | ✓ | Either |
| OAuth/SAML browser flow testing | ✓ | ✗ |
| DOM-based XSS confirmation | ✓ | ✗ |
| Cookie/localStorage inspection | ✓ | ✗ |
| Clickjacking proof | ✓ | ✗ |
| Simple API endpoint probing | ✗ | ✓ |
| Request smuggling | ✗ | ✓ |
| Header manipulation (Host, CL/TE) | ✗ | ✓ |

---

### Core Tool Reference (Playwright MCP)

**Navigation:** `browser_navigate`, `browser_navigate_back`, `browser_reload`
**Interaction:** `browser_click`, `browser_type`, `browser_fill_form`, `browser_select_option`, `browser_check`
**State:** `browser_snapshot` (accessibility tree), `browser_wait_for`
**Storage:** `browser_cookie_list`, `browser_cookie_get`, `browser_cookie_set`, `browser_cookie_delete`, `browser_localstorage_list`, `browser_localstorage_get`, `browser_storage_state`, `browser_set_storage_state`
**Network:** `browser_network_requests`, `browser_route` (mock/intercept)
**JS:** `browser_evaluate` (run arbitrary JS in page context)
**Evidence:** `browser_take_screenshot`, `browser_console_messages`
**Tabs:** `browser_tabs` (list/create/switch/close)

---

### Authentication Workflow Pattern

```
1. browser_navigate → login page URL
2. browser_snapshot → identify form element refs (username, password, submit)
3. browser_type → fill username field (ref from snapshot)
4. browser_type → fill password field
5. browser_click → submit button
6. browser_wait_for → text/element confirming authenticated state
7. browser_cookie_list → extract session tokens for analysis
8. browser_storage_state → save auth state to file for reuse across tests
```

**Reuse saved state:** `browser_set_storage_state` → restore previously saved session without re-authenticating.

---

### Testing Patterns

#### Session Management Testing

```
browser_cookie_list
→ For each session cookie, check:
  - Secure flag (must be set for HTTPS targets)
  - HttpOnly flag (missing = XSS can steal session)
  - SameSite attribute (None = CSRF risk)
  - Path scope (overly broad = session shared across apps)
  - Expiry (persistent sessions = risk if device shared)

browser_localstorage_list
→ Look for: JWTs, API keys, PII, refresh tokens, session identifiers
→ localStorage is accessible to ANY JS on the origin (XSS = full compromise)

browser_evaluate → "document.cookie"
→ Compare with browser_cookie_list — difference reveals HttpOnly cookies
```

#### DOM-Based XSS Validation

```
1. browser_navigate → URL with payload in fragment/query:
   https://target.com/page#<img src=x onerror=alert(1)>
   https://target.com/search?q="><script>alert(document.domain)</script>

2. browser_evaluate → "document.querySelector('img[src=x]') !== null"
   or check if script executed via a marker:
   browser_evaluate → "window.__xss_fired"
   (after payload sets window.__xss_fired = true)

3. browser_console_messages → look for execution evidence

4. browser_take_screenshot → visual proof for report
```

#### Clickjacking / UI Redressing

```
1. browser_navigate → attacker-controlled page (or use browser_evaluate to inject)
2. browser_evaluate → inject iframe:
   document.body.innerHTML = '<iframe src="https://target.com/sensitive-action" style="opacity:0.1;position:absolute;top:0;left:0;width:100%;height:100%"></iframe>'
3. browser_take_screenshot → proof that target renders in frame
4. Check X-Frame-Options / CSP frame-ancestors headers via browser_network_requests
```

#### OAuth / SAML Flow Interception

```
1. browser_navigate → OAuth authorize endpoint
2. browser_network_requests → capture full redirect chain
3. Look for:
   - redirect_uri manipulation (open redirect → token theft)
   - Missing state parameter (CSRF on OAuth)
   - Token in URL fragment (leaked via Referer)
4. browser_route → intercept redirect to modify redirect_uri
5. browser_navigate → modified flow, check if token delivered to attacker URI
```

#### CSRF Token Harvesting & Testing

```
1. browser_navigate → page with form
2. browser_snapshot → extract CSRF token value from hidden field
3. browser_cookie_list → check SameSite policy
4. browser_evaluate → attempt cross-origin fetch:
   fetch('https://target.com/api/action', {method:'POST', credentials:'include', body:'...'})
5. If SameSite=None and no CSRF token validation → confirmed CSRF
```

#### MFA Flow Testing

```
1. Complete primary auth via browser_type + browser_click
2. browser_snapshot → identify MFA input field
3. Test: submit empty OTP, single digit, expired code
4. Test: repeat submission (rate limiting?)
5. browser_network_requests → check if MFA response leaks valid code
6. Test: navigate directly to post-MFA page (MFA bypass via direct URL)
```

---

### Evidence Capture Checklist

| What | Tool | Report Use |
|---|---|---|
| Visual proof of vuln | `browser_take_screenshot` | Embed in report |
| Full request chain | `browser_network_requests` | Show redirect/auth flow |
| JS execution proof | `browser_console_messages` | DOM XSS evidence |
| Cookie state | `browser_cookie_list` | Session misconfiguration |
| Saved session | `browser_storage_state` | Reproducibility |

---

### Related Skills & Chains

- **`hunt-xss`** — Use Playwright to confirm DOM XSS that Burp can't see (client-side rendering). Playwright proves execution; Burp proves injection point.
- **`hunt-oauth`** — OAuth browser flows require real redirects. Playwright captures the full chain; use `browser_route` to intercept redirect_uri.
- **`hunt-csrf`** — Harvest tokens via `browser_snapshot`, test SameSite via `browser_cookie_list`, prove exploitability via `browser_evaluate` cross-origin fetch.
- **`hunt-auth-bypass`** — After mapping the auth flow with Playwright, test direct navigation to authenticated pages, session fixation, cookie manipulation.
- **`hunt-mfa-bypass`** — MFA flows are interactive multi-step; Playwright handles the state machine that curl cannot.
- **`hunt-ato`** — Combine Playwright session management (cookie/localStorage theft proof) with the 9 ATO paths.
- **`evidence-hygiene`** — Screenshots from `browser_take_screenshot` must still be redacted (cookies, PII). Apply evidence-hygiene rules before including in report.
