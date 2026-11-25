---
name: streaming-ssr
description: SSR speed — routes that block TTFB on the slowest await; stream the shell behind Suspense / await boundaries. Correctness is ssr-audit.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# streaming-ssr

## Premise

Slow SSR blocks TTFB on the slowest thing the page awaits. If a route `await`s a 600ms query before returning any HTML, the user stares at a white screen for 600ms even though the header, nav, and layout were ready instantly. The fix is almost never "make the query faster" first — it's **stream the shell now, stream the slow subtree later** behind a boundary, so above-the-fold paints immediately and the slow region fills in.

`ssr-audit` checks SSR *correctness* (hydration mismatches). This skill checks SSR *speed*: it turns the open question "is hydration streaming?" into a real detector + fix. `bundle-perf` *(performance pack, when co-installed)* is where that question is normally raised; when that pack is absent nothing else in the project asks it, which is precisely why this skill has its own TTFB trigger below rather than waiting to be handed a finding. Every finding cites the blocking call at `<file:line>` + its observed/measured latency + the proposed boundary + the expected TTFB delta. A streaming recommendation without the cited blocking call is a halt.

**Closure verbs** — exactly one per finding. This skill emits `report-with-fix` (a boundary that is a mechanical edit — wrap the subtree, un-await the loader field, add `loading.tsx`), `report-flagged` (detector 5: enabling Cache Components / partial prerendering is a config change plus a boundary map, so it names the decision and the subtrees rather than editing), `dismiss` (slowest call under ~100ms, or all data above the fold — the § gotchas carve-out), and `halt-handoff` (upstream endpoint latency → the backend owner; hydration mismatch → `ssr-audit`; LCP priority → `lcp-audit`).

## Adapt to the codebase

Mirror the streaming primitive the project already has; never introduce a second one. Detect the framework + its render entry before proposing a boundary.

| Stack | Streaming boundary primitive | Segment-level shell | Un-awaited / deferred data |
|---|---|---|---|
| **Next (App Router)** | `<Suspense fallback>` around the slow subtree | `loading.tsx` beside the segment (auto-wraps in Suspense) | pass the un-awaited promise down; `use()` in the child |
| **Nuxt** | `<Suspense>` / `<NuxtIsland>` / `.server.vue` | `<NuxtLoadingIndicator>` + page-level fallback | `useLazyFetch` / `useFetch(url, { lazy: true })` |
| **SvelteKit** | `{#await}` in `+page.svelte` | `+layout.svelte` shell renders first | return an **un-awaited** promise from `load` |
| **Remix / React Router** | `<Await>` + `<Suspense fallback>` | the parent route's layout renders while the child's promise streams. `HydrateFallback` is **not** a stream shell: it is what SSR renders for a route whose `clientLoader.hydrate` runs only in the browser | un-awaited promise in the loader return |
| **Angular (SSR)** | none: Angular SSR does not stream a deferred region into the same response. On the server a `@defer` block renders its `@placeholder` (or nothing) and its triggers never fire; with incremental hydration and `hydrate` triggers it renders the main content instead (angular.dev, *Deferred loading with @defer*, fetched 2026-10-05) | route-level shell component | the TTFB lever is a resolver or `await` that blocks render; move non-critical data to the client behind `@defer` + `@placeholder`, and report the trade (content absent from the server HTML) |
| **Astro** | `server:defer` island + slot fallback | static shell is the default | island resolves after the shell flushes |
| **Plain React SSR** | `<Suspense>` + `renderToPipeableStream` (`onShellReady`) | shell = everything outside the boundary | promise passed to a `use()` child |

If the render entry (`renderToString` vs `renderToPipeableStream` vs the framework's own server) is not extracted, halt: the fix differs per entry and a boundary added to a buffering renderer changes nothing.

## Pre-flight greps

Run as **one** script from the repo root; shell state does not survive between tool calls. Grep **N** feeds detector **§N**. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. Files-without-match is `--files-without-match`, never `-L` (that is `--follow` in ripgrep). An `rg` error on stderr (exit 2) is a failed grep, not zero hits.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|next|nuxt)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!*.{md,mdx,snap,map,lock}' -g '!ai/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#|<!--|\{/\*)')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
PAGES=(-g '**/app/**/page.{tsx,jsx,ts,js}' -g '**/app/**/layout.{tsx,jsx,ts,js}')
# 0. Lanes, majors and the render entry: Next / Nuxt / SvelteKit / React Router / Remix / Angular SSR / Astro, and a hand-rolled server.
rg -n --no-heading '"(next|nuxt|@sveltejs/kit|react-router|@react-router/dev|@remix-run/react|@angular/ssr|@angular/platform-server|astro|react-dom)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
# 1. Whole-page await: an async App Router page/layout that awaits and imports no Suspense (1a); a Remix/RR route module whose loader file awaits twice or more (1b, file-level: read the loader).
rg -l --pcre2 '^export\s+default\s+async\s+function' "${PAGES[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg -l '\bawait\b' | xargs -r rg --files-without-match '\bSuspense\b'
rg -l --pcre2 '^export\s+(?:async\s+)?function\s+loader\b|^export\s+const\s+loader\s*=' -g '**/{app,src}/**/routes/**/*.{tsx,jsx,ts,js}' -g '**/app/root.{tsx,jsx}' "${X[@]}" "${ROOTS[@]}" | xargs -r rg -c '\bawait\b' | awk -F: '$NF >= 2'
# 2. App Router segments whose page awaits and that have no loading.* beside them (a sibling or ancestor loading file also covers it — read).
rg -l --pcre2 '\bawait\b' -g '**/app/**/page.{tsx,jsx,ts,js}' "${X[@]}" "${ROOTS[@]}" | while read -r f; do d=$(dirname "$f"); ls "$d"/loading.* >/dev/null 2>&1 || echo "$f"; done
# 3. Awaited-everything loaders: SvelteKit load returning two awaited fields (3a); Nuxt pages awaiting useFetch/useAsyncData (3b; non-critical data wants lazy).
rg -n -U --no-heading --pcre2 'return\s*\{[^}]*\bawait\b[^}]*\bawait\b' -g '**/+{page,layout}{.server,}.{ts,js}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bawait\s+(?:useFetch|useAsyncData)\s*\(' -g '**/{pages,app/pages,layouts,app/layouts}/**/*.vue' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4. A buffering React render entry in server code.
rg -n --no-heading --pcre2 '\brenderToString\s*\(|\brenderToStaticMarkup\s*\(' -g '*.{ts,tsx,js,jsx,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5. Partial-prerender candidates and removed APIs: force-dynamic routes (5a); experimental_ppr / ppr config, removed in Next 16 (5b); cacheComponents on (5c).
rg -n --no-heading --pcre2 '\bdynamic\s*=\s*["\x27]force-dynamic["\x27]' "${PAGES[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bexperimental_ppr\b|\bppr\s*:' -g '*.{ts,tsx,js,jsx,mjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bcacheComponents\s*:\s*true|["\x27]use cache["\x27]' -g '*.{ts,tsx,js,jsx,mjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A hit is a candidate; the finding needs the blocking call's measured latency (Premise). Two blind spots are structural:

- **The slow call hides behind a helper.** `await getProduct()` is one line in the page and three sequential queries in the service. Greps 1 and 3 find the await; the read follows it to the slowest call and the latency comes from the server timing or a log.
- **Grep 2 checks the sibling only.** A `loading.*` in an ancestor segment also wraps the page; read the tree before calling a segment uncovered.

**Measured** (2026-10-05, read-only). Scratch fixture: an awaiting App Router page with no Suspense and no `loading.tsx`, a SvelteKit load returning two awaited fields, a two-await loader, a `renderToString` entry and a `force-dynamic` route, all hit; the page with `<Suspense>` and a sibling `loading.tsx` stays out of 1 and 2. Benchmark fixtures: 0 on greps 1–5 (none ships an SSR route). Real repos: a Nuxt 4 storefront (3b: 1 policy page awaiting `useAsyncData` at the top of setup), a Vue 3 + Vite SPA and an Angular 19 template (0 everywhere: no SSR entry, so every class prints N/A). The first loader grep was a single multi-line PCRE2 pattern that `rg` refused to compile ("regular expression is too large"), which reads as zero hits; it is now file-level.

## The 3,000-hit path

1. **Intersect with the route table** and the server timing: a route whose TTFB is under ~200 ms is dismissed whatever it awaits.
2. **Group** by (layout or loader, pattern). A root layout that awaits a session lookup is one finding for every route under it.
3. **Rank** by route traffic, then by measured TTFB.
4. **Read the top 30 groups.** Ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them, never `checked`.

## Scans for

### 1. Whole-page await before first byte

A page/route that awaits a slow call at the top, with nothing streamed, blocks the entire document.

```
BAD (Next App Router):
export default async function Page() {
  const reviews = await getReviews(id);   // 600ms — blocks the whole shell
  return <><Header/><Product/><Reviews data={reviews}/></>;
}

GOOD:
export default async function Page() {
  return <><Header/><Product/>
    <Suspense fallback={<ReviewsSkeleton/>}>
      <Reviews id={id} />     {/* awaits inside; streams in when ready */}
    </Suspense></>;
}
```

Grep: a top-level `await` on a `fetch(`/`db.`/known-slow call inside a `page.tsx` / `+page.server` `load` / route component, with **no** `<Suspense>` (React/Vue) / `{#await}` (Svelte) / `<Await>` (Remix/RR) wrapping the slow subtree.

### 2. Missing `loading.tsx` on a slow App-Router segment

Next App Router auto-wraps a segment in `<Suspense>` when a sibling `loading.tsx` exists — instant streamed fallback for free.

```
BAD:  app/products/page.tsx awaits a slow fetch, no app/products/loading.tsx
GOOD: app/products/loading.tsx → streamed skeleton; page streams in behind it
```

Flag route dirs with a slow server fetch and no `loading.tsx`.

### 3. Awaited-everything in SvelteKit / Nuxt loaders

```
BAD (SvelteKit load):  return { post: await getPost(), comments: await getComments() };
GOOD:                   return { post: await getPost(), comments: getComments() };  // un-awaited → streamed
                        // consume in +page.svelte: {#await data.comments}…{:then c}…{/await}
```

For Nuxt: a static-but-slow subtree that ships client JS unnecessarily → render it as a server component (`.server.vue` / `<NuxtIsland>`); non-critical data → `useLazyFetch` / `useFetch(url, { lazy: true })` so it doesn't block navigation.

### 4. Blocking `renderToString` in a custom SSR server

```
BAD:   const html = renderToString(<App/>);  res.send(html);   // buffers entire tree
GOOD (Node):  renderToPipeableStream(<App/>, { onShellReady() { res.statusCode=200; pipe(res); } });
GOOD (edge/web): renderToReadableStream(<App/>, { … });        // returns a stream
```

`renderToString` is the blocking baseline — flag it in any hand-rolled SSR entry; propose the streaming variant (`onShellReady` flushes the shell, `onAllReady` for crawlers/SSG).

### 5. Cache Components / partial-prerender candidate (Next 16+)

A route marked fully dynamic (`export const dynamic = 'force-dynamic'`) that has a large static header/footer is a partial-prerender candidate: the static shell prerenders + serves instantly, and only the dynamic holes (anything reading `cookies()` / `headers()` / `searchParams`) stream.

**Read the installed major before emitting anything — this skill runs against repos on both, and the enable line is not the same line:**

```
Next 16+ : cacheComponents: true in next.config.ts, then mark the cacheable shell with the
           "use cache" directive; wrap each dynamic hole in <Suspense>.
Next 15  : export const experimental_ppr = true (+ experimental: { ppr: 'incremental' }).
           BOTH were REMOVED in Next 16 — the config flag and the route-level export.
           Emitting either against a 16+ project produces a build failure, not a warning.
```

Source: the Next.js 16 release notes list `experimental.ppr` and `export const experimental_ppr` in the Removals table, replaced by the Cache Components model (nextjs.org/blog/next-16, published 2025-10-21).

Flag `dynamic = 'force-dynamic'` routes with a large static region as `report-flagged` — the enable is a config + boundary decision, not a mechanical edit.

## Output

```
streaming-ssr audit — <route set>

Findings: 2

1. app/products/[id]/page.tsx:6                        TTFB ~640ms    [report-with-fix]
   Top-level `await getReviews(id)` blocks the shell on a 600ms query.
   Boundary: wrap <Reviews/> in <Suspense fallback={<ReviewsSkeleton/>}>;
             add app/products/[id]/loading.tsx for the segment shell.
   Expected: TTFB 640ms → ~90ms (shell), reviews stream in at ~640ms.

2. src/routes/feed/+page.server.ts:12                  TTFB ~480ms    [report-with-fix]
   `comments: await getComments()` awaited alongside critical `post`.
   Boundary: return un-awaited `comments: getComments()`; consume via {#await}.
   Expected: TTFB blocked on getPost() only (~120ms); comments stream.

Verification: 6 candidates → 2 findings · 1 unconfirmed · 3 refuted

Class coverage:
  §1  whole-page await          checked (3 files → 1 finding)
  §2  no loading.tsx            checked (2 segments → folded into finding 1; 1 covered by an ancestor)
  §3  awaited-everything loader checked (1 hit → 1 finding)
  §4  renderToString entry      N/A (framework server; no hand-rolled entry)
  §5  Cache Components          checked (1 force-dynamic route → 1 unconfirmed: report-flagged, needs the boundary map)
```

`[report-with-fix]`: the blocking call is cited with a measured latency and the boundary is a mechanical edit. `[report-flagged]`: §5, or any row whose latency was not measured; the row names the run that settles it. The coverage block lists **all five** classes on every run: `checked (k hits → m findings)`, `N/A (<reason>)`, or `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

- **Above-the-fold critical data stays in the shell.** Streaming the hero/LCP content defers LCP — only stream below-the-fold / secondary regions.
- **Auth + redirect decisions must resolve before the shell flushes.** You cannot stream a 200 shell and then decide the user should have been redirected — resolve auth synchronously first.
- Streaming adds boundary overhead; a route whose slowest call is <100ms or whose data is all above-the-fold gains little → `dismiss`.
- A streamed boundary needs a layout-stable fallback (reserve dimensions) or you trade TTFB for CLS — coordinate with `lcp-audit` / `navigation-speed`.
- TTFB dominated by *backend endpoint latency* (the API itself is slow) is not a streaming problem — streaming hides server think-time of the page's own render, it doesn't speed up a slow upstream. Route it to `profile-perf` *(performance pack, when co-installed)*; absent that pack, hand the endpoint to the backend owner with the measured latency attached and record `upstream latency: routed out of scope` — do not propose a boundary that cannot help.

## When to run

- Any SSR route with TTFB > 200ms, or where one query measurably dominates the render.
- After `bundle-perf` / `web-vitals-field` *(performance pack, when co-installed)* attributes LCP to a high `timeToFirstByte` on an SSR route. Absent that pack, the trigger is the route's own measured TTFB above.
- When adding a slow data dependency (reviews, recommendations, related items) to an existing fast route.

## Halt conditions

- Halt on any streaming recommendation that doesn't cite the blocking call at `<file:line>` + its observed/measured latency.
- Halt if the proposed boundary would stream above-the-fold / LCP content (defers LCP) — re-scope to secondary regions.
- Halt if a redirect/auth gate sits behind the proposed streamed shell — resolve it before the flush.
- Halt if "enable partial prerendering / Cache Components" is proposed without naming which subtrees become the dynamic (Suspense-wrapped) holes.
- Halt before reporting any candidate that has not been through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) (§1 restate … §9) and [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 90 (dev-server numbers are meaningless). **Proof:** server TTFB (`server-response-time`, median of 5 runs) and the time the shell's first byte arrives on a production build, before and after; the streamed region must still render ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Lighthouse median").
- Halt if a streaming fix is proposed for Angular SSR — it has no in-response streaming; the trade is client-deferred content, stated as such.
- Halt if the enable line is emitted without reading the framework major from `package.json` — `experimental_ppr` against Next 16+ is a removed API, and a reference that emits a deleted API is worse than no reference.

## Related

- `ssr-audit` — the correctness sibling: it owns hydration mismatches, this skill owns TTFB. A route that streams a mismatched shell is that skill's finding, not this one's.
- `lcp-audit` — a streamed boundary must never contain the LCP element, and its fallback must reserve the box; hand LCP-priority findings there.
- `navigation-speed` — owns prefetch / bfcache / instant-loading on the *client* navigation path; this skill owns the server's first byte.
- `rendering-strategy.md` (ai-pattern) — decides whether the route is server-rendered at all; this skill only places the boundary inside a route that already is.
- `code-splitting.md` (ai-pattern) — the JS axis of the same page; a streamed region whose chunk is eagerly bundled still blocks the main thread.
- `.claude/rules/frontend-principles.md` — the "server-rendered routes MUST stream the shell" MUST this skill enforces.
- Cross-pack (`performance`, when co-installed): `web-vitals-field` measures whether the TTFB win actually reached users. Absent that pack, report the before/after server TTFB only and label it `lab only — field impact unmeasured`; never claim a user-visible win this skill could not observe.
