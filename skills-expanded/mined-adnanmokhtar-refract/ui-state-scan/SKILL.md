---
name: ui-state-scan
description: Missing UI states per surface, proved by a state-matrix test.
kind: skill
pack: ui-ux
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: ui-state-scan

## Premise

A surface that shows data is in one of several states at any moment: waiting, empty, failed, half-failed, refused, offline, out of date, submitting. A happy-path build renders one of them. The others show up as defects: a blank list that is really a 500, a spinner that never ends, a 403 shown as "Something went wrong" and retried forever, a second click that charges twice, a delete with no way back. No log records any of them, because the code did exactly what it was written to do.

This skill finds the surfaces that cannot render a state they can be in. It covers web and mobile lanes, §1–§15. It is the detector behind `@ux-reviewer`'s state verdict and gate G12. Its proof is the **state-matrix test**: the network (or the repository behind a mobile screen) is forced into each state, and the test asserts what the user sees. The same test is a row in the feature's state matrix (`state-matrix`, this pack).

**Every finding cites the surface `<file:line>` + the data source it renders + the state it cannot render + the user-visible result + the state-matrix test that fails (or the one that would settle it) + the fix.** A grep hit is never a finding by itself. "All states handled" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by forcing the state.** A candidate read in code with no harness to force the state is **Unconfirmed**, carrying the test that would settle it. Reading alone never promotes it: what a component renders under a 500 is a render fact, and only a render shows it ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10, accessibility and correctness columns).

## The rule

A missing state is a finding when all four hold:

1. **The surface is reachable.** A route, a screen in the navigator, or a dialog a reachable surface opens. A component used only by stories or tests fails here.
2. **The state can occur.** The source can be empty (a list, a search), can fail (any network read), can refuse (an authenticated API), can hang (no timeout), can go offline (a mobile app, a PWA), can be submitted twice (a write). A static config import cannot fail.
3. **Nothing upstream renders it.** Check the shared state wrapper (grep 0d), a route or segment error boundary, a Suspense boundary with an error boundary around it, a `throwOnError` that routes to one, and a presenter that receives the whole result and branches. A global toast is **not** the surface's state: a toast over an empty list is still §3.
4. **The user meets a wrong outcome.** Blank where a failure happened, a spinner forever, data that silently diverges, an action that ran twice, a loss with no undo, an error with no way out.

## Boundaries

- **Swallowed errors in services and API clients** belong to `error-handling-scan` § 2 and § 7 (code-quality pack, when installed). This skill owns the same root cause when it is in a component or a UI hook (§3); dedupe by `<file:line>`. Without the code-quality pack, report it here.
- **Double charge on money, stock or single-use writes** belongs to `logic-race-scan` § 4 (security pack, when installed): the server-side idempotency key is the fix. §8 here owns the UI pending state. Without the security pack, §8 reports the row tagged `security-class (owner pack not installed)`.
- **Hiding a control is not authorization.** A client-only check belongs to `xss-scan` § 16 (security pack, when installed). §6 owns only how a refusal is rendered.
- **Optimistic rollback mechanics** (cache snapshot, `cancelQueries`, restore) belong to `client-data-scan` §5 (frontend pack, when installed): with it installed, 8c/8d hits are deferred there and §8 keeps only the pending state the user sees. Without the frontend pack, §8 runs greps 8c/8d and reports the row itself. **Queue durability and replay for offline writes** belong to `offline-sync-scan` (mobile pack, when installed); §7 owns the offline indicator and the rejected-or-queued answer the user sees.
- **Contrast, focus and announcement of a state** (an error that is never announced, SC 4.1.3) go to `@ux-reviewer`'s WCAG lane. **Translated text that overflows** goes to i18n. §9 owns overflow from user data: names, emails, numbers.
- **Unknown URLs with no catch-all route** (a soft 404) are `routing-scan` §4 (frontend pack, when installed; without it, list them under §15 tagged `owner: routing-scan (frontend pack not installed)`). §15 owns a known detail route that renders a generic error for a missing record.
- **Visual fixes** (an empty state that exists but looks unfinished) go to `ui-design-sweep` verbs 9–11 through `/polish` or `/enhance-ui`. This skill reports the missing branch, not its look.

## Adapt to the codebase — the lane table

Read the framework and data library **and their versions** from the lockfile, never from memory, and print the lanes you ran in the output header. Detectors key on API names, not majors: react-router is at 8.x and SvelteKit at 3.0 (registry, 2026-10-05).

| Lane | Data primitive (grep 0a) | The state branch it must reach | Route / screen boundary | Lint that helps | State-matrix harness |
|---|---|---|---|---|---|
| **React** + TanStack Query 5 / SWR / Apollo / RTK Query / hand-rolled `useEffect` + fetch | `useQuery`, `useSuspenseQuery`, `useInfiniteQuery`, `useQueries`, `useSWR`, `use…Query`, `useEffect` + `fetch`/`axios`/`ky` | `isPending`, `isError`, `isPaused`, `data.length`, `error.status`; `isRefetchError` for §12 | RR 7/8 `errorElement`/`ErrorBoundary`; Next `error.tsx`, `not-found.tsx`, `global-error.tsx`; `react-error-boundary` | `react-hooks/error-boundaries` (eslint-plugin-react-hooks 7.1.1) flags try/catch around JSX | MSW 3 + Vitest/RTL; Storybook + msw-storybook-addon 3.0.3; Playwright `page.route` |
| **Vue 3 / Nuxt 4** | `useFetch`, `useAsyncData`, `useLazyFetch`, TanStack Vue Query | `pending`/`status`, `error`, `v-else` | `error.vue`, `<NuxtErrorBoundary>`, `onErrorCaptured` | — | MSW + Vitest/Vue Test Utils; Playwright |
| **Svelte 5 / SvelteKit** | `load` in `+page(.server).ts`, `createQuery`, `{#await}` | `{:catch}`, `{:else}` on `{#each}` | `+error.svelte` | `svelte/require-each-key` (state rows keep identity) | MSW + Vitest; Playwright |
| **Angular 20–22** | `httpResource`, `rxResource`, `injectQuery`, `async` pipe | `.isLoading()`, `.error()`, `@if`, `@empty` on `@for` | `withNavigationErrorHandler`, a global `ErrorHandler` | `@angular-eslint/template/prefer-at-empty` (22.5.0) | MSW or `HttpTestingController` per state; Playwright |
| **Solid / Qwik / plain HTML** | `createResource`, `routeLoader$`, `fetch` | `.loading`, `.error` | — | — (rg only) | Playwright |
| **React Native / Expo** | the React lane's libraries + `@react-native-community/netinfo` | the React lane + offline | the navigator's error screen | — | RNTL with the API client mocked per state |
| **Flutter** | `FutureBuilder`, `StreamBuilder`, Riverpod `AsyncValue`, `BlocBuilder` | `ConnectionState.waiting`, `hasError`, `.when(loading:, error:)` | — | — | widget test with a fake repository per state |
| **Jetpack Compose** | `collectAsStateWithLifecycle` over a sealed `UiState` | exhaustive `when` over Loading / Empty / Error | — | — | Compose UI test fed a fake `StateFlow` per state |
| **SwiftUI / UIKit** | `.task {}` + an enum state, `AsyncImage` phases | `switch` covering `.loading`, `.empty`, `.failure` | — | — | XCTest per enum case |

## Pre-flight greps

Run as **one** script from the repo root, because shell state does not survive between tool calls. Grep **N** feeds detector **§N**; grep 0 is context. Every `rg` names its path. Any `rg` error on stderr (exit 2) is a failed grep, never zero hits. `ROOTS` = the directories whose `package.json` names a UI framework; mobile lanes (grep M) search `.` by language.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|react-native|expo|vue|svelte|@angular/core|solid-js|preact|astro)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) )
[ ${#ROOTS[@]} -gt 1 ] && ROOTS=( $(printf '%s\n' "${ROOTS[@]}" | grep -vx '\.') ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,.next,.nuxt,.svelte-kit,.output,coverage,storybook-static,.dart_tool,Pods,DerivedData}/**' -g '!**/*.{min.js,md,mdx,lock,map,snap,json,svg}')
# Never a surface: tests, stories, mocks, fixtures, e2e probes, scripts/tools, catalogs, generated clients, docs, ai/.
T=(-g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,fixtures,__fixtures__,stories,playwright,cypress,locales,i18n,generated,__generated__,scripts,tools,bin}/**'
   -g '!**/*.{spec,test,stories,story,e2e,mock,test-data,fixture,fixtures}.*' -g '!**/*_test.dart' -g '!ai/**' -g '!docs/**')
C=(-g '*.{tsx,jsx,vue,svelte,astro}' -g '*.component.html')
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
# rg exit 2 is a failed grep: halt loudly, never print the empty list that would make greps 1, 3a, 4a and 15 silent.
rgok() { [ "$1" -le 1 ] || { echo "BLOCKED: grep $2 failed (rg exit $1); every grep that reads the consumer list is void" >&2; exit 2; }; }
D='\b(?:useQuery|useSuspenseQuery|useInfiniteQuery|useSuspenseInfiniteQuery|useQueries|useSWR|useSWRInfinite|createQuery|createInfiniteQuery|injectQuery|useFetch|useAsyncData|useLazyFetch|useLazyAsyncData|httpResource|rxResource|use[A-Z]\w*Query)\s*[<(]'
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'   # a JSX-aware tag body: `[^>]*` stops at the `>` of an arrow handler

# 0a files that read data (a library primitive, or an effect that fetches); 0b the hooks built on them, followed two
#    hops (api hook → model hook); 0c consumers = component files calling either, printed with the hooks they call.
#    The hook names live in a file, and every `useX(` call is listed once and joined against it: an `\b(?:a|b|…)`
#    alternation of 1,718 names is past PCRE2's compiled-pattern limit, and its unchecked exit 2 once cut 454 consumers
#    to 2. A word match (`rg -w -F -f`) is no substitute: it adds every `ReturnType<typeof useX>` presenter (680, not 454).
{ rg -l --pcre2 "$D" "${X[@]}" "${T[@]}" "${ROOTS[@]}"
  rg -l --pcre2 '\b(?:useEffect|onMounted|onMount|ngOnInit|useFocusEffect)\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg -l --pcre2 '\bfetch\(|\baxios\b|\bky\b|\$fetch\(|\b(?:api|apiClient|client|http)\.(?:get|post|put|patch|delete|request)\b|\bget<'
} | sort -u > "$W/def"; cp "$W/def" "$W/hookfiles"; : > "$W/names"
for hop in 1 2; do
  { cat "$W/names"; tr '\n' '\0' < "$W/hookfiles" | xargs -0 -r rg -o --no-filename -r '$1' --pcre2 'export\s+(?:async\s+)?(?:function|const)\s+(use[A-Z]\w*)'; } | sort -u > "$W/n"; mv "$W/n" "$W/names"
  rg -o -H -N --no-heading -r '$1' '\b(use[A-Z]\w*)\s*\(' -g '*.{ts,js,mjs}' "${X[@]}" "${T[@]}" "${ROOTS[@]}" > "$W/calls"; rgok $? "0b hop $hop"
  awk -F: 'FILENAME == ARGV[1] { n[$1]; next } ($NF in n) { print $1 }' "$W/names" "$W/calls" >> "$W/hookfiles"; sort -u -o "$W/hookfiles" "$W/hookfiles"
done
rg -l --pcre2 "$D" "${C[@]}" "${X[@]}" "${T[@]}" "${ROOTS[@]}" > "$W/c"; rgok $? 0c
rg -o -H -N --no-heading -r '$1' '\b(use[A-Z]\w*)\s*\(' "${C[@]}" "${X[@]}" "${T[@]}" "${ROOTS[@]}" > "$W/calls"; rgok $? 0c
{ awk -F: 'FILENAME == ARGV[1] { n[$1]; next } ($NF in n) { print $1 }' "$W/names" "$W/calls"; grep -E '\.(tsx|jsx|vue|svelte|astro)$|\.component\.html$' "$W/def"; } >> "$W/c"; sort -u "$W/c" > "$W/cons"
hooks() { while IFS= read -r f; do printf '%s\t%s\n' "$f" "$( { rg -o --no-filename --pcre2 "$D" "$f"; rg -o --no-filename --pcre2 '\buse[A-Z]\w*(?=\s*\()' "$f" | grep -Fxf "$W/names"; } | sort -u | paste -sd, -)"; done; }
echo "0a $(wc -l < "$W/def") data files · 0c $(wc -l < "$W/cons") consumers"
# 0d shared state wrappers, global handlers, retry policy (decide §1–§4, §6, §12 before any read).
rg -n --no-heading --pcre2 'export\s+(?:default\s+)?(?:function|const|class)\s+\w*(?:QueryState|QueryBoundary|AsyncBoundary|DataState|StateBlock|ErrorState|EmptyState|ErrorBoundary)\b|new\s+(?:QueryCache|MutationCache|QueryClient)\(|\bthrowOnError\b|\buseErrorBoundary\b|\bnetworkMode\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
# 0e proof infrastructure already in the repo: MSW, network interception, offline emulation, per-state stories.
rg -l --pcre2 'from\s+["\x27]msw(?:/\w+)?["\x27]|\bpage\.route\(|\bcontext\.setOffline\(|msw-storybook-addon|\bsetupServer\(' -g '!**/node_modules/**' .

# 1-4. Consumers with no loading token (1), lists with no empty branch (2), no error token (3a), failure turned into
#      an empty value (3b a one-line `.catch` callback; 3c a catch block, either form, whose first statement empties a
#      setter, a store field `this.x` or a Vue ref `x.value`), 3d a query result whose `.data` is folded to `[]`/0/null
#      while the file never reads its wait or failure field (the presenter split at hook level), an error branch with
#      no way out (4a), routers with no error element (4b), Next pages with no error.tsx in any ancestor segment (4c).
tr '\n' '\0' < "$W/cons" | xargs -0 -r rg --files-without-match --pcre2 '\b(?:isPending|isLoading|isFetching|isInitialLoading|pending|loading|status\s*===?\s*["\x27](?:pending|loading)|aria-busy|Skeleton\w*|Spinner|<Suspense|\{#await|@defer|\.isLoading\(\))\b' | hooks
tr '\n' '\0' < "$W/cons" | xargs -0 -r rg -l --pcre2 '\.map\(|v-for=|\{#each\b|@for\s*\(|\*ngFor=' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\.length\b|\bisEmpty\b|@empty\b|\{:else\}|v-else\b|\bEmpty\w*|\bNoResults\w*|\bempty\w*\s*[=:]|\bempty\b'
tr '\n' '\0' < "$W/cons" | xargs -0 -r rg --files-without-match --pcre2 '\b(?:isError|isRefetchError|isLoadingError|error|errors|status\s*===?\s*["\x27]error|ErrorState|ErrorBoundary|hasError|\.error\(\)|onError|throwOnError)\b' | hooks
rg -n --pcre2 '\.catch\(\s*\(\s*\w*\s*\)\s*=>\s*(?:\[\]|null|\(\s*\{\s*\}\s*\)|set\w+\(\s*(?:\[\]|null)\s*\))\s*\)' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '(?:(?<![\w.])catch\s*(?:\([^)\n]*\))?|\.catch\(\s*(?:\(\s*\w*\s*\)|\w+)\s*=>)\s*\{(?:\s*(?://[^\n]*|if\s*\([^)]*\)))*\s*(?:set\w+\(\s*(?:\[\]|null|\{\}|["\x27]{2}|0)\s*\)|(?:this\.\w+|\w+\.value)\s*=\s*(?:\[\]|null|\{\}|["\x27]{2}|0)(?![\w.]))' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\bconst\s+(\w+)\s*=\s*(?!use(?:QueryClient|Translation|Memo|State|Callback|Ref|Form|Confirm|Navigate|Params|Location|SearchParams|Id|Context|Reducer)\b)(?!use\w*(?:Mutation|Create|Update|Delete|Save|Add|Remove|Toggle|Send|Upload))use[A-Z]\w*\s*[<(](?=[\s\S]*?\b\1\.data\b(?:\?\.[\w?.]+)?\s*(?:\?\?|\|\|)\s*(?:\[\]|0\b|\{\}|null\b|["\x27]{2}))(?![\s\S]*\b\1\.(?:isPending|isLoading|isError|error|status|isSuccess|isFetched|isPlaceholderData|failureReason|isLoadingError)\b)' -g '*.{ts,tsx,js,jsx}' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
tr '\n' '\0' < "$W/cons" | xargs -0 -r rg -l --pcre2 '\b(?:isError|error)\b' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\b(?:refetch|retry|onRetry|reset|resetErrorBoundary|invalidateQueries|reload|tryAgain|ErrorState|QueryBoundary|QueryState)\b'
rg -l --pcre2 'createBrowserRouter|createHashRouter|createMemoryRouter|RouterProvider|provideRouter|createRouter\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'errorElement|ErrorBoundary|errorComponent|withNavigationErrorHandler|ErrorHandler'
for r in "${ROOTS[@]}"; do find "$r" -path '*/node_modules' -prune -o -type f -name 'page.[jt]sx' -path '*/app/*' -print; done | while IFS= read -r p; do d=$(dirname "$p"); ok=0; while :; do ls "$d"/error.[jt]sx >/dev/null 2>&1 && { ok=1; break; }; case "$d" in */app|.|/) break ;; esac; d=$(dirname "$d"); done; [ $ok = 0 ] && echo "4c no error.tsx at or above: $p"; done

# 5. Independent widgets loaded all-or-nothing. 6. Where the app tells 401/403 apart (6a, a count) and its retry policy (0d).
rg -n --pcre2 'await\s+Promise\.all\(\s*\[|\buseQueries\s*\(|\bcombineLatest\(|\bforkJoin\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
rg -c --pcre2 '\b40[13]\b|[Ff]orbidden|FORBIDDEN|PERMISSION_DENIED|[Uu]nauthori[sz]ed|AccessDenied' "${C[@]}" -g '*.{ts,js}' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
# 7. Any network-state primitive at all (repo-level).
rg -n --pcre2 'navigator\.onLine|\bonlineManager\b|\buseOnline\b|\bisPaused\b|addEventListener\(\s*["\x27](?:online|offline)["\x27]|@react-native-community/netinfo|\bNetInfo\b|connectivity_plus|\bNWPathMonitor\b|ConnectivityManager|\bnetworkMode\b' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
# 8. Forms with no pending binding (8a); an action button whose own tag carries no disabled/loading (8b, JSX-aware);
#    optimistic cache writes with no restore (8c TanStack, 8d RTK Query).
rg -l --pcre2 '<form\b[^>]*\bonSubmit=|\(ngSubmit\)=|@submit(?:\.prevent)?=|\bonsubmit=|\bhandleSubmit\(' "${C[@]}" "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bdisabled=|aria-disabled|\bisPending\b|\bisSubmitting\b|useFormStatus|\bpending\b|\bsubmitting\b|\bloading\b|\bbusy\b'
rg -n -U --pcre2 "<(?:button|Button|IconButton|Pressable|TouchableOpacity)\b(?!$TB\b(?:(?:disabled|isDisabled|loading|isLoading|aria-disabled|busy)\b|(?:pending|isPending|submitting|isSubmitting)\s*=))$TB\bon(?:Click|Press)=\{\s*(?:\(\)\s*=>\s*)?(?:\w+\.)*(?:handle|on|do)?(?:[Ss]ubmit|[Ss]ave|[Pp]ay|[Cc]reate|[Rr]efund|[Ss]end|[Pp]lace|[Cc]heckout|[Tt]ransfer|[Pp]ublish|[Cc]harge|[Cc]onfirm)(?:[A-Z]\w*)?\(" "${C[@]}" "${X[@]}" "${T[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\bonMutate\s*:' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bonError\s*[:(]'
rg -l --pcre2 'updateQueryData\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\.undo\(\)'
# 9. Text that cannot wrap and is not truncated (a render candidate only).
rg -n --pcre2 'className=["\x27`{][^"\x27`}\n]*\bwhitespace-nowrap\b(?![^"\x27`}\n]*\b(?:truncate|text-ellipsis|overflow-(?:hidden|x-auto|auto|clip)))' "${C[@]}" "${X[@]}" "${T[@]}" "${ROOTS[@]}"
# 10. Dirty-tracking forms with no leave guard.
rg -l --pcre2 '\bisDirty\b|\.dirty\b|meta\.dirty|\bdirtyFields\b' "${C[@]}" "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'useBlocker|usePrompt|beforeunload|useBeforeUnload|onBeforeRouteLeave|beforeRouteLeave|beforeNavigate|canDeactivate|CanDeactivate|PopScope|BackHandler'
# 11. HTTP clients (read each for a timeout) and raw fetch with no signal or timeout.
rg -n --pcre2 '\baxios\.create\(|\bky\.(?:create|extend)\(|\bofetch\.create\(|\$fetch\.create\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\bfetch\(' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'AbortSignal\.timeout|\bsignal\b|\btimeout\b'
# 12. A background refetch that blanks the data it already has.
rg -n --pcre2 'if\s*\([^)\n]*\bisFetching\b[^)\n]*\)\s*(?:\{\s*)?return\b|\bisFetching\s*\?\s*\(?\s*<\w*(?:Skeleton|Loading)\w*' "${C[@]}" "${X[@]}" "${T[@]}" "${ROOTS[@]}"
# 13. A destructive call wired straight to the control (a call that stages a confirm — set/ask/open… — is not matched).
rg -n --pcre2 '(?:onClick|onPress|onPressed|@click|v-on:click|\(click\)|onclick|on:click)\s*[=:]\s*["{]?\s*(?:\(\)\s*=>\s*)?(?:\w+\.)*(?:handle|on|do)?(?:[Dd]elete|[Rr]emove|[Dd]estroy|[Aa]rchive|[Pp]urge|[Rr]evoke|[Dd]iscard)(?:[A-Z]\w*)?(?:\.mutate(?:Async)?)?\((?!\s*(?:i|idx|index)\s*\))' "${C[@]}" -g '*.dart' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
# 13f follows each grep-13 handler to its definitions three directories up (the feature's model hook): a confirm or an
#     undo in the first 8 body lines dismisses the hit; NO-CONFIRM rows on a server call and NO-DEF rows are what to read.
rg -n -o --no-heading -r '$1' --pcre2 '(?:onClick|onPress|onPressed|@click|v-on:click|\(click\)|onclick|on:click)\s*[=:]\s*["{]?\s*(?:\(\)\s*=>\s*)?(?:\w+\.)*((?:handle|on|do)?(?:[Dd]elete|[Rr]emove|[Dd]estroy|[Aa]rchive|[Pp]urge|[Rr]evoke|[Dd]iscard)(?:[A-Z]\w*)?)(?:\.mutate(?:Async)?)?\((?!\s*(?:i|idx|index)\s*\))' "${C[@]}" -g '*.dart' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | while IFS=: read -r f l h; do
  rg -n -A8 --pcre2 "\b(?:const|let|function)\s+$h\b|\b$h\s*[:=]\s*(?:async\s*)?(?:\([^)\n]*\)|\w+)\s*=>(?!\s*(?:void|Promise|unknown|boolean)\b)|^\s*(?:async\s+)?$h\s*\([^)\n]*\)\s*\{" -g '*.{ts,tsx,js,jsx,vue,svelte,dart}' "${X[@]}" "${T[@]}" "$(dirname "$(dirname "$(dirname "$f")")")" | awk -v h="$h" -v at="$f:$l" 'function out(){ if (loc != "") print "13f " (ok ? "confirm/undo " : "NO-CONFIRM   ") at "  " h " → " loc } /^--$/{ next } match($0, /^[^:]*:[0-9]+:/){ out(); loc = substr($0, 1, RLENGTH - 1); ok = 0 } /[Cc]onfirm|[Uu]ndo/{ ok = 1 } END{ if (NR == 0) print "13f NO-DEF       " at "  " h " (read the parent that passes it)"; out() }'; done
# 14. Validation that fires while typing (14a); field errors from the server never mapped to fields (14b).
rg -n --pcre2 'useForm\s*(?:<[^>]*>)?\(\s*\{[^}]*\bmode\s*:\s*["\x27](?:onChange|all)["\x27]|@if\s*\(\s*\w+(?:\.controls\.\w+|\.get\([^)]*\))\??\.(?:errors|invalid)\s*\)|validateOnInput\s*:\s*true' "${X[@]}" "${T[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\b422\b|fieldErrors|\bfield_errors\b|\bviolations\b' "${C[@]}" -g '*.{ts,js}' "${X[@]}" "${T[@]}" "${ROOTS[@]}" | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\bsetError\(|\bsetErrors\(|\bsetFieldError\(|setFields\('
# 15. Detail consumers (they read a route param) that never tell "not found" apart.
tr '\n' '\0' < "$W/cons" | xargs -0 -r rg -l --pcre2 '\buseParams\b|\$route\.params|useRoute\(\)\.params|\bpage\.params\b|ActivatedRoute|\bparams\.\w+' | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\b404\b|notFound|NotFound|not[_-]found|NOT_FOUND|statusCode\s*:\s*404|error\(\s*404'
# M. Mobile lanes: Flutter builders with no error arm (Ma), forced unwraps of async values (Mb), Compose collectors
#    with no Loading/Error arm (Mc), SwiftUI tasks with no failure case (Md).
rg -l --pcre2 '\b(?:FutureBuilder|StreamBuilder)\b' -t dart "${X[@]}" "${T[@]}" . | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 'hasError|snapshot\.error|ConnectionState\.\w+'
rg -n --pcre2 '\.requireValue\b|\.value!\s*[.;)]' -t dart "${X[@]}" "${T[@]}" .
rg -l --pcre2 'collectAsState(?:WithLifecycle)?\(' -t kotlin "${X[@]}" "${T[@]}" . | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\b(?:Loading|Error|Empty|isLoading|errorMessage)\b'
rg -l --pcre2 '\.task\s*(?:\(id:[^)]*\))?\s*\{|\bAsyncImage\(' -t swift "${X[@]}" "${T[@]}" . | tr '\n' '\0' | xargs -0 -r rg --files-without-match --pcre2 '\.failure\b|case\s+\.error|\bProgressView\b|\bisLoading\b|ContentUnavailableView'
```

Greps 1–4, 10 and 15 are **file-level absence** checks (a set difference, never `rg -L`, which is `--follow`). They see one file. Three blind spots are structural, so work around them rather than trust a quiet grep:

- **The presenter split.** A container calls the hook and hands the whole result to a view (`<OrdersView vm={vm} />`); the view branches. The container is a hit and the view is not a consumer. Read the view before deciding. The reverse split, a model hook that exports only `query.data ?? []` and drops the state fields, is invisible to every file-level grep; grep 3d lists it at hook level.
- **The hook definition is not the surface.** Measured on two fixtures, a file-level grep over `useQuery` callers flags the hook files (3/3 and 2/2) and never the components. Grep 0b follows the exported hooks two hops so the consumers are what grep 1 lists, printed beside the hooks they call. A hit's verdict is decided where the hook's result is rendered.
- **Gate hooks.** A permissions or feature-flag hook read only to show or hide a control renders no data view. One read of the hook (does it default safely while loading?) dismisses its whole group.

**Measured** (2026-10-15, the app of the next paragraph, now inside a real NestJS + React monorepo). The hop-2 name list reached 1,718 hooks (34.5 KB); as one PCRE2 alternation it failed to compile (`regular expression is too large`, exit 2, unchecked), 0c fell to 2 consumers and greps 1, 2, 3a, 4a and 15 printed 0 with no error. The file-and-join form returns 454, the same set a 300-name chunked run gives, in about 6 s (452 once `*.test-data.*` fixture files joined T), and any rg exit 2 now halts the script. Grep 2 fell from 51 to 38 once `emptyMessage=`-style props count as an empty branch (22 of the 51 call a wrapper that owns the empty branch; the 13 dropped pass it an `empty…=` prop). Grep 8b fell from 5 buttons to 4 (the house `<Button pending={…}>` disables itself). Grep 3d returns 203 declarations, about 30 of them summary, list or total names; it carries the presenter-split rows first found only by reading (a till's "today's orders" `data ?? []`, high; a returns summary and a report panel folding to 0, medium). Grep 13f prints 64 definition rows for the 43 grep-13 hits: 17 `confirm/undo` (the handler awaits the confirm provider), 9 `NO-DEF` (no definition three directories up), and 38 `NO-CONFIRM`, which are 37 local-row removals plus the one server revoke with no confirm. The fixtures return the same counts as before (0c, 3a, 3c, 8b seeds unchanged).

**Measured** (2026-10-05). On a real React 19 + Vite + React Router 7 + TanStack Query 5 web app (about 4,750 source files, a shared `QueryBoundary` wrapper, a global `QueryCache` handler, an offline banner), the script runs in about 3 s and returns: 0a 178 data files, 0c 423 consumers; grep 1, 57 files in 50 hook groups (12 call nothing but one gate hook, `usePermissions`); grep 2, 41; grep 3a, 99 files in 90 groups; greps 3b+3c, 5 lines, all `catch → null` followed by a warning toast or a fallback label (5/5 Refuted on read); grep 4a, 30; grep 4b, 1 (a comment that names `RouterProvider`; the real router file carries `errorElement` and is not listed); grep 8b, 5 buttons (the two read close their dialog on the first click or open a payment form: Refuted); grep 9, 80; grep 15, 15; grep 12, 0 after the inline-refetch-spinner shape (`isFetching ? <Spinner/> : null`, the correct one) was dropped from the pattern; grep 13, 47 lines, most of them unsaved local rows (`removeDraft(d.key)`, `vm.removeLine(line.id)`), and the server deletes read so far await the app's confirm provider inside the handler. Before `scripts/` was excluded, grep 3b returned 177 lines, nearly all `.catch(() => {})` in Playwright probe scripts. On the fixtures: `web-dashboard` grep 3a returns the seeded detail panel (no error state, loading forever) and grep 3c the seeded data hook (`catch → setData([])`); `review-decoys/change` grep 8b returns exactly the seeded dialog line (its `pending` drives the label, not `disabled`), and not the decoy beside it (`disabled={saving}`); grep 8b missed the seeded row while it was a file-level check, because the file reads `pending`. On `quality-mix`, grep 3b returns the seeded invoices hook's catch (QM-EH-03, owned by `error-handling-scan` § 2; credited here as corroboration). `slow-marketplace` and `quality-mix` seed no state rows, so their page hits are unscored candidates. On a scratch set of one positive and one decoy per mobile lane (Flutter, Compose, SwiftUI, React Native), grep M and grep 3a return 4/4 positives and 0/4 decoys.

## The 3,000-hit path

1. **Intersect** with the route table (router config, `app/**/page.*`, `src/routes`, the navigator). A consumer no route or screen reaches is dismissed with one read. Storybook-only and design-system-internal files go in their own group.
2. **Group** by the hook (grep 1 and 3a print it) and by the shared wrapper. One read of the hook and one consumer settles the group. A defect in a shared wrapper is **one** finding, however many surfaces use it: fixing the wrapper closes them all.
3. **Rank** by route traffic (RUM or analytics when present), else landing, auth, checkout-class, list, detail and form routes first.
4. **Read the top 30 groups fully.**
5. **Prefer the runtime bulk oracle at scale:** the state sweep (§ Proof) over every route, one run per state. One run confirms or refutes whole groups. Many mature repos already ship a fault-sweep or crawl script (grep 0e); reuse it.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never mark them `checked`.

## Scans for

Severity assumes a reachable surface and a state that can occur. Raise one step on money, permissions or irreversible flows; lower one step on an internal admin surface with a stated audience.

| § | Class | Default |
|---|---|---|
| 1 | No loading state, or a loader that shifts layout (CLS) | medium; low when the data is local and fast by construction |
| 2 | No empty state: the list renders blank | medium |
| 3 | Error rendered as empty, or not at all | high on a primary list or detail |
| 4 | Error with no way out; a route or subtree with no error boundary | high at the root, medium per leaf |
| 5 | One failing part takes the whole page down | medium |
| 6 | Permission-denied shown as a generic error or as empty; 401 with no way back | medium; high when the copy invites a retry loop |
| 7 | Offline: no indicator; a write lost silently | low; high when the product claims offline or PWA |
| 8 | Submit with no pending state: double submit, inputs lost on failure; optimistic write never rolled back | high on create, pay or irreversible; low on search |
| 9 | User data breaks the layout (long names, emails, numbers) | low; medium when a primary action is pushed off-screen |
| 10 | Unsaved changes lost on navigation | medium for long forms |
| 11 | Loading never ends: no timeout, or a paused request shown as pending | medium |
| 12 | Stale data with no indicator, or a background refetch that blanks the data | low–medium |
| 13 | Destructive action with no confirmation or undo (SC 3.3.4 for data deletion) | high when the server deletes |
| 14 | Validation errors while typing; server field errors never mapped to fields | medium |
| 15 | A missing record rendered as a generic error or a crash, not "not found" | medium; high on SSR where the status code is wrong |

### 1. No loading state
```
BAD:   const { data } = useQuery(q); return <Table rows={data ?? []} />        // empty table, then rows: a lie, then a jump
GOOD:  if (isPending) return <TableSkeleton rows={10} />                       // sized like the result, aria-busy
```
**Read the code:** Does a parent render the loading state (`<Suspense>` with a fallback, the shared wrapper, a `loading.tsx`)? Is the skeleton sized like the result, or does a spinner give way to a taller table? Is the query disabled until an id exists (`enabled: !!id`)? Then idle is not loading, and the view must say which it is. **Finding when** the surface renders the empty or zero state while the request is in flight. **Proof:** hold the request (`delay('infinite')`); assert a `role=status` / `aria-busy` region, no empty copy, and a layout-shift sum under 0.1 when it resolves (`proof-oracles.md` § Frontend, layout shift).

### 2. No empty state
```
BAD:   return <ul>{orders.map(o => <Row key={o.id} o={o} />)}</ul>             // [] → a blank panel
GOOD:  if (orders.length === 0) return <Empty title="No orders yet" action={<NewOrder />} />
```
`@empty` (Angular), `{:else}` (Svelte) and `v-else` (Vue) count as the branch, and so does an `empty…=` prop handed to a shared table or wrapper that draws it. **Read the code:** Does the empty branch distinguish "no data yet" from "no match for this filter"? Both need copy, and the filtered one needs a way to clear the filter. **Proof:** respond `[]`; assert the empty copy and its action are visible.

### 3. Error rendered as empty, or not at all
```
BAD:   .catch(() => setItems([]))                 // a 500 is now "no items"
       const { data } = useQuery(q); if (!data) return <p>Loading…</p>      // a failure is a spinner forever
GOOD:  if (isError) return <ErrorState error={error} onRetry={refetch} />
```
**Read the code:** Does the hook keep the error and return it, and does the view read it? A grep 3d row is a hook that hands on `data ?? []` (or `?? 0`) with no state field at all: read who renders it, and rank list, summary and total names before option lookups. A global toast over a blank list is still this class. `catch → null` followed by a branch that tells the user is not. **Finding when** a failed read renders the empty state, the loading state, or nothing. **Proof:** respond 500 and, separately, a network error (`HttpResponse.error()` / `route.abort('failed')`); assert an error role and that the empty copy is **not** shown.

### 4. Error with no way out; no error boundary
```
BAD:   if (isError) return <p>Error</p>                          // no retry, no back, no support path
       createBrowserRouter([{ path: '/', element: <Shell/> }])     // a render throw blanks the app
GOOD:  <ErrorState onRetry={refetch} /> · errorElement: <RouteError/> · app/(shop)/error.tsx
```
**Read the code:** Which errors does a retry fix (5xx, network) and which it never fixes (403, 404, 422)? Is the retry offered only for the first kind? Does the boundary wrap each route or independent widget, or only the root? Next.js: an `error.tsx` in a segment wraps that segment's page but not its layout, and the root layout needs `global-error.tsx` (grep 4c walks the ancestors). Event-handler and async errors are not caught by boundaries. **Proof:** after a 500, the retry control refetches and the view recovers; a child that throws renders the boundary and the shell (navigation) stays usable, with `page.on('pageerror')` recorded.

### 5. One failing part takes the page down
```
BAD:   const [kpis, feed, alerts] = await Promise.all([getKpis(), getFeed(), getAlerts()])
GOOD:  Promise.allSettled, or one query per widget, each with its own error state
```
**Read the code:** Are the parts truly independent, or does the page need all of them (a form needing every lookup)? `useQueries` with one combined error branch has the same shape. **Proof:** fail one of N endpoints; the other N−1 widgets render and the failed one shows a local error.

### 6. Permission-denied rendered as a generic error or as empty
```
BAD:   if (isError) return <p>Something went wrong. <button onClick={refetch}>Retry</button></p>   // a 403, retried forever
GOOD:  if (error.status === 403) return <NoAccess requestAccess={…} />  ·  401 → login with ?returnTo=
```
**Read the code:** Where does the app tell 401, 403 and 404 apart: the API client, the wrapper, or nowhere (grep 6a is the count)? Does the query client retry 4xx? TanStack Query retries a failed query 3 times by default, with backoff, so a 403 shows a spinner for several seconds before the error (grep 0d shows the retry policy). Where one view tells a 403 apart (its own copy, a verify or request-access action), read every sibling view behind the same gate (the same account, workspace or role area): a sibling that sends its `isError` straight to a generic retry is a §6 candidate, Unconfirmed until that endpoint's refusal is documented or observed. **Finding when** a refusal renders as a retryable error, as empty, or as a crash. **Proof:** respond 403 (and 401); assert distinct copy, no retry control, a request count of 1 (`page.route` counter), and for 401 a redirect that carries the return path.

### 7. Offline
```
BAD:   save() while offline → spinner, then nothing; the edit is gone
GOOD:  an offline banner from the network-state primitive; the write is rejected with a message or queued and shown as queued
```
**Read the code:** Does any network-state primitive exist (grep 7)? With TanStack Query's default `networkMode: 'online'`, a query or mutation started offline is **paused**, not failed: a view that reads only `isPending` shows an endless spinner (§11). Mobile: does the screen read NetInfo / connectivity and say so? Queue durability is the mobile pack's (§ Boundaries). **Proof:** `context.setOffline(true)` (Playwright) or the NetInfo mock; trigger the write; assert the offline message and that, back online, a paused write is sent exactly once (request counter).

### 8. Submit with no pending state; optimistic write never rolled back
```
BAD:   <button type="button" onClick={() => submit(amount)}>{pending ? 'Refunding…' : 'Refund'}</button>   // label only
GOOD:  <button disabled={pending} …>  ·  useFormStatus / formState.isSubmitting  ·  an Idempotency-Key on the request
```
**Read the code:** Is the whole chain covered — the mutation, the navigate after it — or does `isSubmitting` reset before the request ends (react-hook-form's flag lasts only while the `handleSubmit` callback's promise is pending, so an un-awaited `mutate()` ends it immediately)? Does Enter in a field resubmit? On failure, are the inputs kept? **8c/8d (optimistic):** an `onMutate` that writes the cache with no `onError` restore, or an RTK `updateQueryData` never `.undo()`ne. Optimistic UI rendered from `variables` while pending, React 19 `useOptimistic`, Apollo `optimisticResponse` and SWR `optimisticData` (with the default `rollbackOnError`) revert by themselves. **Proof:** two clicks (or `dblclick`, or Enter twice) under a held response → one request (route counter); a 500 → inputs still filled and an error shown; for 8c, the optimistic row appears, then disappears with an announced error.

### 9. User data breaks the layout
**Read the code:** Which fields hold user data (names, emails, addresses, amounts)? Do their containers wrap, truncate with a full-text affordance, or push the primary action off-screen? This is a rendered class: a grep 9 line is a candidate for the render, never a finding. **Proof:** a fixture with 120-character values and a 7-digit amount, rendered at 320 CSS px; assert no horizontal overflow on the surface and the primary action in view. No render: `blocked (no harness)`.

### 10. Unsaved changes lost on navigation
**Read the code:** Is the form long enough that losing it costs real work? Guards by stack: React Router `useBlocker`; Vue Router `onBeforeRouteLeave`; SvelteKit `beforeNavigate`; Angular `CanDeactivateFn`; `beforeunload` for tab close. Next.js App Router: confirm against the docs for the installed version before claiming a built-in. Autosave or a persisted draft is the alternative: verify a reload restores the values. **Proof:** fill a field, click a nav link and go back; assert a confirm (and `page.close({ runBeforeUnload: true })` for tab close). After a successful save, navigation must **not** prompt.

### 11. Loading never ends
**Read the code:** Does the HTTP client set a timeout (grep 11)? Read each client: some libraries default to one and others to none, so check the installed version's docs rather than assume. A raw `fetch` has none unless it passes `AbortSignal.timeout`. Is a paused (offline) query rendered as loading? **Proof:** hold the response past the client's timeout; assert the error state replaces the loader.

### 12. Stale data, or a refetch that blanks it
```
BAD:   if (isLoading || isFetching) return <Skeleton/>     // every background refetch wipes the list
GOOD:  rows stay; an inline "Updating…" with aria-busy; a stale notice when the refetch fails and data remains
```
`isFetching` is true on every background refetch. `keepPreviousData` became `placeholderData: keepPreviousData` in TanStack Query 5. **Read the code:** When a refetch fails while data is cached, does the view keep the rows **and** say they may be stale (`isRefetchError`), or replace them with a full-page error? **Proof:** serve v1, then fail the refetch; assert the old rows are visible with a stale indicator. For pagination, the layout-shift sum while moving page to page stays under 0.1.

### 13. Destructive action with no confirmation or undo
```
BAD:   <Button onClick={() => deleteOrder(o.id)}>Delete</Button>
GOOD:  onClick={() => setPendingDelete(o)} → <ConfirmDialog …/>  ·  soft delete + an Undo toast
```
**Read the code:** Follow the handler into its body: many apps await a confirm provider there (`await confirm(…)`), which grep 13 cannot see; grep 13f does the first hop and prints each definition as `confirm/undo`, `NO-CONFIRM` or `NO-DEF`. Is it a server delete, or the removal of an unsaved local row, a filter chip, or an attachment not yet uploaded (not destructive)? Bulk delete, a keyboard Delete shortcut and swipe-to-delete are the same class. **Proof:** click once; assert a dialog (`getByRole('alertdialog'|'dialog')`) or an Undo `status`, and a DELETE request count of 0 before confirming.

### 14. Validation while typing; server field errors not mapped
**Read the code:** react-hook-form `mode: 'onChange' | 'all'` validates on the first keystroke; `onTouched` validates on first blur, then on change. Angular: errors shown with no `touched || dirty` guard. Does a 422 response reach `setError(field, …)` (or the library's equivalent), or only a toast? Password strength, availability checks and character counters are meant to be live. **Proof:** type one character into the email field; assert no `aria-invalid="true"` until blur. Respond 422 `{fieldErrors: {email: 'taken'}}`; assert the field is `aria-invalid` and described by the message.

### 15. Not-found conflated with error
**Read the code:** On a detail route (`:id`, `[id]`, `[slug]`), does the loader or view distinguish a missing record? Next `notFound()`; React Router `throw data(null, { status: 404 })` + `isRouteErrorResponse`; SvelteKit `error(404, …)`; Nuxt `createError({ statusCode: 404 })`; a client view branching on `error.status === 404`. An SPA served with a history fallback returns HTTP 200 for every path: assert the content, not the status. **Proof:** open `/orders/does-not-exist`; assert a not-found heading with a way back, and on SSR `response.status() === 404`.

## Proof — the state-matrix test

The oracle is [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Accessibility and UI states, *State matrix* (V105): one MSW 3 handler module per endpoint (`loading`, `empty`, `error500`, `network`, `forbidden`, `notFound`, `partial`) shared by the component test, the story and the browser test, with the role and copy each state must show. The same section carries the MSW 3 import and Node ≥ 22.12 notes, the Playwright route-and-offline form with no MSW, and the two forms this skill leans on most:

- **The state sweep (the bulk oracle):** each route × each state in {500, network, 403, `[]`, held, offline}; an error or status role is present, the empty copy is absent under an error, and no page error fired. One run per state confirms or refutes whole groups.
- **Mobile:** RNTL, a Flutter widget test, a Compose UI test or an XCTest per state, as listed there.
- **Failing first.** The test fails on the unfixed surface. A test that passes before the fix proves nothing; rebuild it until it fails.

**Whole-class variants** a fix must survive: list, detail and infinite list (a page-2 failure is §5); a refetch-on-focus failure while data is shown (§12); a dependent query that is idle, not loading; the dialog and the drawer, not only the page; the second locale and RTL; dark theme; 320 px; both mobile platforms (V105's variant list).

## Output

```
ui-state-scan — lanes: react 19.2 + @tanstack/react-query 5.102 + react-router-dom 7.18 (apps/web/package.json); vue, svelte, angular, mobile absent
Context: 423 consumers · wrappers: QueryBoundary, ErrorState, EmptyState · QueryCache onError (toast) · retry: shouldRetryQuery · harness: Playwright 1.63, Storybook 10.6, no MSW
Matrix: ai/runs/20261005-refunds-9c1e/ux.md § State matrix (3 surfaces)

Findings: 2 · Unconfirmed: 1

1. src/features/refunds/RefundModal.tsx:19                           [report-with-fix]   high
   §8 double submit — the Refund button binds `pending` to its label, not to `disabled`; a double click
   sends two POST /refunds (the API takes no idempotency key). Proof: e2e/refunds/states.spec.ts
   "one refund per double click" — route counter 2 (fails). Fix: disabled={pending}; send an
   Idempotency-Key (logic-race-scan § 4 owns the server side).

2. src/features/orders/useOrders.ts:24                                  [report-with-fix]   high
   §3 error rendered as empty — `.catch(() => setData([]))`; OrdersPage shows "No orders yet" on a 500.
   Proof: OrdersPage.states.test.tsx error → the empty copy is visible (fails). Fix: keep the error,
   render <ErrorState onRetry={refetch} />. Siblings: 1 more hook with the same catch (followup).

3. src/features/orders/detail/OrderDetailView.tsx:40                   [report-flagged]    medium
   §15 not-found — /orders/:id branches on isError only; a deleted order reads "could not load" with a
   Retry that never succeeds. Unproven link: the API's status for a missing order. Settling test:
   states.notFound on /orders/does-not-exist → a not-found heading, no Retry.

Verification: 14 candidates → 2 findings · 1 unconfirmed · 6 hardening · 0 pre-existing · 5 refuted

Class coverage:
  §1  loading                 checked (57 hits / 50 groups → 0 findings; usePermissions group: gate hook, safe default)
  §2  empty                   checked (41 hits → 0 findings) · Live, unreviewed (12 groups / 14 hits — continue with grep 2)
  §3  error as empty          checked (104 hits / 95 groups → 1 finding)
  §4  no way out / boundary   checked (31 hits → 0 findings; errorElement on every route)
  §5  partial failure         checked (10 hits → 0 findings)
  §6  permission              checked (status discrimination in the API client; 0 findings)
  §7  offline                 checked (offline banner present; 0 findings)
  §8  pending submit          checked (5 hits → 1 finding)
  §9  long content            blocked (no harness — 80 candidates need the 320 px render)
  §10 unsaved changes         checked (5 hits → 0 findings)
  §11 never-ending loading    checked (API client timeout read; 0 findings)
  §12 stale                   checked (0 hits)
  §13 destructive             checked (47 hits → 0 findings; local rows and confirm-provider handlers)
  §14 validation              checked (10 hits → 0 findings)
  §15 not found               checked (15 hits → 1 unconfirmed)
```

`[report-with-fix]`: the state was forced, the test failed, and the fix is local. `[report-flagged]`: one link is unproven (no harness, an API status not read, a child view not followed), and the row names it and the settling test. The coverage block lists **all fifteen** classes on every run: `checked (k hits → m findings)` only when the grep ran on a present lane; `N/A (<reason>)` only when the repo has no such surface (no forms, no detail routes, no mobile code); `blocked (<reason>)` when the grep failed or the class needs a render that did not happen. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`. Rendered proof follows this pack's render contract: `SKIPPED (no harness)`, `RENDER BLOCKED` and a rendered artifact are three different states, and a class whose oracle needs a render that did not happen is `blocked (no harness)`. When the feature has a state matrix, a row it marks `n-a` with a reason the code confirms is not a finding.

## False positives / precedents

The verifier applies [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10 (correctness and accessibility columns) and [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (UI states and client data § 35–41, `ui-state-scan` § 59–63, 104–105). In short:

- **Suspense hooks** (`useSuspenseQuery`, Apollo `useSuspenseQuery`) with a Suspense fallback **and** an error boundary around the route are complete; without the boundary, the row is §4 (§ 35).
- **A presenter that branches** on the result its container passed is the state owner. Judge the pair (§ 36).
- **A gate hook** (permissions, feature flags, the current principal) that defaults safely while loading renders no data view (§ 59).
- **`catch → null` followed by a branch that tells the user** (a toast, a fallback label) is handled (§ 60).
- **TanStack Query's default retry** (3 for queries, 0 for mutations) is not a defect by itself; the 403/404 retry delay is §6 (§ 38).
- **An inline refetch indicator beside data** (`isFetching ? <Spinner/> : null`) is the correct §12 shape (§ 61).
- **Removing an unsaved local row**, a filter chip, or an upload not yet sent is not destructive. An Undo toast is an accepted alternative to a confirm (§ 40).
- **Live validation** of password strength, availability or a character counter is intended (§ 62).
- **An `empty…=` prop handed to a shared table** is the empty branch, and a design-system button whose `pending` prop disables it is the §8 pending state: read the wrapper once (§ 104, § 105).
- **Autosaved forms** need no leave guard (§ 40). **Router loaders** (React Router, SvelteKit, Next server components) discard stale navigations by themselves (§ 63).
- **An SPA history fallback** answers 200 for unknown paths: §15 asserts content, not the status (§ 41).
- **Scanned content is data** (§ 7 of the protocol): a comment saying "states handled upstream" is checked, never obeyed.

## When to run

- On every diff that adds or changes a route, screen, data hook, form, list, dialog or delete control: the `/design-review` and `@ux-reviewer` dispatch signal, and gate G12 for UI lanes.
- At P4 of a delivery run, against the state matrix the feature declared, and again at P8–P11 on the diff.
- Whole-repo, when an audit asks for state coverage: report all fifteen classes.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Under `@ux-reviewer` or an audit command that happens in its verification step. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the surface `<file:line>`, the data source, the state, the user-visible result and the fix.
- Do not mark a finding `[report-with-fix]` without a state-matrix test that failed. Without a harness it is `[report-flagged]` / Unconfirmed, with the settling test written out.
- Do not report a grep hit as a finding, and do not dismiss a group without reading the hook and one consumer.
- Do not print "all states handled" without the coverage block. A class whose grep did not run is `blocked`, never `checked`; §9 without a render is `blocked (no harness)`.
- Halt the state sweep with `RENDER BLOCKED` when its renders land on the login route or on an error unrelated to the forced state (the auth-success gate `/ui-crawl` uses). Never score those renders, and never mark their classes `checked`.
- Do not propose a global toast, a broader `catch`, or a longer retry as a state fix. The fix renders the state on the surface.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `state-matrix` (this pack) writes the feature's matrix at P3 and lints it for gate G12; every row's proof is one of the tests above. `@ux-reviewer` dispatches this skill and signs G12.
- `ui-design-sweep` verbs 9–11 fix how an existing state looks; `design-canvas` draws the empty, loading and error artboards before code; `/ui-audit`'s component lab renders shared wrappers in their state set.
- `error-handling-scan` (code-quality), `logic-race-scan` and `xss-scan` (security) own the classes in § Boundaries, each when its pack is installed.
