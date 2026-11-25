---
name: qa-test-history
section: interactive
description: "Tests browser back/forward navigation and direct deep-link loading. Back/forward runs as ONE in-page async probe (SPA history API); deep-link reload stays MCP because it needs a real page navigation."
model: haiku
applyOn: [laptop]
needsSetup: false
viewportSensitive: true
interactive: true
executable: partial
requires: [hasNavigation]
---
## How the orchestrator runs this

🚨 **The back/forward portion is an EXECUTABLE in-page probe — do NOT hand-drive it.** Make **ONE** call:

```
result = browser_evaluate(<the async function in "## Interactive Probe" below>)
```

The probe clicks a visible internal link, drives the SPA history (`history.back()` / `history.forward()`), asserts the URL is restored at each step, and returns `findings[]` for `navLinkDead`, `backButtonBroken`, `forwardButtonBroken`. It works for single-page-app (pushState/hash) routing, which is the common case, and it restores the start URL before returning. It **self-skips** (returns `[]`) when there is no internal link to click. Transcribe each returned finding verbatim.

The **deep-link** check is the HONEST EXCEPTION: it needs a real cross-document navigation (a full `browser_navigate` to `baseUrl + cell.route`), which `browser_evaluate` cannot perform from inside the page. Run it as the short MCP step below.

## Interactive Probe (browser_evaluate, async) — back / forward

```js
async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  const out = [];
  const add = o => out.push(Object.assign({ skill: 'qa-test-history' }, o));
  const vis = el => { if (!el) return false; const r = el.getBoundingClientRect(); const s = getComputedStyle(el); return r.width > 0 && r.height > 0 && s.display !== 'none' && s.visibility !== 'hidden'; };
  const sel = el => { if (!el) return null; if (el.id) return '#' + el.id; const c = (el.className && typeof el.className === 'string') ? el.className.trim().split(/\s+/).slice(0,2).join('.') : ''; return el.tagName.toLowerCase() + (c ? '.' + c : ''); };
  const bb = el => { const r = el.getBoundingClientRect(); return { x: Math.round(r.left), y: Math.round(r.top), w: Math.round(r.width), h: Math.round(r.height) }; };

  const startUrl = location.href;
  const startPath = location.pathname;

  // find a visible internal link
  const link = [...document.querySelectorAll('a[href]')].find(a => {
    if (!vis(a)) return false;
    const href = a.getAttribute('href') || '';
    if (!href.startsWith('/') && !href.startsWith('./')) return false;
    if (href === '#' || href === '/' || href === location.pathname) return false;
    if (/mailto:|tel:|javascript:/.test(href)) return false;
    return true;
  });
  if (!link) return []; // no internal nav available — self-skip

  const href = link.getAttribute('href');

  // CLICK link → expect URL change (SPA route)
  link.click();
  await sleep(800);
  const afterNavUrl = location.href;
  if (afterNavUrl === startUrl) {
    add({ issueType: 'navLinkDead', severity: 'medium', selector: sel(link), bbox: bb(link), description: `Clicking internal link "${href}" produced no URL change`, evidence: { href, startUrl } });
    return out; // nothing more to test if nav didn't happen
  }

  // BACK → expect to return to startUrl
  history.back();
  await sleep(800);
  const afterBackUrl = location.href;
  if (afterBackUrl !== startUrl)
    add({ issueType: 'backButtonBroken', severity: 'medium', selector: sel(link), bbox: bb(link), description: `Browser back navigation did not return to "${startUrl}" — ended up at "${afterBackUrl}"`, evidence: { startUrl, afterBackUrl } });

  // FORWARD → expect to reach afterNavUrl
  history.forward();
  await sleep(800);
  const afterFwdUrl = location.href;
  if (afterFwdUrl !== afterNavUrl)
    add({ issueType: 'forwardButtonBroken', severity: 'low', selector: sel(link), bbox: bb(link), description: `Forward navigation did not reach "${afterNavUrl}" — ended up at "${afterFwdUrl}"`, evidence: { afterNavUrl, afterFwdUrl } });

  // restore to start (best-effort, same-document)
  if (location.pathname !== startPath) { history.back(); await sleep(600); }

  return out;
}
```

> If the click triggers a full (non-SPA) navigation, the probe's later `location.href` reads simply confirm the new document — `backButtonBroken`/`forwardButtonBroken` will not false-fire because `history.back()`/`history.forward()` are honored by the browser. After the probe returns, the orchestrator should ensure the page is back on `cell.route` (the deep-link MCP step below re-navigates anyway).

## MCP steps (for deep-link only)

This single check needs a real navigation, so keep it as MCP (run AFTER the probe):

```
1. browser_navigate({ url: baseUrl + cell.route, waitUntil: 'domcontentloaded', timeout: 10000 })
2. browser_wait_for(time = 600)
3. errorCheck = browser_evaluate(probe.checkDeepLinkError)
4. If errorCheck.hasError → emit deepLinkFails (high)
     description: `Direct navigation to "{cell.route}" shows a 404/error page — deep linking is broken`
```

```js
// probe.checkDeepLinkError
() => {
  const title = (document.title || '').toLowerCase();
  const body = (document.body.innerText || '').slice(0, 500).toLowerCase();
  const hasError = /\b(404|not found|page not found|error|something went wrong|oops)\b/.test(title + ' ' + body);
  const isEmpty = (document.body.innerText || '').trim().length < 50;
  return { hasError: hasError || isEmpty, title: document.title.slice(0, 100) };
}
```

## Issues
| issueType | severity | description |
|---|---|---|
| backButtonBroken | medium | "Browser back navigation did not return to \"{startUrl}\" — ended up at \"{afterBackUrl}\"" |
| forwardButtonBroken | low | "Forward navigation did not reach \"{afterNavUrl}\" — ended up at \"{afterFwdUrl}\"" |
| deepLinkFails | high | "Direct navigation to \"{cell.route}\" shows a 404/error page — deep linking is broken" |
| navLinkDead | medium | "Clicking internal link \"{href}\" produced no URL change" |

## Notes on this conversion
- Back/forward (3 of 4 issueTypes) folded into ONE in-page async probe using the History API (`history.back()` / `history.forward()`) — the common SPA case. The old `findInternalLink` / `cleanupHistory` helper probes are inlined; no `data-argus-*` attribute needed.
- `deepLinkFails` stays MCP-driven (`executable: partial`) because it requires a real cross-document `browser_navigate` reload that a page-context probe cannot perform.
- Restores the start route before returning (best-effort via `history.back()`); the deep-link MCP step re-navigates to `cell.route` regardless, leaving the page clean.
