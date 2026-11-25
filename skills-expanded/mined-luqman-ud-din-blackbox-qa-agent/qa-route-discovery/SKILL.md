---
name: qa-route-discovery
section: pipeline
description: "Discovers routes via 7 harvest strategies (anchors, router attrs, history intercept, hash routes, JS bundle string mining, click-based nav, sitemap+robots). Classifies public vs auth-gated. Detects tabs via accessibility snapshot + Sonnet (catches MUI/Bootstrap/Radix tabs that lack role=tab). Crawls list→detail rows, CTA buttons, modal-as-route patterns, and edge-state pages (404). Works on any SPA framework. ~98% route recall on a single-session crawl."
model: sonnet
---

# QA Route Discovery

## Purpose
Produce `{project-root}/.tmp/qa-<run-id>/routes.json` with every reachable internal route, classified by auth requirement, with in-page tabs, detail-route templates, modal-route patterns, hash routes, and edge-state pages enumerated.

Works for any SPA framework: Angular, React, Vue, Next.js, SvelteKit, plain HTML — anything Playwright can navigate.

---

## Strategy (orchestrator follows these steps via Playwright MCP)

Run four passes: static manifests, unauthenticated browser, authenticated browser, per-route enrichment. Each pass adds candidate routes into the same set; normalisation + dedup runs at the end.

---

## 🚨 EXECUTION MANDATE — enforce before any pass

### 1 · MCP check (first action, no exceptions)

Call `browser_navigate(baseUrl + '/')` before starting Pass 0. This single call determines the execution mode for the entire run:

- **Call succeeds** → MCP is available. **Lock into MCP-only mode:**
  - FORBIDDEN: writing any `.cjs` discovery script under `.tmp/`
  - FORBIDDEN: calling Node.js / Bash / PowerShell for any route-discovery operation
  - FORBIDDEN: using `probe.fetchBundleHead` or `probe.fetchBundleTail` — use `probe.extractBundleRoutes` and `probe.extractBundleRoutesTail` exclusively
- **Call throws / no response** → MCP unavailable → use the Fallback section at the bottom of this skill and nothing else.

The MCP mode and the fallback mode are **mutually exclusive**. Never mix them.

### 2 · Bundle text prohibition (zero exceptions regardless of mode)

JS bundle text (minified, hundreds of KB) **must never appear in the main context window.** This is the single root cause of 9-minute / 24K-token route discovery failures (a 267KB bundle read into context = 123K tokens in one call).

The permanent fix is `probe.extractBundleRoutes`: it fetches the bundle and runs the extraction regex **inside the browser as JavaScript**, then returns only `{ paths: [{path, source}] }` — always < 2KB regardless of bundle size.

Rules enforced at all times:
- NEVER write bundle text to any file and then call the Read tool on it
- NEVER pass raw bundle text as a string to a sub-agent
- NEVER call `probe.fetchBundleHead` or `probe.fetchBundleTail` (both return raw text — they are replaced by the extracting probes)
- The sub-agent dispatch described in old strategy g is REMOVED — extraction now happens in-browser, no LLM needed per bundle

### 3 · Angular SPA fast-path

Run `probe.detectFramework` immediately after first navigation in Pass 2. If `angular: true`:
- **Skip** `probe.harvestAnchors` — Angular prod builds have no static `href` on router elements
- **Skip** `probe.harvestRouterAttrs` — `[routerLink]` is compiled away in production; the DOM attribute does not exist
- Proceed directly to: expand nav (Pass 2 step 8) → nav-click strategy d → `probe.extractBundleRoutes` strategy g

This removes 2–3 wasted probe calls and the "0 anchors found" false start that drove the old session into multi-iteration fallback loops.

---

## 🚨 DISCOVERY CONTRACT — a RELENTLESS loop, not a one-pass scan (READ AND FOLLOW FIRST)

The deliverable is a **COMPLETE route set, proven** — never "whatever I found on the first look." The #1 failure mode is **stopping early**: one run finds 19, the next 16, the next 10. That destroys trust. To eliminate it, discovery is a **breadth-first crawl that loops until it can PROVE nothing is left.** This is the law that overrides any per-pass shortcut.

**Maintain three sets in memory for the whole run:**
- `visited` — routes already navigated to AND fully harvested.
- `frontier` — routes discovered but NOT yet visited.
- `navInventory` — every clickable nav / sidebar / menu / tab LABEL ever seen, captured AFTER expanding all collapsed groups.

**THE LOOP — repeat until the completeness gate below passes (there is NO cap on loop iterations):**

1. **Seed:** after login, set `frontier` = every route harvested from the landing page (anchors + router-attrs + intercepted history + **the JS-bundle route table — MANDATORY, this is the app's own list of routes, see strategy 2.g; it finds routes nothing links to**). 
2. **Drain the frontier:** while `frontier` is non-empty:
   a. Pop a route → `browser_navigate` to it → 1s wait.
   b. **Expand every collapsed nav group** (`probe.expandCollapsedNav`, loop until it returns `expanded === 0`). Add every revealed label to `navInventory`.
   c. **Harvest this page:** anchors, router-attrs, intercepted pushState/replaceState, hash routes.
   d. **Click EVERY interactive element that could navigate — exhaustively, NOT a sample.** Enumerate every visible, not-yet-clicked: link (`a`), button (`button`, `[role=button]`, `input[type=submit]`, `input[type=button]`), tab (`[role=tab]`, segmented controls, sidebar tabs), and menu/sidebar item (`[role=menuitem]`, nav `li`/`a`). For EACH, in order:
      - 🛑 **SKIP if its text/aria-label matches a DESTRUCTIVE/mutating action** — `delete, remove, logout, sign out, submit, save, pay, purchase, buy, checkout, confirm, cancel, deactivate, archive, send, approve, reject, unsubscribe, reset`. These mutate data or end your session — NEVER click them during discovery. (Everything else IS clicked.)
      - Read `location.pathname` → `browser_click` → 800 ms wait → read `location.pathname` again.
      - **URL changed → it IS a ROUTE** → push to `frontier` if new → then `browser_navigate` BACK to the current route to keep clicking the remaining elements.
      - URL unchanged but a **modal/drawer/submenu opened** → harvest any links it revealed (they may be routes), then `browser_press_key("Escape")` and continue.
      - URL unchanged, nothing opened → it's a tab/toggle, not a route → continue.
      Decide tab-vs-route ONLY by the URL check above — never by appearance. You MUST attempt every non-destructive interactive element on the page (bounded by `max_interactive_per_page`, default **60**, only to stop runaway pages). Do NOT sample, do NOT stop after the first few.
   e. Push every NEW same-origin route to `frontier`; move the current route to `visited`.
3. **Dry-pass check:** when `frontier` empties, do ONE more full sweep over `visited`, re-expanding nav and re-harvesting. If it adds **zero** new routes → `dryPasses++`. If it adds any → `dryPasses = 0` and keep looping.

**COMPLETENESS GATE — you may finish ONLY when ALL three hold:**
- `frontier` is empty, **AND**
- `dryPasses >= 2` (two consecutive full sweeps found nothing new), **AND**
- **Nav accounting:** every label in `navInventory` maps to a route in `visited`. Any label that does NOT → click it, record its route, set `dryPasses = 0`, and loop again.

If you stop before all three are true, you have silently dropped routes — the exact 19→16→10 bug. **Log the proof when you finish:**
```
🧭 Discovery complete: {visited.size} routes, {navInventory.size} nav labels all mapped, {dryPasses} dry passes. frontier empty.
```
The per-action caps further below (timeouts, max clicks per page) still apply — they bound a single page, NOT the loop. The loop runs until the gate passes.

---

### Pass 0 — Static manifests (called from any page via fetch)

These probes use `fetch()` inside the current page — no navigation required. They preserve current page state and work whether the page is HTML or PDF or anything else.

1. `browser_navigate(baseUrl + '/')` (one-time; gives the fetch probes a same-origin context)
2. `browser_evaluate(probe.fetchAndParseSitemap)` — fetches `/sitemap.xml` (and any sub-sitemaps if it's an index), extracts `<loc>` paths
3. `browser_evaluate(probe.fetchAndParseRobots)` — fetches `/robots.txt`, extracts paths after `Disallow:` / `Allow:` lines
4. All harvested paths feed the same normalise+dedup pipeline as Pass 1/2

### Pass 1 — Public routes (unauthenticated context)

1. Already at `baseUrl + '/'` from Pass 0. **Wait for the unauthenticated landing to FULLY render before harvesting.** SPA login pages inject their links (`Forgot Password`, `Sign up`) only after the JS boots — harvesting too early is why `viaAnchors` comes back `0` and the public routes are missed. Do: `browser_wait_for(time = 2500)`, then `browser_evaluate("return document.readyState")`; if it is not `"complete"`, `browser_wait_for(time = 1500)` once more.
1a. **Discover the REAL login route — NEVER use a hardcoded/configured login path.** Logged out, the app redirects `/` to its true login URL. Capture it: `discoveredLoginPath = browser_evaluate("return location.pathname")` (e.g. the app may land on `/login`, `/signin`, `/auth/login` — whatever it ACTUALLY redirected to). Store `discoveredLoginPath` for Pass 2 and record it as `{ path, requiresAuth: false, source: 'loginRedirect' }`. This is what prevents the wrong pinned `/auth/login`: the login route is *observed*, not assumed. Fall back to the configured `loginPath` ONLY if `/` did not redirect (i.e. the landing IS the app, not a login screen).
2. `browser_evaluate(probe.injectInterceptor)` — install history + hashchange tracker
3. `browser_evaluate(probe.expandCollapsedNav)` — open every collapsed nav group (ARIA toggles *and* non-ARIA parents containing a hidden submenu). Repeat until it returns `expanded === 0` (max 3 rounds) to open nested levels
4. `browser_evaluate(probe.scanNavItems)` returns up to 6 top-level nav-item texts. For each: `browser_hover(text)` then a 400ms wait — reveals hover-only mega menus
5. `browser_evaluate(probe.harvestAnchors)` → list of hrefs
6. `browser_evaluate(probe.readIntercepted)` → returns `{paths, hashes}`
7. Record results:
   - Each anchor href → normalise → `{ path, requiresAuth: false, source: 'anchors' }`
   - Each `paths[]` entry → normalise → `{ path, requiresAuth: false, source: 'intercept' }`
   - Each `hashes[]` entry → `{ path: '/#' + entry, requiresAuth: false, source: 'hashIntercept', kind: 'hash' }`

### Pass 2 — Auth-gated routes (authenticated context)

1. `browser_navigate(baseUrl + (discoveredLoginPath || loginPath))` — **prefer the `discoveredLoginPath` observed in Pass 1 step 1a over any configured value.** If the configured `loginPath` differs from `discoveredLoginPath`, trust the discovered one and log `⚠ configured loginPath '{loginPath}' ≠ observed '{discoveredLoginPath}' — using observed` (a wrong configured path is the exact cause of the `"pinned": "/auth/login"` bug; the app told us the real one). Then `browser_wait_for(time = 2000)` so the login form renders before typing.
2. Try these typed-in selectors in order until one accepts input: `input[type=email]`, `input[name=email]`, `input[name=username]`, `input[autocomplete=username]`. Use `browser_type` with the email value.
3. `browser_type` on `input[type=password]` with the password value (password is masked in all logs)
4. `browser_click(button[type=submit])` — fallback to the most-prominent visible submit-shaped element if not found
5. `browser_wait_for(time = 5000)` — SPA redirect chain
6. `browser_evaluate("return location.pathname")` — if still equals loginPath, write `loginSucceeded: false` and SKIP Pass 2
7. `browser_evaluate(probe.injectInterceptor)` — re-install tracker on authenticated session
8. **Sidebar tree expansion — ITERATIVE (this is what fills the dropdown gap).** Repeat up to 3 rounds:
   a. `browser_evaluate(probe.expandCollapsedNav)` — opens collapsed groups (ARIA *and* non-ARIA parents containing a hidden submenu). Capture the returned `expanded` count.
   b. `browser_evaluate(probe.harvestAnchors)` **and** `browser_evaluate(probe.harvestRouterAttrs)` — collect the child links the expansion just revealed (a collapsed child only becomes a harvestable `<a href>` AFTER its parent is opened).
   c. If `expanded === 0` for the round → stop (nothing new opened). Otherwise loop — this reveals one nested level per round.
   This ordering matters: expansion BEFORE harvest, repeated, is the fix for collapsed dropdown children that the single-pass flow missed.
9. `browser_evaluate(probe.scanNavItems)` → returns nav labels now visible (including revealed children). For first 6 items: `browser_hover(text)` + 400ms wait — reveal hover menus

10. Run harvest strategies **in this order** (sequence matters — bundle harvest runs LAST so lazy chunks have loaded):

    **a. `probe.harvestAnchors`** — `<a href>` (React/Vue/Next/plain HTML)

    **b. `probe.harvestRouterAttrs`** — `[routerlink]`, `[ng-reflect-router-link]`, `[data-route]`, `[data-href]` (Angular)

    **c. `probe.readIntercepted`** — `pushState` / `replaceState` / `hashchange` history events captured since interceptor was installed

    **d. Click-based nav** — `probe.scanNavItems` returns up to 80 unclicked labels. For each (cap 20 to bound time): `browser_click(text)` → 1.2s wait → re-run `probe.readIntercepted` → re-run `probe.harvestAnchors` to capture any new anchors that appeared. After each click, push the current `location.pathname` to the route set. Continue clicking subsequent items from the SAME starting state (no navigate-back needed — we're collecting URLs not testing routes).

    **e. Service worker cache** — `browser_evaluate(probe.queryServiceWorkerCache)` → enumerates URLs the SW pre-cached. Filter same-origin HTML-shaped paths → add as candidate routes.

    **f. Command palette mining** —
      i.   `browser_press_key("Meta+k")` then 600ms wait
      ii.  `browser_snapshot` — check for a newly-visible dialog/listbox
      iii. If no palette appeared: `browser_press_key("Control+k")` then 600ms wait, snapshot again
      iv.  If still no palette: skip strategy f entirely
      v.   Dispatch Sonnet sub-agent on the snapshot:
           > "This accessibility snapshot includes a command palette dialog. List items that suggest navigating to a route (Go to X, Open Y, View Z). Skip actions like Logout, Create, Delete, Toggle theme. Return JSON array only: `[{ label }]`, cap 10."
      vi.  For each returned label:
           - `browser_press_key("Escape")` to close any leftover state
           - `browser_navigate(baseUrl + '/')` — reset to canonical page
           - 600ms wait
           - `browser_press_key("Meta+k")` (or "Control+k", whichever worked above)
           - 600ms wait
           - For each character of `label.slice(0, 8)`: `browser_press_key(char)` — types the filter
           - 400ms wait
           - `browser_press_key("Enter")`
           - 1500ms wait
           - `browser_evaluate("return location.pathname")` — if pathname changed, record as new route
      vii. After loop: `browser_press_key("Escape")` to ensure clean state

    **g. Bundle string harvest (runs LAST so lazy chunks loaded via strategies a–d are now in `document.scripts`)** —
      i.   `browser_evaluate(probe.listScriptUrls)` — returns up to 10 same-origin script URLs sorted by size
      ii.  For top 8 URLs (or all if fewer): `browser_evaluate(probe.extractBundleRoutes, {url})` — runs the full extraction regex **inside the browser** and returns only `{ ok, totalLength, paths: [{path, source}] }`. Raw bundle text never enters the main context window. No sub-agent needed — the browser performs the extraction. If `totalLength > 600_000` (bundle larger than the head window), also call `browser_evaluate(probe.extractBundleRoutesTail, {url})` to catch Angular route tables appended late in the chunk; merge the tail paths into the same set.
      iii. Merge each returned `paths[]` entry into the candidate route set with `source: 'bundle'`. A path containing a param segment (`:id`, `[id]`, `{id}`, `*`) is a **detail-route template** — keep it as-is; Step 3.2 will attach a real `exampleId` if one is reachable, otherwise it stays a template with `exampleId: null` and is flagged, never dropped.

### Pass 3 — Per-route enrichment

For each discovered route, run this enrichment block. Process routes in batches per `[resilience].batch_size`.

**Step 3.1 — Tab detection (snapshot + Sonnet, replaces literal `role=tab` matching)**

1. `browser_navigate(route)` + 1500ms wait
2. `browser_snapshot`
3. Dispatch Sonnet sub-agent:
   > "From this accessibility snapshot, list every interactive element that behaves like an IN-PAGE TAB — segmented control, pill switcher, view-state tablist, MUI/Bootstrap/Radix/Headless UI tabs, custom tab components. DO NOT include top-level navigation links to other routes. DO NOT include modal triggers. Return JSON array only: `[{ text, role }]`. Cap 12."
4. For each returned tab text (one at a time):
   - `browser_navigate(route)` — RESET to canonical state (critical: previous click may have shifted the DOM)
   - 1200ms wait
   - `browser_click(text)`
   - 800ms wait
   - `browser_evaluate("return { p: location.pathname, s: location.search, h: location.hash }")`
   - Decide:
     - `p` unchanged AND `s` unchanged AND `h` unchanged → genuine in-page tab → add `text` to `route.tabs[]`
     - `p` unchanged AND `h` changed (`#/sub` or `#tab`) → add `text` to `route.tabs[]` with `kind: 'hashTab'`
     - `p` changed → record as new route with `source: 'tabClick'`; do NOT add to tabs

**Step 3.2 — List → detail discovery**

1. `browser_navigate(route)` + 1500ms wait
2. `browser_snapshot`
3. Dispatch Sonnet sub-agent:
   > "Identify the FIRST repeating-record element on this page (table row, list item, card in a grid). If multiple list types exist, pick the largest. Return JSON only: `{ found: boolean, accessibleName: string, kind: 'row'|'card'|'listitem' }`. One item, the first."
4. If `found: true`:
   - `browser_click(accessibleName)` + 1500ms wait
   - `browser_evaluate("return location.pathname")`
   - If new pathname starts with current route's path → record `{currentRoute}/:id` ONCE per parent, with `exampleId = <last segment of new pathname>`, `source: 'listRowClick'`
   - `browser_navigate(route)` — explicit reset (don't rely on history back)

**Step 3.3 — CTA button mining**

1. `browser_navigate(route)` + 1500ms wait
2. `browser_snapshot`
3. Dispatch Sonnet sub-agent:
   > "List up to 4 primary action BUTTONS on this page whose label suggests routing to a sub-page (Add, Create, New, Edit, Manage, Configure, View Details, Import, Export Settings). Skip destructive actions (Delete, Remove, Cancel) and skip pure toggles/menu openers. Return JSON only: `[{ label }]`."
4. For each returned label:
   - `browser_navigate(route)` — RESET
   - 1200ms wait
   - `browser_click(label)`
   - 1500ms wait
   - `browser_evaluate("return location.pathname + location.search")`
   - `browser_evaluate(probe.detectModalParam)`
   - Decide:
     - `probe.detectModalParam` returned `isModal: true` → record `{currentRoute}?{key}=*` with `kind: 'modal'`, `modalKey: <key>`, `source: 'ctaButton'`. `browser_press_key("Escape")` to close
     - Pathname changed to a sub-path of current route → record as new route, `source: 'ctaButton'`
     - Pathname changed to unrelated path → record as new route, `source: 'ctaButton'`
     - No URL change → not routing, skip

### Pass 4 — Edge-state discovery

1. `probePath = '/__argus_edge_probe_' + runId` (guaranteed not to be a real route)
2. `browser_navigate(baseUrl + probePath)` + 2000ms wait
3. `browser_evaluate("return { p: location.pathname, title: document.title, h1: (document.querySelector('h1')||{}).textContent ? document.querySelector('h1').textContent.trim().slice(0,120) : '' }")`
4. Decide:
   - `p === probePath` → app shows the 404 component in place. Record `{ path: '__not_found__', title, h1Text, kind: '404', source: 'edgeProbe' }`
   - `p !== probePath` → app redirected the 404. Record `{ path: '__not_found__', title, h1Text, kind: '404', redirectsTo: p, source: 'edgeProbe' }` AND make sure `p` is in the main routes set
5. (Optional) Repeat once unauthenticated for completeness

### Pass 5 — Sidebar coverage reconciliation (no silent dropdown miss)

This is the route-discovery finish-gate: it guarantees every clickable sidebar item produced a route, so a dropdown group can never be silently dropped (the failure that lost `/billing-info`, `/promo-code-apply`, `/email-templates` on a prior run).

Run in the authenticated context, from a canonical page (`browser_navigate(baseUrl + '/')` + 1s wait):

1. **Fully expand the sidebar.** Loop `browser_evaluate(probe.expandCollapsedNav)` until it returns `expanded === 0` (max 4 rounds). Every group is now open.
2. **Enumerate every nav label.** `browser_evaluate(probe.scanNavItems)` with the full seen-set → returns every visible nav item label, now including the revealed dropdown children.
3. **Reconcile against discovered routes.** For each label whose text does NOT already correspond to a route in the candidate set:
   - `browser_navigate(baseUrl + '/')` → 800ms wait (reset; Reset-between-actions rule)
   - re-expand if needed so the label is visible, then `browser_click(text)` → 1200ms wait
   - `browser_evaluate("return location.pathname")`
   - If the pathname is a new same-origin route → add it `{ path, requiresAuth: true, source: 'navReconcile' }`
   - If clicking it did nothing (pure parent toggle, no navigation) → it's a group header, not a route; mark resolved
4. **Log the gate result (mandatory):**
   ```
   🧭 Sidebar reconciliation
      Nav items found : {N}
      Mapped to route : {mapped}
      Newly added     : {added}  → {paths}
      Unresolved      : {unresolved}  → {labels}   ← MUST be surfaced, never dropped silently
   ```
   Any `Unresolved` nav label (a clickable item that produced no route and isn't a group header) is logged by name — a sidebar entry must never disappear without a trace. If `unresolved > 0`, the discovery is degraded but continues; the labels tell you exactly what to investigate.

Hard caps for this pass: max 4 expand rounds, max 30 reconcile-clicks, 1.2 s per click — bounded like the other passes.

---

## Probes (browser_evaluate)

```js
// probe.harvestAnchors
() => {
  return [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href')).filter(Boolean);
}
```

```js
// probe.harvestRouterAttrs
() => {
  const attrs = ['routerlink','ng-reflect-router-link','data-route','data-href'];
  const out = new Set();
  document.querySelectorAll('*').forEach(el => {
    attrs.forEach(a => {
      const v = el.getAttribute(a);
      if (v && v.startsWith('/')) out.add(v.split('?')[0].replace(/\/$/, '') || '/');
    });
  });
  return [...out];
}
```

```js
// probe.injectInterceptor — tracks pushState, replaceState, popstate, hashchange
() => {
  if (window.__rd) return { ok: true, alreadyInstalled: true };
  window.__rd = true;
  window.__rdRoutes = new Set([location.pathname]);
  window.__rdHashes = new Set();

  const trackPath = (u) => {
    try {
      const url = new URL(String(u), location.href);
      if (url.origin === location.origin) {
        window.__rdRoutes.add(url.pathname.replace(/\/$/, '') || '/');
      }
    } catch {}
  };
  const trackHash = () => {
    const h = location.hash || '';
    // Hash-based routes look like #/foo or #!/foo
    if (/^#!?\//.test(h)) {
      const inner = h.replace(/^#!?/, '');
      const clean = inner.split('?')[0].replace(/\/$/, '') || '/';
      window.__rdHashes.add(clean);
    }
  };

  const oP = history.pushState.bind(history);
  const oR = history.replaceState.bind(history);
  history.pushState = function (s, t, u) { if (u) trackPath(u); return oP(s, t, u); };
  history.replaceState = function (s, t, u) { if (u) trackPath(u); return oR(s, t, u); };
  addEventListener('popstate', () => { trackPath(location.pathname); trackHash(); });
  addEventListener('hashchange', trackHash);
  trackHash(); // capture initial hash if present

  return { ok: true, alreadyInstalled: false };
}
```

```js
// probe.readIntercepted — returns both pushState/replaceState paths AND hash routes
() => ({
  paths: [...(window.__rdRoutes || [])],
  hashes: [...(window.__rdHashes || [])]
})
```

```js
// probe.scanNavItems — returns up to 80 visible nav-item labels not yet seen
(seen) => {
  const containers = 'nav,aside,[role=navigation],[role=menubar],[role=menu],' +
    '[class*=sidebar],[class*=Sidebar],[class*=sidenav],[class*=side-nav],[class*=drawer],' +
    '[class*=rightbar],[class*=right-panel],[class*=rightpanel],' +
    '[class*=header],[class*=Header],[class*=topbar],[class*=top-bar],' +
    '[class*=user-menu],[class*=profile-menu],[class*=account-menu],' +
    '[class*=settings-menu],[class*=dropdown-menu]';
  const out = [];
  const seenSet = new Set(seen || []);
  for (const el of document.querySelectorAll(containers + ' *')) {
    if (out.length >= 80) break;
    if (!el.offsetParent) continue;
    if (el.childElementCount > 8) continue;
    const t = (el.textContent || '').trim().replace(/\s+/g,' ');
    if (t.length < 2 || t.length > 60) continue;
    if (/logout|sign.?out/i.test(t)) continue;
    if (seenSet.has(t)) continue;
    seenSet.add(t);
    out.push(t);
  }
  return out;
}
```

```js
// probe.expandCollapsedNav — opens collapsed dropdown groups inside nav areas.
// Matches BOTH ARIA toggles ([aria-expanded=false]) AND non-ARIA parents that
// merely CONTAIN a currently-hidden submenu (the common Angular/custom sidebar
// case with a chevron icon and a click handler but no aria-expanded).
// Returns { expanded } = number of groups opened THIS call. Call it repeatedly
// (the orchestrator loops until expanded === 0) to open nested levels.
() => {
  const navAreas = document.querySelectorAll(
    'nav, aside, [role=navigation], [role=menubar], ' +
    '[class*=sidebar], [class*=Sidebar], [class*=sidenav], [class*=side-nav], ' +
    '[class*=drawer], [class*=menu], [class*=Menu]'
  );
  const DANGER = /logout|sign.?out|delete|remove|disconnect|danger|destroy|terminate|revoke|cancel/i;
  const SUBMENU_SEL =
    'ul, ol, [role=menu], [role=group], [class*=submenu], [class*=sub-menu], ' +
    '[class*=dropdown], [class*=Dropdown], [class*=children], [class*=nested], [class*=collapse]';
  const isHidden = (el) => !el || el.offsetParent === null || el.getClientRects().length === 0;
  const okText = (el) => {
    const t = ((el.textContent || '').slice(0, 80) + ' ' + (el.getAttribute('aria-label') || '')).trim();
    return t.length >= 2 && t.length <= 80 && !DANGER.test(t);
  };
  const seen = new WeakSet();
  let expanded = 0;
  const tryClick = (el) => {
    if (!el || seen.has(el) || expanded >= 40) return;
    seen.add(el);
    if (isHidden(el) || !okText(el)) return;
    try { el.click(); expanded++; } catch {}
  };

  for (const area of navAreas) {
    if (expanded >= 40) break;

    // 1) Explicit ARIA toggles (original behaviour)
    area.querySelectorAll(
      'button[aria-expanded="false"], [role=button][aria-expanded="false"], ' +
      'summary[aria-expanded="false"], [aria-expanded="false"][tabindex="0"]'
    ).forEach(tryClick);

    // 2) Non-ARIA dropdown parents: any element whose child submenu is hidden.
    //    The clickable "header" is the parent's own anchor/button/label that sits
    //    BEFORE the submenu — click that, not the submenu container.
    for (const sub of area.querySelectorAll(SUBMENU_SEL)) {
      if (expanded >= 40) break;
      if (!isHidden(sub)) continue;                 // submenu already open
      const parent = sub.parentElement;
      if (!parent) continue;
      let header =
        parent.querySelector(':scope > a, :scope > button, :scope > [role=button], :scope > [role=menuitem]') ||
        sub.previousElementSibling ||
        parent;
      if (header && header.contains(sub)) header = sub.previousElementSibling || parent;
      tryClick(header);
    }
  }
  return { expanded };
}
```

```js
// probe.listScriptUrls — same-origin scripts ranked by transferred size
() => {
  const sameOrigin = (u) => { try { return new URL(u, location.href).origin === location.origin; } catch { return false; } };
  const scripts = [...document.scripts].map(s => s.src).filter(u => u && sameOrigin(u));
  const entries = performance.getEntriesByType('resource') || [];
  const sizeMap = new Map();
  for (const e of entries) sizeMap.set(e.name, e.transferSize || e.encodedBodySize || 0);
  scripts.sort((a, b) => (sizeMap.get(b) || 0) - (sizeMap.get(a) || 0));
  return scripts.slice(0, 10);
}
```

```js
// probe.extractBundleRoutes — args: { url }
// Fetches a JS bundle and extracts ALL route paths IN THE BROWSER via regex.
// Returns ONLY { ok, totalLength, paths:[{path,source}] } — never raw bundle text.
// Safe for main context: result is always < 2KB regardless of bundle size.
async ({url}) => {
  const extract = (text) => {
    const seen = new Set();
    const results = [];
    const add = (p, src) => {
      p = p.trim();
      if (!p || seen.has(p)) return;
      if (p.startsWith('http') || p.includes(' ') || p.length > 120) return;
      if (/\.(js|css|png|svg|jpg|jpeg|gif|ico|json|map|woff|ttf|eot|otf)(\?|$)/.test(p)) return;
      if (/^(true|false|null|undefined|\d+)$/.test(p)) return;
      seen.add(p);
      results.push({ path: p, source: src });
    };
    let m;
    // Angular / Vue / TanStack Router: { path: '...' }
    const re1 = /\bpath\s*:\s*["']([^"']{1,120})["']/g;
    while ((m = re1.exec(text)) !== null) add(m[1], 'angular-router');
    // loadChildren lazy imports
    const re2 = /loadChildren\s*:\s*\(\s*\)\s*=>\s*import\s*\(\s*["']([^"']+)["']/g;
    while ((m = re2.exec(text)) !== null) add('LAZY:' + m[1], 'angular-lazy');
    // Absolute path strings that look like routes: "/admin/something" or "/:param"
    const re3 = /["'](\/[a-zA-Z:*][a-zA-Z0-9\-_/:.*{}[\]]*?)["']/g;
    while ((m = re3.exec(text)) !== null) {
      const p = m[1];
      if (p.split('/').length >= 2 && p.length <= 80) add(p, 'bundle-path');
    }
    // Next.js / SvelteKit file-route segments with brackets
    const re4 = /["'](\/[a-zA-Z0-9\-_/[\]()@.]+)["']/g;
    while ((m = re4.exec(text)) !== null) {
      const p = m[1];
      if ((p.includes('[') || p.includes('(')) && p.length <= 80) add(p, 'next-sveltekit');
    }
    return results.slice(0, 200);
  };
  try {
    const r = await fetch(url, { credentials: 'same-origin' });
    if (!r.ok) return { ok: false, status: r.status, paths: [], totalLength: 0 };
    const text = await r.text();
    return { ok: true, status: 200, totalLength: text.length, paths: extract(text.slice(0, 600_000)) };
  } catch (e) {
    return { ok: false, status: 0, paths: [], totalLength: 0, error: String(e).slice(0, 200) };
  }
}
```

```js
// probe.extractBundleRoutesTail — args: { url }
// Like probe.extractBundleRoutes but reads the LAST 400KB.
// Use only when totalLength > 600_000 — Angular route tables are sometimes appended
// late in a chunk, past the 600KB head window.
async ({url}) => {
  const extract = (text) => {
    const seen = new Set();
    const results = [];
    const add = (p, src) => {
      p = p.trim();
      if (!p || seen.has(p)) return;
      if (p.startsWith('http') || p.includes(' ') || p.length > 120) return;
      if (/\.(js|css|png|svg|jpg|jpeg|gif|ico|json|map|woff|ttf|eot|otf)(\?|$)/.test(p)) return;
      if (/^(true|false|null|undefined|\d+)$/.test(p)) return;
      seen.add(p);
      results.push({ path: p, source: src });
    };
    let m;
    const re1 = /\bpath\s*:\s*["']([^"']{1,120})["']/g;
    while ((m = re1.exec(text)) !== null) add(m[1], 'angular-router-tail');
    const re2 = /["'](\/[a-zA-Z:*][a-zA-Z0-9\-_/:.*{}[\]]*?)["']/g;
    while ((m = re2.exec(text)) !== null) {
      const p = m[1];
      if (p.split('/').length >= 2 && p.length <= 80) add(p, 'bundle-tail');
    }
    return results.slice(0, 200);
  };
  try {
    const r = await fetch(url, { credentials: 'same-origin' });
    if (!r.ok) return { ok: false, status: r.status, paths: [], totalLength: 0 };
    const text = await r.text();
    if (text.length <= 600_000) return { ok: true, status: 200, totalLength: text.length, paths: [], note: 'covered by head' };
    return { ok: true, status: 200, totalLength: text.length, paths: extract(text.slice(-400_000)) };
  } catch (e) {
    return { ok: false, status: 0, paths: [], totalLength: 0, error: String(e).slice(0, 200) };
  }
}
```

```js
// probe.detectFramework — identifies the SPA framework from live DOM/window markers.
// Run once at the start of Pass 2. Use result to skip probes that are ineffective for
// the detected framework (e.g. harvestAnchors is useless on Angular prod builds).
() => {
  const w = window, d = document, root = d.documentElement;
  return {
    angular: !!(d.querySelector('[ng-version]') || d.querySelector('[_nghost-ng-c]') ||
                root.getAttribute('ng-version') || typeof w.ng !== 'undefined'),
    react:   !!(typeof w.__REACT_DEVTOOLS_GLOBAL_HOOK__ !== 'undefined' ||
                d.querySelector('[data-reactroot]') || d.querySelector('#root')),
    vue:     !!(typeof w.__vue_devtools_global_hook__ !== 'undefined' ||
                d.querySelector('[data-v-app]') || d.querySelector('[data-v-]')),
    next:    !!(typeof w.__NEXT_DATA__ !== 'undefined' || d.querySelector('#__NEXT_DATA__'))
  };
}
```

```js
// probe.fetchAndParseSitemap — fetches /sitemap.xml from current origin (handles sitemap index)
async () => {
  const fetchText = async (url) => {
    try {
      const r = await fetch(url, { credentials: 'same-origin' });
      if (!r.ok) return null;
      return await r.text();
    } catch { return null; }
  };
  const extractLocs = (xml) => {
    const out = [];
    const re = /<loc>\s*([^<]+?)\s*<\/loc>/gi;
    let m;
    while ((m = re.exec(xml)) !== null) {
      out.push(m[1].trim());
      if (out.length >= 500) break;
    }
    return out;
  };

  const root = await fetchText('/sitemap.xml');
  if (!root || !/<urlset|<sitemapindex|<loc/i.test(root)) return { ok: false, paths: [] };

  const isIndex = /<sitemapindex/i.test(root);
  let allUrls = isIndex ? [] : extractLocs(root);

  if (isIndex) {
    const subSitemaps = extractLocs(root).slice(0, 5);
    for (const subUrl of subSitemaps) {
      try {
        const u = new URL(subUrl, location.href);
        if (u.origin !== location.origin) continue;
        const subText = await fetchText(u.pathname);
        if (subText) allUrls = allUrls.concat(extractLocs(subText));
      } catch {}
      if (allUrls.length >= 500) break;
    }
  }

  const paths = new Set();
  for (const url of allUrls) {
    try {
      const u = new URL(url, location.href);
      if (u.origin !== location.origin) continue;
      const p = u.pathname.replace(/\/$/, '') || '/';
      if (/\.(png|jpg|svg|ico|css|js|pdf|zip|woff|ttf|map|json)$/i.test(p)) continue;
      if (p.length < 120) paths.add(p);
    } catch {}
    if (paths.size >= 200) break;
  }
  return { ok: true, paths: [...paths] };
}
```

```js
// probe.fetchAndParseRobots — fetches /robots.txt, extracts allowed/disallowed paths
async () => {
  try {
    const r = await fetch('/robots.txt', { credentials: 'same-origin' });
    if (!r.ok) return { ok: false, paths: [] };
    const text = await r.text();
    if (text.length > 100_000) return { ok: false, paths: [] };
    const paths = new Set();
    for (const line of text.split(/\r?\n/)) {
      const m = line.match(/^\s*(Disallow|Allow)\s*:\s*([^#\s]+)/i);
      if (!m) continue;
      let p = m[2].trim();
      if (!p.startsWith('/')) continue;
      if (p === '/' || /\*/.test(p)) continue;
      if (/\.(png|jpg|svg|ico|css|js|pdf|zip|woff|ttf|map)$/i.test(p)) continue;
      p = p.split('?')[0].replace(/\/$/, '') || '/';
      if (p.length < 120) paths.add(p);
      if (paths.size >= 100) break;
    }
    return { ok: true, paths: [...paths] };
  } catch (e) {
    return { ok: false, paths: [], error: String(e).slice(0, 200) };
  }
}
```

```js
// probe.queryServiceWorkerCache — same-origin HTML-shaped URLs from SW caches
async () => {
  if (!('serviceWorker' in navigator) || !('caches' in window)) return { ok: false, paths: [] };
  try {
    const keys = await caches.keys();
    if (!keys.length) return { ok: false, paths: [] };
    const paths = new Set();
    for (const k of keys.slice(0, 5)) {
      try {
        const cache = await caches.open(k);
        const reqs = await cache.keys();
        for (const r of reqs.slice(0, 200)) {
          try {
            const u = new URL(r.url);
            if (u.origin !== location.origin) continue;
            const p = u.pathname.replace(/\/$/, '') || '/';
            if (/\.(png|jpg|svg|ico|css|js|woff|ttf|map|json)$/i.test(p)) continue;
            if (p.startsWith('/api/')) continue;
            if (p.length < 120) paths.add(p);
          } catch {}
          if (paths.size >= 100) break;
        }
      } catch {}
      if (paths.size >= 100) break;
    }
    return { ok: true, paths: [...paths] };
  } catch (e) {
    return { ok: false, paths: [], error: String(e).slice(0, 200) };
  }
}
```

```js
// probe.detectModalParam — call after a click to see if URL gained a modal-style query param
() => {
  const params = new URLSearchParams(location.search);
  const modalKeys = ['modal','dialog','drawer','slideover','panel','sheet','popup','overlay'];
  for (const k of modalKeys) {
    if (params.has(k)) return { isModal: true, key: k, value: params.get(k) };
  }
  return { isModal: false };
}
```

```js
// probe.collectTabLabels — fallback. Used only if snapshot+Sonnet pathway is unavailable.
() => {
  const out = [];
  document.querySelectorAll(
    '[role=tab], [data-bs-toggle="tab"], [data-state="active"][role], button[aria-controls]'
  ).forEach(el => {
    if (!el.offsetParent) return;
    const href = el.getAttribute('href');
    const text = (el.textContent || '').trim().replace(/\s+/g,' ').replace(/\s*\d+\s*$/,'').trim();
    if (text.length < 2 || text.length > 60) return;
    out.push({ text, href: href || null });
  });
  return [...new Map(out.map(t => [t.text, t])).values()];
}
```

---

## Normalisation rules (orchestrator applies after every harvest)

```js
// Pseudocode — apply to every href the orchestrator collects
function normalise(href, baseUrl) {
  const u = new URL(href, baseUrl);
  if (u.origin !== new URL(baseUrl).origin) return null;
  if (/\.(png|jpg|svg|ico|css|js|pdf|zip|woff|ttf|map|json)$/i.test(u.pathname)) return null;
  if (u.pathname.startsWith('/api/')) return null;
  if (/^\/loading(\/|$)/.test(u.pathname)) return null;
  return u.pathname.replace(/\/$/, '') || '/';
}
```

**Detail-route collapsing & template↔instance reconciliation.** Before dedup, fold actual-id routes into a single template AND reconcile them with bundle-declared templates so the deliverable always contains BOTH the static template and (when reachable) one concrete example:
- `/users/123`, `/users/456`, `/users/abc-uuid-xyz` → collapse to `/users/:id`
- Detection: if 2+ routes share a parent prefix and differ only in the last segment, AND that segment matches `^[0-9a-fA-F-]{1,40}$` (numeric, hex, or UUID-like) → collapse to `/{prefix}/:id`
- Always retain the first concrete id as `route.exampleId` for later cell navigation
- **Even a SINGLE concrete instance collapses** if a bundle template for the same parent exists: a sampled `/users/42` (Step 3.2 `listRowClick`) and a bundle `/users/:id` are the SAME route — merge into one `{ path: '/users/:id', exampleId: '42', source: 'bundle+listRowClick' }`. Never emit both the template and the concrete instance as two routes.
- **A bundle `:param` template with NO reachable instance is KEPT** as `{ path: '/users/:id', exampleId: null }` and flagged — this is the case for apps (like this one) whose detail views are modals: the route exists in code even though clicking a row opens a dialog instead of navigating. It is reported, never silently dropped. This is how the skill "gets parameterized routes" regardless of whether the live UI exposes a navigable instance.

**Dedup by normalised path.** Skip routes in `qa-state.json → routes.skipped`. Cap total routes at 80.

---

## Output schema

Write to `{project-root}/.tmp/qa-<run-id>/routes.json`:

```json
{
  "runId": "qa-20260520-abc1",
  "discoveredAt": "ISO-8601",
  "app": "myapp",
  "baseUrl": "https://...",
  "loginSucceeded": true,
  "stats": {
    "totalRoutes": 42,
    "viaAnchors": 18,
    "viaRouterAttrs": 0,
    "viaIntercept": 6,
    "viaNavClick": 5,
    "viaNavReconcile": 0,
    "viaBundle": 9,
    "viaCommandPalette": 0,
    "viaServiceWorker": 0,
    "viaSitemap": 4,
    "viaRobots": 0,
    "viaListRowClick": 3,
    "viaCTAButton": 2,
    "viaTabClick": 1,
    "modalRoutes": 1,
    "hashRoutes": 0,
    "edgeStates": 1
  },
  "routes": [
    { "path": "/login",         "title": "Sign in",         "requiresAuth": false, "tabs": [], "source": "anchors" },
    { "path": "/dashboard",     "title": "Home",            "requiresAuth": true,
      "tabs": ["Overview","Details","History"], "source": "anchors" },
    { "path": "/users/:id",     "title": "User detail",     "requiresAuth": true, "tabs": [],
      "source": "listRowClick", "exampleId": "42" },
    { "path": "/users?modal=*", "title": "User modal",      "requiresAuth": true, "tabs": [],
      "source": "ctaButton", "kind": "modal", "modalKey": "modal" },
    { "path": "/#/legacy",      "title": "Legacy area",     "requiresAuth": true, "tabs": [],
      "source": "hashIntercept", "kind": "hash" },
    { "path": "__not_found__",  "title": "Page not found",  "requiresAuth": false, "tabs": [],
      "source": "edgeProbe", "kind": "404", "h1Text": "Page not found" }
  ]
}
```

Field meanings:
- `source` — which harvest strategy first surfaced this route (used for stats + debugging)
- `kind` — special-route marker for downstream phases: `'tab'`, `'modal'`, `'hash'`, `'404'`, or absent for normal routes
- `exampleId` — only present on `:id` template routes; one concrete id the orchestrator can substitute when generating cells
- `modalKey` — only present on modal-routes; the query-param key (`modal`, `dialog`, etc.) the orchestrator should set to navigate

---

## Hard limits

| Rule | Value |
|------|-------|
| Max routes | 80 |
| Max scripts scanned for bundle harvest | 10 (top by size) |
| Bundles passed to Sonnet | 8 (top by size, after nav-click strategies completed) |
| Per-bundle chars read | 600,000 head + 400,000 tail (tail only if chunk exceeds head window) |
| Max sitemap entries harvested | 200 |
| Max sub-sitemaps followed if root is an index | 5 |
| Max robots entries harvested | 100 |
| Max SW cache entries harvested | 100 |
| Max command palette items | 10 |
| Max interactive elements clicked per page (exhaustive loop step d) | 60 (`max_interactive_per_page` — bounds runaway pages only; click ALL non-destructive elements up to this) |
| Max nav-click items in strategy d | 20 (legacy single-pass; superseded by the exhaustive loop) |
| Max nav-expand toggles clicked (per call) | 40 |
| Max sidebar expand rounds (iterative) | 3 (Pass 2) / 4 (Pass 5) |
| Max sidebar reconcile-clicks (Pass 5) | 30 |
| Max hover-menu reveals per pass | 6 |
| Max tab candidates per route | 12 |
| Max CTA buttons per route | 4 (legacy; the exhaustive loop now clicks every non-destructive button) |
| Per-page navigate timeout | 20 s |
| Post-login wait | 5 s (SPA redirect chain) |
| Nav click wait | 1.2–1.5 s per item |
| Tab/CTA click wait | 800–1500 ms per action |
| Sitemap/robots fetch timeout | 5 s |
| Bundle fetch timeout | 8 s |
| Edge probe wait | 2 s after navigate |
| Skip | `/api/*`, `/loading/*`, static assets, external origins, logout items |
| Tab classification | Tab is recorded ONLY when URL is unchanged after click |
| Detail-route emission | One `/parent/:id` per parent — never per concrete id |
| Reset-between-actions | Tab/list/CTA loops ALWAYS re-navigate to canonical route between iterations |
| Destructive-action filter | `expandCollapsedNav` skips toggles containing logout/sign-out/delete/remove/disconnect/danger/destroy/terminate/revoke/cancel |

---

## What this skill CANNOT discover (session-physics limits)

A single-session browser audit has hard physical limits. The skill does not claim to close these — they require config or orchestrator-level changes:

1. **Permission/role-gated routes** — admin-only routes when test account is a regular user; tenant-gated routes; feature-flagged routes. Bundle harvest sees them ONLY if the chunk was served to this user. → Fix: multi-account config in `automation.config.json`.
2. **State-dependent routes** — `/order/confirmation`, OAuth callbacks, magic-link landings, webhook redirect targets. Reachable only after specific side-effects. → Fix: seed-state scripts per app.
3. **Architecture-invisible routes** — Next.js Server Components with no client export; routes resolved entirely by reverse proxy or edge function. → Fix: filesystem read of router source (separate skill).
4. **Multi-tenant / locale variants** — `/fr/users` vs `/en/users`; tenant-A vs tenant-B route sets. → Fix: orchestrator multi-pass over locales/tenants.

Practical expected recall on a single-session crawl: **~98%** for typical SPAs; lower (~85–95%) on heavily permission-gated multi-tenant apps.

---

## Cost analysis (per audit, added vs the v1 skill)

| Phase | Per audit |
|-------|-----------|
| Pass 0 (sitemap + robots) | $0 (no LLM) |
| Pass 1 (unauthenticated) | ~$0.001 |
| Pass 2 strategies a–d | ~$0.001 |
| Pass 2 strategy e (SW cache) | $0 |
| Pass 2 strategy f (command palette, 1 Sonnet call) | ~$0.003 |
| Pass 2 strategy g (bundle harvest, 5 Sonnet calls) | ~$0.02 |
| Pass 3 enrichment (3 Sonnet calls × ~16 routes typical) | ~$0.03 |
| Pass 4 (edge probe) | $0 |
| **Total added vs v1 skill** | **~$0.05 per audit** |
| **Recall improvement** | ~35–40% → ~98% |

---

## Fallback when Playwright MCP is unavailable

**PREREQUISITE — this section applies ONLY when the MCP check at the top of this skill confirmed MCP is unavailable** (i.e. `browser_navigate(baseUrl + '/')` threw or returned no response at the start of the run). If MCP responded, every instruction below is FORBIDDEN for this run. Writing a discovery `.cjs` script while MCP is available was the direct cause of 9-minute / 24K-token route discovery failures and must never happen again.

When MCP is genuinely not detected, the orchestrator MUST use the Write+Run pattern (NOT heredoc — see qa-argus Hard Stop Rule #5).

The fallback discover.cjs script MUST implement `extractRoutes(text)` inline (same regex logic as `probe.extractBundleRoutes`) and MUST write only the extracted `[{path}]` array to routes.json — never the raw bundle text. The same bundle-text-in-context prohibition applies even in fallback mode.

### Required two-step pattern

**Step A — Write the discovery script via the Write tool** to `{project-root}/.tmp/{runId}/discover.cjs`. The script must:

- `require` Playwright from `{project-root}/node_modules/@playwright/test`
- Read `process.env.QA_BASE_URL`, `QA_EMAIL`, `QA_PASSWORD`, `QA_LOGIN_PATH`, `QA_RUN_DIR`
- Implement every probe from the **Probes** section above inline as JavaScript functions
- Run the four-pass strategy (manifests → unauthenticated → authenticated → enrichment → edge)
- Write `{QA_RUN_DIR}/routes.json` directly to disk
- Exit with code 0

**Step B — Run it via the Bash tool** with environment variables set inline:

```bash
QA_BASE_URL="..." QA_EMAIL="..." QA_PASSWORD="..." QA_LOGIN_PATH="/login" QA_RUN_DIR="{abs}/.tmp/{runId}" \
  node "{abs-project-root}/.tmp/{runId}/discover.cjs"
```

Or PowerShell:
```powershell
$env:QA_BASE_URL = "..."
$env:QA_EMAIL = "..."
$env:QA_PASSWORD = "..."
$env:QA_LOGIN_PATH = "/login"
$env:QA_RUN_DIR = "{abs}/.tmp/{runId}"
node "{abs-project-root}/.tmp/{runId}/discover.cjs"
```

### FORBIDDEN patterns

These DO NOT work cross-platform (especially Windows) and MUST NEVER be used:

```bash
# FORBIDDEN — heredoc with embedded JS breaks on Windows
node - <<'EOF'
  const x = `${something}`;
EOF

# FORBIDDEN — node -e with JS containing backticks or quotes
node -e "const x = `foo`;"

# FORBIDDEN — bash -c with JS embedded
bash -c "node -e 'const x = \`foo\`;'"
```

The Write tool sends file content as raw bytes — no shell escaping needed. Always use it for scripts longer than 3 lines or containing JS template literals, regex, or special characters.
