---
name: add-telemetry-instrumentation
description: Add or update logging, metrics, and tracing by following the repo's observability patterns and OpenTelemetry (OTel) GenAI Semantic Conventions. Use when a service, feature, endpoint, job, or integration needs operational visibility — including AI/LLM features requiring token-level tracing (gen_ai.usage.tokens, gen_ai.response.model, TTFT), kernel-level eBPF socket telemetry, and MWMBR SLI recording rules.
version: 2.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Add Telemetry Instrumentation

Use this skill when code changes need matching observability so operators can understand traffic, failures, latency, and dependency behavior.

## When to Use

- a service/endpoint/feature needs operational visibility
- adding logs, metrics, or distributed traces (OTel v1.30+)
- tracing AI/LLM token usage, response models, and Time-To-First-Token (TTFT)
- instrumenting kernel-level eBPF socket profiling without sidecar tax
- defining Multi-Window Multi-Burn-Rate (MWMBR) SLI recording rules

## Core Rules

- follow the repo's existing logging, metrics, and tracing patterns
- instrument important boundaries rather than every line of code
- keep telemetry names, labels, and dimensions stable enough for dashboards and alerts
- avoid high-cardinality labels unless the repo explicitly supports them
- never log secrets, credentials, tokens, or unnecessary sensitive data
- **W3C-DISTRIBUTED-TRACING**: enforce end-to-end W3C `traceparent` and `tracestate` context propagation across all HTTP, gRPC, and asynchronous message boundaries (Kafka, Dapr, RabbitMQ)
- **EBPF-SOCKET-TELEMETRY**: deploy kernel-level eBPF socket profiling (Cilium Hubble, Grafana Beyla, Coroot) to capture L4/L7 flow telemetry, TCP retransmits, socket buffer queue drops, and DNS resolution latency directly from kernel space without injecting sidecar proxies
- **OTEL-V130-GENAI-CONVENTIONS**: use stable OpenTelemetry GenAI conventions (opt in via `OTEL_SEMCONV_STABILITY_OPT_IN=genai`); mandate `gen_ai.system`, `gen_ai.request.model`, `gen_ai.response.model`, `gen_ai.usage.tokens`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.finish_reasons`, and Time-To-First-Token (TTFT) for streaming responses
- **MWMBR-SLI-RECORDING-RULES**: configure Prometheus/OTel metric recording rules supporting Multi-Window Multi-Burn-Rate (MWMBR) error budget alerting across short (5m, 30m, 2h) and long (1h, 6h, 3d) evaluation windows with empty-vector coalescing (`or on() vector(0)`)
- **OTEL-PROFILING-4TH-PILLAR**: use continuous profiling via the OTLP profiling signal (public Alpha since 2026-03; eBPF agent collects most languages with zero code changes) alongside logs/metrics/traces — Pyroscope and Parca are the reference backends; treat the signal as alpha and keep a Parca/Pyroscope-native export path
- **NATIVE-HISTOGRAMS**: prefer native exponential histograms for dynamic bucket resolution over fixed-bucket counts
- **DORA-METRIC-SPANS**: emit CI/CD and deployment spans (`cicd.pipeline.run.*`, `deploy.environment`) for automated DORA metric computation

## Suggested Process

### 1. Identify Critical Paths
Determine key entrypoints, dependency calls, background jobs, and failure domains needing visibility.

### 2. Add Structured Logging
Add logs for meaningful state changes, warnings, and errors with standard request and correlation IDs.

### 3. Configure Metrics & MWMBR Recording Rules
Add counters and latency histograms for user journeys. Configure multi-window recording rules for error budget burn rates.

### 4. Instrument Distributed Tracing & W3C Context
Propagate W3C `traceparent` across service boundaries, database queries, and async queues. For LLMs, emit GenAI semantic convention attributes.

### 5. Attach eBPF Kernel Telemetry
Deploy zero-overhead eBPF probes for TCP retransmit rates, DNS latency, and socket buffer drops without adding sidecar containers.

### 6. Validate Sensitive Data Handling
Confirm that logs, metric labels, and span attributes do not expose secrets, credentials, or PII.

## Checklist

- [ ] existing telemetry pattern reviewed and critical paths identified
- [ ] structured logs added with correlation IDs
- [ ] metrics and MWMBR SLI recording rules configured for short and long windows
- [ ] distributed tracing instrumented with unbroken W3C traceparent propagation
- [ ] OpenTelemetry v1.30+ GenAI conventions applied (`gen_ai.usage.tokens`, `gen_ai.response.model`, TTFT)
- [ ] kernel-level eBPF socket and network flow telemetry verified without sidecar overhead
- [ ] sensitive data exposure checked and restricted fields redacted
- [ ] dashboards, alerts, and runbooks updated

## Failure Modes

- **Instrumentation added without a dashboard**: metric emitted without consumer. **Mitigation:** require dashboard mapping for every core metric.
- **PII in span attributes**: credential or PII in traces. **Mitigation:** classify attributes and redact restricted fields before export.
- **Sidecar performance degradation**: proxy sidecars causing CPU/latency spikes. **Mitigation:** replace with kernel-level eBPF socket monitoring.
- **Alert flapping on low traffic**: burn-rate alerts firing falsely during traffic dips. **Mitigation:** configure PromQL empty vector coalescing (`or on() vector(0)`).

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: `infrastructure_changes[]`, `config_updates[]`, and `validation_run`. Set `produced_by_role` to the emitting developer role.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: classify telemetry payloads with `data-classification.yaml` and redact credentials.
- **ASI04 Supply Chain**: OTel SDKs, exporters, and collectors must be schema-validated against expected manifests.
- **ASI05 RCE Guard**: never construct telemetry processors or exporters from untrusted external content.
- **ASI07 Inter-Agent Communication**: emit structured contracts so downstream SRE and security roles can validate.
- **ASI09 Human-Agent Trust Exploitation**: verify live telemetry stream before declaring rollout complete.

## Related Skills

- **debug-runtime-platform**: Investigate runtime behavior using telemetry evidence
- **orchestrate-chaos-experiment**: Validate telemetry signals and alert triggering during simulated faults
- **incident-report**: Connect telemetry evidence and trace IDs to incident postmortems
- **setup-deployment**: Wire telemetry config into runtime source of truth
- **performance-profiling**: Measure latency, throughput, or resource bottlenecks
- Companion reference: `references/opentelemetry-semantic-conventions-2026.md`
- Companion example: `examples/kratos-otel-middleware-instrumentation.go`
