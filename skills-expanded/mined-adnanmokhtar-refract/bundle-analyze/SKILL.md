---
name: bundle-analyze
description: Brotli bytes per route; heavy chunk + anchoring import, duplicates, unused code, legacy polyfills, dev-only code in the build.
kind: skill
pack: frontend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: bundle-analyze

## Premise

Find real bloat, not vibes. Every finding cites the chunk + its **brotli** bytes on the route that pays for it + the import that anchors it (`<file:line>`). "Bundle is big" is not a finding; "should split this" without the chunk is not a finding. A report not measured against the **production build** is invalid, and a budget breach without a named cause is a failed analysis, not a passing one.

Brotli, not gzip: it is what users download from any modern CDN, and it is the unit of `proof-oracles.md` § "Bytes per route". Raw or "parsed" sizes, which analyzers show by default, run several times larger, so a report that mixes units produces findings that evaporate on re-check. A gzip figure from an earlier report is not comparable with this skill's numbers.

This skill owns `/bundle-perf` (performance pack) rows **B1** (§1–§3, with `code-splitting`), **B2** (§4–§5), **B4** legacy targets and polyfills (§6, formerly interim lane P4) and **B5** dev-only code in the production client (§7, formerly interim lane P5). The research catalog files §6 and §7 as **P-03** and **P-04**. **Numbering contract:** §4 and §5 are the earlier "Procedure steps 4–5" with the same meaning, so a citation of either form resolves here.

## Boundaries

- **Where to cut a heavy chunk** → `code-splitting` (ai-pattern, this pack). This skill names the chunk and the anchoring import; the pattern decides the split.
- **Render-blocking `<head>`, third-party tags, late-inserted layout shift** → `critical-path-scan` (this pack). A third-party script loaded from its own origin is never in this bundle; it is there.
- **Public source maps as an exposure** → security `xss-scan` (when the security pack is installed); §7 reports the bytes and the dev code, and hands the exposure there. Without that pack, §7 notes the exposure and keeps the medium severity.
- **The page-load verdict and the whole-app budget conversation** → `/bundle-perf` (performance pack, when installed). Without it, this skill is the only bundle instrument in the project: say so in the report rather than implying a budget authority it does not hold.
- **Mobile app size** (React Native, Flutter, native) → the mobile pack's own size skill, when installed. This skill measures web bundles only.

## Adapt to the codebase — the bundler lanes

Read the bundler and framework with versions from the lockfile and print the lane. Sizes come from the build output, never from a dev server (`precedents/performance.md` § 90).

| Lane | Build | Bytes per route (brotli) | Treemap (to find the anchoring module) |
|---|---|---|---|
| **Vite 5–8** (React, Vue, Svelte, Solid, SvelteKit) | `npx --no vite build --manifest` (add `--sourcemap` only for a local analysis build, never the deploy) | the manifest walk in `proof-oracles.md` § "Bytes per route" | `rollup-plugin-visualizer` 7.1.1 (`brotliSize: true`, `template: 'treemap'` or `'raw-data'`; Rollup and Rolldown peers) |
| **Next.js 16** (Turbopack build) | `next build` | `npx --no next experimental-analyze --output` (16.1+, writes `.next/diagnostics/analyze`) | the same analyzer; webpack builds (`next build --webpack`): `ANALYZE=true` with `@next/bundle-analyzer` 16.3.8 |
| **webpack 5 / Rspack** | `npx --no webpack --json > stats.json` | `size-limit` (below) | `webpack-bundle-analyzer` 5.4.0 `stats.json dist --default-sizes brotli --compression-algorithm brotli`; Rsbuild/Rspack: `@rsdoctor/cli` 1.6.4 |
| **Nuxt 4** | `npx --no nuxi analyze` | `size-limit` | built in; read the compressed column, not the raw default |
| **Angular 20–22** | `npx --no ng build --stats-json` | `size-limit` | the stats file the builder writes, in an esbuild-metafile viewer |
| **Any bundler** | the project's build | `size-limit` 14.1.0, brotli by default: one entry per route chunk glob, `npx --no size-limit --json` | — |

Label every number `measured (brotli, <tool@version>, <sha>)` (npm registry versions read 2026-10-05). `vite-bundle-visualizer` (1.2.1, last published 2024-05) and `source-map-explorer` (2.5.3, last published 2022-09) are unmaintained: do not recommend either.

## Pre-flight

Run as **one** script from the repo root. It runs the static half of every §; the build-output lines run only when a production build is present, and print that they did not otherwise. Every `rg` names its path; files-without-match is `--files-without-match`, never `-L`.

```bash
ROOTS=( $(rg -l --pcre2 '"(?:react|react-dom|vue|svelte|@angular/core|solid-js|preact|astro|@builder\.io/qwik)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -n1 dirname | sort -u) ); [ ${#ROOTS[@]} -eq 0 ] && ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,coverage,.next,.nuxt,.output,.svelte-kit,.angular,storybook-static}/**' -g '!**/*.min.*'
   -g '!**/{test,tests,__tests__,spec,e2e,__mocks__,mocks,__fixtures__,stories,playwright,cypress,scripts,tools,locales,i18n,generated,__generated__,docs}/**'
   -g '!**/*.{test,spec,e2e,stories,story,mock}.*' -g '!*.{md,mdx,snap,map,lock}' -g '!ai/**')
UI=(-g '*.{js,jsx,ts,tsx,mjs,vue,svelte,astro,html}')
CFG=(-g '**/package.json' -g '**/{.browserslistrc,browserslist,tsconfig*.json,babel.config.*,.babelrc*,angular.json,project.json}' -g '**/{vite,webpack,next,nuxt,rsbuild,rspack,svelte,astro}.config.*')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(//|/\*|\*(\s|/|$)|#|<!--)')
OUT=(); for r in "${ROOTS[@]}"; do for d in dist build out .next/static .output/public; do [ -d "$r/$d" ] && OUT+=("$r/$d"); done; done
echo "ROOTS: ${ROOTS[*]} · OUT: ${OUT[*]:-none — §1-§3, §6c and §7b are blocked until a production build exists}"
# 4a. Lockfile: client packages (the app's direct dependencies + dual-instance hazards) resolved at more than one version.
#     pnpm 9: only versions inside this app's PRODUCTION closure (its importer's dependencies, workspace links followed,
#     then `snapshots:` transitively) count — a second copy held by the API, a test runner or a build tool is not a client
#     duplicate. Other lockfiles (and pnpm 6–8) are read whole: the scope line says which.
for r in "${ROOTS[@]}"; do [ -f "$r/package.json" ] && node -e '
const fs=require("fs"),p=require("path"),r=process.argv[1];let d=r,lock=null;
for(;;){for(const f of ["pnpm-lock.yaml","package-lock.json","yarn.lock"]) if(!lock&&fs.existsSync(p.join(d,f))) lock=p.join(d,f); if(lock||d===p.dirname(d)) break; d=p.dirname(d);}
if(!lock){console.log(r+": no lockfile");process.exit(0)}
const pk=JSON.parse(fs.readFileSync(p.join(r,"package.json"))),names=new Set([...Object.keys(pk.dependencies||{}),"react","react-dom","react-is","scheduler","vue","@vue/runtime-core","svelte","@angular/core","tslib","core-js","@babel/runtime","regenerator-runtime","lodash","lodash-es","moment","date-fns","dayjs","@emotion/react","styled-components","zod","rxjs"]);
const t=fs.readFileSync(lock,"utf8"),v={},add=(n,ver)=>{if(names.has(n))(v[n]??=new Set).add(ver)},uq=s=>s.replace(/^\x27|\x27$/g,"");let scope="whole lockfile";
const imp={},snap={};if(lock.endsWith("pnpm-lock.yaml")){let sec="",cur=null,sub="",dep=null,m;
for(const L of t.split("\n")){if(/^\S/.test(L)){sec=L.replace(/:.*/,"");cur=null;continue}
if(sec==="importers"){if(m=L.match(/^  (\S.*?):$/)){cur=imp[uq(m[1])]={};sub=""}else if(cur&&(m=L.match(/^    (\w+):$/)))sub=m[1];else if(cur&&(m=L.match(/^      (\S.*?):$/)))dep=uq(m[1]);else if(cur&&dep&&/^(optionalD|d)ependencies$/.test(sub)&&(m=L.match(/^        version: (.*)$/)))cur[dep]=uq(m[1])}
else if(sec==="snapshots"){if(m=L.match(/^  (\S.*?):(?: \{\})?$/)){cur=snap[uq(m[1])]={};sub=""}else if(cur&&(m=L.match(/^    (\w+):$/)))sub=m[1];else if(cur&&/^(optionalD|d)ependencies$/.test(sub)&&(m=L.match(/^      (\S.*?): (.*)$/)))cur[uq(m[1])]=uq(m[2])}}}
const rel=p.relative(p.dirname(lock),r).split(p.sep).join("/")||".";
if(imp[rel]&&Object.keys(snap).length){scope="production closure of importer "+rel;const seen=new Set(),q=[];
const walk=(base,deps)=>{for(const[n,ver]of Object.entries(deps)){if(ver.startsWith("link:")){const ir=p.posix.normalize(p.posix.join(base,ver.slice(5)));if(imp[ir]&&!seen.has(ir)){seen.add(ir);walk(ir,imp[ir])}continue}
const k=n+"@"+ver;if(!seen.has(k)){seen.add(k);q.push(k);add(n,ver.replace(/\(.*$/,""))}}};walk(rel,imp[rel]);while(q.length){const k=q.pop();if(snap[k])walk(rel,snap[k])}}
else if(lock.endsWith("pnpm-lock.yaml"))for(const m of t.matchAll(/^  \x27?((?:@[^\/@\s\x27]+\/)?[^@\s\x27\/]+)@(\d[^:\x27(\s]*)\x27?:/gm))add(m[1],m[2]);
else if(lock.endsWith("package-lock.json"))for(const[k,e]of Object.entries(JSON.parse(t).packages||{})){const m=k.match(/node_modules\/((?:@[^\/]+\/)?[^\/]+)$/);if(m&&e.version)add(m[1],e.version)}
else for(const m of t.matchAll(/^"?((?:@[^\/@\s"]+\/)?[^@\s"\/]+)@[^\n]*:\n\s+version:?\s+"?([^"\n]+)/gm))add(m[1],m[2]);
console.log(p.relative(".",lock)+": 4a scope: "+scope);
for(const[n,s]of Object.entries(v))if(s.size>1)console.log(p.relative(".",lock)+": "+n+" "+[...s].join(" "))' "$r"; done
# 5a. knip needs installed dependencies; say so instead of skipping silently, and list the direct dependencies no source
#     or stylesheet names (a no-install candidate list: types, CLI-only and config-only packages, and framework peers such
#     as react-dom under Next, are read, not reported).
for r in "${ROOTS[@]}"; do [ -d "$r/node_modules" ] || [ -d node_modules ] || { echo "$r: §5 knip blocked (no node_modules) — no-install fallback:"
  node -e 'for (const n of Object.keys(require(require("path").resolve(process.argv[1], "package.json")).dependencies || {})) console.log(n)' "$r" | while read -r n; do rg -q -F -e "\"$n\"" -e "'$n'" -e "\"$n/" -e "'$n/" "${UI[@]}" -g '*.{css,scss,less}' -g '**/*.config.*' "${X[@]}" "$r" || echo "  §5 no import found: $n"; done; }; done
# 6a. Legacy targets and polyfills in config and source (`(?<![\w@/.-])`, not `\b`: `\b` never fits before the `@` of a
#     scoped name); 6b. an explicit build target below the Vite 8 / Next 16 floor.
rg -n --no-heading --pcre2 '(?<![\w@/.-])(?:core-js|regenerator-runtime|@babel/polyfill|@vitejs/plugin-legacy|react-app-polyfill|whatwg-fetch)\b|polyfill\.io|polyfill-fastly|"target"\s*:\s*"ES5"|\bie\s*(?:11|>=?\s*\d)|\bop_mini\b' "${CFG[@]}" "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:target|esbuildTarget)\s*:\s*\[?[^\]\n]*["\x27](?:es5|es20(?:1\d|20|21)|chrome(?:[1-9]\d|10\d|110)|safari(?:1[0-5]|16\.[0-3])|firefox(?:[1-9]\d|10\d|11[0-3])|edge(?:[1-9]\d|10\d|110))\b' -g '**/{vite,webpack,nuxt,rsbuild,rspack,svelte,astro}.config.*' -g '**/{tsconfig*.json,angular.json}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 7a. Dev-only packages imported by shipped source (read the guard); 7c. a mock/demo switch read at runtime.
rg -n --no-heading --pcre2 '\bfrom\s+["\x27](?:msw(?:/browser)?|@faker-js/faker|@welldone-software/why-did-you-render|react-scan|redux-logger|@redux-devtools/\w+|@vue/devtools)["\x27]|import\(\s*["\x27](?:msw|@faker-js|react-scan|@welldone-software)|\bdevTools\s*:\s*true\b' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:import\.meta\.env|process\.env)\.\w*(?:MOCK|FAKE|STUB|DEMO)\w*' "${UI[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 6c. Transpiler helpers per chunk; 7b. dev markers, served maps and the MSW worker — BUILD OUTPUT only.
[ ${#OUT[@]} -gt 0 ] && rg -c --pcre2 'regeneratorRuntime|_classCallCheck|core-js/modules/|_asyncToGenerator|@babel/runtime/helpers|__publicField\(|__spreadValues\(|__async\(' -g '*.{js,mjs}' "${OUT[@]}"
[ ${#OUT[@]} -gt 0 ] && rg -n --no-heading -o --pcre2 'console\.(?:log|debug|trace)\(|Each child in a list should have a unique|\[Vue warn\]|setupWorker|mockServiceWorker|why-?[dD]id-?[yY]ou-?[rR]ender|react-scan|redux-logger|@faker-js|__REDUX_DEVTOOLS_EXTENSION(?:_COMPOSE)?__|devTools:\s*(?:!0|true)|sourceMappingURL=\S+\.map' -g '*.{js,mjs,html}' "${OUT[@]}" | sort | uniq -c | sort -rn | head -40
[ ${#OUT[@]} -gt 0 ] && find "${OUT[@]}" \( -name '*.map' -o -name 'mockServiceWorker.js' \) | head -20
true
```

**Measured** (2026-10-05). On the research fixture for these classes, 6c counts the two helper lines and 7b hits every planted marker kind (a `console.log`, React's missing-key warning, `setupWorker`, `whyDidYouRender`, a `sourceMappingURL`, RTK `devTools:!0`), plus the served map and the MSW worker; the clean build beside it returns 0. On the twelve benchmark fixtures every grep returns 0 (none ships a build output or a polyfill) and 4a prints `no lockfile`, which the coverage block reports as §4 `blocked`, not clean. On a real React 19 + Vite 8 monorepo (read-only, no `node_modules`, no build output) the script runs in a quarter of a second. 4a: 2 candidates (`react-is` at four versions, `rxjs` at two); a lockfile-wide count returns 119 packages at more than one version, almost all build tooling, which is why the list is limited to the app's own dependencies. 6b: 1, an explicit `es2020` / `chrome87` / `safari14` target with a comment calling the floor a product decision: a candidate whose settling input is the old-browser share in RUM. 7a: 0. 7c: 1, a runtime mock switch; refuted on read, because a build plugin replaces the mock modules with stubs when the flag is unset, and the build-output grep would confirm it. §1–§3, 6c and 7b: blocked (no build output); §5: blocked (no `node_modules`). Re-measured 2026-10-15 on the same kind of tree (a real NestJS + React monorepo, pnpm 9): 4a now walks the web importer's production closure — `rxjs` drops out (its second copy belongs to the API) and `react-is` falls from four versions to two (16 and 18, both reached by client packages: read which chunk holds each), with a `4a scope:` line naming the arm; the §5 no-install fallback lists 0 of the app's 42 direct dependencies as never imported. The project's first-load guard was written in gzip-6, which is why the budget arm now prints the unit. On the fixtures the fallback prints 0–3 candidates per app, mostly `react-dom` under Next (a framework peer).

## Procedure

### 1. Build and measure bytes per route

Build for production with the lane's command, twice on the same commit; the bytes must match, or find the non-deterministic input first. Then measure brotli bytes for the **entry closure** (what every route pays) and for **what each lazy route adds**. Base and head on one lockfile give an exact delta with no noise band. Severity follows `/bundle-perf`: critical when the main entry grows by more than 50 KB br in one change; high when a route is over twice its budget; medium when it is over budget by less.

### 2. Top chunks

List the five largest chunks in the entry closure and the five largest lazy chunks, each with its brotli bytes and the routes that load it. A lazy route chunk is not initial-load cost (`precedents/performance.md` § 84).

### 3. Top third-party dependencies and the anchoring import

For each third-party package over 10 KB br in the entry closure, find the import that pulls it in. That is a review prompt with a one-line justification, not a threshold:

```bash
PKG=recharts; rg -n --no-heading --pcre2 "from\s+[\"']${PKG}(?:/[^\"']*)?[\"']|import\(\s*[\"']${PKG}" "${UI[@]}" "${X[@]}" "${ROOTS[@]}"
```
**Read the code:** Is the import in a shared layout or the app shell (every route pays) or in one route? A barrel or whole-library import (`import * as`, a named import from a package root) where a subpath exists? Is the package on Next's `optimizePackageImports` default list (`precedents/performance.md` § 64)? **Finding when** the bytes land in the entry closure and the anchoring import is cited.

### 4. Duplicates

A package resolved at more than one version, or in two module formats, can ship twice. Candidates from grep 4a, then the package manager's dry run: `pnpm dedupe --check`, `npm dedupe --dry-run`, Yarn 1 `npx --no yarn-deduplicate --list --fail` (it has no `--check`), Yarn 2+ `yarn dedupe --check`. **Read the code:** Do both copies reach the **client** build, or is one only in server code or tooling (`precedents/performance.md` § 88)? Does a version constraint force the split (name both consumers and their ranges)? **Finding when** the client build output holds both copies. Severity: high for two copies of the UI framework (two Reacts break hooks; a correctness defect, not only bytes); medium when the duplicate is 10 KB br or more; low otherwise.

### 5. Unused files, exports and dependencies

`npx --no knip --reporter compact` (knip 6.39.0; `--production` limits it to shipped code). **Read the code:** `knip` flags a re-export as unused when no consumer imports through that barrel; verify by hand. An unused dependency costs install time, not client bytes, unless something imports it. **Finding when** an unused file or export is in the client build output, or a dependency is imported only by dead code. Severity: low.

### 6. Legacy targets and polyfills shipped to modern browsers

```
BAD:   build: { target: ['es2020', 'chrome87', 'safari14'] }        // lowers class fields, ??=, etc. for every visitor
       "browserslist": ["> 0.5%", "ie 11"]  ·  import 'core-js/stable'  ·  <script src="https://polyfill.io/v3/polyfill.min.js">
GOOD:  no explicit target: Vite 8 defaults to baseline-widely-available (chrome111, edge111, firefox114, safari16.4); Next 16's
       default browsers are Chrome, Edge and Firefox 111+ and Safari 16.4+  ·  @vitejs/plugin-legacy for the measured old share
```
The Vite 8 default is from the vite 8.3.2 source and the Next 16 default from its upgrade guide (research catalog, read 2026-10-05). `polyfill.io` was compromised in June 2024: any reference is also a security row (security `deps-audit`, when installed). **Read the code:** Does a documented old-browser share in RUM or analytics require the target (cite the number)? Is the output `@vitejs/plugin-legacy` nomodule chunks that modern browsers never fetch (`precedents/performance.md` § 89)? Is the target in a `tsconfig` that only type-checks (a bundler ignores it)? **Finding when** transpiler helpers (6c) or polyfill modules are in the chunks modern browsers load. **Proof:** helper and polyfill bytes per route before and after (§ Proof), then `legacy-javascript` (Lighthouse 12.6.1 under LHCI 0.15.1) or `legacy-javascript-insight` (Lighthouse 13) wasted bytes. Severity: medium.

### 7. Dev-only code in the production build

```
BAD:   in dist/: React's development warnings ("Each child in a list should have a unique…"), setupWorker (MSW running),
       whyDidYouRender, react-scan, redux-logger, @faker-js data, RTK devTools:!0, sourceMappingURL → a served .map
       if (env.mock === 'true') return mockApi[domain]  // a runtime switch: both arms ship
       import { setupWorker } from 'msw/browser'; if (process.env.X === 'true') setupWorker(...)  // a static import: the check guards the call, not the bundle
GOOD:  if (import.meta.env.DEV) { const { worker } = await import('./mocks/browser'); await worker.start() }   // dropped from the build
       build.sourcemap: 'hidden' and the maps uploaded to the error tracker, not deployed
```
**The build output is the oracle** (deterministic, one run): a marker present in `dist` is the finding; the same marker only in source, behind a literal `import.meta.env.DEV` or `process.env.NODE_ENV !== 'production'` guard around a dynamic import, is refuted. A mock arm selected by a flag parsed at runtime is not removed by the bundler: both arms are referenced, so the build keeps both. **A runtime env check around a static import is not a bundle guard:** the module is bundled before any condition runs, so a dev-only package imported at the top of a shipped module is a candidate whatever the `if` around its use says, until the build output shows it absent. **Read the code:** Is the dev-only package reached by a static `import` or only by a dynamic `import()` inside a branch the bundler folds away? Is the MSW worker file only copied into `public/` (harmless) or registered (`setupWorker` in a chunk)? Is `@tanstack/react-query-devtools` used through its default export, which is a no-op in production builds? Is a served `.map` reachable (`curl -s -o /dev/null -w '%{http_code}' https://<host>/assets/<chunk>.js.map` returns 200)? Severity: high for a development React or Vue build, active MSW or faker data; medium for served source maps; low for `console.log` noise.

## Where the budget comes from (this skill does not have authority it did not earn)

A verdict of OVER BUDGET is only meaningful against a budget somebody chose. Resolve in this order and **print which arm was used**:

1. **A project budget** — `ai/runtime/perf-budgets.md`, `ai/stack.md`, a `size-limit` / `bundlesize` config, a `resource-summary:script:size` assertion in the project's `lighthouserc.json`, a CI budget file. `frontend-principles` § Should requires a budget gate but sets no number, because the right number is per product. If the project has one, it wins outright. **Print its unit beside it** — gzip (and which level), brotli, or raw bytes — and measure in that unit: a guard written in gzip-6 is never compared with this skill's brotli figures (brotli is smaller, so the comparison passes a bundle the project's own gate fails). When the unit cannot be read from the config or the guard's code, the verdict is `report-flagged`. **When the budget comes from Lighthouse:** that assertion sums every script the audited *page* loads, while this skill measures one route's initial bundle. It is a ceiling above your number, not the same measurement: print which one you measured, and treat a per-route figure under a page-level ceiling as unproven rather than passing.
2. **The shared default**, when none exists: **150 KB brotli on the initial critical path** — `THR-WEB-BUNDLE` in `templates/governance/thresholds.json`, shared with `/bundle-perf` and `/audit --target-bundle`. It is a working default for an interactive app on a mid-tier mobile connection, not an industry constant, and a project budget wins outright. Say so in the report.

**Budget absent → the verdict is `report-flagged`, never OVER BUDGET.** Emit the measured sizes, the named heavy chunks and the anchoring imports, and flag "no budget declared; measured against the THR-WEB-BUNDLE default of 150 KB br initial" as its own finding, whose fix is *declare a budget*, not *delete a dependency*. Failing a build on a number the project never agreed to is how a bundle gate gets disabled permanently.

## Proof

Failing first, green after the fix ([`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Frontend):

1. **Bytes per route** (§1–§4, §6) — § "Bytes per route": two builds of one commit agree exactly; base → head is an exact delta under the budget. For §6, the helper count from 6c falls to zero in the chunks modern browsers load (V150).
2. **Build-output grep** (§6, §7; V150, V151) — § "Build-output grep": the 6c or 7b marker is present in the built output before the fix and absent after, on the same build command. Deterministic; no Lighthouse run needed.
3. **Lighthouse median** (§4, §6) — § "Lighthouse median", 5 runs, median-run, mobile and desktop. Under LHCI 0.15.1 (Lighthouse 12.6.1) assert `duplicated-javascript` and `legacy-javascript`; under Lighthouse 13 only `duplicated-javascript-insight` and `legacy-javascript-insight` exist. `unused-javascript` exists in both (the LH 12 ↔ 13 id table is in that section). Print the version and the id used.

A candidate read in code with no build to measure is Unconfirmed, with the build command that settles it.

## The 3,000-hit path

Bundle classes rarely reach 3,000 hits; when they do (a monorepo with many apps, a lockfile with hundreds of split versions): group by (package, anchoring import), rank by the bytes it adds to the entry closure of the busiest routes, read the top 30 groups, and ledger the rest as `Live, unreviewed (k groups / n hits)` with the command that continues them. Never `checked`.

## Output

```
bundle-analyze — lane: vite 8.2 + react 19.2 (apps/web/package.json) · measured (brotli, vite manifest walk, a1b2c3d)

Initial (entry closure):  171.4 KB br / 150 KB br   OVER by 21.4 KB   (budget: THR-WEB-BUNDLE default — no project budget declared)

Top chunks:
  vendor-react-*.js     58.2 KB br   every route
  index-*.js            41.0 KB br   every route
  vendor-forms-*.js     30.1 KB br   every route — anchored by src/main.tsx:12 (zod error map installed before render)

Findings:
1. src/app/layout.tsx:9  import { Chart } from 'recharts'          [report-with-fix]  high
   §3 charting library in the shared layout: +44.6 KB br on every route. Fix: lazy-load the dashboard widget
   (code-splitting detector 1); proof: entry closure 171.4 → 126.8 KB br.
2. vite.config.ts:99  build.target ['es2020', …, 'safari14']          [report-flagged]   medium
   §6 explicit target below the Vite 8 default; 6c finds __publicField in 14 chunks (3.9 KB br). Unproven: the
   old-browser share that would justify it. Settling input: RUM share of browsers below safari16.4/chrome111.

Class coverage:
  §1  bytes per route        checked (1 entry, 23 lazy routes)
  §2  top chunks             checked
  §3  third-party anchors    checked (6 packages > 10 KB br → 1 finding)
  §4  duplicates             checked (2 lockfile candidates → 0 in the client build)
  §5  unused                 blocked (no node_modules: knip not run)
  §6  legacy / polyfills     checked (1 config hit → 1 unconfirmed)
  §7  dev-only code          checked (build output: 0 markers, 0 served maps)
```

`[report-with-fix]`: measured on the production build, the anchoring import is cited, and the fix and its expected delta are named. `[report-flagged]`: one link is unproven (no build, a budget not declared, a justification not yet read). The coverage block lists **all seven** classes on every run: `checked` only when the class ran on a present build or config; `N/A (<reason>)` when the lane has no such surface; `blocked (<reason>)` when the build, the lockfile or `node_modules` was missing.

## False positives / gotchas

The verifier reads [`precedents/performance.md`](../../../../snippets/precedents/performance.md) § 64 and § 83–90 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4.

- Dynamic imports show as separate chunks; that is correct, not duplication. A lazy route chunk is not initial-load cost (§ 84).
- Duplicates only in server bundles cost the client nothing (§ 88). `plugin-legacy` nomodule chunks are skipped by modern browsers (§ 89).
- `nuxi analyze` and most treemaps show raw size by default; read the compressed column, and convert to brotli before comparing with a budget.
- A "duplicate" can be intentional (two majors kept for compatibility): name both consumers and their version constraints before calling it either way.
- Replacing a heavy library (moment → `date-fns` or `Intl`) is a refactor: a separate change after this analysis.

## When to run

- After adding a dependency, after a `package.json` upgrade (especially a major), or after changing the bundler config (`target`, chunking, `optimizePackageImports`).
- When `lighthouse-ci` flags a JS-size or TBT regression, or `/bundle-perf` reaches rows B1, B2, B4 or B5.
- Before a release, against the production build, to catch dev-only code (§7).

## Halt conditions

- Halt on hand-waves: every flagged package cites brotli bytes on a named route and the importing `<file:line>`. "Looks heavy" is not a finding.
- Halt if the numbers came from a dev server (`pnpm dev`, `next dev`): dev bundles include HMR and unminified source and lie about size (`precedents/performance.md` § 90).
- Halt if a duplicate is dismissed as "intentional" without naming the two consumers and their version constraints.
- Halt if a budget fails but no chunk or package is named as the cause.
- Halt on an `OVER BUDGET` verdict that does not name which of the two budget arms supplied the threshold.
- Do not report §7 from source alone: the build output decides. Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md); run standalone, tag those rows `self-verified`.

## Related

- `code-splitting` (ai-pattern, this pack) — the fix sibling: where to cut a chunk this skill named.
- `critical-path-scan` (this pack) — render-blocking `<head>`, third-party tags and late-inserted layout shift.
- `lighthouse-ci` (this pack) — knows only the JS total against a budget; a failed JS budget there is unfinished until it has a chunk name from here.
- `lcp-audit` / `streaming-ssr` (this pack) — a lazy hero or a blocked first byte are theirs; do not propose a split as the fix for either.
- `/enhance-ui` (ui-ux pack, when installed) — consumes this skill for its optional bundle-size delta and prints `SKIPPED (no bundle-analyze)` without it.
- `/bundle-perf` (performance pack, when installed) — owns the page-load verdict and ranks rows B1–B5 across routes.
