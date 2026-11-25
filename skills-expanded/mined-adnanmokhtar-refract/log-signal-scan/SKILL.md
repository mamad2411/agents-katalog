---
name: log-signal-scan
description: "Log fidelity: invisible degrades, lost stacks, unstructured or mis-levelled logs, uncorrelated lines — captured-log proved."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: log-signal-scan

## Premise

At 3 a.m. the log is all on-call has, and it fails quietly. A payment fallback hands back the cached price and writes nothing, so the fallback rate is invisible. `this.logger.error('capture failed', err)` looks logged, but pino drops the error object, so the line has no stack and no type. A Nest app never hands its logger to pino, so production prints colored text that the log store cannot split into fields. A 404 flood is logged at error and drowns the real 500s. A BullMQ job's lines carry no request id, so nobody can join them to the request that queued the job. Every one of these passes review and every test, because the line is *there*.

This skill finds those defects across the loggers real services use: pino, pino-http, nestjs-pino, the NestJS `Logger` façade, winston, Python `logging`/structlog/loguru, Go slog/zap/zerolog, SLF4J/Logback, .NET `ILogger`/Serilog, and Rails and Monolog loggers. It proves each one with a **captured log**: drive the failure through the real entry point, capture what the logger actually wrote, and assert on the parsed fields. It owns `/obs-audit`'s Logs rows (§1–§5, `ownership.json` row `obs-logs`) and Correlation rows (§6–§8, row `obs-correlation`). `@observability-reviewer` (this pack) judges its rows.

**Every finding cites the log call or logger config `<file:line>` + the failure or request that reaches it + what the emitted line lacks (stack, type, level, field, id) + the oracle that showed it, or the test that would settle it + the fix in the project's own logger.** A grep hit is a candidate, never a finding. "Logging looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *Captured log*, variants V189–V193.

## The rule

A candidate is a finding when all four hold. These are the protocol's gates as `precedents/observability.md` § Reading the seven gates applies them to logs.

1. **A production path reaches the line.** A route, consumer, cron or worker the process starts. A one-shot CLI or migration script is not one (precedents § 44); a script that a CronJob, compose service or Procfile runs is (grep 3b2).
2. **The failure or the request really happens there.** The dependency can fail, the job is enqueued by a request, the probe is polled. A parse that defaults by specification is not a failure.
3. **Nothing already fixes the line.** None of these is present: an `error` serializer (§ 22), a global filter that logs the cause (§ 39), a logger `mixin` that stamps a context id on every line, the Java agent's MDC injection (§ 28), a log bridge that injects `trace_id`.
4. **The captured line shows it.** The oracle fired on the unfixed code. A static fact (a config production loads, a bootstrap with no logger hand-off) is two-ended: cite the config and the process that loads it. It stays `[report-flagged]` until the capture runs.

## Boundaries

- **A dropped or swallowed error** goes to code-quality `error-handling-scan`, when that pack is installed. That covers §1 (dropped), §2 (success-shaped value) and §6 (cause rewritten). The split is by **who cannot tell**:
  - **Code-quality's case: the caller cannot tell.** An empty or comment-only catch is code-quality's. So is a return the consumer acts on as success: a write, money, an authorization, or "no orders" shown to a user. A cause lost on a rethrow is code-quality's too.
  - **This skill's case: the operator cannot see it.** §1 starts where code-quality would clear the handler as handled. The degrade is right for the caller, but it writes no log at warn or above, no counter and no span event, so nobody can see its rate. Code-quality's own precedent requires a declared degrade to log or count (`precedents/code-quality.md § 14`), and that is the line §1 enforces.
  - **Ownership of shared sites.** §2 here owns *fidelity*: a log call that exists but loses the stack or type.
  - **Without code-quality:** dropped-error hits are listed as `quality-class (owner pack not installed)` and are not graded. A site both skills see is reported once, by `<file:line>`.
- **A secret, token or PII value in any log, or a redaction gap**, goes to security `data-exposure-scan` § 6, when the security pack is installed. This skill cites its rows and stops. Hashing an id is never offered as redaction (precedents § 32). **Log injection** (CR/LF into text logs) goes to security `injection-scan` § 10. Without the security pack, these rows are tagged `security-class (owner pack not installed)`, listed and never graded here (precedents P2). §5 keeps only the *volume* half of a payload logged per item.
- **Telemetry lost on exit** (LG-06: flush on SIGTERM, `process.exit` after a log) goes to `trace-propagation-scan` § 5 (this pack).
- **Exceptions that never reach the error tracker** go to `error-tracking-scan` (this pack). **Browser and mobile logging** are excluded from the pre-flight and belong there too.
- **The dollar cost of volume** is priced by finops `candidate-pricing` §0, judged by `@cost-reviewer` (finops pack, when installed; without it the arithmetic is reported unpriced). §5 here does the arithmetic: bytes per request and lines per probe.

## Adapt to the codebase — the logger lanes

Read each library **with its version** from the lockfile or `node_modules/<pkg>/package.json` (grep 0a). Print the lanes you ran in the output header. A Node logger is classified by its **receiver**, never its name:
- the Nest `Logger` façade over nestjs-pino, or the bare `ConsoleLogger`;
- nestjs-pino's `PinoLogger`;
- raw pino;
- winston.

| Lane | Libraries | Lint lane | Built-in that is a precedent |
|---|---|---|---|
| **Node** | pino 10, pino-http 11, nestjs-pino 5, NestJS 11 `Logger`/`ConsoleLogger`, Fastify 5 `request.log`, winston 3, bunyan | ESLint `no-console` only. ESLint `no-empty` misses comment-only catches, so the **regex lane is the detector** | Fastify `request.log` and nestjs-pino `PinoLogger` are request-bound (precedents § 40) |
| **Python** | `logging`, structlog, loguru; Django, FastAPI, Celery | ruff `G001`–`G004`, `G201`, `LOG001`–`LOG015`, `TRY400`, `TRY401`, `T201` | `structlog.contextvars.merge_contextvars` |
| **Go** | slog, zap, zerolog, logrus | golangci-lint `sloglint` (`context: scope`, `static-msg`), `loggercheck`, `zerologlint` | slog `*Context` variants carry `ctx` |
| **JVM** | SLF4J + Logback, Log4j2, Micrometer Tracing MDC | Error Prone `CatchAndPrintStackTrace`; PMD `PreserveStackTrace`, `SystemPrintln`, `GuardLogStatement` | the Java agent injects MDC trace ids (precedents § 28) |
| **.NET** | `ILogger`, Serilog | `CA2254`, `CA2017`, `CA1848` (off by default on .NET 10, precedents § 50) | `LoggerMessage` source generation |
| **Ruby, PHP** | Rails logger, semantic_logger; Monolog / PSR-3 | RuboCop `Rails/Output` | Rails `log_tags`; PSR-3 `['exception' => $e]` |

**Measured Node behaviour.** The precedents already settle pino 10.4.0, pino-http 11.0.0 and winston 3.19.0 (§ 52). The NestJS shapes were open [K?] items. They were settled by the captured-log oracle on 2026-10-10, on nestjs-pino 5.3.1, pino 10.4.0, `@nestjs/core` 11.2.7, `@nestjs/platform-fastify` 11.2.7 and Fastify 5.12.5. The parsed line was asserted after `bufferLogs` + `useLogger(app.get(Logger))` + `flushLogs()`.

| Call | Emitted line |
|---|---|
| Nest façade `error(err)`, `error(msg, err.stack)`, `error({ err }, msg)` | `err` with type and stack (kept) |
| Nest façade `error('msg', err)` | `msg` + `context` only: **err dropped**, as with raw pino |
| Nest façade or `PinoLogger` `` error(`… ${err.message}`) `` | message only: **stack and type lost** |
| `PinoLogger` `error(err, msg)`, `error({ err }, msg)` | kept |
| `PinoLogger` `error('msg', err)`; `error({ error: err }, msg)`; `{ err: String(e) }` | dropped; no stack; a string |
| request ids, no `genReqId` (nestjs-pino on Fastify, and plain Fastify 5) | `req-1`, `req-2`, `req-3`: a **per-process counter**; an incoming `x-request-id` was **not** used |
| `new ConsoleLogger({ json: true })` | accepted on Nest 11.2.7: `{"json":true,…,"colors":false}` |

Re-run the capture on the installed majors before citing a row for a different major.

## Lint lane

Run in `${TMPDIR:-/tmp}`, never in the project, and never commit a config. A lane that cannot install prints `blocked (lane not installed: <tool>@<ver>)` for its rule column, and the greps still run. A rule CI already fails at error level owns its lines (precedents P3). The finding then is only that a rule is off, at warning, or not run.

```bash
L="$(mktemp -d "${TMPDIR:-/tmp}/lg-lint.XXXXXX")"
python3 -m venv "$L/py" && "$L/py/bin/pip" -q install ruff==0.17.0 && "$L/py/bin/ruff" check --no-cache --isolated --select G,LOG,TRY400,TRY401,T201 --output-format concise --exclude '**/tests/**,**/test_*.py,**/migrations/**' "${ROOTS[@]}"
printf 'version: "2"\nlinters:\n  default: none\n  enable: [sloglint, loggercheck, zerologlint]\n  settings:\n    sloglint: { context: scope, static-msg: true }\n' > "$L/golangci.yml"   # then, in each Go module: golangci-lint run --config "$L/golangci.yml" ./...
```

- **.NET.** Build a copy under `$L` with `dotnet_diagnostic.CA2254.severity = warning` (and CA2017, CA1848) in its `.editorconfig`.
- **JVM.** `pmd check -R category/java/bestpractices.xml/PreserveStackTrace,category/java/bestpractices.xml/SystemPrintln -d <src/main>`; Error Prone runs in the project's build.

Tool versions as read for the research catalog on 2026-10-10: ruff 0.17.0, golangci-lint v2.14.0, sloglint v0.12.0, Error Prone v2.50.0, PMD 7.28.0. **Measured** (ruff 0.17.0, 2026-10-10, on the seeded sample):
- `TRY400` on the stdlib f-string error and on the structlog `log.error` inside an `except`;
- `G004` on the f-string;
- `G201` on the `exc_info=True` decoy, which is style only (precedents § 24, never posted);
- benchmark fixtures: one `T201`, a benchmark script's `print`.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; group 0 is context. Every `rg` names its path; any exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (that is `--follow`).
- **`LGN`** collects the repo's own logger field names (`private readonly audit = new Logger(…)`), so `LG` sees `this.audit.error(` too. Read `LGN` once: a name that is not a logger is removed.
- **`X`** drops browser and mobile packages (a `package.json` with a UI framework and no server dependency).
- **`scripts/` is not excluded.** Its stdout is split out of 3b, and 3b2 lists the deploy files that run a script.

```bash
ROOTS=( . )   # or the service roots from _extracted-codebase.md
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,target,bin,obj,vendor,.venv,venv,__pycache__,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,playwright,cypress}/**'
   -g '!**/*.{spec,test,e2e,e2e-spec,stories,story}.*' -g '!**/*_test.go' -g '!**/test_*.py' -g '!**/conftest.py'
   -g '!**/{migrations,migration,seeders,seeds,db/migrate,alembic/versions}/**' -g '!**/{locales,locale,i18n,translations,messages,lang}/**'
   -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock}' -g '!**/*.min.*')
J=(-g '*.{ts,tsx,js,jsx,mjs,cjs}'); PY=(-g '*.py'); GO=(-g '*.go'); JV=(-g '*.{java,kt,kts}'); CS=(-g '*.cs'); RB=(-g '*.rb'); PHP=(-g '*.php')
for d in $(rg -l --pcre2 '"(?:react|react-native|vue|svelte|@angular/core|solid-js|preact|expo)"\s*:' -g '**/package.json' -g '!**/node_modules/**' "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 '"(?:@nestjs/core|fastify|express|koa|@hapi/hapi|hono|next|nuxt|@sveltejs/kit|@remix-run/node|pino|winston|bullmq)"\s*:' | xargs -r -n1 dirname); do [ "$d" != . ] && X+=(-g "!${d#./}/**"); done
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')   # drops comment-only hit lines
LGN=$(rg -o --no-filename --pcre2 '\b(?:readonly|private|protected|public|const|let|var)\s+(?:readonly\s+)?\K\w+(?=\s*(?::\s*(?:PinoLogger|Logger|LoggerService|winston\.Logger)\b|=\s*(?:new\s+Logger\(|pino\(|(?:winston\.)?createLogger\()))' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | sort -u | paste -sd'|' -)
LG="\\b(?:logger|log|LOG|LOGGER|_log|self\\.logger|req\\.log|request\\.log|ctx\\.log|(?:this\\.)?(?:logger|log${LGN:+|$LGN}))"
OK="(?:$LG\.\w+\(|\.(?:inc|add|observe|record)\(|recordException|addEvent|captureException|capture_exception|\b(?:next|reject|cb|callback|done)\(\s*\w|\bthrow\b|\braise\b)"
# 0a logger libraries and versions (gate 3); 0b logger construction, serializers, mixins; 0c global error boundaries (§ 39).
rg -n --no-heading --pcre2 '"(?:pino|pino-http|pino-pretty|nestjs-pino|winston|bunyan|@nestjs/core|fastify|nestjs-cls|@opentelemetry/(?:sdk-node|instrumentation-pino|instrumentation-winston|auto-instrumentations-node))"\s*:|^(?:structlog|loguru|python-json-logger|asgi-correlation-id|opentelemetry-\S+)\b|go\.uber\.org/zap|rs/zerolog|sirupsen/logrus|<artifactId>(?:logback-classic|log4j-core|logstash-logback-encoder)<' -g '**/{package.json,requirements*.txt,pyproject.toml,go.mod,pom.xml,build.gradle*}' -g '!**/node_modules/**' "${ROOTS[@]}"
rg -n --pcre2 '\bpino\(|\bpinoHttp\(|LoggerModule\.forRoot(?:Async)?\(|createLogger\(|structlog\.configure\(|logging\.config\.dictConfig|zap\.New\w*\(|slog\.New\(|zerolog\.New\(|serializers\s*:|\bformatters\s*:|\bmixin\s*[:(]' "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '@Catch\(|implements\s+ExceptionFilter|setErrorHandler\(|@ControllerAdvice|@exception_handler|add_exception_handler|rescue_from' "${X[@]}" "${ROOTS[@]}"
# 1a a handler that returns a value not carrying the error, with no log, metric, span event, forward or rethrow. In JS/TS
#    only when its try awaits (a sync parse-or-default is CQ precedent 16); then JVM/C#/PHP, Python, Go.
rg -n -U --pcre2 "\}\s*catch\s*(?:\(\s*(\w+)\b[^)]*\))?\s*\{(?![^{}]*$OK)(?![^{}]*\breturn\b[^;{}]*\b\1\b)[^{}]*?\breturn\b[^{}]*\}" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}" | grep -E ':[0-9]+:[[:space:]]*\}[[:space:]]*catch' | while IFS=: read -r f n _; do
  awk -v n="$n" 'NR<n{L[NR]=$0;next} {d=match($0,/[^ \t]/); for(i=n-1;i>0;i--) if(match(L[i],/[^ \t]/)==d && L[i]~/(^|[^A-Za-z_])try[ \t]*\{/){ for(j=i;j<n;j++) if(L[j]~/(^|[^A-Za-z_])await[ \t(]/){print FILENAME":"n":"$0; exit} exit } exit}' "$f"; done
rg -n -U --pcre2 "\}\s*catch\s*(?:\(\s*(\w+)\b[^)]*\))?\s*\{(?![^{}]*$OK)(?![^{}]*\breturn\b[^;{}]*\b\1\b)[^{}]*?\breturn\b[^{}]*\}" "${JV[@]}" "${CS[@]}" "${PHP[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 '^[ \t]*except\b[^:\n]*:[ \t]*\n(?:[ \t]*(?:#[^\n]*)?\n)*[ \t]+return\b' "${PY[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n -U --pcre2 'if\s+err\s*!=\s*nil\s*\{\s*\n?\s*(?:return\b(?![^\n]*\berr\b)|(?!_\s*=)\w+\s*=)[^\n]*\n?\s*\}' "${GO[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 1b .catch(() => fallback) and contextlib.suppress; 1c a catch whose only log is debug / trace / info (debug/trace → §1, info → §4).
rg -n --pcre2 "\.catch\(\s*(?:\(\s*\w*\s*\)|\w+)\s*=>\s*+(?!\{|undefined\b|null\b|void\b|set[A-Z]|$LG)[^)]|contextlib\.suppress\(|^\s*with\s+suppress\(" "${J[@]}" "${PY[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 "\bcatch\s*(?:\([^)]*\))?\s*\{[^{}]{0,300}?$LG\.(?:debug|trace|verbose|info|log)\(" "${J[@]}" "${JV[@]}" "${CS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2a the eval's widened Node grep (message only, String(e), toString(); error(msg, err.stack) excluded), receiver widened to $LG.
rg -n --pcre2 "${J[@]}" "${X[@]}" "$LG"'\.(?:error|warn|fatal)\((?![^\n]*,\s*\w+\.stack\s*[,)])(?:[^()\n]|\([^()\n]*\))*(?:\$\{[^}]*\.message\b|\bString\(\s*(?:e|err|error|ex|exception)\s*\)|\b(?:e|err|error|ex)\.toString\(\))' "${ROOTS[@]}" | "${NC[@]}"
# 2b the catch binding never reaches the error/warn statement (anchored on `} catch (` so an ExceptionFilter.catch() method is no hit).
rg -n -U --pcre2 "\}\s*catch\s*\(\s*(\w+)\b[^)]*\)\s*\{(?:(?!\b\1\b)[^{}])*?$LG\.(?:error|warn|fatal)\((?:\\$\{(?:(?!\b\1\b)[^}])*\}|(?!\b\1\b)[^;{}])*\)\s*;" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2c error(msg, err): err dropped by pino, PinoLogger and the Nest façade over nestjs-pino; 2d { error: err } (read 0b: § 22).
rg -n -U --pcre2 "$LG\.(?:error|warn|fatal)\(\s*(?:'[^'\n]*'|\"[^\"\n]*\"|\`[^\`]*\`)\s*,\s*(?:e|err|error|ex|exception)\s*,?\s*\)" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 "$LG\.(?:error|warn|fatal)\(\s*\{[^}\n]*\berror\s*:" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 2e winston loggers with no format.errors; 2f Python error in an except with no exc_info (TRY400 fallback); 2f2 structlog error=str(e);
# 2g Go err.Error() as a string field; 2h Java concatenation / printStackTrace; 2i .NET; 2j Ruby; 2k PHP (starts with '-', so -e).
rg -l --pcre2 '\bcreateLogger\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg -l --pcre2 '\bwinston\b' | xargs -r rg --files-without-match --pcre2 'format\.errors\('
rg -n -U --pcre2 '^[ \t]*except\b[^\n]*:[ \t]*\n(?:[ \t]+[^\n]*\n){0,8}?[ \t]+(?:logger|log|LOG|_log|self\.logger|logging)\.error\((?![^\n]*exc_info)[^\n]*' "${PY[@]}" "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\b(?:error|err|exc|exception)\s*=\s*(?:str|repr)\(\s*\w+\s*\)' "${PY[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '(?:zap|slog)\.String\(\s*"(?:err|error)"\s*,\s*\w+\.Error\(\)|WithField\(\s*"(?:err|error)"\s*,\s*\w+\.Error\(\)|"(?:err|error)"\s*,\s*\w+\.Error\(\)' "${GO[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\.(?:error|warn)\(\s*"[^"]*"\s*\+\s*\w*(?:e|ex|exc|t|err|throwable)\b(?:\.getMessage\(\))?\s*\)|\.printStackTrace\(\)' "${JV[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'Log(?:Error|Critical|Warning)\(\s*(?:\w+\.Message\s*\)|\$"[^"]*\{\s*(?:e|ex|exception)\b)' "${CS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'logger\.(?:error|fatal|warn)[ (]+[^\n]*\b(?:e|ex|err|error)\.message\b' "${RB[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 "${PHP[@]}" "${X[@]}" -e '->(?:error|critical|warning|alert|emergency)\(\s*\$\w+->getMessage\(\)\s*\)' "${ROOTS[@]}" | "${NC[@]}"
# 3a interpolated messages (Node, Python, Go/JVM/.NET); 3b stdout in server code; 3b2 deploy files that run a script (read those
#    scripts as production); 3c Nest bootstraps with no logger hand-off; 3d pretty transports (read the guard).
rg -n --pcre2 "$LG\.(?:trace|debug|info|log|warn|error|fatal)\(\s*\`[^\`]*\\$\{" "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '\b(?:logger|logging|log|LOG|_log|self\.logger)\.(?:debug|info|warning|warn|error|exception|critical)\(\s*(?:f["\x27]|["\x27][^"\x27]*["\x27]\s*(?:%|\.format\())' "${PY[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 'slog\.\w+\(\s*(?:ctx\s*,\s*)?fmt\.Sprintf\(|\b(?:log|logger|LOG|LOGGER)\.(?:trace|debug|info|warn|error)\(\s*(?:"[^"]*"\s*\+|String\.format\()|Log(?:Trace|Debug|Information|Warning|Error|Critical)\(\s*(?:\w+\s*,\s*)?(?:\$"|"[^"]*"\s*\+)' "${GO[@]}" "${JV[@]}" "${CS[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '^\s*(?:console\.(?:log|info|debug|warn|error)\(|print\(|puts\s|var_dump\(|print_r\(|System\.(?:out|err)\.print|Console\.Write|log\.Print|fmt\.Print)' "${J[@]}" "${PY[@]}" "${GO[@]}" "${JV[@]}" "${CS[@]}" "${RB[@]}" "${PHP[@]}" "${X[@]}" -g '!**/{scripts,bin,tools,cli}/**' "${ROOTS[@]}"
rg -n --pcre2 '\b(?:scripts|bin|tools|cli)/[\w./-]+\.(?:[cm]?[jt]s|py|sh|rb)\b' -g '*.{yml,yaml}' -g '**/Dockerfile*' -g '**/Procfile' -g '**/*cron*' -g '!**/node_modules/**' -g '!**/.github/**' "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 'NestFactory\.create\w*\s*[<(]' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'useLogger\(|bufferLogs|\blogger\s*:'
rg -n --pcre2 'target\s*:\s*["\x27]pino-pretty["\x27]|prettyPrint\s*:\s*true' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
# 4a request-log config with no level map; 4b exception filters that log at error (read the 4xx branch); 4c log-and-rethrow;
# 4d debug in a config production may load (dev/local/test/staging/override files excluded: precedents § 30).
rg -l --pcre2 '\bpinoHttp\s*[:(]|LoggerModule\.forRoot|(?:from\s+|require\(\s*)["\x27]pino-http["\x27]' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'customLogLevel'
rg -l --pcre2 '@Catch\(|implements\s+ExceptionFilter|setErrorHandler\(' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg -n -H --pcre2 "$LG\.error\("
rg -n -U --pcre2 "\}\s*catch\s*\(\s*(\w+)\b[^)]*\)\s*\{[^{}]*?$LG\.(?:error|exception)\([^{}]*?\bthrow\s+\1\b" "${J[@]}" "${JV[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n --pcre2 '^\s*(?:"?(?:root|level|LOG_LEVEL|log_level|logLevel|"Default")"?\s*[:=]\s*["\x27]?(?:DEBUG|debug|TRACE|trace|Debug|Trace|verbose)\b)' -g '*.{yml,yaml,json,properties,toml,env,ini,conf}' -g '.env*' -g '!**/*[-_.]{dev,development,local,test,staging,stage,qa}.*' -g '!**/.env.{development,local,test,staging}' -g '!**/docker-compose.override.*' -g '!**/{package,tsconfig}*.json' "${X[@]}" "${ROOTS[@]}"
# 5a a payload serialized into a log call; 5b a log call in a loop body indented under it (constant arrays skipped); 5c no probe ignore.
rg -n --pcre2 "$LG\.\w+\([^\n]*\b(?:JSON\.stringify|json\.dumps|util\.inspect)\(" "${J[@]}" "${PY[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -n -U --pcre2 "^([ \t]*)(?:(?:for|while)\b(?![^\n]*\bof\s*\[)[^\n]*[{:]|[^\n]*\.forEach\([^\n]*\{)[ \t]*\n(?:\1[ \t]+[^\n]*\n){0,3}?\1[ \t]+$LG\.(?:info|debug|log|trace)\(" "${J[@]}" "${PY[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 '\bpinoHttp\s*[:(]|LoggerModule\.forRoot|(?:from\s+|require\(\s*)["\x27]pino-http["\x27]' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'autoLogging'
# 6a repo level: any request-id mechanism at all; 6b request loggers and Fastify instances with no genReqId (a per-process counter).
rg -l --pcre2 'genReqId|requestIdHeader|x-request-id|nestjs-cls|AsyncLocalStorage|asgi-correlation-id|django-guid|correlation_id|log_tags|MDC\.put|RequestIdMiddleware|chi/middleware' "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 '\bpinoHttp\s*[:(]|LoggerModule\.forRoot|new\s+FastifyAdapter\(|\bFastify\(\s*\{|\bfastify\(\s*\{' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'genReqId'
# 7a jobs, consumers and cron with no context binding in the file; 7b Go slog without ctx; 7c MDC put never cleared; 7d structlog without contextvars.
rg -l --pcre2 '@Processor\(|@Process\(|\bWorkerHost\b|new\s+Worker\(|@Cron\(|@Interval\(|@shared_task|@\w+\.task\b|@KafkaListener|@RabbitListener|@SqsListener|@Scheduled\(|@EventPattern\(|@MessagePattern\(' "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'ClsService|nestjs-cls|AsyncLocalStorage|bind_contextvars|MDC\.|\b(?:trace_?[iI]d|request_?[iI]d|correlation_?[iI]d)\b|PinoLogger'
rg -n --pcre2 '\bslog\.(?:Debug|Info|Warn|Error)\(' "${GO[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
rg -l --pcre2 'MDC\.put\(' "${JV[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'MDC\.(?:remove|clear)\(|MDC\.putCloseable\('
rg -l --pcre2 'structlog\.configure\(' "${PY[@]}" "${X[@]}" "${ROOTS[@]}" | xargs -r rg --files-without-match --pcre2 'merge_contextvars'
# 8a tracing SDK files, then log-bridge files (compare the two lists); 8b camelCase trace fields (read the shipper's field names).
rg -l --pcre2 '@opentelemetry/sdk-node|NodeSDK\b|opentelemetry\.sdk|go\.opentelemetry\.io/otel/sdk|opentelemetry-javaagent' "${X[@]}" "${ROOTS[@]}"
rg -l --pcre2 'instrumentation-pino|instrumentation-winston|auto-instrumentations-node|getNodeAutoInstrumentations|OTEL_PYTHON_LOG_CORRELATION|LoggingInstrumentor|otelslog|otelzap|-javaagent:' "${X[@]}" "${ROOTS[@]}"
rg -n --pcre2 '\b(?:traceId|spanId|traceID|spanID)\s*:' "${J[@]}" "${X[@]}" "${ROOTS[@]}" | "${NC[@]}"
```

A finding is a hit **plus** a read of the call site **plus** the receiver's logger **plus** the oracle. Three blind spots are structural:
- **Wrappers hide the logger.** A project logger, a `failureOf(error)` helper or a job base class can fix or break every caller. Read each wrapper once. A defect in it is one finding with N sites (precedents P4).
- **Global mixins hide the binding.** A pino `mixin` that reads AsyncLocalStorage stamps an id on every line, so a file-level negative (6a, 7a) is only a candidate until 0b's `mixin` is read.
- **Deep try bodies.** The 1a JS filter finds the `try` at the catch's indentation and asks whether its body awaits. A `try` written on the same line as other code is missed, and §1's read covers it.

### Measured (2026-10-10, the script above)

| Tree | Hits that matter | Verdict |
|---|---|---|
| Seeded sample: NestJS on Fastify + nestjs-pino, plain pino, winston, Python logging/structlog, Go slog/zap, Java SLF4J; 36 seeds, 16 decoys; 1.0 s | every § caught its seeds (36/36) | Two decoys hit and are refuted on read: `{ error: err }` with a serializer in 0b (§ 22), and a rethrow with `cause` to a filter that logs it (§ 39). The CLI script's `console.log` stays out of 3b (no deploy file runs it, 3b2). Excluded trees (`migrations/`, `i18n/`, `test/`, `*.spec.ts`, `*.e2e-spec.ts`): **0 hits**. Before `LGN`, 2a/2c missed the two façade seeds on a field named `facade` |
| `benchmarks/fixtures/*` (15 trees, about 1 s each) | review-decoys 2a 2 · slow-marketplace 2a 1 · quality-mix 2b 1 handler · 1a 3 · 3c 4 bootstraps · 6b 3 · 4b 2 | 2a matches the eval's P7 exactly. The global exception filter's `error(msg, err.stack)` decoy stays out. 2b catches P8 (the seeded charges service). The fixtures' Nest bootstraps hand no logger off (eval P10). 1a: two route to code-quality (`return res.status(500)` with the error discarded; `catch { return [] }` read as "no charges"), one is a §1 candidate (a recommendations fallback). Web-only trees: 1 hit total (a tolerant `res.json().catch(() => ({}))`, CQ precedent 15) |
| Real NestJS + Fastify + MikroORM + BullMQ + nestjs-pino monorepo, API package, read-only; 44 greps in 2.4–3.3 s | 1a 3 · 1b 1 · 2a 36 · 3a 108 · 4a 1 · 4b 2 · 5a 2 · 5b 2 loops · 5c 1 · 6a 20 files · 7a 49 files · 8b 1 | Per §, below |

Real-repo triage:
- **§1.** 1a: 3 handlers. 2 are candidates: a best-effort enrichment returning `null` with no signal, and a stock preflight that fails open with no counter. 1 is refuted: a token check whose failure is the expected anonymous path. 1b: 1 hit, refuted (shutdown cleanup, CQ precedent 17).
- **§2.** 2a: 35 of 36 are the same convention, `` `… ${String(error)}` `` through the Nest façade over nestjs-pino, measured above to drop the stack. That is **one finding with 35 sites**. The 36th passes `exception.stack` as the message, which is refuted (§ 38 shape). 2b, 2c, 2d, 2e: 0.
- **§3.** 3a: 108 template-literal messages, one convention group (L). 3b: 0 in server code. 3c: 0 (`bufferLogs` + `useLogger(PinoLogger)`). 3d: refuted, because pino-pretty is a devDependency and the transport keys on its presence.
- **§4.** 4a: 1 candidate (`LoggerModule` with no `customLogLevel`; V192 settles it). 4b: 2 refuted (both filters log only status ≥ 500).
- **§5.** 5a: 2 candidates (`JSON.stringify(job.data)` and of a context object; the sensitive half goes to security). 5b: 2 loops, Hardening (bounded by constants). 5c: 1 candidate.
- **§6.** Refuted: `genReqId` honours `x-request-id`, and a hook mints one when the header is absent.
- **§7.** 49 files, **one group**, refuted after reading two files: a `mixin` stamps ALS-held ids on every line, and the job base class restores the context. V193 settles it.
- **§8.** The bridge is present. The camelCase `traceId` is refuted because the log shipper promotes the same field name.
- **Fixes measured on the way:** 1a fell from 57 handlers to 3 when (a) a return carrying the binding counts as a typed failure, (b) `next(err)` forwards, and (c) the try must await. Before those, about 30 hits were `JSON.parse` / `new URL` / `Intl` parse-or-default. 2b had 9 false positives, where a `)` inside the message text ended the match; it now requires `);`. 3b had 227 one-shot repair scripts under `scripts/`, now split to 3b2. The working tree was unchanged before and after the run.

## The 3,000-hit path

1. **Intersect** with the entry-point map: routes, consumers, cron and workers. Code no process starts is dismissed with one read. Scripts not named by 3b2 are CLI.
2. **Group** by logger receiver and call shape (`` `${String(error)}` `` through the façade is one group), by wrapper or factory, and by job base class.
3. **Rank** by path: payment, auth, checkout-class and consumer paths first, then error level over warn.
4. **Read the top 30 groups.** One read of 0b's serializers and mixins settles whole groups.
5. **Run the bulk oracle:** one captured-log run of the integration suite. Swap the logger destination for a collector and assert `err.stack` on every error-level line. That confirms or refutes every §2 group at once.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing grep id>)`. Never mark them `checked`.

## Scans for

Severity is what on-call loses on a reachable path (`thresholds.json` `THR-LOG-LEVEL` sets the level rule). Raise one step when it is the only signal on a payment, auth or consumer path. Drop one step for internal tooling.

| § | Class | Default |
|---|---|---|
| 1 | LG-01 handled failure invisible | high on payment / consumer paths; else medium |
| 2 | LG-02 error object or stack lost | medium; high when it is the only signal on a critical path |
| 3 | LG-03 unstructured, stdout or non-JSON logger in production | low; medium when request data is interpolated |
| 4 | LG-04 level misuse, log-and-rethrow, debug in a production config | medium |
| 5 | LG-05 hot-loop, full-payload or probe logging at volume | low to medium |
| 6 | CO-01 request id absent or colliding across replicas | medium; high across services |
| 7 | CO-02 logger not bound to context (jobs, consumers, async hops) | medium |
| 8 | CO-03 `trace_id` / `span_id` not injected, or renamed | medium |

### 1. Handled failure invisible (LG-01)

```
BAD:   } catch { return this.cache.get(sku) ?? 0; }     · .catch(() => ({ id }))     · with contextlib.suppress(httpx.TimeoutException):
       } catch (err) { this.logger.debug({ err }, 'discount lookup failed'); return 0; }      · if err != nil { p = 0 }
GOOD:  } catch (err) { fallbacks.inc({ reason: 'quote' }); this.logger.warn({ err, sku }, 'quote failed, cached price'); return cached; }
```
**Read the code:**
- Which dependency fails here?
- Is the degrade right for the caller? If the caller acts on it as success, route it to code-quality (§ Boundaries).
- Would on-call see the fallback rate anywhere: a log at warn or above, a counter, a span event, a tracker capture?
- Is it a payment, auth or consumer path?
- Is it best-effort cleanup (CQ precedent 17) or a parse-or-default (CQ precedent 16)? Neither is LG-01.

**Finding when** a reachable degrade path leaves no signal at warn or above. **Proof:** fault injection (V190). Make the dependency throw, then assert a log at warn or above, **or** a counter +1, **or** a span `exception` event.

### 2. Error object or stack lost (LG-02)

```
BAD:   this.logger.error('capture failed', err)   · logger.error({ error: err }, …)   · `… ${(err as Error).message}`   · { err: String(e) }
       winston format.json() with no format.errors · logger.error(f"… {e}") in except · zap.String("err", err.Error()) · log.error("x: " + e)
GOOD:  logger.error({ err }, 'capture failed') · this.logger.error(msg, err.stack) (Nest, § 38) · logger.exception(…) · zap.Error(err)
       log.error("refund failed for {}", id, e) (§ 23)
```
**Read the code:**
- Which logger is the receiver: the Nest façade, `PinoLogger`, raw pino, or winston? The measured table above says what each one emits.
- Is an `error` serializer configured (0b, precedents § 22)?
- Does the catch rethrow with `{ cause: e }` to a filter that logs the cause (§ 39)? Then the inner site is no finding, and two logs of one error are §4.
- Is a stack text in the message (§ 38)? Then it is kept, though unstructured.
- In Python: does `exc_info=True` or `logger.exception` already apply (§ 24)?

**Finding when** the captured line, for an error that reaches production, lacks `stack` and `type`. **Proof:** *Captured log* (V189), with each shape the repo uses run once.

### 3. Unstructured, stdout or non-JSON logger in production (LG-03)

**Read the code:**
- Is it a CLI (3b2 decides), a bootstrap before the logger exists, or a dev-guarded branch?
- Does the Nest bootstrap hand off to pino (`bufferLogs` + `useLogger`) or use `ConsoleLogger({ json: true })` (measured: available on Nest 11)?
- Is `pino-pretty` reachable in the production image? A devDependency keyed on presence is not.
- Which file does the production process load (precedents § 30)?
- An interpolated message (3a) groups per convention. Request data in it raises the severity, and a sensitive value routes to security.

**Finding when** production emits a line a log store cannot parse into fields, or a message template that changes per call. **Proof:** the lint rule at error is clean, and two calls with different data emit one template with the data in fields (V191).

### 4. Level misuse, log-and-rethrow, debug in a production config (LG-04)

**Read the code:**
- Does a 404 or validation failure log at error? Check the filter's 4xx branch (4b) and pino-http's `customLogLevel` (4a); with no `customLogLevel`, every request line is `info`.
- Is an error logged at info or debug inside a catch (1c)?
- Is one error logged at two layers (4c, plus the global filter)?
- Which config sets the level production loads: compose, Helm values, the manifest (gate 7)?

**Finding when** a level contradicts `THR-LOG-LEVEL`: 4xx at warn or below, 5xx at error, a recovered failure at warn, one log per error per request. **Proof:** *Captured log*, Level (V192). Drive a 404, a validation failure and a 500 through one entry point.

### 5. Hot-loop, full-payload or probe logging (LG-05)

**Read the code:**
- Is the loop bounded by a constant or a page size (then it is Hardening)?
- Does the payload carry user data? Then route the value half to security, and the volume half stays here.
- Does pino-http ignore `/health`, `/readyz` and `/metrics` (`autoLogging.ignore`, 5c)? Excluding probes is correct (precedents § 18).
- Is the stream an audit log with its own sink (§ 31, never a volume finding)?

**Finding when** bytes per request exceed the project's budget, or probes log at full rate. **Proof:** count bytes per request, and lines per 100 probe hits, which should be 0 (V192, V201).

The probe row is named here once: **LG-05 probe — pino-http with no `autoLogging.ignore` (grep 5c)**. `metric-hygiene-scan` §8 (HC-02, probe traffic in telemetry) lists the same logger surface in its grep 8b as corroboration and credits this row, never a second finding; the metric and trace halves of HC-02 stay there.

### 6. Request id absent or colliding (CO-01)

**Read the code:**
- Is an upstream id honoured (a `genReqId` that reads `x-request-id`, or Fastify `requestIdHeader`)?
- Is the fallback unique across replicas (UUID or ULID)? The pino-http and Fastify defaults are per-process counters (measured above, § 52).
- Does a hook mint one when the header is absent?

**Finding when** two replicas can mint the same id, or a request line carries none. **Proof:** two concurrent requests, each line with its own distinct id (V193).

### 7. Logger not bound to context (CO-02)

**Read the code:**
- Does a pino `mixin`, `nestjs-cls` or AsyncLocalStorage stamp the id on every line (0b)?
- Does the job payload carry the originating request or trace id, and does the job base class restore it (§ 40)?
- Go: `slog.Info` vs `slog.InfoContext` in a handler.
- Java: is MDC cleared after the request (7c), and copied to `@Async` and executors?
- Python: structlog `merge_contextvars` (7d), and no `threading.local` under asyncio.

**Finding when** a line on a job, consumer or async path has no correlation id. **Proof:** one request plus the job it enqueues, with the job's lines carrying the originating id (V193).

### 8. Trace ids not in logs, or renamed (CO-03)

**Read the code:**
- Is a log bridge wired (8a vs 8a2): `instrumentation-pino`/`-winston`, auto-instrumentations, `OTEL_PYTHON_LOG_CORRELATION`, the otelslog bridge, the Java agent (§ 28)?
- For a hand-rolled mixin (8b): does the log shipper, the derived field and the dashboard read the **same** name? If they do, it is consistent and not a finding.

**Finding when**, with tracing enabled, log lines lack the trace id under the name the log store joins on. **Proof:** the log `trace_id` equals the exporter's traceId for that request (V193).

## Proof — the captured log

Every § proves with [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *Captured log*, which carries the per-stack capture code:
- pino with a `{ write }` destination and `fastify.inject`;
- nestjs-pino `pinoHttp: [opts, stream]` in the testing module, then `useLogger` and `flushLogs`;
- a Nest `ConsoleLogger` subclass;
- a winston `Stream` transport;
- `caplog` and `structlog.testing.capture_logs()`;
- a slog JSON handler into a buffer, and zap `observer`;
- Logback `ListAppender` (JVM) and `FakeLogger` (.NET).

Variants: V189 (§2), V190 (§1), V191 (§3), V192 (§4–§5), V193 (§6–§8).

A spy on call arguments proves what was passed, not what was written. Use one only for a façade with no destination of its own. Each test drives the failure through the real entry point, asserts the one field the finding names, and **fails before the fix**. A fix is accepted only when all of these hold:
- the capture goes green;
- every shape of the group passes;
- the owning grep goes quiet on the line;
- for any change to a logger, serializer or sink, security's redaction canary (`data-exposure-scan` § 6) still passes.

Never accepted:
- a lint suppression;
- moving the message into a template;
- logging the error twice;
- deleting the test.

## Output

```
log-signal-scan — lanes: node (nestjs-pino 5.1.0, pino 10.3.1, pino-http 11.0.0, @nestjs/core 11.2.6, fastify 5.12.3); python, go, jvm, .net absent
Context: LoggerModule src/app.module.ts:112 (genReqId honours x-request-id; mixin correlationFields; no customLogLevel) · filters log ≥ 500 only
Lint: ESLint no-console (not configured); ruff/golangci/CA/PMD: N/A (lane absent)

Findings: 1 · Unconfirmed: 3

1. src/billing/charge-retry.service.ts:88 (+34 sites, 28 files)     [report-with-fix]   medium
   §2 stack lost — `${String(error)}` interpolated through the Nest Logger façade over nestjs-pino; the captured line
   has msg + context only. Proof: test/obs/log-capture.e2e-spec.ts — V189 fails (no err.type, no stack frame).
   Fix: this.logger.warn({ err: error }, 'retry budget unavailable, charging once') across the group.

2. src/orders/application/stock-preflight.ts:64                     [report-flagged]    medium
   §1 fail-open degrade with no signal — inventory read fails, dispatch proceeds, nothing logged or counted.
   Unproven link: no fault-injection harness for the inventory port. Settling test: V190 (port throws → log ≥ warn or counter +1).

3. src/app.module.ts:115                                              [report-flagged]    medium
   §4 pino-http with no customLogLevel — 4xx and 5xx request lines at info. Settling test: V192 (404 ≤ warn, 500 = error).

4. src/app.module.ts:115                                              [report-flagged]    low
   §5 no autoLogging.ignore — probe traffic logged per hit, unless the probes bypass the HTTP logger. Settling test: 100 probe hits → 0 lines.

Routed: 1 — src/auth/auth.service.ts:59 access token interpolated into an info log → security data-exposure-scan § 6

Verification: 245 candidates → 1 finding · 3 unconfirmed · 3 hardening · 0 pre-existing · 238 refuted / grouped

Class coverage:
  §1 handled failure invisible    checked (3 handlers + 1 .catch → 1 unconfirmed; 2 refuted; 1 unconfirmed best-effort note)
  §2 error / stack lost           checked (36 hits → 1 finding (35 sites); 1 refuted § 38; ruff/golangci N/A)
  §3 unstructured / stdout        checked (108 template messages → 1 group, Hardening; 0 stdout in server code; bootstrap hands off)
  §4 level misuse                 checked (1 config → 1 unconfirmed; 2 filters refuted: ≥ 500 only; 0 prod debug)
  §5 volume                       checked (2 payload logs, 2 loops → 1 unconfirmed, 2 Hardening; sensitive half routed)
  §6 request id                   checked (genReqId honours x-request-id; hook mints one)
  §7 context binding              checked (49 job files → 1 group refuted: mixin + job base class; V193 pending)
  §8 trace ids in logs            checked (bridge present; camelCase traceId matches the shipper)
```

`[report-with-fix]` means the call site, the path that reaches it, and a failing capture are all present, and the fix is local to the project's logger. `[report-flagged]` means one link is unproven (no harness, a wrapper not read, which config production loads), and the row names it with the settling test.

The coverage block lists **all eight** classes on every run:
- `checked (k hits → m findings)` only when the greps, and the lint lane where one applies, ran on a present lane;
- `N/A (<reason>)` only when the repo has no such surface;
- `blocked (<reason>)` when a grep failed or a lane could not install;
- `Live, unreviewed (k groups / n hits)` for a partial review, never `checked`.

## False positives / precedents

The verifier reads [`precedents/observability.md`](../../../../snippets/precedents/observability.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4 and § 10. The ones this skill meets most:
- **pino `error(err, msg)` and `error({ err }, msg)` are correct.** `{ error: err }` is correct with an `error` serializer (§ 22).
- **Nest `error(msg, err.stack)` keeps the stack** (§ 38), and so does a stack passed as the message.
- **A rethrow with `cause` to a filter that logs it** is not LG-02 (§ 39).
- **`exc_info=True`** equals `logger.exception` (§ 24).
- **SLF4J with a trailing throwable** keeps the stack (§ 23).
- **Request-bound loggers** (`request.log`, `PinoLogger`) carry the id. Jobs need CLS, a mixin, or the id in the payload (§ 40).
- **A debug level in a dev, staging or override config** is noise (§ 30).
- **High-cardinality ids belong in log fields** (§ 19).
- **Probes excluded from access logs is correct** (§ 18).
- **Audit streams** are never sampled or volume-cut (§ 31).
- **A one-shot CLI's stdout** is not LG-03 (§ 44 is the same line for exit).
- **Measured defaults** (§ 52): pino drops `error(msg, err)`; pino-http and Fastify ids are per-process counters; winston without `format.errors` writes `{"level":"error"}`.
- **"Noisy" or "too much logging"** without byte counts is `NO-DATA` (§ 36). A field name proposed in a fix that the logger never emits is fabricated (§ 37).

## When to run

- On any diff that adds or changes a catch, a logger call at warn or above, a logger or request-log config, a Nest bootstrap, an exception filter, a job processor or consumer, or a tracing bootstrap.
- On every whole-repo `/obs-audit`, reporting all eight classes.
- As the evidence `@observability-reviewer` judges, and as `/obs-fix`'s RE-DETECT for logger fixes.

## Halt conditions

- Do not report a high or critical row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 10. Under an audit command that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any finding without the call site `<file:line>`, the path that reaches it, and the receiver's logger read.
- Do not mark a row `[report-with-fix]` without a captured line that failed; a config-only §3/§4 row stays `[report-flagged]` until production's config is shown.
- Do not cite pino, nestjs-pino or winston behaviour for a major the capture did not run on.
- Do not grade a secret or PII value, a redaction gap or log injection; route it (§ Boundaries).
- Do not print "logging is fine". Print the coverage block; a class whose grep or lane did not run is `blocked`, never `checked`.

## Related

- `@observability-reviewer` (this pack) judges these rows. `trace-propagation-scan` (this pack) owns LG-06 flush. `error-tracking-scan` (this pack) owns tracker capture.
- `error-handling-scan` (code-quality, when installed) owns dropped and swallowed errors. `data-exposure-scan` § 6 and `injection-scan` § 10 (security, when installed) own sensitive values and log injection.
- `ai-patterns/structured-logging.md` and `rules/observability-principles.md` (this pack) set the project's logger convention, which every fix follows.
