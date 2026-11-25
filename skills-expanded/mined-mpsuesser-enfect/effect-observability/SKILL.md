---
name: effect-observability
description: Implement structured logging, distributed tracing, and metrics in Effect applications. Use this skill when configuring loggers, adding spans/tracing, collecting metrics, or setting up OTLP/Prometheus export.
---

You are an Effect TypeScript expert specializing in observability — structured logging, distributed tracing, and metrics collection.

## Effect Source Reference

The Effect v4 source is available at `~/.local/share/opencode/repos/github.com/Effect-TS/effect@main/`.
Inspect `git show effect@4.1.0:<path>` there for this baseline; main may be ahead.
Keep `effect` and `@effect/*` packages on the same version. The OTLP modules and
`@effect/opentelemetry` APIs are tagged `@stability unstable` and may break in
minor releases; the shorter `effect/observability` import path is not a stability guarantee.

Reference this for:

- `Logger` module: `packages/effect/src/Logger.ts`
- `Tracer` module: `packages/effect/src/Tracer.ts`
- `Metric` module: `packages/effect/src/Metric.ts`
- OTLP export: `packages/effect/src/observability/`
- Observability examples: `ai-docs/src/08_observability/`

---

## 1. Structured Logging

### Log Functions

Effect provides log functions at every level. Each is variadic and accepts one or more message values:

```ts
import { Effect } from 'effect';

const program = Effect.gen(function* () {
	yield* Effect.log('general log message');
	yield* Effect.logDebug('debug-level detail');
	yield* Effect.logInfo('informational message');
	yield* Effect.logWarning('something concerning');
	yield* Effect.logError('something failed');
});
```

Pass additional message values after the first. These extra values become part of the log message/body — they are **not** automatically indexed as queryable annotations:

```ts
yield* Effect.log('User action', { userId: 123, action: 'login' });
yield* Effect.logInfo('Request processed', { duration: 150, statusCode: 200 });
```

For **queryable dimensions** (fields you want to filter or group on in your logging/tracing backend), prefer `Effect.annotateLogs` or span annotations (`Effect.annotateCurrentSpan` / `Effect.annotateSpans`) rather than passing objects as message values.

### Log Annotations

Attach key-value metadata to all log lines within a scope:

```ts
const checkout = Effect.gen(function* () {
	yield* Effect.logInfo('validating cart');
	yield* Effect.logWarning('inventory low for one line item');
	yield* Effect.logError('payment provider timeout');
}).pipe(
	Effect.annotateLogs({
		service: 'checkout-api',
		route: 'POST /checkout'
	})
);
```

Single annotation shorthand:

```ts
Effect.annotateLogs('requestId', 'req-abc-123');
```

### Log Spans

Add duration metadata to log lines — each log will include `label=<elapsed>ms`:

```ts
const withTiming = myEffect.pipe(Effect.withLogSpan('checkout'));
// Log output includes: checkout=42ms
```

---

## 2. Logger Configuration

### Built-in Loggers

Effect v4 provides several logger implementations:

| Logger                     | Output                            | Use Case                       |
| -------------------------- | --------------------------------- | ------------------------------ |
| `Logger.defaultLogger`     | Default runtime format            | General use                    |
| `Logger.consolePretty()`   | Colorized, human-readable         | Development                    |
| `Logger.consoleJson`       | Single-line JSON to console       | Production / log aggregation   |
| `Logger.consoleLogFmt`     | logfmt key=value to console       | Production / structured search |
| `Logger.consoleStructured` | JS object to console              | Development debugging          |
| `Logger.formatSimple`      | String (no console output)        | Composition / piping           |
| `Logger.formatJson`        | JSON string (no console output)   | Composition / piping           |
| `Logger.formatLogFmt`      | logfmt string (no console output) | Composition / piping           |
| `Logger.formatStructured`  | Structured JS object              | Composition / piping           |
| `Logger.tracerLogger`      | Emits logs as tracer span events  | Included by default            |

### Installing Loggers via `Logger.layer`

`Logger.layer` **replaces** the current loggers by default:

```ts
import { Effect, Logger } from 'effect';

// JSON logging for production
const JsonLoggerLayer = Logger.layer([Logger.consoleJson]);

// Pretty logging for development
const PrettyLoggerLayer = Logger.layer([Logger.consolePretty()]);

// Multiple loggers — both receive every log entry
const MultiLoggerLayer = Logger.layer([
	Logger.consoleJson,
	Logger.consolePretty()
]);

// Merge with existing loggers instead of replacing
const AdditionalLoggerLayer = Logger.layer([Logger.consoleJson], {
	mergeWithExisting: true
});
```

### Log Level Filtering

Control the minimum log level via `References.MinimumLogLevel`:

```ts
import { Layer, References } from 'effect';

// Only emit Warn and above (skip Debug, Info)
const WarnAndAbove = Layer.succeed(References.MinimumLogLevel, 'Warn');

// Combine with logger
const ProductionLoggerLayer = Logger.layer([Logger.consoleJson]).pipe(
	Layer.provideMerge(WarnAndAbove)
);
```

Valid levels: `"All"`, `"Trace"`, `"Debug"`, `"Info"`, `"Warn"`, `"Error"`, `"Fatal"`, `"None"`.

### Custom Loggers

Create loggers with `Logger.make`:

```ts
import { Logger } from 'effect';

const customLogger = Logger.make((options) => {
	console.log(`[${options.logLevel}] ${options.message}`);
});

// options fields: message, logLevel, cause, fiber, date
```

### Batched Logging

Aggregate log entries over a time window before flushing:

```ts
import { Effect, Logger } from 'effect';

const batchedLogger = Logger.batched(Logger.formatStructured, {
	window: '1 second',
	flush: Effect.fn(function* (batch) {
		// Send batch to external service
		console.log(`Flushing ${batch.length} log entries`);
	})
});

// batchedLogger is an Effect — use it inside Logger.layer
const BatchedLoggerLayer = Logger.layer([batchedLogger]);
```

`Logger.batched` serializes flushes. Shutdown waits for an in-flight flush before
flushing remaining entries; do not start a competing manual drain or assume
the window timer is the only flush trigger.

### File Logging

Write logs directly to a file (requires the `FileSystem` service from `effect`):

```ts
import { NodeFileSystem } from '@effect/platform-node';
import { Layer, Logger } from 'effect';

const FileLoggerLayer = Logger.layer([
	Logger.toFile(Logger.formatSimple, 'app.log')
]).pipe(Layer.provide(NodeFileSystem.layer));
```

Pipe syntax with options:

```ts
const fileLogger = Logger.formatJson.pipe(
	Logger.toFile('/var/log/myapp.log', {
		flag: 'a',
		batchWindow: '5 seconds'
	})
);
```

### Environment-based Logger Selection

```ts
import { Config, Effect, Layer, Logger } from 'effect';

const LoggerLayer = Layer.unwrap(
	Effect.gen(function* () {
		const env = yield* Config.String('NODE_ENV').pipe(
			Config.withDefault('development')
		);
		if (env === 'production') {
			return Logger.layer([Logger.consoleJson]);
		}
		return Logger.layer([Logger.consolePretty()]);
	})
);
```

---

## 3. Spans and Tracing

### `Effect.withSpan`

Create a tracing span around any effect:

```ts
const processOrder = Effect.gen(function* () {
	yield* chargeCard(orderId);
	yield* persistOrder(orderId);
}).pipe(Effect.withSpan('processOrder'));
```

Spans nest automatically — child effects that also use `withSpan` become child spans.

### `Effect.fn` with Auto-Spans

When you pass a string name to `Effect.fn`, it automatically wraps the function body in a span:

```ts
import { Effect } from 'effect';

const processCheckout = Effect.fn('Checkout.processCheckout')(function* (
	orderId: string
) {
	yield* Effect.logInfo('starting checkout', { orderId });
	yield* chargeCard(orderId).pipe(Effect.withSpan('checkout.charge-card'));
	yield* persistOrder(orderId).pipe(
		Effect.withSpan('checkout.persist-order')
	);
	yield* Effect.logInfo('checkout completed', { orderId });
});
// Creates a span named "Checkout.processCheckout" wrapping the entire body
```

### Span Attributes

Annotate the current span with key-value attributes:

```ts
// Annotate the current span from inside the effect
yield* Effect.annotateCurrentSpan('order.id', orderId);
yield* Effect.annotateCurrentSpan('order.total', 99.95);

// Annotate from outside using pipe
const withAttributes = myEffect.pipe(
	Effect.annotateSpans({
		'checkout.order_id': orderId,
		'checkout.provider': 'acme-pay'
	})
);
```

### Layer Spans

Attach spans to layer construction:

```ts
const MyLayer = Layer.effectDiscard(setupEffect).pipe(
	Layer.withSpan('my-layer-setup')
);
```

### HTTP and RPC trace conventions in 4.1.0

HTTP client/server spans default to the method alone (`GET`, not `http.client
GET` / `http.server GET`). RPC spans likewise default to the method; explicit
RPC `spanPrefix` retains a prefix. Client/server kinds and `rpc.system.name` /
`rpc.method` provide context. Update backend queries rather than depending on
old default names.

HTTP header capture is now opt-in using `HttpClient.TracerHeaderFilter` or
`HttpMiddleware.TracerHeaderFilter`. Captured sensitive headers are still
redacted via `Headers.CurrentRedactedNames`. URL userinfo and query secrets use
separate `UrlParams.CurrentRedactedNames`; supplying a custom list **replaces**
defaults, so retain defaults you still need. Redaction affects telemetry, not
the actual request. Prefer narrow allowlists to blanket header capture.

Client spans mark 4xx/5xx responses as errors even though receiving a response
still succeeds as an Effect; server spans treat 5xx as errors, not ordinary 4xx.
Server spans finish before the request fiber exits so shutdown can flush them.
Client trace propagation writes `b3` and `traceparent` by default; disabling
`HttpClient.TracerPropagationEnabled` suppresses those headers, not span
creation, when a browser target's CORS policy cannot accept them.

Successful WebSocket upgrades report status `101` to server middleware, not the
discarded handler response's status. Incoming W3C contexts reject all-zero trace
or parent IDs; B3 contexts validate identifier widths/hex and honor debug sampling.
Do not rely on malformed propagation values being accepted as a parent.

SQL statement spans now use the database namespace, server address/port, or
database system as the name (fallback `sql.execute`). Effect execution methods
use `effect.sql.method`, not `db.operation.name`; transaction spans are internal
with `effect.sql.transaction.*` events. GenAI spans use `gen_ai.provider.name`
instead of `gen_ai.system`, are client spans, and record `gen_ai.output.type`.
Effect-specific AI fields use `effect.ai.*`; OpenAI-specific fields use
`openai.*`. See `effect-sql` and the AI skills before customizing those attributes.

---

## 4. Metrics

Effect provides five metric types. All metrics are concurrent-safe and integrated into the runtime.

### Counter

Tracks cumulative values that only increase:

```ts
import { Effect, Metric } from 'effect';

const requestCount = Metric.counter('http_requests_total', {
	description: 'Total number of HTTP requests'
});

yield* Metric.update(requestCount, 1);
```

### Gauge

A single numerical value that can go up or down:

```ts
const activeConnections = Metric.gauge('active_connections', {
	description: 'Current active connections'
});

yield* Metric.update(activeConnections, 42);
```

### Histogram

Records observations in configurable buckets:

```ts
const responseTime = Metric.histogram('http_response_time_ms', {
	description: 'HTTP response time in milliseconds',
	boundaries: Metric.linearBoundaries({ start: 0, width: 50, count: 20 })
});

yield* Metric.update(responseTime, 127);
```

### Summary

Calculates quantiles over a sliding time window:

```ts
const dbQueryTime = Metric.summary('db_query_duration', {
	maxAge: '5 minutes',
	maxSize: 1000,
	quantiles: [0.5, 0.9, 0.95, 0.99]
});

yield* Metric.update(dbQueryTime, durationMs);
```

### Frequency

Counts occurrences of discrete string values:

```ts
const statusCodes = Metric.frequency('http_status_codes', {
	description: 'HTTP status code distribution'
});

yield* Metric.update(statusCodes, '200');
yield* Metric.update(statusCodes, '404');
```

### Metric Attributes

Tag metrics with key-value attributes for filtering/grouping:

```ts
const taggedCounter = Metric.withAttributes(requestCount, {
	endpoint: '/api/users',
	method: 'GET'
});

yield* Metric.update(taggedCounter, 1);

// Or inline
yield*
	Metric.update(
		Metric.withAttributes(requestCount, {
			endpoint: '/api/posts',
			method: 'POST'
		}),
		1
	);
```

### Reading Metric Values

```ts
// Get current value of a single metric
const value = yield* Metric.value(requestCount);

// Snapshot all metrics
const snapshots = yield* Metric.snapshot;
// Inspect or export snapshots; do not stringify arbitrary states into log fields.
```

### Series ownership and snapshot-backed gauges

The unstable `Metric.remove`, `removeUnsafe`, and `registerUnsafe` APIs support explicit metric lifecycle control.
Removal targets the metric plus attributes merged with
`Metric.CurrentMetricAttributes`, leaving other series intact. A later update
recreates the removed series from its initial state. Exporters discard removed
series' delta bookkeeping when they disappear from snapshots.

For values already held by a runtime integration, `registerUnsafe` reads
`hooks.get` at snapshot time. Updates/modifications of that series are ignored,
including supplied mutation hooks. The registration retains its getter closure
until removed, so scope it to the source's lifetime. An older registration's
`remove()` cannot remove a replacement registration.

<!-- typecheck -->
```ts
import { Effect, Metric } from 'effect';

const observeQueue = Effect.fn('Queue.observe')(function* (size: () => number) {
	const context = yield* Effect.context<never>();
	const gauge = Metric.gauge('queue_size');
	return yield* Effect.acquireRelease(
		Effect.sync(() => Metric.registerUnsafe(gauge, context, {
			get: () => ({ value: size() }),
			update: () => {},
			modify: () => {}
		})),
		(registration) => Effect.sync(() => registration.remove())
	);
});
// Keep the returned registration inside its owning Scope.
```

Bound metric attribute cardinality. User IDs, request IDs, raw URLs, and arbitrary
error messages belong in redacted logs/spans when needed, not metric labels.
Removal is lifecycle management, not permission to create unbounded series.

---

## 5. OTLP Export

Effect v4 includes built-in OTLP exporters in `effect/observability`. No external OpenTelemetry SDK needed.

### All-in-One: `Otlp.layerJson`

The simplest setup — exports traces, logs, and metrics to a single OTLP endpoint:

```ts
import { Layer } from 'effect';
import { FetchHttpClient } from 'effect/http';
import { Otlp } from 'effect/observability';

const ObservabilityLayer = Otlp.layerJson({
	baseUrl: 'http://localhost:4318',
	compression: 'gzip', // optional; defaults to 'none'
	resource: {
		serviceName: 'my-api',
		serviceVersion: '1.0.0',
		attributes: {
			'deployment.environment': 'staging'
		}
	}
}).pipe(Layer.provide(FetchHttpClient.layer));
```

This creates layers for all three signals with standard OTLP paths (`/v1/traces`, `/v1/logs`, `/v1/metrics`).

Variants:

- `Otlp.layerJson` — JSON serialization (simplest, no extra deps)
- `Otlp.layerProtobuf` — Protobuf serialization (more efficient)
- `Otlp.layer` — requires you to provide `OtlpSerialization` separately

Use `Otlp.layerFromConfig()` for standard OpenTelemetry environment
configuration (`OTEL_EXPORTER_OTLP_ENDPOINT`, signal-specific endpoints,
headers, exporter selection, and `OTEL_SDK_DISABLED`). Provide both
`OtlpSerialization.layerJson` (or protobuf) and an `HttpClient` layer. Explicit
`layerJson({ baseUrl })` is the programmatic endpoint path; it is not the
environment-selected exporter setup.

All combined/individual exporters accept `compression: 'gzip' | 'none'`
(default `none`). Gzip requires runtime `CompressionStream` support and only
compresses bodies at least 1 KB by default; compression happens once before
transient retries. Compression failures temporarily disable the exporter like
transport failures; flush/shutdown do not surface them as typed failures.
With config layers, `OTEL_EXPORTER_OTLP_{LOGS,TRACES,METRICS}_COMPRESSION`
overrides `OTEL_EXPORTER_OTLP_COMPRESSION`. On 429 responses, valid whole
nonnegative seconds or an HTTP date in `Retry-After` control the delay; missing
or invalid values fall back to 5 seconds.

### Exported fields and metric shapes

Update dashboards/queries when moving from 4.0.0 to 4.1.0:

- OTLP logs use `effect.fiberId`, numeric elapsed-millisecond
  `effect.log_span.<label>`, and `exception.type`, `exception.message`,
  `exception.stacktrace` instead of `fiberId`, `logSpan.*`, and `log.error`.
  Event and observation timestamps are separate.
- Resources include `telemetry.sdk.*`; log/trace instrumentation scope is
  `effect` with its release version, not the service name. Trace IDs (including
  links and log correlation) are padded to 128-bit width.
- Interrupt-only spans have Unset status plus `effect.fiber.interrupted: true`,
  not Ok/"Interrupted". Success is Ok; reportable failures use Error and
  exception events.
- OTLP summaries are one native Summary under the metric ID, **always
  cumulative**, replacing the old separate `_quantiles` / `_count` / `_sum`
  export. Quantiles remain windowed; count/sum are lifetime totals.
- Common units normalize to UCUM (`milliseconds` → `ms`, `bytes` → `By`).
  Bigint counters/gauges beyond safe-number range retain decimal precision.
- Histograms include all finite boundaries plus overflow. Later delta intervals
  omit min/max because cumulative extrema cannot represent interval extrema.
  Prometheus emits exactly one `+Inf` bucket.
- OTLP JSON encodes NaN/Infinity correctly. Integer attributes outside signed
  int64 use double values for numbers and strings for bigint values.

### Individual OTLP Exporters

For fine-grained control, configure each exporter independently:

```ts
import { Layer } from 'effect';
import { FetchHttpClient } from 'effect/http';
import {
	OtlpLogger,
	OtlpMetrics,
	OtlpSerialization,
	OtlpTracer
} from 'effect/observability';

const OtlpTracingLayer = OtlpTracer.layer({
	url: 'http://localhost:4318/v1/traces',
	resource: {
		serviceName: 'checkout-api',
		serviceVersion: '1.0.0',
		attributes: { 'deployment.environment': 'staging' }
	}
});

const OtlpLoggingLayer = OtlpLogger.layer({
	url: 'http://localhost:4318/v1/logs',
	resource: {
		serviceName: 'checkout-api',
		serviceVersion: '1.0.0'
	}
});

const OtlpMetricsLayer = OtlpMetrics.layer({
	url: 'http://localhost:4318/v1/metrics',
	resource: {
		serviceName: 'checkout-api',
		serviceVersion: '1.0.0'
	},
	temporality: 'delta' // or "cumulative" (default)
});

const ObservabilityLayer = Layer.mergeAll(
	OtlpTracingLayer,
	OtlpLoggingLayer,
	OtlpMetricsLayer
).pipe(
	Layer.provide(OtlpSerialization.layerJson),
	Layer.provide(FetchHttpClient.layer)
);
```

### Manual OTLP Flush

Each OTLP signal layer now outputs the shared `OtlpExporter.Flusher` service. Use it before a controlled handoff or shutdown when buffered telemetry must be exported immediately:

```ts
import { Effect } from 'effect';
import { OtlpExporter } from 'effect/observability';

const flushTelemetry = Effect.gen(function* () {
	const flusher = yield* OtlpExporter.Flusher;
	yield* flusher.flush.pipe(Effect.timeoutOption('5 seconds'));
});
```

All signal layers in the same memoized layer graph share one flusher registry, so
one call requests exports concurrently. `flush` cannot fail and has no built-in
timeout; it waits only for exports it starts, not exports already in flight.
Exporters in their temporary-disable window are skipped, so completion is not a
delivery acknowledgement. Successful delta-metric flushes advance their aggregation window.

The combined `Otlp.layer*` signatures expose the shared `OtlpExporter.Flusher`.
Use it directly for manual drains:

<!-- typecheck -->
```ts
import { Effect, Layer } from 'effect';
import { FetchHttpClient } from 'effect/http';
import { Otlp, OtlpExporter } from 'effect/observability';

const telemetry = Otlp.layerJson({ baseUrl: 'http://localhost:4318' }).pipe(
  Layer.provide(FetchHttpClient.layer)
);

const flush = Effect.gen(function* () {
	const flusher = yield* OtlpExporter.Flusher;
	return yield* flusher.flush.pipe(Effect.timeoutOption('5 seconds'));
}).pipe(Effect.provide(telemetry));
```

`OtlpResource.fromConfig` trims `OTEL_RESOURCE_ATTRIBUTES` keys/values and retains
empty values as `""`. Unstable `OtlpProxy` can forward browser telemetry through
server routes while keeping vendor credentials on the server; review its body
limits and authentication boundary. Import Node/Web SDK adapters from
`@effect/opentelemetry/NodeSdk` / `WebSdk`, rather than the removed root exports.
`Pool.stats`, `PgPool.stats`, and `PgClient.poolStats` expose idle/in-use/waiting
snapshots for metrics without accessing pool internals.

### Exporter lifecycle

Keep the exporter layer alive for the application's lifetime. Scope finalization
starts a final export and waits for tracked in-flight exports, bounded by
`shutdownTimeout`; a manual flush has the narrower semantics described above.
The HTTP exporter drains response bodies before completing or retrying requests,
including error responses that carry a body. Custom/mock HTTP clients must
supply a consumable response body rather than only a status code. This releases
connections between export attempts; callers need no separate drain step.

### OTLP Layer Options

Common options for the individual OTLP exporters (`OtlpLogger.layer`, `OtlpTracer.layer`, `OtlpMetrics.layer`):

| Option                    | Default          | Description                              |
| ------------------------- | ---------------- | ---------------------------------------- |
| `url`                     | required         | OTLP endpoint URL                        |
| `resource.serviceName`    | —                | Service name in exported telemetry       |
| `resource.serviceVersion` | —                | Service version                          |
| `resource.attributes`     | —                | Additional resource attributes           |
| `headers`                 | —                | HTTP headers for auth etc.               |
| `compression`             | `none`           | `gzip` or `none`; requires runtime support |
| `exportInterval`          | signal-specific  | How often to flush batches (see below)   |
| `maxBatchSize`            | signal-specific  | Max items per export batch (see below)   |
| `shutdownTimeout`         | `3 seconds`      | Timeout for final flush on shutdown      |

Batch/flush defaults differ by signal:

| Exporter            | `exportInterval` | `maxBatchSize`                 | `shutdownTimeout` |
| ------------------- | ---------------- | ------------------------------ | ----------------- |
| `OtlpLogger.layer`  | `1 second`       | `1000`                         | `3 seconds`       |
| `OtlpTracer.layer`  | `5 seconds`      | `1000`                         | `3 seconds`       |
| `OtlpMetrics.layer` | `10 seconds`     | disabled (pull-style snapshot) | `3 seconds`       |

The all-in-one `Otlp.layerJson` / `Otlp.layerProtobuf` use **signal-specific** interval option names instead of a single `exportInterval`: `loggerExportInterval`, `metricsExportInterval`, and `tracerExportInterval` (plus a shared `maxBatchSize`, `shutdownTimeout`, and `metricsTemporality`).

`OtlpMetrics.layer` additionally accepts:

- `temporality`: `"cumulative"` (default) or `"delta"` — determines how metric values relate to their time interval; summaries are always cumulative

`OtlpLogger.layer` additionally accepts:

- `mergeWithExisting`: `true` (default) — merge with existing loggers instead of replacing
- `excludeLogSpans`: omit log span annotations from exported logs

### Wiring Into Your App

Provide the observability layer at the outermost level so all spans and logs are captured:

```ts
import { NodeRuntime } from '@effect/platform-node';
import { Layer } from 'effect';

const Main = AppLayer.pipe(Layer.provide(ObservabilityLayer));

Layer.launch(Main).pipe(NodeRuntime.runMain);
```

---

## 6. Prometheus Metrics

Export Effect metrics in Prometheus exposition format:

```ts
import { Effect, Metric } from 'effect';
import * as PrometheusMetrics from 'effect/observability/PrometheusMetrics';

const program = Effect.gen(function* () {
	const counter = Metric.counter('http_requests_total', {
		description: 'Total HTTP requests'
	});
	yield* Metric.update(counter, 42);

	// Format metrics as Prometheus text
	const output = yield* PrometheusMetrics.format();
	// # HELP http_requests_total Total HTTP requests
	// # TYPE http_requests_total counter
	// http_requests_total 42

	// With prefix
	const prefixed = yield* PrometheusMetrics.format({ prefix: 'myapp' });
	// myapp_http_requests_total 42
});
```

### Prometheus HTTP Endpoint

Automatically register a `/metrics` endpoint on your HTTP router:

```ts
import * as PrometheusMetrics from 'effect/observability/PrometheusMetrics';

// Default: GET /metrics
const PrometheusLayer = PrometheusMetrics.layerHttp();

// Custom path and prefix
const CustomPrometheusLayer = PrometheusMetrics.layerHttp({
	path: '/prometheus/metrics',
	prefix: 'myapp'
});
```

`layerHttp` requires `HttpRouter.HttpRouter` in the context — it adds a route to your existing router.

---

## 7. Testing Observability

### Testing Logged Output

Import `TestConsole` from `effect/testing`; `it.effect` supplies its capture
layer. Effect logs need a console logger installed before asserting its output:

<!-- typecheck -->
```ts
import { Effect, Logger } from 'effect';
import { TestConsole } from 'effect/testing';

const captured = Effect.gen(function* () {
	yield* Effect.logInfo('checkout completed');
	return yield* TestConsole.logLines;
}).pipe(
	Effect.provide(Logger.layer([Logger.consoleLogFmt])),
	Effect.provide(TestConsole.layer)
);
```

A pretty logger still uses the captured Console service. For visible diagnostic
output explicitly provide `Console.Console` with `globalThis.console`, or use
`it.live` when live console/time is the behavior under test. This is separate
from asserting captured output.

### Testing Metrics

Read metric values directly:

```ts
it.effect('increments request counter', () =>
	Effect.gen(function* () {
		const counter = Metric.counter('test_requests');
		yield* Metric.update(counter, 5);
		const state = yield* Metric.value(counter);
		expect(state.count).toBe(5);
	}).pipe(Effect.provideService(Metric.MetricRegistry, new Map()))
);
```

Metric registries are shared by default. Give tests a fresh registry (or remove
their series) so results do not depend on execution order or previous runs.

### Testing Spans

Use a test tracer or assert on span attributes captured via `Effect.withSpan`.

---

## 8. Common Patterns

### Full Observability Stack (Dev + Prod)

```ts
import { Config, Effect, Layer, Logger, References } from 'effect';
import { FetchHttpClient } from 'effect/http';
import { Otlp } from 'effect/observability';

const DevObservability = Logger.layer([Logger.consolePretty()]);

const ProdObservability = Layer.mergeAll(
	Logger.layer([Logger.consoleJson]),
	Layer.succeed(References.MinimumLogLevel, 'Info'),
	Otlp.layerJson({
		baseUrl: 'http://otel-collector:4318',
		resource: {
			serviceName: 'my-api',
			serviceVersion: '1.0.0'
		}
	}).pipe(Layer.provide(FetchHttpClient.layer))
);

const ObservabilityLayer = Layer.unwrap(
	Effect.gen(function* () {
		const env = yield* Config.String('NODE_ENV').pipe(
			Config.withDefault('development')
		);
		return env === 'production' ? ProdObservability : DevObservability;
	})
);
```

### Service with Instrumented Methods

```ts
import { Effect, Layer, Metric, Context } from 'effect';

const requestLatency = Metric.histogram('checkout_latency_ms', {
	boundaries: Metric.linearBoundaries({ start: 0, width: 25, count: 40 })
});

class Checkout extends Context.Service<
	Checkout,
	{
		processCheckout(orderId: string): Effect.Effect<void>;
	}
>()('app/Checkout') {
	static readonly layer = Layer.effect(
		Checkout,
		Effect.gen(function* () {
			return Checkout.of({
				processCheckout: Effect.fn('Checkout.processCheckout')(
					function* (orderId: string) {
						yield* Effect.logInfo('starting checkout', { orderId });
						yield* Effect.annotateCurrentSpan('order.id', orderId);

						yield* chargeCard(orderId).pipe(
							Effect.withSpan('checkout.charge-card')
						);
						yield* persistOrder(orderId).pipe(
							Effect.withSpan('checkout.persist-order')
						);

						yield* Effect.logInfo('checkout completed', {
							orderId
						});
					}
				)
			});
		})
	);
}
```

---

## Critical Rules

1. **Use `Logger.layer` to install loggers** — it replaces the default set. Use `{ mergeWithExisting: true }` to add without replacing.
2. **`Logger.tracerLogger` is included by default** — log messages automatically become span events. If you override loggers, include it explicitly if you want this behavior.
3. **`Effect.fn("name")` creates auto-spans** — prefer this over manual `Effect.withSpan` for service methods.
4. **Provide observability layers outermost** — so all application spans and logs are captured for export.
5. **OTLP exporters require `HttpClient` and `OtlpSerialization`** — `Otlp.layerJson` (and `layerProtobuf`) wires `OtlpSerialization` for you but still requires an `HttpClient`, so provide a client layer such as `FetchHttpClient.layer`. With `Otlp.layer` or the individual exporters, provide both `OtlpSerialization.layerJson` and `FetchHttpClient.layer` manually.
6. **`References.MinimumLogLevel`** controls filtering — not a logger concern, set it via `Layer.succeed`.
7. **Metric names should follow conventions** — snake_case with units suffix (e.g., `http_request_duration_ms`).
8. **`Metric.withAttributes` creates a tagged variant** — it does not mutate the original metric.
9. **`OtlpMetrics` temporality** — use `"delta"` for backends like Datadog/Dynatrace, `"cumulative"` (default) for Prometheus-style backends; summaries remain cumulative in either mode.
10. **OTLP modules are under `effect/observability`** — they remain tagged
    `@stability unstable`; inspect the matching release when upgrading.
11. **Use `OtlpExporter.Flusher` for manual drains** — bound `flusher.flush` with `Effect.timeoutOption` when shutdown latency must be capped.
