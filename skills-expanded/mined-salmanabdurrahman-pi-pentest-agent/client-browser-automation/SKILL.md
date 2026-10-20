---
name: client-browser-automation
description: Safe browser-assisted validation for in-scope authenticated workflows — SPA crawling, DOM inspection, screenshot evidence, and client-side behavior verification with bounded automation.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# Browser automation — client-side validation

Use this skill to automate browser-assisted validation of in-scope web applications. Every automated session must use test-owned accounts, stay within scope boundaries, avoid high-volume crawling, and redact all page content before storing evidence. Browser automation is a means to validate client-side behavior, not a tool for scraping, credential harvesting, or anti-bot bypass.

## Required inputs

- Written scope naming the target URLs, authorized test accounts, allowed automation depth (page count, navigation depth), and explicit permission for authenticated crawling.
- User-owned or project-approved test accounts only. Never automate login with borrowed, shared, or customer credentials.
- Valid authorization cache for the target. Separate explicit permission required for DOM XSS injection, form fuzzing, or file upload automation.
- Known rate limits, crawl-delay expectations, robots.txt policy, and escalation contact.
- Target technology stack: frontend framework (React, Vue, Angular, Svelte, etc.), authentication mechanism, anti-automation controls (CAPTCHA, bot detection), and client-side data storage (localStorage, sessionStorage, IndexedDB).

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy`.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target`.
3. `pentest_agent_check_authorization` before any active probe.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools are useful.
5. `pentest_agent_execute_tool` for execution — never raw shell.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — automation scope and safety baseline

Before launching any browser:

1. Read the target's `robots.txt`. Respect `Disallow` directives unless scope explicitly overrides them. Record crawl-delay if specified.
2. Set a conservative page budget: default 50 pages per session unless scope allows more. Set a navigation depth limit: default 3 levels from entry point.
3. Configure the browser to run headless, disable password saving, disable form autofill, clear cache and storage before each session, and route traffic through a controlled proxy for audit logging.
4. Set a global timeout (default 60 seconds per page load) and a per-session timeout (default 15 minutes).
5. Verify that the browser automation tool (Playwright, Puppeteer, or catalog-equivalent) is available and version-pinned. Never install browser automation tools automatically without approval.

### Phase 2 — authenticated session setup

1. Navigate to the login page. Locate the login form using accessible selectors (label text, test ID attributes, name attributes — never fragile CSS class chains).
2. Submit test account credentials. Wait for navigation or a post-login state indicator (presence of a logout link, dashboard element, or session cookie set).
3. Save the authenticated storage state (cookies + localStorage) to a local session file for reuse. This avoids re-login on every page and reduces target load. Never commit session files; store under `.pi/pentest-agent/` with `.gitignore` protection.
4. Verify login success by requesting a known authenticated-only page. If the page returns a login redirect, the session setup failed — debug with redacted request/response metadata, never log credentials or full cookies.

### Phase 3 — SPA endpoint and route discovery

1. From the authenticated landing page, extract all same-origin links (`<a href>`), JavaScript navigation calls (React Router `<Link to>`, Vue `<router-link to>`, Angular `[routerLink]`), and dynamically loaded route tables from framework-specific bundle artifacts.
2. Navigate to each discovered route in sequence, respecting the crawl budget. For each page:
   - Record the URL, page title, and HTTP status (from response or soft-navigation equivalent).
   - Intercept `fetch` and `XMLHttpRequest` calls triggered by page load. Record: method, URL, request body schema (structure, not values), response status, and response content type.
   - Extract any API endpoint patterns: base URLs, path prefixes, authentication headers, and content-type conventions.
3. Identify admin-only, role-restricted, or hidden routes that return 200 for the test account but should not be accessible. Record these as potential access-control gaps.
4. If the SPA uses code splitting, inspect the route-level chunk URLs and extract chunk contents for additional endpoint references.

### Phase 4 — DOM and client-side storage inspection

1. After each page load, inspect:
   - `localStorage`: keys only, not values. Record key names that suggest sensitive data (`token`, `secret`, `user`, `credit`, `cart`, `order`).
   - `sessionStorage`: same key-only inspection.
   - `IndexedDB`: database names and object store names only, not records.
   - `document.cookie`: cookie names and flags (HttpOnly, Secure, SameSite) only, not values.
2. Identify any client-side data that should not be stored in the browser: passwords, payment tokens, unredacted PII, session tokens in non-HttpOnly cookies, API keys in localStorage.
3. Check for debug or development artifacts: React DevTools global, Vue config devtools hint, Angular `ng.probe`, Redux store exposed on `window`, source maps accessible in production.
4. Inspect the Content Security Policy (CSP) header and compare against inline scripts, eval usage, and external resource loads observed during page execution.

### Phase 5 — screenshot and visual evidence

1. Capture full-page screenshots of key pages: login page, registration page, authenticated landing page, account settings page, admin page (if accessible), and any page where a finding is recorded.
2. Before capturing, redact from the DOM: password fields, API key displays, session tokens, email addresses, phone numbers, and any PII visible in the UI.
3. Capture screenshots at a consistent viewport size (default: 1280×720). Include the URL bar or overlay a URL label on each screenshot.
4. If the page has dynamic content (timelines, real-time updates, countdowns), capture a timestamp and note that content may differ on reload.
5. Store screenshots under `.pi/pentest-agent/` evidence directory. Never include screenshots in reports without redaction review.

### Phase 6 — DOM XSS detection (only when allowed)

When scope explicitly permits DOM XSS injection:

1. For each URL parameter, hash fragment, and `postMessage` listener identified:
   - Inject a benign marker payload (`window.__PENTEST_XSS_MARKER__ = true`).
   - Check whether the marker propagates to `window.__PENTEST_XSS_MARKER__` after page load.
2. If the marker is present, the sink is reachable. Record the source→sink path.
3. Listen for unsanitized `innerHTML`, `document.write`, `eval`, `setTimeout(string)`, and `location` assignments triggered by the payload.
4. Never inject: credential-harvesting payloads, keyloggers, DOM-wiping payloads, auto-redirecting payloads, or payloads that exfiltrate data to external servers.

## Decision points

- **Stop at crawl budget**: when page count or depth limit is reached, summarize discovered endpoints and defer remaining routes.
- **Escalate on exposed sensitive data in client storage**: tokens, secrets, PII in localStorage or non-HttpOnly cookies → high finding.
- **Escalate on admin route accessible**: a route that serves admin content to a non-admin test account → access-control finding.
- **Downgrade when anti-automation blocks**: if CAPTCHA or bot detection prevents crawling, switch to manual analysis notes.
- **Stop if automation triggers security alert**: lockout, IP block, or fraud flag on test account → stop immediately.

## Prohibited behavior

- Crawling beyond the configured page budget or depth limit without explicit re-authorization.
- Bypassing CAPTCHA, bot detection, rate limiting, or WAF controls through evasion techniques.
- Automating login with real user credentials, credential spraying, or brute-force.
- Harvesting or storing full cookie values, tokens, localStorage contents, or IndexedDB records.
- Injecting destructive DOM payloads, auto-redirects, or exfiltration payloads.
- Taking screenshots that contain PII, credentials, tokens, or customer data without redaction.

## Stop conditions

- Crawl budget exhausted → stop, report what was covered.
- Anti-automation controls block further navigation → stop, document the control.
- Test account locked, suspended, or flagged → stop and notify escalation contact.
- PII or credentials visible in DOM, storage, or screenshots → redact immediately, stop if source is real customer data.
- Network error, timeout, or target unreachable → stop, record failure.

## Evidence — session and route log

For each automated session, record:

```text
Session ID: <timestamp>-<target-hash>
Target: <base URL>
Test account: <Account-A>
Pages crawled: <count>
Routes discovered: <count>
API endpoints intercepted: <count>

Per-route log:
  URL: <full URL>
  Title: <page title>
  Status: <HTTP status or soft-nav equivalent>
  API calls: <list of method + path patterns>
  Storage keys: <localStorage | sessionStorage | cookie names>
  Findings: <sensitive data exposure | debug artifacts | admin access | DOM XSS sink>
  Screenshot: <evidence path or "redacted">

Session summary:
  Total unique routes: <N>
  Total unique API endpoints: <M>
  Storage findings: <list>
  Access-control findings: <list>
  DOM findings: <list>
  Screenshots: <N captured, M redacted>
```

Never store: full cookie values, localStorage values, sessionStorage values, IndexedDB records, authentication tokens, password fields, PII, or unredacted page HTML containing customer data.

## Report handoff

When findings are confirmed:
1. `pentest_agent_record_finding` for each finding category: sensitive data in client storage, admin-route exposure, debug artifacts in production, CSP bypass vector, or DOM XSS sink.
2. Reference the session log and screenshot evidence.
3. Recommend: HttpOnly+Secure+SameSite for all session cookies, no sensitive data in web storage, CSP with strict-dynamic or nonce-based script policy, removal of debug/devtools hooks in production builds, source-map exclusion from production deployments, route-level authorization checks server-side (not client-side hiding), and automated client-storage audits in CI.
