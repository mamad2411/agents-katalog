---
name: qa-test-permissions
section: interactive
description: "Tests role-based access control at the UI level. IN-PAGE checks (session active? role indicator present? dangerous actions unblocked? current module hidden-but-data-empty? captured 4xx with no feedback?) run as ONE async probe; cross-route admin-route probing stays as MCP navigation. Works with the current logged-in user's session."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
cacheVersion: "1.0.0"
requires: [hasLoginForm, hasRoleIndicator, hasRestrictedContent]
---
# qa-test-permissions — Role-Based Access Control Testing

Tests what the current logged-in user can and cannot do. Catches: admin routes accessible to non-admins, action buttons that should be disabled but aren't, missing authorization feedback when access is denied.

**Works with the CURRENT session** — does not switch users or log out. Tests from the perspective of whoever is logged in.

## How the orchestrator runs this (probe + admin-route MCP nav)

🚨 This skill is **`executable: partial`**. Probing whether `/admin`, `/users`, `/settings` etc. are accessible requires real cross-page navigation, which stays as MCP `browser_navigate`. Everything that can be judged on the CURRENT page — session state, role indicator, dangerous-action blocking, silent-empty-module detection, captured-403-without-feedback — is in-page.

1. ONE probe on the current page: `state = browser_evaluate(<the async function in "## Interactive Probe" below>)`. It self-skips (returns `[]`) when no session is active (login/auth page or no logged-in indicators). It may emit `missingRoleIndicator`, `actionWithoutConfirmation`, `restrictedActionNotBlocked`, `moduleDataSilentlyHidden`, and `permissionErrorNoFeedback`. Transcribe findings verbatim.
2. Then run **## MCP steps (admin-route probing)** for the cross-route checks (`adminRouteAccessible`, `unauthorizedNoBoundary`, `sensitiveDataExposed`).

## What it checks (8 issue types)

| issueType | severity | what it catches |
|---|---|---|
| `adminRouteAccessible` | high | Route containing `/admin`, `/settings`, `/users`, `/config`, `/manage` returned content (not a redirect or 403) for the current user |
| `restrictedActionNotBlocked` | high | A button/action that looks like it should be role-restricted (Delete All, Manage Users, System Settings) is clickable and not disabled |
| `unauthorizedNoBoundary` | high | Navigating to a restricted route showed page content instead of a 401/403/redirect-to-login |
| `sensitiveDataExposed` | high | A route the current user should not access showed another user's PII or admin-only data |
| `moduleDataSilentlyHidden` | high | Current user can load a module page but the module is NOT in their nav AND the table shows empty/no-records — permission enforced by hiding data silently instead of blocking access |
| `missingRoleIndicator` | medium | User is logged in but no role/permission indicator (badge, menu item list, profile label) is visible anywhere |
| `actionWithoutConfirmation` | medium | A destructive role-restricted action (e.g., "Delete All Records", "Reset System") is accessible with single click and no confirmation |
| `permissionErrorNoFeedback` | medium | An action was blocked by the server (4xx response) but the UI showed no error message to the user |

## Self-skip conditions

The probe returns `[]` if the current page is a login/auth page or no session is active (`detectAuthState` → `loggedIn:false`).

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-permissions' }, o));
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // ── auth state (self-skip if not logged in) ──
  const loginIndicators = document.querySelector('[class*="user-menu"], [class*="user-profile"], [class*="avatar"], mat-toolbar [aria-label*="user" i], [class*="logout"], [class*="sign-out"], [aria-label*="logout" i], [data-testid*="user"], [class*="user-name"]');
  const loginPage = /\b(login|sign.?in|authenticate)\b/i.test(document.title + location.pathname);
  const bodyTextLower = (document.body.innerText || '').slice(0, 500).toLowerCase();
  const hasLogoutText = /\b(logout|sign\s*out|log\s*out)\b/.test(bodyTextLower);
  const loggedIn = !loginPage && (!!loginIndicators || hasLogoutText);
  if (!loggedIn) return []; // self-skip — no active session
  const userEl = document.querySelector('[class*="user-name"], [class*="username"], [class*="display-name"]');
  const userHint = userEl ? (userEl.innerText || '').trim().slice(0, 60) : null;

  // ── role indicator ──
  let role = null, roleFound = false;
  const roleCandidates = document.querySelectorAll('[class*="role"], [class*="permission"], [class*="user-type"], mat-chip[color="primary"], mat-chip[color="accent"], [data-testid*="role"], [aria-label*="role" i], [class*="badge"][class*="role"]');
  for (const el of roleCandidates) {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const txt = (el.innerText || el.getAttribute('aria-label') || '').trim();
    if (txt.length >= 2 && txt.length <= 50) { role = txt.toLowerCase(); roleFound = true; break; }
  }
  if (!roleFound) {
    const profileArea = document.querySelector('[class*="user-info"], [class*="profile"], mat-toolbar');
    if (profileArea) {
      const m = (profileArea.innerText || '').match(/\b(admin|administrator|super\s*admin|manager|viewer|editor|staff|operator|user|member)\b/i);
      if (m) { role = m[0].toLowerCase(); roleFound = true; }
    }
  }
  if (!roleFound)
    add({ issueType: 'missingRoleIndicator', severity: 'medium', selector: 'body', bbox: bb(document.body), description: 'User is logged in but no role/permission indicator (badge, menu item list, profile label) is visible anywhere.', evidence: { currentUser: userHint } });

  // ── dangerous actions on the current page ──
  const dangerousLabels = /\b(delete all|remove all|reset|purge|clear all|destroy|wipe|manage users|grant|revoke|impersonate|system\s+settings|export all|bulk delete)\b/i;
  let dangerCount = 0;
  for (const btn of document.querySelectorAll('button, [role="button"], a[role="button"]')) {
    const r = btn.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    const label = (btn.innerText || btn.getAttribute('aria-label') || btn.title || '').trim();
    if (!dangerousLabels.test(label)) continue;
    const isDisabled = btn.disabled || btn.getAttribute('aria-disabled') === 'true' || getComputedStyle(btn).pointerEvents === 'none';
    const onclickAttr = btn.getAttribute('onclick') || '';
    const hasConfirm = btn.getAttribute('data-confirm') != null || onclickAttr.includes('confirm');
    if (!isDisabled && !hasConfirm)
      add({ issueType: 'actionWithoutConfirmation', severity: 'medium', selector: 'button[aria-label]', bbox: bb(btn), description: 'A destructive role-restricted action is accessible with a single click and no confirmation.', evidence: { actionLabel: label.slice(0, 80) } });
    if (!isDisabled && (role === 'viewer' || role === 'user' || role === 'member' || role === 'staff'))
      add({ issueType: 'restrictedActionNotBlocked', severity: 'high', selector: 'button[aria-label]', bbox: bb(btn), description: 'A role-restricted action is clickable and not disabled for a non-admin user.', evidence: { actionLabel: label.slice(0, 80), currentRole: role } });
    if (++dangerCount >= 5) break;
  }

  // ── silent-empty-module: page loaded, module absent from nav, table shows empty-state ──
  const navEl = document.querySelector('nav, [role="navigation"], [class*="sidebar"], [class*="nav-menu"], [class*="sidenav"], [class*="side-nav"], [class*="main-nav"], [class*="app-menu"], mat-sidenav');
  const navLabels = navEl ? [...new Set([...navEl.querySelectorAll('a, [role="menuitem"], li, mat-list-item, [class*="nav-item"]')]
    .filter(el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; })
    .map(el => (el.innerText || el.getAttribute('aria-label') || '').trim().toLowerCase())
    .filter(t => t.length >= 2 && t.length <= 60))] : [];

  const path = location.pathname.toLowerCase();
  const segments = path.split('/').filter(s => s && !/^\d+$/.test(s));
  const moduleKeyword = segments[segments.length - 1] || segments[segments.length - 2] || '';
  const hasTable = !!document.querySelector('table, [role="table"], [role="grid"], [class*="data-table"]');
  const allText = document.body.innerText || '';
  const emptyMatch = allText.match(/no\s+records?\s*(found)?|no\s+data|nothing\s+found|empty|0\s+results?|no\s+results?/i);
  const deniedInPage = /403|401|forbidden|unauthorized|access denied|not authorized/i.test(allText.slice(0, 600) + ' ' + document.title);
  if (hasTable && allText.length > 100 && emptyMatch && moduleKeyword && !deniedInPage) {
    const inNav = navLabels.some(l => l.includes(moduleKeyword) || moduleKeyword.includes(l));
    if (!inNav)
      add({ issueType: 'moduleDataSilentlyHidden', severity: 'high', selector: 'body', bbox: bb(document.body), description: `Page "${location.pathname}" loaded without error but "${moduleKeyword}" is not in this user's navigation menu. The table shows "${emptyMatch[0]}" instead of "Access Denied" — permission is enforced by hiding data, not blocking access. Fix: redirect unauthorized users to a 403 page or the dashboard.`, evidence: { currentPath: location.pathname, moduleKeyword, emptyStateText: emptyMatch[0], visibleNavModules: navLabels } });
  }

  // ── captured 4xx with no visible feedback (Angular HttpErrorInterceptors set data attrs) ──
  const errorEls = [...document.querySelectorAll('[data-status="403"], [data-status="401"], [data-http-error]')];
  const hasVisibleError = !!document.querySelector('[role="alert"], mat-error, [class*="error-state"]');
  for (const el of errorEls.slice(0, 5)) {
    const status = el.getAttribute('data-status') || el.getAttribute('data-http-error');
    if (!hasVisibleError)
      add({ issueType: 'permissionErrorNoFeedback', severity: 'medium', selector: 'body', bbox: bb(el), description: 'An action was blocked by the server (4xx response) but the UI showed no error message to the user.', evidence: { url: el.getAttribute('data-url') || location.href, status } });
  }

  out._stateForMcp = { role, userHint };
  return out;
}
```

> The probe attaches a non-ticketed `_stateForMcp` field (`role`, `userHint`) for the MCP admin-route step. Only objects with an `issueType` become tickets.

## MCP steps (admin-route probing)

These need real cross-page navigation. For each candidate admin route derived from baseUrl — `{baseUrl}/admin`, `/users`, `/settings`, `/manage`, `/system`, `/config` (max 4):

1. `browser_navigate({url: candidateRoute, waitUntil: 'domcontentloaded', timeout: 8000})`, `browser_wait_for(time=600)`.
2. `result = browser_evaluate(probe.checkRouteAccessResult)`.
3. If `result.status === 'accessible' && result.hasContent` → emit **adminRouteAccessible (high)** with `evidence:{route, pageTitle:result.pageTitle, contentPreview:result.contentPreview}`. If the route clearly belongs to another user's data, also consider **unauthorizedNoBoundary / sensitiveDataExposed (high)**.
4. `browser_navigate({url: cell.route})`, `browser_wait_for(time=500)` — return to original route.

```js
// probe.checkRouteAccessResult — read-only classifier for the route just navigated to
() => {
  const bodyText = (document.body.innerText || '').slice(0, 500);
  let status = 'accessible';
  if (/403|forbidden|unauthorized|access denied|not authorized/i.test(bodyText + document.title)) status = 'blocked';
  else if (location.pathname.includes('/login') || location.pathname.includes('/auth')) status = 'redirected';
  else if (document.body.innerText.length < 100) status = 'empty';
  return { status, hasContent: document.body.innerText.length > 200, pageTitle: document.title.slice(0, 100), contentPreview: (document.body.innerText || '').slice(0, 200) };
}
```

## Hard rules

1. **Read-only probing** — never submit forms, never modify data during permission testing.
2. **Return to original route** after each admin-route probe.
3. **Sonnet model** — role/access interpretation requires semantic judgment.
4. **Do NOT log out** — the skill operates within the current session only.
5. No `data-argus-*` tagging is left behind — the in-page probe does not tag elements (it reads only), so there is nothing to clean up.

## Notes on this conversion
- `executable: partial`. All current-page RBAC checks (session state, role indicator, dangerous-action blocking, silent-empty-module detection, captured-403-without-feedback) are folded into ONE in-page probe that emits findings directly. The cross-route checks (`adminRouteAccessible` and friends) stay as MCP `browser_navigate` steps because they require real navigation, with a small read-only classifier probe for the landed page.
