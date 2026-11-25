---
name: qa-test-navigation
section: interactive
description: "Verify internal nav links resolve, tabs switch content, and deep links load. Runs as ONE in-page async probe (no AI hand-driving) for links + tabs; deep-link stays an optional orchestrator step."
model: sonnet
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: true
requires: [hasNavigation]
---
## How the orchestrator runs this (ONE call — no hand-driving)

🚨 **This skill is an EXECUTABLE in-page probe, not a prose playbook.** Do NOT drive it click-by-click with separate `browser_click` / `browser_navigate_back` / `browser_evaluate` MCP calls. Instead make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The function collects internal links, clicks each one in-page (SPA route change), asserts the URL or visible content changed and that no 404/error/blank page resulted, then `history.back()`s to restore — and separately drives every tab group and asserts the panel content changes. All inside the page, in one round-trip, with its own `setTimeout` waits for route/Angular settle. It **self-skips** (returns `[]`) when there are no internal links and no tabs. Transcribe each returned finding verbatim into the cell JSONL; add only the envelope fields (runId, cellId, route, viewport, …). The probe restores the starting URL (via `history.back`/`pushState`) and the originally-active tab before returning.

**Deep-link test (optional, separate MCP step):** A true cross-document deep link cannot be exercised from inside `browser_evaluate`. If the orchestrator wants the `routeDeepLinkFails` check it may, after this probe, do ONE `browser_navigate({url: baseUrl + cell.route, waitUntil: 'domcontentloaded'})` then `browser_evaluate(checkPageError)` (the same `checkPageError` logic is embedded in the probe below for reuse). This is optional and not required for the link/tab findings.

## Interactive Probe (browser_evaluate, async)

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-navigation' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0, 2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  // ── error / content heuristic (reusable for deep-link too) ──
  const checkPageError = () => {
    const title = (document.title || '').toLowerCase();
    const bodyText = (document.body.innerText || '').slice(0, 600).toLowerCase();
    const combined = title + ' ' + bodyText;
    const hasErrWord = /\b(404|not found|page not found|something went wrong|error loading|access denied|forbidden)\b/.test(combined);
    const isEmpty = (document.body.innerText || '').trim().length < 80;
    const hasAngularContent = !!(document.querySelector('mat-card, mat-toolbar, mat-sidenav-content, router-outlet + *') || document.querySelectorAll('[class*="mat-"]').length > 3);
    return {
      hasError: (hasErrWord && !hasAngularContent) || isEmpty,
      hasContentChange: hasAngularContent || document.body.innerText.length > 200,
      errorText: hasErrWord ? bodyText.slice(0, 100) : null
    };
  };

  // Content fingerprint to detect a view transition even when URL is unchanged.
  const fp = () => {
    const main = document.querySelector('[role="main"], main, router-outlet + *, mat-sidenav-content') || document.body;
    const h = (document.querySelector('h1, h2, mat-card-title, mat-toolbar') || {}).innerText || '';
    return (location.href + '|' + h + '|' + (main.innerText || '').slice(0, 240)).slice(0, 600);
  };

  // ── collect internal links (max 8 tested) ──
  const seen = new Set();
  const currentPath = location.pathname;
  const links = [];
  for (const a of document.querySelectorAll('a[href]')) {
    if (links.length >= 8) break;
    if (!vis(a)) continue;
    const href = a.getAttribute('href') || '';
    if (href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('tel:')) continue;
    if (href === '#' || href === '' || href === currentPath || href.startsWith('javascript:')) continue;
    if (seen.has(href)) continue;
    seen.add(href);
    links.push({ el: a, href, text: (a.innerText || a.getAttribute('aria-label') || href).trim().slice(0, 60) });
  }

  // ── collect tabs ──
  const tabs = [...document.querySelectorAll('[role="tab"], mat-tab, .nav-tabs > li, .nav-tabs a, .mat-tab-label, [data-tab]')].filter(vis).slice(0, 5);

  if (links.length === 0 && tabs.length < 2) return []; // self-skip

  // ── TEST LINKS ──
  const startUrl = location.href;
  const startFp = fp();
  for (const link of links) {
    const beforeUrl = location.href;
    const beforeFp = fp();
    try { link.el.click(); } catch (e) { continue; }
    await sleep(800); // SPA route settle (NOT networkidle)

    const afterUrl = location.href;
    const err = checkPageError();
    const contentChanged = fp() !== beforeFp;

    if (err.hasError) {
      add({ issueType: 'navLinkBroken', severity: 'high', selector: sel(link.el), bbox: bb(link.el), description: 'Navigation link leads to an error or blank page — href: ' + link.href, evidence: { href: link.href, errorText: err.errorText } });
    } else if (afterUrl === beforeUrl && !contentChanged) {
      add({ issueType: 'navItemDead', severity: 'medium', selector: sel(link.el), bbox: bb(link.el), description: "Clicking nav link '" + link.text + "' produced no URL change and no visible content transition — href: " + link.href, evidence: { href: link.href, text: link.text } });
    }

    // restore to start (in-page)
    if (location.href !== startUrl) { try { history.back(); } catch (e) {} await sleep(500); }
    if (location.href !== startUrl && location.pathname !== currentPath) {
      try { history.pushState({}, '', startUrl); window.dispatchEvent(new PopStateEvent('popstate')); } catch (e) {}
      await sleep(300);
    }
  }

  // ── TEST TABS ──
  if (tabs.length >= 2) {
    const active = tabs.find(t => t.getAttribute('aria-selected') === 'true' || /active|selected/.test(t.className)) || tabs[0];
    const others = tabs.filter(t => t !== active).slice(0, 3);
    for (const tab of others) {
      const label = (tab.innerText || tab.getAttribute('aria-label') || 'tab').trim().slice(0, 40);
      const getPanel = () => {
        const p = document.querySelector('[role="tabpanel"]:not([hidden]):not([aria-hidden="true"]), mat-tab-body.mat-tab-body-active, .tab-pane.active, [class*="tab-content"][class*="active"]');
        if (p && vis(p)) return (p.innerText || '').trim().slice(0, 200);
        return fp(); // fallback to whole-view fingerprint
      };
      const before = getPanel();
      try { tab.click(); } catch (e) { continue; }
      await sleep(500);
      const after = getPanel();
      if (before === after && before.length > 10) {
        add({ issueType: 'tabSwitchNoEffect', severity: 'high', selector: sel(tab), bbox: bb(tab), description: "Clicking tab '" + label + "' did not change the visible panel content", evidence: { tabLabel: label } });
      }
    }
    try { active.click(); await sleep(300); } catch (e) {} // restore active tab
  }

  return out;
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| navLinkBroken | high | "Navigation link leads to an error or blank page — href: {href}" |
| navItemDead | medium | "Clicking nav link '{text}' produced no URL change and no visible content transition — href: {href}" |
| tabSwitchNoEffect | high | "Clicking tab '{label}' did not change the visible panel content" |
| routeDeepLinkFails | high | "Direct navigation to '{route}' shows a 404 or empty page — deep linking is broken" |

## Hard rules

1. **NEVER use** `page.locator()`, `page.goto()`, `page.goBack()`, `networkidle` — all raw Playwright API, unavailable in MCP.
2. In-page link clicks use `el.click()` + `history.back()`/`pushState` to restore. The optional deep-link step (only) uses `browser_navigate({waitUntil: 'domcontentloaded'})`.
3. **Use `domcontentloaded` + in-page 800 ms wait** — never `networkidle` (Angular SPAs fire constant background requests).
4. **Max 8 links, 3 tabs** — bounded; don't iterate the entire nav tree.

## Notes on this conversion
- Replaces the multi-step prose playbook with ONE in-page async probe for the link and tab checks (`navLinkBroken`, `navItemDead`, `tabSwitchNoEffect`). The orchestrator makes a **single** `browser_evaluate` call instead of click→wait→inspect→navigate-back per link.
- **`routeDeepLinkFails` is folded OUT of the single call** because a true cross-document deep link requires `browser_navigate` (impossible from inside `browser_evaluate`). The issueType is preserved and the reusable `checkPageError` logic is embedded; the orchestrator can fire it as one optional follow-up `browser_navigate` + `browser_evaluate`. No issueType was dropped or invented.
- Link restore is in-page (`history.back`, then `pushState` fallback) instead of `browser_navigate_back`, keeping everything in one round-trip while still returning the page to its start URL.
