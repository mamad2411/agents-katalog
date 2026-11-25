---
name: http-contract-scan
description: "HTTP contract: action POST 201, missing → 200 null, unsafe GET, PUT/PATCH, pagination, spec drift — read-only."
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: http-contract-scan

## Premise

An endpoint can validate every field, map every error and still break its HTTP contract. Nest answers every `@Post` with 201, so `POST /otp/verify` tells a generated SDK it created something. A controller that returns a use case's `X | null` answers 200 with an empty body on Express and `null` on Fastify, and clients cache "empty" as success. `GET /orders/:id/cancel` is called by prefetchers, crawlers and retries. A PUT typed `Partial<Dto>` merges. A list sorted by `createdAt` alone skips and repeats rows across pages. A batch writes 47 of 50 rows and answers one 200. An `oasdiff` step without `--fail-on ERR` exits 0 on a breaking change. Express 5 reads `?filter[status]=paid` as a key named `filter[status]` and returns the unfiltered list. None of this fails loudly. This skill finds those places in the routes, the kernels and the CI that guards the spec. It proves each one with a request through the project's **own** bootstrap, or with a tool exit that cannot lie. Read-only: it never edits code.

Backend owns **the HTTP contract of one endpoint** (eval § 4.1): status, method, media type, pagination, batch, spec, the router and framework defaults that change them, and the outbound response handling nobody else owns. It owns `/backend-audit`'s HTTP rows (`http-contract-scan §1–§13`); `@api-reviewer` (this pack) judges them in refute mode.

**Every finding cites the route `<file:line>`, the contract source (P1: the project's OpenAPI, `ai/api-conventions.md` / `_extracted-idioms.md § API conventions`, or an RFC rule — without one the row is Hardening), the wiring row it depends on (adapter, interceptor, kernel, client wrapper), the request that shows it, and the fix in the project's own primitive** (its `@HttpCode` convention, its pagination kernel, its idempotency interceptor, its HTTP-client wrapper). A grep hit is a candidate. "The API contract looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/backend.md`](../../../../snippets/precedents/backend.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Backend, V328–V338, V346 and V354–V357.

## The rule

A candidate is a finding when all four hold. They apply `precedents/backend.md` § Reading the seven gates for backend to the HTTP contract.

1. **Part A holds: this is a mounted route, and it is what the row says it is.** The controller's module is imported by the app module the bootstrap uses. The route is a create, not an action (B-A3). The write is business state, not an audit row (B-A6). The list is a client-paged API list, not an internal drain (B-D4). The route word is a whole path segment, never a substring (B-D11).
2. **Part B holds at the installed version and on the adapter that ships.** Framework, router, adapter and client versions come from the lockfile (F1). Without one they are `UNREAD` and every version-gated row is Unconfirmed (V357). Nest rows were **measured on 12.1.3, both adapters** (research lab A, 2026-10-14). **Nest 11 was not run**, so the Nest-11 status and body defaults are Unconfirmed until V328/V329 runs on the installed version.
3. **Nothing already controls it, across files** (P5): a global response interceptor that sets the status, a pagination kernel that appends a tiebreak and clamps (B-D9), an idempotency interceptor of the reference shape (B-D14), an HTTP-client wrapper that refuses redirects, a documented uniform 404 (B-A9), a spec that documents the behaviour.
4. **The oracle fired, or the fact is two-ended.** Either the V-number ran through the real bootstrap (tier U) or a tool ran and exited honestly (tier T: oasdiff with `--fail-on ERR`, Schemathesis with ≥ 1 stateful link). Otherwise both ends of a static fact are cited (tier S): the handler and the default it inherits, or the kernel and the call that bypasses it. Without one, the row is `[report-flagged]` / Unconfirmed, with the request written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration (`precedents/backend.md` § Owned elsewhere). Without the owner's pack the row is listed tagged `<class> (owner pack <x> not installed)`, never graded here.
- **Idempotency-Key on money, credit, order, paid-send and webhook routes** → security `logic-race-scan` §4 (its grep 6 target set), when the security pack is installed. §6 here takes every **other** route that accepts a key; the split is printed by route (`HC6-split`). Without the security pack, those routes are listed tagged `BA-10 (owner pack security not installed)`. A missing key is `api-consistency-audit` #7; the storage contract is distributed-systems' `idempotency` pattern; job and consumer idempotency is distributed-systems' `messaging-scan`.
- **Authorization meaning** of any row (a GET that another user can call, an IDOR through a body id, a Fastify auth hook that misses a scope, a DataLoader that serves another tenant) → security, P3. **404 vs 403** is never backend's (B-A8). **Over-returning** and GraphQL schema disclosure → security `data-exposure-scan` §4/§11.
- **N+1 behind a list or a resolver** → database `n-plus-one-scan`. **Concurrent PUT lost update** → database `transaction-scan` §8. **Deep-offset query cost** → the performance pack; inbound size limits → performance `request-path-scan` §13.
- **Outbound timeouts** → performance `request-path-scan` §12. **Outbound retries** (library defaults that retry POST, a provider key minted per attempt) → distributed-systems `retry-deadline-scan` §5. **Status unchecked** → code-quality `error-handling-scan` §3. **Response cast with no check** → code-quality `type-safety-scan` §1. A **redirect to an internal host** → security `ssrf-scan` §4. §12 here owns only a body never closed (BO-04) and a POST turned into a GET (BO-06).
- **Upload caps** → security `file-access-scan` §2. **Temp files left on failure** → code-quality `error-handling-scan` §7. §13 here owns part order and partial uploads.
- Same pack: **a missing `return` after `http.Error`** (BF-GO-01) and Fastify reply lifecycle → `edge-error-scan` §5. **Status class of an error** (409 vs 500 for a conflict) → `edge-error-scan` §2. **A response field dropped or a value changed by a serializer** (Fastify response schema, FastAPI `response_model`) → `wire-format-scan` §3. **`null` into a NOT NULL column through `@IsOptional`** → `validation-boundary-scan` §5 (§5 here owns the PATCH *semantics* and defaults on Update DTOs). **Consistency across sibling endpoints** → `api-consistency-audit` (#2, #4, #5, #8e, #14): a route that is both wrong and inconsistent is one HC finding, and the consistency row cites it. **Consumer-driven contracts** → testing `contract-test`.
- **Where a route is really mounted.** `dto-types.py --routes` adds `mounted` (global prefix minus its `exclude`, URI version, `RouterModule` path), `version` and `class_decorators` to the HANDLER rows read here (with `--enums`, ENUM rows also gain `values`). Read `mounted` when a row must cite the URL a client calls. The migration pack's `paired-inventory` keys its route lanes on it, when the migration pack is installed; without that pack nothing here changes.

## Adapt to the codebase — the lanes

Read the framework **with its version** (F1) and the wiring (grep 0) first. Each default is tagged `[V]` (ran, research labs A/B, 2026-10-14) or `[K]`/`[K?]` (docs or secondary, not run). A `[K]` default leaves its verdict Unconfirmed until the § oracle runs on the installed version.

| Lane | Status and method defaults that decide verdicts | Router and parser traps | Decoy shape |
|---|---|---|---|
| **NestJS** (Express or Fastify adapter) | `@Post` → 201 unless `@HttpCode`; `@HttpCode(204)` returning an object sends an empty body; a `null` return → Express 200 empty, Fastify 200 `"null"`; wrong method → 404 on both adapters [V 12.1.3] | Express → Fastify deltas: body limit 100 KB → 1 MiB, empty JSON body 201 → 400, `text/plain` `undefined` → string, XML 201 → 415, `__proto__` accepted → 400 [V 12.1.3] | an action POST with `@HttpCode(200)`; `@Res({ passthrough: true })` routes that set their own status |
| **Express 5** (path-to-regexp 8) | wrong method → 404, while auto-OPTIONS still advertises `Allow` [V 5.3]; `express.json()` leaves `req.body` undefined for other types (no 415) | `/:id?`, `/*`, `/:id(\d+)` **throw at boot**; the `simple` query parser turns `?filter[status]=x` into one flat key; `req.query` writes are lost; routing is case-insensitive and non-strict (`/Q/` matches `/q`) [V 5.3] | `/*splat`, `/o{/:id}` (the v5 syntax) |
| **Fastify 5** | wrong method → 404 [V 5.12]; an unknown content type → 415 [V under Nest 12.1.3] | `onRequest` hooks run before the body is parsed; hooks and error handlers inside a child plugin miss sibling routes unless wrapped with `fastify-plugin` [K] | a hook added in the bootstrap on the root instance (no encapsulation) |
| **Koa 3 + `@koa/router`** | no 405 unless `router.allowedMethods()` is mounted [R] | `ctx.body` semantics → `edge-error-scan` §5 | — |
| **GraphQL** (Apollo Server 5, Mercurius 16) | 200 with `errors[]` is the protocol (B-A17) | one `null` inside `[T!]!` nulls the **whole** `data` [V both]; a DataLoader at module scope caches across requests | a documented nullable field |
| **DRF 3.18 / Django 6.1** | PUT with omitted optional fields behaves like PATCH (fields with model defaults are `required=False`) [V 3.18.3]; `partial=True` forced on PUT skips required fields [K] | pagination over an unordered queryset warns (`UnorderedObjectListWarning`) and skips or repeats rows [V] | a model `Meta.ordering` with a unique last key |
| **FastAPI 0.143** | — | `Depends` is cached per request, so a side-effecting dependency used twice runs once [V] | `Depends(dep, use_cache=False)` |
| **Go net/http 1.22+** | method patterns (`"POST /orders/{id}"`) give 405 + `Allow`; a trailing slash 404s; `GODEBUG=httpmuxgo121=1` reverts both [V go1.27.2] | a pattern with no method matches every method [K] | — |
| **axum 0.8 / actix-web 4** | — | axum 0.7's `/:id` path syntax panics on 0.8 [K] | `/{id}` |
| **Outbound clients** | `fetch` and axios follow a 302 on POST as a GET and drop the body [V]; a Go `resp.Body` never closed leaks the connection (golangci-lint `bodyclose` flags it) [V 2.14] | — | a wrapper that sets `redirect: 'manual'` once for every caller (P5) |

## Tool lane and ledger

Each tool prints `ran` / `blocked (<why>)` / `NOT-RUN (<why>)` in the output header.

| Tool | Command | Covers | Limits |
|---|---|---|---|
| `dto-types.py` (the `validation-boundary-scan` skill's script, this pack; installed as `.claude/skills/validation-boundary-scan/scripts/dto-types.py`), Python 3 stdlib | `python3 -I "$DT" --params --decorator-blocks <roots>`; `--action-words=a,b` replaces the default list | HANDLER rows: route (controller prefix joined), verb, declared return type, flags `post-no-httpcode`, `action=<word>@<segment>` (a whole path segment, or its last `-`/`_` word), `res` / `res-passthrough` with `res-status(<arg>)` or `res-no-status` beside it (the handler body's `<res>.status(` / `.code(` / `.statusCode =`), `httpcode=<arg>`, `returns-nullable`, `204-returns(<type>)`; PARAM rows with the route (project wrappers such as `@ContractBody(schema)` print as `ContractBody>Body`); PROP rows with every decorator and `initialiser(<expr>)` on a validated field | TypeScript/Nest only; reads a handler body only for the status call — a write inside a GET, or a status set in a helper the handler calls, is read by hand from the row. **Co-install:** standard mode copies every backend skill; on a minimal install, or with `validation-boundary-scan` removed, the grep prints `dto-types NOT-RUN` and §1/§2/§4/§5/§8 Nest rows are `blocked`, never `checked` |
| oasdiff 1.33.0 (Apache-2.0), the Go binary or `tufin/oasdiff:v1.33.0`, pinned | `oasdiff breaking <committed> <generated> --fail-on ERR` (`<generated>` from the code in the same run) | §10 spec-to-spec: required added, enum changed, type changed, success status removed, path removed | **exit 0 without `--fail-on ERR`** [V]: such a run is `NOT-RUN (no --fail-on)`, never clean. npm has no oasdiff (`@tufin/oasdiff` 404s, `oasdiff` is a placeholder) [V]. Never below 1.18.1 (CVE-2026-53508). Nothing committed to diff → `NOT-RUN (no baseline)`; the fix is `api-snapshot`'s baseline step |
| Schemathesis 4.31.0 (MIT) | `st run <spec> --url <base> --checks all --max-examples 50 --seed 1 --max-time 300 --report junit` on a local or `--live` non-production base | `status_code_conformance`, `response_headers_conformance` (`Location`), `unsupported_method` + `allow_header_conformance` (§3), `use_after_free` + `ensure_resource_availability` (§2), `response_schema_conformance` (§10) | stateful checks walk `links` **on the response object** only: print `API Links: N covered`; **0 covered = `NOT-RUN (no links on response objects)`** [V]. `ignored_auth` / `object_level_authorization` are security's. Needs a spec and a running app |
| Prism 5.16.0 (Apache-2.0) | `prism proxy openapi.yaml http://localhost:3000 --errors` in front of the e2e suite | §10: every request/response pair the suite already sends | sees only the traffic the suite sends |
| golangci-lint 2.14.0 | `golangci-lint run ./...` with `linters.default: none` + `bodyclose` | §12 BO-04 [V] | GPL-3.0 binary (run only); `NOT-RUN` without a Go module |
| Django warnings as gates | `python -W error::django.core.paginator.UnorderedObjectListWarning manage.py test` | §7 BF-DJ-04 [V] | scope the filter; it also fails third-party warnings |

Spectral, Redocly and vacuum findings are never code findings (B-A18). `api-snapshot` (this pack) owns the committed baseline and the CI gate; §10 here reports whether that gate can fail.

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2-safe). Grep **N** feeds detector **§N**. F1 and grep 0 are the gates every § reads first, and every row carries its grep id. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first**, exclusions last (rg-glob-order). With an explicit root, globs match relative to it, so exclusions start with `**/`. An `rg` exit 2 is a failed grep, never zero hits. A decorator block ("`@Post` with no `@HttpCode`") is read by `dto-types.py`, never by `-A<n> | rg -v` (a per-line negation cannot prove an absence: rg-context-negation). Route words match **whole segments** (B-D11).

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api apps/admin). Manifests, specs and CI always search .
DT="${DT:-.claude/skills/validation-boundary-scan/scripts/dto-types.py}"; SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/hc.XXXXXX")}"; mkdir -p "$SCAN"
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,cs,go,php,rb,rs}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/test_*.py' -g '!**/*_test.go' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,db/migrate,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**'
   -g '!**/{openapi,swagger}*.{json,yaml,yml}' -g '!**/{docs,ai,.claude}/**' -g '!**/{venv,site-packages}/**' -g '!**/pkg/mod/**')
L() { sed "s/^/$1 /"; }   # labels every row with its grep id
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines
UNSAFE='cancel|delete|remove|destroy|approve|reject|confirm|unsubscribe|activate|deactivate|enable|disable|reset|sync|run|trigger|retry|send|resend|publish|archive|restore|void|refund|charge|execute'
# F1 framework, router, client and spec-tool versions — ranges from manifests, exact from lockfiles (gate 3; V357)
rg -n --no-heading --pcre2 '"(@nestjs/(?:core|platform-fastify|platform-express|swagger|graphql)|express|fastify|koa|@koa/router|koa-router|@trpc/server|@apollo/server|mercurius|graphql|dataloader|@fastify/multipart|multer|busboy|axios|undici|got|node-fetch)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' . | L F1
rg -n --no-heading --pcre2 '"node_modules/(?:express|fastify|@nestjs/core|koa|@fastify/multipart|axios)":\s*\{|^\s*["\x27]?/?(?:express|fastify|@nestjs/core|koa|axios)@\d[\w.-]*' -g '**/{package-lock.json,pnpm-lock.yaml,yarn.lock}' -g '!**/node_modules/**' . | L F1
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(django|djangorestframework|fastapi|flask|starlette|requests|httpx)\b\s*[=<>~!^]|^go\s+1\.\d+|github\.com/(gin-gonic/gin|labstack/echo/v4|go-chi/chi/v5)\s+v|^\s*(axum|actix-web)\s*=|"laravel/framework"\s*:|spring-boot-starter-web\b' -g '**/{pyproject.toml,requirements*.txt,Pipfile,poetry.lock,go.mod,Cargo.toml,composer.json,pom.xml,build.gradle*}' -g '!**/node_modules/**' . | L F1
# 0 THE WIRING — adapter, response interceptors, the list kernel, the idempotency store. Every § reads this first (P5)
rg -n --no-heading --pcre2 '\bnew\s+(?:Fastify|Express)Adapter\s*\(|\bNestFactory\.create\s*<\s*Nest(?:Fastify|Express)Application|\bAPP_INTERCEPTOR\b|\buseGlobalInterceptors\s*\(|\bset\s*\(\s*["\x27]query parser["\x27]|\bGODEBUG=[^\n]*httpmuxgo121' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L W0
rg -n --no-heading --pcre2 '\b(?:export\s+)?(?:async\s+)?(?:function|class|const|def|func)\s+\w*(?:[Pp]aginat|[Pp]age(?:Query|Request|Result|Params|Options|d)\b|[Cc]ursor(?:Page|Paginat))\w*|\b(?:MAX_PAGE_SIZE|MAX_LIMIT|max_page_size|maxPageSize|max_limit)\b\s*[:=]|\bpagination_class\s*=|DEFAULT_PAGINATION_CLASS' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L W0-kernel
rg -n --no-heading --pcre2 '\b(?:class|function|const|def|func|interface)\s+\w*[Ii]dempoten\w*' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L W0-idem
echo "W0-idem route-level uses: $(rg -c --pcre2 '@Idempotent\w*\s*\(|[Ii]dempotency-?[Kk]ey["\x27]?\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
# 1, 2, 4, 5, 8 (Nest): dto-types HANDLER / PARAM / PROP rows — route, verb, declared return, @HttpCode, @Res, decorator BLOCKS
if command -v python3 >/dev/null 2>&1 && [ -f "$DT" ]; then python3 -I "$DT" --params --decorator-blocks "${ROOTS[@]}" > "$SCAN/hc.tsv" 2> "$SCAN/hc.ledger"; echo "dto-types exit $?"; head -3 "$SCAN/hc.ledger"; else echo 'dto-types NOT-RUN (python3 or validation-boundary-scan absent): HC1/HC2/HC4/HC5/HC8 Nest rows blocked'; : > "$SCAN/hc.tsv"; fi
T="$SCAN/hc.tsv"
awk -F'\t' '$1=="HANDLER" && $7 ~ /post-no-httpcode/ && $7 ~ /action=/ {print "HC1a", $2, $5, $7}' "$T"
awk -F'\t' '$1=="HANDLER" && $4=="POST" && $7 ~ /(^| )res/ && $7 !~ /httpcode=/ && $7 ~ /action=/ {print "HC1b", $2, $5, ($7 ~ /res-no-status/ ? "res-no-status (the reply keeps the POST default 201)" : $7)}' "$T"
awk -F'\t' '$1=="HANDLER" && $7 ~ /204-returns/ {print "HC1c", $2, $5, $7}' "$T"
awk -F'\t' '$1=="HANDLER" && $4 ~ /^(GET|HEAD)$/ && $7 ~ /returns-nullable/ {print "HC2", $2, $5, $6}' "$T"
awk -F'\t' -v W="$UNSAFE" '$1=="HANDLER" && $4 ~ /^(GET|HEAD|ALL)$/ {n=split($5, seg, "/"); for (i=1;i<=n;i++) if (seg[i] ~ "^(" W ")$" || seg[i] ~ "-(" W ")$") {print "HC4", $2, $4, $5; break}}' "$T"
awk -F'\t' '$1=="PARAM" && $3 ~ /(^|>)Body$/ && $11 ~ /^PUT / && ($7=="mapped" || $6 ~ /^(Partial|Update|Patch|Edit)/) {print "HC5", $2, $11, $6, $7}' "$T"
awk -F'\t' '$1=="HANDLER" && $4=="POST" {n=split($5, seg, "/"); for (i=1;i<=n;i++) if (seg[i] ~ /^(bulk|batch)([-_].*)?$|[-_](bulk|batch)$/) {print "HC8", $2, $5; break}}' "$T"
awk -F'\t' '$1=="PROP" && $6 ~ /@ApiPropertyOptional/ && $6 !~ /@(IsOptional|ValidateIf|IsAbsentOr)/ && $6 ~ /@(IsDefined|IsNotEmpty|ArrayMinSize|IsNotEmptyObject)/ {print "HC10-optionality(spec optional, server requires)", $2, $3}' "$T"
# 1 other stacks: 201 sites in files that never set Location (1d); 204 sent with a body (1e)
rg -l0 --pcre2 '\.(?:status|code)\s*\(\s*201\s*\)|\bHttpStatus\.CREATED\b|\bHTTP_201_CREATED\b|status_code\s*=\s*201\b|\bWriteHeader\s*\(\s*http\.StatusCreated\s*\)|\bStatusCode\s*\(\s*201\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match -i --pcre2 '\blocation\b|ResponseEntity\.created\s*\(|CreatedAtAction|CreatedAtRoute|get_success_headers' | L HC1d
rg -n --no-heading --pcre2 '\.(?:status|code)\s*\(\s*204\s*\)\s*\.\s*(?:json|send)\s*\(\s*[^)\s]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC1e
# 2 hexagonal and other stacks: a use case injected into a controller whose output admits null (2b); a find result returned as-is (2c)
rg -n --no-heading --pcre2 '\bUseCase\s*<[^>\n]*\|\s*(?:null|undefined)\s*>|\bres\.(?:json|send)\s*\(\s*await\s+[\w.]+\.(?:findOne|findUnique|findFirst|findById|findByPk|get)\w*\s*\(|\.orElse\s*\(\s*null\s*\)\s*\)?\s*;|\.filter\([^\n]*\)\.first\(\)' -g '**/*{controller,Controller,views,handlers,routes,router,resource,Resource}*.*' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC2b
rg -n --no-heading --pcre2 '\breturn\s+(?:await\s+)?this\.\w+(?:\.\w+)*\.(?:findOne|findUnique|findFirst|findById|findByPk|findOneBy)\s*\(' -g '**/*.controller.{ts,js}' -g '**/*Controller.{java,kt}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC2c
# 3 method and media negotiation: catch-all parsers, routers with no allowedMethods, any 405/415 at all
rg -n --no-heading --pcre2 '\baddContentTypeParser\s*\(\s*["\x27]\*["\x27]|\bexpress\.(?:json|text|raw)\s*\(\s*\{[^}\n]*\btype\s*:\s*["\x27]\*/\*|["\x27](?:koa-router|@koa/router)["\x27]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC3
echo "allowedMethods(: $(rg -c --pcre2 '\ballowedMethods\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') · 405/415 emitted or documented: $(rg -c --pcre2 '\b(?:405|415)\b|METHOD_NOT_ALLOWED|UNSUPPORTED_MEDIA_TYPE|MethodNotAllowed|UnsupportedMediaType' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}')"
# 4 other stacks: a GET route literal whose WHOLE segment is an unsafe word (never a substring: B-D11)
rg -n --no-heading --pcre2 '(?:\b(?:app|router|r|api|route|mux|e|g|v1|group)\.(?:get|Get|GET|head|all)\s*\(|@(?:GetMapping|HttpGet)\s*\()\s*["\x27\x60][^"\x27\x60\n]*(?:^|/)(?:cancel|delete|remove|destroy|approve|reject|confirm|unsubscribe|activate|deactivate|enable|disable|reset|sync|run|trigger|retry|send|resend|publish|archive|restore|void|refund|charge|execute)(?:[-_]\w+)?(?:/|$|[?"\x27\x60])' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC4b
rg -n --no-heading --pcre2 '\b(?:re_)?path\s*\(\s*r?["\x27][^"\x27\n]*(?:^|/)(?:'"$UNSAFE"')(?:[-_]\w+)?(?:/|$|["\x27])' -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L 'HC4b-django(method unknown: read the view)'   # path() routes every method; a @require_POST view clears it
# 5 PUT that merges (5b); initialisers on Update/Patch DTOs, BV-14 (5c); partial and patch dialects (5d)
rg -n --no-heading -U --pcre2 '\.put\s*\(\s*["\x27][^"\x27\n]+["\x27][^\n]*\n?(?:[^\n]*\n){0,12}?[^\n]*(?:Object\.assign\s*\(\s*\w+\s*,\s*(?:req\.body|body|dto|data)\b|\{\s*\.\.\.\w+\s*,\s*\.\.\.(?:req\.body|body|dto|data)\b)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'Object\.assign|\.\.\.' | L HC5b
awk -F'\t' '$1=="PROP" && $3 ~ /^[A-Za-z]*(Update|Patch|Edit)[A-Za-z]*\./ && $5 ~ /initialiser\(/ {print "HC5c-dto", $2, $3, $5}' "$T"   # Nest DTOs: a validated field with a default; the rg below covers the rest
rg -l0 --pcre2 '\bclass\s+(?:Update|Patch|Edit)\w*(?:Dto|Input|Body|Request|Command)\b' -g '*.ts' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '^\s+(?:readonly\s+)?\w+[?!]?\s*(?::\s*[^=;\n]+)?\s=\s(?!>)[^;\n]+;' | "${NC[@]}" | L HC5c
rg -n --no-heading --pcre2 '\bpartial\s*=\s*True\b|\bdef\s+update\s*\(|application/merge-patch\+json|application/json-patch\+json|\bfast-json-patch\b|\bapplyPatch\s*\(' -g '*.{py,ts,js,java,kt,go}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC5d
# 6 Idempotency-Key HTTP semantics inside the store grep 0 found: key composition, body fingerprint, in-flight state; then the S §4 / HC §6 split by route
rg -l0 --pcre2 '\b(?:class|function|const|def|func)\s+\w*[Ii]dempoten\w*' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading -i --pcre2 '\b(?:tenant|principal|actor|caller|user_?id|userId|sub)\w*\b[^\n]{0,60}(?:key|token|scope)|\b(?:fingerprint|bodyHash|body_hash|requestHash|request_hash)\b|\b(?:in[-_]?flight|in[-_]?progress|lease|locked_at|OUTCOME_UNKNOWN)\b' | "${NC[@]}" | head -30 | L HC6
rg -l0 --pcre2 '\b(?:class|function|const|def|func)\s+\w*[Ii]dempoten\w*' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 -i --pcre2 '(?:headers?|META)\s*(?:\[\s*|\.get\s*\(\s*)["\x27](?:idempotency-key|HTTP_IDEMPOTENCY_KEY)["\x27]|\b(?:get|header|getHeader)\s*\(\s*["\x27]idempotency-key["\x27]|@(?:Headers?|RequestHeader)\s*\(\s*(?:name\s*=\s*)?["\x27]idempotency-key["\x27]' > "$SCAN/hc-idem.l0"   # the absences, in the files that read the request header
xargs -0 -r rg --files-without-match -i --pcre2 '\b(?:tenant\w*|principal\w*|actor\w*|caller\w*|user_?id|user\.id|(?:req|request)\.user|account_?id|org_?id|merchant_?id|sub)\b' < "$SCAN/hc-idem.l0" | L 'HC6-no-principal(the stored key names no caller or tenant: read the key composition)'
xargs -0 -r rg --files-without-match -i --pcre2 '\b(?:fingerprint\w*|body_?hash|request_?hash|payload_?hash|sha256|hashlib|createHash|digest)\b' < "$SCAN/hc-idem.l0" | L 'HC6-no-fingerprint(a replay never compares the body: read the replay branch)'
awk -F'\t' '$1=="HANDLER" && $8 ~ /@Idempotent/ {s = ($5 ~ /(^|\/|-)(pay|payment|payments|charge|charges|refund|refunds|payout|payouts|transfer|transfers|credit|credits|wallet|order|orders|checkout|invoice|invoices|webhook|webhooks|sms|otp|send)([-\/]|$)/) ? "S4" : "HC6"; n[s]++} END {print "HC6-split @Idempotent routes:", n["S4"]+0, "-> security logic-race-scan §4 (money/credit/order/paid-send/webhook);", n["HC6"]+0, "-> HC §6"}' "$T"
# 7 pagination, sites that bypass the kernel: one non-unique sort key with a limit (7a), a limit from input with no bound (7b), cursors (7c), DRF over an unordered queryset (7d)
rg -n --no-heading -U --pcre2 '\b(?:take|limit|first)\s*:\s*(?!1\s*[,}\n])[^,}\n]+,[^;]{0,240}?\borderBy\s*:\s*\{\s*(?:(?!id\s*:)\w+\s*:\s*[^,{}\n]+)\}|\borderBy\s*:\s*\{\s*(?:(?!id\s*:)\w+\s*:\s*[^,{}\n]+)\}[^;]{0,240}?\b(?:take|limit|first)\s*:\s*(?!1\s*[,}\n])|\.orderBy\s*\(\s*["\x27](?![\w]+\.id["\x27]|id["\x27])[\w.]+["\x27]\s*(?:,\s*["\x27](?:ASC|DESC|asc|desc)["\x27])?\s*\)\s*\.\s*(?:take|limit)\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'orderBy' | "${NC[@]}" | L HC7a
rg -n --no-heading -i -U --pcre2 '\border\s+by\s+(?![\w"]+\."?id\b|"?id\b)[\w."]+(?:\s+(?:asc|desc))?\s+(?:nulls\s+(?:first|last)\s+)?limit\s+(?!1\b)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC7a
awk -F'\t' '$1=="PROP" && $3 ~ /\.(limit|take|pageSize|page_size|perPage|per_page|size|first|last|top|count)$/ && $6 !~ /@Max\(/ {print "HC7b(limit-like DTO field, no @Max)", $2, $3, $6}' "$T"
rg -n --no-heading --pcre2 '\b(?:take|limit|perPage|per_page|pageSize|page_size|size)\s*[:=]\s*(?:Number\s*\(\s*|parseInt\s*\(\s*|int\s*\(\s*|\+)?(?:req\.query|request\.query|request\.args|request\.GET|request\.query_params|ctx\.query)(?:\.\w+|\.get\s*\(\s*["\x27]\w+["\x27][^)]*\)|\[["\x27]\w+["\x27]\])' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC7b
rg -n --no-heading --pcre2 '\b(?:take|limit|skip|offset)\s*:\s*(?:q|query)\.\w+\s*[,})]' -g '*.{js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC7b
rg -n --no-heading --pcre2 '(?i:cursor)\w*\s*[:=][^\n]*(?:base64|btoa\s*\(|toString\s*\(\s*["\x27]base64)|\b(?:encodeCursor|decodeCursor)\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC7c
rg -l0 --pcre2 '\bpagination_class\s*=|\bPaginator\s*\(' -g '*.py' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\bqueryset\s*=\s*\w+\.objects\.(?:all|filter)\s*\((?![^\n]*\border_by\s*\()' | L HC7d
# 8 batch: per-item try/catch in a loop under one status (read only the loops an HC8 route reaches)
rg -n --no-heading -U --pcre2 '\bfor\s*\(\s*(?:const|let)\s+\w+\s+of\s+[^)\n]+\)\s*\{\s*\n?\s*try\s*\{|\bfor\s+\w+\s+in\s+[^:\n]+:\s*\n\s*try\s*:|\bPromise\.allSettled\s*\(' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'for|allSettled' | "${NC[@]}" | L HC8b
# 9 deprecation signalling
rg -n --no-heading --pcre2 '\bdeprecated\s*[:=]\s*(?:true|True)\b|@ApiOperation\s*\(\s*\{[^}\n]*\bdeprecated\b|["\x27](?:Deprecation|Sunset)["\x27]\s*[,:]' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC9
# 10 spec drift: committed specs and their response-object links, generators, CI diff steps (flag present?), runtime fuzzers
rg --files -g '**/{openapi,swagger}*.{json,yaml,yml}' -g '**/*.{openapi,oas}.{json,yaml,yml}' -g '!**/node_modules/**' . | head -20 | L HC10-spec
rg -c --pcre2 '^\s*["\x27]?links["\x27]?\s*:' -g '**/{openapi,swagger}*.{json,yaml,yml}' -g '!**/node_modules/**' . | L HC10-links
rg -n --no-heading --pcre2 '\bSwaggerModule\.createDocument\s*\(|\bOpenApiGeneratorV3\d?\b|\bzod-to-openapi\b|\bdrf_spectacular\b|\bspringdoc\b|\bswaggo/swag\b|\bget_openapi\s*\(|\bfastify-swagger\b|@fastify/swagger\b' "${CODE[@]}" -g '**/package.json' -g '**/{pyproject.toml,requirements*.txt,go.mod,pom.xml,build.gradle*}' "${X[@]}" . | "${NC[@]}" | head -20 | L HC10-gen
rg -n --no-heading --hidden --pcre2 '\boasdiff\b[^\n]*|\bschemathesis\b|\bst\s+run\b|\bprism\s+proxy\b' -g '**/.github/workflows/*.{yml,yaml}' -g '**/.gitlab-ci.yml' -g '**/{Makefile,Justfile,Taskfile.yml,package.json,*.sh,Dockerfile*}' -g '!**/node_modules/**' -g '!**/.git/**' . | awk '{ t = ($0 ~ /oasdiff.*breaking/ && $0 !~ /--fail-on/) ? "  <- NOT-RUN (no --fail-on)" : ""; if ($0 ~ /oasdiff[[:space:]]+changelog/) t = "  <- informational (changelog never fails: not the gate)"; if ($0 ~ /npx @tufin\/oasdiff|npm i(nstall)? .*oasdiff/) t = "  <- NOT-RUN (npm has no oasdiff)"; print $0 t }' | L HC10-ci
# 11 router and framework traps by version: Express 5 route syntax (11a), query-parser reads (11b), path compares in middleware (11c), Fastify hooks and plugins (11d), GraphQL lists and DataLoader (11e), axum 0.7 paths (11f), Express-only imports under the Fastify adapter (11g)
rg -n --no-heading --pcre2 '\.(?:get|post|put|patch|delete|all|use|route)\s*\(\s*["\x27\x60][^"\x27\x60\n]*(?:/:\w+\?|/\*(?![\w{])|/:\w+\()' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC11a
rg -n --no-heading --pcre2 '\breq\.query\.\w+\.\w+|\breq\.query\[[^\]\n]+\]\.\w+|\breq\.query\.\w+\s*=(?!=)|\breq\.query\s*=(?!=)' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC11b
rg -n --no-heading --pcre2 '\breq\.(?:path|url|originalUrl)\s*===?\s*["\x27]|\breq\.(?:path|url|originalUrl)\.startsWith\s*\(' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC11c
rg -n --no-heading -U --pcre2 '\baddHook\s*\(\s*["\x27]onRequest["\x27](?:(?!\baddHook\b)[\s\S]){0,800}?\b(?:request|req)\.body\b' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'addHook|\.body\b' | L HC11d
rg -l0 --pcre2 '\b(?:export\s+default\s+)?(?:async\s+)?function\s*\w*\s*\(\s*(?:fastify|instance|app|server)\s*[:,)]' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\.addHook\s*\(|\.setErrorHandler\s*\(' | xargs -0 -r rg --files-without-match --pcre2 '\bfastify-plugin\b|\bfp\s*\(' | L HC11d-nofp
{ rg -n --no-heading --pcre2 '\[\w+!\]!' -g '*.{graphql,gql}' "${X[@]}" "${ROOTS[@]}"; rg -l0 --pcre2 '\btypeDefs\b|\bbuildSchema\s*\(|\bmakeExecutableSchema\s*\(' -g '*.{ts,js,mjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\[\w+!\]!'; } | head -20 | L HC11e
rg -n --no-heading --pcre2 '^(?:export\s+)?(?:const|let|var)\s+\w+\s*=\s*new\s+DataLoader\s*(?:<[^\n]*?>)?\s*\(' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | L HC11e
rg -n --no-heading --pcre2 '\.route\s*\(\s*"[^"\n]*/:\w+' -g '*.rs' "${X[@]}" "${ROOTS[@]}" | L HC11f
for r in "${ROOTS[@]}"; do rg -q --pcre2 '\bFastifyAdapter\b' -g '*.ts' "${X[@]}" "$r" && rg -n --no-heading --pcre2 "from\s+[\"\x27](?:@nestjs/platform-express|express|body-parser|multer)[\"\x27]" -g '*.ts' "${X[@]}" "$r" | "${NC[@]}" | L HC11g; done   # per root: an Express app beside a Fastify one is not a trap
# 12 outbound responses: Go bodies never closed (12a), Python streams outside a with block (12b), the redirect setting (12c-setting), POST callers with default redirects (12c)
rg -l0 --pcre2 '"net/http"' -g '*.go' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 --pcre2 '\b(?:resp|res|response|rsp|r)\w*\s*,\s*\w+\s*:?=\s*[\w.]+\.(?:Do|Get|Post|PostForm|Head)\s*\(' | xargs -0 -r rg --files-without-match --pcre2 '\.Body\.Close\s*\(\s*\)' | L HC12a
rg -n --no-heading --pcre2 '^(?!\s*(?:with|async\s+with)\b)[^\n]*\bstream\s*=\s*True\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC12b
rg -n --no-heading --pcre2 '\bredirect\s*:\s*["\x27](?:manual|error|follow)["\x27]|\bmaxRedirects\s*:|\bbeforeRedirect\b|\bfollow_redirects\s*=|\ballow_redirects\s*=' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | L HC12c-setting
rg -l0 --pcre2 '\bfetch\s*\(|\baxios(?:\.(?:post|request|create))?\s*\(|\bgot(?:\.post)?\s*\(|\bundici\.request\s*\(|\brequests\.(?:post|request)\s*\(|\bhttpx\.(?:post|Client|AsyncClient)\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -l0 -i --pcre2 '\bmethod\s*[:=]\s*["\x27]post["\x27]|\b(?:axios|got|requests|httpx|client)\.post\s*\(' | xargs -0 -r rg --files-without-match --pcre2 '\bredirect\s*:\s*["\x27](?:manual|error)["\x27]|\bmaxRedirects\s*:\s*0\b|\bbeforeRedirect\b|\ballow_redirects\s*=\s*False|\bfollow_redirects\s*=\s*False' | L HC12c
# 13 multipart: a file callback reading fields (13a), part loops and field reads (13b), stream-to-storage completion (13c)
rg -n --no-heading -U --pcre2 '\b(?:fileFilter|destination|filename)\s*[:(][^}]{0,400}?\breq\.body\.\w+' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'req\.body' | "${NC[@]}" | L HC13a
rg -l0 --pcre2 '\b(?:request|req)\.(?:file|parts|files)\s*\(' -g '*.{ts,mts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\b(?:request|req)\.(?:file|parts|files)\s*\(|\.fields\.\w+|\bpart\.(?:type|fieldname)\b' | L HC13b
rg -n --no-heading -U --pcre2 '\bfinally\s*\{[^}]{0,300}?\b[Cc]omplete[Mm]ultipart[Uu]pload|\bUpload-Offset\b|\bnew\s+Upload\s*\(\s*\{' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | rg --pcre2 'Complete|Upload' | "${NC[@]}" | L HC13c
```

When `python3` or `dto-types.py` is absent, the Nest rows of §1, §2, §4, §5 and §8 print `blocked (dto-types NOT-RUN)`. Never fall back to a line regex: on the real repo the action-word regex matched 56 routes for about 10 true ones, the block filter took it to 19, and the whole-segment rule to 12.

### Measured (2026-10-14)

- **Real repo, read-only** (a NestJS 11 monorepo on Fastify with MikroORM, about 3,700 `.ts` files under the API's `src`, `ROOTS=(src)`; no lockfile and no `.github/` in that first copy): the block runs in about 5 s and prints 180 lines. dto-types read 3,741 files: 588 GET, 407 POST, 126 PUT, 75 PATCH and 102 DELETE handlers. Grep 0 printed the Fastify adapter, three `APP_INTERCEPTOR`s (one is the idempotency interceptor), and the paging kernel (`resolvePageQuery`, `MAX_PAGE_SIZE = 100`); `HC12c-setting` printed the HTTP-client wrapper's `redirect: 'manual'`.
  - **Full tree, 2026-10-14** (run from the repo root, `ROOTS=(apps/api/src)`, lockfile, CI and the shared contracts package readable): 4.9 s, 183 lines, dto-types read 3,722 files. F1 now prints the locked `@nestjs/core` 11.2.6 and `fastify` 5.12.3 (and `express` 5.2.1, locked as an optional peer of `@nestjs/core`; the adapter that ships is Fastify). Same: HC1a 12, HC1b 3, HC3 1, HC5 16, HC7a 25, HC8 13 + 22. Changed: every HC5 body now prints `custom-pipe(ContractPipe)` and **HC5c 0** (the Update bodies are zod contracts, no class initialisers); **HC2 1** — a new `GET …/shopify/catalogue-import` typed `… | null`, Refuted by reading (an unknown store throws not-found; `null` means never imported); HC2b 20; HC6-split 38 / 38; **HC7b 0**; **HC10:** a committed `openapi.json` is now the oasdiff baseline, CI has no oasdiff, schemathesis or prism step (HC10-ci 0 lines), HC10-optionality 0; HC11c 1 — a `typeof req.url === 'string'` guard in log redaction, a grep false positive; HC13b the one multipart interceptor (5 lines). The sub-bullets below are the first copy.
  - **HC1a: 12 rows, all non-creating actions answering 201.** They are `otp/send`, `otp/verify` (its sibling `password-reset` carries `@HttpCode(200)`), three `…/delete-check` reads, two approve/reject pairs, a journal-entry `post`, a branch `test` and a `resolve`. The eval's ≈ 10 TRUE stands. Without the block filter, the same question matched 56 routes; dto-types' whole-segment rule removed the 7 substring decoys (`accounts`, `checkout`, `check-in`). **HC1b:** 3 more (`login`, `mfa/verify`, `refresh`): `@Res({ passthrough: true })` handlers whose bodies set no status. They stay Unconfirmed until V328 runs. Re-run on the full tree with dto-types' body read: the same 3, each printed `res-no-status` by the script rather than read by hand.
  - **HC2:** 0 declared nullable GET returns (hexagonal controllers). HC2b found 19 nullable use cases injected into controllers; reading those handlers is how the eval's one low row (an unknown shipment code → 200 `{data: null}`) is reached.
  - **HC3: 1 row.** A global `addContentTypeParser('*')` in the bootstrap hands every route `{}` for any content type, so no route can answer 415. The reason is written (27 webhook paths need raw bytes), and the project's `assertJsonBody()` guards the auth routes, so the row is Hardening. It flips to a finding on an all-optional PATCH that answers 200 to `text/plain`.
  - **HC4: 0.** 43 GET routes contain an unsafe word as a substring (`marketer…`); the segment rule kept all 43 quiet.
  - **HC5: 16 PUT rows.** One read to depth (`PUT settings`) replaces: omitted fields become `null`. That is B-G2's replace semantics, so it is a decoy. HC5c found 4 initialisers in Update-DTO files; each needs reading for the class it sits on (B-D13).
  - **HC6: one reference-shape store (B-D14), 84 route-level uses.** `HC6-split` gives 37 → security §4 and 37 → HC §6.
  - **HC7a: 25 lines, 0 paged API lists.** They are internal drains and sweeps (B-D4), top-N reads with no page parameter, and reporting SQL. The kernel appends an `id` tiebreak, clamps the page size and counts `total` under the same `where` (B-D9). The eval's one low row is an unpaged sibling of the kernel, capped at `ROW_CAP + 1` and sorted by one date. It is written in the kernel's own `{ field, direction }` shape, which 7a does not match: a grep for that shape matched about 230 kernel-paged decoys and was dropped. Reading the kernel's siblings finds it. **HC7b:** 1 row (a share `count`, not a page size, so a decoy).
  - **HC8: 13 bulk routes.** One use case read: per-row outcomes aligned to the input (B-G15), so it is a decoy. HC8b found 22 loops, 20 of them in jobs, which are not HC rows.
  - **HC10:** no committed spec and no CI in the first copy, so oasdiff was `NOT-RUN (no baseline)` there (the full tree has both: see above). The spec is generated at boot (`SwaggerModule.createDocument`). HC10-optionality found **1 row**: a field the spec marks optional while its `@ArrayMinSize(1)` makes the server answer 400. It matches the eval's row exactly.
  - **HC11–HC13: 0.** No Express, GraphQL or Go code; the client wrapper refuses redirects (P5: 0 callers); one multipart interceptor buffers its parts.
- **Research labs** (paired POS/NEG sample `lab-A/grepfx`, labs A/B): the POS found are the action POST `orders/search` (the `@HttpCode(200)` `login` NEG stayed quiet), `return this.svc.repo.findOne(` (HC2c), `GET :id/cancel` (HC4), `PUT` with `Partial<OrderDto>` (HC5), the unclamped `take: q.limit` with a single-key sort (HC7a and HC7b), Express 5 `/:id?`, `/*`, `/:id(\d+)` (3/3, while the v5-syntax NEGs `/*path` and `/o{/:id}` stayed quiet), and the Go `bodyclose` sample (HC12a). One noise source was removed: a first Go grep matched `x, ok := m.Get(` across a vendored toolchain, and the rule now requires `net/http` plus a response variable. The eval's `probe-fx`: 0 rows.
- **Fixtures** (`benchmarks/fixtures/*`; none seeds an HC class yet — `backend-defects` is a later build item): 2 HC1a (a `returns/:id/approve` POST at 201; an `email-templates/preview` POST), 1 HC2c (the service throws `NotFoundException` one hop down, so it is Refuted), 5 HC1d (FastAPI and Express 201s with no `Location`), 20 HC7a lines (MikroORM and Prisma lists sorted by `createdAt`/`issuedAt` alone; the `ORDER BY id` lists stayed quiet), 2 HC11d-nofp (hooks added to the root instance, so they are decoys), 15 HC12c files (each needs a read for a configurable base URL), and 4 HC8b loops in jobs. Every other § printed 0.

## The 3,000-hit path

The wiring decides most of a large run (P5). A global response interceptor that sets status, the pagination kernel, the idempotency interceptor and the HTTP-client wrapper are each **one** row with N sites. Then work through the rest in this order:
1. HC1a/HC1b, grouped by controller. Read one route per group against the spec and the project's `@HttpCode` convention.
2. HC4 and HC2b, all of them (they are few and high).
3. HC7a, grouped by file: drains and sweeps close with one cited reason (B-D4).
4. HC5, grouped by DTO base.
5. HC8, then the HC8b loops those routes reach.
6. HC12c, grouped by client wrapper.

A group may be closed with **one cited reason** (`23 HC12c callers: the wrapper at outbound-http.ts:339 sets redirect: 'manual'`) when the reason is checked, not assumed. Whatever is left prints `Live, unreviewed (k groups / n hits — /backend-audit --classes=http)`; public and money routes are read first.

## Scans for

| § | Class (research id) | Default severity | Oracle |
|---|---|---|---|
| 1 | create status, `Location`, action POST 201, 204 with a body (BA-01/02/03) | medium; low for an action 201 nobody keys on | V328 |
| 2 | missing resource → 200 `null` / empty (BA-04) | high | V329 |
| 3 | 405 + `Allow`, 415 / 406 (BA-06/07, BF-GO-04) | low; medium when a wrong type is acted on | V331 |
| 4 | unsafe GET / HEAD (BA-08) | high when business state changes | V332 |
| 5 | PUT / PATCH semantics, PATCH defaults (BA-09, BV-14, BF-DJ-01/02) | medium; high on a wipe | V333 (V342 for `null`) |
| 6 | Idempotency-Key semantics, routes outside security §4 (BA-10) | high | V334 |
| 7 | pagination correctness (BA-11, BF-DJ-04) | medium; high for exports and sync | V335 |
| 8 | batch partial failure (BA-12) | medium; high when callers retry the whole batch | V336 |
| 9 | Deprecation / Sunset (BA-13) | low | V337 |
| 10 | spec drift — tool lane (BA-15) | high | V338 |
| 11 | router and framework traps by version (BN-01/02/05/08/13/14, BN-09 body half, BF-FA-04, BF-RS-01) | blocker at boot; high for an unfiltered list; else medium | V346, V357 |
| 12 | outbound response handling (BO-04, BO-06) | medium | V354, V355 |
| 13 | multipart order and partial uploads (BU-03, BU-05) | medium | V356 |

Every lane row that rests on a framework default also carries V357: the oracle ran on the installed version, and the finding states it.

### 1. Create status, `Location`, action POST, 204 body

```
BAD:   @Post('otp/verify') verify(@Body() dto: VerifyOtpDto)          // Nest default 201 on an action
       res.status(201).json(order)  (no Location)  ·  @HttpCode(204) remove(): Promise<OrderDto>   // body silently dropped
GOOD:  @Post('otp/verify') @HttpCode(200)  ·  res.status(201).location(`/orders/${o.id}`).json(o)  ·  202 + Location of a status resource for an async create
```
**Read the code:** Is it a create (an addressable id comes back) or an action (search, login, verify, calculate, preview, approve, `delete-check`)? Does the spec document 201 for "created a search job" (then 201 is right)? Does a 201 set a `Location` that GETs 200 with the same id? For HC1b, does a passthrough handler set its own status, and does that status survive the framework's reply on the installed version? Does the project already follow a convention (a sibling route with `@HttpCode(200)`)? **Finding when** an action answers 201, a create answers 200 or omits `Location`, or a 204 handler computes a body a client is documented to receive (B-A1, B-A3). **Proof:** V328 — POST create → 201 + `Location` that GETs 200; action → 200; 204 → empty body.

### 2. Missing resource answered as success

```
BAD:   @Get(':id') one(@Param('id') id: string): Promise<OrderDto | null> { return this.getOrder.execute(id); }   // Express 200 empty, Fastify 200 "null"
GOOD:  const o = await this.getOrder.execute(id); if (!o) throw new NotFoundException();   ·   use case throws a domain NotFound mapped to 404
```
**Read the code:** Does a not-found throw below the controller (service, use case, `findOneOrFail`, a repository guard)? That case is Refuted, the research's main false positive. Is `null` a documented sub-resource absence ("no active shift")? A tenant-scoped miss must look identical to an absent row. **Finding when** an unknown id, slug or code reaches a 2xx with an empty or `null` body. **Proof:** V329 — GET a random id → 404 in the envelope, on the adapter that ships; Schemathesis `use_after_free`.

### 3. Method and media-type negotiation

```
BAD:   fastify.addContentTypeParser('*', …, (req, body, done) => done(null, {}))   // every route accepts any type as {}
       express.json() alone: an XML or text/plain body leaves req.body undefined and the route proceeds   ·   Koa router with no allowedMethods()
GOOD:  scope the catch-all parser to the webhook plugin  ·  a 415 for unsupported types  ·  router.allowedMethods()  ·  Go "POST /orders/{id}" patterns
```
**Read the code:** Does the spec document 405 / 415? A public API that answers a uniform 404 for an unknown method and path, and documents it, is not a defect (B-A9). OPTIONS advertising `Allow` while the method 404s is (Express auto-OPTIONS). Is a catch-all parser scoped to the routes that need raw bytes, and is the reason written? 406 is optional (RFC 9110 allows ignoring `Accept`). **Finding when** a wrong content type is **acted on** (a 2xx on `{}`), or the documented 405/415 never comes. **Proof:** V331 — wrong method → 405 + `Allow` where documented; `text/plain` / XML to a JSON route → 415.

### 4. Unsafe GET / HEAD

```
BAD:   @Get('orders/:id/cancel')  ·  router.get('/unsubscribe', …save…)  ·  a GET whose handler calls a command use case, queue.add or emit
GOOD:  @Post('orders/:id/cancel') @HttpCode(200)  ·  GET /unsubscribe shows a confirm page; POST performs it
```
**Read the code:** Does the handler change **business** state? An audit row, a view counter, a cache warm, lazy materialisation or an OAuth callback that must store the grant is B-A6, and is Refuted. Is the word a whole segment (B-D11)? `HEAD` auto-routes run the GET handler. A Django `path()` row (`HC4b-django`) routes every method: it is a row only when the view accepts GET — `@require_POST`, `@require_http_methods(["POST"])` or a class view with no `get` clears it. **Finding when** two identical GETs leave different business rows or effect counts. **Proof:** V332 — two GETs; the row snapshot and effect counters are unchanged.

### 5. PUT / PATCH semantics and PATCH defaults

```
BAD:   @Put(':id') put(@Body() dto: Partial<OrderDto>)  ·  Object.assign(entity, dto) under PUT  ·  class UpdateOrderDto { status: Status = Status.Draft }   // omitted → reset
       DRF: PUT on a serializer whose fields have model defaults (behaves like PATCH)  ·  partial=True forced on update()
GOOD:  PUT replaces (omitted optional → null/default, or 400)  ·  PATCH applies present keys only; no initialisers on Update DTOs  ·  a JSON Patch applied atomically
```
**Read the code:** Replace or merge — what does the spec say (B-A4: PUT documented as partial with no PATCH is naming only, low)? Does an initialiser sit on an Update/Patch DTO class or a query DTO (B-D13)? Is the patch dialect documented, and is `null` a value or a clear in it (B-A5, B-G23)? Does a failing JSON Patch `test` op leave state unchanged? **Finding when** an omitted field is wiped or reset by PATCH, a PUT merges where the spec says replace, or a JSON Patch half-applies. `null` into a NOT NULL column is `validation-boundary-scan` §5. **Proof:** V333 — PUT omitting an optional field, PATCH omitting it, a failing `test` op; V342 for `{"f": null}`.

### 6. Idempotency-Key semantics (routes outside security §4)

```
BAD:   store key = idempotencyKey  (no principal or tenant: another tenant replays this tenant's response)  ·  no body fingerprint  ·  no in-flight state (two concurrent runs)
GOOD:  key = (tenant, principal, operation, key); body hash compared; in-flight lease → 409; lapsed lease → 409 OUTCOME_UNKNOWN, never a re-run   (B-D14)
```
**Read the code:** `HC6-no-principal` / `HC6-no-fingerprint` name the header-reading files with no caller term or no hash term at all — an absence a line grep cannot print; a key composed one hop down (a store that prefixes the tenant) clears it. Take the store grep 0 found and compare it with B-D14, part by part: key composition, fingerprint, in-flight, lapsed lease, which statuses are stored (B-G8), the window (B-G5). Each missing part is its own V334 variant. Is the route in `HC6-split`'s S4 set? Then it goes to security §4, with a count. A PUT to a client-chosen id that ignores the key by documented design is B-A14. **Finding when** a replay re-executes, returns a different success (B-G6), honours a different body silently (B-G7), or hands one principal another's stored response. **Proof:** V334 (property S1) — same key + body twice, different body, N concurrent, another principal.

### 7. Pagination correctness — kernel first

```
BAD:   orderBy: { createdAt: 'desc' }, take: dto.limit, skip   // ties skip/repeat rows across pages; no clamp
       cursor = base64({ id }) while sorting by createdAt  ·  total counted without the list's filter  ·  DRF paginating Order.objects.all() (no order_by)
GOOD:  orderBy: [{ createdAt: 'desc' }, { id: 'desc' }]; take: Math.min(dto.limit ?? 20, MAX) — or every list through the kernel that does this
```
**Read the code:** Read the kernel (W0-kernel) **first**. Does it append a unique tiebreak, clamp the page size (coerce down, B-G10), allow-list sort fields and count `total` under the same filter? Then every caller is one decoy (B-D9), and only lists that **bypass** it are read. Is a 7a site a client-paged list, or an internal drain whose rows leave the filter (B-D4)? A top-N read with no page parameter is not pagination. An unpaged query cut at a cap on a non-unique key is a B-V8 variant (low), and it is found by reading the kernel's siblings. Does a token carry its filters (B-G11), stay opaque (B-G12), and is `next` absent on the last page (B-G13)? **Finding when** a client walking every page misses or repeats a pre-existing row, `limit` is unbounded, or a bad cursor 500s. **Proof:** V335 (property S3) — rows with identical sort keys, inserts between pages, `limit=10000`, a tampered cursor.

### 8. Batch partial failure

```
BAD:   for (const item of dto.items) { try { await create(item) } catch { failed++ } }  return { ok: true }   // 200 while 3 of 50 failed
GOOD:  one transaction, 4xx and zero rows on any invalid item — or 207 / 200 with results[i] aligned to the input index, documented
```
**Read the code:** All-or-nothing or per-item: which does the contract say (B-G15)? Are results aligned to the input order, duplicates inside the batch handled, the max size enforced? An async batch (202 + job) may be partial with per-item status. Loops in jobs are not HC rows. **Finding when** a mixed batch commits partially under one success status, results do not align, or "all-or-nothing" commits per item. **Proof:** V336 — `[valid, invalid, valid]`, all invalid, empty, over max, a DB failure mid-batch.

### 9. Deprecation and Sunset

```
BAD:   res.set('Deprecation', 'true')  (draft syntax)  ·  Sunset earlier than Deprecation  ·  deprecated: true in the spec, no header
GOOD:  Deprecation: @1767225600  ·  Sunset: <HTTP-date ≥ Deprecation>  ·  Link rel="deprecation" to the notice
```
**Read the code:** RFC 9745 makes `Deprecation` a structured-field date (`@<epoch>`), and RFC 8594's `Sunset` is an HTTP-date. Does middleware deprecate a whole version prefix? Is the API internal with no external consumer (low)? **Finding when** the header does not match `^@\d+$`, `Sunset` precedes `Deprecation`, or the spec and the headers disagree. **Proof:** V337.

### 10. Spec drift — the tool lane

```
BAD:   oasdiff breaking base.json rev.json            // exit 0 on a breaking change: the gate cannot fail
       @tufin/oasdiff from npm (404: no such package)  ·  links declared beside responses (0 stateful links)  ·  @ApiPropertyOptional() @ArrayMinSize(1) ids   // spec optional, server 400
GOOD:  oasdiff breaking committed.json generated.json --fail-on ERR  (pinned binary)  ·  responses."201".links  ·  decorators and validators agree
```
**Read the code:** Is the spec **generated from the code in CI** and diffed against a committed baseline with `--fail-on ERR`? Does Schemathesis see ≥ 1 link? Does an `HC10-optionality` row's validator really refuse the absent key (a local `IsAbsentOr()` is read as optional)? Is the field the spec omits dropped by a serializer (→ `wire-format-scan` §3)? **Finding when** the gate cannot fail, or the running app and the spec disagree on required/optional, enum, status or field presence. With nothing committed to diff, the row is `NOT-RUN (no baseline)`, and the fix routes to `api-snapshot`'s baseline step. **Proof:** V338 — the spec diff exits 0 **with** `--fail-on ERR`; Schemathesis clean with ≥ 1 link.

### 11. Router and framework traps, by version

```
BAD:   app.get('/u/:id?')  (Express 5: throws at boot)  ·  req.query.filter.status under the simple parser (unfiltered list)  ·  if (req.path.startsWith('/admin'))  (case-insensitive routing)
       fastify.addHook('onRequest', …request.body…)  ·  a plugin's auth hook with no fp()  ·  [Order!]! over a nullable source  ·  module-scope new DataLoader(…)  ·  axum "/:id" on 0.8
GOOD:  '/u{/:id}'  ·  app.set('query parser', 'extended') or flat keys  ·  preHandler for body reads  ·  fp(plugin)  ·  [Order]!  ·  a DataLoader per request  ·  "/{id}"
```
**Read the code:** Which major is installed (gate 3; an `UNREAD` version is Unconfirmed)? Is the Fastify hook on the root instance (no encapsulation, so a decoy) or inside a registered plugin? Under the Fastify adapter, does any `@Res()` handler, body-parser limit or `multer` import still assume Express (BN-09's body half)? Is a FastAPI dependency with side effects used twice? The auth meaning of a hook or a path compare is security's (P3). **Finding when** the installed version or adapter turns the code into a boot failure, an unfiltered list, a skipped hook or a cross-request cache. **Proof:** V346 — the same e2e requests on both sides of the pair; V357.

### 12. Outbound response handling

```
BAD:   resp, err := client.Do(req)  …no defer resp.Body.Close()  ·  requests.get(url, stream=True) outside with  ·  fetch(providerUrl, { method: 'POST', body })  (default redirect: follow)
GOOD:  defer resp.Body.Close() + io.Copy(io.Discard, resp.Body)  ·  with requests.get(…, stream=True) as r  ·  a wrapper with redirect: 'manual' / maxRedirects: 0 for POST
```
**Read the code:** Does every caller go through one wrapper (P5; read `HC12c-setting` first)? Is the base URL configurable (a provider can move it), and is success judged by 2xx alone? Does a provider document a 303? **Finding when** a body is never closed on some path, or a POST can become a GET that "succeeds". **Proof:** V354 — 2 × pool size + 1 calls, FD count stable; V355 — a stub answering 302 to POST → the client errors (307/308 keep the method).

### 13. Multipart order and partial uploads

```
BAD:   multer({ fileFilter: (req, file, cb) => cb(null, req.body.kind === 'invoice') })   // body fields after the file are not parsed yet
       for await (const part of req.parts()) { if (part.type === 'file') upload(part, fields.orderId) }   ·   completeMultipartUpload in a finally
GOOD:  read fields after the stream ends, or require (and document) field-first order with a 400  ·  check bytes received == declared before completing
```
**Read the code:** Does any decision read a field that may arrive **after** the file part? Does a buffering parser (Django, Starlette `form()`, Spring) make order irrelevant (a decoy)? Is the upload completed only after a byte-count check, with the libraries' own `truncated` checks? **Finding when** file-first and file-last give different outcomes, or an aborted upload leaves an object or a row. **Proof:** V356 — both part orders; abort at 1 %, 50 %, 99 %.

## Output

```
http-contract-scan — lanes: nestjs ^11.2.4 range (apps/api/package.json:45) on fastify · lockfile absent: version-gated rows Unconfirmed (V357)
Wiring: FastifyAdapter src/bootstrap.ts:207 · APP_INTERCEPTOR ×3 (idempotency src/app.module.ts:259) · kernel src/shared/persistence/page-query.ts:43 (tiebreak id, clamp 100, total same where) · client wrapper redirect: 'manual' (src/shared/integration/outbound-http.ts:339)
Tools: dto-types ran (3,741 files; 1,298 handlers) · oasdiff NOT-RUN (no baseline; spec generated at boot) · schemathesis NOT-RUN (no running app) · golangci-lint NOT-RUN (no Go)

Findings: 0 · Unconfirmed: 3 · Hardening: 1

1. src/auth/auth.controller.ts:568 (+ 11 routes, 6 controllers; + 3 passthrough)  [report-flagged]  low
   §1 — @Post('otp/verify') with no @HttpCode: answers 201 for a verification (sibling password-reset :581 uses @HttpCode(200)).
   Contract: RFC 9110 § 15.3.2 (201 = a resource was created) + the project's own @HttpCode(200) convention on 322 handlers.
   Fix: @HttpCode(200) on each action route. Settling: V328 through the app factory.
2. src/modules/orders/interface/dto/list-orders.query.dto.ts:279                 [report-flagged]  medium
   §10 — @ApiPropertyOptional() over @ArrayMinSize(1): the spec says optional, the server answers 400 without it.
   Fix: @ApiProperty({ minItems: 1 }) or make the field truly optional. Settling: V338 (Schemathesis positive_data_acceptance).
3. src/modules/orders/interface/shipment-code.controller.ts:131                  [report-flagged]  low
   §2 — an unknown code answers 200 {data: null} (use case typed RegistryRow | null). Fix: throw the domain NotFound. Settling: V329.
4. src/bootstrap.ts:265                                                           Hardening
   §3 — global addContentTypeParser('*') → {} for any type; reason written (webhook raw bytes). Scope it to the webhook plugin.

Verification: 0 findings · 3 unconfirmed (the first is a group of 15 routes) · 1 hardening · the rest refuted or decoys, each with its precedent (self-verified)

Class coverage:
  §1  create/action status     checked (12 HC1a + 3 HC1b → 1 unconfirmed group; 1 HC1d → B-D1)
  §2  missing → 200 null       checked (0 declared; 19 injected nullable use cases → 1 unconfirmed) · Live, unreviewed (18 injections)
  §3  405 / 415                checked (1 catch-all parser → 1 hardening; 0 allowedMethods: N/A, no Koa)
  §4  unsafe GET               checked (0 segment hits; 43 substring decoys quiet)
  §5  PUT / PATCH              checked (16 PUT rows; 1 read → replace, decoy; 4 initialisers) · Live, unreviewed (15 PUT)
  §6  idempotency key          checked (1 store = B-D14 → 0) · → security logic-race-scan §4 (37)
  §7  pagination               checked (kernel B-D9; 25 7a lines → 0 paged lists; 1 7b → decoy)
  §8  batch                    checked (13 bulk routes; 1 read → aligned results) · Live, unreviewed (12)
  §9  deprecation              checked (0)
  §10 spec drift               NOT-RUN (no baseline: oasdiff) · checked (1 optionality row → 1 unconfirmed)
  §11 framework traps          checked (0: no Express, GraphQL, Go or axum; 0 Express imports under Fastify)
  §12 outbound responses       checked (wrapper refuses redirects → 0 callers; 0 Go/Python)
  §13 multipart                checked (1 interceptor, parts buffered → 0)
```

`[report-with-fix]`: the oracle failed through the real bootstrap on the installed version, the contract source is cited, and the fix is local to the project's own primitive. `[report-flagged]`: one link is unproven (no oracle run, the version `UNREAD`, the spec absent). The row names that link and the settling request. The coverage block lists **all thirteen** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `NOT-RUN (<why>)` for a tool, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. `/backend-audit` prints a missing line as `not run`.

## False positives / precedents

The verifier reads [`precedents/backend.md`](../../../../snippets/precedents/backend.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **B-A1** 204 with no documented body · **B-A3** a create that sets `Location` · **B-A4** PUT documented as partial with no PATCH · **B-A6** a GET that writes an audit row or stores an OAuth grant · **B-A9** a documented uniform 404 · **B-A10** offset on small admin lists · **B-A14** a natural-key PUT that ignores the key · **B-A17** GraphQL 200 with `errors[]` · **B-A18** spec-linter findings.
- **B-D4** internal drains ordered by one key · **B-D9** the pagination kernel · **B-D11** a route word inside a longer segment · **B-D13** initialisers on query DTOs · **B-D14** the reference idempotency module · **B-D1** protocol endpoints (OAuth dynamic client registration answers 201 with the client in the body).
- **B-G1/B-G2** PATCH merges, PUT replaces · **B-G5–B-G8** idempotency windows, replays, mismatched bodies, what is stored · **B-G9–B-G14** pagination · **B-G15** batch · **B-G18/B-G19** breaking changes and versioning · **B-G22** async create (202) · **B-R1** a safe library default.
- **P1** cite the contract · **P3** "an attacker can…" goes to security · **P4** prove on the adapter that ships · **P5** one finding at the wrapper.

Shapes this skill must not report: an action POST with `@HttpCode(200)`; a service that throws `NotFound` one hop below a controller returning `findById`; a hook added to the root Fastify instance; a client wrapper that already refuses redirects; `ORDER BY id … LIMIT`; a `limit 1` lookup; per-row outcomes aligned to the input.

## When to run

- On any diff that touches a controller, a route decorator, a router, the adapter or its parsers, the pagination kernel, the idempotency interceptor, the HTTP-client wrapper, a multipart handler, the spec generator or the CI spec step. These are `/backend-audit`'s "a route, kernel or spec file" signals.
- On every whole-repo `/backend-audit`, reporting all thirteen §s. Before upgrading Express, Fastify, Nest, DRF, axum or Apollo across a major (V346, V357). After `/add-endpoint`, whose gate cites V328 and V329.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it. It gets part A (what the route is), part B (the version and adapter line), the contract source and the request — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/backend.md`. Under `/backend-audit` that is `@api-reviewer` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH. Standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before §2, §6, §7 or §12 when grep 0 is unread.** A verdict on a list, a key or an outbound call without its kernel, store or wrapper is invalid. When a kernel is built in a way grep 0 cannot see, read it by hand and quote it.
- **Halt on any finding missing its anchors:** the route `file:line`, the contract source (P1), the version and adapter, the request, and the fix in the project's own primitive.
- **No `[report-with-fix]` without the oracle through the project's own bootstrap** on the installed version and adapter (or a two-ended static fact). A hand-built `Fastify()` or `express()` in a test is not one (P4). An oasdiff exit 0 without `--fail-on ERR`, or Schemathesis with 0 links, is `NOT-RUN` and never PASS.
- **No proposed fix may hide the class:** never remove `--fail-on`, never `@HttpCode(201)` on an action to make a test pass, never add a catch-all content-type parser to silence a 415, never raise or drop the page-size cap to make a walk complete, never key idempotency on the raw header alone.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "the API contract looks fine"** without the coverage block. A § whose grep or script did not run is `blocked`, never `checked`.

## Related

- `/backend-audit` dispatches this skill and folds its coverage block into its HTTP ledger rows; `/backend-fix` closes findings failing-first through the real bootstrap and re-runs this detector.
- `validation-boundary-scan` (its `dto-types.py` feeds §1, §2, §4, §5 and §8), `edge-error-scan`, `wire-format-scan`, `api-snapshot` (the committed baseline and the CI gate §10 checks) and `api-consistency-audit` (this pack) are the neighbours named in § Boundaries. `endpoint-test-method` (this pack) drives the V328–V337 requests against a running app; `@api-reviewer` judges these rows.
- When those packs are installed: security `logic-race-scan` §4, `ssrf-scan` §4, `file-access-scan` §2 and `data-exposure-scan` §4; database `n-plus-one-scan` and `transaction-scan` §8; performance `request-path-scan` §12/§13; distributed-systems `retry-deadline-scan` §5; code-quality `error-handling-scan` §3/§7 and `type-safety-scan` §1; testing `contract-test`.

## Sources

Defaults tagged `[V]` were run in the backend research labs (2026-10-14): NestJS 12.1.3 on both adapters, Express 5.3, Fastify 5.12, Koa 3.2 with `@koa/router` 15, Apollo Server 5 and Mercurius 16, DRF 3.18.3 / Django 6.1.2, FastAPI 0.143, Go 1.27.2 ServeMux, golangci-lint 2.14.0, oasdiff 1.33.0 and Schemathesis 4.31.0 (the links rule and the exit-0 rule re-measured for `api-snapshot` the same day), and the fetch/axios redirect probe. `[K]` rows (Fastify encapsulation, DRF `partial=True` on PUT, axum 0.8 paths) are from vendor documentation as read by the research. `[R]` rows are the research's static signals, not run. RFC 9110 (status semantics), RFC 9745 (`Deprecation`) and RFC 8594 (`Sunset`) are cited by section, paraphrased. Nest 11 was not run. The real-repo counts come from a read-only run on 2026-10-14 (batch-5 eval § 3, re-measured here with the block above). Paraphrased; no text is reproduced beyond identifiers.
