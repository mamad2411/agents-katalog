---
name: data-exposure-scan
description: Information leakage — stack traces and raw errors in responses, debug and admin endpoints reachable in prod, over-returning serializers, account enumeration, secrets and PII in logs, fingerprinting headers, cacheable private responses, and exposed internal files.
kind: skill
pack: security
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: data-exposure-scan

## Premise

Most breaches start with reconnaissance the app gave away. A stack trace names the ORM and the file layout. A debug page dumps the environment. `/actuator/heapdump` hands over live session tokens. A login that says "no such user" confirms which emails to spray, a log line holds the `Authorization` header, and a CDN serves one user's `/me` to the next. None of these is a break-in. Each one hands the attacker data, or the map they need for the next step. This skill is the static detector for those **runtime leak sinks**, the places where the running app emits what it should keep. It is the depth behind `@security-auditor`'s A02 verbose-error bullet, its A09 redaction bullet and its A10 leak bullet.

**Every finding cites the sink at `<file:line>`, what leaks and to whom (the failing condition), and the fix.** "Errors might leak" without the handler line and the field that reaches the client is not a finding. A grep hit is never a finding by itself: read the enclosing function, its middleware chain and the config that governs it in production.

**Ownership, so nothing is reported twice:**
- **Committed secrets** belong to `secret-scan-method`. This skill finds a secret only where the *running app* emits it: into a log, a response or a served file.
- **The PII lifecycle and its regulation** (lawful basis, erasure, cross-border transfer) belong to `@data-privacy-reviewer`. This skill reports the leaking sink. That agent grades the personal-data consequence.
- **BOPLA design** (the DTO architecture, mass assignment) belongs to `@api-security-reviewer` API3. § 4 here is the grep sweep that feeds it.
- **Log injection** (CWE-117, forged log lines) is `injection-scan`'s. **Client-bundle source maps and secrets**, plus tokens kept in web storage, are `xss-scan`'s. **Path traversal** on read and download is `file-access-scan`'s. **Proxy banners, edge cache rules and dashboards exposed by infrastructure** are `iac-scan`'s. The **content of the edge access log** (what Caddy, nginx, an ingress or a load balancer writes per request) is this skill's § 6: it carries every URL and header secret the app itself redacts.

## Adapt to the codebase

Before the first grep, find the four things every detector below reads. Phrase each fix in the primitive the project already uses:

| Stack | Error handler (read it first) | Debug / verbose-error switch | Logger redaction primitive | Constant-time compare |
|---|---|---|---|---|
| **Node/TS**: Express, NestJS, Fastify, Next.js | Express 4-arg `app.use((err, req, res, next) => …)`; NestJS `@Catch()` filter / `useGlobalFilters`; Fastify `setErrorHandler`; Next.js route-handler `catch` + `error.tsx` | `NODE_ENV` ≠ `production` at runtime → Express's default handler prints the stack; Fastify's default handler sends `err.message` even on a 500 | pino `redact: { paths }` (also through `pino-http`); winston has none built in (a custom `format`); morgan has none (custom tokens only) | `crypto.timingSafeEqual(a, b)` on equal-length Buffers |
| **Python**: Django, FastAPI, Flask | Django `handler500` / middleware `process_exception` / DRF `EXCEPTION_HANDLER`; FastAPI `@app.exception_handler`; Flask `@app.errorhandler` | Django `DEBUG`; FastAPI/Starlette `debug=True` (traceback page); Flask `debug=True` / `FLASK_DEBUG` (the Werkzeug console) | a `logging.Filter` on the handler; a structlog processor; Django `@sensitive_variables` / `@sensitive_post_parameters` for error reports | `hmac.compare_digest` / `secrets.compare_digest`; Django `constant_time_compare` |
| **Go**: net/http, gin, echo, fiber | every `http.Error(w, …)`; gin `c.JSON` in handlers; echo `HTTPErrorHandler`; fiber `ErrorHandler` | echo `e.Debug = true`; fiber's default `ErrorHandler` writes `err.Error()`; the `_ "net/http/pprof"` and `expvar` imports | `slog.HandlerOptions.ReplaceAttr`; a `LogValue()` method on secret-bearing types | `subtle.ConstantTimeCompare`, `hmac.Equal` |
| **Java/Kotlin**: Spring | `@RestControllerAdvice` + `@ExceptionHandler`; a custom `ErrorAttributes` | `server.error.include-stacktrace` / `include-message` / `include-exception` / `include-binding-errors`; actuator exposure | logstash-logback-encoder `MaskingJsonGeneratorDecorator`; Log4j2 `RewritePolicy`; `@ToString.Exclude` | `MessageDigest.isEqual(a, b)` |
| **Ruby/Rails** | `rescue_from` in `ApplicationController`; `config.exceptions_app` | `config.consider_all_requests_local` in `production.rb`; `web-console` / `better_errors` outside the development group | `config.filter_parameters`; `ActiveRecord::Base.filter_attributes` | `ActiveSupport::SecurityUtils.secure_compare`, `Rack::Utils.secure_compare` |
| **PHP/Laravel** | `bootstrap/app.php` `->withExceptions()` (11+) / `app/Exceptions/Handler.php` (≤10); `set_exception_handler` | `APP_DEBUG`; `display_errors`; Ignition / Debugbar / Telescope reachable in production | a Monolog processor (`pushProcessor`); `#[\SensitiveParameter]` (PHP 8.2+) keeps arguments out of traces | `hash_equals($known, $given)` |

**NestJS / Fastify.** A global `@Catch()` filter is usually sound; the leak sits upstream of it, in a use-case `try/catch` that turns any `Error` into a result row or a persisted `lastError` before the filter ever runs (grep 1c). Fastify sends no `X-Powered-By` by default; `NestFactory.create(…, new FastifyAdapter())` is the app instance § 8 reads.

**Served directories.** § 10 inspects what sits in each one. Resolve them per stack: Express / NestJS / Fastify / Koa use every `express.static(dir)` / `app.useStaticAssets(dir)` / `ServeStaticModule` `rootPath` / `@fastify/static` `root` / `koa-static` argument. Next.js, Vite and CRA use `public/`. Nuxt uses `public/` (Nuxt 3) or `static/` (Nuxt 2). Angular uses the `assets` entries in `angular.json` (`src/assets`, or `public/` on newer projects). SvelteKit uses `static/`. Django uses `STATIC_ROOT`, `STATICFILES_DIRS` and `MEDIA_ROOT`. FastAPI / Flask use `StaticFiles(directory=…)` mounts and `static_folder`. Go uses every `http.FileServer(http.Dir(…))`. Spring uses `src/main/resources/{static,public,resources}` and `spring.web.resources.static-locations`. Rails and Laravel use `public/`, which is the document root.

**Production truth lives in config, not in code.** For every switch above, find the value the *production* process actually gets. That means the env file or manifest the deploy loads, plus the default when the variable is unset. A debug flag that defaults to on is on wherever someone forgot to set it.

## Pre-flight greps

Run these from the repo root. They produce the candidate set the detectors below judge, and grep *N* feeds § *N*. Adjust each alternation to the stack's row in the table above. `rg` is assumed.

```bash
# Shared scope. --hidden because .env.production / .well-known are dotfiles rg skips by default.
# Every command passes an explicit `.`: with no path and a non-tty stdin (an agent's shell) rg
# reads stdin and hangs. Tests, mocks, snapshots, lockfiles, tooling scripts and Refract's own trees
# (ai/, .claude/) are not runtime sinks: on a real monorepo they were half of every grep.
X=(--hidden -g '!.git' -g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/dist/**' -g '!**/build/**' -g '!**/.next/**' -g '!**/target/**' -g '!**/*.min.js' -g '!**/*.map' -g '!*.md'
   -g '!**/*.{lock,snap}' -g '!**/*-lock.{json,yaml}' -g '!**/{test,tests,__tests__,__mocks__,__snapshots__,e2e,scripts}/**' -g '!**/*.{spec,test,mock}.*' -g '!**/*.e2e-spec.*' -g '!ai/**' -g '!.claude/**')

# 1a. The universe: every error handler / exception filter / rescue. Read each one (§1).
rg -n --pcre2 '\(\s*(err|error|e|ex|exception)\s*,\s*req\s*,\s*res\s*,\s*next\s*\)|@Catch\(|implements\s+ExceptionFilter|setErrorHandler|exception_handler|errorhandler\(|handler500|EXCEPTION_HANDLER|@(Rest)?ControllerAdvice|@ExceptionHandler|rescue_from|exceptions_app|withExceptions|set_exception_handler|HTTPErrorHandler|ErrorHandler\s*:' "${X[@]}" .
# 1b. Exception internals anywhere but a log call: the finding set. Log lines are filtered out, so a
#     multi-line body (`stack: err.stack,` on its own line) still surfaces — and so does the continuation
#     line of a multi-line `logger.warn(` call: read one line up before counting it.
rg -n --pcre2 '\b(err|error|e|ex|exc|exception)\.(stack|message|sqlMessage|sql|original|parent|getMessage\(\)|getStackTrace\(\)|Error\(\)|backtrace|full_message)|->(getMessage|getTraceAsString)\(\)|traceback\.format_exc\(\)|(str|repr)\((e|err|exc|ex|error)\)|printStackTrace\(' "${X[@]}" . \
  | rg -v --pcre2 '\b(log|logger|console|logging|slog|Log|Sentry)\s*(\.|::)\s*\w+\s*\(|process\.std(out|err)\.write\('
# 1c. A catch-all that copies raw error text into a FIELD — a result row, a persisted `lastError`, a note —
#     before the global filter ever sees the error. Follow each value to where it is served. Also the plain copy with
#     no `instanceof` (`errorMessage: error.message.slice(0, 800)`) and a helper in between (`error: errorText(e)`).
rg -n --pcre2 '\b\w*([Ee]rror|[Rr]eason|[Mm]essage|[Dd]etail|[Nn]ote|[Ff]ailure)\w*["\x27]?\s*[:=]\s*[^;\n]*?\binstanceof\s+\w*(Error|Exception)\s*\?\s*\w+\.message\b|["\x27]?\b\w*(error|detail|message|reason|note)["\x27]?\s*[:=]\s*(str\(\s*(e|exc|err|ex)\s*\)|(e|err|ex)\.(Error\(\)|getMessage\(\)))|\b\w*([Ee]rror|[Rr]eason|[Mm]essage|[Dd]etail|[Nn]ote|[Ff]ailure)\w*["\x27]?\s*:\s*(\w+\()?\s*(e|err|error|ex|cause)\.message\b|\b\w*([Ee]rror|[Rr]eason|[Mm]essage|[Dd]etail|[Nn]ote|[Ff]ailure)\w*["\x27]?\s*:\s*\w*(Text|Reason|Message)(Of)?\(\s*(e|err|error|ex|cause)\s*\)' "${X[@]}" .

# 2a. Debug / verbose-error switches, including a default-on fallback (§2).
rg -n --pcre2 '^\s*DEBUG\s*=\s*True|DEBUG\s*=.*(environ\.get|getenv|env|config)\(.*,\s*["\x27]?(True|true|1)["\x27]?\)|DEBUG_PROPAGATE_EXCEPTIONS\s*=\s*True|\.run\([^)]*debug\s*=\s*True|FLASK_DEBUG\s*=\s*1|(FastAPI|Starlette)\([^)]*debug\s*=\s*True|include-(stacktrace|message|exception|binding-errors)\s*[:=]\s*["\x27]?(always|on[-_]param|true)|consider_all_requests_local\s*=\s*true|APP_DEBUG\s*=\s*true|env\(\s*["\x27]APP_DEBUG["\x27]\s*,\s*true\)|display_errors\s*=\s*(On|1)|\.Debug\s*=\s*true|h2\.console\.enabled\s*[:=]\s*true' "${X[@]}" .
# 2b. What the deploy actually sets: an Express app with NODE_ENV unset prints stacks.
rg -n 'NODE_ENV|RAILS_ENV|APP_ENV|APP_DEBUG|DJANGO_SETTINGS_MODULE|SPRING_PROFILES_ACTIVE|GIN_MODE' -g 'Dockerfile*' -g '*compose*.y*ml' -g 'Procfile' -g 'package.json' -g '*.toml' -g '**/k8s/**' -g '**/helm/**' -g '**/deploy/**' "${X[@]}" .

# 3. Debug, admin, metrics and docs surfaces (§3). GraphQL has its own grep, 11.
#    Anchored: bare `[Ss]wagger` matched every `@nestjs/swagger` decorator, `[Hh]orizon` the word "horizontal",
#    `/metrics` every `observability/metrics.ts` path. App-written debug routes and env dumps count too.
rg -n --pcre2 'management\.endpoints|exposure\.include|^\s*include:\s*["\x27]?\*|show-(details|values)\s*[:=]\s*always|/actuator|jolokia|net/http/pprof|"expvar"|/debug/(pprof|vars)|__debug__|debug_toolbar|/_profiler|laravel/telescope|Telescope::|laravel/horizon|Horizon::|debugbar|web-console|better_errors|Sidekiq::Web|bull-board|express-status-monitor|SwaggerModule\.setup|swagger-ui|swaggerUi|setup_swagger|SpectacularSwaggerView|springdoc|api-docs|redoc|docs_url|openapi_url|FastAPI\(|phpinfo|prom-client|promhttp|(?<![\w.-])/metrics(?![\w.-])|admin\.site\.urls|rails_admin|ActiveAdmin|\.well-known|@(Controller|Get|All|Post)\(\s*["\x27][^"\x27]*\b(debug|_?internal|diag\w*|env)\b|\b(env|environment|config)\s*:\s*process\.env\s*[,}\n]|(json|send)\(\s*process\.env\s*\)|(jsonify|JsonResponse)\([^\n]*os\.environ' "${X[@]}" .

# 4a. Entity / row / whole model handed to the serializer (§4).
rg -n --pcre2 'res\.(json|send)\(\s*(req\.user|user|users|account|customer|member|profile|row|rows|result|record|entity|doc|docs)\s*\)|render\s+json:\s*@?\w+\s*$|fields\s*=\s*["\x27]__all__["\x27]|model_to_dict\(|->toArray\(\)|response\(\)->json\(\s*\$\w+\s*\)|SELECT\s+\*|\.select\(\s*["\x27]\*["\x27]\s*\)|findAll\(\s*\)' "${X[@]}" .
# 4b. Fields that must never serialize, where the model declares them (`*entit*` catches `*.orm-entity.ts`)...
rg -n -i --pcre2 '\b\w*(password_?hash|hashed_?password|passwd|reset_?(token|code)|verification_?token|otp_?secret|totp_?secret|mfa_?secret|api_?key|api_?token|refresh_?token|recovery_?codes?|national_?id|ssn|_?encrypted|token_?hash|key_?hash|secret_?hash)\b' -g '*.prisma' -g '*.sql' -g '**/models/**' -g '**/model/**' -g '**/entities/**' -g '**/entity/**' -g '*entit*.*' -g '*model*.*' -g '**/schemas/**' -g '**/domain/**' "${X[@]}" .
# 4c. ...and the exclusion primitives. A 4b field whose model has no 4c line is a candidate.
rg -n --pcre2 '@Exclude\(|ClassSerializerInterceptor|select:\s*false|omit:|json:"-"|@JsonIgnore|WRITE_ONLY|write_only|exclude\s*=|response_model|\$hidden|\$visible|JsonResource|as_json|ActiveModel::Serializer|jbuilder|\bhidden\s*:\s*true|\blazy\s*:\s*true|\bserializer\s*:' "${X[@]}" .
# 4d. Every read of a model 4b flagged. Each must reach the response through a projection.
M='user|account|customer|member'   # replace with the model names 4b found
rg -n -i --pcre2 "\b(prisma\.($M)\.find\w*|($M)(Repository|Repo|Model)?\.(find\w*|where|all|first)\(|($M)\.objects\.|($M)::(find|where|all|first)|getRepository\(\s*($M)\w*\s*\)|\bem\.(find\w*|count|getReference)\(\s*($M)\w*\s*,)" "${X[@]}" .
# 4e. Projection-first code (no serializer; reads select `fields: [...]` and map rows to views), where 4c is empty by
#     design: controllers typed to return anything, and the files with an identity projection (`toItem: (r) => r`)
#     whose `fields:` list selects a 4b field. Read whether that row reaches a response before a map drops the field.
rg -n --pcre2 'Promise<\s*(unknown|any|object|Record<string,\s*(unknown|any)>)\s*>' -g '*controller*' "${X[@]}" .
rg -l --pcre2 '\b(toItem|map|project\w*|toView|view)\s*:\s*\(?(\w+)\)?(:\s*\w+)?\s*=>\s*\2\s*[,})]' "${X[@]}" . | xargs -r rg -n -i -U --pcre2 '\b(fields|attributes)\s*:\s*\[[^\]]*?\b\w*(password_?hash|hashed_?password|passwd|reset_?(token|code)|verification_?token|otp_?secret|totp_?secret|mfa_?secret|api_?key|api_?token|refresh_?token|recovery_?codes?|national_?id|ssn|_?encrypted|token_?hash|key_?hash|secret_?hash)\b'

# 5a. Auth messages that distinguish "no such account" (§5).
rg -n -i --pcre2 '(user|account|email|member)\s+(not\s+found|does\s*n.?t\s+exist)|no\s+(such\s+)?(user|account)|(unknown|incorrect|wrong)\s+(user(name)?|email|password)|(email|username)\s+(is\s+)?already\s+(taken|registered|exists|in\s+use)|USER_NOT_FOUND|EMAIL_(TAKEN|EXISTS)|(INVALID|WRONG)_PASSWORD|account\s+(is\s+)?(locked|disabled|suspended)' "${X[@]}" .
# 5b. Password-verify sites, hexagonal ones included (`this.hasher.verify(`), and the decoy hash whose presence
#     or absence answers the timing half. Read the unknown-user branch for the skipped-hash gap.
rg -n --pcre2 'bcrypt\.compare|argon2\.verify|verify_password|check_password|password_verify|checkpw|CompareHashAndPassword|passwordEncoder\.matches|authenticate\(|\b\w*[Hh]asher\.verify\(|\.verify\(\s*[\w.]*[Hh]ash|\b(decoy|dummy|fake)_?\w*[Hh]ash|\b(DECOY|DUMMY)_\w*HASH' "${X[@]}" .
# 5c. 403 THROW sites, not the class name. Read only those that follow a find* (existence confirmed to a non-owner).
rg -n --pcre2 'throw\s+new\s+\w*(Forbidden|PermissionDenied|AccessDenied)\w*\(|raise\s+\w*(PermissionDenied|Forbidden)\w*|abort\(\s*403|\bstatus\(\s*403\s*\)|HttpStatus\.FORBIDDEN|HTTP_403|:forbidden\b|http\.StatusForbidden|ResponseEntity\.status\(\s*403' -g '!**/{i18n,locales,guards}/**' -g '!**/*.messages.*' "${X[@]}" .
# 5d. The client-IP derivation every per-IP bound (throttles, daily budgets) is only as good as.
rg -n --pcre2 '\btrust_?[Pp]roxy\b|trust proxy|ProxyFix|TRUSTED_PROXIES|ForwardedHeaders\w*|set_real_ip_from|real_ip_header|use-forwarded-headers|TRUST_PROXY\w*' "${X[@]}" .

# 6a. Secret-shaped values on a log call (§6): Node, Django/Flask, Go, Spring, Rails, Laravel loggers.
#     No \b before the names: `accessToken=${…}` must match.
rg -n -i --pcre2 '(console\.(log|info|warn|error|debug)|\blogger\.\w+|\blog\.\w+|logging\.\w+|Rails\.logger\.\w+|\bslog\.\w+|fmt\.Print\w*|\bprint\(|System\.out\.print\w*|error_log|Log::\w+|process\.std(out|err)\.write)\s*\(?[^\n]*(req\.(body|headers|cookies)|request\.(body|headers|data|json|form|POST|META|cookies)|params\.inspect|authorization|password|passwd|secret|token|api_?key|otp|cvv|card_?number|ssn|session_?id)' "${X[@]}" .
# 6b. Whole request objects folded into a log record or an error-tracker event.
rg -n --pcre2 '\b(body|headers|payload|params|data|cookies)\s*:\s*(req|request|ctx\.request)\.(body|headers|cookies|query)\b|JSON\.stringify\(\s*(req|request)\.(body|headers)|httputil\.DumpRequest|setInclude(Payload|Headers)\(\s*true|log-request-details\s*[:=]\s*true|sendDefaultPii\s*:\s*true|send_default_pii\s*=\s*True' "${X[@]}" .
# 6c. Redaction present at all? A logger in 6a/6b with no 6c primitive is unredacted. Present is not complete: 6d.
rg -n --pcre2 'redact\s*:|redactPaths|filter_parameters|filter_attributes|sensitive_variables|sensitive_post_parameters|SafeExceptionReporterFilter|ReplaceAttr|LogValue\(\)|MaskingJsonGeneratorDecorator|RewritePolicy|pushProcessor|SensitiveParameter|beforeSend|before_send|maskAllInputs|maskAllText' "${X[@]}" .
# 6d. Every credential header NAME the app accepts (guards, webhook-verifier registries, API-key headers), deduped.
#     Diff it against the redact list 6c points at — and against any second redactor (a webhook ledger, an audit or
#     trace scrubber). Add 7b's query / path secrets. A name the log list lacks is a candidate.
rg -o -N --no-filename --pcre2 '["\x27`](?i:x-[a-z0-9-]*(token|key|secret|signature|sig|auth|hmac)[a-z0-9-]*|([a-z0-9]+-)*authorization(-[a-z0-9]+)*|[a-z0-9]+(-[a-z0-9]+)*-(token|api-?key|secret|signature|hmac))["\x27`]' "${X[@]}" . | tr 'A-Z' 'a-z' | sort -u
#     The QUERY credential names an app declares in config objects (a webhook-verifier registry, a provider table:
#     `tokenParam: 'hub.verify_token'`, `callbackToken: { query: 't' }`, `{ from: 'query', key: 'token' }`) — 7b's
#     `req.query` / `@Query(` shapes never see them. Each value goes into the same diff against the redact list.
rg -o -N --no-filename --pcre2 "\b\w*(?i:token|secret|key|sig|signature|auth)\w*(Param|Query|QueryParam|Field)\s*:\s*['\"\x60][\w.-]+['\"\x60]|\b(query|queryParam|param|searchParam)\s*:\s*['\"\x60][\w.-]+['\"\x60]|\bfrom\s*:\s*['\"\x60]query['\"\x60]\s*,\s*(key|name|param)\s*:\s*['\"\x60][\w.-]+['\"\x60]" "${X[@]}" . | sort -u
# 6e. A payload serialized INTO a log call, multi-line, outbound vendor bodies included. A secret-only deny-list
#     (`redact(body, secretFields)`) over a body of names, phones and addresses is still a PII sink.
rg -n -U --pcre2 '\b(console|logger|log|logging|Log)\s*\.\s*(log|info|debug|warn|error|verbose|trace)\s*\([^;]{0,240}?\b(JSON\.stringify|json\.dumps|inspect|util\.format|to_json|Marshal)\s*\(' "${X[@]}" .
# 6f. Traces are a log sink: span attributes, exception events and status messages (`recordException`) carry the same
#     error text and URLs. A URL scrub at span start does not reach events and status set later.
rg -n --pcre2 '\b(getNodeAutoInstrumentations|NodeSDK|registerInstrumentations|\w*SpanProcessor|\w*SpanExporter|recordException|TracerProvider|\w+Instrumentor|dd-trace|ddtrace)\b|opentelemetry-instrument|-javaagent:\S*opentelemetry' "${X[@]}" .
# 6g. The edge access log is a second sink for every URL and header secret (§6, §7): Caddy's JSON log writes
#     `request.uri` and `request.headers`, nginx's `$request` the full query. Then the collector that ships it, and retention.
rg -n --pcre2 '^\s*(access_log|log_format)\b|^\s*log\s*\{|^\s*format\s+(json|console|filter)\b|\b(accessLog|access-log|enable-access-log|log-format-upstream|CustomLog|LogFormat)\b|\bloki\.(write|source\.\w+)|\b(promtail|fluent-?bit|fluentd|otelcol)\b|\[sinks\.|retention_period' -g '*Caddyfile*' -g '*.conf' -g '*.y*ml' -g '*.toml' -g '*.alloy' -g '*.river' "${X[@]}" .
# 6h. Personal data handed to a log call by field name (§6, PII sink): `{ name: …, phone, address }`, `"email", u.Email`,
#     `email=${…}`, `${address}`, `order.customerPhone`. Keys are anchored to `{ , (`, so prose ("send email: …") and
#     `queueName: 'email'` stay out; a bare `name` key is not listed (measured: 9 of 9 were metric, job or error names).
rg -n -U --pcre2 '\b(console|logger|log|logging|Log|slog)\s*\.\s*(log|info|debug|warn|warning|error|verbose|trace|Info|Debug|Warn|Error)\s*\([^;]{0,240}?(?:(?<!\$)[{,(]\s*["\x27]?(?:first_?[Nn]ame|last_?[Nn]ame|full_?[Nn]ame|customer_?[Nn]ame|phone|phone_?[Nn]umber|mobile|address|street|post_?code|zip_?code|e_?mail|dob|date_?of_?birth|birth_?date)["\x27]?\s*[:=,}]|\b(?:phone|mobile|address|e_?mail|dob)=(?:\$\{|%|\{)|\$\{\s*(?:phone|mobile|address|e_?mail|dob)\s*\}|\.(?:e_?mail|phone(?:_?[Nn]umber)?|mobile|dob|date_?of_?birth|(?:first|last|full|customer)_?[Nn]ame|customer_?(?:[Pp]hone|[Ee]mail)|(?:delivery|billing|shipping|home)_?[Aa]ddress)\b(?!\s*\())' "${X[@]}" .

# 6i. AI lane (LG-1, routed here by ai-engineering llm-gateway-audit §R and security llm-trust-scan): log calls inside the
#     files that call a model. The prompt input and the completion rarely carry a telling name (`notes`, `text`), so the
#     lane is the FILE, not the variable. LLM_FILES = llm-trust-scan's `llm-files.txt` when it ran; else the inline list.
LLMF="${LLM_FILES:-$(mktemp "${TMPDIR:-/tmp}/de-llm.XXXXXX")}"
[ -s "$LLMF" ] || rg -l --pcre2 '/chat/completions\b|/v1/responses\b|:generateContent\b|\b(?:max_completion_tokens|tool_choice|toolChoice|response_format|stream_options)\b\s*["\x27]?\s*[:=]|(?:\bfrom\s+|\brequire\(\s*|\bimport\(\s*)["\x27](?:openai|@anthropic-ai/sdk|ai|@ai-sdk/[\w-]+|@langchain/[\w-]+|@google/genai|@openai/agents)["\x27]|^\s*(?:from|import)\s+(?:openai|anthropic|langchain\w*|litellm)\b|\brole\s*:\s*["\x27](?:system|developer)["\x27]|\b\w*(?:complete|chat|generate|invoke)\w*\(\s*(?:system|messages|prompt)\s*=|\bmessages\s*[:=]\s*\[\s*\{\s*["\x27]?role["\x27]?\s*[:=]' -g '*.{ts,tsx,mts,js,jsx,mjs,py,go,rb,java,kt,cs,php}' "${X[@]}" . > "$LLMF"
[ -s "$LLMF" ] && tr '\n' '\0' < "$LLMF" | xargs -0 rg -n --pcre2 '\b(console|logger|log|logging|Log|slog|this\.logger)\s*\.\s*(log|info|debug|warn|warning|error|verbose|trace|Info|Debug|Warn|Error)\s*\(' || echo "6i: 0 LLM files"
# 7. Credentials in URLs, and the Referrer-Policy that decides how far they travel (§7).
rg -n -i --pcre2 '[?&](access_?token|id_?token|refresh_?token|token|api_?key|apikey|secret|password|passwd|pwd|session_?id|sid|otp|ssn)=' "${X[@]}" .
rg -n --pcre2 '(req\.query|request\.(args|GET|query_params)|params\[|@RequestParam|c\.Query\(|\$_GET\[|URL\.Query\(\)\.Get\()[^\n]*(token|api_?key|apiKey|secret|password|session|otp)|@Query\(\s*["\x27]\w*(token|key|secret|sig|signature|password|otp)|@Param\(\s*["\x27]\w*(secret|token)' "${X[@]}" .
rg -n 'Referrer-Policy|referrerPolicy|referrer_policy|SECURE_REFERRER_POLICY|ReferrerPolicy' "${X[@]}" .

# 8. Fingerprinting: what is set, and every app that must remove X-Powered-By (§8).
rg -n --pcre2 '(?i:x-powered-by)|poweredBy|expose_php|server\.server-header|\bX-Runtime\b|X-Debug-Token|helmet\(|hidePoweredBy|(set|header|setHeader)\(\s*["\x27]Server["\x27]' "${X[@]}" .
rg -n --pcre2 '\bexpress\(\)|\bfastify\(|new\s+Koa\(|NestFactory\.create|new\s+(Fastify|Express)Adapter' "${X[@]}" .

# 9. Cache policy on responses that carry per-user data (§9). Case-sensitive `Vary`: `-i` matched SQL `character varying`.
rg -n --pcre2 '(?i:cache-control|cache_control)|cacheControl|cache_page|never_cache|@Cacheable|expires_in|fresh_when|s-maxage|max-age|\brevalidate\s*[:=]|unstable_cache|force-cache|force-static|\b(?i:etag)\b|\bVary\b' "${X[@]}" .

# 10a. Internal files COMMITTED under a served directory (§10). git ls-files = what ships.
#      A mount from 10b whose directory is not in this name list: add it to the alternation.
git ls-files | rg -i --pcre2 '(^|/)(public|static|staticfiles|www|wwwroot|webroot|htdocs|assets|media|uploads)/(.*/)?(\.env(\.[^/]*)?$|\.DS_Store$|[^/]*\.(bak|old|orig|swp|tmp|sql|sqlite3?|db|dump|log|pem|key|p12|pfx|map|zip|tar|gz|tgz|7z|rar)$|[^/]*~$|\.htpasswd$|web\.config$|phpinfo\.php$|(composer|package)(-lock)?\.json$)' \
  | rg -v --pcre2 '(^|/)packages/[^/]+/(uploads|assets|media)/(.*/)?package\.json$'   # a workspace subpath export, not a served dir
# 10b. Every static mount. Flag one rooted at the project root / cwd / ".", or one that allows dotfiles.
rg -n --pcre2 'express\.static\(|serveStatic\(|useStaticAssets\(|ServeStaticModule|@fastify/static|koa-static|StaticFiles\(|static_folder|http\.FileServer|static-locations|dotfiles\s*:\s*["\x27]allow' "${X[@]}" .
# 10c. A deploy that copies the whole checkout (with .git/) into a web root.
rg -n --pcre2 '^\s*(COPY|ADD)\s+\.\s+/(var/www|usr/share/nginx/html|srv/www|app/public)' -g 'Dockerfile*' "${X[@]}" .

# 11. GraphQL servers and their disclosure switches (§11).
rg -n --pcre2 'ApolloServer|graphqlHTTP|createYoga|GraphQLModule\.forRoot|mercurius|graphene|strawberry|ariadne|gqlgen|spring\.graphql|GraphQL::Schema|introspection\s*[:=]|graphiql\s*[:=]|playground\s*[:=]|ApolloServerPluginLandingPage|NoSchemaIntrospectionCustomRule|DisableIntrospection|blockFieldSuggestions|hideSchemaDetailsFromClientErrors' "${X[@]}" .

# 12. Error text that names the failing check, or forwards an upstream's body (§12). Matches the
#     value placed into a body / field (`error: err.name`), not a branch on it (`if (err.code === …)`).
rg -n --pcre2 '(:|=>|=|\()\s*\$?(err|e|error|ex|exc)(\.|->)(name|code|errno|constraint|detail|table|column)\b(?!\s*(===?|!==?|==|!=))|\b(err|e|error)\.response\.(data|body)\b' "${X[@]}" . \
  | rg -v --pcre2 '\b(log|logger|console|logging|slog|Log|Sentry)\s*(\.|::)\s*\w+\s*\(|process\.std(out|err)\.write\('

# 13a. A secret compared with short-circuiting equality (§13), including names with no keyword (`stored !== codeHash`).
#      Null checks and Redis lock-ownership checks (`held === token`) filtered out. Browser code is out: the attacker owns
#      the clock there, and its cache-key compares (`token === lastToken`) were 16 of 26 hits on a real monorepo. A web app
#      that emits SERVER code as a string (an Apps Script body) needs one run without the two client globs.
rg -n -i --pcre2 '(token|secret|signature|sig(?!n)|hmac|digest|api_?key|otp|nonce|csrf)\w*["\x27]?\]?\)?\s*(===?|!==?|!=)\s*[\w$@]|(===?|!==?|!=)\s*[\w$@.>\[\]-]*(token|secret|signature|sig(?!n)|hmac|digest|api_?key|otp|nonce|csrf)|\b(stored|expected|computed|presented|given)\w*\s*(===?|!==?)\s*\w|\.equals\(\s*\w*(token|secret|signature|hmac|digest|key|otp)|(token|secret|signature|key)\w*\.equals\(|bytes\.Equal\(|strcmp\(' "${X[@]}" -g '!**/*.{tsx,jsx,vue,svelte}' -g '!**/{web,frontend,client}/src/**' . \
  | rg -v --pcre2 '(===?|!==?|!=)\s*(null|undefined|None|nil|true|false|""|\x27\x27)(\W|$)|\bheld\s*(===?|!==?)'
# 13b. The constant-time primitive, where one exists.
rg -n 'timingSafeEqual|compare_digest|constant_time_compare|ConstantTimeCompare|hmac\.Equal|MessageDigest\.isEqual|secure_compare|hash_equals' "${X[@]}" .
```

A finding is a grep hit **plus** a read of the surrounding function and the production config that governs it. The greps narrow the search. They do not decide.

Measured on a real repo (a NestJS-on-Fastify monorepo with MikroORM) before and after the exclusion array and the anchors: grep 5c went from 1,937 lines to 109, grep 3 from 529 to 30, grep 9 from 240 to 19, grep 1b from 351 to 142 and grep 13a from 58 to 17, while 4b, 4d and 5b gained the ORM-entity, `em.findOne` and hasher shapes they had missed. Every seeded defect of the benchmark fixture is still hit, and its debug-route defect, missed by every grep before, now is.

Grep 6h (2026-10-10): 1 hit on `benchmarks/fixtures/obs-defects` (its dispatch adapter's `{ name, phone, address }` at `info`, which no other grep printed), 0 on the other 15 fixtures and on a seeded observability sample. On ten real trees, read-only, it printed 47 hits: 45 read as customer or admin emails, phones, delivery addresses and full names at `info`/`log`/`debug` level, 2 refuted on the read (a boolean `email: !!email`, a phone masked to its first six digits); the NestJS monorepo above had 6 (one email in a message, one delivery address logged by five verification paths). With a bare `name` key it printed 56: the 9 extra were metric, ad-set, cart-item and `error.name` names, so that key is left out.

## Scans for

Severity measures what leaks, not which class it falls in. A stack trace that prints a DB connection string is high. One that prints a file path is low.

### 1. Raw exception content in the HTTP response — A10 · CWE-209

The global handler, an exception filter or a per-route `catch` writes `err.message`, `err.stack`, a SQL/ORM error (`sqlMessage`, `original`, a constraint name) or `str(e)` into the body. The client learns table and column names, file paths, library versions and sometimes the query itself, which is how an injection gets tuned.

```
BAD:   app.use((err, req, res, next) => res.status(500).json({ message: err.message, stack: err.stack }))
       return jsonify(error=str(e)), 500          |   ResponseEntity.status(500).body(e.getMessage())
       http.Error(w, err.Error(), 500)            |   response()->json(['error' => $e->getMessage()], 500)
GOOD:  log the full error server-side with the request id; answer
       { "error": "internal_error", "requestId": "<id>" }. Only typed domain errors (4xx) map to client-safe text.
```

Grep 1a is the universe, and every handler in it gets read: is any field of the exception object copied into the response? Grep 1b lists every exception internal outside a log call. Follow each value to where it lands. Also check a 4xx path that forwards `err.message` from a library, because validation libraries and ORMs put internal names there.

**Persisted, then served.** The response is not the only exit. Grep 1c finds a catch-all that copies raw error text into a field before the global handler sees it: a bulk result row, a job queue's `lastError`, an attempt note. That field is served later, often to other members (an export queue is shown to every exporter). A driver error there carries the statement with its bound values, so one member reads another's search terms. The fix is the project's own split: a typed domain error contributes its message key, anything else becomes `errors.internal` with the detail logged. In an i18n'd app, also check whether exception text travels in translation `args` into a template placeholder. Measured on a real repo: grep 1b returned 351 lines with 3 real sinks; grep 1c returned 23 with all 3. Re-measured 2026-10-15 on a real NestJS + React monorepo: 1c held 2 of 4 sinks, because one copied `error.message.slice(0, 800)` with no `instanceof` and one went through `const errorText = (e) => …` called as `error: errorText(e)`; with the two new alternations it prints 35 lines holding all 4 (fixtures 4 → 7, the seeded filter's `message: err.message` among them).

**Severity:** medium. High when the text can carry secrets (connection strings, a query with bound values, an upstream response).

### 2. Framework debug / verbose-error mode reachable in production — A02 · CWE-489 · CWE-215

A switch from § Adapt to the codebase is on in production, or defaults to on when its variable is unset. Some switches are an RCE console, not a leak: the Werkzeug debugger (Flask `debug=True`), `better_errors` / `web-console` outside the development group, Ignition with `APP_DEBUG=true`, and the Spring H2 console.

```
BAD:   DEBUG = os.environ.get("DEBUG", "True") == "True"     # unset in prod → Django debug pages with settings + SQL
       server.error.include-stacktrace: on_param             # any client appends ?trace=true
       config.consider_all_requests_local = true             # in production.rb
       Express with no 4-arg handler + NODE_ENV unset in the image → finalhandler prints the stack
GOOD:  default OFF, turned on only by an explicit dev setting; NODE_ENV=production in the image;
       include-stacktrace: never; consider_all_requests_local = false
```

Grep 2a finds the switch. Grep 2b shows what the deploy sets. A hit in a dev-only file (`development.rb`, `settings/dev.py`, `application-dev.yml`, `.env.example`) is not a finding unless production loads that file. **Severity:** critical for an interactive console (code execution). High for a debug page (settings, env, SQL). Medium for stack-on-param or message inclusion.

### 3. Debug, admin, metrics and docs endpoints reachable without auth — A02 · CWE-200 · CWE-306

Framework-shipped and ops surfaces mounted on the public listener with no auth gate. Examples: Spring `/actuator/*` (`heapdump` and `env` with `show-values: always` leak live secrets and sessions, and `jolokia` can act), Go `net/http/pprof` and `expvar` on `DefaultServeMux`, `/__debug__` / django-debug-toolbar, Symfony `/_profiler`, Laravel Telescope / Horizon / Debugbar, Rails `Sidekiq::Web` with no route constraint, `bull-board`, `express-status-monitor`, `phpinfo()`, `/metrics`, `/health` with `show-details: always`, and Swagger / ReDoc / `/api-docs` / FastAPI's default `/docs` + `/openapi.json`. Under `/.well-known/`, only the registered public documents belong (`security.txt`, `openid-configuration`, app-association files). A generic static mount there, or an internal file in it, is exposure.

```
BAD:   import _ "net/http/pprof"  + http.ListenAndServe(":8080", nil)     // pprof on the public mux
       management.endpoints.web.exposure.include: "*"
       app = FastAPI()                                                     // /docs, /redoc, /openapi.json public
GOOD:  ops endpoints on a separate internal port (Spring Boot management.server.port, a private Go mux) or behind the
       admin guard; exposure.include: health,info; FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
       in prod, or docs behind auth
```

Read each hit for three things: the listener it is mounted on, the guard in front of it, and the env gate that disables it in production. Business admin routes missing a role check are BFLA. Hand those to `@api-security-reviewer` API5 and `logic-race-scan`'s role matrix. **Severity:** critical for heapdump / env / jolokia / an unauthenticated admin panel. High for pprof or Telescope. Medium for `phpinfo`, a detailed health check, or docs that list internal routes. Low for a public spec of an already-public API.

### 4. Over-returning responses — A01 · API3:2023 · CWE-213

The handler returns the ORM entity, the raw row or `SELECT *` instead of a projection. The response then carries the password hash, reset or verification tokens, MFA secrets, internal flags, cost fields, or other users' emails on a list endpoint. A list endpoint that returns fields the UI never renders is the same defect, found by comparing the payload with what the client reads.

```
BAD:   res.json(user)          |  render json: @user         |  fields = '__all__'
       SELECT * FROM users WHERE org_id = $1   → list endpoint ships password_hash for every member
GOOD:  a response DTO / serializer naming client-safe fields: Nest ClassSerializerInterceptor + @Exclude(),
       Prisma select/omit, DRF explicit fields + write_only, Pydantic response_model, Go `json:"-"`,
       Jackson @JsonIgnore / record DTOs, Rails as_json(only:) / a serializer, Laravel $hidden / API Resources
```

Grep 4a lists the raw returns. Greps 4b and 4c are a set difference: a sensitive field declared on a model that has no exclusion primitive, and that some handler serializes whole, is a finding. Grep 4d lists every read of such a model, and each one is followed to the response. Prisma's `include` adds relations *on top of* every scalar, so `findUnique({ where, include: { products } })` with no `select` / `omit` returns the password hash too. Read the query as well, because an explicit column list in SQL is a projection. MikroORM's exclusion primitives are `@Property({ hidden: true })`, `lazy: true` and a custom `serializer`. **Projection-first code** (CQRS read adapters, `fields: […]`, view mappers) never hands an entity to a controller, so 4c is empty and the app can still be clean: follow the controllers' return types instead of the 4b − 4c set difference: grep 4e lists the controllers typed `Promise<unknown>` and the credential columns selected in files that also pass rows through an identity projection. Measured 2026-10-15 on a real NestJS + React monorepo with 483 `toItem: (r) => r` lines: 4e printed 33 loosely typed controller returns and 7 `fields:` lists selecting a hash or encrypted column, a set one reader can finish. Measured on a real repo: 4b matched none of 129 `*.orm-entity.ts` files before `*entit*` joined its globs, and 4d matched none of 25 `em.findOne(User, …)` reads before the `em.` shape. Hand the DTO architecture and mass assignment to `@api-security-reviewer` API3, and the personal-data grading to `@data-privacy-reviewer`. Report the line once. **Severity:** high for credentials, tokens or secrets, or other users' PII (critical on an unauthenticated route). Medium for internal flags or business fields.

### 5. Account and resource enumeration — A07 · CWE-204 · CWE-208

Login, password reset, signup, invite or OTP answers an unknown account differently from a known one. The difference can be the message ("User not found" vs "Incorrect password"), the status (404 vs 401), or the timing: the unknown-user branch returns before the password hash runs, so it answers several milliseconds faster. On resources, a 403 for "exists but not yours" against a 404 for "does not exist" confirms which ids exist.

```
BAD:   if (!user) return res.status(404).json({ error: 'User not found' })   // and no hash work on this path
GOOD:  same status + same body ("invalid credentials") on every failure, and the unknown-user branch verifies
       against a fixed dummy hash so both paths cost the same; reset always answers 200 "if an account exists…"
       with the email send queued; signup emails the existing owner instead of saying "already registered"
```

Grep 5a finds the messages and grep 5b the verify sites. Read the branch order. Two shapes no message grep shows:
- **A check that runs after the lookup.** A password-floor or field validation evaluated AFTER the existence check answers 422 for a new address and 409 for a taken one, with zero side effects: send a deliberately weak password and read the status.
- **A global identity table behind a per-tenant or public form.** Users who span workspaces live in one table, so a sign-up or "add member" form on any workspace probes all of them.

For grep 5c, read whether the object was loaded before the ownership check. If it was, answer 404 where the project's convention allows. Every per-IP bound on these routes (throttle, daily budget) is only as good as the client IP: read grep 5d's `trustProxy` / hop count against the real proxy chain, and state the bound with that caveat. `@auth-reviewer` § Account enumeration owns this inside the auth ceremony review. This detector sweeps every surface, including invite and resource endpoints that no auth review reaches. Hand auth-path hits to it rather than re-deriving. **Severity:** medium on login, reset or signup (it feeds credential stuffing). Low for 403 vs 404 unless the id or the existence itself is sensitive.

### 6. Secrets, credentials and PII written to logs — A09 · CWE-532

A logger or `console.log` receives a password, token, OTP, `Authorization` or `Cookie` header, card data, or a whole request or user object. Logs are retained, shipped to third parties, and read by more people than the database is. The fixture-proven shape is a request logger that folds `body: req.body` into every line. Other shapes are Rails `params.inspect` logged by hand (it bypasses `filter_parameters`), Spring `spring.mvc.log-request-details=true` / `CommonsRequestLoggingFilter` with headers or payload, Go `httputil.DumpRequest`, an error tracker with `sendDefaultPii: true` and no `beforeSend` scrub, and session replay with input masking turned off.

```
BAD:   logger.info({ body: req.body, headers: req.headers }, 'login')
       console.log('issued token', token)
GOOD:  log ids, not objects; redaction configured in the logger itself
       pino({ redact: ['req.headers.authorization', 'req.headers.cookie', '*.password', '*.token', '*.otp'] })
```

Greps 6a, 6b and 6h are the sinks: 6a is secret-shaped, 6h is personal data by field name (`phone`, `address`, `email`, `dob`, a customer's name), read per hit for whose value it is — a masked value (`phone.slice(0, 6) + '****'`) or a boolean (`email: !!email`) is refuted on the read. Grep 6c is the set difference: if no redaction primitive exists, every whole-object hit is a finding. PII here is reported as a sink. Hand the lawful-basis and erasure reach to `@data-privacy-reviewer`. Forged log lines (CWE-117) are `injection-scan`'s.

**Present is not complete.** Grep 6c proves a redactor exists, not that it covers what the app accepts. Grep 6d lists every credential header name the app accepts; add 7b's query and path secrets. Every accepted name missing from the log's redact list is a candidate: the set difference is the detector, as 4b − 4c is for § 4. An app with two redactors usually has them drift — the request log's path list beside a webhook ledger's or audit trail's policy — so diff them against each other. A body signature (`x-…-signature`) only replays its own body; a bearer-style header token is the high case. Measured on a real repo: the log list named 6 headers, the app accepted 5 more carrier-token headers its ledger redactor already knew, and all 5 were logged whole at `info`.

Three sinks sit outside the request log:
- **A payload serialized into the message** (grep 6e). `JSON.stringify(body)` inside the log string hides the fields from `redact`, which walks the log object. A vendor adapter that logs its outbound body at `info` behind a secret-only deny-list still ships every name, phone and address it dispatches.
- **Traces** (grep 6f). Span attributes, exception events and `status.message` carry the same driver error text and URLs as the log line. A URL scrub in `onStart` does not reach events or a status set later. The scrub belongs in a wrapping exporter, over `exception.message`, `exception.stacktrace` and `status.message` too.
- **The edge access log** (grep 6g). The reverse proxy logs before the app runs. Caddy's JSON access log carries `request.uri` with its query and every `request.headers` entry, redacting only `Cookie`, `Set-Cookie`, `Authorization` and `Proxy-Authorization` by default. nginx's `$request` and ingress-nginx log the full query. Every secret the app redacts must be filtered at the edge too (Caddy `format filter`, an nginx `log_format` without `$request` / `$args`), or that route must not be logged. Read the collector config (Alloy, Promtail, Fluent Bit, Vector) for which namespaces ship, who can query them, and the retention. `[report-flagged]` until a query of the log store shows the value.

**The AI lane** (grep 6i; LG-1, the class ai-engineering routes here). In a file that calls a model, read every log call for whether an argument holds the prompt input (the user's text, retrieved documents, tool results) or the completion. Content is the finding — whoever can read the log can read every conversation, including other tenants'; a length, a hash, token counts, a model id or a finish reason are not content. A whole-body request logger (6b) that covers the AI routes is the same finding. Tracing content capture (span attributes, exporter capture flags) is `llm-trust-scan` §5, not this lane. Measured 2026-10-19: 1 hit on `benchmarks/fixtures/llm-assist` (its seeded answer log), 0 on the other 31 fixtures. **Severity:** medium; high when the text carries credentials or another tenant's data.

**Severity:** high for credentials, tokens, session cookies, signed-link `sig`, or card number / CVV. Medium for PII.

### 7. Credentials and tokens in URLs — A07 · CWE-598

A token, API key, password, session id or OTP travels in a query string. URLs are written to access logs (morgan's default formats included), proxy and CDN logs, browser history, and the `Referer` sent to every third-party resource on the landing page.

```
BAD:   GET /api/export?api_key=…     |   /verify?token=…&email=… landing page that loads analytics
GOOD:  credentials in the Authorization header or a POST body. A one-time link token is single-use and
       short-TTL, and its landing page sets Referrer-Policy: no-referrer, exchanges the token immediately
       and strips it from the address bar.
```

Grep 7's first two lines find the producer and consumer; the second includes NestJS `@Query('token')` and path secrets (`@Param('secret')`). The third shows whether a Referrer-Policy exists at all. A query token or path secret forced by a partner protocol is not this finding, but it is still written by every access log in front of the app: that half is § 6's edge-log sink (grep 6g). An API key in a query string is also `@api-security-reviewer` API2. Credit the line once. PII in URLs belongs to `@data-privacy-reviewer` § PII in URLs / query-strings / error messages. **Severity:** medium for long-lived credentials or session ids. Low for single-use, short-TTL tokens.

### 8. Fingerprinting headers and banners — A02 · CWE-497

`X-Powered-By: Express` / `Next.js` / `PHP/8.x`, `Server` with a version, `X-Runtime`, or `X-Debug-Token`. These hand the attacker the exact CVE list to try.

```
BAD:   const app = express()                 // no app.disable('x-powered-by'), no helmet()
       expose_php = On   |   next.config without poweredByHeader: false
GOOD:  app.disable('x-powered-by') or helmet(); poweredByHeader: false; expose_php = Off
```

The second line of grep 8 lists every app instance. One that neither disables the header nor mounts helmet is the finding. Fastify, and NestJS on `FastifyAdapter`, send no `X-Powered-By` by default; Express and Nest's default Express adapter do. Report it once per app, not per route. Proxy banners (`server_tokens`, `ServerTokens`) are `iac-scan`'s. **Severity:** low. Never inflate it: removing a banner raises attacker cost, it does not close a hole.

### 9. Private responses cacheable — A02 · CWE-524 · CWE-525

An authenticated, per-user response can be stored by a shared cache or the browser:
- `Cache-Control: public` or `s-maxage` on an authed route.
- No `no-store` on authenticated JSON.
- Django `@cache_page` on a view that reads `request.user` without `Vary: Cookie`.
- A Next.js page or `fetch` that reads the session yet is `force-static`, uses `revalidate` or `force-cache`, or sits in `unstable_cache` with no user id in the key.
- A server-side cache key that omits the principal.
- A strong ETag on a secret-bearing response (key reveal, recovery codes). The validator keeps a stable fingerprint of the secret in every cache and log that records it.

```
BAD:   app.get('/me', auth, (req, res) => { res.set('Cache-Control', 'public, max-age=300'); res.json(req.user) })
GOOD:  Cache-Control: no-store on authenticated API responses (one middleware for the API prefix);
       private, no-store on per-user HTML; no ETag on secret-bearing responses
```

Read each grep 9 hit against the auth guard on the same route. An authenticated API with no `no-store` anywhere is one finding at the middleware that should set it. CDN and edge cache rules are `iac-scan`'s. Server-side cache-key design is the backend `caching-strategy` pattern's when the backend pack is installed (`backend/ai-patterns/caching-strategy.md` § What NOT to cache). Without that pack, this detector's BAD/GOOD is the contract. **Severity:** high when a shared cache can serve one user's response to another. Low or medium for browser-only storage.

### 10. Internal files reachable from a served directory — A02 · CWE-538 · CWE-527 · CWE-530

Files that must never be served are committed under a served directory: `.env`, `*.sql` dumps, `*.bak` / `*.old` / `*~` backups, `*.map` source maps, `.DS_Store`, private keys, archives, `package.json`. A static mount can also point at the project root (Express `express.static(__dirname)`, or Go `http.Dir(".")`, which also serves dotfiles), or set `dotfiles: 'allow'`. A `.git/` directory is never in `git ls-files`. It reaches a web root through a deploy that copies the checkout (`COPY . /var/www/html`), so check grep 10c.

```
BAD:   public/backup.sql   |   public/.env   |   http.FileServer(http.Dir("."))   |   express.static(__dirname)
GOOD:  serve only a dedicated build-output directory; dotfiles ignored; backups and dumps never under it;
       the image copies build output, not the checkout
```

Grep 10a lists committed files and grep 10b the mounts. A `.env` or dump found here is **also** a `secret-scan-method` finding. Rotation and the history scrub are that skill's, and this skill reports the reachability. Source maps that the bundler emits into the production build are `xss-scan`'s. Upload storage inside the web root is `file-access-scan`'s. **Severity:** critical for `.git/`, `.env`, dumps or keys. High for server source served through a root mount. Medium for committed source maps. Low for `.DS_Store`.

### 11. GraphQL schema disclosure — A02 · CWE-200

Introspection is enabled in production, GraphiQL or Playground is served, or field suggestions ("Did you mean `adminDeleteUser`?") are on. Suggestions let a tool rebuild the schema even with introspection off.

```
BAD:   new ApolloServer({ typeDefs, resolvers, introspection: true })   |   GraphQLModule.forRoot({ playground: true })
GOOD:  introspection and the landing page off in production; suggestions blocked (graphql-armor
       blockFieldSuggestions, or the server's hide-schema-details option); persisted queries where possible
```

Schema hiding is defense in depth, never authorization. A resolver without a field-level check is still `@api-security-reviewer`'s finding. Depth, complexity and batching limits are in that agent's GraphQL checklist too. This detector is the disclosure sweep across every GraphQL server in the repo. **Severity:** low. Medium when the schema exposes admin or internal mutations.

### 12. Error codes that disclose decision state — A10 · CWE-209 · CWE-204

Hand-written errors can tell the attacker which check failed. Examples: `err.name` from token verification (`JsonWebTokenError` vs `TokenExpiredError` vs a wrong algorithm), a DB constraint or column name in a 409, or a lockout message that confirms the password was right. An upstream's error body forwarded verbatim (`res.status(e.response.status).json(e.response.data)`) leaks the partner's internals and sometimes the request it was sent, credentials included.

```
BAD:   catch (e) { return res.status(401).json({ error: e.name }) }    |   .json(err.response.data)
GOOD:  one client code per class: invalid_token (RFC 6750 § 3.1) for every verification failure, with
       the reason logged; upstream failures → 502 upstream_unavailable, with the upstream body logged
```

Grep 12 finds the shapes. Read whether the distinguishing value reaches the client. **Severity:** medium for forwarded upstream bodies or auth-step oracles. Low for constraint or column names.

### 13. Timing-unsafe secret comparison — A07 (token / API key / OTP) · A08 (webhook signature) · CWE-208

An HMAC signature, API key, reset token, OTP or CSRF token is compared with `===`, `==`, `.equals`, `strcmp` or `bytes.Equal`. These stop at the first differing byte, so the response time leaks how much of a guess is right.

```
BAD:   if (req.headers['x-signature'] === expected)     |   apiKey.equals(provided)    |   if sig == expected
GOOD:  the stack's constant-time compare from § Adapt to the codebase, on equal-length inputs. Compare two HMAC
       digests, or hash both sides first, so a length mismatch neither throws nor short-circuits.
```

Grep 13a lists the candidates (null checks are filtered out). Grep 13b shows whether the primitive is used anywhere: a repo that has it in one webhook and `===` in another is the common shape. Passwords go through the hash library's verify (`bcrypt.compare`, `password_verify`), never a compare. **Severity:** medium. High on a webhook signature or an admin API key.

## Output

```
data-exposure-scan — <scope: diff | whole repo>   roots: <dirs scanned>

Findings: 4

1. src/app.js:46                                        [report-with-fix]  high · A10 · CWE-209
   Global error handler returns err.message + err.stack on every 500. A failed query echoes the SQL text.
   Fix: log the error with the request id; respond { error: "internal_error", requestId }.

2. config/application.yml:9                             [report-flagged]   critical · A02 · CWE-200
   management.endpoints.web.exposure.include: "*" puts /actuator/heapdump on the public port.
   Runtime fact to confirm: management.server.port is unset in the prod profile (/security-live-scan probe).
   Fix: exposure.include: health,info; management.server.port on an internal listener.

3. src/http/access-logger.js:17                         [report-with-fix]  high · A09 · CWE-532
   Request logger writes body: req.body on every request. Login and reset bodies carry passwords and OTPs.
   No redaction primitive in the repo (grep 6c empty).
   Fix: drop the body; log route + status + actor id; add pino redact paths for any field kept.

4. src/http/psp-callback.js:33                          [report-with-fix]  high · A08 · CWE-208
   req.headers['x-signature'] === expected. Short-circuit compare on the HMAC.
   Fix: crypto.timingSafeEqual(Buffer.from(sig, 'hex'), Buffer.from(expected, 'hex')) after a length check.

Class coverage
  §1  raw exception in response        checked (6 hits → 1 finding)
  §2  debug / verbose-error mode       checked (2 hits → 0 findings)
  §3  debug / admin / metrics / docs   checked (3 hits → 1 finding)
  §4  over-returning responses         checked (9 hits → 0 findings)
  §5  account / resource enumeration   checked (4 hits → 0 findings)
  §6  secrets / PII in logs            checked (3 hits → 1 finding)
  §7  credentials in URLs              checked (0 hits → 0 findings)
  §8  fingerprinting headers           checked (1 hit → 0 findings)
  §9  cacheable private responses      checked (2 hits → 0 findings)
  §10 internal files served            checked (0 hits → 0 findings)
  §11 GraphQL schema disclosure        N/A (no GraphQL server in repo)
  §12 decision-state error codes       checked (1 hit → 0 findings)
  §13 timing-unsafe compare            checked (2 hits → 1 finding)
```

`[report-with-fix]` means the sink, the failing condition and the fix are all established from the repo. `[report-flagged]` means the code is established but exploitability turns on a runtime fact the repo cannot show: the prod env value, a CDN rule, the port a listener binds. The finding names that fact so `/security-live-scan` or the operator can settle it. Every coverage row is `checked (k hits → m findings)`, `N/A (<reason: no such sink in repo>)` or `blocked (<reason>)`. A row may not be omitted, so "found nothing" and "did not look" stay distinguishable. § 6's row names each sink it read — request log (6d names against the redact list), serialized payloads, traces, edge access log — and a sink the repo has but the run did not read makes the row `blocked`. `/security-audit` copies these rows into its class coverage ledger.

## False positives / gotchas

- **Dev-only config is not production.** `development.rb`, `settings/dev.py`, `application-dev.yml`, `.env.example` and test setup files are findings only if the production process loads them. Prove which file it loads.
- **A framework default can be the leak.** Express without a 4-arg handler, Fastify's default handler, fiber's default `ErrorHandler`, FastAPI's `/docs` and Next.js's `X-Powered-By` all leak with no line of code to grep. Absence of the override is the finding, the same set-difference reading as ssrf-scan's redirect grep.
- **`err.message` on a typed 4xx domain error is the design, not a leak.** Flag a message only when it can come from a library, the ORM, the driver or an upstream.
- **An explicit SQL column list is a projection.** `res.json(customer)` over `SELECT id, email, display_name` is not § 4. Read the query before you flag the return.
- **The OAuth `code` and `state` parameters belong in the URL by protocol.** § 7 targets long-lived credentials, not protocol parameters.
- **A plaintext token looked up with `WHERE token = $1` is also timing-variable.** The fix is to store the token's hash and look up by hash, which also protects it at rest. Do not wrap the query in a constant-time compare.
- **Metrics and docs on an internal-only port are fine.** Confirm the listener, not the route string.
- **Hidden files.** rg skips dotfiles unless `--hidden` is set, and every grep here sets it. A custom grep without it reports a clean `.env.production` it never read.

## When to run

- On any diff touching an error handler or exception filter, a `catch` that stores or returns error text, a logger call or logger config, a tracing setup, a reverse-proxy or log-collector config, a new credential header or webhook verifier, a serializer / response DTO / ORM projection, an auth message, a debug / docs / metrics / admin route, cache headers, a static or public directory, a GraphQL server config, or a signature / token comparison.
- Always on a whole-repo `/security-audit` run, and before launch on any public surface.

## Halt conditions

- Do not report a critical or high row as confirmed until a verifier other than the run that found it has passed it through [`finding-verification.md`](../../../../snippets/finding-verification.md). Under `/security-audit` that happens in Phase 4; run standalone, it applies the protocol as a separate second pass, tags those rows `self-verified`, and lists the rest as Unconfirmed, Hardening or Refuted — never drops them.
- Halt on any finding without the sink `<file:line>`, what leaks and to whom, and the fix.
- Halt on a grep hit reported as a finding without a read of the enclosing function and the production config that governs it.
- Halt on a § 2 or § 3 finding that asserts production state from a dev-only file, or one that does not name the runtime fact it depends on (`[report-flagged]`).
- Halt on output with no class coverage block, or with a detector row missing from it.
- Do not report a line another owner already credits (see § Premise). Cross-link it and keep one finding per sink.
- Do not inflate § 8 above low, or call schema hiding (§ 11) an access control.

## Related

- `/security-audit`: dispatches this skill on the error, logger, serializer, auth-message, debug-route and public-directory signals. Its class coverage ledger reads the block above.
- `/security-fix`: consumes these findings. `/security-live-scan` settles `[report-flagged]` rows against the deployed URL (`/.git/HEAD`, `/actuator`, response headers).
- `@security-auditor`: its A02, A09 and A10 rows are the surface pass, and this skill is the executor behind them.
- `@api-security-reviewer`: API3 BOPLA design (§ 4), API2 keys in URLs (§ 7), API5 admin-function authorization (§ 3), and its GraphQL checklist (§ 11).
- `@data-privacy-reviewer`: the PII consequence of § 4, § 6 and § 7 (lawful basis, erasure reach, regulation).
- `@auth-reviewer`: § Account enumeration inside the auth ceremony. § 5 here sweeps the rest.
- `secret-scan-method`: committed secrets, rotation and the history scrub. A `.env` or dump found by § 10 goes there too.
- `xss-scan`: client-bundle source maps and secrets, tokens in web storage. `file-access-scan`: path traversal and uploads in the web root. `injection-scan`: log injection. `iac-scan`: proxy banners, edge cache rules, infra dashboards and the Dockerfile copy behind grep 10c. `sast-scan`: overlapping analyzer hits, deduped by `<file:line>`.
- Backend pack, when installed: `backend/ai-patterns/error-handling.md` § Detectors (cite-or-halt) holds the single-mapper contract § 1's fix lands in, and `backend/ai-patterns/caching-strategy.md` holds cache-key design (§ 9). Without the backend pack, the BAD/GOOD pairs above are the contract.
- Observability pack, when installed: `observability/ai-patterns/structured-logging.md` § Redaction holds the logger redaction contract § 6's fix lands in. Without it, § 6's GOOD line is the floor.
- `rules/security-principles.md` § Must not: never log passwords, full tokens or full card numbers.
