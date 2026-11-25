---
name: trace-propagation-scan
description: "Trace breaks: lost async/queue context, late SDK init, unended spans, unsafe samplers — in-memory-exporter proved."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: trace-propagation-scan

## Premise

A trace is only useful when it is whole. The failure is silent: a goroutine started with `context.Background()`, a BullMQ job enqueued with no context in its payload, a Python thread pool, an SDK the start command never preloads, a span that never ends on the error path. Each one leaves spans that still export, so dashboards stay green. On-call opens the trace of a failed checkout and finds a root span with no children, or no trace at all. OTel's own defaults are safe: the default sampler is `parentbased_always_on`, the default propagators are `tracecontext,baggage`, and an unnamed service becomes `unknown_service:<executable>` (the OTel SDK environment-variable spec and `service.name` resource convention, both fetched 2026-10-10). So most defects here are **a safe default overridden, or a hop the default cannot see**. OTelBench (Quesma, 2026-01) found context propagation to be the main failure of LLM-written instrumentation, so tracing code an agent wrote is unverified until an exporter shows one trace across the hop.

This skill finds those breaks in code and run config for every tracer real repos use: OpenTelemetry in Node, Python, Go, Java and .NET; Datadog, New Relic and Elastic APM; Micrometer Tracing; and Sentry performance tracing. It proves each break with an **in-memory span exporter** driven through the real entry point. It owns `/obs-audit`'s Tracing (§1–§8) and Sampling (§9–§10) rows (`ownership.json` rows `obs-tracing`, `obs-sampling`). `@observability-reviewer` (this pack) judges its rows.

**Every finding cites the break `<file:line>` + the hop it breaks (async, queue, outbound, process start, sampler) + the entry point whose trace it splits + the oracle that showed it, or the test that would settle it + the fix in the project's own tracer.** A grep hit is a candidate. "Tracing looks fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). The oracles are [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *In-memory span exporter*, variants V194–V197.

## The SDK gate — run before any §

Pre-flight 0a and 0b decide whether the repo traces at all. The gate is **open** when either of these holds:
- 0a prints a tracer dependency: OTel SDK or API, `dd-trace`/`ddtrace`, New Relic, Elastic APM, or Micrometer Tracing.
- 0b prints zero-code wiring: `-javaagent:`, `opentelemetry-instrument`, `ddtrace-run`, a `--require`/`--import` preload, or an OTLP exporter endpoint.

A Sentry SDK opens the gate only when 0b also prints a `traces*` key. Print the result in the header: `gate: open (<file:line>)` or `gate: closed (no tracing SDK)`.

**Gate closed.** Every § prints `N/A (no tracing SDK)`, with two exceptions that still run:
- **§10, SA-02 requirement half.** The repo states that errors must be traced (grep 10a), and no tracer exists to do it. The row asks whether an error tracker captures every error instead. If one does (the `error-tracking-scan` rows, this pack), the requirement is met. If none does, the requirement has no mechanism.
- **§5, LG-06 flush half.** A logger with an async destination, or a process that exits right after a log (greps 5c), loses its last lines on SIGTERM whether or not traces exist.

No other row is graded on a closed gate. "No tracing SDK" is itself a design gap, but it belongs to `/add-tracing`, not to this detector.

## The rule

A candidate is a finding when all four hold. These are the protocol's gates as `precedents/observability.md` § Reading the seven gates applies them to traces.

1. **A production path crosses the hop.** A route, consumer, cron or worker that the process type starts (0c) crosses this goroutine, executor, queue, outbound call, process start or sampler. Health and readiness routes excluded from tracing are correct (precedents § 18).
2. **Nothing already carries the context.** None of these is present: auto-instrumentation for this client at this version, the Java agent (precedents § 28), `context.WithoutCancel` (§ 26), a .NET flow that is never suppressed (§ 27), Python `start_as_current_span` (§ 25), `bullmq-otel` telemetry on both the queue and the worker, or a wrapper that injects.
3. **The version has the behaviour.** The SDK and instrumentation majors are read from the lockfile, never assumed (gate 3). Examples: JS SDK 2.x took span processors in the constructor; dd-trace-py 3 dropped `DD_TRACE_SAMPLE_RATE` (§ 48); the semconv opt-in decides which attribute names are emitted (§ 46).
4. **The oracle fired, or the trace is two-ended.** An in-memory exporter shows the split trace, the orphan root or the unended span. Or, for a static-fact class (§5 start command, §6 identity, §9 and §10 sampler config), both ends are cited: the config the production process loads, and the code or service that depends on it. That case is `[report-flagged]` until the exporter runs.

## Boundaries

- **Trace ids missing from log lines (CO-03)** → `log-signal-scan` (this pack). This skill proves the trace; that skill proves the log carries its id.
- **Collector pipeline health** (processor order other than sampling, `memory_limiter`, exporters, queues, tail-sampler topology) → `telemetry-config-scan` (this pack). §10 here owns only **where sampling sits relative to span-derived metrics**.
- **Error-tracker init, release and capture** → `error-tracking-scan` (this pack). §10 reads its rows as evidence that errors are captured. It never re-checks the tracker.
- **A secret or PII value in a span attribute or baggage** → security `data-exposure-scan` § 6, when the security pack is installed. Without it, the row is tagged `span PII (owner pack not installed)`, listed and never graded (precedents P2).
- **A swallowed error inside a span** → code-quality `error-handling-scan`, when that pack is installed. §4 owns only the missing `recordException`/status on a failure that *is* raised.
- **The shutdown chain** (SIGTERM handler, drain, `terminationGracePeriodSeconds`) → devops (code chain) and infrastructure (manifest), when those packs are installed. §5 owns only the telemetry flush inside that chain (V196). Without them, §5 still reports a missing flush and names the chain as unowned.
- **Trace coverage as a resilience target** ("every endpoint has spans") → the distributed-systems pack, when installed. This skill owns the mechanics that make spans join.
- **Sampling cost in money** → finops `candidate-pricing` §0 prices the volume when installed; §9 carries the span-count arithmetic.

## Adapt to the codebase — the tracer lanes

Read every tracer, instrumentation package and queue client **with its version** from the lockfile or manifest. Print the lanes you ran in the header. Facts marked *(fetched 2026-10-10)* were read today from the official doc named in § Sources. `[K]` is established but not re-fetched. `[K?]` is unverified: a row that rests on a `[K?]` item is Unconfirmed until its settling test runs.

| Lane | Init and preload | Auto-propagation (decoy) | Manual breaks to grep | Lint lane |
|---|---|---|---|---|
| **Node** (NestJS 10/11 on Express or Fastify, Express, Fastify 5, Koa) | `@opentelemetry/sdk-node` `NodeSDK`, or `NodeTracerProvider` + `registerInstrumentations`. CJS: `node --require ./tracing.js`, or `NODE_OPTIONS="--require …"`. ESM needs **both** `--experimental-loader=@opentelemetry/instrumentation/hook.mjs` and `--import ./telemetry.js` (opentelemetry-js `doc/esm-support.md`, fetched 2026-10-10). In `main.ts`, the tracing import must come **before** `@nestjs/core`, `@nestjs/platform-*`, `fastify` and `express` | `auto-instrumentations-node` ships 39 instrumentations, including `http`, `undici` (native `fetch`), `kafkajs`, `amqplib`, `aws-sdk`, `pg`, `mysql2`, `ioredis`, `redis`, `knex`, `nestjs-core`, `pino` and `winston`. `fs` and `host-metrics` are off by default. There is **no BullMQ and no Fastify entry** (package README, fetched 2026-10-10). MikroORM queries ride the driver's instrumentation (`pg`, `mysql2`, `knex`) | BullMQ with no `telemetry: new BullMQOtel(…)` on the `Queue` **and** the `Worker`. BullMQ's own telemetry captures the context into the job and restores it in the worker (docs.bullmq.io *Telemetry*, fetched 2026-10-10). Whether the worker span is a child or a link, and the minimum `bullmq` version, are not stated: [K?]. Also a hand-picked `instrumentations: [...]` list that omits a client in use, a module-scope `setInterval` that drains request-queued work, and manual `propagation.inject` into a header allow-list | none tracing-aware; greps |
| **Python** (FastAPI, Django, Flask; Gunicorn, Uvicorn; Celery) | `opentelemetry-instrument` wrapper or a code `TracerProvider`. `BatchSpanProcessor` is not fork-safe under pre-fork servers: with `preload_app`, build the provider in Gunicorn `post_fork` (OTel Python *Working with fork process models*, fetched 2026-10-10) | Instrumentors per client: `requests`, `httpx`, `aiohttp-client`, `celery`, `kafka-python`/`confluent-kafka`, `pika`/`aio-pika`, `botocore`, `threading` [K]. `start_as_current_span` defaults are `record_exception=True`, `set_status_on_exception=True`, `end_on_exit=True` (API reference, fetched 2026-10-10; precedents § 25). `asyncio.to_thread` copies the context [K] | `ThreadPoolExecutor`, `threading.Thread`, `run_in_executor` with no `contextvars.copy_context()` and no `ThreadingInstrumentor` (R8c); `tracer.start_span(` outside `with`; Celery with no instrumentor | ruff has no tracing rule |
| **Go** | `sdktrace.NewTracerProvider` in `main`, with `defer tp.Shutdown(ctx)` | `otelhttp.NewHandler` / `NewTransport` (pkg.go.dev, fetched 2026-10-10: `NewTransport` wraps a `RoundTripper`. `http.DefaultClient` and `http.Get` are not wrapped). `context.WithoutCancel` (precedents § 26) | R8a `context.Background()/TODO()` outside `main`/tests; R8b `tracer.Start` with no `defer span.End()`; `http.DefaultClient`; a span name from `fmt.Sprintf` | golangci-lint `contextcheck` (non-inherited context), `noctx` (missing `context.Context`), `spancheck` |
| **Java / Kotlin** (Spring Boot, Micronaut, Quarkus) | `-javaagent:opentelemetry-javaagent.jar` (Dockerfile, `JAVA_TOOL_OPTIONS`, manifest), or a manual `OpenTelemetrySdk`, or Micrometer Tracing | The agent instruments executors and injects MDC ids (precedents § 28) | R8d `Executors.new*` with no `Context.taskWrapping(…)` / `Context.current().wrap(…)` (both exist in `opentelemetry-context`, read from source 2026-10-10) and no agent; `GlobalScope.launch` with no `asContextElement()` [K]; `span.end()` outside `finally` | Error Prone / PMD have no tracing rule |
| **.NET** | `AddOpenTelemetry().WithTracing(…)` hosting (disposes on shutdown [K]); a manual `Sdk.CreateTracerProviderBuilder()` must be disposed | `Task.Run` and `new Thread` flow `Activity.Current` (precedents § 27) | `ExecutionContext.SuppressFlow()` (suppresses the execution context's flow to async threads: Microsoft Learn, fetched 2026-10-10); `ThreadPool.UnsafeQueueUserWorkItem`; `StartActivity(` not in `using`; `StartActivity($"…")` | the CA rules have no tracing rule |
| **Vendors** | `dd-trace`: `require('dd-trace').init()` first, or `--require dd-trace/init`; `ddtrace-run`. New Relic: `-r newrelic`. Elastic: `elastic-apm-node/start` first | the vendor auto-instrumentation | Sampling knobs (§9): dd-trace-py ≥ 3 reads `DD_TRACE_SAMPLING_RULES`, not `DD_TRACE_SAMPLE_RATE` (precedents § 48) | — |
| **Ruby / PHP** | `opentelemetry-instrumentation-all` + `use_all`; PHP auto-instrumentation | Sidekiq middleware [K] | `Thread.new` with no context capture [K?]; a long-running PHP worker with no per-job scope detach [K?] | — |

## Lint lane

Go only. Run in `${TMPDIR:-/tmp}` against the module, never committing a config. The research pinned golangci-lint 2.14.0 and spancheck 0.6.5. spancheck checks `end` by default; `record-error` and `set-status` must be listed (jjti/go-spancheck README, fetched 2026-10-10):

```bash
L="$(mktemp -d "${TMPDIR:-/tmp}/tps-lint.XXXXXX")"; printf 'version: "2"\nlinters:\n  default: none\n  enable: [contextcheck, noctx, spancheck]\n  settings:\n    spancheck:\n      checks: [end, record-error, set-status]\n' > "$L/golangci.yml"
golangci-lint run -c "$L/golangci.yml" --output.json.path "$L/out.json" ./... ; echo "exit=$?"
```

Keep only `contextcheck` (→ §1), `noctx` (→ §3) and `spancheck` (→ §4). `contextcheck` is noisy on `WithoutCancel` [R]: read each hit against precedents § 26. The lane needs a Go toolchain. Without one it prints `blocked (lane not installed: golangci-lint@2.14.0)` in the §1, §3 and §4 cells, and greps 1a, 3a and 4b still run.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is the gate and context. Every `rg` names its path (`.`): given no path, rg reads stdin under an agent's shell and reports a silent zero. Any rg exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L`, which is `--follow`. `scripts/` is not excluded: a script a cron container runs is production. A CLI is a decoy (precedents § 44), read per hit.

```bash
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,target,bin,obj,vendor,.venv,venv,__pycache__,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,playwright,cypress}/**'
   -g '!**/*.{spec,test,e2e,stories,story}.*' -g '!**/*_test.go' -g '!**/test_*.py' -g '!**/conftest.py'
   -g '!**/{migrations,migration,seeders,seeds,db/migrate,alembic/versions}/**' -g '!**/{locales,locale,i18n,translations,messages,lang}/**'
   -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock}' -g '!**/*.min.*')
J=(-g '*.{ts,tsx,js,jsx,mjs,cjs}'); PY=(-g '*.py'); GO=(-g '*.go'); JV=(-g '*.{java,kt,kts}'); CS=(-g '*.cs')
CODE=(-g '*.{ts,tsx,js,jsx,mjs,cjs,py,go,java,kt,kts,cs,rb,php}')
RUN=(-g '**/Dockerfile*' -g '**/*.dockerfile' -g '**/Procfile*' -g '**/package.json' -g '**/*.{yml,yaml,env,toml,ini,cfg,conf,sh,properties}' -g '**/.env*' -g '**/gunicorn*.py'
     -g '!**/node_modules/**' -g '!**/.github/**' -g '!**/{test,tests,__tests__,e2e,fixtures,__fixtures__,testdata}/**' -g '!**/{pnpm-lock,package-lock}.*')
DOCS=(-g '*.{md,mdx,adoc,rst,txt}' -g '!**/node_modules/**' -g '!**/{CHANGELOG,changelog}*' -g '!**/.claude/skills/**' -g '!**/.claude/agents/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
# 0a GATE: tracer dependencies and versions (OTel, Datadog, New Relic, Elastic, Micrometer Tracing; Sentry and bullmq-otel listed for 0b/§2)
rg -n --no-heading --pcre2 '"(?:@opentelemetry/[\w-]+|dd-trace|newrelic|elastic-apm-node|@sentry/[\w-]+|bullmq-otel|@fastify/otel)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(?:opentelemetry-[\w-]+|ddtrace|newrelic|sentry-sdk|elastic-apm)\b' -g '**/{requirements*.txt,pyproject.toml,Pipfile,setup.cfg}' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '^\s*(?:require\s+)?(?:go\.opentelemetry\.io/(?:otel|contrib)\S*|(?:github\.com|gopkg\.in)/DataDog/dd-trace-go\S*|github\.com/newrelic/go-agent\S*)\s+v\d' -g '**/go.mod' .
rg -n --no-heading --pcre2 '<artifactId>(?:opentelemetry-[\w-]+|micrometer-tracing[\w-]*|dd-trace-api)</artifactId>|["\x27](?:io\.opentelemetry[\w.:-]*|io\.micrometer:micrometer-tracing[\w:.-]*)|PackageReference\s+Include="(?:OpenTelemetry[\w.]*|Datadog\.Trace[\w.]*)"|\bgem\s+["\x27](?:opentelemetry-[\w-]+|ddtrace|datadog)["\x27]|"open-telemetry/[\w-]+"\s*:' -g '**/{pom.xml,*.gradle,*.gradle.kts,*.csproj,Directory.Packages.props,Gemfile,composer.json}' -g '!**/node_modules/**' .
# 0b GATE: zero-code wiring and tracing switches in run config (agent, wrappers, preloads, exporter endpoints, tracker tracing keys)
rg -n --no-heading --pcre2 '\bJAVA_TOOL_OPTIONS\b|-javaagent:|\bopentelemetry-instrument\b|\bddtrace-run\b|\bNODE_OPTIONS\b|--(?:require|import|experimental-loader)\b|\bOTEL_(?:EXPORTER_OTLP\w*|TRACES_EXPORTER|SDK_DISABLED)\b|\bDD_TRACE_ENABLED\b' "${RUN[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:tracesSampleRate|tracesSampler|traces_sample_rate|traces_sampler|enableTracing|enable_tracing)\b' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
# 0c process types and their start commands (§5): Dockerfile, Procfile, package.json scripts, compose / k8s command, gunicorn
rg -n --no-heading --pcre2 '^\s*(?:CMD|ENTRYPOINT)\b|^\s*"(?:start|start:prod|serve|worker|start:worker)"\s*:|^(?:web|worker|clock|release)\s*:\s*\S|^\s*-?\s*(?:command|entrypoint|args)\s*:|\bpreload_app\b|--preload\b|\bdef\s+post_fork\b' "${RUN[@]}" . | "${NC[@]}"
# 1a Go: a fresh root context outside main and tests (R8a)
rg -n --no-heading --pcre2 '\bcontext\.(?:Background|TODO)\(\)' "${GO[@]}" -g '!**/main.go' "${X[@]}" . | "${NC[@]}"
# 1b Python: thread / executor hops in files that never copy the context (R8c); 1c Java/Kotlin executors and GlobalScope with no wrapping (R8d)
rg -l0 --pcre2 '\b(?:ThreadPoolExecutor|ProcessPoolExecutor|threading\.Thread)\(|\.run_in_executor\(' "${PY[@]}" "${X[@]}" . | xargs -0 -r rg --files-without-match --pcre2 'copy_context\(|ThreadingInstrumentor'
rg -l0 --pcre2 '\bExecutors\.new\w+\(|\bnew\s+Thread\(|\bGlobalScope\.(?:launch|async)\b' "${JV[@]}" "${X[@]}" . | xargs -0 -r rg --files-without-match --pcre2 'Context\.(?:taskWrapping|current\(\)\.wrap)\(|asContextElement\('
# 1d .NET flow suppressed; 1e Node: a module-scope timer draining work that request code queued (spans become roots)
rg -n --no-heading --pcre2 '\bThreadPool\.UnsafeQueueUserWorkItem\(|\bExecutionContext\.SuppressFlow\(' "${CS[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '^(?:setInterval|setImmediate|queueMicrotask)\(|^(?!process\.)\w+\.on\(\s*["\x27]\w+["\x27]' "${J[@]}" "${X[@]}" . | "${NC[@]}"
# 2a producers and 2b consumers per client; 2c manual inject / extract and client instrumentation present
rg -l0 --pcre2 'from\s+["\x27](?:bullmq|bull|@nestjs/bullmq|@nestjs/bull)["\x27]|require\(\s*["\x27](?:bullmq|bull)["\x27]' "${J[@]}" "${X[@]}" . | xargs -0 -r rg -H -n --no-heading --pcre2 '\.add(?:Bulk)?\(\s*["\x27`\[]'
rg -n --no-heading --pcre2 '\b\w*(?:[Qq]ueue|[Ff]low[Pp]roducer)\w*\.add(?:Bulk)?\(|\bproducer\.send(?:Batch)?\(|\.(?:publish|sendToQueue)\(|\bnew\s+SendMessage(?:Batch)?Command\(|\b\w*(?:sqs|SQS|queue|Queue)\w*\.send_message\(|\.(?:delay|apply_async)\(|\.perform_async\(|\bkafkaTemplate\.send\(|\brabbitTemplate\.convertAndSend\(|\.WriteMessages\(|\.PublishWithContext\(' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\bnew\s+Worker\(|@Processor\(|\bconsumer\.run\(|\.consume\(|\bnew\s+ReceiveMessageCommand\(|@(?:\w+\.)?(?:task|shared_task)\b|@(?:Kafka|Rabbit|Sqs|Jms)Listener\b|\.ConsumeClaim\(|\.FetchMessage\(|\.ReadMessage\(' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\bpropagation\.(?:inject|extract)\(|\bpropagate\.(?:inject|extract)\(|GetTextMapPropagator\(\)\.(?:Inject|Extract)\(|\btelemetry\s*[,:}]|\bBullMQOtel\b|\b(?:Celery|Kafka|Pika|AioPika|Botocore|Boto3SQS|Requests|HTTPX\w*|AioHttpClient|Threading)Instrumentor\b|@opentelemetry/instrumentation-(?:kafkajs|amqplib|aws-sdk|undici|http|pg|mysql2|ioredis|redis)' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
# 3a Go outbound with no otelhttp transport; 3b Python client libraries (compare with the 0a instrumentors); 3c JS hand-picked instrumentation lists; 3d header allow-lists on manual propagation
rg -l0 --pcre2 '\bhttp\.(?:Get|Post|PostForm|Head)\(|\bhttp\.DefaultClient\b|&http\.Client\{' "${GO[@]}" "${X[@]}" . | xargs -0 -r rg -H -n --no-heading --pcre2 '\bhttp\.(?:Get|Post|PostForm|Head)\(|\bhttp\.DefaultClient\b|&http\.Client\{(?![^}\n]*otelhttp)' | rg -v --pcre2 'otelhttp\.NewTransport'
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(?:requests|httpx|aiohttp|urllib3|grpcio|psycopg2?(?:-binary)?|psycopg|asyncpg|pymongo|redis|sqlalchemy|celery|kafka-python|confluent-kafka|pika|aio-pika|boto3)\b' -g '**/{requirements*.txt,pyproject.toml,Pipfile}' -g '!**/node_modules/**' .
rg -n --no-heading --pcre2 '\binstrumentations\s*:\s*\[(?!\s*getNodeAutoInstrumentations)|\benabled\s*:\s*false\b' "${J[@]}" "${X[@]}" . | "${NC[@]}"
rg -l0 --pcre2 '\bpropagation\.inject\(|\bpropagate\.inject\(|GetTextMapPropagator\(\)\.Inject\(' "${CODE[@]}" "${X[@]}" . | xargs -0 -r rg -H -n --no-heading --pcre2 '\b(?:pick|omit)\w*\(|\b[A-Z_]*(?:ALLOW|FORWARD|WHITELIST|PASS)[A-Z_]*HEADERS?\b|\bnew\s+Headers\(\s*\)'
# 4a manual span starts (read: ended on every exit, error recorded in the catch); 4b Go start with no deferred End (R8b); 4c catch blocks with no recordException / setStatus in span files
rg -n --no-heading --pcre2 '\.startSpan\(|\btracer\.start_span\(|\bspanBuilder\([^\n]*\)\s*\.startSpan\(\)|\.startSpan\(\)|^\s*(?!using\b)[\w<>?]+\s+\w+\s*=\s*\w+\.StartActivity\(' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading -U --pcre2 '\b(\w+)\s*:?=\s*[\w.]+\.Start\([^\n]*\n(?!\s*defer\s+\1\.End\(\))' "${GO[@]}" "${X[@]}" . | rg --pcre2 '\.Start\('
rg -l0 --pcre2 '\.start(?:Active)?Span\(|\bstart_span\(|\.startSpan\(\)' "${CODE[@]}" "${X[@]}" . | xargs -0 -r rg -H -n --no-heading -U --pcre2 '\b(?:catch\s*(?:\([^)\n]*\))?\s*\{|except\b[^\n]*:\s*\n)(?:(?!\b(?:recordException|record_exception|setStatus|set_status)\b)(?:[^{}]|\{[^{}]*\}))*?(?:\}|\n\s*\n)' | rg --pcre2 '\b(?:catch|except)\b'
# 5a JS SDK bootstrap files and every import of them (order vs @nestjs/core, fastify, express); ESM packages
rg -n --no-heading --pcre2 '\bnew\s+NodeSDK\(|\bnew\s+NodeTracerProvider\(|\bregisterInstrumentations\(|\bsdk\.start\(\)|require\(\s*["\x27]dd-trace["\x27]\s*\)\.init\(|^import\s+["\x27]dd-trace/init["\x27]' "${J[@]}" "${X[@]}" . | "${NC[@]}"
rg -l0 --pcre2 '^(?:import\s+|require\(\s*)["\x27](?:\.{1,2}/(?:[\w./-]*/)?(?:tracing|instrumentation|otel|telemetry)(?:\.[cm]?[jt]s)?|dd-trace(?:/init)?)["\x27]' "${J[@]}" "${X[@]}" . | xargs -0 -r rg -H -n --no-heading --pcre2 '^import\s+(?:[^\n]*\bfrom\s+)?["\x27](?:@nestjs/core|@nestjs/platform-\w+|fastify|express|koa|@hapi/hapi|\.{1,2}/(?:[\w./-]*/)?(?:tracing|instrumentation|otel|telemetry)(?:\.[cm]?[jt]s)?|dd-trace(?:/init)?)["\x27]|^require\(\s*["\x27](?:\.{1,2}/(?:[\w./-]*/)?(?:tracing|instrumentation|otel|telemetry)(?:\.[cm]?[jt]s)?|dd-trace(?:/init)?)["\x27]'
rg -l0 --pcre2 '"(?:@opentelemetry/(?:sdk-node|sdk-trace-node|auto-instrumentations-node)|dd-trace|newrelic|elastic-apm-node)"\s*:' -g '**/package.json' -g '!**/node_modules/**' . | xargs -0 -r rg -H -n --no-heading --pcre2 '"type"\s*:\s*"module"'
# 5b Python: provider + batch processor at import time in a preloaded server (pair with 0c preload_app / post_fork)
rg -n --no-heading --pcre2 '^\w[^\n]*\bBatchSpanProcessor\(|^\w+\s*=\s*TracerProvider\(' "${PY[@]}" "${X[@]}" . | "${NC[@]}"
# 5c flush: SDK / provider / logger files with no shutdown, sync or flush; exit right after a log (precedents § 44 for CLIs)
rg -l0 --pcre2 '\bnew\s+NodeSDK\(|\bNodeTracerProvider\(|sdktrace\.NewTracerProvider\(|\bOpenTelemetrySdk\.builder\(|\bSdk\.CreateTracerProviderBuilder\(|\bzap\.New\w*\(|\bpino\.destination\(\s*\{[^}\n]*sync\s*:\s*false' "${CODE[@]}" "${X[@]}" . | xargs -0 -r rg --files-without-match --pcre2 '\.shutdown\(|\.Shutdown\(|\.forceFlush\(|\.ForceFlush\(|\.Sync\(\)|\.flushSync\(|\.close\(\)|\bDispose\(|\bAddOpenTelemetry\('
rg -n --no-heading -U --pcre2 '\b(?:logger|log|this\.logger|slog|zap\.L\(\))\.\w+\([^\n]*\n(?:[^\n]*\n)?\s*\K(?:process\.exit|os\.Exit|sys\.exit|System\.exit)\(' "${CODE[@]}" "${X[@]}" .
# 6a propagators (env and code) and 6b service identity, per service
rg -n --no-heading --pcre2 '\bOTEL_PROPAGATORS\b|\btextMapPropagator\s*:|\bnew\s+(?:B3|Jaeger|W3CTraceContext|Composite)Propagator\(|\bset_global_textmap\(|\bSetTextMapPropagator\(' "${CODE[@]}" "${RUN[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\bOTEL_SERVICE_NAME\b|\bOTEL_RESOURCE_ATTRIBUTES\b[^\n]*service\.name|\bserviceName\s*:|\bATTR_SERVICE_NAME\b|SERVICE_NAME\b\s*[\]:=,]|["\x27]service\.name["\x27]|\bDD_SERVICE\b|^\s*service_name\s*[:=]|\bspring\.application\.name\b|\bsemconv\.ServiceName(?:Key)?\b|\.AddService\(|-Dotel\.service\.name=' "${CODE[@]}" "${RUN[@]}" "${X[@]}" . | "${NC[@]}"
# 7 span names built from data (template literal, f-string, concatenation, Sprintf, interpolated C#)
rg -n --no-heading --pcre2 '\.start(?:Active)?Span\(\s*(?:`[^`\n]*\$\{|["\x27][^"\x27\n]*["\x27]\s*\+)|\bstart_(?:as_current_)?span\(\s*(?:f["\x27]|["\x27][^"\x27\n]*["\x27]\s*(?:%|\.format\())|\.Start\(\s*[\w.()]+\s*,\s*(?:fmt\.Sprintf\(|"[^"\n]*"\s*\+)|\bspanBuilder\(\s*(?:"[^"\n]*"\s*\+|String\.format\()|\bStartActivity\(\s*\$"|\.(?:updateName|update_name|SetName)\(\s*(?:`[^`\n]*\$\{|f["\x27]|fmt\.Sprintf)' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
# 8a deprecated semconv names in code and in the dashboards / rules that read them; 8b the declared dual-emit window
rg -n --no-heading --pcre2 '["\x27](?:http\.(?:url|method|status_code|target|scheme|host|user_agent|flavor)|net\.(?:peer|host)\.(?:name|port)|db\.(?:statement|operation)|db\.system(?!\.name)|deployment\.environment(?!\.name))["\x27]|\b(?:SemanticAttributes|SemanticResourceAttributes)\.(?:HTTP_(?:URL|METHOD|STATUS_CODE|TARGET)|DB_STATEMENT|DEPLOYMENT_ENVIRONMENT)\b|\bSEM(?:RES)?ATTRS_(?:HTTP_(?:URL|METHOD|STATUS_CODE|TARGET)|DB_STATEMENT|DEPLOYMENT_ENVIRONMENT)\b' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\b(?:http_method|http_status_code|http_url|http_target|http\.method|http\.status_code)\b' -g '**/*.{json,yml,yaml,jsonnet,libsonnet}' -g '!**/node_modules/**' -g '!**/package*.json' -g '!**/{test,tests,fixtures}/**' .
rg -n --no-heading --pcre2 '\bOTEL_SEMCONV_STABILITY_OPT_IN\b' "${CODE[@]}" "${RUN[@]}" "${X[@]}" .
# 9a ratio samplers (read: inside ParentBased?); 9b AlwaysOn / rate 1.0 (R9a); 9c Datadog sample rate knobs (dd-trace-py ≥ 3 ignores DD_TRACE_SAMPLE_RATE, precedents § 48)
rg -n --no-heading --pcre2 '\bTraceIdRatioBased(?:Sampler)?\(|\bTraceIDRatioBased\(|\btraceIdRatioBased\(|OTEL_TRACES_SAMPLER\b[\s"\x27]*[=:]\s*["\x27]?traceidratio\b|^\s*-?\s*value:\s*["\x27]?traceidratio\b' "${CODE[@]}" "${RUN[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\bAlwaysSample\(\)|\bAlwaysOnSampler\b|\bSampler\.alwaysOn\(\)|\bALWAYS_ON\b|\balways_on\b|\btracesSampleRate\s*:\s*1(?:\.0+)?\b|\btraces_sample_rate\s*=\s*1(?:\.0+)?\b|\bsampling\.probability\s*[:=]\s*1(?:\.0+)?\b' "${CODE[@]}" "${RUN[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '\bDD_TRACE_SAMPLE_RATE\b|\bDD_TRACE_SAMPLING_RULES\b' "${CODE[@]}" "${RUN[@]}" "${X[@]}" .
# 10a the stated error-retention requirement (project docs, ADRs, SLO docs, rules); 10b head-ratio values and tail policies; 10c sampler env per service; 10d sampling before span-derived metrics
rg -n --no-heading -i --pcre2 '\b100\s*%\s*(?:of\s+)?(?:error|failed)\w*|\b(?:all|every)\s+(?:error|failed)\w*\s+(?:\w+\s+){0,3}(?:trace[ds]?|sampled|kept|retained)\b|\balways[- ]sample[- ]errors?\b' "${DOCS[@]}" .
rg -n --no-heading --pcre2 '\bOTEL_TRACES_SAMPLER(?:_ARG)?\b|\btail_sampling\s*:|\bstatus_code\s*:|\bprobabilistic_sampler\s*:|\bsampling_percentage\s*:|\b(?:spanmetrics|servicegraph)\s*:' "${RUN[@]}" -g '!**/k8s/dev*/**' -g '!**/*{dev,local,test}*.*' .
rg -l0 --pcre2 '\b(?:probabilistic_sampler|tail_sampling)\s*:' -g '*.{yml,yaml}' -g '!**/node_modules/**' . | xargs -0 -r rg -H -n --no-heading --pcre2 '^\s*processors:\s*\[[^\]\n]*\b(?:probabilistic_sampler|tail_sampling)\b|^\s*exporters:\s*\[[^\]\n]*\b(?:spanmetrics|servicegraph)\b'
```

Reading the output:
- **0a/0b are the gate** (§ The SDK gate).
- **0c is the process map**: every process type, and the command that starts it.
- The **file-level lines** (1b/1c, 4c, 5c) list files, not lines. Read each whole.
- A k8s `- name: OTEL_*` hit carries its value on the next line. Read it before comparing services in §6, §9 and §10.

Two blind spots are structural, so work around them instead of trusting a quiet grep:
- **A hop behind a helper.** A wrapper such as `this.bus.emit(…)`, `enqueue(…)` or `runInBackground(…)` hides the producer or the executor from greps 1 and 2. For each consumer in 2b, follow back to whoever enqueues for it.
- **A preload outside the repo.** The real start command may live in a Helm chart, a platform buildpack or a PaaS setting. When 0c shows no command for a process type, §5 is `Unconfirmed (start command not in the repo)`, with the probe: print the running container's command line.

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample: 48 files over Node (NestJS + Fastify, ESM worker), Python (FastAPI + Gunicorn + Celery), Go, Java (bare and with agent), .NET, `deploy/` (compose, k8s prod and dev, collector, Grafana), ADRs, Sentry, plus a no-SDK sub-repo | Whole script 0.54 s, 123 output lines, 0 rg errors. **All 40 seeded positives surface** in their § (TR-01 ×5, TR-02 ×3 producer/consumer pairs, TR-03 ×3, TR-04 ×4, TR-05 ×3, LG-06 ×3, TR-06, TR-07 ×5, TR-08 ×2, TR-09 ×2, SA-01 ×4, SA-02, SA-03 ×2, SA-04 ×2). 8 decoys never appear: `WithoutCancel`, `Task.Run`, `asyncio.to_thread`, `start_as_current_span`, `startActiveSpan` with `finally`, Go `defer span.End()`, a `tracesSampler`, `parentbased_traceidratio` in env. 11 decoys appear and are cleared by the read step, each by one precedent or one 0a/0b line: the agent-instrumented executor (§ 28), kafkajs and SQS (both in the auto list), BullMQ with `BullMQOtel` on both sides, a header allow-list above an instrumented `fetch`, two CLI `process.exit` calls (§ 44), a multi-line `ParentBasedSampler({ root: … })`, and three dev or non-prod rate-1.0 configs (§ 33) |
| No-SDK sub-repo alone | Gate closed (0a and 0b empty). Exactly 4 lines: 5c (an async pino destination with no flush + `process.exit` after `fatal`, plus a CLI decoy) and 10a (an ADR requiring every error traced). Everything else prints `N/A (no tracing SDK)` |
| `benchmarks/fixtures/*` (15 fixtures) | **Gate closed in all 15**: no OTel, Datadog, New Relic or Elastic dependency, and no tracing key. 27 lines in total, all context: 0c 19 (start commands), 1a 1, 1e 1 (a rate-limiter cleanup timer), 3 6 (client libraries), 5 and 10 0. They print, but they are not graded. Two FP classes were fixed before shipping: 5a framework imports in files that never import a tracer (38 → 0), and a `"type": "module"` in frontend packages (11 → 0, now scoped to packages that depend on a tracer). Also an smtplib `send_message` (2a, now scoped to queue/SQS receivers) and a Procfile alternative that matched an indented `release:` label |
| Sibling seeded trees for `log-signal-scan` and `alert-rule-lint` | 10 lines, all on their own trees' tracer bootstraps and queue consumers. 0 in rule YAML after the Procfile fix |
| Real repository (eval § 3.7) | Not available at the read-only path on 2026-10-10. The row stays open: the gate result, init order against `main.ts`, BullMQ propagation and the `pg` instrumentation MikroORM rides on are unmeasured |
| Lint lane | `blocked (lane not installed: golangci-lint@2.14.0)`: no Go toolchain on the measuring host. The v2 config shape above is [K?] until it runs |

## The 3,000-hit path

1. **Intersect** with the process map (0c) and the entry points: routes, consumers, cron, workers. A hop in code that no production process type starts is dismissed with one read. Name the directory in the coverage block.
2. **Group** by root cause: one SDK bootstrap (§5, §9), one wrapper (an HTTP client factory, a queue helper, a tracing decorator), one queue client (§2), one executor factory (§1), one manifest family (§6, §10).
   Fifty `queue.add` calls through one `QueueService` with no telemetry are **one** finding with fifty sites (precedents P4).
3. **Rank:**
   - payment, auth, checkout and consumer paths first;
   - then any hop the declared incident tool relies on (a runbook that says "open the trace");
   - then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once.** Wire the in-memory exporter into the existing integration or e2e suite (§ Proof). Count orphan roots: spans with no parent, whose name is not an entry-point span. Count unended spans and distinct traceIds per test request. Each orphan names its hop.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a production path and an open gate. Raise a §5 row to **BLOCKER** only when tracing is the declared incident tool (a runbook, an ADR or the SLO doc says so) and the oracle shows zero spans.

| § | Classes | Default severity |
|---|---|---|
| 1 | TR-01 context lost across in-process async | high on a payment, auth or consumer path; else medium |
| 2 | TR-02 queue hop without inject/extract | high |
| 3 | TR-03 outbound HTTP/DB client uninstrumented, or a wrapper drops `traceparent` | medium; high on a cross-service critical path |
| 4 | TR-04 span never ended, or error not recorded | medium; high when the unended span is a request or consumer root |
| 5 | TR-05 SDK initialised late or in the wrong process; LG-06 telemetry not flushed on exit | high (zero traces, silently); flush medium, high in serverless and on crash paths |
| 6 | TR-06 propagator mismatch; TR-09 service identity missing or shared | medium |
| 7 | TR-07 span name from data; boundary span kind unset | medium |
| 8 | TR-08 deprecated semconv names | medium |
| 9 | SA-01 ratio without ParentBased; SA-03 AlwaysOn / rate 1.0 in production | SA-01 medium; SA-03 low–medium (cost) |
| 10 | SA-02 100 % errors required, only head sampling; SA-04 sampler drift, sampling before span metrics | medium |

### 1. Context lost across an in-process async hop (TR-01)

```
BAD:   go notifyWarehouse(context.Background(), id)                       // Go: new root, the request trace ends here
       loop.run_in_executor(pool, render_pdf, oid)                          # Python: no context in the pool thread
       Executors.newFixedThreadPool(4).submit(() -> …)                      // Java, no agent, no wrapping
       using (ExecutionContext.SuppressFlow()) { ThreadPool.QueueUserWorkItem(…); }   // .NET
       setInterval(() => drain(buffer), 1000)                                // Node: request work runs under the timer's context
GOOD:  go notifyWarehouse(context.WithoutCancel(ctx), id)  ·  ctx = contextvars.copy_context(); loop.run_in_executor(pool, ctx.run, f, oid)
       Context.taskWrapping(Executors.newFixedThreadPool(4))  ·  Task.Run(…)  ·  capture context.active() at enqueue, restore with context.with()
```
**Read the code:**
- Does the hop run work a request started, or is it a true root, like a cron tick or a startup task? A root is correct, not TR-01.
- Is the detachment deliberate and still trace-carrying (`WithoutCancel`, precedents § 26)?
- Is the Java agent in the runtime config (0b, § 28)? Is `ThreadingInstrumentor` enabled (0a)?
- Does .NET flow by default here (§ 27)?
- In Node, does the drained buffer carry a captured context? If it does not, every span in the timer is an orphan root.

**Finding when** request-originated work runs on the hop with no context carried. **Proof (V194):** the exporter shows the hop's span with a different traceId, or no parent, while the request span is still open.

### 2. Queue hop without inject / extract (TR-02)

```
BAD:   await this.queue.add('capture', { orderId })                 // BullMQ, no telemetry option: the worker starts a new trace
       send_receipt.delay(oid)                                         # Celery with no CeleryInstrumentor
       ch.sendToQueue('notifications', buf)  ·  ch.consume('refunds', …)   // amqplib, not in a hand-picked instrumentation list
GOOD:  new Queue('orders', { connection, telemetry: new BullMQOtel('api') }) + the same on new Worker(…)
       CeleryInstrumentor().instrument() in both the producer and the worker process
       propagation.inject(context.active(), headers) on publish; context.with(propagation.extract(ROOT_CONTEXT, msg.properties.headers), handle)
```
**Read the code:**
- Which client, and which version? Does auto-instrumentation cover it in **this** process? `auto-instrumentations-node` covers kafkajs, amqplib and aws-sdk (SQS), but a hand-picked list (grep 3c) may not.
- BullMQ is never covered by the auto list. Is `telemetry` set on **both** the `Queue` and the `Worker`? With one side only, the trace still splits.
- Is the consumer run in the same process type as an instrumented producer, or in a separate worker that never loads the SDK (§5)?
- Is a link the intended design, because a batch consumer has one span per batch? A link is a pass (V194).

**Finding when** a producer and its consumer are both reachable and the consumer span neither has the producer as parent nor links to it. **Proof (V194):** HTTP → enqueue → consume in one test with the in-memory exporter. Assert one traceId with correct parentage, or a link. Run it against a real broker (testcontainers, or a local Redis for BullMQ). A mocked queue proves nothing about headers.

### 3. Outbound HTTP or DB client uninstrumented, or a wrapper drops `traceparent` (TR-03)

```
BAD:   http.DefaultClient.Get(url)                                    // Go: no otelhttp transport
       new NodeSDK({ instrumentations: [new HttpInstrumentation()] }) + fetch(…)   // native fetch is undici: not in the list
       requests.get(…) with no RequestsInstrumentor and no opentelemetry-instrument wrapper
       headers: pick(carrier, ['content-type', 'authorization'])      // manual inject, then an allow-list drops traceparent
GOOD:  &http.Client{Transport: otelhttp.NewTransport(http.DefaultTransport)} · getNodeAutoInstrumentations() · RequestsInstrumentor().instrument()
```
**Read the code:**
- **Is the transport instrumented?** In Node, the `http` and `undici` instrumentations inject at the transport. A header object rebuilt *above* an instrumented transport cannot drop `traceparent`, so that hit is Refuted. The allow-list breaks the trace only when propagation is manual, or when the transport is uninstrumented.
- Is each DB driver in deps also in the instrumentation set? MikroORM, TypeORM and Knex ride `pg`/`mysql2`.
- For a gateway that forwards inbound headers, does it forward `traceparent`/`tracestate`?

**Finding when** a reachable outbound call or query emits no client span, or the downstream server span's parent is not the client span. **Proof (V194):** a local downstream (an `http.createServer` sink or `httptest.Server`) records the received `traceparent`. Assert its trace id equals the caller's, and that the exporter holds a CLIENT span for the call.

### 4. Span never ended, or the error not recorded (TR-04)

```
BAD:   const span = tracer.startSpan(`capture ${id}`); try { await pay(); span.end(); } catch (e) { throw e; }   // no end, no status on failure
       ctx, span := tracer.Start(ctx, "x"); if err != nil { return }   … span.End()                          // early return leaks it
       span = tracer.start_span("load")  # never ended
GOOD:  tracer.startActiveSpan('payments.capture', async (span) => { try { … } catch (e) { span.recordException(e); span.setStatus({ code: SpanStatusCode.ERROR }); throw e; } finally { span.end(); } })
       ctx, span := tracer.Start(ctx, "x"); defer span.End()  ·  with tracer.start_as_current_span("load"):
```
**Read the code:**
- Is `end()` on **every** exit: return, throw, `finally`, `defer`?
- Does each catch that owns a span record the exception and set ERROR?
- Python `start_as_current_span` records and sets status by default (precedents § 25). A missing `record_exception` there is Refuted.
- Is the swallow itself the defect? Then it is code-quality's (§ Boundaries).

**Finding when** a reachable path leaves a span open, or returns an error from a span left UNSET. **Proof (V195):** drive the failing path with the exporter wired in. Every span finished; the failing span has `status=ERROR` and an `exception` event. An unended span never reaches the exporter, so the test asserts the expected count.

### 5. SDK initialised late or in the wrong process; telemetry not flushed on exit (TR-05, LG-06)

```
BAD:   CMD ["node", "dist/main.js"]  +  main.ts: import '@nestjs/core' … import './tracing'      // modules load before the hooks: no server spans
       "start": "node --import ./otel.js src/index.js"  with "type": "module" and no loader hook  // ESM imports unpatched
       preload_app = True  +  BatchSpanProcessor built at import  +  no post_fork               // pre-fork servers: not fork-safe
       new NodeSDK(…) with no sdk.shutdown() on SIGTERM  ·  tp := sdktrace.NewTracerProvider(…) with no defer tp.Shutdown(ctx)
       logger.fatal({ err }, 'listen failed'); process.exit(1)   with an async destination        // the line that explains the crash is lost
GOOD:  CMD ["node", "--require", "./dist/tracing.js", "dist/main.js"]  ·  import './tracing' as the first line of main.ts
       node --experimental-loader=@opentelemetry/instrumentation/hook.mjs --import ./otel.js src/index.js
       build the TracerProvider inside gunicorn post_fork  ·  process.on('SIGTERM', () => sdk.shutdown())  ·  defer tp.Shutdown(ctx); defer logger.Sync()
```
**Read the code:**
- Which command starts each production process type (0c, plus Helm values or the platform setting)? Does it preload the bootstrap, or is the bootstrap the first import?
- Is a Lambda layer, `opentelemetry-instrument`, `ddtrace-run` or the Java agent doing the init? That is the decoy.
- Is the package ESM (5a)? Then it needs both flags.
- Does a worker process type (BullMQ, Celery, cron) load the SDK at all?
- On exit, does the process call shutdown or flush before `process.exit`/`os.Exit`? `os.Exit` skips `defer` [K].
- `pino.destination({ sync: false })` plus `process.exit` losing the last line is [K?]: the captured-log run settles it.
- A CLI or one-shot script is precedents § 44.

**Finding when** the first production request yields no server span, or the last span or log line before SIGTERM never reaches the sink. **Proof (V196):** spawn the real start command with the OTLP endpoint pointed at a local sink, serve one request, then assert server spans exist. Send SIGTERM and assert the sink got the last span and the last log line.

### 6. Propagator mismatch; service identity missing or shared (TR-06, TR-09)

```
BAD:   api: OTEL_PROPAGATORS=b3   while every other service keeps the default tracecontext,baggage
       py-svc: no OTEL_SERVICE_NAME, no Resource service.name   →  unknown_service:python
       go-svc and jvm-svc both OTEL_SERVICE_NAME=backend
GOOD:  one propagator set everywhere (tracecontext,baggage, or tracecontext,b3multi on both sides of a B3-only edge); one distinct name per service
```
**Read the code:**
- Build the per-service table from 6a/6b and 0c: service, its propagators, its name, and its source file.
- Compare **only the config each service's production process loads** (gate 7).
- Is there an edge proxy or a legacy service that only speaks B3? Then `tracecontext,b3multi` on both sides is the correct design.
- `serviceName` in code counts.

**Finding when** two services on one call path use disjoint propagators, or a production process's resource is `unknown_service*` or shares a name with another service. **Proof (V196):** the cross-service test shows the downstream parent missing, or the exporter resource names `unknown_service`. The static two-ended trace (both env blocks cited) is `[report-flagged]`.

### 7. Span name from data; boundary span kind unset (TR-07)

```
BAD:   tracer.startSpan(`capture ${orderId}`) · start_span(f"load user {uid}") · tracer.Start(ctx, fmt.Sprintf("order %s", id))
       spanBuilder("export " + reportId) · StartActivity($"ship {orderId}")
GOOD:  tracer.startSpan('payments.capture', { attributes: { 'order.id': orderId } })   // the id is an attribute, never the name
```
**Read the code:**
- Is the interpolated part a route template or a bounded enum (a decoy), or an id, email or path?
- Do manual spans around a queue publish, a consume or an outbound call set `kind` (PRODUCER, CONSUMER, CLIENT)? Unset means INTERNAL, which breaks service graphs and span metrics.
- An id in a span *attribute* is correct (precedents § 19).

**Finding when** a name takes unbounded values, or a boundary span is INTERNAL. **Proof (V194):** 100 requests with random ids leave the set of exported span names at the number of operations.

### 8. Deprecated semantic-convention names (TR-08)

```
BAD:   span.setAttribute('http.url', u) · a Grafana panel `sum by (http_method)` over span metrics · `deployment.environment` in the Resource
GOOD:  url.full · http.request.method · http.response.status_code · deployment.environment.name — or a declared OTEL_SEMCONV_STABILITY_OPT_IN=http/dup window
```
**Read the code:**
- Which names does the installed instrumentation emit at its version and opt-in (8b)?
- Which dashboards, alerts and recording rules read the old name (8a, second grep)?
- A declared dual-emit window is precedents § 46.
- Never assert what an instrumentation emits from memory: dump the attributes in the exporter test.

**Finding when** code writes a deprecated name with no dual-emit window, or a consumer reads a name the installed instrumentation no longer emits (an empty view). **Proof (V194):** Weaver `registry live-check --fail-on violation` reports `deprecated`, or the exporter dump lacks the name the dashboard reads.

### 9. Ratio sampler without ParentBased; AlwaysOn or rate 1.0 in production (SA-01, SA-03)

```
BAD:   new TraceIdRatioBasedSampler(0.1) · sdktrace.TraceIDRatioBased(0.1) · Sampler.traceIdRatioBased(0.2) · OTEL_TRACES_SAMPLER=traceidratio
       web/src/instrument.ts tracesSampleRate: 1.0 · sentry_sdk.init(…, traces_sample_rate=1.0) loaded by production
GOOD:  new ParentBasedSampler({ root: new TraceIdRatioBasedSampler(0.1) }) · sdktrace.ParentBased(sdktrace.TraceIDRatioBased(0.1)) · parentbased_traceidratio
       a tracesSampler by route · rate 1.0 only in a dev file, or on a low-RPS service with a stated budget (precedents § 33)
```
**Read the code:**
- Is the ratio wrapped? A multi-line `ParentBasedSampler({ root: … })` is the decoy grep 9a still prints.
- Is the file the production process loads (gate 7)? A dev manifest or `settings_dev.py` is noise.
- Which Datadog tracer reads `DD_TRACE_SAMPLE_RATE` (precedents § 48)?
- For SA-03: the request rate × 1.0 × spans per request, priced by finops `candidate-pricing` §0 when installed.

**Finding when** a production service's resolved sampler is a bare ratio, or samples everything with no stated budget. **Proof (V197):** a config-load test prints the resolved sampler's description, which must contain `ParentBased`. For SA-03, the span-count arithmetic.

### 10. Errors required but only head-sampled; sampler drift; sampling before span metrics (SA-02, SA-04)

```
BAD:   docs/adr/0007: "we keep 100% of error traces"  +  SDK ratio 0.1  +  no tail_sampling status_code policy  +  no tracker capture
       worker OTEL_TRACES_SAMPLER_ARG=0.1, py-svc 0.5                       // one trace, two decisions
       traces pipeline: [memory_limiter, probabilistic_sampler, batch] → exporters: [spanmetrics]   // RED metrics computed on 10 %
GOOD:  a collector tail_sampling policy on status_code ERROR (with trace-id load balancing in front, telemetry-config-scan's) · one sampler per call graph
       spanmetrics/servicegraph fed before any sampling processor, or consistent sampling with adjusted counts
```
**Read the code:**
- **Where is the requirement stated (10a)?** A project ADR, SLO doc, runbook or rule makes it a requirement. If the only source is this pack's installed `observability-principles` default line, the row is Hardening, listed once, unless a project document repeats it.
- Does an error tracker capture every error on the same paths (`error-tracking-scan` rows)? Then the requirement is met by the tracker.
- Do services on one call graph resolve to different samplers?
- Does any sampling processor sit before the `spanmetrics`/`servicegraph` connector?

**Finding when** the stated requirement has no mechanism that keeps error traces, or span-derived metrics are computed on sampled spans. **Gate closed:** only the requirement half runs. A requirement with neither a tracer nor a tracker prints `requirement <source> has no mechanism (no tracing SDK, no tracker capture)`, medium. **Proof (V197):** send N error traces through the configured SDK ratio and the collector config, and count the retained ones against the requirement. For SA-04, the static two-ended trace: the processor list and the connector, both cited.

## Proof — the in-memory exporter

The oracle, its per-stack exporter and the assertions are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *In-memory span exporter*, with variants **V194** (async, queue, outbound, names, semconv), **V195** (lifecycle), **V196** (init, identity, flush) and **V197** (sampling). The per-stack exporters: JS `InMemorySpanExporter` + `SimpleSpanProcessor` passed in the provider constructor (SDK 2.x removed `addSpanProcessor`: opentelemetry-js *Upgrade to 2.x*, fetched 2026-10-10); Python `InMemorySpanExporter`; Go `tracetest.NewSpanRecorder()`; Java `InMemorySpanExporter`; .NET `AddInMemoryExporter(list)`.

The shape:
1. Wire the exporter into the test harness the repo already runs: `fastify.inject` or supertest, `TestClient`, `httptest`, MockMvc, `WebApplicationFactory`. Use the **same bootstrap file production uses**, so §5 is exercised too.
2. Drive the real entry point **across the hop**: HTTP → enqueue → consume against a real broker; HTTP → outbound to a local sink; HTTP → executor.
3. Assert:
   - one traceId;
   - each child's parent, or a link;
   - every span ended;
   - ERROR plus an `exception` event on the failure path;
   - span names from a closed set;
   - resource `service.name` ≠ `unknown_service*`.
4. The test **fails on the unfixed code**. A test that passes before the fix proves nothing; rebuild it until it fails.

For §5, spawn the production command against a local OTLP sink and send SIGTERM. For §8, use Weaver `registry live-check` (SIGHUP, then the exit code). Without a harness, the row is `[report-flagged]` / Unconfirmed, with the test written out.

## Output

```
trace-propagation-scan — gate: open (api/package.json:11 @opentelemetry/sdk-node 0.206.0; py-svc/requirements.txt:4 opentelemetry-sdk 1.37.0; go.mod otel v1.38.0)
Lanes: node (NestJS 11 + Fastify, ESM worker), python (FastAPI + gunicorn + celery), go, java (agent in jvm-agent-svc only), .net · lint lane: blocked (golangci-lint@2.14.0)
Processes: api (Dockerfile:6), worker (package.json:5), py-svc (Dockerfile:5 gunicorn, preload_app), go-svc, jvm-svc, jvm-agent-svc

Findings: 2 · Unconfirmed: 3

1. api/src/main.ts:3                                             [report-with-fix]   high
   §5 TR-05 — `import './tracing'` follows `@nestjs/core` (:1) and `@nestjs/platform-fastify` (:2), and the
   production command api/Dockerfile:6 `node dist/main.js` has no --require. Proof: e2e boot with the in-memory
   exporter — GET /orders yields 0 SERVER spans (fails). Fix: CMD ["node","--require","./dist/tracing.js","dist/main.js"].

2. api/src/orders/orders.producer.ts:9 · api/src/orders/order.processor.ts:4      [report-with-fix]   high
   §2 TR-02 — BullMQ queue and worker with no `telemetry`; the auto list has no BullMQ entry. Proof: HTTP → add →
   worker against local Redis: 2 traceIds, consumer span has no parent and no link (fails).
   Fix: telemetry: new BullMQOtel('api') on both the Queue and the Worker.

3. deploy/docker-compose.yml:18 · py-svc/app/main.py (no Resource)                [report-flagged]   medium
   §9 SA-01 + §6 TR-09 — py-svc resolves `traceidratio` (not parent-based) and no service name.
   Unproven link: no Python harness run. Settling test: resolved sampler description + exporter resource name.

Verification: 41 candidates → 2 findings · 3 unconfirmed · 4 hardening · 0 pre-existing · 32 refuted (self-verified)

Class coverage:
  gate  tracing SDK                    open (4 tracers, 6 process types)
  §1  async context (TR-01)           checked (5 hits → 1 finding; 1 refuted by -javaagent)
  §2  queue hop (TR-02)               checked (7 producers / 5 consumers → 1 finding; kafkajs, SQS covered by auto list)
  §3  outbound / DB (TR-03)           checked (5 hits → 0 findings; partner allow-list sits above instrumented undici)
  §4  span lifecycle (TR-04)          checked (5 hits → 0 findings) · Live, unreviewed (2 groups — rerun 4c on jvm-svc)
  §5  init order + flush (TR-05, LG-06)  checked (3 processes → 1 finding)
  §6  propagators + identity          checked (7 config lines → 1 flagged)
  §7  span names / kind               checked (5 hits → 0 findings; route-template names)
  §8  semconv                         checked (2 hits → 1 unconfirmed: dashboard reads http_method)
  §9  ParentBased / AlwaysOn          checked (10 hits → 1 flagged; 3 dev configs refuted)
  §10 error retention / drift         checked (1 requirement, 1 drift)
```

`[report-with-fix]`: the hop is traced from the entry point, the exporter test failed, and the fix is local to the project's tracer or start command. `[report-flagged]`: one link is unproven (no harness, a start command outside the repo, a version the lockfile leaves ambiguous); the row names it and the settling test.

The coverage block lists the gate and **all ten** §s on every run:
- `checked (k hits → m findings)` only when the grep ran on an open gate;
- `N/A (no tracing SDK)` on a closed gate, except §5's flush half and §10's requirement half;
- `blocked (<reason>)` when a grep failed or a lane could not install;
- `Live, unreviewed (k groups / n hits)` for a partial review, never `checked`.

## False positives / precedents

The verifier reads [`precedents/observability.md`](../../../../snippets/precedents/observability.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 25** Python `start_as_current_span` records the exception, sets ERROR and ends the span by default (re-verified against the OTel Python API reference, 2026-10-10).
- **§ 26** Go `context.WithoutCancel` keeps the trace on detached work.
- **§ 27** .NET `Task.Run` / `new Thread` flow the context.
- **§ 28** The Java agent instruments executors.
- **§ 33** Rate 1.0 with a per-route `tracesSampler`, in a non-production file, or on a low-RPS service with a stated budget is not SA-03.
- **§ 44** `process.exit` in a CLI is not LG-06.
- **§ 46** A declared `OTEL_SEMCONV_STABILITY_OPT_IN=*/dup` window is not TR-08.
- **§ 48** dd-trace-py ≥ 3 ignores `DD_TRACE_SAMPLE_RATE`: gate the row on the tracer.
- **§ 18** Health routes excluded from tracing are correct.
- **§ 19** An id in a span attribute is correct.

Two rules of verdict discipline hold:
- **§ 36:** a claim only a backend can settle, such as the trace volume or the retained error count in production, is `NO-DATA(<source>)`, never an estimate.
- **§ 37:** an attribute, span or service name a finding or a fix cites must resolve in the repo or the exporter dump.

Two shapes this skill must not report:
- **A header allow-list above an instrumented transport** (§3 read). The transport injects after the wrapper runs.
- **An auto-covered client** (kafkajs, amqplib, aws-sdk in the auto list) in a process that loads the auto list. Check the process (§5) before clearing it.

## When to run

- On any diff that touches a tracer bootstrap, a start command (Dockerfile `CMD`, `package.json` scripts, Procfile, compose, k8s), a queue producer or consumer, an HTTP client factory, an executor or goroutine spawn, a sampler setting, or `OTEL_*` env. This is `/obs-audit`'s "a tracer, SDK init or queue client" dispatch signal.
- On every whole-repo `/obs-audit`, reporting the gate and all ten §s.
- After `/add-tracing`, or any agent-written instrumentation: the exporter test is the acceptance check.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier must not be the run that found it, and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/observability.md`.
  - Under `/obs-audit`, that happens in its verification phase.
  - Run standalone, apply the protocol as a second pass and tag those rows `self-verified`.
  - List the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- **Halt before any § when the gate is unread.** Without the 0a/0b result printed, no row may be graded.
- **Halt on any finding missing its anchors:** the break `<file:line>`, the hop, the entry point and the fix in the project's tracer.
- **No `[report-with-fix]` without an exporter test that failed**, or a SIGTERM sink run for §5. Without one, the row is `[report-flagged]` / Unconfirmed.
- **No proposed fix may sample errors away or switch tracing off** (`always_off`, a ratio of `0`, `OTEL_SDK_DISABLED=true`, removing a span), and none may silence the lint lane (`//nolint:spancheck|contextcheck`).
- **Do not assert what an instrumentation covers or emits from memory.** A coverage claim cites the lockfile version and the package's list, or the exporter dump.
- **Do not print "tracing looks fine" without the coverage block.** A § whose grep did not run is `blocked`, never `checked`.
- **Do not re-derive a class another skill owns** (§ Boundaries). Cross-link it.

## Related

- `/obs-audit` dispatches this skill and folds its coverage block into the Tracing and Sampling ledger rows. `/obs-fix` closes findings with the failing-first exporter test, the fix at the bootstrap or wrapper, a re-run of this detector, and the sibling search.
- `/add-tracing` (this pack) builds instrumentation; its closing gate is this skill's exporter test across a queue hop.
- `log-signal-scan` (CO-03 trace ids in logs), `telemetry-config-scan` (collector pipeline) and `error-tracking-scan` (tracker capture) are this pack's neighbours.
- `@observability-reviewer` judges these rows in refute mode. `ai-patterns/tracing.md` holds the span-naming and propagation conventions the fixes follow.
- `chaos-test` and `dlq-replay` (distributed-systems pack, when installed) exercise the queue hops whose traces §2 joins.

## Sources

Fetched 2026-10-10: the OpenTelemetry SDK environment-variable spec (sampler and propagator defaults); semantic conventions `service.name` (the `unknown_service:` fallback); opentelemetry-js `doc/esm-support.md` and `doc/upgrade-to-2.x.md`; the `auto-instrumentations-node` README (39 instrumentations); docs.bullmq.io *Telemetry* (getting started, traces); the OTel Python API reference (`start_as_current_span`) and *Working with fork process models*; pkg.go.dev `otelhttp` v0.72.0; the jjti/go-spancheck README; golangci-lint linter settings (`contextcheck`, `noctx`); opentelemetry-java `Context.java` (`taskWrapping`, `wrap`); Microsoft Learn `ExecutionContext.SuppressFlow`. Carried from the observability research catalog and the batch-4 eval: the R8a–R8d and R9a regexes, the lint-lane versions and OTelBench (2026-01). Paraphrased; no text reproduced beyond identifiers.
