---
name: navigation-speed
description: Page-to-page navigation — prefetch, Speculation Rules, bfcache breakers, instant loading UI, full reloads, scroll, View Transitions, route announcement.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# navigation-speed

## Premise

A real session is dominated by page-to-page navigation, not the first cold load. The first paint is measured to death (Lighthouse, CWV); the 2nd → 50th navigation usually isn't measured at all, and that's where "the app feels slow" actually lives. This skill audits the levers that make the NEXT page appear instantly: prefetch the route before the click, serve from bfcache on back/forward, paint a layout-stable skeleton the instant a navigation starts, and never hard-reload when a soft navigation would do.

Every finding cites `<file:line>` + the matched pattern + a concrete fix + a closure verb. "Navigation feels sluggish" without a cited link / handler / missing boundary is not a finding. A scan that returns zero findings on a multi-route app without listing the patterns it grepped is a failed scan.

**Closure verbs (one per finding)** — what each means here:
- `report-with-fix` — pattern matched at `<file:line>` + the concrete prefetch / boundary / `router.push` / `pagehide` patch.
- `report-flagged` — measured-relevant but the fix is an architectural call (adopt Speculation Rules host-wide, restructure a layout) → surface for ADR, naming who decides.
- `dismiss` — pattern matched but the carve-out applies (auth-mutating link, logout prerender, pagination tail) → documented so the next scan doesn't re-flag it.

## Pre-flight greps

Run as **one** script from the repo root; shell state does not survive between tool calls. Grep **N** feeds detector **§N**. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. Files-without-match is `--files-without-match`, never `-L` (that is `--follow` in ripgrep). An `rg` error on stderr (exit 2) is a failed grep, not zero hits.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|next|nuxt)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!*.{md,mdx,snap,map,lock}' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#|<!--|\{/\*)')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
CMP=(-g '*.{jsx,tsx,vue,svelte,astro}' -g '*.component.html')
CODE=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro}')
# 0. Lanes: the client router and its prefetch primitive (§ Prefetch primitive per framework); no router = a document-navigation surface.
rg -n --no-heading '"(next|nuxt|@sveltejs/kit|react-router|react-router-dom|@tanstack/react-router|vue-router|@angular/router|astro|quicklink|ngx-quicklink)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
# 1. Internal links that do not prefetch: a raw <a href="/…"> in a component (1a); a link with prefetch turned off (1b).
rg -n --no-heading --pcre2 '<a\b[^>]*\bhref=["\x27{`]*/(?![/\\])' "${CMP[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bprefetch=\{?\s*false\b|:prefetch=["\x27]false|data-sveltekit-preload-(?:data|code)=["\x27]off|\bpreload=\{?\s*false\b' "${CMP[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. Speculation Rules present (2a) — the detector fires only on a document-navigation surface (§2 conditions).
rg -n --no-heading --pcre2 'type=["\x27]speculationrules|Speculation-Rules\s*:' "${UI[@]}" -g '**/{nuxt,next,astro}.config.*' -g '**/_headers' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 3. bfcache breakers: unload / beforeunload listeners (3a); long-lived connections — WebSocket, socket.io `io(…)`,
#    EventSource, BroadcastChannel, IndexedDB (3b) — in files that never listen for pagehide (3c).
rg -n --no-heading --pcre2 'addEventListener\(\s*["\x27](?:unload|beforeunload)["\x27]|\bon(?:before)?unload\s*=|useEventListener\([^,]*,\s*["\x27](?:before)?unload' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bnew\s+(?:WebSocket|BroadcastChannel|EventSource|Manager)\s*\(|\bio\s*\(|from\s+["\x27]socket\.io-client["\x27]|\bindexedDB\.open\s*\(|\bopenDB\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match 'pagehide'
# 4. Instant-loading UI: Next App Router page dirs with no loading.* (4a); pending-state primitives in use — React Router useNavigation,
#    Nuxt <NuxtLoadingIndicator>, Vue/React <Suspense>, SvelteKit navigating (4b); the deprecated SvelteKit $app/stores import (4c).
rg --files -g '**/app/**/page.{tsx,jsx,ts,js}' "${X[@]}" "${ROOTS[@]}" | while read -r f; do ls "$(dirname "$f")"/loading.* >/dev/null 2>&1 || echo "$f"; done
rg -n --no-heading --pcre2 '\buseNavigation\(\)|\buseRouterState\(|\bnavigating\b|<Suspense\b|\bisNavigating\b|\buseLoadingIndicator\(|<NuxtLoadingIndicator\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | wc -l
rg -n --no-heading --pcre2 'from\s+["\x27]\$app/stores["\x27]' -g '*.{svelte,ts,js}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5. Full reload where a soft navigation belongs (an assignment, not a comparison).
rg -n --no-heading --pcre2 '\b(?:window\.|document\.)?location\.(?:href|pathname)\s*=(?!=)|\blocation\.(?:assign|replace)\s*\(|\bwindow\.location\s*=(?!=)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6. Manual scroll restoration.
rg -n --no-heading --pcre2 'scrollRestoration\s*=\s*["\x27]manual' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7. View Transitions in use (7a) and whether a reduced-motion guard exists anywhere in the styles (7b).
rg -n --no-heading --pcre2 'startViewTransition\s*\(|view-transition-name|@view-transition|viewTransition\s*:|withViewTransitions\(|<ViewTransitions\b' "${CODE[@]}" -g '*.{css,scss}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -c --pcre2 'prefers-reduced-motion' -g '*.{css,scss,sass,less,vue,svelte,tsx,jsx,ts}' "${X[@]}" "${ROOTS[@]}"
# 8. Route-change announcement: live regions, focus moves (`.focus()` and `.focus({ preventScroll: true })`), framework announcers.
rg -n --no-heading --pcre2 'aria-live=|role=["\x27]status["\x27]|<NuxtRouteAnnouncer\b|\.focus\(\s*(?:\{[^)]*\})?\s*\)' "${CODE[@]}" -g '*.component.html' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A hit is a candidate. Two blind spots are structural:

- **A listener added by a library is invisible to grep 3a.** Analytics, chat and session-replay SDKs register `unload` / `beforeunload` themselves. The Lighthouse `bf-cache` audit's `notRestoredReasons` (same id in 12 and 13) is the ground truth; the grep only finds the first-party ones.
- **Grep 1a sees literal paths only.** A raw anchor whose `href` is built from a variable (`:href="url"`, `href={link}`) is not listed; read the shared link components instead.

**Measured** (2026-10-05, read-only). Scratch fixture: a raw internal anchor, a `preload-data="off"` link, an `unload` listener, a `location.href` assignment, a page with no `loading.tsx` and a `$app/stores` import, all hit; the external and protocol-relative anchors, the comparison `location.href === …`, and the WebSocket in a file that listens for `pagehide` stay out. Benchmark fixtures: 1a hits once each in `quality-mix` and `vuln-fullstack`; 8 lists the existing live regions; the rest 0. Real repos: a Nuxt 4 storefront (3a: 2 `beforeunload` listeners in an engagement tracker; 5: 1 post-checkout redirect, a legitimate cross-origin carve-out on read; 1a: 4, of which 2 are anchors inside translated HTML strings), a Vue 3 + Vite admin SPA (5: 1 hard reload in a router guard) and an Angular 19 template (5: 6, four of them `mailto:` assignments, which are not navigations). Re-measured 2026-10-15 on a real NestJS + React monorepo (Vite SPA, socket.io realtime): 3b 0 → 1 — the app's socket bus opens `io(env.wsUrl, …)` and never listens for `pagehide`, a bfcache blocker the WebSocket-only pattern missed; 8: 56 → 61 lines, five new `.focus({ preventScroll: … })` calls, two of them the portal shell's route-change focus on `<main>` that the bare `.focus()` pattern had missed (the other three move focus inside a form, a popover and a landing tour). Fixtures: unchanged.

## The 3,000-hit path

1. **Group** by (shared component or module, pattern). One `NavLink` wrapper, one analytics module or one router guard is one finding for every caller.
2. **Rank** by route traffic and by navigation frequency (primary nav, list → detail, back from detail).
3. **Read the top 30 groups.** Ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them, never `checked`.

## Scans for

### 1. Internal links that don't prefetch

The framework's link primitive prefetches the next route's code (and often data) before the click — usually on viewport-entry or hover. A raw `<a>` to an internal route, or a link with prefetch explicitly disabled, pays the full round-trip on click.

```
BAD:
<a href="/products/42">View</a>          // raw anchor — no prefetch, full reload
<NuxtLink to="/x" :prefetch="false">     // prefetch turned off without a reason

GOOD:
<Link href="/products/42">View</Link>    // Next: auto-prefetch in-viewport (prod)
<NuxtLink to="/x">                        // Nuxt: prefetches in-viewport by default
<a href="/x" data-sveltekit-preload-data="hover">  // SvelteKit
```

Grep: raw `<a href="/` (app-internal paths) in framework component files; `prefetch=\{?false`, `:prefetch="false"`, `data-sveltekit-preload-data="off"`. Per-framework primitives → §"Prefetch primitive per framework".

### 2. No Speculation Rules on a content/MPA surface

For multi-page apps (or any surface where the framework link doesn't prerender), the Speculation Rules API lets the browser **prerender** the next document in the background — the navigation then resolves in ~0ms.

```
GOOD (in <head> or injected):
<script type="speculationrules">
{ "prerender": [{ "where": { "href_matches": "/*" },
                  "eagerness": "moderate" }] }
</script>
```

`eagerness`: `immediate` / `eager` / `moderate` (hover ~200ms) / `conservative` (pointerdown). Prefer `prefetch` (cheaper, no JS execution) when prerender is too aggressive. Grep for `type="speculationrules"`.

**This detector only fires on a surface the framework link primitive cannot already serve** — otherwise it proposes a second prefetch mechanism beside a working one. Two conditions, both required, both checkable:

1. **The navigation is a document navigation.** Either the project ships no client router (no entry in the § Prefetch-primitive table matches its stack), or the specific links in question leave the router's control — `target="_blank"`, a cross-app link inside a monorepo, a link into a separately-deployed marketing or docs surface, a server-rendered pagination link.
2. **The next document is prerenderable** — a GET with no side effect, no per-click personalisation that a prerender would resolve early and stale.

Fail either → `dismiss` with the reason (`SPA: <Link> already prefetches` / `side-effecting GET`). Pass both and no `speculationrules` block exists → `report-flagged`: adopting it is a host-wide `<head>` change with a `where` allow-list somebody has to own, not a mechanical edit.

### 3. bfcache (back/forward cache) breakers

Back/forward navigations should restore the page instantly from memory — no re-fetch, no re-render. The page becomes **ineligible** if it ships disqualifying code.

```
BAD:
window.addEventListener('unload', save);        // HARD disqualifier
window.addEventListener('beforeunload', warn);  // disqualifies unless conditionally added

GOOD:
window.addEventListener('pagehide', save);
window.addEventListener('visibilitychange', save);  // most robust persistence hook
```

Grep: `addEventListener\(['"](unload|beforeunload)`. Also flag open `IndexedDB` / `WebSocket` / `BroadcastChannel` not closed on `pagehide` (these hold the page out of bfcache). `Cache-Control: no-store` on the document is a **warn/review**, not a hard fail — Chrome rolled bfcache for no-store ("CCNS") to 100% in 2025 where safe; the hard disqualifier remains the `unload` listener. Cite the actual reason from a Lighthouse `bf-cache` audit when claiming ineligibility (see §"Verify").

### 4. Missing instant-loading UI on navigation

When a navigation starts, the user must see a layout-stable skeleton **immediately** — not a spinner, not a frozen old page, not a blank screen. Otherwise even a fast route feels slow because nothing acknowledges the click.

```
BAD:  app/products/page.tsx exists, no app/products/loading.tsx  (Next App Router)
BAD:  <RouterView/> with no pending/transition state         (Vue/React Router)

GOOD: app/products/loading.tsx → streams a skeleton instantly
GOOD: const nav = useNavigation(); nav.state === 'loading' → <Skeleton/>  (React Router)
GOOD: import { navigating } from '$app/state'   // SvelteKit ≥ 2.12 (Svelte 5); `$app/stores` is the deprecated form (grep 4c)
```

The skeleton MUST match final dimensions (reserve width/height) — a skeleton that reflows just trades a blank screen for a CLS hit. Grep route segments lacking a sibling loading convention; flag router outlets with no pending-state branch.

### 5. Full reload where a soft navigation belongs

Programmatic navigation through `window.location` throws away the SPA — full document reload, re-parse, re-hydrate, lost client state.

```
BAD:   window.location.href = '/dashboard';
       location.assign('/orders/' + id);

GOOD:  router.push('/dashboard');           // Vue / Next useRouter / SvelteKit goto
       navigate('/orders/' + id);            // React Router
```

Grep: `(window\.)?location\.(href|assign|replace)\s*=` and `location\.(assign|replace)\(` in component / handler code. Carve-out: cross-origin redirects, post-logout, and intentional hard reloads after a deploy-version mismatch are legitimate → `dismiss` with the reason.

### 6. Scroll restoration mishandled

On back/forward the browser restores scroll position; a route that sets `history.scrollRestoration = 'manual'` without re-implementing restoration leaves users at the top of a long list they scrolled. Grep `history.scrollRestoration\s*=\s*['"]manual` with no paired restore logic.

### 7. View Transitions as a perceived-instant mechanism

The View Transitions API cross-fades / morphs between states so a soft navigation *feels* continuous instead of a hard swap. It is a **perception** layer — never a substitute for real prefetch/streaming (a slow route with a pretty transition is still slow).

```
Same-document:  document.startViewTransition(() => updateDOM());
Cross-document: @view-transition { navigation: auto; }   /* CSS, MPA */
Shared element: view-transition-name: hero-<id>;
```

Always gate motion behind `@media (prefers-reduced-motion: reduce)`. Flag a shared-element transition with no `view-transition-name`, or a `startViewTransition` that wraps an async data fetch (it should wrap the DOM update only, after data is ready).

### 8. Soft navigation that never announces itself (focus + live region)

A client-side navigation swaps the DOM without a document load, so **the screen reader says nothing and focus stays on a link that no longer exists**. The user hears silence, then lands mid-document with no idea the page changed. Every lever above makes navigation faster; this one makes it perceivable. It is the a11y consequence of the mechanism this skill owns, which is why the detector lives here — `@accessibility-auditor` grades conformance, this scan finds the missing wiring.

```
BAD:  router.push('/orders')            // that is the whole handler; nothing else happens
GOOD: after the route resolves, move focus to the new view's <h1> (tabindex="-1" + .focus()),
      OR announce the new document title through ONE app-shell live region:
      <p aria-live="polite" class="sr-only">{routeAnnouncement}</p>
```

Grep 8 lists the live regions, `role="status"` and `.focus()` calls (ripgrep exits 2 on a missing path, which reads like "no findings" if you only check the output) — zero hits in a project that ships a client router is the finding. Then check the opposite failure: **one** live region in the app shell, not one per view (N regions announce N times, or fight each other). Carve-out: a router that already ships route announcement (some do) — cite the router's mechanism and `dismiss`.

## Prefetch primitive per framework

| Framework | Prefetch primitive | Default | Disable / tune |
|---|---|---|---|
| **Next (App Router)** | `<Link>` (+ `useRouter().prefetch()`) | auto-prefetch in-viewport in **prod** | `prefetch={false}`; `prefetch={null}` = partial (default) |
| **Nuxt** | `<NuxtLink>` (+ `prefetchComponents`) | prefetches in-viewport links | `:prefetch="false"`; `prefetchOn="interaction"` |
| **SvelteKit** | `data-sveltekit-preload-data` | off until set (often on `<body>`) | `"hover"` / `"tap"` / `"off"`; code: `data-sveltekit-preload-code="eager\|viewport\|hover\|tap"` |
| **React Router** | `<Link prefetch>` | `"none"` | `"intent"` (hover/focus) / `"render"` / `"viewport"` |
| **TanStack Router** | `<Link preload>` | off | `preload="intent"` (router default configurable) |
| **Angular** | route `PreloadingStrategy` | none | `withPreloading(PreloadAllModules)` or `ngx-quicklink` |
| **Plain HTML / MPA** | Speculation Rules + `<link rel="prefetch">` | none | `eagerness` tuning |

## Output

```
Navigation-speed audit — <route set or full scan>

Per-route table:
  route          prefetch  loading-UI  bfcache   spec-rules      finding
  /products      ✓ (Link)  ✗           ✓         dismissed (SPA) missing loading.tsx
  /orders/[id]   ✗ (<a>)   ✓           ⚠         dismissed (SPA) raw anchor → <Link>
  /docs/*        ✗ (MPA)   n/a         ✓         ABSENT          no speculationrules on a document-nav surface
  /reports       ✓         ✓           ✗ unload  dismissed (SPA) bfcache-blocked

The `spec-rules` column never prints `n/a`: detector 2 either fired, was `dismiss`ed with its reason, or found the block present. `n/a` on every row is what a column looks like when the detector never ran, and it is indistinguishable from a clean result.

Findings: 3

1. components/OrderRow.vue:18                          [report-with-fix]
   Raw <a href="/orders/{{id}}"> for internal nav — no prefetch, full reload.
   Fix: <RouterLink :to="`/orders/${id}`"> (vue-router does NOT auto-prefetch
        the chunk — warm import('./OrderDetail.vue') on hover, or adopt quicklink).

2. app/products/  (segment)                            [report-with-fix]
   No loading.tsx beside a route whose page awaits a slow server fetch.
   Fix: add app/products/loading.tsx returning a dimension-matched skeleton;
        wrap the slow subtree in <Suspense> so the shell streams first.

3. lib/analytics.ts:44                                 [report-with-fix]
   window.addEventListener('unload', flush) — HARD bfcache disqualifier.
   Fix: switch to 'pagehide' (or 'visibilitychange' + navigator.sendBeacon).

Verification: 14 candidates → 3 findings · 1 unconfirmed · 10 refuted

Class coverage:
  §1  no prefetch               checked (4 hits → 1 finding)
  §2  speculation rules         checked (SPA: <Link> already prefetches → dismissed; /docs/* → 1 unconfirmed, report-flagged)
  §3  bfcache breakers          checked (1 hit → 1 finding; bf-cache audit confirms)
  §4  instant-loading UI        checked (2 segments → 1 finding)
  §5  full reload               checked (3 hits → 0 findings; logout and cross-origin carve-outs)
  §6  scroll restoration        checked (0 hits)
  §7  View Transitions          N/A (none in use)
  §8  route announcement        checked (Next App Router announcer; dismissed with its mechanism)
```

`[report-with-fix]`: a cited line and a local patch. `[report-flagged]`: an architectural call (Speculation Rules host-wide, a layout restructure) or an unproven link; the row names who decides or the run that settles it. The coverage block lists **all eight** classes on every run: `checked (k hits → m findings)`, `N/A (<reason>)`, or `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

- `prefetch={false}` is CORRECT on auth-mutating links, expensive dynamic pages, and the long tail of paginated links — flag only the *primary* in-viewport nav. Treat an intentional `data-sveltekit-preload-data="off"` the same way.
- Speculation Rules **prerender** must NEVER target logout, delete, or any GET that triggers a side effect — prerender executes the page. Use `prefetch` for those, or exclude them with `where`.
- bfcache eligibility must be cited from a real Lighthouse `bf-cache` audit (it reports the actual `notRestoredReasons`) — a grep is a *candidate*, the audit is ground truth.
- `vue-router`'s `<router-link>` and plain React Router (without the framework) do NOT auto-prefetch route chunks the way Next `<Link>` / `<NuxtLink>` do — don't assume a prefetch you didn't wire.
- View Transitions degrade gracefully (unsupported browsers just hard-swap) — don't block a navigation waiting for the API.

## When to run

- After adding routes or a new navigation surface (nav bar, command palette, deep links).
- Before shipping a logged-in, multi-page app — internal navigation is the dominant interaction.
- On any "the app feels slow when I click around" report (distinct from "the first load is slow" → `lighthouse-ci` in this pack, or `bundle-perf` *(performance pack, when co-installed)*).
- Pair with `streaming-ssr` (this pack) when a slow route blocks the navigation on a server query. Field INP on the *navigated-to* route comes from `web-vitals-field` *(performance pack, when co-installed)*; absent that pack this scan is static only — report `INP: no field source` rather than inferring one from the greps.

## Halt conditions

- Halt if detector 8 is reported as PASS without naming either the focus target or the live region at `<file:line>` — "the router handles it" is a claim, and the claim is checkable.
- Halt on hand-waves: every prefetch / bfcache / reload / loading-UI finding cites `<file:line>` + the matched pattern + a concrete fix. "Could prefetch more" without a link is not a finding.
- Halt if a bfcache-ineligible claim isn't backed by either the grepped `unload`/`beforeunload` line OR a Lighthouse `bf-cache` audit reason.
- Halt if Speculation Rules are proposed without excluding side-effecting GETs (logout/delete) from the `prerender` set.
- Halt if an instant-loading fix proposes a spinner or an unsized skeleton (CLS) instead of a dimension-matched one.
- Halt if a default framework prefetch is disabled in a fix without a documented reason.
- Halt before reporting any candidate that has not been through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§1 restate … §9) and [`precedents/ui.md`](../../../../snippets/precedents/ui.md) § 27 (built-in route announcers). **Proof:** §3 the `bf-cache` audit passes (same id in Lighthouse 12 and 13) and a Playwright back navigation reports `persisted === true` on `pageshow`; §1 and §4 the next route's chunk is requested before the click (`page.on('request')`) and the skeleton paints before the data resolves; §8 the focus target or live-region text is asserted after a client navigation.

## Related

- `code-splitting.md` (ai-pattern) — this skill owns prefetching the likely-next route's chunk on hover/idle so the split click resolves from cache; that pattern owns where the chunk boundary is cut.
- `list-virtualization.md` (ai-pattern) — restore a windowed list's scroll by first-visible index, not pixel `scrollTop`, on back/forward + bfcache restore.
- `lighthouse-ci` — owns the cold first load and reports `bf-cache` ineligible; this skill owns every navigation after it and names the listener that caused the ineligibility.
- Cross-pack (`performance`, when co-installed): `web-vitals-field` confirms whether a prefetch/bfcache win actually reached users. Absent that pack this skill's output is a static claim, not a measurement, and the report must say which.
