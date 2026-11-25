---
name: qa-test-auth-flow
section: interactive
description: "Tests login, logout, and protected route redirect. In-page CHECKS (login form present, logout button reachable, protected-route redirect detection, role/session state) run as ONE async probe; real navigation + form submission stay as MCP steps."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
requires: [hasLoginForm, hasLogoutOption]
---
## How the orchestrator runs this (probe + a few MCP steps)

🚨 This skill is **`executable: partial`**. The in-page CHECKS are a single `browser_evaluate` probe; the parts that genuinely need a real browser (navigating to the login route, typing credentials, submitting the form, navigating to a protected route) stay as MCP steps because `browser_evaluate` cannot perform a real cross-page navigation or a credentialed form POST that the SPA router honors.

1. Make ONE probe call to detect the in-page state (is there a login form? is a logout control reachable? is this currently a logged-in or logged-out view? does the page look like a 403/redirect?):
   ```
   state = browser_evaluate(<the async function in "## Interactive Probe" below>)
   ```
   Transcribe any findings it returns verbatim (it self-skips with `[]` on routes that are not auth-related).
2. Then run the **## MCP steps (navigation/login)** below for the live flow, using the selectors/flags the probe tagged.

## Self-skip
The probe self-skips (returns `[]`) unless the route contains `login`, `signin`, or `auth`, OR a login form / logout control is detected. Also skip the live-login MCP steps if no email/password exists in config.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-auth-flow' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0 && getComputedStyle(el).display !== 'none' && getComputedStyle(el).visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  const path = (location.pathname + location.search).toLowerCase();
  const isAuthRoute = /login|sign.?in|auth/.test(path);

  // detect login form
  const emailInput = [...document.querySelectorAll('input[type="email"], input[name="email"], input[name="username"], input[id*="email" i], input[id*="user" i]')].find(vis);
  const pwInput = [...document.querySelectorAll('input[type="password"]')].find(vis);
  const submitBtn = [...document.querySelectorAll('button[type="submit"], input[type="submit"], button:not([type])')].find(vis);
  const hasLoginForm = !!(emailInput && pwInput);

  // detect logout control (for an authenticated view)
  const logoutRe = /\b(log\s*out|sign\s*out|logout|signout)\b/i;
  const logoutBtn = [...document.querySelectorAll('button, a, [role="button"], mat-menu-item, mat-list-item')]
    .find(el => vis(el) && logoutRe.test(el.innerText || el.getAttribute('aria-label') || el.getAttribute('title') || ''));
  const profileBtn = [...document.querySelectorAll('[aria-label*="account" i], [aria-label*="profile" i], [class*="user-menu"] button, [class*="avatar"]')].find(vis);

  // self-skip if this is neither an auth route nor an authenticated view with a login form / logout control
  if (!isAuthRoute && !hasLoginForm && !logoutBtn && !profileBtn) return [];

  // tag controls so the MCP steps can target them deterministically
  if (emailInput) emailInput.setAttribute('data-argus-auth-email', '1');
  if (pwInput) pwInput.setAttribute('data-argus-auth-pw', '1');
  if (submitBtn) submitBtn.setAttribute('data-argus-auth-submit', '1');
  if (logoutBtn) logoutBtn.setAttribute('data-argus-logout', '1');
  else if (profileBtn) profileBtn.setAttribute('data-argus-profile-btn', '1');

  // in-page check: a protected/authenticated view should expose SOME way to log out
  const looksAuthenticated = !isAuthRoute && !hasLoginForm && (document.body.innerText || '').length > 200;
  if (looksAuthenticated && !logoutBtn && !profileBtn)
    add({ issueType: 'logoutNotRedirected', severity: 'medium', selector: 'body', bbox: bb(document.body), uncertain: true, description: 'Authenticated view exposes no logout / account control — users cannot end their session from this page.', evidence: { path } });

  // in-page check: are we already on a 403 / access-denied screen?
  const denied = /403|forbidden|unauthorized|access denied|not authorized/i.test((document.body.innerText || '').slice(0, 600) + ' ' + document.title);

  // emit the MCP plan as a non-finding hint object (orchestrator reads stateForMcp, does NOT ticket it)
  out._stateForMcp = {
    isAuthRoute, hasLoginForm, deniedScreen: denied,
    emailSelector: emailInput ? '[data-argus-auth-email="1"]' : null,
    pwSelector: pwInput ? '[data-argus-auth-pw="1"]' : null,
    submitSelector: submitBtn ? '[data-argus-auth-submit="1"]' : null,
    logoutSelector: logoutBtn ? '[data-argus-logout="1"]' : (profileBtn ? '[data-argus-profile-btn="1"]' : null),
    logoutNeedsMenuExpand: !logoutBtn && !!profileBtn
  };
  return out;
}
```

> The probe attaches a non-ticketed `_stateForMcp` field (selectors + flags) the orchestrator uses to drive the MCP steps. Only objects with an `issueType` become tickets.

## MCP steps (navigation/login)

Run these AFTER the probe, using `state._stateForMcp.*` selectors. These need a real browser; they cannot be done in-page.

**Test 1 — Valid login** (only if `hasLoginForm` and credentials exist in config):
- `browser_navigate({url: baseUrl + loginPath, waitUntil: 'domcontentloaded', timeout: 15000})`
- `browser_wait_for(time=500)` — let Angular change detection settle, then re-run the probe to (re)tag the form
- Fill `emailSelector` and `pwSelector` via `browser_type` or `browser_fill_form`
- `browser_click(submitSelector)`
- `browser_wait_for(time=2000)` — SPA route change (not networkidle, which never resolves)
- `currentUrl = browser_evaluate(() => location.href)`
- If `currentUrl` still contains `loginPath` → **loginFailed (critical)**
- (Optional) repeat with a WRONG password: if it leaves the login page → **badCredentialsAccepted (critical)**; if it stays but shows no `[role="alert"]`/`mat-error` → **noErrorOnBadCredentials (medium)**

**Test 2 — Logout** (only if `logoutSelector` present):
- If `logoutNeedsMenuExpand` → `browser_click('[data-argus-profile-btn="1"]')`, `browser_wait_for(time=400)`, then re-probe to find the revealed logout item
- `browser_click(logoutSelector)`
- `browser_wait_for(time=1500)`
- `currentUrl = browser_evaluate(() => location.href)`
- If URL does NOT contain `login`/`signin` and is not `baseUrl + '/'` → **logoutNotRedirected (medium)**

**Test 3 — Protected route redirect** (JS session-clear, since `page.context().clearCookies()` is MCP-unavailable):
- `browser_evaluate(probe.clearSessionStorage)` — clears localStorage, sessionStorage, and JS-accessible cookies
- `browser_navigate({url: baseUrl + (cell.route.includes('dashboard') ? cell.route : '/dashboard'), waitUntil: 'domcontentloaded'})`
- `browser_wait_for(time=1000)`
- `currentUrl = browser_evaluate(() => location.href)`
- If URL does NOT contain `login`/`signin` → **noProtectedRouteRedirect (high)**

```js
// probe.clearSessionStorage — JS-only session clearing (replaces page.context().clearCookies(), MCP-unavailable)
() => {
  try { localStorage.clear(); } catch (_) {}
  try { sessionStorage.clear(); } catch (_) {}
  try {
    document.cookie.split(';').forEach(c => {
      const name = c.trim().split('=')[0];
      document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    });
  } catch (_) {}
  return { cleared: true, note: 'HttpOnly cookies remain (server-controlled)' };
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| loginFailed | critical | "Login with provided credentials failed — still on {url}" |
| loginError | critical | "Login flow threw an error: {msg}" |
| logoutNotRedirected | medium | "Logout did not redirect to login page — landed on {url}" |
| noProtectedRouteRedirect | high | "Accessing \"{path}\" while logged out did not redirect to login — landed on {url}" |
| badCredentialsAccepted | critical | "Submitting a WRONG password logged the user in (or left the login page) instead of being rejected" |
| noErrorOnBadCredentials | medium | "Wrong password was rejected (stayed on login) but NO error message was shown to the user" |

## Notes on this conversion
- `executable: partial`. The in-page detections (login form present, logout control reachable, already-on-403 screen, authenticated-view-without-logout) are now ONE probe. Real navigation + credentialed submission stay as the MCP steps above because a real cross-page login cannot be performed inside `browser_evaluate`.
- The probe tags every control with `data-argus-*` so the MCP steps target them deterministically (no AI selector guessing). It also self-skips on non-auth, non-authenticated pages.
