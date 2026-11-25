---
name: feature-surface-scan
description: "Half-built feature detector: unserved client calls, uncalled routes, dead links, shipped placeholders, dead buttons."
kind: skill
pack: product
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: feature-surface-scan

## Premise

A half-built feature passes every gate a team runs. The button typechecks, lints and passes its mocked tests, then sends `GET auth/me/permissions` to a route nobody serves, so the first real user gets a 404. Or the user gets an admin screen, when the failed fetch falls back to "allow". A navigation link points at a page that was never built. A form posts to `/api/tasks/bulk`, which does not exist. A list renders two hard-coded deals. A "Coming soon" card sits on a paid plan's page. An export button runs `onClick={() => {}}`. Each side is consistent with itself. Only the **join** is broken, so per-line greps and unit tests miss it.

**Every finding cites both ends:** the reference at `<file:line>` (a call, link, form action, placeholder or control) and its counterpart (the served route or page that answers it), or the words "no counterpart after the written search". It also cites the route or screen that reaches the reference, the oracle that failed or the test that would settle it, and the fix. A script row or grep hit is a candidate, never a finding by itself. "No half-built features" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by execution.** The static half is a join of two inventories: served routes against client references, and page routes against links. `scripts/surface-map.py` builds that join (§ The join script). The proof is the project's own parity test, a generated one, or a live request (`proof-oracles.md` § Product, V409–V412). A candidate with no harness is **Unconfirmed**, carrying the test that would settle it ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The rule

A candidate is a finding when all four hold:

1. **It ships.** The file is production source, not a test, story, fixture, seed, scaffolder template or demo build ([`precedents/product.md`](../../../../snippets/precedents/product.md) § 5). It is reachable: a mounted route, a rendered component, a page in the router.
2. **The join is decided, not guessed.** Both tables were built for that package, and the normaliser is sane: the ledger prints no `join: SUSPECT`, which means it did not find more than half of the calls unserved **and** more than half of the routes uncalled (§ 9). A name built at runtime is `unresolved`, never a miss (§ 17).
3. **No counterpart exists anywhere it could.** No served route answers the call after prefix and version resolution. No production proxy or rewrite serves it (§ 2). No other service, mobile app, webhook sender or public client is the intended caller (§ 1). The flag that guards the placeholder is not off in every environment (§ 4).
4. **The oracle fires, or would.** The project's parity test, a generated route-table test, a render test or a `--live` request fails. Without a harness, the row is Unconfirmed with the test written out.

## Boundaries

- **A page or component nothing mounts** → code-quality `dead-code-scan`, when the code-quality pack is installed. Without it, list the file here tagged `dead-code (owner pack code-quality not installed)`. knip never reports dead pages, because route files are its plugin entries (§ 6).
- **Unbuilt capability** (partial CRUD, a promised feature with no code) → `/roadmap`. Its detectors 1, 2 and 6 consume §1, §3 and §4 rows here when the product pack is installed. This skill owns the **shipped** half: code that reaches users today.
- **Unknown-URL handling and catch-all 404s, and click-navigation on non-links** → frontend `routing-scan` §4 and §1, when the frontend pack is installed. §3 here asks only whether a link's target exists. Its route table and this one are one table: reuse whichever ran first. Without the frontend pack, unknown-URL handling is unreported here; §3 still runs.
- **Copy completeness** (hard-coded strings, missing keys) → frontend `i18n-scan`, when the frontend pack is installed. §4 reads catalogs only for placeholder *values*; without frontend, copy completeness is unreported here.
- **Error, empty, loading and permission states** → ui-ux `ui-state-scan`, when installed. A control disabled by a permission or a pending request is that skill's §6 or §8, not §5 here. Without ui-ux, list such controls tagged `ui-state (owner pack ui-ux not installed)`.
- **A flag that hides a placeholder** → devops `progressive-delivery` owns flag state (§1–§9, when installed). §4 reads its config rows to decide reachability. Without devops, read the flag's default and every environment file once, and cite them.
- **The attack surface of an uncalled route** → security (`@api-security-reviewer`, when installed). §2 owns the product question: why does the route exist? Without security, a `writes` row on an unauthenticated route is tagged `security-class (owner pack security not installed)`.
- **Drift between a generated OpenAPI client and its spec** → backend `http-contract-scan` §10, when the backend pack is installed; without it, spec drift is unreported here. A generated, typed client is a compile-time control (grep 0b), and its calls are skipped here.

## Adapt to the codebase — the lanes

Read the framework **and its version** from the lockfile. Print the lanes the script reports in the output header. Lanes the script cannot read are named in its ledger, never silently skipped.

| Stack | Served routes (script lane) | Page routes | References | Compile-time control |
|---|---|---|---|---|
| **NestJS** 10 / 11 | `@Controller(prefix)` (string, array, `{ path }`, or no argument) × verb decorators; `setGlobalPrefix`; URI versioning stripped. `RouterModule.register` paths are noted, not composed | — | — | `@nestjs/swagger` + a generated client |
| **Express / Fastify / Koa / Hono** | router vars × verbs; `app.use('/p', router)`, `route('/p', sub)` and `register(plugin, { prefix })` resolved through relative imports; `fastify.route({ url })` | — | outbound calls from server packages are `outbound`, not joined | — |
| **Next.js** 14–16 | `app/**/route.*` exported verbs; `pages/api/**` | `app/**/page.*` (groups, `[id]`, `[...slug]`, a `[locale]` root aliased away); `pages/**` | `fetch`, `<Link href>`, `router.push`, `redirect()` | `typedRoutes: true` + `next typegen && tsc` |
| **React / Vue / Angular SPA** | — | route objects and `<Route>` JSX (React Router, Vue Router, Angular `Routes`, TanStack `createFileRoute`), nested `path` composed through `children` | the client wrapper (`http.get('stores')`, `api.post`, `this.http.get`), `fetch`, `axios`, `ky`, `<Link to>`, `navigate()` | React Router typegen (framework mode), `openapi-fetch` |
| **Remix / React Router framework**, **SvelteKit**, **Nuxt** | `action` exports, `+server.*` | flat routes (`app/routes/a.b.$id.tsx`), `+page.svelte`, Nuxt `pages/**` | `$fetch`, `useFetch`, `<form action>` | — |
| **FastAPI / Flask** | `APIRouter(prefix=)` × `include_router(prefix=)`; `Blueprint(url_prefix=)` × `register_blueprint` | Jinja templates are served GET routes | `<form action>`, `href`, `RedirectResponse` | — |
| **Django / DRF** | `urls.py` `path` / `re_path` through `include()` prefixes; `router.register`, with each ViewSet expanded to its methods (ModelViewSet / mixin actions, `@action(methods=…, url_path=…)`, `as_view()` method defs, `@api_view`; an unread view stays `ANY`) | served GET routes | template links, `redirect('/x')` | — |
| **Rails / Laravel** | `routes.rb` (`namespace`, `scope`, `resources only:/except:`); `routes/*.php` (`prefix()->group`, `resource`, `apiResource`; `api.php` gets `/api`) | served GET routes | ERB / Blade links, `redirect_to` | — |
| **Go** | net/http 1.22 `"GET /x"` patterns, chi, gin, echo, groups | — | — | — |
| **Flutter / React Native / Expo** | — | `GoRoute(path:)`, Expo Router `app/**`, React Navigation screen names | `dio.get`, `context.go`, `router.push`, `navigation.navigate('Screen')` | go_router typed routes |
| **Spring, ASP.NET, tRPC, GraphQL** | not a lane: pass `--routes-from=<tsv>` (any TSV with `METHOD /path` cells, such as the migration pack's `pair-inventory` I-ROUTES record, when that pack is installed). tRPC prints a ledger note | — | — | tRPC is typed end to end |

## The project's own control first

Run grep 0 before the script. A two-sided route-parity test is the best oracle there is (§ 7). Examples: every call names a served route, every route is used or explained, every link names a route. On the measured monorepo, that test's header records two unserved calls on its first run, and one of them failed open. When such a test exists:

1. Run it (tier U), and record the command and exit code.
2. Print its classes as `controlled (<test>)` in the coverage block.
3. Report from the script only what the test does not cover. For example, form actions and placeholders when the test reads only `http.<verb>()` calls.
4. Read the test's allow-list. An entry with no reason, or one for a route the client does call, is a §2 row against the list itself.

A compile-time control (grep 0b) counts the same way for the paths it types. A typed route or a generated client turns a dead target into a type error. An `as Route` cast or a hand-written `fetch` beside it is outside the control, and the script still covers it.

## The join script

`scripts/surface-map.py`, beside this file (installed as `.claude/skills/feature-surface-scan/scripts/surface-map.py`). It uses the Python 3.8 standard library only. It reads files and never writes into the scanned repo. Run it from the repo root:

```bash
python3 -I .claude/skills/feature-surface-scan/scripts/surface-map.py . --client=<wrappers from 0c> --reasons=<allow-list, if any> --max=40
python3 -I .claude/skills/feature-surface-scan/scripts/surface-map.py --self-test        # 35 checks; exit 3 on a failure
```

It builds three tables: served routes, page routes, and references. References are calls, links, redirects, form actions and screen names. It normalises both sides: `:id`, `{id}`, `<int:id>`, `[id]`, `$id` and `${x}` become `{}`, splats become `{*}`, and query strings are dropped. The global prefix it found (`setGlobalPrefix`, Laravel `api.php`) and version segments are stripped. A leading base-URL variable in a client template is removed. It then joins:

- **FS1:** a call with no served route. `near` gives `method-mismatch:<served verbs>`, and `tags` gives `gate-fetch` for permission, entitlement, plan and module fetches, `form`, or `base=<var>`.
- **FS2:** a route no reference names, tagged webhook, callback, oauth, health, metrics, public, internal, well-known, `writes` or `explained(<reason>)`.
- **FS3:** a link, redirect or GET form whose target matches no page route of its own package and no served GET route.
- **FS4** placeholders and **FS5** dead affordances (§4, §5).
- **CONTROL:** the parity and link tests it saw.

`--inventory` prints every ROUTE, PAGE and REF row. The stderr ledger gives per-lane counts and the reference status mix: served, page, unserved, deadlink, outbound, external, unresolved, self-origin, asset, no-page-table. It also gives the prefixes stripped and the lanes present but not joined. Exit codes: 0 means no FS1 or FS3 row, 2 means at least one, 1 means usage, 3 means the self-test failed.

These are the rules the script applies before any row is printed:

- A call made from a **server package** (one whose manifest directory declares backend routes) goes to another service, so it is `outbound`.
- A link in a package with **no page-route table and no served routes** is `no-page-table`, not a dead link.
- With **no served routes** under the roots, FS1 and FS2 are `blocked`. Add the API root, or pass `--routes-from`.
- A root catch-all route (`*`, `/[...slug]`) is the not-found boundary and serves nothing.
- `scripts/`, `tools/`, `docs/` and design-system documentation pages are not shipped surface.

**Measured** (2026-10-19). On `benchmarks/fixtures/half-built-crm` (FastAPI + Jinja):

- FS1 returns the seeded tasks template's form (`POST /api/tasks/bulk`, `method-mismatch:GET,PUT`): CRM-WIRE-04.
- FS3 returns the base layout's three navigation links (`/contacts`, `/deals`, `/tasks`): CRM-WIRE-05.
- FS4 returns the 501 on the mounted `POST /api/deals/{deal_id}/convert` (CRM-STUB-02), the same router's two literal records returned under a `# TODO` (CRM-STUB-01), the importer's two stubs (CRM-STUB-03) and the exporter's one (CRM-STUB-04).
- FS2 lists all 14 API routes, because the app has no client. That is the read step's call.

Across the 23 fixture roots, three script changes removed noise:

- **Outbound classification.** Server-side calls to third parties had been reported as unserved: `ds-defects` 23 → 2, `slow-marketplace` 8 → 0, `quality-mix` 7 → 1, `node-api` 2 → 0, `brittle-suite` 4 → 1.
- **The blocked rule.** It turned 41 calls in `a11y-states` and 20 in `mobile-defects`, which have no API under the root, into `blocked`.
- **FS2 without a client.** FS2 now needs a client reference under the roots. Without one it is `N/A`: `backend-defects` went from 94 uncalled rows to `N/A`.

The join-sanity line flags `convention-drift` as `SUSPECT`: 12 of 15 calls are unserved and 8 of 10 routes are uncalled. That fixture's API implements only part of what its web app calls, which is exactly what the line exists to make you read first.

FS3 needed three lanes: per-package page tables, the `[locale]` alias and the Expo Router lane. With them, `mobile-defects` went 9 → 1 (`/addresses/${id}`, which has no `[id]` screen). In `a11y-states`, 9 → 8, and all eight are pages the fixture never built. `vuln-fullstack` gave 1 unseeded row: `/s/${id}`, where the router has `/p/:id`.

On a real NestJS 11 + React 19 monorepo (read-only):

- **Size.** The run read 7,616 files in 24 s. It found 1,310 served routes (Nest; `api` prefix + URI version stripped) and 128 page routes (a route registry plus the router). It joined 1,268 calls, of which 1,247 were served.
- **FS1: 0.** One FS1 row was a scaffolder template under `scripts/`, and one was a same-origin chunk probe, now `self-origin`. That agrees with the repo's own parity test.
- **FS3: 0 of 70 links**, matching its `every-link-names-a-route` test.
- **FS2: 120 rows**, which its `every-route-is-used-or-explained` ledger controls.
- **FS4: 6 catalog "Coming soon" values.** The copy lane's only JSX-adjacent hit was a JSDoc line. `mock-rows` went 117 → 0 once table-column and option configs stopped counting as records.
- **FS5: 9 → 5** after the design-system docs were excluded. One is the PP-FS-3 decoy (`onSubmit={() => undefined}`, `near=handler:88`). One is a priced AI package card whose only button is literally disabled with the "Coming soon" label: one root cause with the catalog row. One is a "forced active" status button, disabled by design.

On `benchmarks/fixtures/launch-gaps` (2026-10-19, staged copy, `--reasons=` its allow-list; 42 routes, 20 pages, 66 references, 0.1 s, exit 2), every seed prints: FS1 3 of 3 (the fail-open permissions fetch tagged `gate-fetch`, a `method-mismatch:PUT`, a bare `fetch` to a renamed route), FS2 2 of 2 (an uncalled `DELETE`; an allow-list line with no reason, tagged `explained(listed)`), FS3 3 of 3, FS4 4 of 4 (catalog, 501, mock rows in a hook and in a service), FS5 2 of 2. Seven decoy rows print and the read clears each: the nginx-proxied path (FS1, grep 0d), the webhook, health, metrics, public and allow-listed routes (FS2), the flagged-off "coming soon" (FS4) and the PP-FS-3 no-op submit (FS5). A GET form to `/orders/search` matched the `orders/:orderId` page by shape, correctly: a dynamic segment answers any single segment.

## Pre-flight greps

Run as **one** script from the repo root. Every `rg` names its path: given no path and a piped stdin, `rg` reads stdin and reports zero hits. An `rg` exit 2 is a failed grep, printed as `blocked (rg exit 2)`, never as zero hits. Grep 0 is context for the script; grep 4 cross-checks the script's copy lane.

```bash
ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.turbo,coverage,.venv,venv,__pycache__,generated,__generated__}/**' -g '!**/*.min.*' -g '!**/{docs,ai,.claude,.git}/**')
T=(-g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,stories}/**' -g '!**/*.{spec,test,e2e-spec,stories,test-data}.*' -g '!**/{test_*,*_test,conftest}.*')
C=(-g '*.{ts,tsx,js,jsx,mjs,cjs,vue,svelte,py,rb,go,php,dart,kt}')
NC='^[^:]+:\d+:\s*(?://|\*|/\*|#|<!--)'                                   # comment-only lines
g() { out=$("$@" 2>&1); ec=$?; [ $ec -eq 2 ] && { echo "blocked (rg exit 2): $out" | head -3; return; }; printf '%s\n' "$out" | rg -v --pcre2 "$NC" | head -40; }
# 0a. The project's own parity / link tests (run them first: § The project's own control first).
g rg --files -g '**/*{every-call,served-route,route-parity,routes-are-used,used-or-explained,unserved,every-link,dead-link,link-names-a-route}*' -g '!**/node_modules/**' "${ROOTS[@]}"
# 0b. Compile-time controls: typed routes, generated clients.
g rg -n --no-heading --pcre2 -g '*.{ts,mts,js,mjs,json}' -g '!**/node_modules/**' -g '!**/*.d.ts' '\btypedRoutes\s*:\s*true|"(?:openapi-typescript|openapi-fetch|orval|@hey-api/openapi-ts|@rtk-query/codegen-openapi|swagger-typescript-api)"\s*:|\bcreateClient<\s*paths\s*>|react-router\s+typegen' "${ROOTS[@]}"
# 0c. Client wrappers: every name here goes into --client= (the script knows http, api, apiClient, client, axios, ky, dio …).
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" "${T[@]}" '\b(?:axios|ky|ofetch)\.create\s*\(|\bcreateFetch\s*\(|\bbaseURL\s*:|\bprefixUrl\s*:|^\s*export\s+const\s+(?:http|api|apiClient|client|httpClient|request)\s*=' "${ROOTS[@]}"
# 0d. Proxies and rewrites (§ 2): a production rewrite serves a path; Vite server.proxy is dev-only.
g rg -n --no-heading --pcre2 -g '**/{next.config,vite.config,nuxt.config,svelte.config,vercel,netlify,angular,proxy.conf,firebase}.*' -g '**/{nginx,*.nginx}.conf' -g '**/Caddyfile' -g '**/netlify.toml' -g '!**/node_modules/**' '\brewrites\b|\bproxy\s*:|\bproxy_pass\b|\breverse_proxy\b|\[\[redirects\]\]|"source"\s*:\s*"/api' "${ROOTS[@]}"
# 0e. Routes meant for outside callers (§ 1): public markers, webhook / callback / health paths.
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" "${T[@]}" '@Public\s*\(|@ApiExcludeEndpoint|@SkipAuth|\bAllowAnonymous\b|csrf_exempt|skip_before_action\s+:authenticate|\b(?:path|route)\s*\(\s*["\x27]/?(?:webhooks?|callbacks?|oauth|health[z]?|metrics|\.well-known)' "${ROOTS[@]}"
# 4. Placeholder copy in markup: a text node after `>`, on its own line (multi-line JSX), or a string literal
#    (cross-check of the script's copy lane; catalog values are the script's, comments are dropped by $NC).
g rg -n --no-heading -i --pcre2 -g '*.{tsx,jsx,vue,svelte,html,erb,jinja,j2,dart}' "${X[@]}" "${T[@]}" '(?:^|>|["\x27`])\s*(?:coming soon|lorem ipsum|not (?:yet )?implemented|under construction|work in progress)\b' "${ROOTS[@]}"
```

**Measured** (2026-10-19). Across the 23 fixture roots, 0 exit-2 runs. 0c hit in 10 roots (1–6 lines each: `axios.create`, `baseURL`). 0d hit in 5. 0e hit in `port-pair` (1). 0a, 0b and 4 had 0 hits. On the real monorepo:

- 0a found 4 control tests: the call parity test, the link test (literal targets only; the script also joins template targets such as `/orders/${id}`), the route-ledger test, and a store-link wizard test matched by name (not a route control).
- 0c found 3 lines: a `ky.create` client named `api`, the `http` wrapper, and a Playwright `baseURL` (not app code).
- 0d found 1: a Vite `proxy`, dev-only.
- 0e found 51 `@Public()` and webhook markers.
- 4 found 1 line, a JSDoc comment, which the comment filter drops to 0.

## The 3,000-hit path

1. **Fix the normaliser first.** `join: SUSPECT` in the ledger means more than half of the calls are unserved **and** more than half of the routes are uncalled, so a prefix, a version or a wrapper's base URL is probably missing (§ 9). Read the ledger's `prefixes stripped`, add the missing piece (or `--client=`, or `--routes-from`), and rerun. Never triage a broken join.
2. **Let the controls take their classes.** A class the project's parity test covers is `controlled`. Only its uncovered remainder is triaged.
3. **Group.** For FS1, group by (client module, missing path stem). A wrapper with the wrong base URL is one group. For FS2, group by controller or router file and tag. For FS4, group by (component or catalog key). For FS5, group by component.
4. **Rank.** Rank `gate-fetch` FS1 rows first (the fail-open shape), then primary navigation (FS3 in a header, sidebar or menu), writes (FS2 `writes`), and placeholders on priced or onboarding screens.
5. **Read the top 30 groups**, both ends of each.
6. **Prefer the runtime bulk oracle at scale.** One route-table test generated from the script's `--inventory` rows, or one Playwright crawl that visits every page route and clicks every primary-navigation link, settles hundreds of rows at once (V409, V410).
7. **Ledger the rest** as `Live, unreviewed (k groups / n rows)`, with the command that continues them. Never mark them `checked`.

## Scans for

| § | Class | Research id | Default severity |
|---|---|---|---|
| 1 | A client call no served route answers | PR-FS-1 | high; **critical-candidate** when the failure path fails open (a permission, entitlement or plan fetch whose error means "allow") |
| 2 | A served route no reference names and no reason explains | PR-FS-2 | low; medium when it writes |
| 3 | A link, form action, redirect or `navigate()` target with no page | PR-FS-3 | medium; high on primary navigation |
| 4 | A shipped placeholder: copy, catalog value, 501 / NotImplemented on a mounted route, mock rows, mock modules, `USE_MOCKS=true` | PR-FS-4 | high on a reachable primary route or a priced screen; low behind a flag off in every environment |
| 5 | A dead affordance: a no-op handler, `href="#"`, a literally disabled control, a `<form>` with no action and no submit handler | PR-FS-5 | medium |

### 1. Unserved call

**Class** PR-FS-1 · **Severity** high; critical-candidate when the failure path fails open.

```
BAD:   http.get('auth/me/permissions')           // no @Get('me/permissions') under @Controller('auth')
       http.get(`stores/${id}/sync`)              // served as @Post(':id/sync'): method mismatch
GOOD:  the route exists with that verb, or the call is removed and its caller reads the served route
```

**Read the code:**

- Does a production proxy, BFF or gateway serve the path (grep 0d, § 2)?
- Is the caller a generated client (skip it) or hand-written?
- On failure, what does the caller render? A `catch` or `?? true` that grants access makes this the fail-open shape.
- Is the call behind a flag off everywhere?
- For `method-mismatch`, which side is wrong? Read the controller and the component.

**Finding when** the call ships and nothing serves (method, path) after normalisation.

**Proof:** the project's parity test fails listing the path. Otherwise, a generated test over the script's REF and ROUTE rows fails (V409, tier U). `--live`: the request returns 404 or 405 (tier L).

### 2. Uncalled route

**Class** PR-FS-2 · **Severity** low; medium when the route writes; Hardening when read-only and authenticated.

```
BAD:   @Get('api-keys') list() {…}        // no client, no reasons-file line, not public, not a webhook
GOOD:  called by a screen, or listed: "GET /api-keys  partner CLI (docs/partners.md)"
```

**Read the code:**

- Is the route a webhook, callback, OAuth, health, metrics, public or partner API, or a cron target? Or is it called by a mobile app or another service in the repo (§ 1)?
- Does it write?
- Was its caller removed in a refactor (search the history of the path string)?

**Finding when** it is none of those and no reasons-file line names it. Default is low; it is Hardening when read-only and authenticated.

**Proof:** the reverse half of the parity test, with a reasons file, fails (V409).

### 3. Link to a missing page

**Class** PR-FS-3 · **Severity** medium; high on primary navigation.

```
BAD:   <a href="/contacts">Contacts</a>     // only /api/* routers are mounted
       <Link to={`/s/${seller.id}`}>        // the router has /p/:id and /seller/products/:id
GOOD:  the target is a page route (dynamic segments match by shape) or a server-handled path (/logout, a download)
```

**Read the code:**

- Is the target handled by the server (§ 8), or reached from outside (§ 6)?
- Is it built from a route-constant map? Resolve the constant.
- Is the link in primary navigation (a header, sidebar or menu)?

**Finding when** the target matches no page of its package and no served GET route.

**Proof:** a route-table test over the link targets fails. A Playwright visit lands on the not-found boundary (V410).

### 4. Shipped placeholder

**Class** PR-FS-4 · **Severity** high on a reachable primary or priced route; low behind a flag off in every environment.

```
BAD:   "reports": { "title": "Coming soon" }     (en.json, rendered on /reports)
       raise HTTPException(status_code=501)     (POST /api/deals/{id}/convert is mounted and linked)
       return [ { id: 1, title: 'Acme renewal', value_cents: 480000 }, … ]   (GET /api/deals, no query)
       import { faker } from '@faker-js/faker'   (app code, not gated by import.meta.env.DEV)
GOOD:  the data comes from the store; the unfinished surface is hidden behind a flag that is off, or removed
```

**Read the code:**

- Is the surface reachable? Find the route that renders it and the flag that guards it, and read that flag's value in every environment (§ 4).
- For a catalog row: which component reads the key?
- For `mock-rows`: is there a repository, ORM or HTTP call in the same function (the script checked the lines above the return; read the whole function)?
- For `mock-import`: is it a declared demo build the production bundle excludes (§ 5)?

**Finding when** a user on a production route sees the placeholder or the fake rows.

**Proof:** a render or handler test asserts the copy is absent and the rows come from the store, or a 2xx where a 501 was (V411).

### 5. Dead affordance

**Class** PR-FS-5 · **Severity** medium.

```
BAD:   <button onClick={() => {}}>Export</button>   ·   <a href="#">More</a>   ·   <Button disabled>Pay</Button>
GOOD:  the control does what its label says, or it is not rendered
```

**Read the code:**

- Does a sibling control perform the action? A form's no-op submit beside a footer button that confirms is deliberate (§ 3; the script's `near=handler:<line>` points at the sibling).
- Is the control disabled by a permission or a status? Then it is not literal: that is a ui-ux state.
- Is it inside a skeleton or a design-system documentation page?

**Finding when** activating the control has no observable effect, and nothing else on the screen performs it.

**Proof:** an interaction test (click, then an asserted request, navigation or state change) fails (V412).

## Proof

The oracles, failing first and green after the fix, are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Product: V409 (route-parity join), V410 (page-route table), V411 (placeholder absence), V412 (interaction effect).

A static fact needs no runtime oracle when both ends are cited: a call path that no route table holds, read in both files. Every other row needs its oracle to fire. Without a harness, the row is Unconfirmed with the test written out.

The fix's regression set covers every variant of the class (`/product-fix`):

- a literal path, a template path and a wrapper path with no leading slash;
- a method mismatch;
- a missing prefix on one side;
- the fail-open fetch;
- `<Link to>`, `href`, `navigate()`, `redirect()` and `<form action>`;
- catalog, inline and template copy;
- mock rows in a handler, a hook and a service.

## Output

```
feature-surface-scan — lanes: nest 212 routes (api prefix + URI v1 stripped), route-object 64 pages; clients http (wrapper), fetch
Controls: web/src/shared/api/every-call-names-a-served-route.test.ts (run: exit 0); no reverse-route or link control

Findings: 2 · Unconfirmed: 1

1. web/src/entities/permission/use-access.ts:17                                       [report-with-fix]   critical
   §1 unserved call, fail-open — http.get('auth/me/permissions'); no @Get('me/permissions') under @Controller('auth')
   (api/src/auth/auth.controller.ts, read whole). The hook's catch returns ALL_PERMISSIONS, so the 404 renders the
   admin screens to a team member. Proof: the parity test, extended to this wrapper, lists the path (fails).
   Fix: serve GET auth/me/permissions from the session's grants; the hook fails closed on error.
2. web/src/layout/NavRail.tsx:41                                                        [report-with-fix]   high
   §3 primary-navigation link to no page — <Link to="/reports/cohorts">; the router (web/src/app/router.tsx) has
   /reports and /reports/:id only, and no API route serves the path. Proof: route-table test over the link targets
   (fails). Fix: remove the entry until the page ships (stop and ask: build, flag or remove).
3. web/src/i18n/en.json:212  billing.upgrade.cta = "Coming soon"                         [report-flagged]    medium
   §4 catalog placeholder — rendered by UpgradeCard.tsx:30. Unproven link: whether /settings/billing shows the card
   with the flag `billing_v2` on in production. Settling test: render /settings/billing with production flags.

Verification: 14 candidates → 2 findings · 1 unconfirmed · 4 hardening · 7 refuted (2 webhooks, 1 health, 1 PP-FS-3
no-op submit, 3 `mock-rows` in a declared demo build)

Class coverage:
  §1  unserved call        controlled (every-call-names-a-served-route.test.ts: exit 0) + script for the fetch() calls it skips: 31 calls → 1 finding
  §2  uncalled route       checked (18 rows → 0 findings; 11 webhook/health/public, 7 Hardening read-only)
  §3  link to no page      checked (52 links → 1 finding)
  §4  placeholder          checked (3 catalog + 1 copy + 0 not-implemented + 3 mock rows → 1 unconfirmed)
  §5  dead affordance      checked (2 rows → 0 findings; 1 PP-FS-3)
```

`[report-with-fix]`: both ends are read, the reachable route is named, the oracle failed, and the fix is local. `[report-flagged]`: one link is unproven (reachability, a flag value, a proxy not read), and the row names it and the settling test.

The coverage block lists **all five** classes on every run:

- `controlled (<test>: exit <n>)` when the project's own test covers the class and ran this session;
- `checked (k rows → m findings)` when the script ran on a present lane;
- `N/A (<reason>)` when the repo has no such surface (no client, no page router);
- `blocked (<reason>)` when the script or a grep failed, a lane is missing, or the root holds no API;
- `Live, unreviewed (k groups / n rows)` for a partial review, never `checked`.

## False positives / precedents

The verifier reads [`precedents/product.md`](../../../../snippets/precedents/product.md) § 1–9 and § 36–38 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Routes for outside callers** (§ 1). Webhooks, OAuth callbacks, health and metrics, public and partner APIs, mobile apps and other services in the repo.
- **Proxied paths** (§ 2). Next `rewrites`, a BFF or a gateway serves them. Vite `server.proxy` serves nothing in production.
- **A no-op handler beside a real one** (§ 3).
- **Placeholders out of reach** (§ 4). A doc comment, a flag off everywhere, a story or test-data file. The `placeholder=` attribute is not placeholder UI.
- **Demo builds** (§ 5).
- **Pages reached from outside the app** (§ 6).
- **The project's control decides** (§ 7).
- **Server-handled links** (§ 8).
- **Prefix sanity** (§ 9). Hundreds of unserved calls are one normaliser bug.
- **Disabled by design.** A status badge rendered as a disabled button ("forced active"). A control a permission or a pending request disables (ui-ux owns those states).

## When to run

- On a diff that adds or changes a client call, a route, a link, a router entry, a catalog value, a handler body that returns literals, or a button's handler.
- On every whole-repo `/audit-requirements --repo`, reporting all five classes. `/roadmap` detectors 1, 2 and 6 consume its rows when the product pack is installed.
- Before a launch (`launch-readiness` reads §1 and §4 for PRR-FS-1), and after a large refactor that moved routes or the client wrapper.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/product.md`](../../../../snippets/precedents/product.md). Under `/audit-requirements --repo`, that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without both ends, or without "no counterpart after the written search" and the search written out.
- Halt when the join fails the prefix-sanity check (§ 9). Fix the normaliser, never the rows.
- Do not mark a finding `[report-with-fix]` without an oracle that failed first. Without a harness it is `[report-flagged]` / Unconfirmed.
- Do not print `checked` for a class the project's control owns unless the control ran this session. A class whose script lane or grep did not run, or whose `rg` exited 2, is `blocked`.
- Do not write into the scanned repo. The script writes nothing. Any generated test goes under `${TMPDIR}` until `/product-fix` adds it.
- Do not propose deleting a route, a page or a placeholder without the stop-and-ask: build it, hide it behind a flag, or remove it. That decision is the owner's.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/audit-requirements --repo` (this pack) dispatches this skill and folds its coverage block into the class ledger. `/product-fix` closes the findings failing-first.
- `tracking-plan-scan` and `entitlement-consistency-scan` (this pack) are the other two product joins. `launch-readiness` (this pack) reads §1 and §4 as PRR-FS-1.
- `/roadmap` consumes §1, §3 and §4 for unbuilt capability. Frontend `routing-scan` (when installed) owns unknown-URL handling. Code-quality `dead-code-scan` (when installed) owns unmounted pages. Ui-ux `ui-state-scan` (when installed) owns disabled-while-pending and permission states.
