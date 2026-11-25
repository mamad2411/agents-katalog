---
name: ssr-audit
description: SSR correctness — hydration mismatch, browser globals on the server, client-boundary leaks, double fetch, cross-request state; proved on a production build.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# ssr-audit

## Premise

A server-rendered page is rendered twice: once on the server into HTML, once in the browser to hydrate it. Every defect here comes from the two renders disagreeing or from the server doing something only a browser can. The client tree differs from the server HTML, so React regenerates it, Vue patches it, Angular skips it and the user sees a flash. A browser global throws on the server and the route answers 500. A server module or secret crosses into the client bundle. The data is fetched once by the server and again by the browser. A value one request stored at module scope is rendered to the next user.

**Every finding cites `<file:line>` + the pattern + the lane (framework and rendering mode) + the oracle that failed (or the test that would settle it) + the fix in the project's own server/client primitive.** "Might have hydration issues" is not a finding. A grep hit is a candidate. "No SSR issues" is never printed without the class-coverage block (§ Output).

**Detect statically, prove on a production build.** The proof is runtime: the console-hydration capture, a server render answering 200, the framework's build failing on the boundary, a request count across server and client, and a 60-request leak probe for module-scope state ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states: *Console hydration*, *Server render*, *Build gate*, *Server + client request count*, *Cross-request leak probe*; V107, V114–V117). A dev server is never the oracle: React reports hydration differently in development, and HMR keeps state alive. A candidate with no harness is **Unconfirmed** with its settling test written out ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

**No SSR, no audit.** A client-rendered app (a Vite or CRA SPA with `createRoot`) has no server render, so every § is `N/A (client-rendered)`. The pre-flight checks that first and stops. Measured below: ungated, the same greps return about 440 client-only lines on a real SPA.

## The rule

A candidate is a finding when all four hold:

1. **The code runs on the server.** A Server Component, a page or layout, a Client Component (it **does** render during SSR), a Nuxt `<script setup>` or plugin, a SvelteKit universal `load`, a React Router route module, an Angular component rendered by `@angular/ssr`. Code behind `ssr: false`, `<ClientOnly>`, `onMounted` / `onMount` / `useEffect` / `afterNextRender` does not.
2. **The two sides really differ, or the server really fails.** A value that is the same on both sides (an id from `useId()`, a timestamp produced once on the server and passed down) is not a mismatch.
3. **No framework control already handles it** — a framework-provided escape hatch, a `server-only` import, Nuxt `useState`, an Angular root service (one app instance per request), `AsyncLocalStorage`.
4. **The oracle fires, or would** — on a production build.

## Boundaries

- **The cost of a client boundary** (client bytes per route) → § Client-boundary cost below, ranked by `/bundle-perf` row T2 (performance pack, when installed). **TTFB and streaming** → `streaming-ssr` (this pack).
- **Secrets shipped in the client bundle** → security `xss-scan` §12, and **state serialised into a `<script>` tag** → its §6, when the security pack is installed. §3 here reports the boundary that lets the secret through and credits security. Without the security pack, report it here tagged `security-class (owner pack not installed)` (`refute-before-report.md` § 9). A private SSR page cached by a CDN → security `data-exposure-scan` §9.
- **A confirmed cross-user leak** (§4c) is a security incident too: with the security pack installed it goes through `finding-verification.md` to the security owner, deduped by `<file:line>`.
- **`useSearchParams()` with no `<Suspense>`** → `routing-scan` §7 (this pack). **Listeners and timers that leak in the browser** → `render-correctness-scan` §2. **Memory held by a Node SSR server's own caches** → performance `memory-growth-scan` §1 and §4, when installed.
- **Locale and time-zone presentation** outside the hydration question → `i18n-scan` §4 (this pack); §1e here keeps only the formatting that makes server and client disagree.
- **bfcache-blocking `unload` / `beforeunload` listeners** → `navigation-speed` (this pack).

## Adapt to the codebase — the SSR lanes

Read the framework **and its version** from the lockfile and the rendering mode from config (`output: 'export'`, Nuxt `ssr: false`, SvelteKit `export const ssr = false`, Angular `provideClientHydration`). Print the lanes you ran. A static export renders at build time: per-request values (cookies, headers, geo) do not exist there, and §4c does not apply. Key on API names, not majors: Next is at 16.3.8, Nuxt 4.5.2, SvelteKit 3.0.0, react-router 8.4.0 and Angular 22.2.1 (npm registry, 2026-10-05).

| Lane | Server / client boundary | Browser-only escape hatch | Data handed to the client (§4) | Hydration message family (§1 oracle) | Coverage |
|---|---|---|---|---|---|
| **Next App Router** 15–16 | Server Components by default; `'use client'` marks the boundary; `cookies()`, `headers()`, `params`, `searchParams` are **async** (Next 16 removed the synchronous form) | `useEffect`, `dynamic(…, { ssr: false })` inside a Client Component | RSC payload; `fetch` is not cached by default since 15 (`cache`, `next.revalidate`, `'use cache'`) | React 19 | §1–§4 + Client-boundary cost |
| **Next Pages Router** | `getServerSideProps` / `getStaticProps` server-only; the page renders on both | `useEffect` | props from the data function | React 19 | §1, §2, §4a |
| **Nuxt 4** | `.server.*` / `.client.*` suffixes; `<script setup>` runs on both | `onMounted`, `import.meta.client`, `<ClientOnly>` | `useFetch` / `useAsyncData` payload (auto-keyed by file and line); `useState` per request | Vue 3.5 (`data-allow-mismatch`) | §1, §2, §4 |
| **SvelteKit 2–3** | `+page.server.ts` server-only; `+page.ts` / `+layout.ts` run on **both** | `onMount`, `browser` from `$app/environment`, `$effect` | the `fetch` passed to `load` (inlined into the HTML) | Svelte 5 `hydration_mismatch` | §1, §2, §4 |
| **React Router 7–8 framework mode / Remix** | `loader` / `action` server-only; the module body and default export run on both | `useEffect`; `clientLoader` + `HydrateFallback` | loader data (turbo-stream keeps `Date` in RR ≥ 7) | React 19 | §1, §2, §4 |
| **Angular 20–22 SSR** | `isPlatformServer` / `isPlatformBrowser`; root services are per request | `afterNextRender`, `afterRender` | `provideClientHydration(withHttpTransferCache())`, `TransferState` | `NG0500`–`NG0509` | §1, §2, §4 |
| **Astro, Solid Start, Qwik City, Vike, custom `renderToString` / `hydrateRoot`** | per framework | per framework | per framework | the rendering library's | §1–§2 generic greps only — print `generic only` |

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; `CB` feeds § Client-boundary cost. Every `rg` names its path; files-without-match is `--files-without-match`, **never `-L`**, which in ripgrep means `--follow` — the old version of this skill told agents to use `grep -L`, agents translated it to `rg -L`, and two research passes in this batch were bitten by it. Commands live in this fenced block, never in a table cell, where a `\|` escape reaches ripgrep as a literal pipe. Any `rg` error on stderr (exit 2) is a failed grep, never zero hits.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|@builder\.io/qwik|astro)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,.vercel,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,scripts,tools,locales,i18n,generated,__generated__}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!ai/**' -g '!docs/**')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro}')
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*?'   # a lazy JSX tag body that survives `onClick={() => x}`
# 0. Lanes, versions and rendering mode. The SSR gate: an SSR framework, or a custom SSR entry. Neither → stop. The gate
#    is per root: ROOTS narrows to the roots that own one (an SPA or widget loader beside a Next app cannot hydrate).
rg -n --no-heading '"(next|nuxt|@sveltejs/kit|@remix-run/[\w-]+|react-router|@react-router/dev|@angular/ssr|@angular/core|astro|@solidjs/start|@builder\.io/qwik-city|vike|@tanstack/react-start|server-only)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --no-heading --pcre2 'output\s*:\s*["\x27]export["\x27]|\bssr\s*:\s*(?:true|false)\b|\bexport\s+const\s+(?:ssr|prerender)\s*=|provideClientHydration\([^)\n]*\)|\bhydrateRoot\(|renderToPipeableStream|renderToReadableStream|createSSRApp\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
SSR=( $( { rg -l --pcre2 '"(?:next|nuxt|@sveltejs/kit|@remix-run/[\w-]+|@react-router/dev|@angular/ssr|astro|@solidjs/start|@builder\.io/qwik-city|vike|@tanstack/react-start)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}" | xargs -r -n1 dirname
  rg -l --pcre2 '\bhydrateRoot\(|renderToPipeableStream|renderToReadableStream|createSSRApp\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | while IFS= read -r f; do printf '%s\n' "${ROOTS[@]}" | awk -v f="$f" 'index(f, $0 "/")==1 {print length($0) "\t" $0}' | sort -n | tail -1 | cut -f2; done; } | sort -u ) )
[ ${#SSR[@]} -gt 0 ] || { echo 'SSR gate: no SSR framework or SSR entry under ROOTS — every § is N/A (client-rendered)'; exit 0; }
ROOTS=( "${SSR[@]}" ); echo "SSR roots: ${ROOTS[*]}"
NEXT=$(rg -l '"next"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}")
# 1. Hydration nondeterminism: 1a an impure value in render (effect, handler and timer lines skipped), 1b an environment
#    branch in markup, 1c storage / matchMedia in initial state or a two-argument useSyncExternalStore, 1d invalid nesting
#    on one line, 1e formatting with the runtime's default locale or zone, 1f the suppression inventory, 1g a React Router
#    clientLoader that hydrates with no HydrateFallback.
rg -n --pcre2 '^(?!.*\b(?:useEffect|useLayoutEffect|onMounted|onMount|afterNextRender|afterRender|\$effect|addEventListener|setTimeout|setInterval|requestAnimationFrame)\s*\()(?!\s*(?:const|let)\s+(?:on|handle)[A-Z]\w*\s*=)(?!.*\bon[A-Z]\w*=\{)(?!\s*(?://|\*|/\*)).*?(?:\b(?:Date\.now|Math\.random|performance\.now|crypto\.randomUUID)\(\)|\bnew Date\(\)(?!\s*\.(?:getTime|valueOf|toISOString)\(\)\s*[-+<>]))' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'typeof\s+(?:window|document|navigator|localStorage)\s*[!=]==?\s*["\x27]undefined["\x27]\s*(?:\?|&&|\|\|)|\b(?:isServer|isClient|process\.client|process\.server|import\.meta\.(?:client|server|env\.SSR)|browser)\s*\?\s*<|v-if="!?\s*(?:isClient|isServer|process\.client|\$?isBrowser)|\{#if\s+!?browser\b|@if\s*\(\s*!?isBrowser' "${UI[@]}" -g '*.html' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^\s{0,4}(?:const|let|var)\s+[\w{}\s,]+=\s*(?:window|document|localStorage|sessionStorage|navigator|matchMedia)\b|useState\(\s*(?:\(\)\s*=>\s*)?(?:localStorage|sessionStorage|window|navigator|document)\.|\b(?:ref|shallowRef|signal|\$state)\(\s*(?:localStorage|sessionStorage|window|navigator)\.|useSyncExternalStore\(\s*[^,()]+,\s*[^,()]+\)' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '<p\b[^>]*>(?:(?!</p>).)*<(?:div|p|ul|ol|table|h[1-6]|section|form|blockquote|pre|hr)\b|<a\b[^>]*>(?:(?!</a>).)*<a\b|<button\b[^>]*>(?:(?!</button>).)*<(?:button|a|input|select|textarea)\b|<table\b[^>]*>\s*<tr\b|<form\b[^>]*>(?:(?!</form>).)*<form\b' "${UI[@]}" -g '*.html' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\.toLocale(?:Date|Time)?String\(\s*\)|\bnew\s+Intl\.(?:DateTimeFormat|NumberFormat|RelativeTimeFormat)\(\s*\)|\.toLocale(?:Date|Time)?String\(\s*undefined\b' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'suppressHydrationWarning|data-allow-mismatch|ngSkipHydration' "${UI[@]}" -g '*.html' "${X[@]}" "${ROOTS[@]}"
rg -l0 --pcre2 'clientLoader\.hydrate\s*=\s*true' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match 'HydrateFallback'
# 2. Browser globals on the server: 2a at module scope, 2b files that touch one with no guard anywhere, 2c a SvelteKit
#    universal load, 2d Angular DOM access in a file with no afterNextRender / isPlatformBrowser.
rg -n --pcre2 '^(?:export\s+)?(?:const|let|var)\s+[\w{}\s,:]+=\s*[^;\n]*?\b(?:window|document|localStorage|sessionStorage|navigator|location)\.\w|^(?:window|document|localStorage|sessionStorage|navigator)\.\w+' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l0 --pcre2 '\b(?:window|document|localStorage|sessionStorage|navigator)\.\w' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 'useEffect|useLayoutEffect|onMounted|onBeforeMount|\bonMount\b|\$effect|afterNextRender|afterRender|isPlatformBrowser|typeof\s+(?:window|document)|import\.meta\.client|process\.client|\bbrowser\b|ClientOnly|ssr\s*:\s*false|on[A-Z]\w*=\{|@click|\(click\)'
rg -n --pcre2 '\b(?:window|document|localStorage|sessionStorage|navigator)\.\w' -g '**/+{page,layout}.{ts,js}' "${X[@]}" "${ROOTS[@]}"
rg -l0 --pcre2 'nativeElement\.(?:innerHTML|appendChild|insertBefore|removeChild|focus)|\bdocument\.(?:querySelector\w*|getElementById|createElement|body)' -g '*.ts' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 '@angular/core' | xargs -0 -r rg --files-without-match 'afterNextRender|afterRender|isPlatformBrowser|PLATFORM_ID'
# 3. Server → client boundary: 3a a server module, Node built-in or non-public env read inside a 'use client' file,
#    3d `ssr: false` in a file that is not a Client Component. 3b and 3c are Next-only (inside the block below).
rg -l0 --pcre2 '^\s*["\x27]use client["\x27]' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -n -H --pcre2 'from\s+["\x27](?:server-only|(?:node:)?(?:fs|fs/promises|child_process|path|os|crypto)|@prisma/client|drizzle-orm[^"\x27]*|pg|mysql2(?:/promise)?|mongoose|redis|ioredis|[^"\x27]*/(?:server|db|database|prisma)(?:/[^"\x27]*)?)["\x27]|process\.env\.(?!NEXT_PUBLIC_|NODE_ENV\b)\w+'
rg -l0 --pcre2 '\bssr\s*:\s*false' -g '*.{tsx,jsx,ts,js}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 'next/dynamic' | xargs -0 -r rg --files-without-match --pcre2 '^\s*["\x27]use client["\x27]'
# 4. SSR data semantics: 4c Nuxt $fetch awaited in setup / an unkeyed useAsyncData, 4d a SvelteKit universal load that
#    does not take the event's fetch (or imports axios), 4e Angular hydration and transfer-cache wiring (context),
#    4f module-scope mutable state on a server path (in `.vue` / `.svelte`, only a module script — a Vue `<script>` with no
#    `setup`, a Svelte `<script module>` — since `<script setup>` / instance-script state is per component), 4g tenant or
#    user identity read from browser storage.
rg -n --pcre2 '^\s*(?:const|let)\s+[\w{}:\s,]+=\s*await\s+\$fetch\(|useAsyncData\(\s*(?:\(|async\b|function\b)' -g '*.{vue,ts,js}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'export\s+(?:async\s+function\s+load|const\s+load\s*(?::[^=]+)?=\s*async)\s*\(\s*(?!\{[^}]*\bfetch\b)|^import\s+axios\b' -g '**/+{page,layout}.{ts,js}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 'provideClientHydration|withHttpTransferCache|withNoHttpTransferCache|\bTransferState\b|withEventReplay|withIncrementalHydration' -g '*.ts' "${X[@]}" "${ROOTS[@]}"
F4='^(?:export\s+)?(?:let|var)\s+\w+|^(?:export\s+)?const\s+\w+\s*(?::\s*[^=\n]+)?=\s*(?:new\s+(?:Map|Set|WeakMap|Array)\b|\[\s*\]|\{\s*\}|(?:ref|reactive|shallowRef|writable|signal|atom|observable|proxy)\(|\$state\(|create(?:Store)?\s*(?:<[^>\n]*>)?\(\s*(?:\(\s*set|set\b))|\baxios\.defaults\.headers|\bi18n(?:ext)?\.changeLanguage\(|\bdayjs\.locale\(|\bmoment\.locale\('
rg -n --pcre2 "$F4" "${UI[@]}" -g '!*.{vue,svelte}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 "$F4" -g '*.{vue,svelte}' "${X[@]}" "${ROOTS[@]}" | while IFS= read -r h; do f=${h%%:*}; r=${h#*:}; awk -v n="${r%%:*}" '/^<script/ {m = (FILENAME ~ /\.vue$/ && $0 !~ /setup/) || $0 ~ /context="module"|[ ]module[ >]/} /^<\/script>/ {m=0} NR==n {exit !m}' "$f" && echo "$h"; done
rg -n --pcre2 '(?:localStorage|sessionStorage)\.getItem\(\s*["\x27`](?:tenant|org|organization|workspace|account|store|shop|merchant|company)\w*|document\.cookie' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
# CB. Client-boundary cost: CB1 'use client' files with no hook, handler, browser API or context; CB2 a client page,
#     layout or template (the boundary at the top of a route).
rg -l0 --pcre2 '^\s*["\x27]use client["\x27]' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\buse[A-Z]\w*\(|\buse\(|\bon[A-Z]\w*=\{|\b(?:window|document|navigator|localStorage|sessionStorage)\.|createContext\(|addEventListener|\bmotion\.|forwardRef'
rg -l --pcre2 '^\s*["\x27]use client["\x27]' -g '**/app/**/{layout,page,template}.{tsx,jsx}' "${X[@]}" "${ROOTS[@]}"
if [ -n "$NEXT" ]; then
# 3b a module under lib/ server/ services/ actions/ data/ (a path filter: two -g include globs are a union, not an
#    intersection) reading a non-public env var with no `import 'server-only'`; 3c a function or class instance passed as a prop
#    from a Server Component (a file under app/ with no 'use client'); 4a synchronous request APIs (removed in Next 16);
#    4b request APIs in a layout (the whole subtree turns dynamic).
rg -l --pcre2 'process\.env\.(?!NEXT_PUBLIC_|NODE_ENV\b)\w+' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 '/(?:lib|server|services|actions|data)/' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '^\s*import\s+["\x27]server-only["\x27]|^\s*["\x27]use server["\x27]'
rg --files-without-match --pcre2 '^\s*["\x27]use client["\x27]' -g '**/app/**/*.{tsx,jsx}' "${X[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -n -H -U --pcre2 "<[A-Z]\w*\b${TB}\s(?!action=|formAction=)\w+=\{\s*(?:\([^)]*\)\s*=>|\w+\s*=>|async\s|function\b|new\s+(?!Date\b)[A-Z])"
rg -n --pcre2 '\b(?:cookies|headers|draftMode)\(\)\s*\.(?!then)|\b(?:params|searchParams)\.(?!then\b)\w+' -g '**/app/**/{page,layout,route,default,template}.{tsx,jsx,ts,js}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\b(?:cookies|headers|connection|draftMode)\(\)' -g '**/app/**/layout.{tsx,jsx,ts,js}' "${X[@]}" "${ROOTS[@]}"
fi
```

A finding is a hit **plus** a read of where the code runs (server, client, both) **plus** the route that renders it **plus** the oracle. Three blind spots are structural:

- **Cross-component nesting** (`<Text as="p">` wrapping a `<Card>` that renders a `<div>`) is invisible to 1d, which sees one line. The development console names it (`In HTML, <div> cannot be a descendant of <p>`); `html-validate` over the server HTML of a production build finds it too.
- **A helper hides the impure call.** `formatRelative(date)` calling `Date.now()` two files away never matches 1a. The hydration capture across two time zones and two locales (§ Proof) does.
- **A store created at module scope in one file and filled per request in another.** 4f lists the declaration; read every writer of it before deciding it is constant.

**Measured** (2026-10-05). On this batch's research SSR fixtures plus a scratch Next 16 tree (positives and decoys per class): 1a 3/3 (the client decoy's `setNow(Date.now())` in an effect and `localStorage` in a handler: 0), 1b 1/1, 1c 2/2, 1d 4/4 (`<p><span>`: 0), 1e 2/2, 1f 2/2 (one is the `<time>` precedent), 2a 1/1, 2b 2 files (a Nuxt setup, a SvelteKit universal load), 2c 1/1 (`load({ fetch })`: 0), 3a 1/1, 3b 1/1 (the module importing `server-only`: 0), 3c 1/1 (`action={save}`: 0), 3d 1/1, 4a 2/2, 4b 1/1, 4c 2/2, 4d 2/2, 4f 5/5 (`const MAX`, `Object.freeze`, a fixed-locale `Intl`, Nuxt `useState`: 0), CB1 2/2 (a custom-hook consumer: 0), CB2 1/1. None of the six benchmark fixtures with UI code ships an SSR framework: the gate prints N/A on all of them. On a real React 19 + Vite SPA (about 4,300 TS/TSX files, read-only) the gate prints N/A in under a second. Run ungated, the same greps return about 440 lines there (1a 108, 1c 56, 2b 44, 4f 145, and 3c 62 because a SPA's `src/app/` matched the App Router glob), every one of them client-only. That is why the gate stops the script, and why 3b, 3c, 4a and 4b sit inside the Next block.

## The 3,000-hit path

1. **Intersect with the route table.** Keep hits in files a server render reaches (pages, layouts, route modules and what they import). A component under `ssr: false` / `<ClientOnly>` or a client-only route drops out with one read.
2. **Group** by (component, pattern). A shared formatter, a layout or a design-system wrapper with the defect is one group.
3. **Rank:** indexable and landing routes first (they are server-rendered for crawlers and first paint), then authenticated routes by traffic.
4. **Read the top 30 groups.**
5. **Prefer the runtime bulk oracle at scale.** One Playwright pass of the console-hydration capture over the route table, under two time zones and two locales, confirms or refutes every §1 group at once; one leak-probe run per server-rendered authenticated route settles §4f.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | Standard id | Default severity |
|---|---|---|---|
| 1 | Hydration nondeterminism: an impure value, an environment branch, storage or media in initial state, invalid nesting, default-locale formatting, suppression overused, a hydrating `clientLoader` with no fallback | — | high on a primary route (the tree is regenerated on the client); medium elsewhere; low for a dead suppression |
| 2 | Browser globals during server render | CWE-248 (uncaught exception) | high when the route answers 500; medium when an error page or fallback renders |
| 3 | Server → client boundary: a server module or secret in a client module, a non-serializable prop, `ssr: false` in a Server Component | CWE-200 when a secret crosses | blocker when a credential reaches the client (security's leak, credited); high for a build or runtime break; medium for server code with no secret |
| 4 | SSR data semantics: Next request APIs and caching, double fetch, unkeyed data, module-scope state shared across requests, identity from browser storage | CWE-488 (data exposed to the wrong session) for 4f/4g | blocker when 4f or 4g holds user or tenant data; high for a Next 16 synchronous request API; medium for double fetch or unintended dynamic rendering |

### 1. Hydration nondeterminism

```
BAD:   <span>{Date.now()}</span>  ·  const id = Math.random()  ·  <div>{new Date().toLocaleTimeString()}</div>
       {typeof window === 'undefined' ? <Skeleton/> : <Chart/>}     ·  {#if browser}<Chart/>{/if}
       const [theme] = useState(() => localStorage.getItem('theme'))   ·  useSyncExternalStore(subscribe, getSnapshot)
       <p className="lead"><div>…</div></p>                            ·  <span suppressHydrationWarning>{user.name}</span>
GOOD:  useId() for ids; the time produced once on the server and passed down, or set in an effect after mount
       render the same placeholder on both sides, then switch in useEffect / onMounted / $effect
       theme from a cookie read on the server; useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot)
       Intl.DateTimeFormat(locale, { timeZone }) with the locale and zone taken from the request on both sides
```
**Read the code:** Does the line run during render on both sides, or inside an effect, a handler or a Server Component that is never hydrated? Is the value the same on both sides (a server-produced timestamp passed as a prop)? For 1e, are the locale and zone explicit and identical on server and client? For 1f, is the suppression on a leaf whose text is genuinely unknowable on one side (a relative time, a theme attribute on `<html>`), or on an element with children? React's suppression is one level deep; `ngSkipHydration` drops the whole subtree to client rendering. **Finding when** the two renders differ for a real request. **Proof:** console hydration (`proof-oracles.md` § "Console hydration", variant V107) — production build, `page.on('console')` and `page.on('pageerror')`, under `timezoneId: 'Pacific/Kiritimati'` and `locale: 'ar-SA'` as well as UTC/en-US, in a clean browser profile. The message families, read from the shipped sources on 2026-10-05:

```ts
const HYDRATION = /Hydration failed because|A tree hydrated but some attributes|cannot be a (?:child|descendant) of|error while hydrating|Hydration (?:node|text|children|class|style|attribute) mismatch|Hydration completed but contains mismatches|hydration_mismatch|hydration_attribute_changed|hydration_html_changed|NG050\d|Minified React error #(?:418|422|423)\b/;
```
React 19.3 production builds report minified codes (#418 the mismatch; #422 and #423 recovered by client rendering; #425 is React 18 only) through `hydrateRoot`'s `onRecoverableError`. Vue production builds print details only with `__VUE_PROD_HYDRATION_MISMATCH_DETAILS__: true`; Vue 3.5 adds the `data-allow-mismatch` opt-out. Angular: `NG0500` node mismatch … `NG0505` no hydration info (the server did not call `provideClientHydration`), `NG0506` the app never became stable, `NG0507` the HTML was altered after SSR (a CDN stripped comment nodes). For a dead suppression (1f), remove it in a scratch build and run the capture: silence means it can go; a message means the divergence is real.

### 2. Browser globals during server render

```
BAD:   const width = window.innerWidth;                       // module scope: throws on the server
       export async function load() { return { w: window.innerWidth }; }   // SvelteKit +page.ts runs on the server too
       this.el.nativeElement.focus()  in ngOnInit             // Angular SSR has no DOM
       window.addEventListener('resize', …)  at the top of a Nuxt plugin
GOOD:  onMounted(() => { const width = window.innerWidth; })  ·  useEffect(…)  ·  onMount(…)
       move the read into +page.server.ts, or guard with `browser`; afterNextRender(() => this.el.nativeElement.focus())
       export default defineNuxtPlugin(() => { if (import.meta.client) window.addEventListener(…) })
```
**Read the code:** Where does the line run — module top, the render body, a `load` both sides run, a lifecycle the server skips? A React Router route module's body and default export run on the server; its `loader` is server-only (a browser API there is a different bug: it always throws). A guard **outside** render is the fix; the same guard **inside** render is §1's branch. **Finding when** the access executes during a server render. **Proof:** server render — `next build && next start` (or the lane's production server), then `curl -s -o /dev/null -w '%{http_code}'` on the route returns 200 and the server log holds no `ReferenceError: window is not defined` (or `document`, `localStorage`, `navigator`); it fails before the fix.

### 3. Server → client boundary

```
BAD:   'use client'; import { db } from '@/lib/db'                     // the server module ships to the browser
       <OrderList onSelect={(o) => track(o)} fmt={new Intl.NumberFormat()} />   // from a Server Component
       const Map = dynamic(() => import('./Map'), { ssr: false })     // in a Server Component: build error
       lib/payments.ts reads process.env.STRIPE_SECRET_KEY with no import 'server-only'
GOOD:  call a Server Action or a route handler from the client; pass plain data, not functions or class instances
       move dynamic(…, { ssr: false }) into a 'use client' wrapper; start every server module with import 'server-only'
```
**Read the code:** Does the imported module read a secret, open a connection or use a Node built-in? Is the prop a Server Action (`'use server'`, allowed) or a plain function (not)? `Date`, `Map`, `Set`, `BigInt`, typed arrays and promises are serialisable by the RSC protocol. Is the module reachable from any client module, transitively? **Finding when** server-only code or a non-serialisable value crosses the boundary. **Proof:** build gate — add `import 'server-only'` to the server module and `next build` fails with `This module cannot be imported from a Client Component module.`; a non-serialisable prop fails at request time with `Functions cannot be passed directly to Client Components unless you explicitly expose it by marking it with "use server"` or `Only plain objects, and a few built-ins, can be passed to Client Components from Server Components.`; `ssr: false` fails the build with `` `ssr: false` is not allowed with `next/dynamic` in Server Components. Please move it into a Client Component. `` (Next 16.3.8 strings). A secret found in the built client output is security `xss-scan` §12's 12d proof.

### 4. SSR data semantics

```
BAD:   const data = await $fetch('/api/x')            // Nuxt <script setup>: fetched by the server, then again by the browser
       export async function load() { const r = await fetch('/api/items') }   // SvelteKit +page.ts without the event's fetch
       const { id } = params; cookies().get('t')      // Next 16: synchronous request APIs were removed
       let currentUser = null; export const cache = new Map(); export const useCart = create((set) => …)   // module scope on the server
       const tenant = localStorage.getItem('tenant')   // undefined on the server: the wrong tenant renders
GOOD:  const { data } = await useFetch('/api/x')  ·  export async function load({ fetch }) { … }
       const { id } = await params; (await cookies()).get('t')
       per-request state: Nuxt useState, Pinia via @pinia/nuxt, SvelteKit event.locals / context, a store created per request
       (React context provider), AsyncLocalStorage; the tenant from the request (host header, server session)
```
**Read the code:** 4a/4b — is the route meant to be static, and does a `cookies()` in a layout turn the whole subtree dynamic (the build's route table shows `ƒ` instead of `○`)? Next ≥ 15 does not cache `fetch` by default: is a cache or `revalidate` intended? 4c — Nuxt auto-keys `useAsyncData` by file and line, so an unkeyed call is a finding only in a composable reused with different inputs. 4e — with `@angular/ssr` present, is `provideClientHydration()` there, and does it keep the HTTP transfer cache (on by default; `withNoHttpTransferCache` turns it off)? 4f — is the module value written per request (a user, a token, a cart, `axios.defaults.headers.Authorization`, a server-side `i18next.changeLanguage`, a global dayjs locale), or a frozen constant, a fixed-locale formatter, a lookup table? A Client Component **does** render on the server, so its module scope is shared too. 4g — is the identity resolved from the request on the server? **Finding when** a request's data reaches another request, or one navigation fetches twice. **Proof:** for double fetch, a request count across server and client (the API's access log for the server render plus `page.on('request')` after hydration — the counter shape is `proof-oracles.md` § "Request count"); for 4a, the build; for 4f/4g, the cross-request leak probe (§ Proof).

### Client-boundary cost (React Server Components)

React and Next App Router specific; bundle-perf row T2 cites this heading. Every `"use client"` directive marks a hydration boundary: everything from that file down ships JavaScript and hydrates. An unjustified directive is wasted client JavaScript; one placed too high drags server-safe children into the bundle.

```
BAD:
"use client";                         // file has no state/effect/event/browser API
export function Price({ amount }) { return <span>{format(amount)}</span>; }

GOOD:
export function Price({ amount }) { return <span>{format(amount)}</span>; }  // server component, ships 0 JS
```

Detectors:

- **Detector 1 — unjustified directive.** Grep CB1: `'use client'` files with no hook call, event handler, browser API, `createContext` or `forwardRef` (`--files-without-match`, never `-L`). Each hit is a candidate to DELETE the directive so the component renders on the server.
- **Detector 2 — boundary too high.** Grep CB2 lists client pages, layouts and templates; for any `"use client"` file importing large server-safe children, push the directive DOWN to the interactive leaf and pass the server-rendered subtree through `children`.
- **Detector 3 — server-only leak (BLOCKER).** Now §3 above (grep 3a), proved by the build gate.
- **False positive:** a component consuming client Context still needs the directive. CB1 keeps any file that calls a hook, so a `useContext` / `use(Context)` consumer is never listed; a file that only re-exports a client library component may still need it (read the library).
- **Halt:** never strip a directive without the CB1 command's output showing zero hooks, handlers and browser APIs in that file, and a build that passes after the change.

Output per finding: `file:line` of the directive + why it is unjustified + the demotion or push-down fix + the client bytes per route before and after (`proof-oracles.md` § "Bytes per route", V48), measured, never estimated.

## Proof

Each oracle is in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states, under the heading of the same name:

1. **Console hydration** (§1, V107) — above.
2. **Server render** (§2, V114) — the production server answers the route 200 with no `ReferenceError` for a browser global in its log.
3. **Build gate** (§3, §4a; V115, V116) — the framework's production build fails on the violation before the fix and passes after it; the message is quoted.
4. **Server + client request count** (§4 double fetch, V116) — each URL fetched once for one navigation.
5. **Cross-request leak probe** (§4f, §4g; V117) — two signed-in sessions with unique page markers plus anonymous requests, 60 interleaved and concurrent against the production server. Any leak confirms the class; zero of 60 keeps the row `[report-flagged]` until the deterministic two-request test fails.

Whole-class variants: a value in render, in a custom hook, in a `useState` initialiser, in `useMemo`, in a Vue `computed`, in Svelte `{#if browser}`, in Angular `@if (isBrowser)`; nesting across components; a suppression moved one level up; for 4f, `let`, a `Map`/`Set` cache, module-scope `ref` / `reactive` / `writable` / signal / `$state`, a Zustand or Pinia store at module scope, `axios.defaults.headers`, a server-side `changeLanguage`, a global dayjs locale.

## Output

```
ssr-audit — lanes: next 16.3.8 App Router (apps/shop/package.json), server-only 0.0.1; nuxt, sveltekit, angular absent
Rendering: dynamic (no output: 'export'); coverage: §1–§4 + Client-boundary cost

Findings: 2 · Unconfirmed: 1

1. apps/shop/lib/session-cache.ts:3                                   [report-with-fix]   blocker
   §4f module-scope state — `export const sessions = new Map()` written in getUser() per request and read by the
   header Server Component. Proof: leak probe — 60 interleaved requests, 4 anonymous bodies held ZZ_U1_MARK (fails).
   Fix: React cache() per request or AsyncLocalStorage; delete the module Map. Also routed to security (cross-user).
2. apps/shop/app/orders/[id]/page.tsx:2                               [report-with-fix]   high
   §4a synchronous params on Next 16 — `const id = params.id`. Proof: next build fails (type error under next typegen).
   Fix: const { id } = await params.
3. apps/shop/components/RelativeTime.tsx:9                            [report-flagged]    high
   §1a Date.now() in render of a Client Component on /orders. Unproven: no Playwright harness. Settling test: the
   console-hydration capture on /orders under Pacific/Kiritimati + ar-SA. Fix: render the server timestamp; update in an effect.

Verification: 11 candidates → 2 findings · 1 unconfirmed · 2 hardening · 6 refuted

Class coverage:
  §1  hydration nondeterminism   checked (9 hits → 1 unconfirmed; 2 hardening: <time suppressHydrationWarning>, the next-themes <html>)
  §2  browser globals on server  checked (3 hits → 0 findings; all inside useEffect or onMounted)
  §3  server → client boundary   checked (1 hit → 0 findings: the import is a type-only import)
  §4  SSR data semantics         checked (4 hits → 2 findings)
  CB  client-boundary cost       checked (CB1 0 files; CB2 1 client layout → 0 findings: it only renders the app's context providers)
```

`[report-with-fix]`: the code runs on the server for a cited route, the oracle failed on a production build, and the fix is local. `[report-flagged]`: one link is unproven (no harness, a helper not followed, a lane read but not run), with the settling test named. The coverage block lists **all four** classes plus `CB` on every run: `checked (k hits → m findings)` only when the greps ran on a present lane; `N/A (<reason>)` — `client-rendered`, `no RSC framework` for CB, `static export` for §4f/§4g; `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (§ 43–45) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this skill meets most:

- **A browser API inside a client-only lifecycle is correct** — `useEffect`, `onMounted`, `onMount`, `$effect`, `afterNextRender`. The verdict says why it was dismissed (`precedents/ui.md` § 43).
- **A guard outside render is the fix; inside render it is the bug.** `typeof window !== 'undefined'` in an effect or handler is fine; branching the returned markup on it is §1b.
- **Deliberate suppression** — `<html suppressHydrationWarning>` for a theme script, `suppressHydrationWarning` on a `<time>` leaf, Vue `data-allow-mismatch="text"` on a relative time — is a scoped decision (`precedents/ui.md` § 44). On an element with children it is a finding.
- **Server Components are not hydrated.** `Date.now()` in a Server Component renders once; only Client Components hydrate.
- **A hydration error that disappears in a clean profile** came from a browser extension (`precedents/ui.md` § 45).
- **Per-request by construction:** Angular root services (a new app per request), Nuxt `useState`, SvelteKit `event.locals` and context, `AsyncLocalStorage`, React `cache()`. Frozen constants, fixed-locale `Intl` formatters and lookup tables at module scope are not state.
- **Static export changes the rules** — per-request values do not exist at build time; extract the rendering mode before grading §4.
- **Dev-server output is not evidence.** Hydration messages, request counts and memory read on a dev server do not count.

## When to run

- Before merging a change to a page, layout, route module, Server Component boundary, plugin or composable on an SSR app.
- On every whole-repo frontend audit with an SSR lane present; it prints N/A and stops on a client-rendered app.
- When production shows a hydration error in RUM (`onRecoverableError` forwarded), a 500 on first load that a client navigation does not reproduce, or one user's data on another user's page.

## Halt conditions

- Do not report a high or blocker row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (and `finding-verification.md` for a cross-user leak when the security pack is installed). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without `<file:line>`, the lane, the route that renders it, and a concrete fix in the project's primitive. "Might cause hydration issues" is not a finding.
- Do not dismiss a hit without saying where the code runs and why that clears it.
- Do not use `rg -L` (it is `--follow`), and do not put a runnable `rg` in a table cell.
- Do not report zero findings without the class-coverage block and the lanes printed. A lane with no boundary-specific greps (Astro, Solid Start, Qwik, a custom server) reads `generic only`, never a pass.
- Do not mark a finding `[report-with-fix]` without the oracle failing on a production build. A fix that adds `suppressHydrationWarning`, `ngSkipHydration` or `ssr: false` to silence a real divergence is rejected.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `streaming-ssr` — the speed sibling: this skill asks "does the server render match the client, and is it safe?"; that one asks "why is the first byte late?".
- `render-correctness-scan` — the client side of the same render: effects, keys, reactivity, SPA memory growth.
- `ssr-safety.md` (ai-pattern) — the per-framework client-guard primitives and closure verbs; fix wording comes from there.
- `visual-check` — a hydration failure the greps cannot see often shows as a blank or duplicated region in a real render.
- `navigation-speed` — owns bfcache and `unload` listeners.
- `routing-scan` §7 — `useSearchParams()` without `<Suspense>`.
- `/bundle-perf` row T2 (performance pack, when installed) — ranks § Client-boundary cost by client bytes per route.
- security `xss-scan` §6 and §12 (when installed) — serialised state and bundle secrets.
- `error-boundaries.md` (ai-pattern) — a hydration throw surfaces through a boundary; the boundary contains it, never fixes it.
- `.claude/rules/frontend-principles.md` — the SSR-safety MUSTs this scan enforces.
