---
name: metric-hygiene-scan
description: "Metric and probe defects: unbounded labels, unmetered jobs, unit/bucket misfit, lying readiness — scrape-proved."
kind: skill
pack: observability
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: metric-hygiene-scan

## Premise

A metric fails on-call in two ways. It can take down the store that holds it: one raw URL or user id as a label adds a series per value, and the TSDB runs out of memory during the incident it should explain. Or it can mislead quietly. A cron job with no counter fails for a week unseen. Milliseconds land in a `_seconds` histogram, so every sample falls in `+Inf` and the latency SLI reads 0 %. A summary is averaged across replicas into a percentile that means nothing. A readiness route answers 200 while its database is down, and kubelet probes inflate the request rate the dashboards show. None of these breaks a build, and every one looks like a healthy service.

This skill finds those defects in code and run config for the metric clients real repos use: prom-client (directly, through `@willsoto/nestjs-prometheus` or through `fastify-metrics`), the OpenTelemetry metrics API, StatsD/DogStatsD, Python `prometheus_client`, Go `client_golang`, Java Micrometer and .NET `System.Diagnostics.Metrics` / prometheus-net. It also covers the health routes those apps expose. It proves each defect with a **registry scrape** driven through the real entry point. It owns `/obs-audit`'s Metrics (§1–§6) and Health (§7–§8) rows (`ownership.json` rows `obs-metrics`, `obs-health`). `@observability-reviewer` (this pack) judges its rows.

**Every finding cites the metric or route `<file:line>`, the entry point that feeds it (route, consumer, cron, probe), what the scrape then shows (an unbounded series count, a sample in `+Inf`, no series at all, a 200 from a dead dependency), the oracle that showed it or the test that would settle it, and the fix in the project's own client.** A grep hit is a candidate. "Metrics look fine" is never printed; the output is the class-coverage block (§ Output). Verification follows [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/observability.md`](../../../../snippets/precedents/observability.md). The oracles are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *Registry scrape*, variants V198–V201. Label budgets come from `THR-OBS-CARDINALITY` (`templates/governance/thresholds.json`).

## The metrics gate — run before any §

Pre-flight 0a and the metric-file set `METRIC_PATHS` decide whether the repo registers metrics at all. The gate is **open** when 0a prints a metrics client or `METRIC_PATHS` is non-empty. Print `gate: open (<file:line>)` or `gate: closed (no metrics library)` in the header.

**Gate closed.** §1–§6 print `N/A (no metrics library)`. §7 and §8 still run: a readiness route that lies, and probe traffic in traces and request logs, need no metrics client. A repo with no metrics at all is a design gap for `/add-metrics` (this pack), not a finding of this detector.

## The rule

A candidate is a finding when all four hold. These are the protocol's gates as `precedents/observability.md` § Reading the seven gates applies them to metrics.

1. **A production path feeds it.** A route, consumer, cron or worker that a production process type starts registers or observes the metric, or a probe the deploy config points at calls the route. A metric in a CLI, a test helper or dead code is dismissed with one read.
2. **Nothing already bounds or covers it.** No route-template label (precedents § 29), no wrapper or explorer that meters the entry point (grep 2c), no `/1000` conversion, no `getSingleMetric` guard, no exclusion at the source or in every consuming selector.
3. **The version has the behaviour.** The client major is read from the lockfile (gate 3). Examples: prom-client 15 throws on a second registration of one name; `prometheus_client` adds `_total` to counter names; the OTel → Prometheus name translation depends on the server (precedents § 43).
4. **The scrape showed it, or the trace is two-ended.** The registry scrape after randomized ids holds an unbounded series, the sample lands in the wrong bucket, the entry point's counter does not move, or `/readyz` answers 200 with the dependency stopped. Or, for a static-fact class (§3 bucket edge vs SLO threshold, §4 summary across replicas, §6 consumer set-diff), both ends are cited. That case is `[report-flagged]` until the scrape runs.

## Boundaries

- **Liveness that checks a shared dependency** → performance `request-path-scan` §15 (V47), when the performance pack is installed. Grep 7c lists those handlers as routed and never grades them. Without that pack, the row is tagged `liveness on a shared dependency (owner pack not installed)`, listed and never graded (precedents P2). This skill owns only the lying *readiness* (§7) and probe pollution (§8).
- **Probe manifests** (whether `readinessProbe` / `livenessProbe` / `startupProbe` exist, their paths, timings and `terminationGracePeriodSeconds`) → infrastructure `k8s-availability-scan` §2 (probes) and §7 (the grace period), when the infrastructure pack is installed. This skill reads a manifest only to learn which path is readiness and which is liveness.
- **Alert rules that read a metric** → `alert-rule-lint` (this pack). A selector that names no registered series is its §4 (AL-10). §6 here is the converse: a registered metric that nothing reads. Both use one inventory; neither re-derives the other.
- **An SLO's latency threshold with no matching bucket** is shared with `slo-rule-scan` §5 (this pack). §3 reports it when the **bucket list** is the fix; `slo-rule-scan` reports it when the SLI is. Dedupe by `file:line`.
- **Probe lines in request logs** (pino-http with no `autoLogging.ignore`) → `log-signal-scan` §5 (LG-05, this pack). Grep 8b lists the logger surface as corroboration and credits that row.
- **Loki label maps and collector-side cardinality** → `telemetry-config-scan` §4. **Dashboard lint** → `telemetry-config-scan` §8. Grep 8c reads dashboard selectors only for probe filters.
- **A sensitive value as a label** (an email, a token): the cardinality half stays here (precedents § 19); the value policy is security `data-exposure-scan` § 6, when the security pack is installed. **Public health details** (`show-details: always`) → `data-exposure-scan` § 3.
- **Readiness during the shutdown drain** → devops (the code chain), when the devops pack is installed.
- **Series cost in money** → finops `candidate-pricing` §0 prices it when installed; every §1 row carries the series arithmetic (its quantity × unit).

## Adapt to the codebase — the metric lanes

Read every client, wrapper and health library **with its version** from the lockfile or manifest (0a). Print the lanes you ran in the header. *Read from the package tarball 2026-10-10* marks a fact read in that version's published source. `[K]` is established but not re-read. `[K?]` is unverified: a row that rests on one is Unconfirmed until its settling test runs.

| Lane | Clients and wrappers | Bounded-label decoys | Shapes to grep | Health and probes |
|---|---|---|---|---|
| **Node** (NestJS 10/11 on Express or Fastify, Fastify 5, Express) | prom-client 15; `@willsoto/nestjs-prometheus` 7 (`makeCounterProvider`, `@InjectMetric`, a default `/metrics` controller; no HTTP RED metrics of its own); `fastify-metrics` 14; `express-prom-bundle`; `@opentelemetry/api` meters; `hot-shots` (DogStatsD) | Fastify `request.routeOptions.url` (the template); `fastify-metrics` labels routes by `routeOptions.config.statsId ?? routeOptions.url` and skips unknown routes by default; Express `req.route?.path` | `labelNames` holding ids; `.labels(request.url)`; `observe(Date.now() - t)`; `new Counter(` in a handler. prom-client 15.1.3: default histogram buckets `0.005 … 10` s, a second registration of one name throws *already been registered*, `Counter.inc` rejects a negative value (all read from the package tarball 2026-10-10) | `@nestjs/terminus` 11: `HealthCheckService.check([])` with an empty list resolves `status: 'ok'` (200); any failed indicator or the shutdown state answers 503 (read from the package tarball 2026-10-10) |
| **Python** (FastAPI, Django, Flask; Celery) | `prometheus_client`, `prometheus-fastapi-instrumentator`, `django-prometheus`, OTel meters, `datadog` | `request.scope["route"].path` (Starlette template) [K]; the instrumentator templates by default [K] | `labels(request.url.path)`, `labels(error=str(e))`; `observe((time.time() - t) * 1000)`; `Counter(` inside a `def` (re-registration raises) [K]; counters gain `_total` on exposition [K] | a FastAPI/Django view returning `{"ok": True}` |
| **Go** | `client_golang` (`New*Vec`, `promauto`, `promhttp`) | chi `RoutePattern()`, gorilla `GetPathTemplate()` [K] | `WithLabelValues(r.URL.Path)`; `Observe(float64(time.Since(t).Milliseconds()))`; `MustRegister` outside `init`/`main`/a constructor (panics on duplicate) [K]; `DefBuckets` = the same 0.005–10 s [K] | a handler that only writes `http.StatusOK` |
| **JVM** (Spring Boot, Micronaut) | Micrometer + `micrometer-registry-prometheus`, actuator | Spring's `http.server.requests` tags the templated `uri` [K] | `Tag.of("uri", request.getRequestURI())`; `Timer.builder(…).publishPercentiles(…)` with no `publishPercentileHistogram()` (client-side percentiles do not aggregate) [K] | actuator probe groups; `management.endpoint.health.group.*` |
| **.NET** | `System.Diagnostics.Metrics` (`Meter.CreateCounter`), prometheus-net, OTel | `http.route` on ASP.NET Core's `http.server.request.duration` [K] | a tag fed by `HttpContext.Request.Path` | `MapHealthChecks(path)` with no `Predicate` runs every registered check, the DB included [K] |
| **Ruby / PHP** | Yabeda; promphp `getOrRegisterCounter` | yabeda-rails controller/action tags [K] | `tags:` fed by `request.path` [K?] | — |

## Tool lane

`promtool check metrics` lints an exposition: naming, units, `_total` on counters. Feed it a scrape from the registry test (§ Proof) or a running instance, never production:

```bash
L="$(mktemp -d "${TMPDIR:-/tmp}/mhs.XXXXXX")"; curl -fsS "http://127.0.0.1:${METRICS_PORT:?}/metrics" > "$L/scrape.txt"
promtool check metrics < "$L/scrape.txt"; echo "exit=$?"      # 0 clean · 3 lint (naming) · 1 error (precedents § 53)
promtool check metrics --extended < "$L/scrape.txt" | head -40  # series per metric: the §1 arithmetic
```

The research pinned promtool from Prometheus 3.15.0; golangci-lint 2.14.0 `promlinter` is the Go naming lane. Keep only the naming and cardinality lines (→ §1, §5). Without the binary, print `blocked (lane not installed: promtool@3.15.0)` in the §1 and §5 cells, and greps 1 and 5c still run.

## Pre-flight greps

Run as **one** script from the repo root. Grep **N** feeds detector **§N**; grep 0 is the gate and context. Every `rg` names its path: `.`, or the arrays `METRIC_PATHS` and `CONSUMER_PATHS`, each guarded non-empty, because rg with no path reads stdin and reports a silent zero. Any rg exit 2 is a failed grep, never zero hits. File-level greps use `--files-without-match`, never `rg -L` (`--follow`). `METRIC_PATHS` is the set of files that touch metrics: those importing a client, plus files importing a module that registers metrics (a project `metrics.registry.ts`). Greps 1b, 1c, 2c, 3c and 6 read only `METRIC_PATHS`, which is what keeps response bodies, log fields and rate limiters out.

```bash
X=(-g '!**/node_modules/**' -g '!**/{dist,build,out,target,bin,obj,vendor,.venv,venv,__pycache__,coverage,.next,.nuxt,.output,generated,__generated__}/**'
   -g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,playwright,cypress}/**'
   -g '!**/*.{spec,test,e2e,stories,story}.*' -g '!**/*_test.go' -g '!**/test_*.py' -g '!**/conftest.py'
   -g '!**/{migrations,migration,seeders,seeds,db/migrate,alembic/versions}/**' -g '!**/{locales,locale,i18n,translations,messages,lang}/**'
   -g '!**/{docs,ai,.claude}/**' -g '!*.{md,mdx,snap,lock}' -g '!**/*.min.*')
J=(-g '*.{ts,tsx,js,jsx,mjs,cjs}'); PY=(-g '*.py'); GO=(-g '*.go'); CODE=(-g '*.{ts,tsx,js,jsx,mjs,cjs,py,go,java,kt,kts,cs,rb,php}')
CFG=(-g '*.{yml,yaml,json,jsonnet,libsonnet,alloy,river,tf}' -g '!**/node_modules/**' -g '!**/{vendor,charts/*/charts}/**' -g '!**/package*.json' -g '!**/tsconfig*.json' -g '!**/{test,tests,__tests__,fixtures,testdata}/**' -g '!**/.github/**' -g '!**/{locales,locale,i18n,translations,messages,lang}/**')
NC=(rg -v --pcre2 '^[^:]+:\d+:\s*(?://|/\*|\*(?:\s|/|$)|#)')
MET='\.(?:inc|dec|observe|startTimer|labels|record|increment|decrement|timing|histogram|distribution|gauge|time)\(|\.(?:Inc|Add|Observe|Set)\(|\bWithLabelValues\(|\bmetrics?\.\w|\bMetrics\.\w|\bmeter\.\w|\bstatsd\.\w|@Timed\b|@Counted\b|\bTimer\.(?:start|builder)|\bregistry\.(?:counter|timer|gauge)\('
# METRIC_PATHS: files importing a metrics client, then files importing a module that registers metrics
METRIC_PATHS=(); while IFS= read -r f; do METRIC_PATHS+=("$f"); done < <(rg -l --pcre2 'from\s+["\x27](?:prom-client|@willsoto/nestjs-prometheus|@opentelemetry/api|hot-shots)["\x27]|require\(\s*["\x27](?:prom-client|hot-shots)["\x27]|^\s*(?:from|import)\s+(?:prometheus_client|datadog)\b|"github\.com/prometheus/client_golang/prometheus(?:/promauto)?"|^import\s+io\.micrometer\.|\bSystem\.Diagnostics\.Metrics\b|^using\s+Prometheus\b|\bopentelemetry\.metrics\b|\bmetrics\.getMeter\(' "${CODE[@]}" "${X[@]}" .)
MB=$([ "${#METRIC_PATHS[@]}" -gt 0 ] && rg -l --pcre2 '\bnew\s+(?:\w+\.)?(?:Counter|Gauge|Histogram|Summary)\b|\b(?:Counter|Gauge|Histogram|Summary)\(\s*["\x27]|\bmake(?:Counter|Gauge|Histogram|Summary)Provider\(|\bcreate(?:Counter|Histogram|UpDownCounter|Gauge)\(|\bNew\w+Vec\(' "${METRIC_PATHS[@]}" | while read -r f; do b="${f##*/}"; b="${b%.*}"; printf '%s\n' "${b//./\\.}"; done | sort -u | paste -sd'|' -)
[ -n "$MB" ] && while IFS= read -r f; do case " ${METRIC_PATHS[*]} " in *" $f "*) ;; *) METRIC_PATHS+=("$f");; esac; done < <(rg -l --pcre2 "(?:from|import|require\\()\\s*[\"']\\.{1,2}/(?:[\\w.-]+/)*(?:$MB)[\"']|^\\s*from\\s+[\\w.]*\\b(?:$MB)\\s+import\\b" "${CODE[@]}" "${X[@]}" .)
# 0a GATE: metrics and health libraries with versions (lanes, gate 3); 0b the dependencies a readiness must reflect
rg -n --no-heading --pcre2 '"(?:prom-client|@willsoto/nestjs-prometheus|fastify-metrics|express-prom-bundle|@opentelemetry/(?:api|sdk-metrics|sdk-node|exporter-prometheus)|hot-shots|node-statsd|@nestjs/terminus|@fastify/under-pressure)"\s*:\s*"[^"]+"' -g '**/package.json' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '^\s*["\x27]?(?:prometheus[-_]client|prometheus-fastapi-instrumentator|django-prometheus|starlette-exporter|datadog|opentelemetry-sdk|github\.com/prometheus/client_golang\S*|go\.opentelemetry\.io/otel/sdk/metric\S*)\b|<artifactId>(?:micrometer-registry-\w+|micrometer-core|spring-boot-starter-actuator)</artifactId>|["\x27]io\.micrometer:micrometer-[\w-]+|PackageReference\s+Include="(?:prometheus-net[\w.]*|OpenTelemetry\.Exporter\.Prometheus[\w.]*|AspNetCore\.HealthChecks[\w.]*)"' -g '**/{requirements*.txt,pyproject.toml,Pipfile,go.mod,pom.xml,*.gradle,*.gradle.kts,*.csproj,Directory.Packages.props}' -g '!**/node_modules/**' .
rg -n --no-heading -i --pcre2 '"(?:@mikro-orm/core|typeorm|@prisma/client|pg|mysql2|mongoose|ioredis|redis|bullmq|kafkajs|amqplib)"\s*:|^\s*(?:asyncpg|psycopg2?(?:-binary)?|psycopg|sqlalchemy|redis|celery|pymongo)\b|\b(?:github\.com/jackc/pgx\S*|gorm\.io/gorm|github\.com/redis/go-redis\S*)\s+v\d|<artifactId>(?:spring-boot-starter-data-\w+|postgresql|spring-kafka)</artifactId>|Include="(?:Npgsql[\w.]*|StackExchange\.Redis)"' -g '**/{package.json,requirements*.txt,pyproject.toml,go.mod,pom.xml,*.gradle,*.gradle.kts,*.csproj}' -g '!**/node_modules/**' .
# 0c consumers: rule, recording-rule, dashboard, SLO and analysis files (the §6 set-diff, the §3 thresholds, §8c)
CONSUMER_PATHS=(); while IFS= read -r f; do CONSUMER_PATHS+=("$f"); done < <(rg -l --pcre2 '^\s*-?\s*(?:alert|record|expr)\s*:|"(?:expr|query)"\s*:|kind:\s*(?:PrometheusRule|AnalysisTemplate|ServiceLevelObjective)|^\s*(?:slos|objectives)\s*:' "${CFG[@]}" .); [ "${#CONSUMER_PATHS[@]}" -gt 0 ] && printf '%s\n' "${CONSUMER_PATHS[@]}"
# 1a label NAMES unbounded by kind (R10a, widened to every lane); 1b label VALUES from the raw request or an error string (R10b, widened; § 29 is the decoy)
rg -n --no-heading -U --pcre2 '(?:labelNames\s*:\s*\[|labelnames\s*=\s*[\[(]|\bNew\w+Vec\([^\n]*\[\]string\{|\b(?:Counter|Gauge|Histogram|Summary)\(\s*["\x27][\w:]+["\x27]\s*,\s*["\x27][^"\x27\n]*["\x27]\s*,\s*[\[(]|\bTag\.of\(\s*|\.tags?\(\s*|\bTags\.of\(\s*)[^\]\})\n]*?["\x27](?:user_?id|userId|email|e_?mail|path|url|uri|request_?id|requestId|session_?id|sessionId|ip|client_?ip|token|trace_?id|traceId|span_?id|order_?id|orderId|customer_?id|customerId|tenant_?id|tenantId|error|message)["\x27]' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
[ "${#METRIC_PATHS[@]}" -gt 0 ] && rg -H -n --no-heading --pcre2 '(?:\.(?:labels|inc|dec|set|observe|startTimer|add|record|increment|timing|histogram|distribution|counter|timer)\(|\bWithLabelValues\(|\.With\(|\bTag\.of\(|\bTags\.of\(|\.tags?\(|\bKeyValuePair<)[^\n]*?(?:\b(?:req|request|ctx|c)\.(?:originalUrl|url|path|raw\.url)\b(?!\s*[(.]|\w)|\brequest\.url\.path\b|\br\.URL\.(?:Path|String\(\)|RawQuery)|\br\.RequestURI\b|\brequest\.(?:get_full_path\(\)|path_info)|\bgetRequestURI\(\)|\bRequest\.Path\b|\b(?:e|err|error|ex|exc)\.(?:message|Error\(\))|\bstr\(\s*(?:e|err|exc|ex)\s*\)|\bString\(\s*(?:e|err|error)\s*\))|[{,]\s*["\x27]?(?:route|path|url|uri|endpoint|handler|error|reason)["\x27]?\s*[:=]\s*(?:\b(?:req|request|ctx|c)\.(?:originalUrl|url|path|raw\.url)\b(?!\s*[(.]|\w)|\brequest\.url\.path\b|\br\.URL\.(?:Path|String\(\)|RawQuery)|\br\.RequestURI\b|\bgetRequestURI\(\)|\bRequest\.Path\b|\b(?:e|err|error|ex|exc)\.(?:message|Error\(\))|\bstr\(\s*(?:e|err|exc|ex)\s*\)|\bString\(\s*(?:e|err|error)\s*\))' "${METRIC_PATHS[@]}" | "${NC[@]}"
# 1c OTel meter attributes and StatsD/DogStatsD tags carrying ids or interpolations (PL-08)
[ "${#METRIC_PATHS[@]}" -gt 0 ] && rg -H -n --no-heading --pcre2 '\.(?:add|record|increment|decrement|gauge|timing|histogram|distribution|Add|Record)\([^\n]*(?:["\x27](?:\w+[._])?(?:user|order|session|request|customer|tenant|trace|account)[._]?id["\x27]\s*:|`[^`\n]*\$\{[^}\n]*\}`|\bf["\x27][^"\x27\n]*\{|tags\s*=\s*\[[^\]\n]*\{)' "${METRIC_PATHS[@]}"
# 2 entry points whose body moves no metric (cron, intervals, schedulers, queue workers, consumers, tasks); 2c the wrapper that may meter them all; 2b pools with no gauge
rg -n --no-heading -U --pcre2 '^[ \t]*(?:@(?:Cron|Interval|Timeout|Process|Processor|Scheduled|SqsMessageHandler|EventPattern|MessagePattern|KafkaListener|RabbitListener|JmsListener|SqsListener|shared_task|(?:\w+\.)?task|periodic_task)\b[^\n]*\n[^\n]*|[^\n]*\bnew\s+Worker\(\s*[^\n]*=>\s*\{|[^\n]*\b(?:cron\.schedule|schedule\.scheduleJob|consumer\.run|\.AddFunc)\([^\n]*)\n(?:(?![ \t]*(?:@|def |async def |func |public |private |protected ))(?![^\n]*(?:'"$MET"'))[^\n]*\n){0,40}?(?=[ \t]*(?:\}\)?;?[ \t]*$|@|def |async def |func |public |private |protected )|\z)' "${CODE[@]}" "${X[@]}" . | rg --pcre2 '^[^:]+:\d+:\s*(?:@(?:Cron|Interval|Timeout|Process|Processor|Scheduled|SqsMessageHandler|EventPattern|MessagePattern|KafkaListener|RabbitListener|JmsListener|SqsListener|shared_task|(?:\w+\.)?task|periodic_task)\b|.*\bnew\s+Worker\(|.*\b(?:cron\.schedule|scheduleJob|consumer\.run|AddFunc)\()'
[ "${#METRIC_PATHS[@]}" -gt 0 ] && rg -H -n --no-heading --pcre2 '\b(?:SchedulerRegistry|ScheduleExplorer|DiscoveryService|MetadataScanner|wrapFunctionInTryCatchBlocks)\b|\.on\(\s*["\x27](?:completed|failed)["\x27]|\bworker_(?:process_init|ready)\b|\b(?:task_prerun|task_postrun|task_failure)\b|@(?:Timed|Counted)\b|\babstract\s+class\s+\w+' "${METRIC_PATHS[@]}" | "${NC[@]}"
rg -l0 --pcre2 '\bnew\s+Pool\(|\bcreatePool\(|\bcreate_pool\(|\bcreate_async_engine\(|\bSetMaxOpenConns\(|\bnew\s+HikariDataSource\(|\bpgxpool\.New' "${CODE[@]}" "${X[@]}" . | xargs -0 -r rg --files-without-match --pcre2 "$MET|\bcollectDefaultMetrics\b|\bmetricsCollector\b"
# 3a a millisecond delta observed raw (R10c, plus the Python and Go shapes); 3b non-base-unit names; 3c every histogram and its buckets; 3d SLO thresholds (le literals)
rg -n --no-heading --pcre2 '\.observe\(\s*(?:\{[^\n]*value\s*:\s*)?\(?\s*(?:Date\.now\(\)|performance\.now\(\))\s*-\s*[\w.]+(?![\w.(])(?!\s*\)?\s*[/*])|\.observe\(\s*\(\s*time\.(?:time|perf_counter|monotonic)\(\)\s*-\s*\w+\s*\)\s*\*\s*1000|\.Observe\(\s*float64\(\s*time\.Since\([^)]*\)\.Milli(?:seconds)?\(\)\s*\)|\.(?:record|Record)\(\s*(?:Date\.now\(\)|performance\.now\(\))\s*-\s*\w+\s*[,)]' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '(?:\bname\s*:\s*|\bName:\s*|\b(?:Counter|Gauge|Histogram|Summary)\(\s*|\b(?:builder|counter|timer|summary|Create\w+<\w+>)\(\s*|createHistogram\(\s*)["\x27][\w.:]*[._](?:ms|millis|milliseconds|msec|us|micros|microseconds|minutes|hours|kb|mb|kilobytes|megabytes|percent)["\x27]' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
[ "${#METRIC_PATHS[@]}" -gt 0 ] && rg -H -n --no-heading --pcre2 '\bnew\s+(?:\w+\.)?Histogram\(|\bmakeHistogramProvider\(|\bHistogram\(\s*["\x27]|\bNewHistogram(?:Vec)?\(|\bHistogramOpts\b|\bbuckets\s*[:=]\s*(?:\[|\(|\w+Buckets\b|[A-Z][A-Z_]*BUCKETS\b|linearBuckets|exponentialBuckets)|\b[A-Z][A-Z_]*BUCKETS\s*=|\bBuckets:\s*(?:\[\]float64|prometheus\.)|\bDefBuckets\b|\b(?:Exponential|Linear)Buckets(?:Range)?\(|\bpublishPercentileHistogram\(|\bserviceLevelObjectives\(|\bCreateHistogram<|\b[Ee]xplicitBucketBoundaries\b|\badvice\s*:' "${METRIC_PATHS[@]}" | "${NC[@]}"
rg -n --no-heading --pcre2 '\bpercentiles-histogram\b|\bslo\.[\w.-]+\s*[:=]|\bpublishPercentileHistogram\b' -g '**/application*.{yml,yaml,properties}' -g '!**/{test,tests}/**' .
rg -n --no-heading -o --pcre2 '\w+_bucket\{[^}\n]*\ble\s*=~?\s*\\?["\x27][^"\x27\\]+|\ble\s*:\s*["\x27]?[0-9.]+\b' "${CFG[@]}" . | sort -u
# 4a a gauge named like a counter; 4b gauges only ever incremented; 4c summaries and client-side percentiles (replicas printed only when one exists)
rg -n --no-heading -U --pcre2 '\b(?:new\s+(?:\w+\.)?Gauge\(\s*\{\s*name\s*:|makeGaugeProvider\(\s*\{\s*name\s*:|Gauge\(|NewGauge(?:Vec)?\(\s*prometheus\.GaugeOpts\{[^}]*?Name:)\s*["\x27][\w:]*(?:_total|_count|_processed|_handled|_served)["\x27]' "${CODE[@]}" "${X[@]}" . | rg --pcre2 '_total|_count|_processed|_handled|_served'
rg -o -I --no-filename --no-heading --pcre2 '\b(?:(?:const|let|var|val)\s+|self\.)?\K\w+(?=\s*(?::\s*\w+(?:<[^>]*>)?)?\s*:?=\s*(?:new\s+)?(?:\w+\.)?(?:Gauge|NewGauge(?:Vec)?|makeGaugeProvider)\()' "${CODE[@]}" "${X[@]}" . | sort -u | while read -r g; do
  rg -q --pcre2 "\\b$g\\b[^\\n]*\\.(?:inc|Inc)\\(" "${CODE[@]}" "${X[@]}" . && ! rg -q --pcre2 "\\b$g\\b[^\\n]*\\.(?:dec|set|Dec|Set|Sub|set_function|set_to_current_time|track_inprogress)\\(" "${CODE[@]}" "${X[@]}" . && echo "4b gauge only incremented: $g"; done
rg -n --no-heading --pcre2 '\bnew\s+(?:\w+\.)?Summary\(|\bmakeSummaryProvider\(|\bSummary\(\s*["\x27]|\bNewSummary(?:Vec)?\(|\bpublishPercentiles\(|@Timed\([^)\n]*percentiles' "${CODE[@]}" "${X[@]}" . | "${NC[@]}"
rg -q --pcre2 '\bnew\s+(?:\w+\.)?Summary\(|\bmakeSummaryProvider\(|\bSummary\(\s*["\x27]|\bNewSummary(?:Vec)?\(|\bpublishPercentiles\(' "${CODE[@]}" "${X[@]}" . && rg -n --no-heading --pcre2 '^\s*(?:replicas|minReplicas|maxReplicas|replicaCount)\s*:\s*\d+' -g '*.{yml,yaml}' -g '!**/node_modules/**' .
# 5a registration inside a function body (module scope is column 0; the getSingleMetric ?? guard is the decoy); 5b Go registration with its enclosing func; 5c counters without _total
rg -n --no-heading --pcre2 '^[ \t]+(?!export\b)(?:(?:const|let|var|final)\s+\w+(?:\s*:\s*[\w<>]+)?\s*=\s*|\w+\s*=\s*|return\s+|this\.\w+\s*=\s*)?(?:new\s+(?:\w+\.)?(?:Counter|Gauge|Histogram|Summary)\b(?:<[^>]*>)?\(|(?:prometheus_client\.)?(?:Counter|Gauge|Histogram|Summary)\(\s*["\x27])(?![^\n]*\?\?)' "${J[@]}" "${PY[@]}" "${X[@]}" . | "${NC[@]}"
rg -n --no-heading --pcre2 '^\s+(?:prometheus\.(?:MustRegister|Register)\(|\w+\s*:?=\s*promauto\.New|prometheus\.New\w+\()' "${GO[@]}" "${X[@]}" . | while IFS=: read -r f l _; do awk -v L="$l" -v F="$f" 'NR<=L && /^func /{fn=$0} NR==L{print F":"L": in "fn; exit}' "$f"; done | rg -v --pcre2 'in func (?:init|main)\(\)|in func New\w*\('
rg -n --no-heading -U --pcre2 '(?:\bnew\s+(?:\w+\.)?Counter\(\s*\{\s*name\s*:|makeCounterProvider\(\s*\{\s*name\s*:|\bCounterOpts\{[^}]*?Name:)\s*["\x27](?![\w:]*_total["\x27])[\w:]+["\x27]' "${J[@]}" "${GO[@]}" "${X[@]}" . | rg --pcre2 'name\s*:|Name:'
# 6 dead metrics: names registered in METRIC_PATHS (dots → underscores, precedents § 43) that no consumer file (0c) names
if [ "${#METRIC_PATHS[@]}" -eq 0 ]; then echo "6: N/A (no metric registered in code)"; elif [ "${#CONSUMER_PATHS[@]}" -eq 0 ]; then echo "6: NO-DATA(no consumer file in the repo)"; else
  rg -U -o -I -r '$1' --no-filename --no-heading --pcre2 '(?:(?:^[ \t]*|[{,(][ \t]*)name\s*:\s*|\bName:\s*|\b(?:Counter|Gauge|Histogram|Summary|Info|Enum)\(\s*|\b(?:builder|counter|timer|gauge|summary)\(\s*|\bCreate\w+<\w+>\(\s*|\bcreate(?:Counter|Histogram|UpDownCounter|ObservableGauge|Gauge)\(\s*)["\x27]([A-Za-z_:][\w:.]*)["\x27]' "${METRIC_PATHS[@]}" | sort -u | while read -r n; do
    rg -q -F -e "$n" -e "${n//./_}" "${CONSUMER_PATHS[@]}" || echo "6: no consumer: $n"; done; fi
# 7a probe routes and health wiring; 7b readiness/health handlers answering a constant with no dependency touched first; 7c liveness touching a dependency (routed to performance §15)
rg -n --no-heading --pcre2 '@Controller\(\s*["\x27][\w/-]*health["\x27]|@(?:Get|GetMapping)\(\s*["\x27][\w/:-]*(?:health|healthz|ready|readyz|readiness|live|livez|liveness)["\x27]|\.(?:get|route|Get|HandleFunc|Handle|MapGet)\(\s*["\x27][\w/:{}-]*/(?:health|healthz|ready|readyz|readiness|live|livez|liveness)["\x27]|@(?:app|router|\w+_router)\.(?:get|api_route)\(\s*["\x27][\w/-]*(?:health|ready|live)|\bMapHealthChecks\(|\bmanagement\.endpoint\.health\.\w+|^\s*(?:readiness|liveness)(?:Probe)?\s*:' "${CODE[@]}" -g '**/application*.{yml,yaml,properties}' "${X[@]}" . | "${NC[@]}"
rg -n --no-heading -U --pcre2 '(?:@(?:Get|GetMapping)\(\s*["\x27][\w/:-]*(?:health|healthz|ready|readyz|readiness)["\x27]|\.(?:get|Get|HandleFunc|MapGet)\(\s*["\x27][\w/:-]*/(?:health|healthz|ready|readyz|readiness)["\x27]|@(?:app|router|\w+_router)\.get\(\s*["\x27][\w/-]*(?:health|ready)\w*["\x27]|\bfunc\s+\w*(?:[Rr]eady|[Hh]ealth)\w*\(|\bdef\s+\w*(?:ready|health)\w*\()(?:[^\n]*\n(?:(?![^\n]*(?:[Pp]ing|\bcheck\(\s*\[\s*\(|\bisHealthy|select\s+1|SELECT\s+1|fetchval|\bexecute\(|\.query\(|isConnected|isReady|PingContext|\bdb\.|\bpool\.|\bredis\.|\bstatus\(\)|ShuttingDown|draining))[^\n]*\n){0,6}?)?[^\n]*?\K(?:\.check\(\s*\[\s*\]\s*\)|return\s*\{\s*["\x27]?(?:status|ok|healthy)["\x27]?\s*:\s*(?:["\x27](?:ok|up|UP|healthy)["\x27]|true|True)\s*\}|res\.sendStatus\(\s*200\s*\)|res\.(?:status\(\s*200\s*\)\.)?(?:json|send)\(\s*(?:\{\s*["\x27]?(?:status|ok)["\x27]?\s*:\s*(?:["\x27](?:ok|up)["\x27]|true)\s*\}|["\x27](?:ok|OK)["\x27])?\s*\)|res\.status\(\s*200\s*\)\.end\(|reply\.(?:code\(\s*200\s*\)\.)?send\(|w\.WriteHeader\(\s*http\.StatusOK\s*\)|return\s+["\x27](?:ok|OK)["\x27]|Results\.Ok\(|ResponseEntity\.ok\()' "${CODE[@]}" "${X[@]}" .
rg -n --no-heading -U --pcre2 '(?:@(?:Get|GetMapping)\(\s*["\x27][\w/:-]*(?:live|livez|liveness)["\x27]|\.(?:get|Get|HandleFunc|MapGet)\(\s*["\x27][\w/:-]*/(?:live|livez|liveness)["\x27]|@(?:app|router)\.get\(\s*["\x27][\w/-]*live\w*["\x27]|\bfunc\s+\w*[Ll]ive\w*\(|\bdef\s+\w*live\w*\()[^\n]*\n(?:[^\n]*\n){0,6}?[^\n]*?\K(?:[Pp]ingCheck\(|[Pp]ing(?:Context)?\(|select\s+1|SELECT\s+1|fetchval\(|\.query\(|\bdb\.|\bpool\.|\bredis\.)' "${CODE[@]}" "${X[@]}" .
# 8a probe exclusions present; 8b request-telemetry surfaces (tracer, HTTP metric hook, request logger) whose file has no exclusion; 8c RED selectors in consumers with no probe filter
rg -n --no-heading --pcre2 '\bignoreIncomingRequestHook\b|\bignoreIncomingPaths\b|\bOTEL_PYTHON_(?:\w+_)?EXCLUDED_URLS\b|\bexcluded_urls\b|\bautoLogging\b|\brouteBlacklist\b|\bexclude(?:Routes|Paths|_paths|d_handlers)\b|\bexcludedHandlers\b|\bignore(?:Paths|Routes)\b|\bObservationPredicate\b|\bmanagement\.observations\b|\bshould_ignore\b' "${CODE[@]}" -g '**/*.{yml,yaml,env}' -g '**/.env*' "${X[@]}" . | "${NC[@]}"
rg -l0 --pcre2 '\bnew\s+NodeSDK\(|\bgetNodeAutoInstrumentations\(|\bFastAPIInstrumentor\b|\botelhttp\.NewHandler\(|\bAddAspNetCoreInstrumentation\(|\bfastify-metrics\b|\bexpress-prom-bundle\b|\bInstrumentator\(\)|\bpromhttp\.InstrumentHandler\w*\(|addHook\(\s*["\x27]onResponse["\x27]|@app\.middleware\(\s*["\x27]http["\x27]\)|\bpinoHttp\s*[:(]|(?:from\s+|require\(\s*)["\x27]pino-http["\x27]|\bmorgan\(|\bexpress-winston\b|\bUseSerilogRequestLogging\(' "${CODE[@]}" "${X[@]}" . | xargs -0 -r rg --files-without-match --pcre2 '\bignore\w*|\bexclude\w*|\bskip\w*|\b\w*(?:[Bb]lack|[Dd]eny)list\b|\bPROBE\w*|\bPredicate\b|["\x27]/(?:health|healthz|ready|readyz|live|livez|metrics)\b[^\n]*(?:===?|!==?|\bin\b|startsWith|includes|has\()|(?:startsWith|includes|has)\(\s*["\x27]/(?:health|ready|live|metrics)'
[ "${#CONSUMER_PATHS[@]}" -gt 0 ] && rg -H -n --no-heading -o --pcre2 '\b(?:http|grpc)_\w*(?:requests?|duration|latency)\w*\{[^}\n]*\}' "${CONSUMER_PATHS[@]}" | rg -v --pcre2 'health|ready|live|probe|metrics["\\]|route\s*!~|handler\s*!~|path\s*!~'
```

Reading the output:
- **0a is the gate** (§ The metrics gate). **0b** lists the clients a readiness must reflect. **0c** prints the consumer set.
- The **file-level lines** (2b, 8b) list files, not lines. Read each whole. Grep 2 prints one line per unmetered entry point; read the body.
- **2c settles §2 in groups.** A scheduler explorer wrap, a worker `completed`/`failed` hook or an abstract worker base that observes meters every entry point behind it. Read it once, then clear or confirm the whole group.

Two blind spots are structural, so work around them instead of trusting a quiet grep:
- **A label set behind a helper.** `routeLabel(req)`, `labelsFor(ctx)` or a Nest interceptor hides the label source from 1b. Read every helper that 1a/1b's `METRIC_PATHS` files call to build labels.
- **A consumer outside the repo.** Dashboards provisioned through the Grafana UI, a separate rules repo or Datadog monitors are invisible to 0c. §6 is then `NO-DATA(consumers outside the repo)`, never "dead".

### Measured (2026-10-10)

| Tree | Result |
|---|---|
| Seeded sample: 27 files over Node (NestJS + Fastify, prom-client, terminus, OTel meter, hot-shots worker), Python (FastAPI + Celery), Go (chi), Java (Micrometer), .NET, `deploy/` (rules, a dashboard, a Deployment) | Whole script 0.7 s, 89 lines, 0 rg errors. **All 32 seeded positives surface** in their § (§1 ×8 incl. PL-08 and an OTel attribute, §2 ×4, §3 ×5, §4 ×3, §5 ×4, §6 ×2, §7 ×3, §8 ×3 + one 8c selector). 15 decoys never print: a `routeOptions.url` label, an exemplar `traceId`, a Starlette route-template label, chi `RoutePattern()`, `(Date.now() - t) / 1000`, Fastify `elapsedTime / 1000`, a `getSingleMetric ??` guard, Go `MustRegister` in `init`, an in-flight gauge with `inc`/`dec`, two constant liveness routes, a processor and a Celery task that do meter, a metered StatsD worker, pino `autoLogging.ignore`, a hook that skips a probe set. Test and migration files: 0 hits. One context line is cleared at read: a histogram whose buckets hold the SLO edge (3c) |
| `benchmarks/fixtures/*` (15 fixtures) | **Gate closed in all 15** (no metrics client). 23 lines in total, 4 s for all 15. 0a/0b 13 (context); §2 2 and 2b 1, both `N/A (no metrics library)`. 7a/7b 7: two 7b constant `/healthz` handlers (a FastAPI app on in-process SQLite, an Express app), both Refuted at read: no probe manifest names them readiness. A startup-flag readiness was not hit. FP classes fixed before shipping: response bodies, log fields and an audit call carrying `err.message` / `req.path` (1b, 4 → 0, now `METRIC_PATHS`-only, with the key form requiring the raw value right after the key); a rate limiter's `buckets:` map (3c, `METRIC_PATHS`-only); an email's `@` passing the §2 filter |
| Real repository (eval § 3.7: NestJS 11 + Fastify 5 + MikroORM + BullMQ, prom-client 15, terminus 11, OTel SDK; read-only, `git status` clean before and after) | 3.0–4.4 s wall over runs, 129 lines, 0 rg errors, **0 hits in excluded trees**. §1 0 hits: the route label is `request.routeOptions.url` through a helper that collapses unmatched URLs to one value (§ 29). §2: 61 entry points (54 `@Cron`/`@Interval`, 7 `@Processor`) → **2 groups via 2c**: a schedule-explorer wrap counting every tick `{job,outcome}` with no duration (1 Hardening), and an abstract worker base observing job duration (Refuted). §3: SLO edges 0.1 / 0.3 / 1 are all in the shared bucket constant → 0. §4, §5: 0. §6: 4 names no consumer file names → 3 Unconfirmed low (`NO-DATA(mimirtool)`) + 1 named only in an SLO doc, routed to `slo-rule-scan` §1. §7: 7b 0 (readiness checks DB, Redis and the shutdown flag; liveness constant); one 7a line is an app route ending in `/health`. §8: tracing excludes the health prefix; the pino-http config has no `autoLogging.ignore` → credited to `log-signal-scan` §5; 8c 9 selectors → SLO rules already filter the probe routes, a `sum by (route)` ticket rule keeps probe rows apart (Refuted), one dashboard's rate and error-ratio panels include probe traffic → 1 low candidate, Unconfirmed until the scrape. FP classes fixed before shipping: i18n catalogs with `"query"` keys as consumers, comment-only mentions of pino-http as surfaces (3 → 0), a ternary `name : '…'` as a metric name, `@Controller('…/bulk-status')` as a probe |
| Tool lane | `blocked (lane not installed: promtool@3.15.0)`; no Prometheus binary on the measuring host. Eval unknown 5 (the HC-01 constant-200 regex) is now measured on real code: 0 hits against a correct readiness, 2 refuted on fixtures |
| `benchmarks/fixtures/obs-defects`, staged copy | 187 lines, 0.4 s, 19/19 seeds. Grep 6 now reads a name across a newline (`-U`, captured with `-r '$1'`: with `\K`, rg 15.2.0 printed the whole line of a match that spans lines): 25 names, the black-formatted `Histogram(` included, and still exactly the two seeded dead metrics |

## The 3,000-hit path

1. **Intersect** with the process map and the entry points: routes, consumers, cron, workers, and the probe paths a manifest names. A metric that no production process registers is dismissed with one read; name the directory in the coverage block.
2. **Group** by root cause: one registry module, one label helper (§1), one scheduler or worker wrapper (§2, grep 2c), one bucket constant (§3), one registration factory (§5), one consumer repo (§6), one health module (§7), one telemetry bootstrap (§8). Thirty `labels(req.url)` sites through one middleware are **one** finding with thirty sites (precedents P4).
3. **Rank:** unbounded labels on the request path first (an outage risk to the TSDB); then payment, auth, checkout and consumer paths; then SLI-feeding histograms; then the rest.
4. **Read the top 30 groups.**
5. **Run the bulk oracle once.** Drive the integration or e2e suite with randomized ids, scrape the registry once, and run `promtool check metrics --extended`. Series per metric, `+Inf`-only histograms and counters that never moved settle whole groups.
6. **Ledger the rest** as `Live, unreviewed (k groups / n hits — <continuing command>)`. Never mark it `checked`.

## Scans for

Severity assumes a production path and an open gate (§7–§8 run on a closed gate).

| § | Classes | Default severity |
|---|---|---|
| 1 | MT-01 unbounded label value; MT-02 `trace_id` as a label; PL-08 StatsD/DogStatsD tag explosion | high |
| 2 | MT-03 RED/USE missing on handlers, consumers, cron, pools | medium |
| 3 | MT-04 unit or bucket misfit (+ the static half of SLO-07) | medium; high when it breaks an SLI |
| 4 | MT-05 type misuse: gauge as counter, summary across instances, client-side percentiles | medium |
| 5 | MT-06 registration per call; naming lint | low–medium (medium when a duplicate throws on a request path) |
| 6 | MT-07 dead metric | low |
| 7 | HC-01 readiness that always answers 200 | medium |
| 8 | HC-02 probe traffic in RED metrics, traces and logs | low–medium |

### 1. Unbounded label; `trace_id` as a label; tag explosion (MT-01, MT-02, PL-08)

```
BAD:   labelNames: ['route', 'user_id']  ·  httpDuration.labels(req.method, request.url, code)   // Fastify raw URL
       REQUESTS.labels(request.url.path)  ·  reqs.WithLabelValues(r.URL.Path)  ·  Tag.of("uri", request.getRequestURI())
       counter.add(1, { 'user.id': user.id })  ·  statsd.increment('x', 1, [`customer:${id}`])  ·  labels(error=str(e))
GOOD:  request.routeOptions.url · request.scope["route"].path · chi RoutePattern() · Spring's templated uri · a bounded enum
       the id in a log line, a span attribute or an exemplar (observe({ value, exemplarLabels: { traceId } }))
```
**Read the code:**
- What is the label's value set? Use a route template, a status class or a closed enum (precedents § 29). A raw path, id, email, error text or `trace_id` is unbounded.
- `tenant_id`: run the series arithmetic `∏ distinct values × replicas` against `THR-OBS-CARDINALITY` (precedents § 21). It is neither approved nor rejected without that arithmetic.
- An id in a log field, span attribute or exemplar is correct (§ 19, § 20).
- Does a helper collapse unmatched URLs to one value (`unmatched`, `__unknown__`)? Then the 404 flood stays one series.

**Finding when** a reachable label takes unbounded values. **Proof (V198):** hit the entry point with 100 random ids and paths, then scrape. The metric's series count must stay at route templates × bounded values (`THR-OBS-CARDINALITY`: past 10 values a design question, past 100 an investigation), with no raw path, id or error string as a value.

### 2. Entry point with no RED; pool with no USE (MT-03)

```
BAD:   @Cron('0 2 * * *') async chargeRenewals() { this.logger.log(…); await this.run(); }   // no counter, no duration
       new Worker('emails', async (job) => send(job.data))  ·  @app.task def rebuild_index(): …  ·  @Scheduled purgeCarts()
GOOD:  a wrapper every tick passes through: jobs_total{job,outcome} + job_duration_seconds{job} (one place, grep 2c)
```
**Read the code:**
- Does a wrapper meter the entry point: a scheduler explorer, a worker event hook, an abstract base, `@Timed`, auto-instrumentation (2c)? One read clears or confirms the whole group.
- Is there a counter **with an outcome label** and a duration? A counter alone leaves "slow" invisible. That is Hardening unless a runbook, SLO or deadline names the job's latency.
- Does a pool expose in-use/idle/waiting (`collectDefaultMetrics` does not)?

**Finding when** a reachable entry point emits neither a counter with an outcome nor a duration. **Proof (V200):** run the job, consumer or cron handler once in a test, then scrape. Its counter (with outcome) and its duration must both move. The test fails on the unmetered entry point.

### 3. Unit or bucket misfit (MT-04, SLO-07 static half)

```
BAD:   paymentDuration.observe(Date.now() - t0)          // ms into payment_duration_seconds: every sample in +Inf
       LATENCY.observe((time.time() - start) * 1000)  ·  dur.Observe(float64(time.Since(t).Milliseconds()))  ·  name: 'job_wait_ms'
       default buckets (…, 0.25, 0.5, …) while the SLO rule reads http_request_duration_seconds_bucket{le="0.3"}
GOOD:  observe((Date.now() - t0) / 1000) · time.Since(t).Seconds() · base units (_seconds, _bytes) · buckets: [0.1, 0.3, 1, …] with an edge at T
```
**Read the code:**
- Is there a `/1000` or `.Seconds()` conversion on the line or in the helper (the decoy)?
- For each SLO threshold T (3d), is T an edge of the metric's bucket list (3c)? Use the defaults when no list is given (prom-client and `client_golang`: `0.005 … 10`, no `0.3`).
- On Prometheus 3, `le` values are floats (precedents § 45). An integer `le="1"` in the SLI belongs to `alert-rule-lint` §5.

**Finding when** a reachable observation lands in the wrong unit, or an SLO threshold has no bucket edge. **Proof (V199):** observe one known duration in a test. It must land in the finite bucket its seconds value belongs in (a ms value lands in `+Inf`), and `x_bucket{le="T"}` must exist for each T.

### 4. Type misuse (MT-05)

```
BAD:   new Gauge({ name: 'http_requests_handled_total' }) … handledRequests.inc()   // only ever incremented: resets look like drops
       new Summary({ name: 'checkout_latency_seconds' }) on 3 replicas · avg(checkout_latency_seconds{quantile="0.99"})
       Timer.builder("checkout.latency").publishPercentiles(0.95, 0.99)     // no publishPercentileHistogram()
GOOD:  a Counter for monotonic counts · a Histogram for latency aggregated across instances · publishPercentileHistogram() behind an SLO
```
**Read the code:**
- Is the gauge ever decremented or set (4b checks every name)? A gauge only ever incremented is a counter that loses `rate()`'s reset handling. Counter resets are handled by `rate()`; that is not this class.
- Is the summary served by one instance only (the decoy), or averaged across replicas (4c prints replicas)?
- Does a dashboard or rule average a `quantile` series?

**Finding when** the type cannot answer the question its consumers ask. **Proof (V198):** in the registry test, the type prints in the exposition (`# TYPE`). Two instances' summaries cannot be combined into the true percentile, and a histogram's buckets can. Use the static two-ended trace (declaration plus consumer) until that test runs.

### 5. Registration per call; naming (MT-06)

```
BAD:   async create() { const created = new Counter({ name: 'orders_created_total', … }); }   // 2nd request throws "already been registered"
       def report(): render = Histogram("report_render_seconds", …)  ·  func exportHandler(…) { prometheus.MustRegister(exports) }
       new Counter({ name: 'http_errors' })                                                    // promtool: counter without _total
GOOD:  module-scope registration · register.getSingleMetric(name) ?? new Counter(…) · MustRegister in init() or a constructor
```
**Read the code:**
- Is the enclosing function called once (module init, `onModuleInit`, a factory, Go `init`/`New…`)? Grep 5b prints the Go function.
- Is it a NestJS `REQUEST`-scoped provider, where a class field is per request?
- Python `prometheus_client` adds `_total` itself [K], so 5c skips Python.

**Finding when** a registration runs more than once per process on a reachable path, or the exposition fails the naming lint. **Proof (T):** `promtool check metrics` exits 3 on the scrape, or a second request through the entry point throws in the test.

### 6. Dead metric (MT-07)

```
BAD:   cart_abandon_total, retry_attempts — registered, read by no rule, recording rule, dashboard or SLO file
GOOD:  every registered metric named by at least one consumer, or removed
```
**Read the code:**
- Is the consumer outside the repo (Grafana UI, a rules repo, Datadog)? Then the verdict is `NO-DATA(<source>)`, never dead (precedents § 36).
- Was it added in the same change as its consumer?
- Is it named only in a document (an SLO doc, a runbook) with no rule? Then route it to `slo-rule-scan` §1 or `alert-rule-lint`.
- Ground the translated name: OTel and Micrometer dotted names become underscored and suffixed (§ 43).

**Finding when** a registered metric has no consumer in the repo **and** the repo is the declared home of its consumers. Otherwise the row is Unconfirmed. **Proof:** S, the set-diff above; L, `mimirtool analyze prometheus` against the live TSDB (else `NO-DATA(mimirtool)`).

### 7. Readiness that always answers 200 (HC-01)

```
BAD:   @Get('ready') @HealthCheck() ready() { return this.health.check([]); }      // terminus: empty list → status ok
       @app.get("/readyz") async def readyz(): return {"ok": True}                 # while the app holds an asyncpg pool
       func readyz(w, r) { w.WriteHeader(http.StatusOK) }
GOOD:  readiness pings each per-pod dependency (DB pool, Redis, broker client) and answers 503 while draining; liveness stays constant
```
**Read the code:**
- Is this the **readiness** route? Check the manifest's `readinessProbe` path (infrastructure's file, read only), else the name. A constant **liveness** is the right design (decoy). `healthz` with no manifest is ambiguous: Unconfirmed.
- Which dependencies does the pod need to serve (0b)? Does readiness reflect each one it can lose on its own (its pool, its connection)?
- A fleet-wide fact (a schema assertion, a shared upstream's health) on a 5-second readiness loop empties every pod at once. That belongs in a startup probe or a deploy gate, so leaving it out of readiness is correct, not HC-01.
- Liveness that checks a shared dependency is performance's (7c, § Boundaries).

**Finding when** the readiness route of a pod that holds a dependency answers 200 with that dependency down. **Proof (V201):** stop the dependency in a test (or point its client at a closed port). `/readyz` must answer 503 while `/livez` stays 200, and readiness must recover when the dependency returns.

### 8. Probe traffic in telemetry (HC-02)

```
BAD:   new NodeSDK({ instrumentations: [getNodeAutoInstrumentations()] })      // no ignoreIncomingRequestHook: a span per probe
       app.addHook('onResponse', …httpDuration.labels(…).observe(…))            // counts /health/* and /metrics
       sum(rate(http_request_duration_seconds_count{namespace="x"}[5m]))        // a dashboard request rate that includes the kubelet
GOOD:  ignoreIncomingRequestHook: (req) => req.url?.startsWith('/health') · OTEL_PYTHON_EXCLUDED_URLS · a PROBES skip set in the hook
       or the filter in every consumer: route!~".*/health/.*" (SLO rules), sum by (route) (per-route rules)
```
**Read the code:**
- For each surface (tracer, HTTP metric hook, request logger), is every probe path from 7a excluded at the source, **or** filtered in every consuming selector (8c)? Either one closes the metric half.
- Is the selector grouped `by (route)`? Then probe rows stay separate: Refuted.
- After excluding probes, does the SLI still have traffic, such as a synthetic probe on a real route (precedents § 18)?
- A logger surface is `log-signal-scan` §5's row (**LG-05 probe**: pino-http with no `autoLogging.ignore`, its grep 5c). Credit that row; never report it here (§ Boundaries).

**Finding when** probe hits reach a span store, or a RED series that a rule or dashboard reads unfiltered. **Proof (V201):** 100 probe hits in a test must add 0 spans, 0 request-log lines and no change to the SLI series.

## Proof — the registry scrape

The oracle, its per-stack registry and the assertions are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Observability, *Registry scrape*, with variants **V198** (cardinality, type), **V199** (units, buckets), **V200** (RED/USE coverage) and **V201** (health, probe traffic). The registries: prom-client `await register.metrics()`; Python `generate_latest(REGISTRY)` or `REGISTRY.get_sample_value(…)`; Go `testutil.CollectAndCount` / `testutil.ToFloat64`; Micrometer `SimpleMeterRegistry`; .NET `MetricCollector<T>` [K].

The shape:
1. Boot the app through the test harness it already runs (`fastify.inject` / supertest, `TestClient`, `httptest`, MockMvc, `WebApplicationFactory`), with the **same registry module production uses**.
2. Drive the real entry point: 100 randomized ids and paths (§1); one known duration (§3); one run of each job (§2); a stopped dependency (§7); 100 probe hits (§8).
3. Scrape and assert: series count bounded, the sample in its finite bucket, `le="T"` present, the counter (with outcome) and duration moved, 503 on `/readyz`, 0 spans and lines per probe. Pipe the scrape through `promtool check metrics`.
4. The test **fails on the unfixed code**. A test that passes before the fix proves nothing; rebuild it until it fails.

A promtool test with mocked series proves no metric exists (precedents § 16). Without a harness, the row is `[report-flagged]` / Unconfirmed, with the test written out.

## Output

```
metric-hygiene-scan — gate: open (api/package.json:19 prom-client 15.1.3; py-svc/requirements.txt:2 prometheus-client 0.23.1; go.mod client_golang v1.23.2)
Lanes: node (NestJS 11 + Fastify 5, terminus 11, OTel meter, hot-shots), python (FastAPI + Celery), go, java (Micrometer), .net · tool lane: blocked (promtool@3.15.0)
Consumers: deploy/prometheus/rules/api.yml, deploy/grafana/api.json

Findings: 2 · Unconfirmed: 2

1. api/src/metrics/request-metrics.ts:12                         [report-with-fix]   high
   §1 MT-01 — `httpDuration.labels(request.method, request.url, …)` labels by the raw Fastify URL on every route.
   Proof: registry test, 100 GET /orders/<uuid> → 100 new series of http_request_duration_seconds (fails;
   THR-OBS-CARDINALITY investigate at 100). Fix: request.routeOptions.url ?? 'unmatched' (precedents § 29).

2. api/src/health/health.controller.ts:16                        [report-with-fix]   medium
   §7 HC-01 — readiness `this.health.check([])` answers 200 with Postgres stopped; the pod holds a MikroORM pool
   (api/package.json:10). Proof: e2e with the DB container stopped: GET /health/ready → 200 (fails).
   Fix: check([() => this.db.pingCheck('database')]); /health/live unchanged.

3. api/src/metrics/registry.ts:7 · deploy/prometheus/rules/api.yml:6          [report-flagged]   medium
   §3 MT-04 — default buckets have no 0.3 edge; the SLO rule reads le="0.3". Unproven: no registry run.
   Settling test: observe(0.29) and assert x_bucket{le="0.3"} exists.

Verification: 41 candidates → 2 findings · 2 unconfirmed · 3 hardening · 0 pre-existing · 34 refuted (self-verified)

Class coverage:
  gate  metrics library                 open (5 clients, 13 metric files)
  §1  unbounded labels (MT-01/02, PL-08)  checked (11 hits → 1 finding; 3 route-template labels refuted)
  §2  RED/USE coverage (MT-03)          checked (4 entry points → 0 findings; 1 hardening: counter, no duration)
  §3  units / buckets (MT-04)           checked (9 hits → 1 flagged)
  §4  type misuse (MT-05)               checked (4 hits → 1 unconfirmed: summary averaged across 3 replicas)
  §5  registration / naming (MT-06)     checked (4 hits → 0 findings) · tool lane blocked
  §6  dead metrics (MT-07)              checked (17 names → 2 hardening) · NO-DATA(mimirtool)
  §7  readiness (HC-01)                 checked (3 constant handlers → 1 finding; 2 liveness decoys)
  §8  probe traffic (HC-02)             checked (3 surfaces → 0 findings; logger row credited to log-signal-scan §5)
```

`[report-with-fix]`: the entry point is traced, the registry or probe test failed, and the fix is local to the project's client or health module. `[report-flagged]`: one link is unproven (no harness, a consumer outside the repo, a probe role the manifest does not state); the row names it and the settling test.

The coverage block lists the gate and **all eight** §s on every run:
- `checked (k hits → m findings)` only when the grep ran;
- `N/A (no metrics library)` for §1–§6 on a closed gate;
- `blocked (<reason>)` when a grep failed or the tool lane could not install;
- `NO-DATA(<source>)` for a live-only half;
- `Live, unreviewed (k groups / n hits)` for a partial review, never `checked`.

## False positives / precedents

The verifier reads [`precedents/observability.md`](../../../../snippets/precedents/observability.md) and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:
- **§ 29** A route-template label is bounded; only the raw path or URL is MT-01.
- **§ 19** A high-cardinality field is correct in a log line, a span attribute or a wide event, and wrong as a metric label.
- **§ 20** `trace_id` as an exemplar is correct; as a label it is MT-02.
- **§ 21** `tenant_id` as a label needs the series arithmetic before any verdict.
- **§ 18** Health routes excluded from tracing, logs and SLIs are correct, unless the SLI is left with no synthetic traffic.
- **§ 43** OTel → Prometheus names gain unit and `_total` suffixes. Ground the translated name.
- **§ 16** A promtool test with mocked series proves no metric exists.
- **P2** Liveness on a shared dependency, probe manifests and label values that are PII are other packs' rows.
- **P4** One finding per registry, label helper, wrapper or health module.

Two rules of verdict discipline hold:
- **§ 36:** dead, cardinality-in-production and series-cost claims only a backend can settle are `NO-DATA(<source>)`, never an estimate.
- **§ 37:** a metric, label or route a finding or fix cites must resolve in the repo inventory or the scrape.

Two shapes this skill must not report:
- **A constant liveness route.** Liveness should depend on the process alone.
- **Probe traffic filtered in every consumer.** A `route!~` filter on each SLI selector, or `sum by (route)`, closes the metric half without a source exclusion.

## When to run

- On any diff that touches a metric registration, a label set, a histogram's buckets, a metrics hook or middleware, a scheduler or queue worker, a health controller or route, a tracer's ignore hooks, or a rule or dashboard's RED selector. This is `/obs-audit`'s "a metric registration or health route" dispatch signal.
- On every whole-repo `/obs-audit`, reporting the gate and all eight §s.
- After `/add-metrics` or any agent-written instrumentation: the registry scrape is the acceptance check.

## Halt conditions

- **Do not report a high row as confirmed until a separate verifier has refuted it.** That verifier must not be the run that found it, and passes the row through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with `precedents/observability.md`.
  - Under `/obs-audit`, that happens in its verification phase.
  - Run standalone, apply the protocol as a second pass and tag those rows `self-verified`.
  - List the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- **Halt before any § when the gate is unread.** Without the 0a result printed, no §1–§6 row may be graded.
- **Halt on any finding missing its anchors:** the metric or route `<file:line>`, the entry point, the scrape result and the fix in the project's client.
- **No `[report-with-fix]` without a registry or probe test that failed.** Without one, the row is `[report-flagged]` / Unconfirmed.
- **No proposed fix may hide the signal:** deleting the metric, dropping a label at the scrape (`metric_relabel_configs: drop`) instead of bounding it at the source, raising `THR-OBS-CARDINALITY`, or making readiness answer 200 unconditionally.
- **Do not assert a client default from memory.** A bucket, suffix or registration claim cites the lockfile version and the package source, or the scrape.
- **Do not print "metrics look fine" without the coverage block.** A § whose grep did not run is `blocked`, never `checked`.
- **Do not re-derive a class another skill owns** (§ Boundaries). Cross-link it.

## Related

- `/obs-audit` dispatches this skill and folds its coverage block into the Metrics and Health ledger rows. `/obs-fix` closes findings with the failing-first registry test, the fix at the registry or helper, a re-run of this detector, and the sibling search.
- `/add-metrics` (this pack) builds instrumentation; its closing gate is this skill's registry scrape.
- `alert-rule-lint` (selectors that name no series), `slo-rule-scan` (SLI thresholds), `log-signal-scan` (probe log volume) and `telemetry-config-scan` (Loki labels, dashboards) are this pack's neighbours.
- `@observability-reviewer` judges these rows in refute mode. `ai-patterns/metrics.md` holds the naming and cardinality conventions the fixes follow.
- performance `request-path-scan` §15 owns liveness on a shared dependency, when the performance pack is installed.

## Sources

Read from the published package tarballs on 2026-10-10: prom-client 15.1.3 (`lib/histogram.js` default buckets, `lib/registry.js` duplicate-registration error, `lib/counter.js` negative-increment error, `lib/summary.js` default percentiles); `@nestjs/terminus` 11.1.1 (`HealthCheckService.check`, `HealthCheckExecutor` status); `fastify-metrics` 14.1.0 (README options; `dist/fastify-metrics.js` default route label); `@willsoto/nestjs-prometheus` 7.0.0 README. Carried from the observability research catalog and the batch-4 eval: the R10a–R10c regexes, the per-lane decoys marked `[K]`, the promtool and golangci-lint versions and exit codes. Paraphrased; no text reproduced beyond identifiers.
