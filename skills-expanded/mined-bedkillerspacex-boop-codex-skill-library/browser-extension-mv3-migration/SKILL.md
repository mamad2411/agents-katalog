---
name: browser-extension-mv3-migration
description: >
  Migrate owned Chrome/Edge extensions from Manifest V2 to Manifest V3: service workers
  replacing background pages, host_permissions, declarativeNetRequest vs blocking webRequest,
  scripting API, content security policy, remotely hosted code bans, and store review readiness.
  Use when MV3 migration, service_worker background, dNR rules, chrome.scripting, or extension
  MV2 deprecation fixes — not for malicious extension development.
---

# Browser Extension MV3 Migration

## Scope And Authorization

- **In scope:** Extensions you own or are authorized to maintain (Chrome, Edge, Chromium derivatives; note Firefox differences).
- **Out of scope:** Shipping spyware, drive-by installs, or bypassing store security for malware.
- Test in sideload/developer mode before store submission.
- Redact extension keys, OAuth client secrets, and user data from bug reports.
- Pair security review with `browser-extension-security`; code quality with `code-quality-standards`.

## When To Use

- Chrome MV2 deprecation forces migration timelines.
- Background page / persistent scripts must become service workers.
- Blocking `webRequest` needs `declarativeNetRequest` (dNR) redesign.
- CSP and “no remote code” rules break current architecture (eval, remote scripts).
- Preparing Chrome Web Store / Edge Add-ons listing updates.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Full extension security assessment | `browser-extension-security` |
| General web XSS/CSP | `xss-cross-site-scripting`, frontend CSP skills |
| Browser storage token risks | `browser-storage-security` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| MV2 pattern | MV3 direction |
| --- | --- |
| `"background": { "scripts": [...], "persistent": true }` | `"background": { "service_worker": "sw.js", "type": "module" }` |
| Blocking `webRequest` | `declarativeNetRequest` (+ feedback APIs where allowed) |
| `chrome.tabs.executeScript` | `chrome.scripting.executeScript` |
| Broad `<all_urls>` | Least `host_permissions` + optional permissions |
| Remote script load | Bundle all JS; no eval/new Function of remote strings |
| DOM in background | Offscreen documents (limited) or move UI to extension pages |

## Workflow

### 1. Confirm scope and success criteria

1. Record browsers/versions supported, store listings, enterprise force-install policy.
2. Success: MV3 manifest loads; all critical user journeys work; permissions minimized; store policy checks pass.
3. Inventory features that **cannot** map 1:1 (arbitrary blocking body modification, long-lived background timers).

### 2. Inventory MV2 surface

```bash
# Repo inventory
ls manifest.json src/background* src/content* rules/
rg -n "webRequest|executeScript|eval\\(|new Function|XMLHttpRequest|persistent" --glob '*.{js,ts,json}'
```

1. List permissions and host permissions actually used at runtime.
2. Map each background event to a service-worker-safe handler (idempotent, re-entrant).
3. Note alarm/storage usage for state that previously lived in memory.

### 3. Baseline behavior

1. Automated tests / manual script of: install, login-with-extension, content script inject, network modify if any, update path.
2. Capture permission warnings users will see (copy for store listing honesty).
3. Snapshot MV2 package size and CSP.

### 4. Manifest and core migrations

**Manifest skeleton (illustrative):**

```json
{
  "manifest_version": 3,
  "name": "Owned Extension",
  "version": "3.0.0",
  "background": {
    "service_worker": "background.js",
    "type": "module"
  },
  "action": { "default_popup": "popup.html" },
  "permissions": ["storage", "scripting", "declarativeNetRequest"],
  "host_permissions": ["https://api.example.com/*"],
  "optional_host_permissions": ["https://*/*"],
  "content_scripts": [{
    "matches": ["https://app.example.com/*"],
    "js": ["content.js"],
    "run_at": "document_idle"
  }],
  "web_accessible_resources": [{
    "resources": ["assets/*"],
    "matches": ["https://app.example.com/*"]
  }],
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'"
  }
}
```

**Service worker rules of thumb:**

1. No `window` / DOM; use `chrome.storage` + alarms for durable state.
2. Register listeners at top level (Chrome may terminate SW).
3. Keep startup under time budget; lazy-import heavy modules carefully.
4. Use `chrome.runtime.onInstalled` / `onStartup` for migration of storage schema.

**Scripting API:**

```js
// MV3
await chrome.scripting.executeScript({
  target: { tabId },
  files: ["inject.js"]
});
```

**declarativeNetRequest:**

```json
// rules.json (static ruleset example)
[{
  "id": 1,
  "priority": 1,
  "action": { "type": "block" },
  "condition": {
    "urlFilter": "||evil-tracker.example^",
    "resourceTypes": ["script"]
  }
}]
```

1. Dynamic rules have quotas — design allow/block lists accordingly.
2. Replace header-modify blocking flows with supported dNR actions only.
3. Document residual product gaps where dNR cannot equal old `webRequestBlocking`.

### 5. Kill remote code and tighten permissions

1. Bundle analytics/config; if remote config needed, fetch **data** JSON and validate schema — do not execute it.
2. Remove `unsafe-eval` expectations; fix template compilers that need eval.
3. Convert broad permissions to optional + runtime `requestPermissions` with UX justification.
4. Review `externally_connectable` and `web_accessible_resources` for XSS bridges (`browser-extension-security`).

### 6. Verify

```bash
# Load unpacked in Chrome → Extensions → Developer mode
# Check service worker “Inspect views” for errors on idle wake
# Automated smoke (Playwright/puppeteer with extension loading where supported)
npm test
```

1. Restart browser; ensure SW rehydrates alarms and rules.
2. Verify content scripts on matched hosts only.
3. Enterprise: test forced-install policy JSON for MV3.
4. Store: privacy practices form matches actual host permissions.

### 7. Hand off

1. Ship migration notes for users (permission warning changes).
2. Monitor crash/SW restart metrics post-release.
3. Keep MV2 branch only until minimum browser support ends.
4. Apply `code-quality-standards` to TS/JS refactors.

## Firefox / other notes

| Topic | Note |
| --- | --- |
| Firefox | Manifest V3 support differs (background scripts vs SW timelines); verify MDN for target ESR |
| Safari | Separate web extension packaging |
| Edge | Chromium MV3 largely aligned; store policies differ |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Background | Event-driven SW + storage | Assuming persistent in-memory globals |
| Network | dNR rulesets with least hosts | Keep blocking webRequest and hope |
| Code | Fully packaged scripts | Load remote `https://cdn/.../plugin.js` |
| Permissions | Optional hosts + rationale | `<all_urls>` “just in case” |
| WAR | Tight matches | `web_accessible_resources` to all sites |
| Testing | Kill SW and re-test flows | Only tested with SW always warm |

## Output Checklist

- [ ] Feature inventory and MV2→MV3 gap list
- [ ] Manifest V3 valid; SW registered
- [ ] webRequest blocking replaced or product gap documented
- [ ] scripting API migration complete
- [ ] No remote code execution paths
- [ ] Permissions minimized / optional where possible
- [ ] CSP and WAR reviewed
- [ ] Cross-browser notes recorded
- [ ] Store/enterprise packaging verified
- [ ] `browser-extension-security` pass + `code-quality-standards`

## Rules

- Owned extensions only; no malware features.
- Design for service worker ephemerality from day one.
- Least host permissions; justify each to users and stores.
- Never execute remote strings as code.
- Route deep threat modeling of extension attack surface to `browser-extension-security`.
