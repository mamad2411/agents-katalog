---
name: render-correctness-scan
description: Render bugs — React Compiler rule breaks, effects with no cleanup (SPA memory growth), index keys, lost reactivity, controlled-input flips; each test-proved.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: render-correctness-scan

## Premise

A render bug shows the wrong thing, or keeps doing work after the user has left. The UI renders twice with a stale value, a row keeps the text typed into its neighbour, a store change never reaches the view, an input jumps from uncontrolled to controlled and drops a keystroke. A listener, interval or subscription outlives the component that started it. None of these is visible in a screenshot of one state, and none fails a type check. The class that costs the most is the last one: every navigation leaves another listener behind, so the heap of a single-page app grows until the tab slows down. That is the **SPA memory growth** row `/bundle-perf` lists as X1a, and §2 owns it.

**Every finding cites the component `<file:line>` + the rule or pattern it breaks + the route or component that mounts it + the oracle that failed (or the test that would settle it) + the fix in the project's framework.** A lint message or a grep hit is a candidate, never a finding by itself. "No render bugs found" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by execution.** Each class has a deterministic oracle — a render count, a timer and listener balance, a heap slope across navigations, a reorder test, a console warning — in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § "Mount/unmount balance, reorder identity, request order", *Heap slope*, *Console warning* and *View update* (§ Accessibility and UI states), and § "Render count" (frontend). A candidate read in code with no harness to run the test is **Unconfirmed**, carrying the test that would settle it. It is never dropped as "speculative" and never promoted on reading alone ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The rule

A candidate is a finding when all four hold:

1. **It renders.** A real route or screen mounts the component. Storybook-only files, design-system docs pages and dead components fail here (`precedents/ui.md` § 10).
2. **The trigger occurs.** The prop really changes, the list really reorders or loses a row, the user really navigates away and back, the value really starts `undefined`. A list built once from a constant never reorders.
3. **No framework control already handles it.** The cleanup is managed by the framework (`precedents/ui.md` § 46), the compiler memoises the value, the store binding is reactive by construction (Vue 3.5 `defineProps` destructure, Svelte 5 `$props` read without mutation).
4. **The oracle fires, or would.** A failing test is a finding. A candidate whose test cannot run here is Unconfirmed with the test written out.

## Boundaries

- **`exhaustive-deps` and the stale closure inside one effect** → code-quality `correctness-smell-scan` §3, when the code-quality pack is installed. The lint lane here still runs `react-hooks/exhaustive-deps`; a hit both skills see is reported once, credited to both. Without that pack, report it here under §1.
- **Out-of-order responses, missing cancellation, mutations with no invalidation, server state copied into a global store** → `client-data-scan` (this pack) §3, §4 and §9. An effect that fetches belongs there unless the defect is the effect itself (a loop, a missing cleanup).
- **Re-render cost** (a whole-store selector, an unstable context value, a provider value literal) → performance `inp-responsiveness` § 3 when the performance pack is installed, proved by V52 in `proof-oracles.md`. §1 here keeps re-renders that change **what** is shown, not how fast. Without the performance pack, report it here tagged `performance-class (owner pack not installed)` (`precedents/ui.md` § 8).
- **Hydration mismatches, browser globals during SSR, module-scope state shared across requests** → `ssr-audit` (this pack). A leak in server code (a Node service, an SSR server's own caches) → performance `memory-growth-scan`, when installed.
- **Heap cost and ranking** of a confirmed §2 leak → `/bundle-perf` row X1 and `@performance-optimizer` (performance pack, when installed). This skill proves the leak exists; it does not rank its cost across routes.
- **Missing loading, error, empty or offline states** → `ui-state-scan` (ui-ux pack, when installed).

## Adapt to the codebase — the render lanes

Read the framework, the compiler and the lint plugins **with versions** from the lockfile, never from memory, and print the lanes in the output header. Key on API names, not majors: react-router is at 8.x, SvelteKit at 3.0 and Angular at 22 as of 2026-10-05 (npm registry, read that day), and the APIs below are unchanged in them.

| Lane | Lint lane (rule ids — the lane keeps only these `ruleId`s) | Cleanup primitive (§2) | Identity (§3) | Reactivity trap (§4) | Oracle harness |
|---|---|---|---|---|---|
| **React 19** (Next, React Router 7/8, Remix, Vite) | eslint-plugin-react-hooks **7.1.1**: `rules-of-hooks`, `purity`, `refs`, `immutability`, `set-state-in-render`, `set-state-in-effect`, `static-components`, `globals`, `use-memo`, `preserve-manual-memoization`, `error-boundaries`, `incompatible-library`, `unsupported-syntax`, plus opt-in **`no-deriving-state-in-effects`**; `exhaustive-deps` (credited §Boundaries). `@eslint-react/web-api/no-leaked-{event-listener,interval,timeout,resize-observer,intersection-observer,fetch}` (5.24.4) when installed; `react/jsx-key`, `react/no-array-index-key` (eslint-plugin-react 7.37.5) when installed | `return () => …` from `useEffect`; `AbortController` `signal` on listeners | `key` | in-place mutation then `setX(sameRef)` — §1 | Vitest/Jest + Testing Library; `<Profiler>` |
| **Vue 3.5 / Nuxt 4** | eslint-plugin-vue **10.11.1** essential: `no-mutating-props`, `require-v-for-key`, `valid-v-for`, `no-side-effects-in-computed-properties`, `no-async-in-computed-properties`, `no-ref-as-operand`, `no-watch-after-await`, `no-lifecycle-after-await`; opt-in `no-setup-props-reactivity-loss`, `no-ref-object-reactivity-loss` | `onUnmounted` / `onBeforeUnmount` / `onScopeDispose`; VueUse `useEventListener` | `:key` | destructured `reactive()` or store without `storeToRefs`; mutated props | Vitest + Vue Test Utils |
| **Svelte 5 / SvelteKit** | eslint-plugin-svelte **3.23.0**: `prefer-writable-derived`, `infinite-reactive-loop`, `require-each-key`, `valid-each-key`, `no-reactive-reassign`; compiler `state_referenced_locally`; runtime `effect_update_depth_exceeded`, `state_unsafe_mutation`, `ownership_invalid_mutation` | the function returned from `$effect` / `onMount` | `{#each … (key)}` | `$effect` assigning state that `$derived` should compute; a child mutating a non-bound `$props` value | Vitest + `@testing-library/svelte` |
| **Angular 20–22** (signals, control flow) | angular-eslint **22.5.0**: `no-uncalled-signals`, `computed-must-return`, `reactive-context-must-read-signal`, `no-implicit-take-until-destroyed`, `template/use-track-by-function`; rxjs-x 1.0.6 `no-nested-subscribe`, `no-unsafe-takeuntil`, opt-in `no-ignored-subscription` | `takeUntilDestroyed()`, `DestroyRef`, `async` pipe, `toSignal` | `@for (…; track item.id)` | `signal.update(a => { a.push(x); return a })` returns the same reference; a component opting out of OnPush and mutating | TestBed + `fakeAsync` |
| **Solid, Qwik, Preact, Lit** | none mapped — rg only | `onCleanup`, `useVisibleTask$` return, `disconnectedCallback` | `<For>` / `key` | — | the project's runner |

Lint lane, React (the other lanes take the same shape with their ids): run the **project's own** ESLint config with the rules switched on by `--rule`, because a config that loads the plugin often enables only `rules-of-hooks`, and keep only the lane's `ruleId`s. Without the plugin installed, the lane is `blocked (eslint-plugin-react-hooks not installed)` and the rg fallback below carries §1 alone; never install into the target repo — use a throwaway worktree.

```bash
# ROOTS as computed by the first line of § Pre-flight greps — run in the same shell, after it.
npx --no eslint -f json --rule '{"react-hooks/purity":"error","react-hooks/refs":"error","react-hooks/immutability":"error","react-hooks/set-state-in-render":"error","react-hooks/set-state-in-effect":"error","react-hooks/static-components":"error","react-hooks/globals":"error","react-hooks/use-memo":"error","react-hooks/preserve-manual-memoization":"error","react-hooks/error-boundaries":"error","react-hooks/no-deriving-state-in-effects":"error","react-hooks/unsupported-syntax":"warn","react-hooks/incompatible-library":"warn"}' "${ROOTS[@]}" > "${TMPDIR:-/tmp}/rc-lint.json"
jq -r '.[] | .filePath as $f | .messages[] | select((.ruleId // "") | test("^react-hooks/|^@eslint-react/web-api/|^react/(jsx-key|no-array-index-key)$")) | "\($f):\(.line) \(.ruleId)"' "${TMPDIR:-/tmp}/rc-lint.json" | sort | uniq -c | sort -rn | head -40
```

A file the compiler bails on (`unsupported-syntax`, `incompatible-library`) is a silent gap for every Compiler rule: list it as `blocked (compiler bailout)`, never as clean.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls). Grep **N** feeds detector **§N**. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. Files-without-match is `--files-without-match`, **never `-L`**, which in ripgrep means `--follow`; an `rg -L` printed the matches of a file that *does* remove its listener in this batch's own measurement. Any `rg` error on stderr (exit 2) is a failed grep, not zero hits.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|@builder\.io/qwik)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,scripts,tools,locales,i18n,generated,__generated__}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!ai/**' -g '!docs/**')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte}')
LC='useEffect|useLayoutEffect|useInsertionEffect|onMounted|onBeforeMount|ngOnInit|ngAfterViewInit|afterNextRender|\$effect|onMount\(|createEffect|connectedCallback|useVisibleTask\$'
TB='(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*'   # a JSX tag body that survives `onClick={() => x}`
PJ=(); [ -f package.json ] && [[ " ${ROOTS[*]} " != *" . "* ]] && PJ=(package.json)   # a workspace root holds the lint plugins
# 0. Lanes and versions; React Compiler on or off.
rg -n --no-heading '"(react|next|react-router(-dom)?|vue|nuxt|svelte|@sveltejs/kit|@angular/core|solid-js|eslint-plugin-react-hooks|babel-plugin-react-compiler|@eslint-react/eslint-plugin|eslint-plugin-react|eslint-plugin-vue|eslint-plugin-svelte|angular-eslint|eslint-plugin-rxjs-x|pinia|zustand)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${PJ[@]}" "${ROOTS[@]}"
rg -n --no-heading --pcre2 '["\x27](?:react-hooks|react-compiler|@eslint-react/[\w-]+|react)/[\w-]+["\x27]\s*:' -g '{eslint.config,.eslintrc}*' -g '!**/node_modules/**' .   # rules the config switches on
rg -n --no-heading 'reactCompiler|babel-plugin-react-compiler|react-compiler' -g '**/{next,vite,babel,rsbuild}.config.*' -g '**/.babelrc*' -g '!**/node_modules/**' "${ROOTS[@]}"
# 1. React/Compiler rules by rg (the lint lane is primary): 1a setState as an effect's first statement (derived state),
#    1b mutate the state value then set it (back-reference keeps a copy-then-push out), 1c a component declared inside a
#    function body, 1d Vue watch writing another ref, 1e Svelte $effect assigning state, 1f Angular effect() calling set/update.
rg -n -U --pcre2 'use(?:Layout)?Effect\(\s*\(\)\s*=>\s*\{\s*\Kset(?!SearchParams\b|Attribute\b|Item\b|Property\b|Header\b)[A-Z]\w*\((?![^)\n]*=>)' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 'const\s*\[\s*(\w+)\s*,\s*set\w+\s*\]\s*=\s*useState[\s\S]*?(?<![.\w])\K\1\.(?:push|splice|unshift|pop|shift|sort|reverse|fill|copyWithin)\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '^[ \t]{2,}(?:const|let|function)\s+[A-Z]\w*\s*(?:=\s*(?:memo\(|React\.memo\(|forwardRef\()?\s*(?:\([^)\n]*\)|\w+)\s*=>|\()' -g '*.{jsx,tsx}' "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 'watch(?:Effect)?\([^,\n]*,\s*\(?[^)\n]*\)?\s*=>\s*\{?\s*\w+\.value\s*=(?!=)' -g '*.{vue,ts,js}' "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\$effect(?:\.pre)?\(\s*\(\)\s*=>\s*\{[^}]*?^\s*[A-Za-z_$][\w$]*\s*(?:=(?!=)|\+=|-=)' -g '*.{svelte,svelte.ts,svelte.js}' "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 '\beffect\(\s*\(\)\s*=>\s*\{?(?:(?!\}\s*\)\s*;)[\s\S]){0,300}?\bthis\.\w+\.(?:set|update)\(' -g '*.ts' "${X[@]}" "${ROOTS[@]}"
# 2. Cleanup (SPA memory growth). File-level set difference over files that mount something (the $LC intersect drops
#    module-scope boot code), plus 2f, the same-line React effect with no return, which catches a leak in a file that
#    removes some other listener. 2a listeners, 2b intervals, 2c observers, 2d sockets/streams/workers, 2e subscriptions,
#    2g a module-scope Map/Set that only grows.
rg -l0 'addEventListener\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 "$LC" | xargs -0 -r rg --files-without-match --pcre2 'removeEventListener|\bsignal\s*[:,}]|\bonce\s*:\s*true|useEventListener|AbortController'
rg -l0 'setInterval\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match 'clearInterval'
rg -l0 --pcre2 'new\s+(?:Resize|Intersection|Mutation|Performance)Observer\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match '\.disconnect\('
rg -l0 --pcre2 'new\s+(?:WebSocket|EventSource|BroadcastChannel|SharedWorker|Worker)\(|\bio\(\s*[\x27"`\w]' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --pcre2 '\.(?:close|disconnect|terminate)\('
rg -l0 --pcre2 '\.subscribe\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 "$LC" | xargs -0 -r rg --files-without-match --pcre2 'unsubscribe|\bunsub\w*|takeUntil|DestroyRef|toSignal|\|\s*async\b|\bfirst\(\)|\btake\(1\)|(?:=>|return)\s*[\w.]+\.subscribe\('
rg -n --pcre2 'use(?:Layout)?Effect\(\s*\(\)\s*=>\s*\{(?:(?!\breturn\b).)*\b(?:addEventListener|setInterval|subscribe|observe|on)\((?:(?!\breturn\b).)*\}\s*,' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -l0 --pcre2 '^(?:export\s+)?(?:const|let)\s+\w+\s*(?::[^=\n]+)?=\s*new\s+(?:Map|Set)\s*(?:<[^>\n]*>)?\(\s*\)' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\.(?:set|add)\(' | xargs -0 -r rg --files-without-match --pcre2 '\.delete\(|\.clear\(|\bmax\w*|\b[Ll][Rr][Uu]\b'
# 3. Keys: 3a index keys in four stacks, 3a′ the files where that list also reorders or loses rows (`onRemove(i)`,
#    `.filter((_, j) => j !== i)`, or a keyed row component handed `index={i}` — follow its import), 3b keys that change
#    every render, 3c a JSX element returned from .map() with no key (JSX-aware body).
#    `k|n|j` count only as the .map callback's SECOND parameter: bare, they are value names (`([k, v]) => key={k}`).
KI='\bkey=\{\s*(?:i|idx|index|_i|ix)\s*\}|:key="\s*(?:i|idx|index)\s*"|\btrack\s+\$index\b'
KJ='\.map\(\s*\(\s*(?:\{[^{}]*\}|\[[^\]]*\]|[^,(){}\[\]]+),\s*(k|n|j)\s*\)\s*=>[\s\S]{0,600}?\K\bkey=\{\s*\1\s*\}'
rg -n --pcre2 "$KI"'|\{#each\s+[^}]*,\s*(\w+)\s*\(\s*\1\s*\)\s*\}|trackBy:\s*\w*[Ii]ndex' "${UI[@]}" -g '*.html' "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 "$KJ" "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
{ rg -l --pcre2 "$KI" "${UI[@]}" -g '*.html' "${X[@]}" "${ROOTS[@]}"; rg -l -U --pcre2 "$KJ" "${UI[@]}" "${X[@]}" "${ROOTS[@]}"; } | sort -u | tr '\n' '\0' | xargs -0 -r rg -l --pcre2 '\.(?:sort|splice|unshift|toSorted|toSpliced|reverse)\(|(?:\b|(?<=on)|(?<=handle))(?:[Mm]ove|[Rr]emove|[Rr]eorder|[Ss]wap|[Ii]nsert)[A-Z]?\w*\(|\.filter\(\s*\(\s*_\w*\s*,\s*\w+\s*\)\s*=>\s*\w+\s*!==|useFieldArray|useSortable|draggable|\bindex=\{\s*(?:i|idx|index)\s*\}'
rg -n --pcre2 '\bkey=\{\s*(?:Math\.random|crypto\.randomUUID|Date\.now|uuid\w*|nanoid|v4)\(|:key="\s*(?:Math\.random|Date\.now)\(' "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 "\.map\(\s*(?:\([^)]*\)|\w+)\s*=>\s*\(?\s*<[A-Za-z][\w.]*\b(?!${TB}\bkey=)${TB}>" -g '*.{jsx,tsx}' "${X[@]}" "${ROOTS[@]}"
# 4. Reactivity loss: 4a Vue/Pinia destructure, 4b mutated props (Vue, Svelte), 4c Angular update() returning the same
#    array, 4d Angular components that opt out of OnPush (read for in-place mutation).
rg -n --pcre2 'const\s*\{[^}]+\}\s*=\s*(?:\w*[sS]tore|use\w+Store\(\)|props|reactive\([^)]*\))\s*;?\s*$' -g '*.{vue,ts,js}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\bprops\.\w+(?:\.\w+)*\s*(?:=(?!=)|\+\+|--|\.(?:push|splice|pop|shift|unshift|sort|reverse)\()' -g '*.{vue,svelte}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\.update\(\s*\(?(\w+)\)?\s*=>\s*\{[^}]*\b\1\.(?:push|splice|unshift|sort|reverse)\(' -g '*.ts' "${X[@]}" "${ROOTS[@]}"
rg -n 'ChangeDetectionStrategy\.(Default|Eager)' -g '*.ts' "${X[@]}" "${ROOTS[@]}"
# 5. Controlled/uncontrolled: 5a a state that starts undefined/null fed straight to value= or checked=, 5b value={x?.y},
#    5c a form keyed by a value (read whether the key changes while the user edits).
rg -n -U --pcre2 'const\s*\[\s*(\w+)\s*,\s*set\w+\s*\]\s*=\s*useState(?:<[^>]*>)?\(\s*(?:undefined|null)?\s*\)[\s\S]*?\K\b(?:value|checked)=\{\s*\1\s*\}' -g '*.{jsx,tsx}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\b(?:value|checked)=\{\s*\w+\?\.[\w.?]+\s*\}' -g '*.{jsx,tsx}' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 "<(?:form|[A-Z]\w*Form)\b(?=${TB}\bkey=)" -g '*.{jsx,tsx}' "${X[@]}" "${ROOTS[@]}"
```

A finding is a hit **plus** a read of the component **plus** the route that mounts it **plus** the oracle. Three blind spots are structural:

- **A custom hook hides the effect.** 2a–2e read the file that calls `addEventListener`, which may be a hook; follow the hook to every component that calls it before deciding it is mounted per route.
- **A wrapper hides the listener.** A design-system `useResizeObserver` or a chart library that attaches its own listeners is invisible to 2a–2c. The heap-slope oracle across navigations (§ Proof) sees it; the grep never will.
- **A row component hides the move.** 3a′ greps the file that holds the index key. When the keyed element is a capitalised component handed `index={i}` (`<AttributeCard key={index} index={index}/>`), the move-up/down or remove usually lives in that component's own file after a split: follow the import and run the 3a′ verb pattern there before calling the list append-only.
- **A lint lane that did not run is not a clean lane.** The rg in §1 covers four shapes of the thirteen Compiler rules. When the lint lane is blocked, §1 is `checked (rg only; lint blocked: <reason>)`, never `checked`.

**Measured** (2026-10-05). On this batch's research fixtures (positives and decoys per class): 1a 1/1, 1b 2/2 with 0/2 decoys (`[...rows].sort()`, `toSorted`), 1d–1f 3/3, 2a 1/1 (the decoy that removes its listener: 0), 2e 1/1 Angular (the `takeUntilDestroyed` decoy: 0), 2f 3/3 on one file that also holds a correct effect — file-level 2a prints nothing there, which is why 2f exists — 3a 4/4 across React, Vue, Svelte and Angular (decoys `key={item.id}` with an index prop, `track item.id`: 0), 3b 1/1, 3c 2/2 (decoys with `key` after an arrow handler: 0), 4a 1/1 plus one known false positive (a Pinia **action** destructure; actions may be destructured), 4c 1/1 (the regex, on a `.tsx` fixture line; the lane globs `*.ts`), 5a 1/1, 5b 1/1. On the six benchmark fixtures with UI code every grep returns 0 except 2g on `review-decoys`: a server-side metrics `Map` in a package that lists both `express` and `react` — routed to `memory-growth-scan` §1. The interval the batch eval flagged in `slow-marketplace` has its `clearInterval` beside it: 0 here, correctly. On a real React 19 + Vite SPA (about 4,300 TS/TSX files, read-only), the script runs in under 2 s: 1a 17 (every one a reset on a dependency change — reading one, a page reset to 1 after a filter change renders and fetches the old page once under the new filter first), 1c 2 (1 candidate: a component declared inside a dialog view's body; 1 Refuted: a factory at module level), 2a–2g 0 after the `$LC` intersect (before it, 2a returned 6 files and 2e 2, all module-scope boot listeners or listeners on a print window that dies with it), 3a 109 lines in 72 files → 3a′ 13 files (first read: a reorderable attribute editor with move-up/down, remove and an input per row — a candidate), 5a 6 (design-system pickers fed `useState<Date | undefined>()`: read whether the component forwards to a native input). Re-measured 2026-10-15 on a real NestJS + React monorepo (React 19.2, the lint plugin declared only in the workspace-root `package.json`): grep 0 now prints that root manifest line and the one enabled `react-hooks/*` rule, which the `ROOTS`-only scan had missed (the header read "plugin not installed"); 1a 17 → 16 (`setSearchParams` dropped; the remaining DOM helper `setLinkHref` is refuted by reading its declaration); 3a 110 → 93 lines (17 of the 18 bare `k|n|j` hits were value keys such as `([k, v]) => key={k}`; the one index kept is a second `.map` parameter); 3a′ 10 → 17 files, now listing all five reorderable or removable row editors (`onRemove(i)`, `.filter((_, j) => j !== i)`, a keyed row component whose move lives in its own file), 3 of them noise. On the 20 benchmark fixtures the only changes are the two dropped `key={n}` skeleton and star lists in `a11y-states` (value keys, not seeds) and one gained root-manifest line. Its ESLint config loads eslint-plugin-react-hooks 7.1.1 and enables only `rules-of-hooks`; the lint lane was blocked (no `node_modules` in the read-only copy).

## The 3,000-hit path

1. **Intersect with the route table.** A component no route imports is dismissed with one read; Storybook-only and design-system-internal files are their own group (`precedents/ui.md` § 10).
2. **Group** by (component, pattern). A shared hook or wrapper with the defect is one group however many call sites it has: fixing it there closes them all (`precedents/ui.md` § 9).
3. **Rank** by route traffic — RUM or analytics when present, else long-lived routes first (dashboards, editors, POS and chat screens a user keeps open for hours), then list and form routes.
4. **Read the top 30 groups.**
5. **Prefer the runtime bulk oracle at scale.** For §2, run the existing component suite once with a global `afterEach` that asserts `vi.getTimerCount() === 0` and a balanced `window.addEventListener` / `removeEventListener` spy, under React StrictMode: every failing test is a confirmed site. For §1, the lint lane is the bulk oracle. For SPA growth across routes, one heap-slope run over the top route pairs.
6. **Ledger the rest** `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Scans for

| § | Class | Standard id | Default severity |
|---|---|---|---|
| 1 | React and Compiler rules broken: impure render, refs read in render, state mutated in place, `setState` in render or synchronously in an effect, a component defined in a component; the Vue, Svelte and Angular equivalents | react-hooks rule ids | high when it loops or hits the network; medium when the UI shows a stale or wrong value; low for a derived-state effect with no visible flash |
| 2 | Effect or subscription with no cleanup — **SPA memory growth (`/bundle-perf` X1a)** | CWE-401, CWE-772 | medium; high when a leaked handler duplicates network calls or the heap slope exceeds 1 MB per cycle on a primary route |
| 3 | Keys and identity: index key on a list that reorders or loses rows, a key that changes every render, a missing key | `react/jsx-key`, `vue/require-v-for-key`, `svelte/require-each-key`, `@angular-eslint/template/use-track-by-function` | medium when rows hold state (inputs, focus, expansion, animation); low for display-only rows |
| 4 | Reactivity loss: destructured reactive state, mutated props, a signal updated with the same reference, OnPush opt-out with mutation | `vue/no-mutating-props`, `vue/no-setup-props-reactivity-loss`, `@angular-eslint/no-uncalled-signals` | medium; high when the stale view drives a money, stock or submit action |
| 5 | Controlled ↔ uncontrolled flip; form state reset by a key that changes while the user edits | — | low; medium when typed input is lost |

### 1. React and Compiler rules broken

```
BAD:   useEffect(() => { setFullName(first + ' ' + last); }, [first, last]);   // extra commit with a stale value
       todos.push(t); setTodos(todos);                                         // same reference: no re-render
       function Dialog() { const Picker = () => <List/>; return <Picker/>; }   // new component type every render: remount, state lost
       watch(first, v => { full.value = v + last.value })  ·  $effect(() => { full = first + last })  ·  effect(() => this.d.set(this.c() * 2))
GOOD:  const fullName = first + ' ' + last;                                    // derive during render
       setTodos([...todos, t])  ·  setRows(rows.toSorted(byName))
       const Picker = …  at module scope, props passed in
       computed(() => …)  ·  let full = $derived(first + last)  ·  d = computed(() => this.c() * 2)
```
**Read the code:** Does the effect sync with an external system (`document.title`, storage, a chart instance) — the legitimate use — or compute a value React could compute in render? Does the reset-on-change effect fire a request with the old state first (a filter change that renders page N, then page 1)? Is the mutated array the state value itself or a copy? Is the inner component's type stable (module scope, `useMemo`)? With React Compiler on, does the file compile, or does it bail out (`unsupported-syntax`)? **Finding when** the rule's failure is observable: a stale frame, a lost update, a remount that drops state, a loop. **Proof:** render count — wrap in `<Profiler onRender>` with StrictMode off; a prop change commits 2 times before the fix and 1 after; a remount shows as state reset in the same test; a loop is the console's `Maximum update depth exceeded` (React) / `effect_update_depth_exceeded` (Svelte) plus a request count over 5 idle seconds of less than 2.

### 2. Effect or subscription with no cleanup — SPA memory growth

```
BAD:   useEffect(() => { window.addEventListener('resize', onResize); }, []);
       useEffect(() => { const id = setInterval(tick, 1000); }, []);
       ngOnInit() { this.route.params.subscribe(p => this.load(p['id'])); }
       onMounted(() => window.addEventListener('scroll', f))            // no onUnmounted
       $effect(() => { const ws = new WebSocket(url); })                // no teardown returned
GOOD:  useEffect(() => { const ac = new AbortController(); window.addEventListener('resize', onResize, { signal: ac.signal }); return () => ac.abort(); }, []);
       return () => clearInterval(id)  ·  this.route.params.pipe(takeUntilDestroyed()).subscribe(…)
       useEventListener(window, 'scroll', f)  ·  $effect(() => { const ws = new WebSocket(url); return () => ws.close(); })
```
**Read the code:** Is the subscription made per mount (component, hook called by a component, a route-level effect) or once at boot (module scope, the app root)? A boot-time singleton is app-lifetime, not a leak across navigations; note it and move on. Is the target an element or window that dies with the component (a print iframe, a popup)? Then it is collected with it. Does the callback capture large state (a dataset, a canvas, a chart)? Does StrictMode's double mount register twice? Module-scope `Map`/`Set` (2g): is the key space bounded (an enum, a route list) or per entity/user (unbounded)? **Finding when** a per-mount subscription survives unmount. **Proof:** mount/unmount balance — with fake timers, mount, exercise, unmount, assert `vi.getTimerCount() === 0` and add/remove spies balanced per event type (`proof-oracles.md` § "Mount/unmount balance, reorder identity, request order", variant V108). The cost across routes is the heap slope or memlab (§ Proof). CWE-401 for retained memory, CWE-772 for a socket or worker never closed.

### 3. Keys and identity

```
BAD:   {attributes.map((a, index) => <div key={index}><Input value={a.name}/>…<button onClick={() => move(index, -1)}/></div>)}
       <li v-for="(item, i) in items" :key="i">   ·   {#each items as item, i (i)}   ·   @for (item of items(); track $index)
       <Row key={Math.random()} />                                     // remounts every render
       items.map(it => <li>{it.name}</li>)                             // no key
GOOD:  key={a.id} (assign an id on creation when the data has none)   ·   :key="item.id"   ·   (item.id)   ·   track item.id
```
**Read the code:** Does the list reorder, filter, insert at the head or lose a middle row (3a′ lists the files that do)? Do rows hold anything not derived from the item — an uncontrolled input, focus, an open popover, an animation? A static, display-only list is fine (`precedents/ui.md` § 42). Do the items have a stable id, or must one be assigned at creation? **Finding when** a row's local state can attach to a different item. **Proof:** reorder identity — type into row 2, then insert at the head, delete the middle, sort and filter; the typed value, focus and expansion stay with the same item id (`proof-oracles.md` § "Mount/unmount balance, reorder identity, request order", variant V109).

### 4. Reactivity loss

```
BAD:   const { items, total } = store                 // Pinia: plain values, frozen at setup
       props.items.push(x)                            // Vue / Svelte: mutating the parent's data
       this.items.update((arr) => { arr.push(x); return arr; })   // Angular: same reference, no notification
       if (this.loading) { … }                        // Angular: the signal, not its value — always truthy
GOOD:  const { items, total } = storeToRefs(store)    // actions may still be destructured from the store itself
       emit('update:items', [...props.items, x])  ·  this.items.update((arr) => [...arr, x])  ·  if (this.loading()) …
```
**Read the code:** Are the destructured names state or getters (lost) or actions (fine)? Is it Vue ≥ 3.5 `const { x } = defineProps()` in `<script setup>`, which the compiler keeps reactive? Does the Angular component run under OnPush (the default angular-eslint 22.5 assumes) or opt out (4d) and then mutate a field in place? Svelte 5: is the mutated `$props` value bound by the parent (`bind:`) — allowed — or not (`ownership_invalid_mutation` at runtime)? **Finding when** the view does not update after the state changes. **Proof:** a component test that changes the state through the real action and asserts the rendered text changes — it fails before the fix.

### 5. Controlled ↔ uncontrolled flip and key reset

```
BAD:   const [name, setName] = useState<string>();  …  <input value={name} onChange={…} />   // undefined → string
       <input value={user?.name} />                                                    // undefined until the fetch lands
       <ProfileForm key={profile.updatedAt} … />                                       // every save remounts the form mid-edit
GOOD:  useState('')  ·  value={user?.name ?? ''}  ·  defaultValue for an uncontrolled field  ·  key={profile.id}
```
**Read the code:** Does the value reach a native `input`, `select` or `textarea` (directly or through a component that forwards it), or a design-system component that normalises `undefined` itself? Does the key change while the user is typing (a refetch timestamp, a version counter) or only when the entity changes (reset by key is the documented pattern there)? **Finding when** the flip or the remount can drop typed input or move the cursor. **Proof:** spy on `console.error` during render → type → refetch; React's warning that a component changed an uncontrolled input to be controlled must not appear, and the typed text survives the refetch.

## Proof

The oracle per class, failing first and green after the fix ([`proof-oracles.md`](../../../../snippets/proof-oracles.md)):

1. **Render count** (§1) — § "Render count" in the frontend section; StrictMode off, or halve the count.
2. **Mount/unmount balance** (§2) and **reorder identity** (§3) — § "Mount/unmount balance, reorder identity, request order"; variants V108 and V109.
3. **Heap leak (memlab)** (§2 across routes) — § "Heap leak (memlab)", variant V53: a scenario with `url`, `action` and `back`, then `npx --no memlab analyze unbound-object` or `detached-DOM` for the retainer trace.
4. **Heap slope with a plateau check** (§2 across routes, Chromium) — § Accessibility and UI states, *Heap slope*, variant V113: on the **production** build, 3 warm-up then 20 measured A → B → A cycles with GC before each CDP sample. Finding when the heap slope exceeds max(64 KB, 0.5 % of the first sample) per cycle with R² ≥ 0.8 and nodes or listeners non-decreasing; a second-half slope under 10 % of the first is a cache warming up, Refuted.
5. **Console warning** (§1 loops, §5) — § Accessibility and UI states, *Console warning*, variant V119 (§5; the §1 update loops have no variant of their own): `vi.spyOn(console, 'error')` or `page.on('console')`, failing on the framework's message.
6. **View update** (§4) — § Accessibility and UI states, *View update*, variant V118: change the state through the real action and assert the rendered text changes (Angular `fakeAsync` + one `detectChanges()`, Vue `nextTick()`, Svelte 5 `flushSync()`).

A static fact needs no runtime oracle only when the rule is the claim (a `key={Math.random()}` remount, a mutated prop the linter reports); every other class needs its oracle to fire. Without a harness the candidate is Unconfirmed with the test written out.

## Output

```
render-correctness-scan — lanes: react 19.2 (apps/web/package.json), react-hooks 7.1.1 (config enables rules-of-hooks only),
React Compiler off; vue, svelte, angular absent
Lint lane: blocked (no node_modules in this checkout) — §1 is rg only

Findings: 1 · Unconfirmed: 2

1. src/features/products/editor/AttributesTab.tsx:80                        [report-with-fix]   medium
   §3 index key on a reorderable list — key={index} on rows with move up/down, remove and an <Input> per row.
   Mounted by /products/:id/edit. Proof: test/AttributesTab.identity.test.tsx — focus row 2, move it up:
   focus stays on position 2 (fails). Fix: give each attribute an id on creation; key={attr.id}.
2. src/features/pos/ShiftDialogView.tsx:36                                  [report-flagged]    medium
   §1 component defined in a component — `const ShiftPicker = () => …` in the view body: a new type every
   render, so the picker remounts and drops its scroll and selection. Unproven: no component test for the
   dialog. Settling test: select a template, trigger a parent re-render, assert the selection survives.
   Fix: lift ShiftPicker to module scope and pass its props.
3. src/shared/lib/use-pagination.ts:20                                      [report-flagged]    low
   §1 set-state-in-effect — setPage(1) after a filter change; the first commit renders the old page under the
   new filter. Same shape at 16 more sites (one group). Settling test: Profiler commit count and the request log
   on one filter change (2 → 1 expected).

Verification: 7 candidates → 1 finding · 2 unconfirmed · 1 hardening · 3 refuted

Class coverage:
  §1  React / Compiler rules        checked (rg only; lint blocked) (19 hits / 3 groups → 0 findings, 2 unconfirmed, 1 refuted)
  §2  cleanup / SPA memory growth   checked (0 hits after the lifecycle intersect; 8 boot-time listeners dismissed by read)
  §3  keys and identity             checked (72 files → 13 reorderable; 2 read → 1 finding, 1 refuted) · Live, unreviewed (11 files — continue with grep 3a′)
  §4  reactivity loss               N/A (no Vue, Svelte or Angular lane)
  §5  controlled / uncontrolled     checked (6 hits / 2 groups → 0 findings; 1 hardening: the design-system picker normalises undefined; 1 refuted: a docs page)
```

`[report-with-fix]`: the component is mounted by a cited route, the oracle failed, and the fix is a local change in the project's framework. `[report-flagged]`: one link is unproven (no harness, a hook not followed to its callers, a lint lane blocked), and the row names that link and the settling test. The coverage block lists **all five** classes on every run: `checked (k hits → m findings)` only when the greps ran on a present lane; `N/A (<reason>)` when the stack has no such surface; `blocked (<reason>)` when a grep or the lint lane failed. A partial review reads `Live, unreviewed (k groups / n hits)`, never `checked`.

## False positives / gotchas

The verifier reads [`precedents/ui.md`](../../../../snippets/precedents/ui.md) (§ 42–46 for this skill) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this skill meets most:

- **An effect that syncs with an external system is the legitimate use** — `document.title`, storage, analytics, an imperative chart or map instance. Only an effect that computes what render could compute is §1.
- **Reset by key is the fix, not the bug**, when the key is the entity id. §5 is a key that changes while the same entity is being edited.
- **Framework-managed cleanup** — VueUse `useEventListener` / `useIntervalFn`, template listeners, the Angular `async` pipe, `takeUntilDestroyed`, `toSignal`, `@HostListener` (`precedents/ui.md` § 46).
- **App-lifetime singletons** — a listener or store subscription at module scope or in the app root, registered once at boot. Not a growth source across navigations; one read per file.
- **A listener on an element or window that is discarded with the component** — a print iframe, a popup window, a detached node — is collected with it.
- **`key={index}` on a static, display-only list** (skeleton rows, a fixed legend) is fine (`precedents/ui.md` § 42).
- **Pinia actions may be destructured**; state and getters may not. Vue ≥ 3.5 `defineProps` destructure in `<script setup>` stays reactive.
- **React Compiler on** makes manual `useMemo` / `useCallback` advice noise; it does not fix a mutated state value or a component defined inside a component — those still fail.
- **Dev builds lie about memory.** StrictMode mounts twice and HMR keeps old modules alive: a heap number from a dev server is not evidence (`precedents/performance.md` § "Browser load and interaction").

## When to run

- On a diff that adds or changes an effect, a subscription, a list render, a store binding or a form: the `/frontend-audit` dispatch signal when that command is present, and the review-frontend lens.
- On every whole-repo frontend audit, reporting all five classes.
- When `/bundle-perf` reaches row X1, or a user reports a tab that slows down after an hour on one screen.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md). Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the component `<file:line>`, the route or parent that mounts it, the oracle, and the fix in the project's framework.
- Do not mark a finding `[report-with-fix]` without an oracle that failed first. Without a harness it is `[report-flagged]` / Unconfirmed, with the settling test written out.
- Do not use `rg -L` for files-without-match; it is `--follow`. Do not print "no render bugs found" without the class-coverage block, and do not mark §1 `checked` when the lint lane did not run.
- Do not propose a fix that hides the symptom: an `eslint-disable` line, an empty dependency array to stop a loop, `key={Math.random()}` to force a reset, a larger memlab threshold.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `ssr-audit` (this pack) — hydration, browser globals on the server and cross-request state; the server side of the same render.
- `client-data-scan` (this pack) — races, invalidation and server state in client stores.
- `/bundle-perf` and `inp-responsiveness` (performance pack, when installed) — rank §2 leaks by heap cost and own re-render cost.
- code-quality `correctness-smell-scan` §3 (when installed) — the stale closure inside one effect.
- `@ui-reviewer` — dispatches this skill at review time and routes its findings.
- `rules/frontend-principles.md` — the component and state MUSTs this scan enforces.
