---
name: web-dast-functional-walk
description: Browser-driven functional DAST — crawl the app, enumerate every link/form/action, and walk each function one by one (normal input first to learn the flow, then security payloads), including the full auth flow (register → login → session → privileged actions → logout) and IDOR attempts across roles. Use for SPAs and stateful multi-step apps where a blind scanner misses functionality behind JS, wizards, or login. The DRIVER/crawler layer of the operator — it discovers and exercises functionality, then delegates the actual vuln analysis to the focused injection/xss/access-control/auth/business-logic sub-skills. WSTG-INFO/BUSLOGIC, OWASP A01/A03/A04.
---

# Functional DAST walk (browser-driven)

You are the **driver**: open the app the way a real user would, exercise **every** function
one at a time, and at each function do a **functional pass** (normal input, learn the flow)
then a **security pass** (the payloads from the relevant sub-skill). This skill finds the
attack surface a URL-only scan misses (SPA routes, multi-step wizards, actions behind login).
It does **not** re-implement vuln logic — once you reach a form/param/action, hand off to the
matching sub-skill for payloads and confirmation.

`dr(){ docker run --rm detech/toolbox:latest "$@"; }`

## 0. Pick the walking engine (check once, degrade gracefully)
A real functional walk of a JS app needs a **headless browser**. In order of preference:
1. **Headless browser** — if a browser MCP / Playwright skill is available in the session
   (`playwright-pro`, `browser-automation`, `webapp-testing`), use it: it renders JS, clicks,
   fills forms, and gives real DOM + screenshots. This is the intended engine.
2. **Chromium in the toolbox (baked in — preferred default here).** `detech/toolbox:latest`
   ships **Playwright + Chromium** (`PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright`). Drive it with a
   `python3` Playwright script mounted into the container. Verified invocation (Windows/Docker
   Desktop → reach a host app via `host.docker.internal`):
   ```bash
   docker run --rm -v "$SCRATCH:/work" --add-host host.docker.internal:host-gateway \
     --entrypoint python3 detech/toolbox:latest /work/walk.py
   ```
   Launch headless with `chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])`.
   Capture the real API surface with `page.on("request", ...)` filtered to `resource_type in
   ("xhr","fetch")`; harvest SPA routes from rendered `a[href]` (hash routers put them after
   `#/`); do auth/security calls through `ctx.request` so they share the browser session.
   Confirm present: `dr --entrypoint bash detech/toolbox:latest -c 'python3 -c "import playwright"'`.
3. **Scripted HTTP crawl (fallback)** — no browser: use `katana`/`ffuf`-style discovery plus a
   `python3 -c` (stdlib `urllib` + `html.parser`) crawler that extracts `<a href>`, `<form>`
   (action/method/inputs), and JS-embedded routes/`fetch(`/`axios`/`XMLHttpRequest` URLs from
   returned JS bundles. Covers server-rendered surface and API calls; **note in the report**
   that JS-only client behaviour was not fully exercised. Never claim full coverage you did not
   achieve.

State which engine you used — it bounds your coverage claim.

## 1. Map the functionality (crawl)
Build a **function inventory**, not just a URL list. For each discovered thing record:
`{ route/url, kind(link|form|button|xhr|ws), method, params/fields, requires_auth, role }`.
- Enumerate reachable routes: nav links, buttons, client-side router paths, sitemap, robots,
  JS bundles (extract `fetch`/`axios`/route tables), and `katana`/`ffuf` for server paths.
- For every **form**: capture action, method, every field name + type + client validation.
- For every **action/button** that changes state (create/update/delete/transfer/upload/pay).
- Seed with `recon-attack-surface` output; this skill turns that surface into a walkable tree.

## 2. Auth flow — walk it end to end
If credentials or a signup exist, exercise the identity lifecycle as a user would, capturing
session material for reuse:
1. **Register** (if open) → note validation, verification, whether login is immediate.
2. **Login** per role → capture bearer/cookie (see `access-control-idor` §1 for the scripted
   capture). Resolve each role's own user id (JWT payload / `whoami`) to avoid self-access FPs.
3. **Authenticated walk** → re-crawl logged-in; new routes/functions appear here.
4. **Privileged actions** → profile edit, settings, admin panels, order/basket, upload.
5. **Logout** → confirm the session actually dies (token still valid after logout = finding →
   `auth-session-jwt`).
Hand identity/session/reset/MFA flaws to `auth-session-jwt`; login-page injection to injection.

## 3. Per-function loop (do this for EACH inventory item)
```
for each function:
  A. FUNCTIONAL PASS  — submit valid input, observe the normal happy-path response/state.
                        (You must understand the intended behaviour before you can abuse it.)
  B. calibrate        — one benign baseline + one junk/non-existent variant (soft-404/SPA check,
                        see operator §5). A 200 whose body ≈ baseline is NOT real content.
  C. SECURITY PASS    — apply the matching sub-skill's payloads + confirmation marker:
       reflected/stored field, redirect param → client-side-xss-csrf
       any server-processed param            → injection-sqli-cmdi / injection-ssti-xxe
       object id / owner-scoped resource      → access-control-idor  (IDOR across the 2 roles)
       file upload                            → server-side-ssrf-lfi
       url/host/callback field                → server-side-ssrf-lfi (SSRF, interactsh OOB)
       multi-step / price / quantity / coupon → business-logic
       state-changing action w/o token        → client-side-xss-csrf (CSRF)
       API/XHR/GraphQL endpoint               → api-graphql
  D. EVIDENCE         — save exact request+response; screenshot + DOM snapshot if browser engine.
  E. RECORD           — only after validation-gates; else keep as "potential".
```
Be relentless per the operator mindset: **CHECK → TRY → RETRY** with encodings/bypasses before
concluding a function is safe. Log every payload BEFORE reading the response.

## 4. Stored / second-order coverage
A stored payload injected in step 3 may only fire on a **different** page (admin view, a list,
an export, a notification). After a stored-injection attempt, re-visit every page that renders
that data — including higher-privilege views if you hold that role. Track injected markers so
you can attribute a later hit to its source function (this is where the walk beats a scanner).

## 5. Scope & safety while walking (do not skip)
- **Stay on target.** The browser/crawler must not follow off-scope hosts — auth providers,
  CDNs, analytics, payment processors, external redirects. Restrict navigation to the
  authorized host(s); an off-site `Location`/link is noted, never followed as an attack.
- **Non-destructive.** Walk create/read flows freely; for delete/transfer/PUT/DELETE and
  payment, prove the *capability* (e.g. IDOR reaches another user's object) without actually
  destroying data or moving money. Prefer your own test objects.
- **Rate control.** Respect the engagement rate limit; back off on 429/503/5xx (operator §7).
- **Secrets.** Redact captured tokens/passwords in notes and any notification.

## 6. Confirmation discipline (per class)
Confirmation is owned by the sub-skill you delegated to — do not lower its bar because you
arrived via the browser: XSS needs unencoded marker reflection (or a real DOM sink hit); blind
SSRF/RCE need an OOB callback; IDOR needs a second account actually reading/altering the first
account's resource; open redirect is `Location`-header based. Browser execution (e.g. `alert`
actually firing) is *stronger* evidence — capture the screenshot when you get it.

## 7. Output & recording
Deliver two things:
1. **Coverage map** — the function inventory with, per item: walked? engine used, functional
   pass result, which security classes were tested, outcome. Makes "we tested X" auditable and
   exposes what was NOT reached (be honest about JS-only gaps in fallback mode).
2. **Findings** — each confirmed issue in the operator's `findings.md` format (title, severity,
   CVSS 3.1, CWE, OWASP, URL/param, repro/PoC, exact request+response, screenshot if any,
   impact, remediation, confidence, zero-day class). Every finding passes `validation-gates`.
