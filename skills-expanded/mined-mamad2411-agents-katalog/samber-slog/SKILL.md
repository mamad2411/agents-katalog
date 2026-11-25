---
name: samber-slog
description: "pipeline — structured log pipelines in Go with samber/slog-*: order sampling before formatting before routing, compose handlers (Fanout, Router, FirstMatch, Failover, Pool, Pipe), and ship to backend sinks. Use when adopting or tuning a slog pipeline, or when the codebase imports any github.com/samber/slog-* package."
license: MIT
---

# samber/slog-\*\*\*\*

**Leading word: pipeline.** Every log record flows left to right through a pipeline of `slog.Handler`s — sampling drops noise early, formatters strip PII before records leave the process, and routers send errors to Sentry while info goes to Loki. The discipline: fix the canonical order first, then pick the composition pattern per routing need.

## Steps — design the pipeline

1. **Fix the order: record → Sampling → Pipe → Router → Sinks.** Sampling is outermost so dropped records cost nothing; formatting happens before routing so every sink receives clean attributes.
   *Done when: the pipeline order is sampling, then formatting, then routing, and the reasoning is stated.*

## Steps — compose and route

1. **Pick the composition pattern per routing need.** `Fanout` broadcasts, `Router` routes by predicate, `FirstMatch` takes the first match, `Failover` tries handlers until one succeeds, `Pool` broadcasts concurrently, `Pipe` runs middleware before a sink.
   *Done when: the chosen pattern matches the routing need and the latency budget.*
2. **Give every Router a catch-all handler.** Add a handler with no predicate so unmatched records reach a sink instead of vanishing silently.
   *Done when: no Router exists without a default/catch-all handler.*
3. **Use `Pool` for slow parallel sinks.** Sequential `Fanout` blocks the caller for the sum of all handler latencies; `Pool` waits only for the slowest.
   *Done when: any slow multi-handler fan-out uses `Pool`, or the latency is accepted.*
4. **Prefer Router over Fanout when handlers need subsets.** Router evaluates predicates and skips non-matching handlers.
   *Done when: per-subset routing uses Router predicates, not unconditional Fanout.*

## Steps — sample and format

1. **Choose the sampling strategy by environment.** Uniform for dev/staging noise reduction, Threshold for production (log first N per interval, then rate), Absolute for a hard cap, Custom for level- or time-aware rules.
   *Done when: the strategy matches the environment and the visibility requirement.*
2. **Keep sampling the outermost handler.** Placing it after formatting wastes CPU formatting records that get dropped.
   *Done when: sampling wraps the rest of the pipeline.*
3. **Apply formatters as Pipe middleware.** `PIIFormatter`, `ErrorFormatter`, `IPAddressFormatter`, `TimeFormatter` plus generic `FormatByType[T]`, `FormatByKey`, `FormatByKind`, `FormatByGroup`; flatten nested attributes with `FlattenFormatterMiddleware`.
   *Done when: PII and error shaping run before any sink, and attribute transforms are middleware, not per-handler logic.*

## Steps — ship to sinks and middleware

1. **Use the `Option{}.NewXxxHandler()` constructor pattern** for backend sinks across the cloud, messaging, notification, storage, and bridge packages.
   *Done when: each sink follows the Option + constructor pattern.*
2. **Flush batch handlers on shutdown.** `slog-datadog`, `slog-loki`, `slog-kafka`, `slog-parquet` buffer records internally — `defer handler.Stop(ctx)` (Datadog), `defer lokiClient.Stop()` (Loki), `defer writer.Close()` (Kafka) or buffered logs are lost.
   *Done when: every batch sink has a shutdown flush.*
3. **Install HTTP middleware before using `AttrFromContext`.** `router.Use(slogXXX.New(logger))` per framework; configure `DefaultLevel`, `ClientErrorLevel`, `ServerErrorLevel`, request/response body, IDs, and `Filters` (e.g. `IgnorePath` for `/health`).
   *Done when: request attributes are populated by middleware before any `AttrFromContext` reads them.*

## Reference

### The pipeline model

```
record → [Sampling] → [Pipe: trace/PII] → [Router] → [Sinks]
```

Order matters: sampling before formatting saves CPU; formatting before routing ensures all sinks receive clean attributes. Reversing this wastes work on records that get dropped.

### Core libraries

| Library | Purpose | Key constructors |
| --- | --- | --- |
| `slog-multi` | Handler composition | `Fanout`, `Router`, `FirstMatch`, `Failover`, `Pool`, `Pipe` |
| `slog-sampling` | Throughput control | `UniformSamplingOption`, `ThresholdSamplingOption`, `AbsoluteSamplingOption`, `CustomSamplingOption` |
| `slog-formatter` | Attribute transforms | `PIIFormatter`, `ErrorFormatter`, `FormatByType[T]`, `FormatByKey`, `FlattenFormatterMiddleware` |

### Composition patterns

| Pattern | Behavior | Latency impact |
| --- | --- | --- |
| `Fanout(handlers...)` | Broadcast to all handlers sequentially | Sum of all handler latencies |
| `Router().Add(h, predicate).Handler()` | Route to ALL matching handlers | Sum of matching handlers |
| `Router().Add(...).FirstMatch().Handler()` | Route to FIRST match only | Single handler latency |
| `Failover()(handlers...)` | Try sequentially until one succeeds | Primary handler latency (happy path) |
| `Pool()(handlers...)` | Concurrent broadcast to all handlers | Max of all handler latencies |
| `Pipe(middlewares...).Handler(sink)` | Middleware chain before sink | Middleware overhead + sink |

```go
// Route errors to Sentry, all logs to stdout
logger := slog.New(
    slogmulti.Router().
        Add(sentryHandler, slogmulti.LevelIs(slog.LevelError)).
        Add(slog.NewJSONHandler(os.Stdout, nil)).
        Handler(),
)
```

Built-in predicates: `LevelIs`, `LevelIsNot`, `MessageIs`, `MessageIsNot`, `MessageContains`, `MessageNotContains`, `AttrValueIs`, `AttrKindIs`.

### Sampling strategies

| Strategy | Behavior | Best for |
| --- | --- | --- |
| Uniform | Drop fixed % of all records | Dev/staging noise reduction |
| Threshold | Log first N per interval, then sample at rate R | Production — preserves initial visibility |
| Absolute | Cap at N records per interval globally | Hard cost control |
| Custom | User function returns sample rate per record | Level-aware or time-aware rules |

Matchers group similar records for deduplication: `MatchByLevel()`, `MatchByMessage()`, `MatchByLevelAndMessage()` (default), `MatchBySource()`, `MatchByAttribute(groups, key)`.

```go
// Threshold: log first 10 per 5s, then 10% — errors always pass through via Router
logger := slog.New(
    slogmulti.
        Pipe(slogsampling.ThresholdSamplingOption{
            Tick: 5 * time.Second, Threshold: 10, Rate: 0.1,
        }.NewMiddleware()).
        Handler(innerHandler),
)
```

### Formatter example

```go
logger := slog.New(
    slogmulti.Pipe(slogformatter.NewFormatterMiddleware(
        slogformatter.PIIFormatter("user"),          // mask PII fields
        slogformatter.ErrorFormatter("error"),       // structured error info
        slogformatter.IPAddressFormatter("client"),  // mask IP addresses
    )).Handler(slog.NewJSONHandler(os.Stdout, nil)),
)
```

### Backend sinks

| Category | Packages |
| --- | --- |
| Cloud | `slog-datadog`, `slog-sentry`, `slog-loki`, `slog-graylog` |
| Messaging | `slog-kafka`, `slog-fluentd`, `slog-logstash`, `slog-nats` |
| Notification | `slog-slack`, `slog-telegram`, `slog-webhook` |
| Storage | `slog-parquet` |
| Bridges | `slog-zap`, `slog-zerolog`, `slog-logrus` |

### Performance notes

- **Fanout latency** = sum of all handler latencies (sequential). With 5 handlers at 10ms each, every log call costs 50ms — `Pool()` reduces it to max(latencies)
- **Pipe middleware** adds per-record function call overhead — keep chains short (2–4 middlewares)
- **slog-formatter** processes attributes sequentially — many formatters compound. For hot-path attribute formatting, prefer implementing `slog.LogValuer` on your types
- **Benchmark** the pipeline with `go test -bench` before production deployment; measure per-record allocation and latency to find which handler allocates most
- **Test pipelines with `slogmulti.NewHandleInlineHandler`** — assert on records reaching each stage without real sinks

- **[Pipeline Patterns](./references/pipeline-patterns.md)** — full code examples of every pattern
- **[Sampling Strategies](./references/sampling-strategies.md)** — strategy comparison and configuration details
- **[HTTP Middlewares](./references/http-middlewares.md)** — framework-specific setup
- **[Backend Handlers](./references/backend-handlers.md)** — configuration examples and shutdown patterns

## Watch for

| Mistake | Fix |
| --- | --- |
| Sampling after formatting | Place sampling as the outermost handler |
| Fanout to many slow synchronous handlers | Use `Pool()` for concurrent dispatch |
| Missing shutdown flush on batch handlers | `defer` the handler's `Stop`/`Close` |
| Router without default/catch-all handler | Add a predicate-less handler as default |
| `AttrFromContext` without HTTP middleware | Install the framework middleware first |
| `Pipe` with no middleware | Remove the no-op wrapper |

## Cross-references

- → See `go-observability` for slog fundamentals (levels, context, handler setup, migration)
- → See `go-safety` for the log-or-return rule
- → See `go-security` for PII handling in logs
- → See `samber-oops` for structured error context with `samber/oops`
