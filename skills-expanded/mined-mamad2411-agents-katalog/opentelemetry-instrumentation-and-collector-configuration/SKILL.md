---
name: opentelemetry-instrumentation-and-collector-configuration
description: >
  Guides instrumenting applications with the OpenTelemetry SDK (auto vs.
  manual instrumentation, resource attributes, context propagation) and
  configuring the OpenTelemetry Collector's receiver/processor/exporter
  pipeline architecture — the vendor-neutral instrumentation and routing
  layer that feeds telemetry into Prometheus, Loki, Tempo/Jaeger, or any
  other backend without coupling application code to a specific vendor
  SDK. Use when the user asks to "instrument this service with
  OpenTelemetry," "add OTel auto-instrumentation," "configure the
  OpenTelemetry Collector," "set up a receiver/processor/exporter
  pipeline," "route traces/metrics/logs to multiple backends from one
  Collector," or "why is the Collector not receiving spans/metrics/logs."
license: Apache-2.0
compatibility: "Claude Code, GitHub Copilot, OpenAI Codex, Cursor, Gemini CLI"
metadata:
  domain: observability-and-platform-extras
  maturity: stable
---

# OpenTelemetry Instrumentation and Collector Configuration

## Purpose

OpenTelemetry (OTel) is the vendor-neutral instrumentation layer that sits
between application code and whichever observability backend actually
stores the data — an application instrumented with the OTel SDK emits
telemetry in one standard format (OTLP) regardless of whether the
destination is Prometheus, Loki, Grafana Tempo, Jaeger, or a commercial
APM, and the **Collector** is the component that receives, transforms, and
routes that telemetry to one or many of those destinations. Getting this
layer wrong doesn't just mean a missing dashboard panel: an
auto-instrumentation agent that misses a key library, a Collector pipeline
that references a processor that was never wired into `service.pipelines`,
or a propagator mismatch between two services breaks the *foundation*
every backend-specific skill in this repo assumes is already working. This
skill covers instrumenting applications (auto vs. manual, resource
attributes, context propagation) and configuring the Collector's
receiver → processor → exporter pipeline — the plumbing that feeds
[prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md),
[loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md),
and
[distributed-tracing-with-tempo-and-jaeger](../distributed-tracing-with-tempo-and-jaeger/SKILL.md).
It does not cover validating that a Collector config is actually correct
before rollout (see
[opentelemetry-configuration-validation](../opentelemetry-configuration-validation/SKILL.md))
or the tracing backend's own storage/sampling/correlation concerns (see
[distributed-tracing-with-tempo-and-jaeger](../distributed-tracing-with-tempo-and-jaeger/SKILL.md)).

## When to use

- Instrumenting a new service and deciding between auto-instrumentation
  (a language agent/launcher requiring no code changes) and manual SDK
  instrumentation (custom spans, metrics, and attributes hand-written into
  the code).
- Standing up an OpenTelemetry Collector deployment — as a per-node/
  per-pod **agent** (sidecar or DaemonSet) versus a centralized
  **gateway** tier, or both together.
- Wiring a receiver (OTLP gRPC/HTTP, Prometheus scrape, filelog, Jaeger/
  Zipkin compatibility receivers) through processors to one or more
  exporters in a Collector pipeline.
- Fanning the same telemetry out to multiple backends at once (e.g.
  traces to both Tempo and a commercial APM during a migration).
- Setting resource attributes (`service.name`, `deployment.environment`)
  correctly so telemetry is attributable once it reaches a backend.
- Diagnosing why a service's spans, metrics, or logs never show up
  anywhere downstream, or show up incompletely.
- Migrating an application off a vendor-specific instrumentation SDK to
  OpenTelemetry to decouple it from a specific observability vendor.

## Prerequisites & environment

- The **OpenTelemetry Collector** — either the core distribution (OTLP
  receiver/exporter and a small processor set only) or the **contrib**
  distribution, which is required for most non-OTLP receivers/exporters
  (Prometheus remote-write exporter, Loki exporter, Jaeger receiver,
  cloud-provider exporters, etc.). Pin an exact image tag per environment
  rather than tracking `latest`, and keep the same version across the
  whole Collector fleet — mixed versions across agent/gateway tiers is a
  common source of subtly incompatible config behavior.
- A language-specific OpenTelemetry SDK/auto-instrumentation
  distribution for each service being instrumented (a Java agent JAR, the
  Python `opentelemetry-instrument` launcher plus
  `opentelemetry-bootstrap`, the Node.js
  `@opentelemetry/auto-instrumentations-node` package, or a manual SDK
  integration for languages without mature auto-instrumentation, such as
  Go, where instrumentation is largely manual/library-level today).
- Network reachability from every instrumented service to its Collector
  on the OTLP ports — gRPC on `4317`, HTTP/protobuf on `4318` — and from
  the Collector to whichever backend(s) its exporters target.
- Destinations already provisioned for each signal type this pipeline
  will route to: a Prometheus remote-write endpoint or scrape target (see
  [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md)),
  a Loki push endpoint (see
  [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md)),
  and/or a Tempo/Jaeger OTLP ingest endpoint (see
  [distributed-tracing-with-tempo-and-jaeger](../distributed-tracing-with-tempo-and-jaeger/SKILL.md)).
- Agreement across the whole system on which **context propagation**
  format is used (W3C Trace Context is the current default and
  recommended choice) — every service in a call chain must use the same
  propagator or traces silently break at the boundary between them.

## Step-by-step guidance

### Instrumenting applications

1. **Prefer auto-instrumentation as the default starting point** — it
   requires no application code changes and covers the common
   frameworks/libraries (HTTP servers/clients, common DB drivers,
   messaging clients) out of the box:
   ```bash
   # Java: attach the agent at process start, no code changes
   java -javaagent:/otel/opentelemetry-javaagent.jar \
     -Dotel.service.name=checkout-service \
     -Dotel.exporter.otlp.endpoint=http://otel-collector:4317 \
     -jar checkout-service.jar
   ```
   ```bash
   # Python: bootstrap installs instrumentation packages for detected
   # libraries, then opentelemetry-instrument wraps the process
   opentelemetry-bootstrap -a install
   OTEL_SERVICE_NAME=checkout-service \
   OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317 \
   opentelemetry-instrument python app.py
   ```
   ```javascript
   // Node.js: registered before any other imports (auto-instrumentations-node)
   const { NodeSDK } = require('@opentelemetry/sdk-node');
   const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
   const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');

   const sdk = new NodeSDK({
     traceExporter: new OTLPTraceExporter({ url: 'http://otel-collector:4317' }),
     instrumentations: [getNodeAutoInstrumentations()],
   });
   sdk.start();
   ```

2. **Add manual instrumentation for business-meaningful spans/metrics**
   auto-instrumentation cannot know about — a checkout step, a specific
   cache-hit ratio, a queue-processing span:
   ```python
   from opentelemetry import trace, metrics

   tracer = trace.get_tracer("checkout-service")
   meter = metrics.get_meter("checkout-service")
   checkout_duration = meter.create_histogram("checkout.duration", unit="ms")

   with tracer.start_as_current_span("apply-discount-code") as span:
       span.set_attribute("discount.code_type", "percentage")
       result = apply_discount(order)
       if not result.ok:
           span.set_status(trace.StatusCode.ERROR, result.error)
   ```
   Manual spans nest correctly inside whatever span auto-instrumentation
   already created for the enclosing HTTP request — no extra propagation
   wiring is needed within a single process.

3. **Set `service.name` and other resource attributes at SDK
   initialization**, not scattered per-span — these identify *which*
   service, version, and environment every span/metric/log came from:
   ```bash
   OTEL_RESOURCE_ATTRIBUTES="service.name=checkout-service,service.version=2.14.0,deployment.environment=production,service.namespace=commerce"
   ```
   Without a correct `service.name`, every service's telemetry shows up
   as `unknown_service` in every downstream backend, making dashboards and
   trace views unusable regardless of how well everything else is
   configured.

4. **Standardize context propagation across every service in a call
   chain** — W3C Trace Context (`traceparent`/`tracestate` headers) is the
   current default for OTel SDKs and should be the default choice unless
   a specific legacy system requires B3 or another format:
   ```bash
   OTEL_PROPAGATORS=tracecontext,baggage
   ```
   > **Warning:** if even one service in the call chain is configured
   > with a different propagator (e.g. legacy B3 while everything else
   > uses W3C Trace Context), that service becomes an invisible break in
   > every trace passing through it — the trace doesn't error, it just
   > silently splits into two disconnected traces at that hop. Audit
   > propagator configuration explicitly when onboarding any
   > legacy/third-party service into an existing trace topology.

### Deploying the Collector

5. **Choose a deployment topology deliberately** — an **agent** tier (one
   Collector per node/pod, receiving OTLP locally with minimal network
   hops) forwarding to a central **gateway** tier (fewer, larger
   Collector instances doing the heavier processing — tail sampling,
   PII scrubbing, multi-backend fan-out) scales further than either alone
   for most production deployments:
   ```yaml
   # agent (DaemonSet) — minimal processing, just forward to the gateway
   receivers:
     otlp:
       protocols:
         grpc: {}
         http: {}
   processors:
     batch: {}
     memory_limiter:
       check_interval: 1s
       limit_mib: 400
       spike_limit_mib: 100
   exporters:
     otlp:
       endpoint: otel-gateway.observability.svc:4317
       tls:
         insecure: false
   service:
     pipelines:
       traces:
         receivers: [otlp]
         processors: [memory_limiter, batch]
         exporters: [otlp]
       metrics:
         receivers: [otlp]
         processors: [memory_limiter, batch]
         exporters: [otlp]
       logs:
         receivers: [otlp]
         processors: [memory_limiter, batch]
         exporters: [otlp]
   ```

6. **Configure the gateway's full receiver → processor → exporter
   pipeline**, fanning out to multiple backends by signal type:
   ```yaml
   receivers:
     otlp:
       protocols:
         grpc:
           endpoint: 0.0.0.0:4317
         http:
           endpoint: 0.0.0.0:4318

   processors:
     memory_limiter:
       check_interval: 1s
       limit_mib: 1500
       spike_limit_mib: 400
     batch:
       timeout: 5s
       send_batch_size: 8192
     resource:
       attributes:
         - key: deployment.environment
           value: production
           action: upsert
     attributes/scrub:
       actions:
         - key: http.request.header.authorization
           action: delete
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

   exporters:
     prometheusremotewrite:
       endpoint: http://prometheus.observability.svc:9090/api/v1/write
     loki:
       endpoint: http://loki-gateway.observability.svc:3100/loki/api/v1/push
     otlp/tempo:
       endpoint: tempo.observability.svc:4317
       tls:
         insecure: false

   service:
     pipelines:
       traces:
         receivers: [otlp]
         processors: [memory_limiter, attributes/scrub, tail_sampling, batch]
         exporters: [otlp/tempo]
       metrics:
         receivers: [otlp]
         processors: [memory_limiter, resource, batch]
         exporters: [prometheusremotewrite]
       logs:
         receivers: [otlp]
         processors: [memory_limiter, resource, batch]
         exporters: [loki]
     telemetry:
       metrics:
         address: 0.0.0.0:8888
   ```
   Every processor listed here must also be **referenced inside the
   specific `service.pipelines.<signal>.processors` list it applies to**
   — a processor defined at the top level but never referenced in a
   pipeline is silently inert (see Common pitfalls).

7. **Order `memory_limiter` first in every pipeline's processor list.**
   It exists specifically to shed load *before* the rest of the pipeline
   (and the Collector process itself) runs out of memory — placing it
   anywhere else means the Collector can still OOM under load before the
   limiter gets a chance to act.

8. **Secure the OTLP receiver** with TLS and, for multi-tenant or
   internet-facing Collectors, an authentication extension rather than an
   open, unauthenticated ingest endpoint:
   ```yaml
   receivers:
     otlp:
       protocols:
         grpc:
           endpoint: 0.0.0.0:4317
           tls:
             cert_file: /etc/otel/tls/server.crt
             key_file: /etc/otel/tls/server.key
   extensions:
     bearertokenauth:
       token: "${OTLP_INGEST_TOKEN}"
   ```
   Never inline a real token/certificate in the config file — reference
   an environment variable or a mounted secret path.

9. **For tail-based sampling at scale, route by trace ID with a load
   balancing exporter** so every span belonging to the same trace lands
   on the same gateway instance — tail sampling requires seeing the whole
   trace before deciding, which is impossible if its spans are scattered
   across independent Collector replicas:
   ```yaml
   exporters:
     loadbalancing:
       routing_key: traceID
       protocol:
         otlp:
           tls:
             insecure: false
       resolver:
         k8s:
           service: otel-gateway-headless.observability.svc
   ```
   See
   [distributed-tracing-with-tempo-and-jaeger](../distributed-tracing-with-tempo-and-jaeger/SKILL.md)
   for the sampling-strategy tradeoffs (head vs. tail) this decision feeds
   into at the backend.

10. **Enable the Collector's own internal telemetry** (`service.telemetry.metrics`
    above, scraped on `:8888`) and treat it as a first-class monitored
    target, not an afterthought — this is the only way to see the
    Collector itself dropping data before someone notices a gap in a
    downstream dashboard.

## Best practices

- Default to auto-instrumentation; add manual spans/metrics only for
  business logic auto-instrumentation can't know about — hand-rolling
  spans for HTTP/DB calls auto-instrumentation already covers just adds
  maintenance burden for no benefit.
- Set `service.name`/`service.version`/`deployment.environment` once at
  SDK initialization (env vars or a Resource Detector), never derived
  ad hoc per span.
- Standardize on OTLP as the *only* protocol between applications and the
  Collector — let the Collector's exporters handle translation to
  vendor-specific formats (Prometheus remote-write, Loki push, a
  commercial APM's proprietary protocol) so application code never
  couples to a specific backend.
- Standardize the context-propagation format across every service in the
  organization and audit it explicitly whenever a new/legacy/third-party
  service is onboarded into an existing trace topology.
- Always put `memory_limiter` first in every pipeline's processor list —
  treat any pipeline missing it as a production risk, not a minor
  omission.
- Split agent and gateway tiers once volume/processing complexity
  justifies it (PII scrubbing, tail sampling, multi-backend fan-out
  belong at the gateway, not duplicated on every node's agent).
- Pin the exact Collector image version identically across agent and
  gateway tiers — mixed versions are a common source of subtly
  incompatible pipeline behavior that's hard to diagnose after the fact.
- Scrape and dashboard the Collector's own `:8888` internal metrics
  (`otelcol_processor_dropped_spans`, `otelcol_exporter_queue_size`,
  `otelcol_receiver_refused_spans`) as a standing part of the platform's
  own monitoring, not something checked only when someone reports missing
  data.

## Common pitfalls

- **Symptom:** An application is "instrumented with OTel" and configured
  with an OTLP endpoint, but the Collector never shows any spans/metrics
  arriving from it.
  **Fix:** Check the transport/port mismatch first — gRPC OTLP listens on
  `4317`, HTTP/protobuf OTLP on `4318`; an SDK configured for gRPC
  pointed at the HTTP port (or vice versa) fails silently or with an
  opaque connection error depending on the SDK. Also confirm the
  Collector's receiver is actually bound to `0.0.0.0` and not `localhost`
  if the app runs in a separate pod/container.

- **Symptom:** Metrics from a service show up fine in the backend, but
  its traces never do, even though both come from the same
  auto-instrumented process and the same Collector config "has" a traces
  pipeline.
  **Fix:** A processor or exporter can be defined at the top level of the
  Collector config and still be completely inert if it isn't referenced
  inside `service.pipelines.traces` specifically — YAML config validity
  doesn't imply pipeline wiring correctness. Confirm every receiver/
  processor/exporter intended for a signal is explicitly listed under
  that signal's `service.pipelines.<signal>` block; see
  [opentelemetry-configuration-validation](../opentelemetry-configuration-validation/SKILL.md)
  for a systematic pre-deploy check for exactly this mistake.

- **Symptom:** The Collector drops data under load with no visible error
  in application logs, and only the Collector's own internal metrics
  eventually reveal it.
  **Fix:** `memory_limiter` either isn't first in the processor chain, or
  its `limit_mib`/`spike_limit_mib` values are set too low for real
  traffic (or too close to the pod's actual memory limit, so the
  Collector OOMs before the limiter can shed load gracefully). Reorder it
  first, size it with headroom under the container's memory limit, and
  watch `otelcol_processor_refused_spans`/`otelcol_processor_dropped_spans`
  after any change.

- **Symptom:** Two services in the same request path show up as
  completely separate, disconnected traces instead of one trace spanning
  both.
  **Fix:** A context-propagation mismatch — one service uses a different
  propagator format (commonly a legacy B3-instrumented service alongside
  W3C-Trace-Context-instrumented ones) so the trace context isn't
  understood across that hop. Standardize `OTEL_PROPAGATORS` across every
  service in the call chain, prioritizing W3C Trace Context for new
  instrumentation.

- **Symptom:** A dashboard built from OTel-instrumented metrics explodes
  in series count and query latency shortly after a new auto-instrumented
  HTTP library update.
  **Fix:** Auto-instrumentation's `http.route`/`http.target` attribute can
  capture the raw, unparameterized request path (`/api/users/48213`
  instead of `/api/users/{id}`) if route templating isn't detected
  correctly for that framework/version, creating one series per unique
  path value. Add an `attributes` processor to normalize/drop the raw
  path attribute at the Collector before it reaches a metrics backend,
  and confirm the framework's route-template detection is actually
  working for auto-instrumentation to emit the templated form directly.

- **Symptom:** Spans stop arriving from a specific service intermittently
  under bursty traffic, and the Collector logs show exporter queue
  warnings.
  **Fix:** The exporter's `sending_queue`/`retry_on_failure` settings are
  either absent or sized too small for burst traffic, so the queue fills
  and the exporter starts dropping instead of buffering/retrying:
  ```yaml
  exporters:
    otlp/tempo:
      endpoint: tempo.observability.svc:4317
      sending_queue:
        enabled: true
        queue_size: 5000
      retry_on_failure:
        enabled: true
        max_elapsed_time: 60s
  ```

## Worked example

**Scenario:** `checkout-service` (Python) and `payments-service` (Java)
need distributed tracing across their shared request path, with metrics
routed to Prometheus, logs routed to Loki, and traces routed to Tempo —
all through a two-tier Collector deployment (per-pod agent → central
gateway).

1. Both services are instrumented with auto-instrumentation and a
   consistent resource/propagator configuration:
   ```bash
   OTEL_SERVICE_NAME=checkout-service
   OTEL_RESOURCE_ATTRIBUTES=service.version=2.14.0,deployment.environment=production
   OTEL_PROPAGATORS=tracecontext,baggage
   OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317   # local agent, not the gateway directly
   ```
   ```bash
   OTEL_SERVICE_NAME=payments-service
   OTEL_RESOURCE_ATTRIBUTES=service.version=1.9.2,deployment.environment=production
   OTEL_PROPAGATORS=tracecontext,baggage
   OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
   ```
2. Each pod runs a sidecar agent Collector (step 5's config) forwarding
   everything to the central gateway.
3. The gateway (step 6's config) applies `memory_limiter` first, scrubs
   the `authorization` header from span attributes, applies tail sampling
   (all errors, all requests over 500ms, plus a 10% baseline sample), and
   fans out: metrics → `prometheusremotewrite`, logs → `loki`, traces →
   `otlp/tempo`.
4. A checkout request that calls into `payments-service` produces one
   trace spanning both services because both share the same W3C
   Trace Context propagator — confirmed by pulling the trace in Tempo and
   seeing both services' spans nested under the same trace ID.
5. The gateway's `:8888` internal metrics are scraped by Prometheus and a
   dashboard panel tracks `otelcol_exporter_queue_size` and
   `otelcol_processor_dropped_spans` per exporter, so a future capacity
   problem shows up as a Collector-level alert rather than a silent gap
   discovered during an incident.

## Cross-references

- [opentelemetry-configuration-validation](../opentelemetry-configuration-validation/SKILL.md) — validating this exact pipeline config (pipeline wiring, sampling rates, resource attributes) before it ships, to catch silently dropped signals pre-rollout.
- [distributed-tracing-with-tempo-and-jaeger](../distributed-tracing-with-tempo-and-jaeger/SKILL.md) — the tracing backend this Collector's `otlp/tempo` exporter feeds, including backend-side sampling strategy and trace-to-metrics/logs correlation.
- [prometheus-and-grafana-monitoring-stack](../prometheus-and-grafana-monitoring-stack/SKILL.md) — the metrics backend this Collector's `prometheusremotewrite` exporter feeds, and where alerting on the Collector's own internal telemetry would be wired.
- [loki-log-aggregation-configuration](../loki-log-aggregation-configuration/SKILL.md) — the log backend this Collector's `loki` exporter feeds, including the label-cardinality discipline that also applies to any log-related resource attributes forwarded here.
- [incident-investigation-using-metrics-logs-traces](../incident-investigation-using-metrics-logs-traces/SKILL.md) — the cross-signal investigation workflow this instrumentation/Collector layer makes possible, by ensuring a trace ID actually propagates into logs and metrics exemplars.
