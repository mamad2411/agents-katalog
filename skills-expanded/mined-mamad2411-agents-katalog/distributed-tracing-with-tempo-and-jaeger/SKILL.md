---
name: distributed-tracing-with-tempo-and-jaeger
description: >
  Guides configuring Grafana Tempo or Jaeger as the distributed tracing
  backend — trace storage backend selection and retention, sampling
  strategy at the backend/collector level (head-based vs. tail-based),
  and trace-to-metrics/trace-to-logs correlation so a trace ID can pivot
  directly into a log line or a metrics exemplar. Use when the user asks
  to "set up Tempo," "configure Jaeger storage," "set trace retention,"
  "configure trace-to-logs correlation in Grafana," "design a sampling
  strategy for traces," or "query traces with TraceQL." This is the
  tracing *backend/storage* layer — instrumenting applications and
  configuring the OpenTelemetry Collector that feeds this backend is
  covered separately in
  opentelemetry-instrumentation-and-collector-configuration.
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# Distributed Tracing with Tempo and Jaeger

## Purpose

A distributed trace is only as useful as the backend that stores,
retains, and lets you query it — and that backend has its own set of
operational decisions distinct from how telemetry gets produced and
routed to it. **Grafana Tempo** and **Jaeger** are the two dominant
open-source tracing backends: Tempo is object-storage-native (S3/GCS/
Azure Blob, or local disk for small deployments) and designed to be
cheap to run at scale by trading fast arbitrary search for
ID-based lookup plus structural indexing via TraceQL; Jaeger supports a
wider range of storage backends (Elasticsearch, Cassandra, Badger for
local/dev) and has historically stronger built-in search-by-tag UX. Both
solve the same core operational problems this skill covers: how long to
retain traces and at what storage cost, how much of the total trace
volume to actually keep (sampling), and how to make a trace ID pivotable
into the logs and metrics for the same request rather than a dead-end
visualization. This skill covers the backend/storage layer specifically
— instrumenting applications and configuring the receiver → processor →
exporter pipeline that feeds traces *into* Tempo/Jaeger is the OpenTelemetry
Collector's job, covered in
[opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md),
which this skill assumes is already in place and cross-references
rather than repeats.

## When to use

- Standing up Tempo or Jaeger as the tracing backend for an
  OpenTelemetry-instrumented (or Jaeger-native) system.
- Deciding a trace retention period and storage backend (object storage
  vs. Elasticsearch/Cassandra) based on trace volume and query needs.
- Designing or tuning a sampling strategy — deciding what fraction of
  traces to keep, and whether that decision happens at the SDK/Collector
  (head-based) or at the backend after seeing a whole trace (tail-based).
- Wiring **trace-to-logs** and **trace-to-metrics** correlation in
  Grafana so a responder can pivot from a slow/failing trace directly to
  the exact log lines and metric exemplars for that request.
- Writing or debugging a TraceQL (Tempo) or a tag-based search (Jaeger)
  query to find a representative trace matching specific criteria
  (duration, service, error status).
- Reviewing why traces aren't retained long enough, aren't searchable by
  a needed attribute, or don't correlate into logs/metrics as expected.

## Prerequisites & environment

- Traces already arriving in OTLP (or Jaeger native protocol/Thrift)
  format from an OpenTelemetry Collector or directly-instrumented
  applications — see
  [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md)
  for getting spans emitted and routed correctly in the first place;
  this skill assumes that plumbing works and covers only what happens
  once spans reach the backend.
- **For Tempo:** an object storage bucket (S3, GCS, Azure Blob) for
  anything beyond a small single-node/local-disk deployment, and
  familiarity with Tempo's block-based storage model (`compactor`,
  `ingester`, `querier`, `distributor` components — deployable
  monolithically for small setups or as separate microservices at
  scale).
- **For Jaeger:** a supported storage backend already provisioned —
  Elasticsearch/OpenSearch for production-scale deployments with rich
  tag search, Cassandra as an alternative wide-column option, or Badger
  (embedded, local disk) for a single-node/development instance only.
- Grafana (see
  [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md))
  with Tempo and/or Jaeger configured as a datasource, plus Prometheus
  and Loki datasources already provisioned if trace-to-metrics/
  trace-to-logs correlation is in scope.
- Clarity on the sampling decision *before* provisioning storage
  capacity — tail-based sampling requires seeing every span of a trace
  before deciding to keep it, which has different infrastructure
  implications (a load-balancing exporter routing by trace ID, more
  Collector-side buffering) than head-based sampling decided once at
  the start of a trace.
- Tempo 2.x if relying on TraceQL (introduced in Tempo 2.0) as the
  primary query interface — earlier Tempo releases support only trace-ID
  lookup and a more limited search API.

## Step-by-step guidance

### Storage backend and retention

1. **Choose Tempo's storage backend deliberately** for anything beyond a
   quick local trial — object storage is the intended production
   backend, trading some query latency for storage cost far below
   Elasticsearch/Cassandra at comparable trace volume:
   ```yaml
   # tempo.yaml
   storage:
     trace:
       backend: s3
       s3:
         bucket: tempo-traces-prod
         endpoint: s3.us-east-1.amazonaws.com
         region: us-east-1
       pool:
         max_workers: 100
         queue_depth: 10000
   ```

2. **Set retention via the compactor**, sized to an explicit
   investigation/compliance window rather than an unconsidered default —
   trace storage grows quickly at real production volume, so retention
   is a genuine cost/usefulness tradeoff, not a "keep everything" default:
   ```yaml
   compactor:
     compaction:
       block_retention: 336h   # 14 days
   ```
   A shorter retention (days, not weeks) is common for traces
   specifically, since traces are typically used for near-term incident
   investigation rather than long-term trend analysis (which metrics
   handle far more cheaply) — validate the actual retention need against
   how far back responders realistically need to pull a trace, not a
   copy-pasted value from an unrelated system.

3. **For Jaeger, choose the storage backend based on query needs and
   existing operational expertise**, not just default familiarity:
   ```yaml
   # jaeger-collector storage flags (Elasticsearch backend)
   --es.server-urls=https://elasticsearch.observability.svc:9200
   --es.index-prefix=jaeger
   --es.num-shards=3
   --es.num-replicas=1
   ```
   Elasticsearch gives Jaeger rich ad hoc tag-based search out of the
   box, at the operational cost of running (and capacity-planning) an
   Elasticsearch cluster; Badger is fine for a single-node/development
   Jaeger instance but is not a multi-node/HA-capable production backend.

4. **Set Jaeger's index rollover and retention via curator/ILM policy**
   on the Elasticsearch side, mirroring the same deliberate-retention
   discipline as Tempo's compactor setting:
   ```json
   {
     "policy": {
       "phases": {
         "hot":   { "min_age": "0ms",  "actions": { "rollover": { "max_age": "1d" } } },
         "delete": { "min_age": "14d", "actions": { "delete": {} } }
       }
     }
   }
   ```

### Sampling strategy

5. **Decide head-based vs. tail-based sampling deliberately** — head-based
   (a probabilistic decision made once, at or near the start of a trace,
   usually in the SDK or the Collector) is cheap and simple but can miss
   rare, interesting traces (a specific slow or erroring request) purely
   by chance; tail-based (a decision made after the whole trace is
   assembled, keeping traces that match interesting criteria regardless
   of a random sample) catches those but requires every span of a trace
   to reach the same Collector instance before a decision can be made:
   ```yaml
   # head-based: simple probabilistic sampling at the SDK/Collector
   processors:
     probabilistic_sampler:
       sampling_percentage: 10
   ```
   ```yaml
   # tail-based: keep all errors and all slow requests, sample the rest
   # (this belongs in the OpenTelemetry Collector gateway tier — see
   # opentelemetry-instrumentation-and-collector-configuration for the
   # full pipeline this feeds into Tempo/Jaeger from)
   processors:
     tail_sampling:
       decision_wait: 10s
       policies:
         - name: sample-errors
           type: status_code
           status_code: { status_codes: [ERROR] }
         - name: sample-slow
           type: latency
           latency: { threshold_ms: 500 }
         - name: sample-baseline
           type: probabilistic
           probabilistic: { sampling_percentage: 10 }
   ```
   Tail-based sampling is the right default for production systems where
   the rare slow/erroring request is exactly what an investigation needs
   to find — but it only works correctly if every span for a given trace
   ID reaches the same Collector replica (see the load-balancing exporter
   note in
   [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md)).

6. **Set Jaeger's per-service sampling strategy** if using Jaeger's own
   native sampling configuration rather than Collector-side sampling:
   ```json
   {
     "service_strategies": [
       {
         "service": "checkout-service",
         "type": "probabilistic",
         "param": 0.1
       },
       {
         "service": "payments-service",
         "type": "probabilistic",
         "param": 1.0
       }
     ],
     "default_strategy": { "type": "probabilistic", "param": 0.05 }
   }
   ```
   A higher-value or higher-risk service (payments) can warrant a much
   higher (or 100%) sampling rate than a high-volume, lower-risk service,
   trading storage cost for near-complete visibility where it matters
   most.

### Correlation and querying

7. **Configure trace-to-logs correlation in Grafana's Tempo datasource**
   so a trace view links directly into the matching Loki log lines,
   scoped by the trace ID:
   ```yaml
   # Grafana datasource provisioning
   apiVersion: 1
   datasources:
     - name: Tempo
       type: tempo
       url: http://tempo-query-frontend.observability.svc:3100
       jsonData:
         tracesToLogsV2:
           datasourceUid: loki-datasource-uid
           spanStartTimeShift: '-5m'
           spanEndTimeShift: '5m'
           filterByTraceID: true
           filterBySpanID: false
           customQuery: true
           query: '{service_name="$__span.tags.service.name"} | json | trace_id="$__trace.traceId"'
   ```
   This is the backend-side half of the correlation described in
   [incident-investigation-using-metrics-logs-traces](../incident-investigation-using-metrics-logs-traces/SKILL.md);
   it only works if the application/Collector layer actually puts the
   `trace_id` into structured log lines in the first place, which is an
   instrumentation concern covered in
   [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md).

8. **Configure trace-to-metrics correlation** so a trace view can jump
   to the relevant service's request-rate/error-rate/latency dashboard,
   and so metrics exemplars (a specific trace ID attached to a
   histogram data point) link back into Tempo:
   ```yaml
   jsonData:
     tracesToMetrics:
       datasourceUid: prometheus-datasource-uid
       queries:
         - name: 'Request rate'
           query: 'sum(rate(http_requests_total{service="$__span.tags.service.name"}[5m]))'
   ```
   Exemplars require the metrics backend and instrumentation to actually
   attach a trace ID to a metric sample at scrape/ingest time — confirm
   Prometheus has `--enable-feature=exemplar-storage` enabled and the
   application's metrics library is configured to attach exemplars, not
   just that the Grafana panel is configured to display them.

9. **Query traces with TraceQL (Tempo) for structural, multi-condition
   searches** that go beyond a single tag match:
   ```traceql
   { .service.name = "checkout-service" && duration > 500ms && status = error }
   ```
   ```traceql
   { .service.name = "payments-service" } >> { .db.system = "postgresql" && duration > 200ms }
   ```
   The second example finds traces where a `payments-service` span has a
   descendant Postgres span slower than 200ms — a structural query no
   single-tag search could express.

10. **For Jaeger, search by service, operation, tags, and duration range**
    via its query API/UI rather than pulling every trace and filtering
    client-side:
    ```
    GET /api/traces?service=payments-service&tags={"error":"true"}&minDuration=200ms&lookback=1h
    ```

## Best practices

- Choose Tempo's object-storage backend as the default for new
  production tracing deployments — the storage-cost advantage at real
  trace volume is substantial compared to Elasticsearch/Cassandra-backed
  Jaeger, unless Jaeger's richer native tag-search UX or existing
  operational investment is a specific, deliberate reason to choose it
  instead.
- Set retention explicitly and separately from any other signal's
  retention policy — traces are typically the shortest-retained signal
  (days), with metrics retained far longer for trend analysis; don't
  copy a metrics or log retention value onto traces by default.
- Default to tail-based sampling for production traffic where the rare
  slow/erroring request matters — a flat probabilistic sample can easily
  miss the exact trace an investigation needs.
- Sample higher-risk or higher-value services (payments, auth) at a
  higher rate than high-volume, lower-risk services — sampling rate is a
  per-service decision, not a single global percentage.
- Wire both trace-to-logs and trace-to-metrics correlation as a standing
  platform configuration, not something set up ad hoc during an
  incident — confirm the correlation actually works (a real trace pivots
  to real matching log lines) as part of onboarding any new service, not
  just once at initial platform setup.
- Treat a missing `trace_id` in a service's structured logs as a
  platform gap to close, not an accepted limitation — correlation is
  only as good as the weakest-instrumented service in a call chain.
- Version-control Tempo/Jaeger configuration and Grafana datasource
  provisioning (correlation config, TraceQL-backed dashboard panels)
  alongside the rest of the observability stack's IaC, not as hand-edited
  console configuration.

## Common pitfalls

- **Symptom:** A trace that should still be within the configured
  retention window returns "trace not found" when queried.
  **Fix:** Check the compactor's `block_retention` (Tempo) or the
  Elasticsearch ILM delete phase (Jaeger) against the actual query time —
  a retention value that looks generous in days can still be shorter
  than expected if it was set relative to ingestion time rather than
  span time, or if a recent compactor/ILM policy change hasn't fully
  applied to already-written blocks/indices yet. Confirm the effective
  retention with `tempo-cli` (or the Elasticsearch ILM explain API)
  rather than assuming the configured value has already taken effect
  everywhere.

- **Symptom:** Tail-based sampling is configured, but a known slow/
  erroring trace never shows up in Tempo/Jaeger.
  **Fix:** Tail sampling requires every span of a trace to reach the
  same Collector replica before the sampling decision fires — if
  multiple stateless Collector replicas sit behind a plain round-robin
  load balancer, a trace's spans scatter across replicas and no single
  replica ever sees the whole trace to make a keep/drop decision. Route
  by trace ID with a load-balancing exporter (see
  [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md))
  so tail sampling actually has complete traces to evaluate.

- **Symptom:** Clicking "Logs for this span" in Grafana's trace view
  returns no results, even though the corresponding log lines definitely
  exist in Loki.
  **Fix:** The `tracesToLogsV2` correlation query's label selector or
  the `trace_id` JSON field name doesn't match what the service actually
  emits in its structured logs (e.g. the correlation config expects
  `trace_id` but the application logs `traceId` or a different casing).
  Pull a real log line for that trace ID directly in Loki's Explore view
  to confirm the actual field name/format, then align the datasource's
  correlation query to match exactly.

- **Symptom:** A dashboard's metric panels never show exemplar dots,
  even though tracing and metrics both appear to be working
  independently.
  **Fix:** Exemplars require explicit opt-in on both the metrics backend
  (`--enable-feature=exemplar-storage` on Prometheus) and the
  application's metrics instrumentation library — confirming traces
  work and metrics work independently doesn't confirm the two are
  actually being linked at the sample level. Enable exemplar storage and
  confirm the client library version/config actually attaches a
  `trace_id` exemplar to relevant histogram observations.

- **Symptom:** Trace storage costs (or Elasticsearch/Cassandra cluster
  size for Jaeger) grow far faster than expected shortly after a
  service's traffic increases.
  **Fix:** Sampling is likely set too high (or absent — 100% head
  sampling) for the new traffic volume, or tail-based sampling's
  baseline probabilistic rate wasn't re-evaluated after the volume
  change. Revisit per-service sampling rates against current traffic
  and re-confirm retention is still set deliberately rather than
  drifting upward from a well-intentioned but unreviewed change.

## Worked example

**Scenario:** Standing up Tempo as the tracing backend for
`checkout-service` and `payments-service` (both already emitting OTLP
traces via the Collector gateway from
[opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md)),
with tail-based sampling, 14-day retention, and full trace-to-logs/
trace-to-metrics correlation in Grafana.

1. Tempo deployed with S3 object storage and 14-day retention:
   ```yaml
   storage:
     trace:
       backend: s3
       s3:
         bucket: tempo-traces-prod
         region: us-east-1
   compactor:
     compaction:
       block_retention: 336h   # 14 days, matching the platform team's agreed incident-investigation window
   ```
2. The Collector gateway (configured per
   [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md))
   applies tail sampling — all errors, all requests over 500ms, plus a
   10% baseline — and exports via `otlp/tempo`, with a load-balancing
   exporter routing by `traceID` so tail sampling sees complete traces.
3. Grafana's Tempo datasource is provisioned with `tracesToLogsV2`
   pointed at the Loki datasource, matching on `trace_id` in the same
   structured-log field both services already emit, and
   `tracesToMetrics` pointed at Prometheus for a per-service request-
   rate/latency query.
4. A responder investigating a slow checkout pulls a representative
   trace with:
   ```traceql
   { .service.name = "checkout-service" && duration > 1s } >> { .service.name = "payments-service" }
   ```
   finding traces where `checkout-service` is slow specifically because
   of a downstream `payments-service` span, then clicks "Logs for this
   span" to land directly on `payments-service`'s log lines for that
   exact `trace_id`, closing the loop from trace to root-cause log
   detail without a separate manual log search.

## Cross-references

- [opentelemetry-instrumentation-and-collector-configuration](../opentelemetry-instrumentation-and-collector-configuration/SKILL.md) — the feeder layer: instrumenting applications and configuring the Collector pipeline (including the load-balancing exporter tail sampling depends on) that produces the spans this backend stores and queries.
- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md) — the metrics backend and Grafana instance this skill's trace-to-metrics correlation and exemplar configuration integrate with.
- [incident-investigation-using-metrics-logs-traces](../incident-investigation-using-metrics-logs-traces/SKILL.md) — the cross-signal investigative workflow that depends on the trace-to-logs/trace-to-metrics correlation this skill configures at the backend.
- [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md) — the log backend this skill's trace-to-logs correlation queries against, including the label-cardinality discipline that also applies to the `trace_id` correlation query.
