---
name: critical-path-scan
description: Render-blocking head tags, critical-path third parties, late-inserted layout shift — proved on a production build.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: critical-path-scan

## Premise

Between the first byte of HTML and the first useful paint, the browser does only what the document tells it to. A synchronous `<script src>` in the `<head>`, a stylesheet on another origin or a CSS `@import` chain stops rendering until it arrives. A tag manager or a chat widget loaded before the page can respond takes main-thread time the user's first tap needs. After the paint, a banner, a consent bar, an embed or an ad that arrives late pushes the content the user is already reading. None of this is visible in the component tree, and none of it fails a type check.

This skill owns three rows `/bundle-perf` (performance pack) delegates to the frontend pack: **L2** render-blocking `<head>` (§1), **I3** third-party scripts on the critical path (§2), and **X1b** late-inserted content that shifts layout (§3). The first two replace bundle-perf's interim lanes **P2** and **P3**; their greps were copied here and hardened. The research catalog files the same classes as **P-01**, **P-02** and **P-06**. Its ids run one ahead of bundle-perf's lane names, so P-01 is lane P2.

**Every finding cites the tag or component `<file:line>` + the route whose first load it is on + the oracle that fired (or the run that would settle it) + the fix in the project's framework.** A grep hit is a candidate, never a finding by itself. "Critical path clean" is never printed without the class-coverage block (§ Output).

## The rule

A candidate is a finding when all four hold:

1. **Users receive it.** The file is the shell or a component a real route renders on first load. A dev-only page, a design-system docs page or Storybook fails here (`precedents/ui.md` § 10).
2. **It is on the critical path.** For §1, the resource blocks first render: not `async`, `defer`, `type="module"`, a print-media swap or an inline bootstrap. For §2, the script runs before first interaction, not after consent, idle or a click. For §3, the content arrives after first paint, inside the viewport, in normal flow.
3. **No control already covers it.** The space is reserved (`min-height`, `aspect-ratio`, a sized skeleton, a `fixed` overlay). A framework primitive loads the tag late (`next/script` `lazyOnload`, `@nuxt/scripts` with a `trigger`).
4. **The oracle fires.** The browser marks the resource render-blocking; ablating the vendor moves the median outside the noise band; the layout-shift observer records a shift whose source is the node.

## Boundaries

- **Fonts** (FOIT, a Google Fonts stylesheet, swap shift) → `font-optimization` (this pack). 1b prints `fonts.googleapis.com` hits so the run can route them; they are counted there, not here.
- **Unsized `<img>`** → `image-optimization` §3. **The LCP resource** (lazy hero, late discovery, `fetchpriority`) → `lcp-audit`. **Lists that insert above the viewport** → `list-virtualization` detector 5 (ai-pattern, this pack). §3 cross-links it rather than counting it twice.
- **Third-party script integrity, CSP, and tags that load before consent as a privacy question** → security `xss-scan` and `data-exposure-scan`, when the security pack is installed. §2 here judges main-thread cost only. Without the security pack, the consent-ordering question is printed as a note, never as a finding of this skill.
- **Bytes, legacy polyfills and dev-only code in the build** → `bundle-analyze` §1–§7 (this pack).
- **Ranking across routes and the page-load verdict** → `/bundle-perf` (performance pack, when installed). Without it, this skill reports per route and never issues a page-load verdict.

## Adapt to the codebase — the critical-path lanes

Read the framework and its version from the lockfile and print the lanes in the output header.

| Lane | Where the shell lives (§1) | How third parties load (§2) | Late-insert surface (§3) | Fix vocabulary |
|---|---|---|---|---|
| **Vite SPA** (React, Vue, Svelte, Solid) | `index.html` at the app root | `<script>` in `index.html`; `document.createElement('script')` in an effect | everything after `#root` mounts: banners in the app shell, `Suspense fallback={null}` | `defer`/`async`; inject after `requestIdleCallback` or consent; reserve space |
| **Next.js 16** (App Router, Pages) | `app/layout.tsx` `<head>`; `pages/_document.tsx` | `next/script` `strategy` (`beforeInteractive` blocks); `@next/third-parties` 16.3.8 | `dynamic(…, { ssr: false })` with no `loading`; client-only banners | `afterInteractive`/`lazyOnload`; `GoogleTagManager`, `YouTubeEmbed`; `loading` placeholder |
| **React Router 7 / Remix** | `app/root.tsx` `<Links/>`, `links()` exports | `<script>` in `root.tsx`; effects | route `clientLoader` content swapped in | same as Vite SPA |
| **Nuxt 4 / Vue SSR** | `nuxt.config` `app.head.script` / `link`; `useHead` | `@nuxt/scripts` 1.3.12 `useScript` (with or without `trigger`) | `<ClientOnly>` with no `#fallback` slot | `trigger: 'onNuxtReady'` / consent trigger; `#fallback` sized like the content |
| **SvelteKit** | `src/app.html`; `<svelte:head>` in `+layout.svelte` | `<svelte:head>` scripts; `onMount` injection | `{#if browser}` blocks above the fold | `defer`; inject in `onMount` after idle |
| **Angular 20–22** | `src/index.html`; `angular.json` `scripts` / `styles` arrays | `index.html` tags; `Renderer2` injection | `@defer` blocks with no `@placeholder` | `@defer (on idle)` with a sized `@placeholder` |
| **Astro** | layout `.astro` files; `<script is:inline src>` | `is:inline` tags; Partytown integration | client islands (`client:only`) | let Astro bundle the script; sized island wrapper |

`@builder.io/partytown` was last published 2024-12-20 (0.10.3, npm, read 2026-10-05). Offer it as a fix only after checking the vendor works inside a worker; many do not.

## Lighthouse ids by version

Lighthouse 13 removed the legacy audit ids; only the `*-insight` audits remain. `@lhci/cli` 0.15.1 (2025-06-25, still the latest on 2026-10-05) bundles Lighthouse **12.6.1**, which has both sets. A standalone `npx lighthouse` is 13.5.0 and has only the insight ids (research catalog § 1.9 and its notes § 1.4, from the unpacked 12.6.1 and 13.5.0 packages). Read the version the runner prints and pick the row:

| Class | Lighthouse 12.6.1 (LHCI 0.15.1) | Lighthouse 13.x (`npx lighthouse`) |
|---|---|---|
| §1 render-blocking | `render-blocking-resources` (assert `maxLength: 0`); `render-blocking-insight` also present | `render-blocking-insight` |
| §2 third parties | `third-party-summary`; `third-parties-insight` also present | `third-parties-insight` |
| §2 facades | `third-party-facades` | removed; no insight replaces it |
| §3 layout shift | `cumulative-layout-shift`, `layout-shifts`, `cls-culprits-insight` | the same three |

When both ids exist, assert on the insight id so the assertion survives the upgrade, and keep the legacy id beside it while CI still runs LHCI 0.15.x:

```bash
LHV=$(npx --no-install lighthouse --version 2>/dev/null || echo 12.6.1)   # under LHCI the bundled 12.6.1 applies whatever this prints
case "${LHV%%.*}" in 13) IDS=render-blocking-insight,third-parties-insight,cls-culprits-insight,layout-shifts ;;
                     *)  IDS=render-blocking-resources,render-blocking-insight,third-party-summary,third-parties-insight,cls-culprits-insight,layout-shifts ;; esac
```

## Pre-flight greps

Run as **one** script from the repo root; shell state does not survive between tool calls. Grep **N** feeds detector **§N**. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. Files-without-match is `--files-without-match`, never `-L` (that is `--follow` in ripgrep). An `rg` error on stderr (exit 2) is a failed grep, not zero hits.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|@builder\.io/qwik)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,scripts,tools,locales,i18n,generated,__generated__,docs}/**' -g '!**/*.doc.*'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!*.{md,mdx,snap,map,lock}' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#|<!--)')       # drops comment-only lines; every -n grep ends in it
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
SHELL_G=(-g '*.html' -g '**/{_document,document,root,layout,app}.{tsx,jsx,js,ts}' -g '**/+layout.svelte' -g '**/{nuxt,astro}.config.*' -g '*.astro')
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'                            # a JSX tag body that survives `onClick={() => x}`
V='googletagmanager\.com|google-analytics\.com|connect\.facebook\.net|static\.hotjar\.com|clarity\.ms/|cdn\.segment\.com|widget\.intercom\.io|client\.crisp\.chat|embed\.tawk\.to|js\.driftt\.com|js\.hs-scripts\.com|cdn\.optimizely\.com|dev\.visualwebsiteoptimizer\.com|cdn\.cookielaw\.org|app\.usercentrics\.eu|consent\.cookiebot\.com|js\.stripe\.com|cdn\.amplitude\.com|cdn\.mxpnl\.com|browser\.sentry-cdn\.com|snap\.licdn\.com|static\.ads-twitter\.com|analytics\.tiktok\.com|plausible\.io/js|cdn\.jsdelivr\.net|unpkg\.com|cdnjs\.cloudflare\.com'
# 0. Lanes and versions.
rg -n --no-heading '"(next|nuxt|vite|@sveltejs/kit|@angular/core|astro|react-router(-dom)?|@remix-run/react|webpack|@rsbuild/core|@next/third-parties|@nuxt/scripts|@builder\.io/partytown|web-vitals|@lhci/cli|lighthouse)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}" | "${NC[@]}"
# 1. Render-blocking head: 1a a sync script src in a shell; 1b a cross-origin stylesheet (either attribute order, print swap
#    skipped) or a CSS @import of a URL — in HTML that TS/JS template strings write too (print and receipt frames); 1c an @import chain in raw-served CSS; 1d beforeInteractive or a head script in config.
rg -n --no-heading --pcre2 '<script\b(?![^>]*\b(?:async|defer|type=["\x27](?:module|application/(?:ld\+)?json|importmap|speculationrules|text/template)["\x27]))[^>]*\bsrc=' "${SHELL_G[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '@import\s+(?:url\()?["\x27]?(?:https?:)?//|<link\b(?=[^>]*\brel=["\x27]?stylesheet)(?=[^>]*\bhref=["\x27]?(?:https?:)?//)(?![^>]*\bmedia=["\x27]?print)' -g '*.{css,scss,sass,less,html,tsx,jsx,ts,js,mjs,vue,svelte,astro}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading '@import\b' -g '**/{public,static}/**/*.css' -g '!**/node_modules/**' "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 'strategy=["\x27{]*beforeInteractive|\bsrc\s*:\s*["\x27](?:https?:)?//' -g '**/{nuxt,astro,next}.config.*' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2. Third parties: 2a vendor hosts; 2b anti-flicker, a consent stub, a next/script with an external src and no strategy;
#    2c a script element injected from code; 2d a Nuxt useScript with no trigger.
rg -n --no-heading -i --pcre2 "$V" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 "\\basync-hide\\b|otSDKStub|<Script\\b(?!${TB}\\bstrategy=)${TB}\\bsrc=[\"\\x27{]*(?:https?:)?//" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 'createElement\(\s*["\x27]script["\x27]\s*\)' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l0 'useScript\(' -g '*.{vue,ts,js}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match '\btrigger\s*:'
# 3. Late-inserted content: 3a an in-flow banner (multi-line tag body; `fixed`/`absolute` skipped, `sticky` kept — a sticky
#    band is in flow); 3b an iframe/embed/video with no size; 3c an ad slot with no reserved height; 3d a null fallback or a
#    client-only swap with no placeholder.
rg -n -U --no-heading --pcre2 "(?<![\\w.\$])<(?:CookieBanner|Consent\\w*|Announcement\\w*|PromoBar|TopBanner|\\w*Banner|Cookie\\w*Notice|\\w*NotificationBar|\\w*WarningBar|Alert[A-Z]?\\w*Bar|Marquee)\\b(?!${TB}\\b(?:fixed|absolute))" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --no-heading --pcre2 "(?<![\\w.\$])<(?:iframe|embed|video)\\b(?!${TB}\\b(?:width|height|aspect|className=[\"\\x27][^\"\\x27]*\\b(?:aspect-|h-|size-)|class=[\"\\x27][^\"\\x27]*\\b(?:aspect-|h-|size-)))" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '<ins\b(?=[^>]*adsbygoogle)(?![^>]*(?:min-height|height))|googletag\.defineSlot' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 'fallback=\{\s*null\s*\}|\bssr\s*:\s*false\b(?![^}\n]*\bloading\s*:)|<ClientOnly>(?![\s\S]{0,80}#fallback)|@defer\b(?![^{\n]*\{[\s\S]{0,200}@placeholder)' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a hit **plus** a read of where it renders **plus** the oracle. Two blind spots are structural:

- **Sizing in a stylesheet is invisible to 3b.** An iframe whose height comes from a project class (`.receipt-frame { height: 26rem }`) hits the grep; read the class before calling it unsized.
- **A shell assembled at build time is invisible to §1.** A Vite plugin, an HTML transform or a CDN edge rule can add tags the source never shows. On a production build, read the emitted `index.html` (or `curl` the deployed document) once and grep it with 1a and 1b.

**Measured** (2026-10-05). On the research fixture set for these classes, every positive hits and every decoy stays out: 1a 3/3 (`type=module`, `defer`, `async` and `ld+json` skipped), 1b 2/2 (the `media=print` swap and a local `@import` skipped), 2a/2b 3/3 plus the anti-flicker style and the consent stub, 3a–3c 3/3 (the sized iframe skipped). On the twelve benchmark fixtures every grep returns 0 except 3a on `slow-marketplace` (`<PromoBar>`, rendered in the first commit with the rest of the app, so not late-inserted: refuted on read). On a real React 19 + Vite 8 SPA (about 4,300 TS/TSX files, read-only) the script runs in under half a second. §1: 0 (the shell holds a module entry, a self-hosted font preload and an inline theme bootstrap). 2a: 3 and 2c: 3, one group: a tracking provider that injects a tag manager and a pixel from effects once a settings request resolves, `async`, so cost needs the ablation run. 3a: 10 lines in 6 groups; two read as candidates, both data-driven warning bands rendered into the app's sticky top stack after their query resolves. 3b: 2, both sized by a project CSS class (refuted on read). 3d: 5; one inside a `fixed` container (refuted), two in the sticky stack (candidates). Before the comment filter, the generic-type lookbehind and the docs-page exclusion, 2a returned 4 and 3a 16; the earlier single-line 3b missed the multi-line tag body that `-U` reads. Re-measured 2026-10-15 on a real NestJS + React monorepo (the same Vite SPA family): 1b 0 → 3 — three print and receipt frames written as HTML in `.ts` template strings load Google Fonts stylesheets (and wait on `document.fonts.ready`) against the shell's self-hosting rule, invisible while 1b globbed markup files only; 3a 10 → 11 lines, the new one a low-credit `*NotificationBar` in the sticky top stack that only 3d had surfaced. A bare `\w*Notice` was tried and dropped: 13 of its 15 extra hits were inline notices inside dialogs and cards; `Cookie*Notice` is kept (one hit in `a11y-states`).

## The 3,000-hit path

1. **Intersect with the route table.** A component no route renders is dismissed by one read. Design-system docs and Storybook files are their own group (`precedents/ui.md` § 10).
2. **Group** by (shell or component, pattern). A shared banner primitive or one tracking provider is one group however many routes mount it. Fixing it there closes them all (`precedents/ui.md` § 9).
3. **Rank** by route traffic: RUM or analytics when present, else landing, auth, product/detail and checkout-class routes.
4. **Read the top 30 groups.**
5. **Prefer the runtime bulk oracle at scale.** One Playwright pass over the top routes with the layout-shift observer and the render-blocking list (§ Proof) confirms or refutes whole groups of §1 and §3 hits. One ablation run per vendor host settles §2.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | bundle-perf row (interim lane) · research id | Default severity |
|---|---|---|---|
| 1 | Render-blocking `<head>`: sync script, cross-origin stylesheet, CSS `@import` chain, first-party `beforeInteractive` | L2 (P2) · P-01 | medium; high for a cross-origin sync script |
| 2 | Third-party scripts on the critical path: tag manager, chat, A/B anti-flicker, consent, session replay | I3 (P3) · P-02 | medium; high when ablation moves the mobile median LCP or TBT outside the band; a leftover anti-flicker snippet is always a finding |
| 3 | Late-inserted content shifting layout: in-flow banner, consent bar, ad, embed, null fallback, client-only swap | X1b · P-06 | medium; high when field p75 CLS on the route is over 0.1 |

### 1. Render-blocking `<head>`

```
BAD:   <script src="https://cdn.example.com/lib.js"></script>                 // parser waits for another origin
       <link rel="stylesheet" href="https://cdn.example.com/x.css">           // render waits for another origin
       @import url("https://cdn.example.com/base.css");                        // a chain: found only after the first sheet
       <Script src="/vendor/legacy.js" strategy="beforeInteractive" />          // first-party code forced ahead of hydration
GOOD:  <script type="module" src="/src/main.ts"></script>  ·  <script defer src="/a.js"></script>
       self-host the stylesheet and let the bundler inline or link it; <link rel="preload" as="style"> + media swap for non-critical CSS
       <Script src="…" strategy="afterInteractive" />
```
**Read the code:** Is this the document users receive, or a dev harness page? Is the resource cross-origin, or same-origin and small (critical CSS is meant to block)? Is the `@import` raw-served, or inlined by the bundler? Is an inline script a tiny pre-paint bootstrap (theme, locale) that must block to avoid a flash? **Finding when** a blocking resource ends after the first paint would otherwise have happened. **Proof:** the render-blocking list (§ Proof, item 1), failing first; then the Lighthouse id for the runner's version, median of 5 (§ Lighthouse ids by version). The cost reads in field LCP attribution as `elementRenderDelay`.

### 2. Third-party scripts on the critical path

```
BAD:   <script src="https://cdn.cookielaw.org/…/otSDKStub.js"></script>       // sync consent stub in the head
       <style>.async-hide { opacity: 0 !important }</style>                     // Google Optimize anti-flicker: the product
                                                                                //   was sunset 2023-09-30, the page still hides
       useEffect(() => injectTagManager(id), [])  ·  Vue onMounted(() => injectTagManager(id))   // on mount, before the user acts
       <Script src="https://widget.intercom.io/widget/x" strategy="beforeInteractive" />
GOOD:  load after consent, on `requestIdleCallback`, or on first interaction; next/script `lazyOnload`;
       `@next/third-parties` `GoogleTagManager`; `useScript(src, { trigger: 'onNuxtReady' })`; a facade for chat and video
```
**Read the code:** When does the tag run: in the head, on mount, after a settings or consent request, on idle, on click? Is it `async`/`defer` (not render-blocking, `precedents/performance.md` § 86) and only competing for the main thread? Does a legal requirement force the consent manager first (then it should be small and self-hosted)? Is the anti-flicker snippet still wired to a live experiment? **Finding when** ablating the vendor moves the 5-run median outside the measured noise band, or LoAF attributes long frames to its host before first interaction. A leftover anti-flicker snippet is a finding on read: it hides the page for its timeout and nothing removes the class. **Proof:** third-party ablation and LoAF attribution (§ Proof, item 2).

### 3. Late-inserted content shifting layout

```
BAD:   <div className="sticky top-0">{rate !== null && <DeliveryRateBanner rate={rate} />}<TopBar/></div>   // query lands, page drops
       <Suspense fallback={null}><LowCreditBar /></Suspense>   (above the fold, in flow)
       <iframe src="https://www.youtube.com/embed/x"></iframe>   ·   <ins class="adsbygoogle" style="display:block"></ins>
       <ClientOnly><PromoCarousel/></ClientOnly>   ·   dynamic(() => import('./Map'), { ssr: false })
GOOD:  reserve the band's height while the query is pending, or render the notice as a `fixed` overlay / toast
       <Suspense fallback={<div className="h-10" />}>  ·  width/height or `aspect-ratio` on the embed  ·  `min-height` on the ad slot
       <ClientOnly><template #fallback><div style="height:320px"/></template></ClientOnly>  ·  dynamic(…, { loading: () => <Skeleton h={320}/> })
```
**Read the code:** Does the content arrive after first paint (behind a query, a lazy chunk, a consent decision, a client-only boundary) or in the first commit with everything else? Is it inside the first viewport? Is it in flow (`sticky` is in flow until it sticks) or a `fixed`/`absolute` overlay? Does it appear on load or only after a user action (a shift within 500 ms of input is excluded)? Is a skeleton there, but a different height from the content? **Finding when** the layout-shift observer records a shift of 0.01 or more whose source node is this content, or the route's session-window CLS is over 0.1. **Proof:** the layout-shift observer (§ Proof, item 3); field cost through web-vitals attribution `largestShiftTarget` (§ Proof, item 4).

## Proof

Run on the **production** build (`vite preview`, `next start`, `nuxi preview`, the deployed site), never a dev server (`precedents/performance.md` § 90), on the mobile profile and on desktop. Shared shapes are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Frontend: "Lighthouse median", "Trace insight", "Field attribution" and the three oracles below. Resource Timing `renderBlockingStatus` and Long Animation Frames `scripts[]` are Chromium features, not Baseline (MDN, fetched 2026-10-05); the oracles run in Chromium.

1. **Render-blocking list** (§1, run-invariant; § Frontend, *Render-blocking list*, V147). After load, the resources Resource Timing marks `renderBlockingStatus === 'blocking'`; the candidate's URL is on the list before the fix and gone after.
2. **Third-party ablation and LoAF** (§2, cost; *Third-party ablation*, V148). Measure the band, then interleave 5 runs with the third-party hosts aborted and 5 without; a delta inside the band is `NO-CHANGE` (`precedents/performance.md` § 51). Localise with Long Animation Frames `scripts[]` grouped by host.
3. **Layout-shift observer** (§3, run-invariant per scenario; *Layout-shift observer*, V149). Observer installed before navigation; load, accept and then reject consent through its own buttons, scroll two viewports, wait 5 s. Fails first when one shift of 0.01 or more names the candidate's node, or the session CLS is over 0.1; green when neither holds.
4. **Field attribution** (cost). `web-vitals/attribution` 6.2.3: `onCLS` → `largestShiftTarget`, `largestShiftValue`, `loadState`; `onLCP` → `elementRenderDelay` for §1. A CrUX "after" needs 28 days of post-deploy traffic; the project's own RUM reads sooner.

Without a browser harness, every candidate is Unconfirmed with the run that would settle it written out; it is never promoted on reading alone ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## Output

```
critical-path-scan — lanes: react 19.2 + vite 8.2 (apps/web/package.json); next, nuxt, sveltekit, angular, astro absent
Lighthouse: not run (no harness) · production build: absent in this checkout

Findings: 0 · Unconfirmed: 3

1. src/app/layout.tsx:77 + src/entities/billing/LowCreditBar.tsx           [report-flagged]   medium
   §3 late-inserted band — lazy bar with fallback={null} inside the sticky top stack (in flow), shown after the
   principal's credit query resolves; every route of the console pushes down by its height. Unproven: no
   production build to run the observer. Settling run: layout-shift observer on /orders, owner session.
   Fix: render a fixed-height placeholder while the query is pending, or move the notice to a toast.
2. src/entities/delivery-rate/DeliveryRateBanner.tsx:20 (mounted by 2 portal shells)   [report-flagged]   medium
   §3 same class, one group — the warning band renders into the sticky stack when its counts arrive.
3. src/features/tracking/model/AnalyticsProvider.tsx:95                      [report-flagged]   medium
   §2 tag manager and pixel injected from effects once the settings request resolves, async. Unproven: main-thread
   cost. Settling run: ablation of googletagmanager.com / connect.facebook.net, 5-run medians, mobile.
   Fix: inject on requestIdleCallback or after consent; consider @next/third-parties-style deferral.

Verification: 12 candidates → 0 findings · 3 unconfirmed · 0 hardening · 9 refuted

Class coverage:
  §1  render-blocking head     checked (0 hits; shell read: module entry, self-hosted font preload, inline theme bootstrap)
  §2  critical-path 3P         checked (6 hits / 1 group → 1 unconfirmed)
  §3  late-inserted shift      checked (17 hits / 10 groups → 2 unconfirmed, 8 refuted)
```

`[report-with-fix]`: the oracle fired on a production build, the route is cited, and the fix is a local change in the project's framework. `[report-flagged]`: one link is unproven (no build, no harness, a vendor's cost unmeasured), and the row names the run that settles it. The coverage block lists **all three** classes on every run: `checked (k hits → m findings)` only when the greps ran on a present lane; `N/A (<reason>)` when the stack has no such surface; `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

The verifier reads [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 83–90 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **`async`, `defer` and `type="module"` are not render-blocking** (§ 86). Judge such a third party by main-thread time, never by its presence.
- **An inline pre-paint bootstrap** (theme, locale, direction) is blocking on purpose and tiny; it prevents a flash. **Same-origin critical CSS** is meant to block. **A `media="print"` swap** does not block.
- **A bundler-inlined local `@import`** is not a chain; only raw-served CSS chains (1c) cost a round trip each.
- **`fixed` and `absolute` overlays do not shift content.** A `sticky` element does: it holds its place in flow until it sticks, so inserting one at the top pushes everything below it.
- **Shifts within 500 ms of discrete input are excluded** (`hadRecentInput`), and `transform` animations produce no layout-shift entries. Content inserted below the viewport moves nothing the user sees.
- **A banner rendered in the first commit is not late-inserted**, even if it is in flow. Only content that arrives after first paint (behind a query, a lazy chunk, a consent decision, a client-only boundary) is §3.
- **Dev-server numbers are meaningless** (§ 90). React StrictMode and HMR change timing and mount order.

## When to run

- On a diff that touches a document shell, a `<head>` tag, a `next/script` / `useScript` call, a script injected from code, a top-of-page banner or band, an embed or ad slot, or a `Suspense` / `ClientOnly` / `@defer` boundary above the fold.
- When `/bundle-perf` reaches rows L2, I3 or X1, or Lighthouse flags render-blocking resources, third-party cost or CLS.
- On every whole-repo frontend audit, reporting all three classes.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the `<file:line>`, the route whose first load it is on, the oracle, and the fix in the project's framework.
- Do not mark a row `[report-with-fix]` without an oracle that failed first on a production build. A dev-server or single-run Lighthouse number is not evidence (`precedents/performance.md` § 51, § 90).
- Do not assert a Lighthouse 12 id on a Lighthouse 13 runner or the reverse; print the version and the id used (§ Lighthouse ids by version).
- Do not print "critical path clean" without the class-coverage block, and do not use `rg -L` for files-without-match.
- Do not propose a fix that hides the symptom: `content-visibility` on the shifting band, removing the consent manager, or raising the CLS threshold.

## Related

- `bundle-analyze` (this pack) — bytes per route, legacy polyfills (§6) and dev-only code in the build (§7); the other half of the frontend load path.
- `font-optimization`, `image-optimization` §3, `lcp-audit` (this pack); `list-virtualization` detector 5 (ai-pattern) — the neighbouring load classes (§ Boundaries).
- `lighthouse-ci` (this pack) — the lab runner whose ids § Lighthouse ids by version selects.
- `/bundle-perf` and `web-vitals-field` (performance pack, when installed) — rank these rows across routes and read field CLS and LCP. Without that pack this skill is the only owner of these classes; say so in the report.
- security `xss-scan` (when installed) — third-party script integrity, CSP and consent ordering.
