---
name: edge-error-scan
description: "Edge errors: catch-alls that flatten status, unmapped ORM errors, wrong-adapter filters, default error paths — read-only."
kind: skill
pack: backend
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: edge-error-scan

## Premise

Every API declares one error contract — a status class per failure and one envelope — and then lets a dozen code paths answer errors without it. A global `@Catch()` that knows the project's domain errors sends the framework's own `BadRequestException` (pipe 400), `ThrottlerException` (429) and body-limit 413 to 500. The ORM's `NotFoundError` from `findOneOrFail` reaches the filter unmapped, hidden behind a **domain** class of the same name that the filter does test. A filter written against Express's `res.status().json()` runs on the Fastify adapter and turns **every** error into 500. Express 4 lets an `async` handler's rejection crash the process; a Fastify handler that sends without `return reply` answers twice; a Nest handler that injects `@Res()` and returns a value hangs. DRF answers `IntegrityError` with an HTML page, FastAPI answers an uncaught error with `text/plain`, Flask's `errorhandler(Exception)` turns 404 into 500. None of these fails a unit test: the handler is fine, the edge is wrong. This skill finds them in the wiring and proves each with the **failure-class matrix** through the project's own bootstrap. Read-only: it never edits code.

Backend owns **the wiring between the HTTP framework and the domain** (eval § 4.1): here, which status and shape the edge emits for each failure, and what the framework's default error path does. It owns `/backend-audit`'s edge-error rows (`edge-error-scan §1–§8`); `@api-reviewer` (this pack) judges them in refute mode.

**Every finding cites the mapper or throw site `<file:line>` + the wiring row it depends on (the global filter, error middleware or handler, quoted from the bootstrap, and the adapter) + the failure class and the status/content type/envelope it gets versus the contract source (P1) + the oracle that showed it, or the request that would settle it + the fix in the project's own mapper.** A grep hit is a candidate. "Errors look handled" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/backend.md`](../../../../snippets/precedents/backend.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Backend: V345 (failure-class matrix), V330 (domain and DB error mapping), V346 (version and adapter pair), V354 (outbound response handling) and V357 (the version pair rule).

## The rule

A candidate is a finding when all four hold — `precedents/backend.md` § Reading the seven gates for backend, applied to the edge.

1. **Part A holds: this is the mapper that ships, on the path the failure takes.** The filter is registered where the bootstrap registers it (`APP_FILTER` in the app module, `useGlobalFilters` in `main.ts` or a shared `configureApp`, `@UseFilters` on one controller — which then wins for that controller only), the error middleware is mounted **after** the routes, the DRF/Django/FastAPI/Spring handler is the one the settings name. A unit test that builds its own filter proves nothing about what ships (P4, B-D7).
2. **Part B holds at the installed version and adapter.** Framework, adapter and ORM versions come from the lockfile (F1); without one they are `UNREAD` and every version-gated row is Unconfirmed (V357). The adapter is the one `main.ts` (or the factory it calls) builds — Express and Fastify differ in the filter API, in the body parser's errors and in what a `null` return renders (V346).
3. **Nothing already controls it**, across files: an `instanceof HttpException` / `getStatus()` arm before the 500, `super.catch()` delegation to Nest's `BaseExceptionFilter` (which keeps a non-HttpException's `statusCode` — any one with a message on 11.2.6, only a `FastifyError` or `http-errors` shape on 12.1.3), a `findOneOrFailHandler` that throws a mapped class, an application-layer mapper that translates a domain family on every path, `express-async-errors` or a wrapper on every async handler, a recover middleware on the router.
4. **The oracle fired, or the fact is two-ended.** V345/V330 through the real bootstrap (tier U) shows the wrong status, content type or envelope, or the static fact cites both ends (tier S: the thrower or the ORM call reached by client input, and the mapper that has no arm for it — with the import that proves which class the arm tests). Without one, the row is `[report-flagged]` / Unconfirmed with the request written out.

## Boundaries

One class, one owner. A neighbour that sees the same `file:line` lists it as corroboration (`precedents/backend.md` § Owned elsewhere).
- **What the error body leaks** — a stack, SQL, a hostname, a raw `err.message`, a debug mode — → security `data-exposure-scan` §1/§2, when the security pack is installed; 404-vs-403 and enumeration by status → its §5 (B-A8). Here: the status **class**, the content type and the envelope **shape**. Without the pack the row is listed tagged `error body content (owner pack security not installed)`, never graded here (P3).
- **A swallowed error, a failure returned as success, a local catch that rewrites the status or cause** → code-quality `error-handling-scan` §1/§2/§6, and an unobserved async failure → its §4, when the code-quality pack is installed. The dedupe key is the file: a `@Catch`/`ExceptionFilter`/`@ControllerAdvice`/error-middleware/exception-handler file is EE; a `catch` inside a handler or service is code-quality's.
- **Error telemetry** — a 5xx the edge maps without capture, a handled failure that leaves no log, a lost stack → observability `error-tracking-scan` §4 and `log-signal-scan` §1/§2, when the observability pack is installed. A filter can be right here and silent there; both rows stand.
- **Outbound status never checked** (`fetch` with no `.ok`) → code-quality `error-handling-scan` §3; retry eligibility → distributed-systems `retry-deadline-scan`. §8 here owns only an upstream status handed to **our** caller as our own.
- **Upload size caps** → security `file-access-scan` §2; the proxy's HTML 413 is one row of §6's matrix, not a class.
- Same pack: **a validator that never ran** → `validation-boundary-scan` (its BV-16, a validator exception answered 500, is §6 here); **a missing resource answered 200 `null`** → `http-contract-scan` §2; **400 vs 422 drift across sibling routes** → `api-consistency-audit` #2 (B-A7).

## Adapt to the codebase — the lanes

Read the framework, adapter and ORM **with their versions** (F1) and the wiring (grep 0) first. `[V]` rows were run (§ Sources); `[K]` are vendor docs not run here; a `[K]` default makes its verdict Unconfirmed until V345 runs on the installed version.

| Lane | Where the edge mapping lives | What the default does | Decoy shape |
|---|---|---|---|
| **NestJS** (Express or Fastify adapter) | `@Catch()` classes registered by `APP_FILTER` / `useGlobalFilters` / `@UseFilters`; `BaseExceptionFilter`; `HttpAdapterHost` | no filter: `HttpException` keeps its status, a domain error → 500 `Internal server error`, a non-HttpException with `statusCode` keeps it (narrowed on 12, see gate 3); on Fastify, the adapter's own refusals (malformed or empty JSON 400, 413, 415, unknown route 404) reach **any** filter already converted to `HttpException` [V 11.2.6 and 12.1.3]; `HttpException({…}, 422)` returns the object verbatim, no `statusCode`/`message`; an Express-API filter on Fastify → 500 for every routed error; `@Res()` without `passthrough` + `return` → the request hangs [V 12.1.3, both adapters] | `reply.status(s).send()` and `reply.redirect(url, 302)` on Fastify v5 (B-D3); `@Res()` routes where every branch sends or throws (B-D2); `reply.send` with no `return` inside a Nest controller or filter (B-D8) |
| **Express 4 / 5** | 4-arity `app.use((err, req, res, next) => …)` after the routes; a JSON 404 `app.use((req, res) => …)` | default error and 404 pages are **HTML**; Express 4: an `async` handler's rejection crashes Node 22; Express 5: it reaches the error handler (HTML 500 by default), `res.send(404)` sends **200** with body `404`, `res.status('201')` throws, and with no parser `req.body` is undefined → destructuring 500 [V 4.21 / 5.3.0] | `express-async-errors` imported once at boot; handlers wrapped in `try/catch` + `next(e)` (B-A15) |
| **Fastify 5** (plain) | `setErrorHandler` (per encapsulation scope), `setNotFoundHandler` | an `async` handler that `reply.send()`s and also returns → `FST_ERR_REP_ALREADY_SENT`, first answer wins; a send inside `setTimeout` → **200 empty** first; returning `undefined` → 200 empty; a thrown object literal → 500 with that object [V 5.12.7] | `return reply.send(…)` or `reply.send(…); return reply` (both correct); `reply.hijack()` streams |
| **Koa 3** | the first `app.use` wrapping `try { await next() } catch` | an un-awaited `next()` → async routes answer **404**; a `ctx.body` still unset when the chain returns → 404; `ctx.body = null` → 204 [V 3.2.1] | `return next()` |
| **tRPC 11** | `initTRPC.create({ errorFormatter })` | a plain `Error` → 500 with the raw message; `TRPCError({ code })` → its status; a batch with mixed outcomes → 207 [V 11.19.0] | — |
| **GraphQL** (Apollo 5, Mercurius 16) | `formatError` / `errorFormatter` | resolver errors → 200 + `errors[]` (the GraphQL-over-HTTP norm, B-A17); bad variables and validation errors → 400 [V Apollo 5.5.1, Mercurius 16.12.0] | 200 with `errors[]` and a mapped `extensions.code` |
| **Django REST Framework** | `REST_FRAMEWORK['EXCEPTION_HANDLER']` | `IntegrityError`, Django `ValidationError` (from `full_clean`), `DoesNotExist`, `KeyError` → **HTML 500**: the handler returns `None` for non-`APIException`; `Http404` and `PermissionDenied` are translated [V 3.18.3 / Django 6.1.2] | a custom handler that maps the DB classes before delegating |
| **FastAPI / Starlette** | `@app.exception_handler(Exception \| RequestValidationError \| StarletteHTTPException)` | unhandled → **`text/plain` 500**; malformed JSON and `text/plain` bodies → 422 [V 0.143.0 / 1.8.0] | a project that documents 422 |
| **Flask 3** | `@app.errorhandler(HTTPException)` + `errorhandler(Exception)` | every default error page is HTML; `errorhandler(Exception)` alone turns `abort(404)`, unknown routes and 405 into **500** [V 3.1.3] | an `isinstance(e, HTTPException)` passthrough first |
| **Spring Boot** | `@RestControllerAdvice` (+ `ResponseEntityExceptionHandler`), `spring.mvc.problemdetails.enabled` | `@ExceptionHandler(Exception.class)` catches `ResponseStatusException` and the MVC exceptions unless more specific handlers exist; without advice, Boot's `/error` JSON [K; Boot 4 defaults K?] | — |
| **ASP.NET Core** | `AddProblemDetails` + `UseExceptionHandler` / `IExceptionHandler`; `InvalidModelStateResponseFactory` | `[ApiController]` answers its own 400 `ValidationProblemDetails` before the action — outside a custom envelope [K] | — |
| **Rails / Laravel** | `rescue_from` + `config.exceptions_app`; `bootstrap/app.php` `->withExceptions()` | `RecordNotFound` → 404 in production, `RecordNotUnique` → 500 unless rescued [K]; a `render(fn (Throwable $e) => …)` with one status flattens all; `shouldRenderJsonWhen` must cover `api/*` [K] | — |
| **Go** (net/http, gin 1.12, echo 4) | recover middleware; gin `Default()` vs `New()`; echo `HTTPErrorHandler` | `http.Error` does not stop the handler: a write after it appends to the body (`superfluous WriteHeader`); `gin.New()` has no recovery — the panic propagates; gin `c.Bind` writes 400 before the handler (a later `c.JSON(422)` keeps 400); echo plain error → 500 `{"message":"Internal Server Error"}` [V go1.27.2, gin v1.12.0, echo v4.16.0]; net/http panic → connection aborted [K] | `ShouldBind*`; a `return` after every `http.Error` |
| **Rust** (axum 0.8, actix 4) | custom rejection (`WithRejection`); `CatchPanicLayer`; `impl ResponseError` | `Json` rejections answer 415/400/422 in plain text; a panic without `CatchPanicLayer` aborts the connection; `ResponseError` defaults to 500 [K] | — |

**ORM and DB error classes the mapping must name (§2).** Read the class names from the installed package (F1) before asserting; the column is what reaches the edge when nothing maps it.

| ORM | Not found | Unique / FK / NOT NULL / CHECK | Concurrency | What decides it |
|---|---|---|---|---|
| MikroORM 6 | `NotFoundError` from `em.findOneOrFail` / `repo.findOneOrFail`, unless `findOneOrFailHandler` is set | `UniqueConstraintViolationException`, `ForeignKeyConstraintViolationException`, `NotNullConstraintViolationException`, `CheckConstraintViolationException` | `OptimisticLockError` | the import in the filter: `@mikro-orm/core`, never a local `./errors` of the same name |
| TypeORM | `EntityNotFoundError` (`findOneOrFail`, `findOneByOrFail`) | `QueryFailedError` with `driverError.code` `23505` / `23503` / `ER_DUP_ENTRY` | `OptimisticLockVersionMismatchError` | the code read off `driverError` |
| Prisma | `P2025` (`findUniqueOrThrow`, `update` on a missing row) | `P2002` / `P2003` on `PrismaClientKnownRequestError` | — | `err.code`, not `instanceof` alone |
| Sequelize | `EmptyResultError` (`rejectOnEmpty`) | `UniqueConstraintError`, `ForeignKeyConstraintError` | `OptimisticLockError` | — |
| Drizzle / Knex / pg | — (an empty array) | the driver's SQLSTATE: `23505`, `23503`, `23502`, `23514` | — | `err.code` on the driver error |
| Mongoose | `DocumentNotFoundError` (`orFail`) | `MongoServerError` code `11000` (`E11000`) | `VersionError` | — |
| Django / SQLAlchemy | `DoesNotExist` / `NoResultFound` (`.get()`, `.one()`, `scalar_one()`) | `IntegrityError` | — | the DRF/FastAPI handler, not the view |
| JPA / Hibernate | `EntityNotFoundException`, `EmptyResultDataAccessException` | `DataIntegrityViolationException` | `OptimisticLockingFailureException` | the advice |
| ActiveRecord / Eloquent | `RecordNotFound` / `ModelNotFoundException` (404 by default in production [K]) | `RecordNotUnique`, `InvalidForeignKey` / `QueryException` SQLSTATE 23000 | `StaleObjectError` | `rescue_from` / `withExceptions` |
| GORM / EF Core | `ErrRecordNotFound` (returned, mapped in the handler) / — | `ErrDuplicatedKey` (only with `TranslateError: true`) / `DbUpdateException` | — / `DbUpdateConcurrencyException` | `errors.Is` in the handler; the exception handler |

## Tool lane and ledger

Each tool prints `ran` / `blocked (<why>)` / `NOT-RUN (<why>)` in the output header.

| Tool | Command | Covers | Limits |
|---|---|---|---|
| **The failure-class matrix** (V345) | the real-bootstrap harness of `proof-oracles.md` § Backend — one request per failure class through the app the project's factory builds, plus one healthy request after | §1, §3–§7 at runtime; §2 with the ORM rows of V330 | needs the e2e harness or the app factory and a scratch database in a container; `NOT-RUN` without them, never PASS |
| Captured logs | the e2e run with the logger captured (a pino test stream, `caplog`, a log recorder); fail on `FST_ERR_REP_ALREADY_SENT`, `ERR_HTTP_HEADERS_SENT`, `superfluous response.WriteHeader`, `unhandledRejection` | §4, §5 | sees only the routes the suite drives |
| semgrep rule `go-http-error-without-return` (two patterns: `http.Error(…)` not followed by `return`, and an `if` whose block ends in `http.Error` with no `return`) | `semgrep --metrics=off --config <rule>.yml <roots>` | §5 Go lane | research lab B, semgrep 1.180.0: 6 TP, 0 FP on paired samples [V]; golangci-lint 2.14 (bodyclose, errcheck, staticcheck, …) and `go vet` did **not** flag it [V] |
| RuboCop `Rails/SaveBang` | `rubocop --only Rails/SaveBang app/controllers` | §5 Rails lane | disabled by default; `if @x.update(…)` is correct [K docs] |

## Pre-flight greps

Run as **one** script from the repo root (shell state does not survive between tool calls; bash 3.2-safe). Grep **N** feeds detector **§N**; F1 and grep 0 are the gates every § reads first. Every `rg` names its path — `.` or `"${ROOTS[@]}"`: given no path, `rg` reads stdin under an agent's shell and reports a silent zero. Include globs come **first**, exclusions last. With an explicit root, globs match relative to it, so exclusions start with `**/`. Any `rg` exit 2 is a failed grep, never zero hits. A block question ("this filter has no HttpException arm") is answered at the **file** or with a bounded `-U` pattern, never by `-A<n> | rg -v` (a per-line negation cannot prove an absence: rg-context-negation).

```bash
ROOTS=(.)   # server code; in a monorepo name the apps: ROOTS=(apps/api apps/admin). Manifests always search .
SCAN="${SCAN:-$(mktemp -d "${TMPDIR:-/tmp}/ee.XXXXXX")}"; mkdir -p "$SCAN"
CODE=(-g '*.{ts,mts,cts,js,mjs,cjs,py,java,kt,cs,go,php,rb,rs}')
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,target,coverage,.next,.venv,venv,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata}/**'
   -g '!**/*.{spec,test,e2e-spec,stories}.*' -g '!**/test_*.py' -g '!**/*_test.go' -g '!**/*.d.ts' -g '!**/*.min.*'
   -g '!**/{migrations,migration,db/migrate,seeders,seeds}/**' -g '!**/{locales,locale,i18n,translations}/**'
   -g '!**/{openapi,swagger}*.{json,yaml,yml}' -g '!**/{docs,ai,.claude}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#(?!\[))')   # drops comment-only lines
# F1 framework, adapter, ORM and error-library versions — ranges from manifests; exact versions from the lockfile (gate 3; V357)
rg -n --no-heading --pcre2 '"(@nestjs/(?:core|platform-fastify|platform-express|graphql)|express|fastify|koa|@trpc/server|@apollo/server|mercurius|express-async-errors|@mikro-orm/core|typeorm|@prisma/client|sequelize|drizzle-orm|knex|mongoose)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '"node_modules/(?:@nestjs/core|@nestjs/platform-fastify|@nestjs/platform-express|express|fastify|koa|@trpc/server|@apollo/server|mercurius|@mikro-orm/core|typeorm|@prisma/client|sequelize|mongoose)":\s*\{|^\s*["\x27]?/?(?:@nestjs/core|@nestjs/platform-fastify|@nestjs/platform-express|express|fastify|koa|@trpc/server|@apollo/server|mercurius|@mikro-orm/core|typeorm|@prisma/client|sequelize|mongoose)@\d[\w.-]*' -g '**/{package-lock.json,pnpm-lock.yaml,yarn.lock}' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(django|djangorestframework|fastapi|starlette|flask|sqlalchemy)\b\s*[=<>~!^]|\bspring-boot-starter-web\b|github\.com/(?:gin-gonic/gin|labstack/echo/v4|go-chi/chi/v5|gorilla/mux)\s+v|gorm\.io/gorm\s+v|^\s*(?:axum|actix-web|tower-http)\s*=|gem\s+["\x27](?:rails|activerecord)["\x27]|"laravel/framework"\s*:|<PackageReference Include="Microsoft\.(?:AspNetCore|EntityFrameworkCore)[\w.]*"' -g '**/{pyproject.toml,requirements*.txt,Pipfile,pom.xml,build.gradle*,go.mod,Cargo.toml,Gemfile,composer.json,*.csproj}' -g '!**/node_modules/**' .
# 0 THE WIRING — every edge mapper (filters, error middleware, handlers, advice, recover layers) and the adapter. Every § reads this first (P5)
W='@Catch\s*\(|\bAPP_FILTER\b|\buseGlobalFilters\s*\(|@UseFilters\s*\(|\bextends\s+BaseExceptionFilter\b|\bimplements\s+(?:Rpc|Ws|Gql)?ExceptionFilter\b|\bnew\s+(?:FastifyAdapter|ExpressAdapter)\s*\(|\bsetErrorHandler\s*\(|\bsetNotFoundHandler\s*\(|\berrorFormatter\b|\bformatError\b|\bEXCEPTION_HANDLER\b|\b(?:add_)?exception_handler\s*\(|\berrorhandler\s*\(|\bregister_error_handler\s*\(|\brescue_from\b|\bexceptions_app\b|\bwithExceptions\s*\(|@(?:RestControllerAdvice|ControllerAdvice|ExceptionHandler)\b|\bproblemdetails\b|\bAddProblemDetails\s*\(|\bUseExceptionHandler\s*\(|\bIExceptionHandler\b|\bInvalidModelStateResponseFactory\b|\bgin\.(?:New|Default)\s*\(\s*\)|\bHTTPErrorHandler\b|\bmiddleware\.Recover(?:er)?\b|\bCatchPanicLayer\b|\bimpl\s+ResponseError\s+for\b'
E4='\(\s*(?:err|error|e)\b[^,()]*,\s*req\w*\b[^,()]*,\s*res\w*\b[^,()]*,\s*next\b[^()]*\)\s*(?:=>|\{|:)'   # Express 4-arity error middleware
rg -n --no-heading --pcre2 "$W|$E4" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 'spring\.mvc\.problemdetails\.enabled|server\.error\.\w+' -g '**/application*.{yml,yaml,properties}' -g '!**/node_modules/**' .
rg -l --null --pcre2 "@Catch\s*\(|\bsetErrorHandler\s*\(|$E4|\berrorhandler\s*\(|\bregister_error_handler\s*\(|\bexception_handler\s*\(|@ExceptionHandler\b|\brescue_from\b|\bwithExceptions\s*\(|\bdef\s+\w*exception_handler\s*\(|\bIExceptionHandler\b|\bHTTPErrorHandler\b|\berrorFormatter\b|\bformatError\b" "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" > "$SCAN/mappers"
echo "mapper files: $(tr -cd '\0' < "$SCAN/mappers" | wc -c | tr -d ' ')"
# 1 catch-alls (1a: read every one WHOLE) · 1b: files that never preserve a framework status · 1c: Nest catch-alls that never read a non-HttpException statusCode
CA='@Catch\s*\(\s*\)|'"$E4"'|\berrorhandler\s*\(\s*Exception\s*\)|\bregister_error_handler\s*\(\s*Exception\b|\bexception_handler\s*\(\s*Exception\s*\)|@ExceptionHandler\s*\(\s*\{?\s*(?:Exception|Throwable|RuntimeException)\.class|\brender\s*\(\s*(?:function|fn)\s*\(\s*\\?(?:Throwable|Exception)\b|\brescue_from\s+(?:StandardError|Exception)\b|\bsetErrorHandler\s*\('
KEEP='\binstanceof\s+HttpException\b|\.getStatus\s*\(|\bsuper\.catch\s*\(|\bisinstance\s*\(\s*\w+\s*,\s*\(?\s*(?:HTTPException|APIException|HttpException)\b|\b(?:err|error|e|ex|exc|exception)\.(?:status|statusCode|status_code)\b|\bResponseStatusException\b|\bgetStatusCode\s*\(|\bisHttpError\b'
xargs -0 -r rg -H -n --no-heading --pcre2 "$CA" < "$SCAN/mappers" | "${NC[@]}"
xargs -0 -r rg -l --null --pcre2 "$CA" < "$SCAN/mappers" > "$SCAN/ca"
echo "1b catch-alls with no status-preserving branch:"; xargs -0 -r rg --files-without-match --pcre2 "$KEEP" < "$SCAN/ca"
echo "1c Nest catch-alls that never read a non-HttpException statusCode:"; xargs -0 -r rg -l --null --pcre2 '@Catch\s*\(\s*\)' < "$SCAN/ca" | xargs -0 -r rg --files-without-match --pcre2 '\.statusCode\b|\bisHttpError\b|\bsuper\.catch\s*\('
# 2a per ORM present: each lane class → the mapper that names it and the MODULE it is imported from (a same-named domain class hides the gap)
ORMS='mikro-orm|"@mikro-orm/core"|NotFoundError UniqueConstraintViolationException ForeignKeyConstraintViolationException NotNullConstraintViolationException CheckConstraintViolationException OptimisticLockError|@mikro-orm/
typeorm|"typeorm"|QueryFailedError EntityNotFoundError|^typeorm
prisma|"@prisma/client"|PrismaClientKnownRequestError P2002 P2003 P2025|@prisma/|prisma
sequelize|"sequelize"|UniqueConstraintError ForeignKeyConstraintError EmptyResultError|^sequelize
mongoose|"mongoose"|MongoServerError E11000 DocumentNotFoundError|mongo
django|^\s*["\x27]?django\b|IntegrityError ObjectDoesNotExist|^django
sqlalchemy|^\s*["\x27]?sqlalchemy\b|IntegrityError NoResultFound|^sqlalchemy
gorm|gorm\.io/gorm|ErrRecordNotFound ErrDuplicatedKey|gorm
jpa|spring-boot-starter-data-jpa|DataIntegrityViolationException EntityNotFoundException EmptyResultDataAccessException|springframework|persistence
activerecord|gem\s+["\x27]rails["\x27]|RecordNotFound RecordNotUnique InvalidForeignKey|ActiveRecord
eloquent|"laravel/framework"|ModelNotFoundException QueryException|Illuminate
efcore|Microsoft\.EntityFrameworkCore|DbUpdateException DbUpdateConcurrencyException|EntityFrameworkCore'
: > "$SCAN/ormnames"
printf '%s\n' "$ORMS" | while IFS='|' read -r orm pkg names mod; do
  rg -q --pcre2 "$pkg" -g '**/{package.json,pyproject.toml,requirements*.txt,Pipfile,go.mod,pom.xml,build.gradle*,Gemfile,composer.json,*.csproj}' -g '!**/node_modules/**' . || continue
  for n in $names; do echo "$n" >> "$SCAN/ormnames"
    f=$(xargs -0 -r rg -l --pcre2 "\\b$n\\b" < "$SCAN/mappers" | tr '\n' ' ')
    if [ -z "$f" ]; then echo "EE2 $orm $n: named by NO mapper"; continue; fi
    for g in $f; do
      m=$(rg -U -o --no-filename --pcre2 "import\\s+(?:type\\s+)?\\{[^}]*\\b$n\\b[^}]*\\}\\s*from\\s*[\"\\x27]([^\"\\x27]+)|^from\\s+([\\w.]+)\\s+import\\s+[^\\n]*\\b$n\\b|^import\\s+([\\w.]+)\\.$n\\s*;" -r '$1$2$3' "$g" | head -1)
      case "$m" in "") v="UNRESOLVED — read the file" ;; *) if printf '%s' "$m" | grep -Eq -- "$mod"; then v="$m"; else v="$m ≠ the ORM's package: a SAME-NAMED class — the ORM's $n is UNMAPPED here"; fi ;; esac
      echo "EE2 $orm $n: $g (imported from: $v)"
    done
  done
done
rg -n --no-heading --pcre2 '\bfindOneOrFailHandler\b|\bfindExactlyOneOrFailHandler\b|\brejectOnEmpty\b|\bTranslateError\s*:\s*true\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
echo "2b not-found throwers per file (sites):"   # the call sites a client id reaches
rg -c --no-heading --pcre2 '\.(?:findOneOrFail|findOrFail|findOneByOrFail|findOneOrThrow|findUniqueOrThrow|findFirstOrThrow|firstOrFail|findByPkOrFail|getOrFail|sole)\s*\(|::findOrFail\s*\(|\.objects\.get\s*\(|\.getReferenceById\s*\(|\b(?:find|find_by)!\s*\(|\.scalar_one\s*\(\s*\)|\.one\s*\(\s*\)' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}"
# 2c error classes (TS/JS, Python) whose whole parent chain no mapper names (instanceof / @Catch / isinstance / @ExceptionHandler / rescue_from / except / [X.name])
{ rg -o --no-filename --no-heading --pcre2 '\bclass\s+(\w+)\s+extends\s+(?:\w+\.)?(\w+)' -r '$1 $2' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}"
  rg -o --no-filename --no-heading --pcre2 '^\s*class\s+(\w+)\s*\(\s*(?:\w+\.)*(\w+)' -r '$1 $2' -g '*.py' "${X[@]}" "${ROOTS[@]}"; } | sort -u > "$SCAN/classes"
xargs -0 -r rg -o --no-filename --pcre2 '\binstanceof\s+(\w+)|@Catch\s*\(\s*(\w+)|\bisinstance\s*\(\s*\w+\s*,\s*\(?\s*(\w+)|@ExceptionHandler\s*\(\s*\{?\s*(\w+)|\brescue_from\s+(\w+)|\bexcept\s+\(?\s*(\w+)|\bexception_handler\s*\(\s*(\w+)|\berrorhandler\s*\(\s*(\w+)|\[\s*(\w+)\.name\s*\]' -r '$1$2$3$4$5$6$7$8$9' < "$SCAN/mappers" | sort -u > "$SCAN/mapped"
rg -q --pcre2 '\b(?:from|import)\s+rest_framework\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" && printf '%s\n' APIException ParseError AuthenticationFailed NotAuthenticated PermissionDenied NotFound MethodNotAllowed NotAcceptable UnsupportedMediaType Throttled Http404 >> "$SCAN/mapped"   # DRF's default handler maps these inside DRF views (a plain Django view still answers 500)
awk 'NR==FNR {m[$1]=1; next} {p[$1]=$2} END {
  root="^(Error|Exception|BaseException|TypeError|RangeError)$"
  for (c in p) { x=c; d=0; ok=0; err=0; top=c
    while (x!="" && d<15) { if (x ~ root) {err=1; break}
      if (x in m) ok=1
      if (x ~ /^(BadRequest|Unauthorized|NotFound|Forbidden|NotAcceptable|RequestTimeout|Conflict|Gone|PayloadTooLarge|UnsupportedMediaType|UnprocessableEntity|InternalServerError|NotImplemented|BadGateway|ServiceUnavailable|GatewayTimeout|PreconditionFailed|MethodNotAllowed)Exception$/ && ("HttpException" in m)) ok=1
      if (!(x in p)) { if (x ~ /(Error|Exception)$/) err=1; break }
      top=x; x=p[x]; d++ }
    if (err) { n++; if (!ok) { u[top]++; if (length(ex[top]) < 120) ex[top]=ex[top] " " c } } }
  print "EE2c error classes:", n+0
  for (t in u) print "EE2c family named by NO mapper:", t, "(" u[t] " classes):" ex[t] }' "$SCAN/mapped" "$SCAN/classes" | sort
awk 'NR==FNR {o[$1]=1; next} ($1 in o) {print "EE2 name collision: project class", $1, "extends", $2, "— same name as an error class of the ORM in use"}' "$SCAN/ormnames" "$SCAN/classes"
# 3 under Fastify only: Express-only reply calls in filters, interceptors and middleware (3a, chained calls included); express-typed
#   responses and platform-express interceptors (3b). `.status(` and `.redirect(url, code)` are valid FastifyReply calls (B-D3): never listed
FA=$(rg -l --pcre2 '\bnew\s+FastifyAdapter\b|\bNestFastifyApplication\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' '); echo "3 Fastify adapter files: $FA (0 → §3 N/A)"
if [ "$FA" -gt 0 ]; then
rg -l --null --pcre2 '@Catch\s*\(|\bimplements\s+(?:NestInterceptor|NestMiddleware|ExceptionFilter)\b|\bHttpAdapterHost\b' -g '*.ts' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\b(?:res|response|reply)\b(?:\s*\.\s*\w+\s*\([^()\n]*\))*\s*\.\s*(?:json|sendStatus|set|setHeader|locals|render|attachment|sendFile|download|cookie)\s*\(|getResponse\s*<\s*(?:express\.)?Response\s*>' | "${NC[@]}"
rg -n --no-heading --pcre2 'import\s+(?:type\s+)?\{[^}]*\bResponse\b[^}]*\}\s+from\s+["\x27]express["\x27]|from\s+["\x27]@nestjs/platform-express["\x27]' -g '*.ts' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
fi
# 4 errors that escape the framework: Express async handlers (4a — a finding only on express ^4 with no wrapper, F1) and wrappers (4b);
#   Koa next() not awaited (4c); Go routers vs recover layers (4d); axum routers vs CatchPanicLayer (4e); gin.New (4f)
echo "4a express async handlers: $(rg -c --no-heading --pcre2 '\.(?:get|post|put|patch|delete|all|use)\s*\([^\n]*\basync\s*(?:function\s*)?\(\s*req\b' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') · 4b wrappers: $(rg -l --pcre2 'express-async-errors|express-async-handler|\basyncHandler\s*\(|\bcatchAsync\s*\(' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
rg -l --null --pcre2 '\(\s*ctx\w*\s*(?::\s*\w+)?\s*,\s*next\b' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '(?:^\s*|[{;]\s*)next\s*\(\s*\)\s*(?:;|$)' | "${NC[@]}"
echo "4d go routers: $(rg -l --pcre2 '\bhttp\.NewServeMux\s*\(|\bchi\.NewRouter\s*\(|\bmux\.NewRouter\s*\(|\becho\.New\s*\(|\bgin\.(?:New|Default)\s*\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') · recover layers: $(rg -l --pcre2 '\brecover\s*\(\s*\)|\bmiddleware\.Recover(?:er)?\b|\bgin\.(?:Recovery\w*|Default)\s*\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') · 4e axum routers: $(rg -l --pcre2 '\bRouter::new\s*\(' -g '*.rs' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') · CatchPanicLayer: $(rg -l --pcre2 '\bCatchPanicLayer\b' -g '*.rs' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
rg -n --no-heading --pcre2 '\bgin\.New\s*\(\s*\)' -g '*.go' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 5 reply lifecycle: raw Fastify sends with no return (5a — never inside a Nest controller or filter, B-D8); a send inside a timer or .then (5b);
#   @Res() with no passthrough in a method that returns a value (5c, bounded by the next route decorator); Express status as body (5d);
#   Go http.Error not followed by return (5e); Rails save/update as a bare statement (5f)
rg -l --null --pcre2 '\bFastifyReply\b|\bFastifyInstance\b|from\s+["\x27]fastify["\x27]|require\(\s*["\x27]fastify["\x27]\s*\)|\bfastify\.(?:get|post|put|patch|delete|route|register|addHook)\s*\(' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg --files-without-match --null --pcre2 '@(?:Controller|Catch|Injectable)\s*\(' | xargs -0 -r rg -H -n --no-heading -U --pcre2 '(?:^[ \t]+|[{;][ \t]*)(?:void\s+)?reply\b[^\n;]*?\.send\s*\((?:[^()\n]|\((?:[^()\n]|\([^()\n]*\))*\))*\)[ \t]*;?+(?![ \t]*\n?[ \t]*return\s+reply\b)' | "${NC[@]}"
rg -n --no-heading --pcre2 '(?:setTimeout|setImmediate|\.then)\s*\([^\n]*\b(?:reply|res)\.send\s*\(' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '@Res\(\s*\)[^\n]*?\{[^\n]*?\breturn\s+(?!(?:res|reply|response)\b|void\b|;|undefined\b)[^\n;]+|@Res\(\s*\)[^\n]*\n(?:(?![ \t]*@(?:Get|Post|Put|Patch|Delete|All|Head|Options)\b|\}|(?:export\s+)?(?:async\s+)?(?:function|const|class)\b)[^\n]*\n){0,80}?[ \t]+\Kreturn\s+(?!(?:res|reply|response)\b|this\.\w+\(\s*(?:res|reply|response)\b|void\b|;|undefined\b)[^\n;]+' -g '*.ts' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bres\.send\s*\(\s*\d{3}\s*\)|\bres\.status\s*\(\s*["\x27]\d{3}' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\bhttp\.Error\s*\([^\n]*\)[ \t]*\n(?:[ \t]*//[^\n]*\n)*(?:[ \t]*\}[ \t]*\n)?[ \t]+\K(?!\}|return\b|//|break\b|continue\b|panic\b)\S[^\n]*' -g '*.go' "${X[@]}" "${ROOTS[@]}"
rg -n --no-heading --pcre2 '^\s+@?\w+(?:\.\w+)*\.(?:save|update)(?:\s*\([^)\n]*\))?\s*$' -g '**/app/controllers/**/*.rb' "${X[@]}" "${ROOTS[@]}"
# 6 framework default error paths — the static inputs of the V345 matrix, one line per lane present
rg -l --pcre2 '\bFastAPI\s*\(' -g '*.py' "${X[@]}" "${ROOTS[@]}" | head -1 | grep -q . && echo "6 fastapi: handlers Exception=$(rg -l --pcre2 'exception_handler\s*\(\s*Exception\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') RequestValidationError=$(rg -l --pcre2 'exception_handler\s*\(\s*RequestValidationError\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') HTTPException=$(rg -l --pcre2 'exception_handler\s*\(\s*(?:Starlette)?HTTPException\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
rg -l --pcre2 'rest_framework' -g '*.py' "${X[@]}" "${ROOTS[@]}" | head -1 | grep -q . && echo "6 drf: EXCEPTION_HANDLER=$(rg -l --pcre2 '["\x27]EXCEPTION_HANDLER["\x27]' -g '*.py' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') (absent: IntegrityError, DoesNotExist and model ValidationError answer HTML 500)"
rg -l --pcre2 '\bFlask\s*\(' -g '*.py' "${X[@]}" "${ROOTS[@]}" | head -1 | grep -q . && echo "6 flask: errorhandler(HTTPException)=$(rg -l --pcre2 '(?:errorhandler|register_error_handler)\s*\(\s*(?:werkzeug\.exceptions\.)?HTTPException\b' -g '*.py' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
rg -l --pcre2 '\[ApiController\]' -g '*.cs' "${X[@]}" "${ROOTS[@]}" | head -1 | grep -q . && echo "6 aspnet: InvalidModelStateResponseFactory=$(rg -l --pcre2 'InvalidModelStateResponseFactory' -g '*.cs' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') AddProblemDetails=$(rg -l --pcre2 'AddProblemDetails\s*\(' -g '*.cs' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') UseExceptionHandler=$(rg -l --pcre2 'UseExceptionHandler\s*\(' -g '*.cs' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
rg -l --pcre2 '@(?:RestController|Controller)\b' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | head -1 | grep -q . && echo "6 spring: advice=$(rg -l --pcre2 '@(?:RestControllerAdvice|ControllerAdvice)\b' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') ResponseEntityExceptionHandler=$(rg -l --pcre2 '\bResponseEntityExceptionHandler\b' -g '*.{java,kt}' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
rg -n --no-heading --pcre2 '\.(?:Bind|BindJSON|BindQuery|BindUri)\s*\(' -g '*.go' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bfrom\s+["\x27]express["\x27]|require\(\s*["\x27]express["\x27]\s*\)' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | head -1 | grep -q . && echo "6 express: body destructures=$(rg -c --no-heading --pcre2 '\bconst\s*\{[^}]*\}\s*=\s*req\.body\b' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') json-parser=$(rg -l --pcre2 '\bexpress\.json\s*\(|\bbodyParser\.json\s*\(' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') 404-handler=$(rg -l --pcre2 '\b(?:app|router)\.use\s*\(\s*(?:async\s*)?\(\s*req\w*\s*(?::\s*\w+)?\s*,\s*res\w*[^,)]*\)\s*=>' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') schema.parse(req.*)=$(rg -c --no-heading --pcre2 '\.parse\s*\(\s*req\.(?:body|query|params)\b' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | awk -F: '{s+=$NF} END {print s+0}') ZodError-in-mapper=$(xargs -0 -r rg -l --pcre2 '\bZodError\b|\bValidationError\b' < "$SCAN/mappers" | wc -l | tr -d ' ')"
# 7 throwers that break the envelope: an object body to an HttpException, a thrown string or object literal (7a); tRPC plain Error (7b); formatters (7c)
rg -n --no-heading --pcre2 '\bthrow\s+new\s+\w*Exception\s*\(\s*\{|\bthrow\s+["\x27`]|\bthrow\s+\{' -g '*.{ts,mts,cts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | awk '{print} END {print "7a throwers:", NR}' | tail -40
rg -l --null --pcre2 '@trpc/server' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | xargs -0 -r rg -H -n --no-heading --pcre2 '\bthrow\s+new\s+Error\s*\(' | "${NC[@]}"
echo "7c graphql/trpc servers: $(rg -l --pcre2 '@trpc/server|@apollo/server|\bmercurius\b|GraphQLModule\.forRoot' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ') · formatters: $(rg -l --pcre2 '\berrorFormatter\b|\bformatError\b' -g '*.{ts,js,mjs,cjs}' "${X[@]}" "${ROOTS[@]}" | wc -l | tr -d ' ')"
# 8 an upstream status handed to our caller as our own
rg -n --no-heading --pcre2 '\.status\s*\(\s*(?:\w+\.)*(?:err|e|error|ex)\.response\.status\b|\.status\s*\(\s*(?:\w+\.)*response\.status(?:Code)?\s*\)|\bnew\s+HttpException\s*\([^\n]*,\s*(?:\w+\.)*(?:response|res)\.status(?:Code)?\b|HTTPException\s*\(\s*status_code\s*=\s*\w+(?:\.response)?\.status_code\b|\bw\.WriteHeader\s*\(\s*\w+\.StatusCode\s*\)|\bc\.(?:Status|JSON|AbortWithStatus\w*)\s*\(\s*\w+\.StatusCode\b|\babort\s*\(\s*\w+\.status_code\b' "${CODE[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

Three blind spots are structural; work around them rather than trust a quiet grep. **A mapper built in a function grep 0 cannot see** (a factory that returns the filter, a plugin that registers `setErrorHandler`) — read the bootstrap by hand and quote it. **An application-layer mapper** (a module's `toHttpError(err)`, a refusal mapper called in every use case) maps a family the global filter never names: 2c lists the family; a read decides whether every path calls the mapper. **A send whose arguments span lines** is not matched by 5a; read 5a's file list.

### Measured (2026-10-14)

- **Real repo, read-only, full tree** (a NestJS 11 monorepo on Fastify 5 with MikroORM 6.6, 3,722 `.ts` files under the API's `src`, `ROOTS=(apps/api/src)`; the pnpm lockfile, `.github/` and the workspace contracts package present): the block runs in about 1.5 s and prints 72 lines (60 before the lockfile line), 0 `rg` errors, 0 files written into the tree. **F1 reads the pnpm lockfile** (the reader `validation-boundary-scan` uses, pnpm 9's indented single-quoted keys): Nest 11.2.6, Fastify 5.12.3, MikroORM 6.6.16 — and `@nestjs/platform-express` 11.2.3 with `express` 5.2.1, locked only as optional peers of `@nestjs/core` (`/backend-audit`'s F1 tags them `[peer-only]`; grep 0's adapter is Fastify). Before that line this F1 printed ranges only, so a run of this skill alone read every version-gated row `UNREAD`. Grep 0: one `new FastifyAdapter` in the shared configure function, one `APP_FILTER` catch-all, one controller-scoped catch-all for a v1 door (B-D6), one Fastify scope `setErrorHandler` (3 mapper files). **1b 0** — both catch-alls keep `getStatus()`. **1c 2** → the configure function's parser hook and the filter's 413 arm both say Nest hands the filter an `HttpException`/`SyntaxError` for Fastify's own refusals; the lab V345 parser rows on the same versions (Nest 11.2.6, Fastify 5.12.3, 2026-10-14) confirm it for malformed, empty, oversized and wrong-type bodies and the unknown route (B-D17). Both stay Unconfirmed, low, until a read shows no pipeline thrower carries a `statusCode` (not re-read in this run). **2a: the ORM's `NotFoundError` is still unmapped** — both filters name `NotFoundError`, but import it from the project's domain errors module (`./errors`, a class that even sets `this.name = 'NotFoundError'`), not from `@mikro-orm/core`; no `findOneOrFailHandler` is configured, so the error falls to the filter's unclassified 500 `INTERNAL` arm. **2b: 12 `findOneOrFail` sites in 11 files**; 3 are reached by an optional body `id` on an upsert POST (rate cards, shipping costs, pricing rules) → a random id answers 500, not 404 (`[report-flagged]`, settling request: one of those POSTs with a random UUID). `NotNullConstraintViolationException` is named by no mapper (lower: only a missed check or a race reaches it); unique, FK, check (now mapped, with a SQLSTATE `23514` fallback) and optimistic-lock are mapped from `@mikro-orm/core`. Collision row: 1 (`NotFoundError`). **2c**: 64 error classes, 11 families no mapper names — one of 24 classes (a `Refusal` base that each module's application layer translates; its doctrine comment says one that escapes its mapper surfaces as the machine code, i.e. a 500 — a per-path read) and 10 singletons (job, outbound and import internals, read). **§3** 0 Express-only calls, 0 express-typed responses (B-D3: `reply.status()` and `redirect(url, 302)` are not listed by design). **§4** N/A (Nest catches; no Express, Koa, Go or axum router). **§5**: 5a 0 (the raw Fastify hooks return or throw); 5c 1 of 34 `@Res()` lines — a `return` inside a nested arrow in a private helper → decoy (B-D2); 5b, 5d 0. **§7** 0 throwers; the envelope is now readable: every arm of the global filter returns the contracts package's `ApiError` type and sends it through the package's `fail()`, and the package pins a zod `apiErrorSchema` to that type, so "every error body validates against the envelope" holds at the type level (the V345 matrix still settles it at runtime). **§8** 0. An earlier partial copy (no lockfile, no contracts package, an older commit) printed the same 60 lines with 11 sites in 10 files, 66 classes in 13 unnamed families and `CheckConstraintViolationException` unmapped.
- **Research labs** (paired POS/NEG lines): Nest `@Catch()` that writes 500 with `res.status().json()` (1b and 3a), an Express 4-arity handler with no status (1b), a Flask `errorhandler(Exception)` (1b), `reply.send` with no return (5a, both one-line forms) while `return reply.send` and `reply.send(…); return reply` stay quiet, a send inside `setTimeout` (5b), `@Res()` without passthrough returning a value (5c) while two passthrough routes stay quiet, `res.send(404)` and `res.status('201')` (5d), Go `http.Error` with no `return` in both shapes (5e) while the `return` sample stays quiet, Koa `next()` un-awaited (4c) while `await next()` stays quiet, `gin.New()` (4f) and `c.Bind` (6), tRPC `throw new Error` (7b), a thrown string, a thrown object and `HttpException({…}, 422)` (7a), FastAPI and DRF with no handler (6). A scratch pair added for 2a/2c/§8 found the domain family no mapper names, the `err.response.status` and `HTTPException(status_code=r.status_code)` pass-throughs, and stayed quiet on the 502 rewrite.
- **Fixtures** (`benchmarks/fixtures/*`, 18 roots; none seeds an EE class yet — the `backend-defects` fixture is a later build item): 0 `rg` errors on any root. `node-api` 1b 1 (its error middleware); `obs-defects` 1b 1 (a Spring `@ExceptionHandler(Exception.class)`), 1c 1, six MikroORM classes named by no mapper; `quality-mix` 1c 1, four Prisma rows named by no mapper, 5 domain families outside the filter's `DomainError` arm; `vuln-fullstack` (Express adapter: §3 N/A) four Prisma rows; `ci-defects`, `slow-marketplace`, `brittle-suite` have no mapper at all, so every ORM row reads "named by NO mapper" — the framework default decides, a §6 read.
- **`backend-defects` fixture** (2026-10-14, after the fixture's IR-11): when `rest_framework` is imported, DRF's `APIException` family counts as mapped, so `IllegalTransition(APIException)` is no longer a 2c row; `LedgerError` (BD-EE-2b, 4 classes) is the only family left. With the lockfile line the block prints 86 lines (5 lockfile lines: Nest core and its Fastify platform 11.1.6, Fastify 5.4.0, MikroORM 6.4.16, Express 5.1.0 for the admin app), the same seeds and decoys.

## The 3,000-hit path

EE is wiring-first: one global mapper decides most rows (P5). Read **every** 1a mapper whole before any per-site grep — a repo has a handful. Then: §2 grouped by ORM class (one finding per unmapped class, with the 2b sites as its N; one row per 2c family, never per class); §5 grouped by controller file; §7 grouped by the mapper that rebuilds the body — when the global filter rebuilds every body from `getResponse()`, all 7a object throws close with **one** cited read. A group may close with one cited reason when the reason is checked, not assumed. A partial review prints `Live, unreviewed (k groups / n hits)`, never `checked`.

## Scans for

| § | Class (research id) | Default severity | Oracle |
|---|---|---|---|
| 1 | catch-all flattens status (BE-01, BX-02, BF-FL-01, BF-LA-05) | high (a client 4xx answered 500, or every failure answered 400) | V345 |
| 2 | domain, ORM and DB errors unmapped (BA-05, BE-02, BX-03) | high when client input reaches it (a random id → 500); medium on a race-only path | V330 |
| 3 | filter on the wrong adapter API (BE-03, BN-09 filter half) | blocker during an adapter migration, else high | V345, V346 |
| 4 | async errors escape; process crash (BE-04, BE-06, BX-05, gin `New()`, BF-RS-05, BF-FL-03) | blocker on a crash, else high | V345 |
| 5 | reply lifecycle: double send, empty 200, hang, continue after error (BE-05, BN-04, BN-10, BN-11, BF-GO-01, BF-RA-01) | high; Go `http.Error` followed only by a log → low (B-R10) | V345 |
| 6 | framework default error path outside the envelope (BX-01, BX-04, BN-03, BV-16, BA-14, BF-NET-01, BF-RS-03, BF-RA-06) | high on a public API, medium internal | V345 |
| 7 | thrower breaks the envelope; RPC/GraphQL mapping (BE-07, BE-08) | medium | V345 |
| 8 | upstream status passed through (BO-07) | medium; high when a provider 401 logs our user out | V354 |

Every lane row that rests on a framework default also carries V357: the oracle ran on the installed version and the finding states it.

### 1. Catch-all flattens status

```
BAD:   @Catch() class AllFilter { catch(e, host) { const s = e instanceof DomainError ? e.status : 500; … } }   // pipe 400, throttler 429, 413, 415 → 500
       app.use((err, req, res, next) => res.status(500).json({ code: 'internal' }))   ·   @app.errorhandler(Exception) → 500   ·   @ExceptionHandler(Exception.class) → 500
GOOD:  if (e instanceof HttpException) return reply.status(e.getStatus()).send(toEnvelope(e.getResponse()));   // before the 500 arm
       Flask: an errorhandler(HTTPException) that keeps e.code · Spring: specific handlers + ResponseEntityExceptionHandler
```
**Read the code:** does every exception kind the app throws keep its status — the framework's own (pipe 400, `NotFoundException`, throttler 429, body-limit 413, 415) included? 1c: does the catch-all keep a non-HttpException that carries `statusCode`? On the Fastify adapter Nest converts Fastify's own refusals before any filter runs — `{` 400, empty JSON body 400, over `bodyLimit` 413, `application/xml` 415, unknown route 404 and a `FastifyError` thrown in a Fastify hook all arrive as `HttpException` with Fastify's status, so `instanceof HttpException ? getStatus() : 500` keeps them [V lab 2026-10-14: Nest 11.2.6 on Fastify 5.12.3, Nest 12.1.3 on 5.12.5; B-D17]. A 1c hit stays a candidate only for a `statusCode`-carrying non-HttpException thrown **inside** the pipeline (handler, guard, interceptor, pipe) — `@fastify/multipart`'s `file()`/`parts()` limits, an `http-errors` or `@fastify/error` object from a library — or a plain `Error` with `statusCode` thrown in a Fastify hook: those reach the catch-all raw and answer 500 (measured on both versions; Nest's default filter keeps the first two, and the hook one only on 11). On the Express adapter the 11.2.6 core converts only `SyntaxError`/`URIError` (to 400) [read, not run], so body-parser's 413/415 reach the catch-all raw — read the installed adapter there. The reverse is the same class: everything → 400 hides outages from 5xx alerting. **Finding when** a failure the contract gives a 4xx (or 5xx) answers another class through the shipped mapper. **Proof:** V345 — the framework `HttpException` rows (400, 404, 413, 415, 429) and malformed JSON through the real app keep their status.

### 2. Domain, ORM and DB errors unmapped

```
BAD:   import { NotFoundError } from './errors';            // the DOMAIN class; MikroORM's NotFoundError from findOneOrFail falls to 500
       await em.findOneOrFail(RateCard, { id: dto.id })     // a random id → 500
       class LedgerError extends Error {}                    // thrown by a use case; no mapper names it or a parent
GOOD:  import { NotFoundError as OrmNotFoundError } from '@mikro-orm/core';   + an arm → 404
       or findOneOrFailHandler: (entity, where) => new NotFoundError({ … })   // the ORM throws the mapped domain class
```
**Read the code:** which statuses does the contract give 404 / 409 / 412 / 422? For each 2a row: is the class imported from the ORM's package, or is the arm testing a same-named project class? Is the race-time unique violation mapped, not only the pre-check? With `rest_framework` imported, DRF's `APIException` and its built-in subclasses (and `Http404`) count as mapped — the default handler answers their `status_code` inside DRF views; a plain Django view raising one still answers 500. For each 2c family: does an application-layer mapper translate it on **every** path that reaches the edge (B-D15)? A genuinely infrastructural error (a DB timeout) may be 5xx by contract — then it is a 503 with `Retry-After`, not "mapped". **Finding when** a client-reachable failure the contract gives a 4xx answers 500. **Proof:** V330 — a random id into each 2b site, a sequential duplicate **and** a duplicate after a passing pre-check, an FK violation, a NOT NULL/CHECK violation, a stale `If-Match` (412), an illegal state (409), each on the production engine in a container (B-R16).

### 3. Filter on the wrong adapter API

```
BAD:   (FastifyAdapter)  const res = host.switchToHttp().getResponse<Response>(); res.status(500).json(body);   // .json is Express: TypeError in the filter → 500 for every error
       @Res() res: Response   (from 'express')  ·  FileInterceptor from @nestjs/platform-express on Fastify
GOOD:  reply.status(s).send(body)  ·  reply.code(s).send(body)  ·  httpAdapterHost.httpAdapter.reply(ctx.getResponse(), body, s)   // portable
```
**Read the code:** which adapter does the bootstrap build — and does the filter run on it (a filter shared by two apps)? `reply.status()` is a valid Fastify alias and `reply.redirect(url, code)` is the v5 order (B-D3); `reply.raw.setHeader` is the Node response, valid. **Finding when** an Express-only call runs inside a filter, interceptor or middleware on the Fastify adapter. **Proof:** V345 on the real adapter; V346 when the project is mid-migration — the same error suite on both adapters, status and body diffed.

### 4. Async errors escape; the process crashes

```
BAD:   (express ^4)  app.get('/x', async (req, res) => { await svc.run(); })   // a rejection crashes Node 22
       app.use(async (ctx, next) => { next(); })   (Koa: async routes answer 404)   ·   r := gin.New()   ·   Router::new() with no CatchPanicLayer
GOOD:  import 'express-async-errors' at boot, or asyncHandler(fn) on every route · await next() · gin.Default() or r.Use(gin.Recovery()) · .layer(CatchPanicLayer::new())
```
**Read the code:** what does F1 say — Express 5 forwards rejections to the error handler, Express 4 does not [V]? Is a wrapper applied to **every** async handler (one router without it is the finding)? For Go: is the recover middleware on the router that serves the API? A thread or executor started from a Flask view loses the app context (BF-FL-03, [K]). **Finding when** a throw in a handler can end the process or the connection instead of answering. **Proof:** V345 — a route that throws inside an `await`, a rejected promise, a panic; then one healthy request is served.

### 5. Reply lifecycle: double send, empty 200, hang, continue after error

```
BAD:   fastify.get('/a', async (req, reply) => { reply.send(x); return y; })   // FST_ERR_REP_ALREADY_SENT; first answer wins
       setTimeout(() => reply.send(x), 10)   (200 empty first)  ·  @Get() f(@Res() res) { return dto; }   (hangs)
       res.send(404)   (Express 5: 200 with body "404")  ·  if err != nil { http.Error(w, "bad", 400) }  w.WriteHeader(201)   (body appended)
GOOD:  return reply.send(x)  ·  @Res({ passthrough: true })  ·  res.sendStatus(404)  ·  http.Error(…); return
```
**Read the code:** is the 5a hit in a raw Fastify handler or hook, not a Nest controller or filter (B-D8)? For a 5c hit: does every branch of the method send or throw, and is the `return` in the handler itself, not a nested callback (B-D2)? Record the trade a `@Res()` route makes: it bypasses the response, idempotency and deadline interceptors. For Go: what follows the missing `return` — only a log (low) or a write (high, B-R10)? Rails: is `save`/`update` a bare statement whose `false` the controller ignores? **Finding when** a branch answers twice, never, empty or after its error. **Proof:** V345 — each route with a timeout, the logs captured, no `FST_ERR_REP_ALREADY_SENT` / `ERR_HTTP_HEADERS_SENT` / `superfluous WriteHeader`, a non-empty body on every non-204.

### 6. Framework default error path outside the envelope

```
BAD:   DRF with no EXCEPTION_HANDLER: IntegrityError → HTML 500   ·   FastAPI with no Exception handler: text/plain 500
       Express: no JSON 404 handler (HTML), const { name } = req.body with no parser (Express 5 → 500), schema.parse(req.body) with no ZodError arm
       [ApiController] with no InvalidModelStateResponseFactory  ·  gin c.Bind (writes 400 before you)  ·  axum Json with no custom rejection
GOOD:  one handler per lane that renders the project's envelope for every failure class, framework errors included
```
**Read the code:** what does each of the ten failure classes — unknown route, wrong method, malformed JSON, wrong content type, validation, not-found, conflict, unique violation, uncaught, panic or thrown non-Error — answer (content type, envelope, status class)? Which ones never reach the project's mapper (the proxy's 413 page, Kestrel's limits, a parser that runs before routing)? A server-rendered HTML app whose envelope **is** HTML is out of scope; a project that documents 422 for validation is not a finding (B-A7). **Finding when** a client receives a non-envelope body or another status class for a failure the contract covers. **Proof:** V345 — the full matrix through the real bootstrap.

### 7. Thrower breaks the envelope; RPC and GraphQL mapping

```
BAD:   throw new UnprocessableEntityException({ code: 'X' })   // Nest returns the object verbatim: no statusCode, no message
       throw 'boom'  ·  throw { message: 'x' }  ·  tRPC: throw new Error('db down')   (500 + the raw message)  ·  no formatError / errorFormatter
GOOD:  throw new DomainError('X') mapped by the filter  ·  throw new TRPCError({ code: 'CONFLICT' })  ·  formatError mapping extensions.code
```
**Read the code:** does the global filter rebuild every body from `getResponse()` into the envelope (then every 7a object throw is mapped: one read closes the group)? Does a v1 door document its own shape (B-D6)? For GraphQL, 200 with `errors[]` is the norm (B-A17): the finding is an unmapped `extensions.code`, or alerting that reads only the HTTP status. The raw message's **content** is security's (§ Boundaries). **Finding when** an error body does not validate against the declared envelope, or a thrown non-Error loses its status. **Proof:** V345 — each 7a site's route, its body validated against the envelope schema.

### 8. Upstream status passed through

```
BAD:   catch (err) { res.status(err.response.status).json(…) }   ·   raise HTTPException(status_code=r.status_code)   ·   w.WriteHeader(resp.StatusCode)
GOOD:  a provider 401/403 → our 502 with code UPSTREAM_AUTH · 404 → 502 or our own 404 only when it means "your resource" · 429 → 503 + Retry-After
```
**Read the code:** is this a documented pass-through proxy or BFF (decoy)? Which provider statuses can arrive — a provider's 401 means **our** credentials failed and, passed through, logs our user out; a provider 404 becomes "your order does not exist". **Finding when** a provider's status reaches our caller unmapped where the contract defines our own. **Proof:** V354 — a provider stub answering 401, 404 and 429 → our 502/503/424 with our code.

## Proof

The failure-class matrix of `proof-oracles.md` § Backend is the oracle for §1 and §3–§7 (V345) and its ORM rows for §2 (V330): **one request per class through the app the project's own factory builds**, on the adapter `main.ts` uses, against a scratch database in a container — `GET /__nope`, a wrong method, a body of `{`, `Content-Type: text/plain`, a validation failure, a random id into a 2b site, a duplicate (sequential and after a passing pre-check), a route that throws `new Error()`, one that throws a string, the framework's `HttpException`s (400, 404, 413, 415, 429) — then one healthy request to prove the process survived. Assert status class, content type and envelope per class, and capture the logger. The control: a documented v1 door shape (B-D6) and a 200-with-`errors[]` GraphQL answer still pass. A matrix that did not run is `NOT-RUN`, never PASS; a hand-built filter or `Fastify()` in the test is not the shipped wiring (P4).

## Output

```
edge-error-scan — lanes: nestjs 11.2.6 on fastify 5.12.3, mikro-orm 6.6.16 (pnpm-lock.yaml; express 5.2.1 locked only as an optional peer)
Wiring: APP_FILTER src/app.module.ts:198 AllExceptionsFilter (@Catch(), getStatus() kept) · @UseFilters v1 door (documented shape, B-D6) · Fastify scope setErrorHandler src/bootstrap.ts:179
Tools: failure-class matrix NOT-RUN (no scratch database in this run) · captured logs NOT-RUN · semgrep N/A (no Go)

Findings: 0 · Unconfirmed: 4 (2 listed)

1. src/shared/catch-all.filter.ts:167 (+ 12 findOneOrFail sites in 11 files)                [report-flagged]  high
   §2 — the arm `instanceof NotFoundError` tests the domain class imported from ./errors, not @mikro-orm/core; no findOneOrFailHandler.
   3 sites take an optional body id on an upsert POST: POST /delivery/carrier-rates {"id":"<random uuid>"} → expect 404, gets 500.
   Fix: an arm for @mikro-orm/core's NotFoundError (aliased import), or findOneOrFailHandler throwing the domain class. Settling: V330.
2. src/shared/catch-all.filter.ts (no arm)                                                    [report-flagged]  medium
   §2 — NotNullConstraintViolationException named by no mapper → 500 on a missed check or a race (unique, FK, CHECK, optimistic lock mapped).
   Fix: map it to the 400 the contract gives. Settling: V330 NOT NULL row.

Verification: 5 candidates → 0 findings · 4 unconfirmed (2 listed; 1c ×2 low: parser rows settled by B-D17, pipeline throwers unread) · 1 refuted (self-verified: 5c, B-D2)

Class coverage:
  §1 catch-alls                checked (3 mappers → 0 in 1b; 1c 2 → 2 unconfirmed, low)
  §2 ORM/domain mapping        checked (7 lane rows → 2 unconfirmed; 1 name collision) · Live, unreviewed (11 families / 34 classes from 2c)
  §3 adapter API               checked (0 Express-only calls on Fastify)
  §4 escaping errors           N/A (Nest adapter catches; no Express 4, Koa, Go or axum router)
  §5 reply lifecycle           checked (5a 0 · 5c 1 → 0, B-D2 · 5b/5d 0)
  §6 default error paths       checked (Nest only; matrix NOT-RUN)
  §7 envelope                  checked (0 throwers; every filter arm returns the contracts package's ApiError through fail(), pinned by its zod schema)
  §8 upstream status           checked (0)
```

`[report-with-fix]`: the matrix or the V330 row failed through the real bootstrap on the installed version and the fix is local to the project's mapper. `[report-flagged]`: one link is unproven (no matrix run, the version `UNREAD`, the path from client input to the thrower not traced); the row names it and the settling request. The coverage block lists **all eight** §s on every run: `checked (k → m)`, `N/A (<reason>)`, `blocked (<grep or tool>)`, `→ <owner> (k)` or `Live, unreviewed (k groups / n hits)`. A missing line is printed by `/backend-audit` as `not run`.

## False positives / precedents

The verifier reads [`precedents/backend.md`](../../../../snippets/precedents/backend.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **B-D2** `@Res()` routes where every branch sends or throws and the reason is written; **B-D3** `reply.status()` and `reply.redirect(url, 302)` on Fastify v5; **B-D6** a v1 door documenting its own error shape (its table still owes the DB arms — a minor §2 row); **B-D8** `reply.send` with no `return` inside a Nest controller or filter.
- **B-A2 / B-A17** 200 with an error object where the protocol says so (GraphQL, JSON-RPC, tRPC batches); **B-A7** one consistent 400 or 422 across the API; **B-A15** Express 4 async handlers all wrapped; **B-R10** `http.Error` followed only by a log → low.
- **B-G16 / B-G20 / B-G21** one envelope with a stable machine code; the most specific status; downstream errors mapped to our own semantics.
- **P1** every finding cites the contract; **P3** "an attacker learns…" goes to security; **P4** prove on the adapter and filter that ship; **P5** one finding at the mapper, N throw sites.

Shapes this skill must not report: `reply.raw.setHeader` (the Node response); a log-then-`super.catch()` filter; a 503 with `Retry-After` for a DB timeout; a module mapper that translates its family on every path (cited); HTML error pages in a server-rendered app.

## When to run

- On any diff that touches a filter, error middleware, an exception handler or advice, the adapter or its options, a domain error class, an ORM call that throws on absence, a `@Res()` handler, or an outbound client's error path — `/backend-audit`'s "an error mapper or adapter file" signal.
- On every whole-repo `/backend-audit`, reporting all eight §s; before switching Nest adapters, upgrading Express 4 → 5, Fastify, Apollo, tRPC or the ORM across a major (V346, V357); after `/add-endpoint`, whose gate cites V345.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier is not the run that found it, gets part A (the mapper and where it is registered), part B (the version and adapter lines), the throw site and the request — never this run's reasoning — and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/backend.md`. Under `/backend-audit` that is `@api-reviewer` in refute mode, then `@verifier` mode `refute` on every BLOCKER and HIGH; standalone, apply the protocol as a second pass and tag the rows `self-verified`. List the rest as Unconfirmed, Hardening or Refuted; never drop them.
- **Halt before any § when grep 0 is unread.** A verdict on a throw site without the mapper that answers it is invalid; when the mapper is built where grep 0 cannot see, read the bootstrap by hand and quote it.
- **Halt on any finding missing its anchors:** the mapper or throw `file:line`, the wiring row, the adapter and version, the failure class with its expected and actual answer, the contract source, the fix in the project's own mapper.
- **No `[report-with-fix]` without V345 / V330 / V354 through the project's own bootstrap** on the installed version and adapter (or a two-ended static fact). A test that builds its own filter, `Fastify()` or `express()` is not one.
- **No proposed fix may hide the class:** never a blanket `catch` that answers 200, never mapping every unknown error to 400, never deleting a route's `@Res()` without restoring what it sent, never widening a test's expected status to accept 500.
- **Do not grade a class another pack owns** (§ Boundaries); route it with a count. **Do not print "errors look handled"** without the coverage block; a § whose grep did not run is `blocked`, never `checked`.

## Related

- `/backend-audit` dispatches this skill and folds its coverage block into its edge-error ledger rows; `/backend-fix` closes findings failing-first through the real bootstrap and re-runs this detector.
- `validation-boundary-scan`, `http-contract-scan` and `api-consistency-audit` (this pack) are the neighbours named in § Boundaries; `endpoint-test-method` (this pack) drives the matrix requests against a running app; `@api-reviewer` judges these rows.
- security `data-exposure-scan` §1/§2/§5 and `file-access-scan` §2, code-quality `error-handling-scan` §1–§4/§6, observability `error-tracking-scan` §4 and `log-signal-scan` §1/§2, distributed-systems `retry-deadline-scan`, when those packs are installed.

## Sources

Defaults tagged `[V]` were run in the backend research labs on 2026-10-14: NestJS 12.1.3 on both adapters (default filter behaviour, an Express-API filter on Fastify, `HttpException` with an object body, `@Res()` without passthrough, body-parser and Fastify parser errors), Express 4.21 and 5.3.0, Fastify 5.12.7, Koa 3.2.1, tRPC 11.19.0, Apollo Server 5.5.1, Mercurius 16.12.0, DRF 3.18.3 / Django 6.1.2, FastAPI 0.143.0 / Starlette 1.8.0, Flask 3.1.3, Go 1.27.2, gin v1.12.0, echo v4.16.0, semgrep 1.180.0, golangci-lint 2.14.0 (backend research notes A and B, labs A and B). `[K]` rows (Spring, ASP.NET Core, Rails, Laravel, axum, actix, Go net/http panic handling) are vendor documentation as read by the research, not run; `[K?]` Spring Boot 4 defaults are secondary. Nest 11.2.6 (`core`, `common`, `platform-fastify`) on Fastify 5.12.3, with class-validator 0.15.1 and class-transformer 0.5.1, was run on 2026-10-14 for the 1c rows only — the parser, body-limit, content-type, empty-body, JSON-`null` and unknown-route requests plus statusCode-carrying errors thrown in a handler and in a hook, with a project-style catch-all and with Nest's default filter, repeated on Nest 12.1.3 / Fastify 5.12.5; the conversion is `RoutesResolver.mapExternalException` (`isHttpFastifyError`) in 11 and the adapter's `mapException` in 12. Nest 11's Express adapter was not run. The ORM class names are those the packages export; the MikroORM ones were read in the real repo's filter imports. The real-repo counts are from a read-only run on 2026-10-14 (batch-5 eval § 3, re-measured with the block above). Paraphrased; no text reproduced beyond identifiers.
