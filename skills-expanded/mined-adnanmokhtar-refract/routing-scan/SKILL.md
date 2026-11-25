---
name: routing-scan
description: "Routing bugs: onClick navigation, URL state not synced, unvalidated params, soft 404, redirect loops, nav races."
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: routing-scan

## Premise

The URL is the one piece of UI state a user can keep, share, bookmark and reload — and client-side routers make it easy to break. A table row navigates on click, so it cannot be opened in a new tab or copied. The list's filters live in component state, so reload, Back and a shared link all lose the view. `/orders/abc` reaches a fetch for `NaN`. An unknown path renders the home page with status 200. A guard on the sign-in route and a guard on the dashboard route send the browser back and forth. The protected page paints, and fires its requests, before the effect that redirects runs. A slow response for the previous route paints over the current one. No lint rule catches any of these (the research for this batch found none for `onClick` navigation or missing URL sync); each is visible in source and provable in a browser.

This skill finds them across Next.js (App Router), React Router / Remix, Vue Router / Nuxt, SvelteKit and the Angular Router, and proves each with a navigation oracle. It owns the routing family the earlier batches lacked (research ids R-01, R-03–R-07, R-09, R-10). The routing **speed** classes — prefetch, a full reload where a soft navigation belongs, scroll restoration, bfcache — stay in `navigation-speed`.

**Every finding cites the source `<file:line>` + the route it affects + the navigation that exposes it (reload, Back, a new tab, a typed URL, two fast clicks) + the oracle that proved it (or the test that would settle it) + the fix in the project's own router.** A grep hit is never a finding by itself. "Routing is fine" is never printed: the output is the class-coverage block (§ Output).

**Detect statically, prove by navigation.** The proof is a Playwright navigation on a production build (§ Proof): open in a new tab, a URL round trip, a garbage param, an unknown URL, a redirect hop count, the first protected frame, a build exit code, a held response. A candidate with no harness is **Unconfirmed**, carrying the settling test. It is never dropped, and never promoted on reading alone ([`precedents/ui.md`](../../../../snippets/precedents/ui.md), the proof rule).

## The rule

A candidate is a finding when all four hold:

1. **A route reaches it.** The component renders on a route a user can open; the guard or middleware runs on a real path. Route modules nobody mounts, stories and design-system demo pages fail here.
2. **A real navigation exposes it.** A reload, Back / Forward, a middle-click, a link pasted into a new browser, a typed or stale URL, a signed-out visit, two clicks faster than the API answers.
3. **The router does not already handle it.** A framework loader that discards a superseded navigation, a built-in 404 (Next, Nuxt, SvelteKit render one for unmatched paths), a data router's root `errorElement`, a server-side redirect, a typed search-param parser (§ False positives).
4. **The oracle fired.** The new tab did not open, the view did not survive the round trip, the page threw, the status or content was wrong, the hops exceeded one, the protected request went out, the build failed, the stale response painted.

## Boundaries

- **The keyboard half of a clickable non-link** (2.1.1) is `a11y-code-scan` §1, and **title, focus and announcement after a route change** are its §5 (this pack). §1 here owns the missing `href`: no new tab, no copy-link, no crawl. One element, one finding, credited to both; `seo-audit` §9 (this pack) corroborates on SEO routes.
- **A raw `<a href>` that reloads the SPA**, `window.location` navigation, **scroll restoration**, bfcache and prefetch → `navigation-speed` §1, §3, §5 and §6 (this pack).
- **Stale data after a write and Back / Forward** (R-08, a Server Action with no `revalidatePath`) → `client-data-scan` §4 (this pack). **Input-driven races** (typeahead, filters, tabs) → `client-data-scan` §3; §8 here owns races keyed on a **route param**. Dedupe by `<file:line>`.
- **A known detail route that renders a generic error for a missing record** → `ui-state-scan` §15 (ui-ux pack, when installed); §4 here owns **unknown URLs** (no route matches) and catch-all routes that never 404. Grep 4c lists dynamic Next segments with no `notFound()` for that owner; without ui-ux, they are reported here tagged `owner: ui-state-scan`. Error boundaries per route are `ui-state-scan` §4; unsaved-changes guards are its §10.
- **Authorization** is never decided here. A guard that exists only in the client → `xss-scan` §16 (security pack, when installed); §6 here owns the flash and the wasted protected requests. **A navigation target read from the URL** (`?redirect=`, `returnTo`, `next=`) → `xss-scan` §3 for the `javascript:` half and `ssrf-scan` § 7 for the open redirect, as `xss-scan` states. Without the security pack those rows print `N/A (owner pack security not installed)` and the hit is listed for it.
- **SSR request-API misuse** (Next 16 removed synchronous `params` / `searchParams` / `cookies()`) is `ssr-audit` (this pack); §3 here reports a param read that reaches a fetch or a render unvalidated, whatever the API shape.

## Adapt to the codebase — the router lanes

Read each router **with its version** from the lockfile and print the lanes you ran in the output header. Detectors key on API names, never on major numbers (react-router 8.4.0, SvelteKit 3.0.0 released 2026-10-01, Next 16.3.8, Nuxt 4.5.2, Angular 22.2.1 — npm registry, read 2026-10-05).

| Lane | Route table (grep 0b) | Navigation API | Catch-all / 404 (§4) | Server-side guard (§5, §6) | Race-safe built-in (§8) |
|---|---|---|---|---|---|
| **Next App Router** | `app/**/page.tsx` | `<Link>`, `useRouter().push`, `redirect()` | unmatched paths → built-in 404; `not-found.tsx`; `notFound()` | `middleware.ts` / `proxy.ts`, server-component `redirect()` | RSC navigation |
| **React Router / Remix** | `createBrowserRouter`, `<Routes>`, `routes.ts` | `<Link>`, `useNavigate()`, `<Navigate>` | `path: '*'`; a data router's root `errorElement` renders a 404 response | loader `throw redirect()` | loaders drop the superseded navigation |
| **Vue Router / Nuxt** | `createRouter({ routes })`, `pages/` | `<RouterLink>` / `<NuxtLink>`, `router.push`, `navigateTo` | `/:pathMatch(.*)*`; Nuxt renders `error.vue` with 404 | `router.beforeEach`, Nuxt route middleware | keyed `useFetch` |
| **SvelteKit** | `src/routes/**/+page.svelte` | plain `<a>` (client-routed), `goto` | unmatched → `+error.svelte` with 404; `[...rest]` must `error(404)` | `hooks.server.ts`, `+layout.server.ts` | `load` |
| **Angular** | `Routes = [...]`, `provideRouter` | `routerLink`, `router.navigate` | `{ path: '**' }` | `canActivate` / `canMatch` | `switchMap` on `paramMap` |
| **TanStack Router / wouter / Solid** | `createFileRoute`, `<Route>` | `<Link>`, `navigate` | per library — read | per library | `validateSearch` (TanStack) |

There is no lint lane for these classes. `svelte/no-navigation-without-resolve` (eslint-plugin-svelte 3.23.0, recommended) and `@next/next/no-html-link-for-pages` cover base paths and raw links, which route elsewhere (§ Boundaries). For §7 the Next production build is the checker.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path (`"${ROOTS[@]}"`); given no path, rg reads stdin under an agent's shell and reports a silent zero. Any rg exit 2 is a failed grep, never zero hits. `TB` is the JSX-aware tag body (`[^>]*` stops at the `>` of `onClick={() => x}`). File-level greps use `--files-without-match` — never `rg -L`, which is `--follow`. `NAV` excludes `navigate(-1)` (a Back button).

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|vue|svelte|@angular/core|solid-js|preact|next|nuxt)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.angular,coverage,storybook-static}/**'
   -g '!**/{test,tests,__tests__,__mocks__,mocks,e2e,fixtures,__fixtures__,playwright,cypress,msw,scripts}/**' -g '!**/*.{test,spec,stories,story,e2e,mock,mocks}.*'
   -g '!**/*.{test-data,fixture,fixtures}.*' -g '!**/{locales,locale,i18n,translations,docs,generated,__generated__}/**' -g '!**/*.min.*')
J=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte}'); M=(-g '*.{jsx,tsx,vue,svelte,html}')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|\{/\*|<!--)')   # drops comment-only lines
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'
NAV='(?:navigate(?!\(\s*-1\s*\))|router\.(?:push|replace|navigate|navigateByUrl)|\$router\.(?:push|replace)|this\.router\.(?:navigate|navigateByUrl)|goto|history\.push|navigateTo)\('
NET='(?:\bfetch|\$fetch|\baxios(?:\.\w+)?|\bky(?:\.\w+)?|\b(?:api|http|client|apiClient|request)\.(?:get|post|put|patch|delete|request|query))\s*[<(]'
S2='const\s*\[\s*(?:filters?|sort\w*|order(?:By|Dir\w*)|page|pageIndex|pageNumber|pageSize|perPage|query|q|search\w*|keyword|activeTab|tab|selectedTab|view(?:Mode)?|dateRange|statusFilter)\s*,\s*set\w+\s*\]\s*=\s*useState\b|\bconst\s+(?:filters?|sort\w*|page|pageSize|search\w*|activeTab|tab|dateRange)\s*=\s*ref\(|\blet\s+(?:filters?|sort\w*|page|pageSize|search\w*|activeTab|tab)\s*=\s*\$state\('
# 0a routers and parsers with versions; 0b route tables, guards and middleware files.
rg -n --no-heading --pcre2 '"(?:next|nuxt|vue-router|@sveltejs/kit|@angular/router|react-router(?:-dom)?|@remix-run/react|@tanstack/react-router|wouter|nuqs|zod|valibot)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -l --pcre2 'createBrowserRouter|createHashRouter|createMemoryRouter|<Routes\b|createRouter\(|createFileRoute\(|provideRouter\(|RouterModule\.for(?:Root|Child)\(|\bRoutes\s*=\s*\[|defineNuxtRouteMiddleware|router\.beforeEach' "${J[@]}" "${X[@]}" "${ROOTS[@]}"
for r in "${ROOTS[@]}"; do find "$r" \( -name node_modules -o -name .next -o -name dist \) -prune -o -type f \( -name 'middleware.[jt]s' -o -name 'proxy.[jt]s' -o -name 'hooks.server.[jt]s' -o -name 'routes.[jt]s' \) -print; done
# 1a a non-link element that navigates on click; 1b a button whose only job is to navigate; 1c a table / card prop that navigates;
# 1d the same through a named handler: functions whose body navigates within 3 lines (sign-out actions dropped), then every
#    event prop that calls one (`onOpen={() => actions.openOrder(id)}`, `onRowClick={(o) => openOrder(o.id)}`) or passes it
#    on (`openOrder={openOrder}` in a column factory) — the wrapper button inside the cell is the §1 row.
rg -n -U --pcre2 '<(?:div|span|tr|td|li|section|article|img|p|Card|Box|Stack|Row|TableRow)\b(?='"$TB"'\s(?:onClick|@click|v-on:click|\(click\)|onclick|on:click)\s*=\s*["{]\s*(?:\(\s*\w*\s*\)\s*=>\s*\{?\s*)?'"$NAV"')'"$TB"'>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '<(?:button|Button)\b(?='"$TB"'\s(?:onClick|@click|\(click\)|onclick)\s*=\s*["{]\s*(?:\(\s*\)\s*=>\s*)?'"$NAV"'[^;{}]*\)\s*["}])'"$TB"'>' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\bon(?:Row|Card|Item|Select)Click\s*=\s*\{\s*(?:\(\s*\w*\s*\)|\w+)\s*=>\s*\{?\s*'"$NAV" "${M[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
W="$(mktemp -d "${TMPDIR:-/tmp}/rt-pre.XXXXXX")"
rg -o -U --no-filename --pcre2 '(?:(?:const|let)\s+(\w+)\s*=\s*(?:useCallback\(\s*)?(?:async\s*)?(?:\([^()\n]*\)|\w+)\s*(?::[^=\n]{1,60})?=>|function\s+(\w+)\s*\([^()\n]*\)[^{\n]*\{)[^\n]*\n?(?:[^\n]*\n){0,2}?[^\n]*?'"$NAV" -r '$1$2' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | rg -v -i '^(?:handle)?(?:log|sign)_?out$' | sort -u > "$W/navfn"
rg -n -o --pcre2 '\bon[A-Z]\w*\s*=\s*\{\s*(?:(?:async\s*)?\(\s*[\w,\s]*\)\s*=>\s*\{?\s*)?(?:[\w.]+\.)?(\w+)\s*[(}]|\b\w+=\{\s*(?:[\w.]+\.)?(\w+)\s*\}' -r '$1$2' "${M[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: 'NR==FNR{n[$1]=1;next} ($NF in n)' "$W/navfn" -
# 2a URL-able view state held in component state, in route-level code that never writes the URL (overlay components dropped).
rg -l --pcre2 "$S2" -g '**/{pages,routes,app,views,screens,features}/**' "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'setSearchParams|useQueryStates?\b|router\.(?:replace|push)\(\s*\{[^}]*query|navigate\(\s*\{[^}]*search|[?&]page=|goto\(\s*[`"\x27]\?|queryParamsHandling|\$page\.url\.searchParams\.set' | rg -v --pcre2 '(?:Dialog|Popover|Combobox|Picker|Sheet|Drawer|Modal|Select|Menu)\w*\.(?:tsx|vue|svelte)$' | xargs -r rg -H -n --pcre2 "$S2"
# 3a a route or search param coerced or cast with no validation; 3b every route-param consumer (targets for the garbage-param oracle);
#    a bare `params` object counts only in a page, layout or route file (elsewhere it is any local `params`, e.g. an API helper's).
rg -n --pcre2 '\b(?:Number|parseInt|parseFloat|BigInt)\(\s*(?:params|searchParams|query|route\.(?:params|query)|\$route\.(?:params|query)|page\.(?:params|url\.searchParams)|this\.route\.snapshot\.(?:params|queryParams|paramMap))\b|\bsearchParams\.get\(\s*["\x27]\w+["\x27]\s*\)\s*(?:as\s+[A-Z]|!(?!=))|\buseParams(?:<[^>]*>)?\(\)\s*as\b|\b(?:route|\$route)\.(?:params|query)\.\w+\s+as\s+(?!const)\w' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'const\s*\{[^}]+\}\s*=\s*(?:use(?:Params|Route)(?:<[^>]*>)?\(\)|await\s+(?:props\.)?params\b|props\.params\b|route\.params|\$page\.params|page\.params)' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'const\s*\{[^}]+\}\s*=\s*params\b' -g '**/{page,layout,route,default,template}.{js,jsx,ts,tsx}' -g '**/+{page,layout}{,.server}.{js,ts}' -g '**/{routes,pages}/**/*.{js,jsx,ts,tsx,vue}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4a catch-all routes, error elements and 404 files present; 4b catch-all pages that never 404; 4d route tables with no catch-all and no error element.
rg -n --pcre2 'path\s*:\s*["\x27](?:\*|\*\*)["\x27]|path=["\x27]\*["\x27]|pathMatch\(\.\*\)\*|:catchAll\(\.\*\)|errorElement\s*[:=]|ErrorBoundary\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
for r in "${ROOTS[@]}"; do find "$r" \( -name node_modules -o -name .next -o -name dist -o -name .nuxt -o -name .svelte-kit \) -prune -o -type f \( -name 'not-found.[jt]s*' -o -name '+error.svelte' -o -name 'error.vue' -o -name '404.*' -o -path '*\[...*' -o -path '*\[\[...*' \) -print; done
for r in "${ROOTS[@]}"; do find "$r" \( -name node_modules -o -name .next -o -name dist \) -prune -o -type f \( -path '*/\[...*/page.[jt]s*' -o -path '*/\[\[...*/page.[jt]s*' -o -path '*/\[...*\].vue' -o -path '*/\[...*/+page.*' \) -print; done | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'notFound\(|createError\(|error\(\s*404|statusCode\s*:\s*404|status\s*:\s*404'
rg -l --pcre2 'createBrowserRouter|createHashRouter|<Routes\b|createRouter\(\s*\{|provideRouter\(|RouterModule\.forRoot\(|\bRoutes\s*=\s*\[' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'path\s*:\s*["\x27](?:\*|\*\*)["\x27]|path=["\x27]\*["\x27]|pathMatch\(\.\*\)\*|:catchAll\(|errorElement|ErrorBoundary'
# 4c (owner ui-state-scan §15) Next dynamic segments with no notFound(), and the nearest not-found.tsx up the segment tree — the boundary walk.
#    A leading `[locale]`/`[lang]` segment alone does not make a page dynamic: the page needs a bracket segment below it.
for r in "${ROOTS[@]}"; do for A in $(find "$r" \( -name node_modules -o -name .next \) -prune -o -type d -name app -print); do find "$A" -type f -name 'page.[jt]s*' -path '*\[*' | while read -r p; do case "$(printf '%s' "${p#"$A"/}" | sed -E 's#^\[(locale|lang|lng|language)\]/##')" in *\[*) ;; *) continue ;; esac; grep -Eq 'notFound\(' "$p" && continue; d=$(dirname "$p"); nf=""; while :; do [ -n "$(find "$d" -maxdepth 1 -name 'not-found.[jt]s*' | head -1)" ] && { nf="$d"; break; }; [ "$d" = "$A" ] && break; d=$(dirname "$d"); done; echo "NO-notFound() $p (nearest not-found: ${nf:-none, Next default})"; done; done; done
# 5a redirect sites with their targets; 5b guards / middleware that redirect to sign-in with no check of the current path.
rg -n --pcre2 '(?:redirect|navigate|router\.(?:push|replace)|navigateTo|goto|createUrlTree|parseUrl|next)\(\s*\[?\s*["\x27`]/(?:login|signin|sign-in|auth|dashboard|home|onboarding|welcome|select-\w+|setup)\b|<Navigate\b[^>]*\bto=\{?\s*["\x27`]/|return\s+["\x27`]/(?:login|signin|auth)\b|\{\s*name\s*:\s*["\x27](?:login|signin|auth)["\x27]' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
{ rg -l --pcre2 'NextResponse\.redirect|router\.beforeEach|defineNuxtRouteMiddleware|CanActivateFn|\bcanActivate\s*\(|export\s+(?:const|async\s+function)\s+handle\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}"; for r in "${ROOTS[@]}"; do find "$r" \( -name node_modules -o -name .next -o -name dist \) -prune -o -type f \( -name 'middleware.[jt]s' -o -name 'proxy.[jt]s' -o -name 'hooks.server.[jt]s' -o -name '*.guard.ts' -o -path '*/middleware/*.[jt]s' \) -print; done; } | sort -u | tr '\n' '\0' | xargs -0 -r rg -l --pcre2 '["\x27`]/(?:login|signin|sign-in|auth)\b|name\s*:\s*["\x27](?:login|signin)' | xargs -r rg --files-without-match --pcre2 'matcher|pathname|to\.(?:name|path|fullPath|meta|matched)|state\.url|isPublic|publicPaths|PUBLIC_|startsWith\(\s*["\x27`]/(?:login|auth)'
# 6a a redirect decided in an effect / mount hook; 6b a component guard returning <Navigate> (read what renders while the session is unknown).
rg -n -U --pcre2 '(?:useEffect|onMounted|onMount|\$effect|ngOnInit)\s*\(\s*(?:async\s*)?(?:\(\)\s*=>|function\s*\(\))?\s*\{?\s*if\s*\(\s*!\s*(?:\w+\.)*(?:user|session|isAuthenticated|isLoggedIn|loggedIn|token|auth\w*|currentUser)\b[^)]*\)\s*\{?\s*(?:return\s+)?(?:router\.(?:push|replace|navigate)|navigate|redirect|goto|navigateTo|this\.router\.navigate)\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'if\s*\(\s*!\s*(?:\w+\.)*(?:user|session|isAuthenticated|isLoggedIn|token|auth\w*|currentUser|principal)\b[^)]*\)\s*(?:\{\s*)?return\s+<Navigate\b' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7a (Next) client components calling useSearchParams, and how many of their renderers place every <Tag> between
#    <Suspense> and </Suspense> (JSX ancestry, not "the file has a Suspense somewhere").
rg -l --pcre2 "from\s+['\"]next/navigation['\"]" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg -l '\buseSearchParams\(' | while read -r f; do n=$(rg -o --no-filename --pcre2 'export\s+(?:default\s+)?function\s+([A-Z]\w+)' -r '$1' "$f" | head -1); [ -z "$n" ] && { echo "$f (no named export: read)"; continue; }; imp=$(rg -l --pcre2 "<$n\b" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | grep -vxF "$f")
  s=$(printf '%s\n' "$imp" | while IFS= read -r i; do [ -n "$i" ] && awk -v n="$n" '{s=$0; while (match(s, "</?Suspense([^A-Za-z0-9_]|$)|<" n "([^A-Za-z0-9_]|$)")) {t=substr(s,RSTART,RLENGTH); s=substr(s,RSTART+RLENGTH); if (t ~ /^<\/Suspense/) d--; else if (t ~ /^<Suspense/) d++; else if (d<1) bad=1}} END{exit bad}' "$i" && echo "$i"; done | wc -l | tr -d ' '); echo "$f <$n> rendered by $(printf '%s' "$imp" | grep -c .) file(s), $s with every <$n> inside <Suspense>"; done
# 8a files keyed on a route param that fetch in an effect / subscription with no cancellation and no keyed cache; 8b Angular paramMap flattened without switchMap, or nested subscribe.
rg -l --pcre2 '\buseParams\(|\buseRoute\(\)|\broute\.params\b|\$route\.params|\bpage\.params\b|\bparamMap\b|\buseSearchParams\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg -l --pcre2 '\buseEffect\(|\bwatch(?:Effect)?\(|\$effect\(|ngOnInit|\.subscribe\(' | xargs -r rg -l --pcre2 "$NET" | xargs -r rg --files-without-match --pcre2 'AbortController|\bsignal\b|\bignore\b|cancel(?:l)?ed|\bactive\s*=\s*false|onCleanup|onWatcherCleanup|switchMap|takeUntil|useQuery|useSWR|createQuery|loader'
rg -n -U --pcre2 '(?:paramMap|params|queryParamMap|queryParams)\s*\.\s*pipe\([^;]{0,300}?\b(?:mergeMap|concatMap|flatMap)\(|(?:paramMap|params)\.subscribe\([^;]{0,200}?\.subscribe\(' -g '*.ts' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a hit **plus** a read **plus** the route **plus** the oracle. Three blind spots are structural:

- **Navigation hides behind handlers and view models.** `onClick={open}` where `open` calls `navigate` is what 1d resolves, one file hop at a time: a handler built inside a view-model hook and returned as `vm.open` resolves by name, but a handler named by a computed key or built by a factory does not. A view-model hook that owns `page` state is invisible to 2a. Read the handler; add the project's table and card components to 1c.
- **Guards compose.** A layout guard, a loader redirect and middleware can each be correct alone and loop together. §5 needs the route table read as a whole, then the hop-count oracle.
- **The router's own behaviour is version-specific.** Read the lockfile version before asserting a built-in (a data router's `errorElement`, Next's default 404, SvelteKit's `+error.svelte`).

**Measured** (2026-10-05, the script above, under 1 s per tree):

| Tree | Hits that matter | Verdict |
|---|---|---|
| research fixtures `B-rg/fx` | 1a 6 sites in 5 files · 1b 1 · 6a 1 | every seeded R-01 positive caught (React `tr` and `div`, Vue `@click` with `router.push` and `$router.push`, Svelte 5 `onclick` + `goto`, Angular `(click)` + `router.navigate`); 0 hits on `<Link to>`, `[routerLink]` and a button that saves then navigates. The client-guard positive caught by 6a; the server `redirect()` decoy is not. The first 5b listed that decoy too — 5b is now restricted to guard and middleware files |
| scratch fixtures (Next 16 app dir, React Router 7 config, Vue Router, Angular 22, SvelteKit 3; one positive + one decoy per grep) | 1c 1 · 2a 2 · 3a 3 · 3b 4 · 4b 2 · 4c 2 · 4d 2 · 5b 2 · 6b 1 · 7a 2 rows · 8a 2 · 8b 1 | every positive caught; decoys refuted: a page that writes `setSearchParams`, a `safeParse`d param, a catch-all that calls `notFound()`, an Angular table with `**`, a `<Suspense>`-wrapped `useSearchParams`, a `switchMap` on `paramMap` |
| `benchmarks/fixtures/slow-marketplace/web` | 2a 2 · 3b 2 | the catalog keeps its search and sort in `useState` — a §2 candidate (unseeded); the router's root `errorElement` satisfies 4d |
| `benchmarks/fixtures/vuln-fullstack/web` | 3b 2 · 4d 1 | `<Routes>` with no `path="*"` and no `/` route: an unknown URL renders nothing — a §4 candidate (unseeded). The first 2a counted a `status` save-message variable; the name list now takes `statusFilter` only |
| real React 19 + React Router 7 app, 28 route files | 1a 0 · 1b 30 · 1c 2 · 2a 176 lines in 107 files · 3a 0 · 3b 21 · 4a catch-all present · 5a 27 · 5b 0 · 6b 1 · 7 N/A (no Next) · 8a 0 | 1b: call-to-action buttons that only navigate (sign-in, install, back-to-list) — low-severity §1 rows, one group per wrapper. 1c: two table rows navigating through `onRowClick` (read for a real link in the row). 2a: `search` 56, `page` 34, `pageSize` 21, `tab` 15 — three read: a tab read once from the URL and never written back, a hub tab and a storefront grid in state — candidates; grouped by view-model hook. 3a: a `!==` comparison the first version took for a non-null assertion. 3b: route params destructured from `useParams()` with an empty-string default — garbage-param targets. 6b: the layout guard renders a fallback until the session is known, then `<Navigate>` before `<Outlet>` — no flash, refuted on read (authorization stays security's). 8a: every param-keyed read goes through a keyed query |
| a real NestJS + React monorepo (React Router 7.18 SPA), re-measured 2026-10-15 | 1d 71 · 3a 11 → 0 · 3b 26 → 19 | 3a: all 11 were `*-backend.test-data.ts` builders, now excluded by X. 3b: the 7 dropped were API helpers destructuring a local `params`. 1d (new): 16 navigating handlers, 71 call sites — it is the only grep that reaches the largest §1 row, an order code rendered as a `<button>` whose `onOpen` prop is bound to `navigate` in a column factory (4 tables) plus `onRowClick={(o) => openOrder(o.id)}`; 42 of the 71 are one `openCreate` handler on "new" buttons (one low group). Fixtures: nothing lost; 3 new 1d candidates (a save-then-navigate button — read, not a link — and two React Native screens) |

Small fixtures prove the greps parse and catch seeded rows; precision at scale comes from the real-app row.

## The 3,000-hit path

1. **Intersect** with the route table (grep 0b): a component no route mounts is dismissed with one read.
2. **Group** by (route module or view-model hook, pattern). A table component whose `onRowClick` navigates, or a list hook that holds `page` / `search` in state, is one group however many routes use it; fixing it closes them.
3. **Rank** by route traffic (RUM or analytics when present), else list, search, detail, sign-in and checkout-class routes first.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale.** Generate navigation property tests from the route manifest — for every list and detail route: middle-click opens a tab, reload keeps the view, a garbage param renders a handled state, an unknown URL renders not-found, every route settles in at most one redirect. One pass confirms or refutes whole groups.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

Severity is the user-visible consequence on a reachable route. Raise one step on primary navigation, sign-in, checkout-class or shared-link routes; drop one step on an internal tool with a single operator.

| § | Class | Research id | Default |
|---|---|---|---|
| 1 | Navigation by click on a non-link: no `href`, no new tab, no copy-link, no crawl | R-01 | medium; high on primary navigation; low for a button that only navigates |
| 2 | URL-able view state (filters, sort, page, tab, search) kept only in component state | R-03 | medium on list and search routes; low elsewhere |
| 3 | Route or search params not validated or parsed | R-04 | medium; high when the raw value reaches a write |
| 4 | Unknown URL with no catch-all, or a catch-all that never 404s (soft 404) | R-05 | medium; high when the unknown URL renders the home page with 200 on an SEO route |
| 5 | Redirect loop | R-07 | high (the app is unusable on that path) |
| 6 | Protected content painted, or protected requests sent, before the client guard redirects | R-06 (UX half) | medium; the authorization half is security's |
| 7 | Next `useSearchParams` with no `<Suspense>` boundary (client-side rendering bailout) | R-09 | medium; high when it blanks a static landing route |
| 8 | Navigation race: a slow response for the previous route param paints on the current one | R-10 | medium; high on detail views that drive a write |

### 1. Navigation by click on a non-link

```
BAD:   <tr onClick={() => navigate(`/orders/${o.id}`)}>   · <div @click="router.push(`/p/${p.id}`)">   · <Button onClick={() => navigate('/login')}>
GOOD:  <Link to={`/orders/${o.id}`}>…</Link> (a stretched link for a whole row)   · <Button asChild><Link to="/login">…</Link></Button>
```
**Read the code:** For a 1d hit, open the component that receives the handler and find the element it lands on (a cell's `<button onClick={(e) => { e.stopPropagation(); onOpen(); }}>` is the row). Does the row or card also hold a real link for the same action (`precedents/ui.md` § 17)? Does the button do work first (save, then navigate — not this class)? Is the target a route (not an external origin, which routes to the security owners)? **Finding when** the only path to a route is a click handler: no new tab, no copy-link, and no `href` for crawlers. The keyboard half is credited to `a11y-code-scan` §1. **Proof:** *Open in new tab* (§ Proof).

### 2. URL-able view state kept only in component state

```
BAD:   const [page, setPage] = useState(1) · Vue const page = ref(1) · Svelte let page = $state(1)      (list route; nothing writes the URL)
GOOD:  useSearchParams / nuqs useQueryState('page', parseAsInteger.withDefault(1)) · router.replace({ query }) · goto('?page=2', { replaceState: true, keepFocus: true, noScroll: true })
```
**Read the code:** Is the state view state a user would share or come back to (filters, sort, page, tab, search on a list or report route), or local (a dialog's search, a picker, a wizard step, PII in a filter — `precedents` below)? Is it read from the URL once and never written back (deep-link in, not out)? Does typing write with `replace`, not one history entry per keystroke? **Finding when** reload, Back or a shared link loses the view on a list or search route. **Proof:** *URL round trip* (§ Proof).

### 3. Route or search params not validated

```
BAD:   const id = Number(params.id); fetch(`/api/orders/${id}`)   · searchParams.get('page')!   · useParams() as { id: string }   · const { id = '' } = useParams()
GOOD:  z.coerce.number().int().positive().safeParse(params.id) → notFound() / a 404 view · TanStack Router validateSearch · nuqs parseAsInteger
```
**Read the code:** What does `/route/abc`, `/route/-1` or `?page=-5&sort=%27` do — reach a fetch with `NaN` or `undefined`, throw in render, or render a handled state? Does the API's 400 / 404 come back as a not-found view? On Next 16, `params` and `searchParams` are Promises: a synchronous `params.id` is `undefined` (owner `ssr-audit` for the API, this § for the unvalidated value). **Finding when** a malformed param crashes the view, sends a request carrying `NaN` / `undefined`, or renders a wrong entity. **Proof:** *Garbage param* (§ Proof).

### 4. Unknown URL with no catch-all, or a soft 404

**Read the code:** Which lane (§ Adapt)? React Router `<Routes>` with no `path="*"` renders nothing for an unknown path; a data router with a root `errorElement` renders its 404 response. Vue Router with no `/:pathMatch(.*)*` renders an empty `<RouterView>`. Angular with no `**` fails the navigation. Next, Nuxt and SvelteKit 404 unmatched paths themselves — but a catch-all page (`[...slug]`, `[[...path]]`, `[...rest]`) that never calls `notFound()` / `createError({ statusCode: 404 })` / `error(404)` answers every typo with 200 (grep 4b), and middleware that rewrites unknown paths to `/` is a soft 404. An SPA behind a history fallback answers 200 by design: assert the content (`precedents/ui.md` § 41). **Finding when** an unknown URL renders blank, the home page or a crash instead of a not-found view. **Proof:** *Unknown URL* (§ Proof).

### 5. Redirect loop

**Read the code:** Read the route table and every guard together (greps 0b, 5a, 5b): does the sign-in guard run on the sign-in route itself (Next middleware with no `matcher` and no `pathname` check; a `beforeEach` that never looks at `to`)? Do the protected side and the sign-in side read the session from different sources (a cookie the server sees, a store the client fills later)? Do trailing-slash, locale-prefix or onboarding redirects chain? **Finding when** some path, in some session state (signed out, signed in, expired, mid-onboarding), never settles. **Proof:** *Redirect hop count* (§ Proof).

### 6. Protected content painted before the client guard redirects

```
BAD:   useEffect(() => { if (!user) router.push('/login') }, [user]) · Vue onMounted(() => { if (!user) router.push('/login') })   (the page renders and fetches first)
GOOD:  middleware / proxy, a loader `throw redirect()`, hooks.server.ts, canActivate — or a guard that renders a fallback until the session is known
```
**Read the code:** What renders while the session is unknown — the protected children, or a fallback? Do the page's queries fire before the guard decides? Is there a server-side redirect in front of the route? **Finding when** a signed-out visit paints protected content or sends protected API requests before the redirect. Whether the server refuses those requests is `xss-scan` §16's question, never this skill's. **Proof:** *First protected frame* (§ Proof).

### 7. Next `useSearchParams` with no `<Suspense>` boundary

**Read the code:** For each client component that calls `useSearchParams` (grep 7a), is the nearest renderer inside `<Suspense>`, is the route dynamic anyway (`await connection()`, dynamic APIs), or does the page pass `searchParams` (a Promise) and `use()` it under Suspense? The `experimental.missingSuspenseWithCSRBailout` escape hatch existed only in Next 14 (Next docs, *Missing Suspense boundary with useSearchParams*, read by the research 2026-10-05). **Finding when** the production build fails, or the static route bails out to client rendering. **Proof:** the **Build gate** oracle (§ Proof): `next build` (or `next build --debug-prerender`, which names the component) fails with `missing-suspense-with-csr-bailout` before the fix and passes after. Not Next: `N/A (no Next App Router)`.

### 8. Navigation race

```
BAD:   const { id } = useParams(); useEffect(() => { fetch(`/api/items/${id}`).then(r => r.json()).then(setItem) }, [id])
       this.route.paramMap.pipe(mergeMap((p) => this.http.get(`/api/p/${p.get('id')}`)))
GOOD:  a loader · a keyed useQuery({ queryKey: ['item', id] }) · AbortController in the effect's cleanup · switchMap
```
**Read the code:** Can the param change while the previous response is in flight (next / previous buttons, a list beside a detail pane, fast clicks)? Does a loader or a keyed cache already discard the stale answer? **Finding when** the response for the previous param can paint under the current one. **Proof:** *Request order* (V110, [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states) — the route-param variant: `/items/1` delayed 800 ms, `/items/2` 50 ms, click 1 then 2; the heading must show item 2 and never flash item 1.

## Proof

Each oracle is in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states — the six navigation shapes under *Client data and navigation oracles*, §7 under *Build gate* (V131), §8 under § "Mount/unmount balance, reorder identity, request order" (V110). Run on a production build:

- **Open in new tab** (V125, §1) — middle-click or Ctrl/Cmd-click opens a page, and the element has an `href`.
- **URL round trip** (V126, §2) — reload, back after one more change, and a fresh context all show the same controls and rows; a typed search adds at most one history entry.
- **Garbage param** (V127, §3) — `/orders/abc`, `/orders/-1`, `?page=-5&sort=%27` give a not-found or normalized view, zero `pageerror`, no request URL with `NaN` / `undefined` / `null`.
- **Unknown URL** (V128, §4) — status 404 on SSR; on an SPA fallback, a not-found heading and a link home, not the home page.
- **Redirect hop count** (V129, §5) — signed in, signed out and expired: no `ERR_TOO_MANY_REDIRECTS`, at most 2 main-frame navigations in 3 s, a server chain of at most one hop.
- **First protected frame** (V130, §6) — signed out, no protected API request before the URL reaches sign-in, and no protected content at commit plus one frame.

Every test asserts the **one** behaviour the finding names and **fails before the fix**; a test that passes on the unfixed code proves nothing. A fix is accepted when the oracle goes green, the class variants pass (§1: row, card, image, icon, breadcrumb, menu item in each stack present; §2: filter, sort, page, page size, tab, date range, search; §5–§6: hard load, client navigation from a public page, session expiry mid-session; §8: next / previous, list-detail, fast clicks), and the owning grep goes quiet on the line. Never accepted: `role="link"` + `tabIndex` on a `div` in place of an `href`, a `try/catch` that renders the home page for a bad param, `suppressHydrationWarning` or `export const dynamic = 'force-dynamic'` added only to silence §7 without a reason, deleting the test.

## Output

```
routing-scan — lanes: react-router 7.18 (data router, 28 route files); next, vue-router, sveltekit, angular absent
Context: catch-all path '*' → NotFoundPage (src/app/router.tsx:212) · guards: RequireSession (layout route) · no middleware

Findings: 1 · Unconfirmed: 2

1. src/orders/list/useOrdersList.ts:58                             [report-with-fix]   medium
   §2 list state not in the URL — page, pageSize, search and statusFilter in useState; /orders?page=3 is never written.
   Proof: e2e/routing/orders-url.spec.ts — URL round trip: page 3 + search "cairo" → reload → page 1, empty search.
   Fix: useSearchParams with replace for the search (the pattern src/reports/useReportsHub.ts already uses); one hook, 4 routes.

2. src/shared/ui/data-table.tsx:212                                [report-flagged]    medium
   §1 onRowClick navigates; rows carry no link. Unproven link: whether the first cell renders a <Link> for the same target.
   Settling test: Open in new tab on /orders and /returns rows (one wrapper, 9 call sites).

3. src/accounts/AccountTasksPage.tsx:18                            [report-flagged]    medium
   §3 const { accountId = '' } = useParams() reaches the tasks query unvalidated.
   Settling test: Garbage param — /accounts/abc/tasks renders the not-found view, 0 pageerror, no request with an empty id.

Verification: 41 candidates → 1 finding · 2 unconfirmed · 4 hardening · 0 pre-existing · 34 refuted

Class coverage:
  §1 click navigation on a non-link  checked (0 + 30 button + 2 row hits → 1 unconfirmed; 30 button-only navigations Hardening, 1 group)
  §2 URL state not synced            checked (176 hits / 107 files → 1 finding (4 routes); Live, unreviewed (96 groups — continue with grep 2a))
  §3 params not validated            checked (0 casts; 21 route-param reads → 1 unconfirmed; Live, unreviewed (18 — garbage-param pass))
  §4 unknown URL / soft 404          checked (catch-all present → 0 findings)
  §5 redirect loop                   checked (27 redirect sites, 0 guard files without a path check → 0 findings)
  §6 protected content flash         checked (1 guard → refuted: fallback until the session is known)
  §7 useSearchParams without Suspense N/A (no Next App Router)
  §8 navigation race                 checked (0 files; param-keyed reads go through keyed queries)
```

`[report-with-fix]`: the source line, the route, a failing navigation oracle and a local fix in the project's router are all present. `[report-flagged]`: one link is unproven (a wrapper not read, no harness, an unknown API behaviour), and the row names it and the settling test. The coverage block lists **all eight** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present router; `N/A (<reason>)` only when the lane is absent (§7 without Next); `blocked (<reason>)` when a grep failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / precedents

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (§ 17 cards with an inner link, § 27 route announcers, § 41 history-fallback 200, routing § 70–75) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10 (the correctness column). The routing precedents, in short:

- **§1** (ui § 17, 70): a row or card that also holds a real link for the same action; a button that does work and then navigates; `navigate(-1)` / `router.back()`; drag, select and map-marker interactions.
- **§2** (ui § 71): dialog, picker and combobox search; wizard steps not meant to be deep-linked; filters that carry PII (privacy wins over shareability); state already mirrored through `nuqs`, `useSearchParams` or `router.replace({ query })`.
- **§3** (ui § 72): a param parsed by a schema (`safeParse`, `validateSearch`, nuqs parsers) or checked before use; a param that only selects a tab with a default.
- **§4** (ui § 73): Next, Nuxt and SvelteKit unmatched paths (built-in 404); a React Router data router whose root `errorElement` renders the 404 response; SvelteKit's plain `<a>` is client-routed.
- **§5–§6** (ui § 74): a guard that renders a fallback until the session is known and redirects before rendering the protected outlet (measured: refuted on read); server-side redirects in middleware, loaders, `hooks.server.ts` or `canActivate`.
- **§8** (ui § 63, 75): router loaders (React Router, SvelteKit, Next server components) drop the superseded navigation; keyed TanStack / SWR queries discard a stale response by key; `switchMap` cancels.

## When to run

- On any diff that adds or changes a route, a route module, a guard or middleware, a list or search page, a table or card component that navigates, or a `useParams` / `useSearchParams` consumer.
- On every whole-repo `/frontend-audit` (when the frontend audit command ships), reporting all eight classes; after a router major upgrade (`/upgrade-dep`).

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under an audit command that happens in its verification phase; run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the source `<file:line>`, the route it affects, the navigation that exposes it, and the fix in the project's own router.
- Do not mark a finding `[report-with-fix]` without a navigation oracle that failed.
- Do not decide authorization (§6) or an open redirect: route them to the security owners named in § Boundaries.
- Do not report a §4 soft 404 on an SPA by its HTTP status alone (history fallback answers 200): assert the content.
- Do not print "routing is fine". Print the coverage block; a class whose grep did not run is `blocked`, never `checked`.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `a11y-code-scan` §1 and §5, `navigation-speed`, `seo-audit` §9, `client-data-scan` §3 and §4, `ssr-audit` (this pack) — the neighbouring halves named in § Boundaries.
- `ui-state-scan` §4, §10 and §15 (ui-ux pack, when installed) — error boundaries, unsaved-changes guards, a missing record on a known route.
- `xss-scan` §3 and §16, `ssrf-scan` § 7 (security pack, when installed) — URL sinks, client-only authorization, open redirects.
- `@ui-reviewer` (this pack) — consumes this skill's findings in a diff review.
