---
description: "Spring Boot Micrometer Tracing and OpenTelemetry OTLP contract for application tracing."
applyTo: "**/*Tracing*.java, **/src/main/resources/application*.yml, **/src/main/resources/application*.yaml, **/logback*.xml"
---

# Spring Boot Tracing Contract

Apply this contract when a module adds distributed tracing with Micrometer Tracing
and OpenTelemetry. It does not replace the logging, actuator, controller, or pom
contracts.

## Stack

- Use Spring Boot's OpenTelemetry support via `spring-boot-starter-opentelemetry`.
- Prefer Micrometer Tracing with the OpenTelemetry bridge. Do not add Brave / Zipkin
  unless the user explicitly asks for that stack.
- Export traces with OTLP to a Collector (or compatible backend). Do not invent a
  custom HTTP exporter.

## Configuration

- Set `management.tracing.sampling.probability` to `1.0` for local demos so every
  request produces spans. Use a lower probability in production when volume or cost
  requires it, and document why.
- Configure OTLP with `management.opentelemetry.tracing.export.otlp.endpoint` (HTTP
  protobuf default), pointing at the Collector (for example
  `http://localhost:4318/v1/traces`).
- Disable OTLP metrics export (`management.otlp.metrics.export.enabled=false`) when the
  Collector pipeline is traces-only, so demos do not spam failed `/v1/metrics` posts.
- Disable OTLP export in `application-test.yml` so context tests do not require a
  running Collector.
- Give each traced service a distinct `spring.application.name`.

## Propagation and HTTP clients

- Build outbound `RestClient` instances from the auto-configured `RestClient.Builder`
  (requires `spring-boot-starter-restclient`) so observation and W3C trace context
  propagate automatically.
- Do not manually set `traceparent` headers in application code for ordinary HTTP
  calls when Boot instrumentation covers the client.

## Log correlation

- When a module enables Micrometer Tracing, include MDC `traceId` and `spanId` in
  that module's Logback console and file patterns.
- Do not add correlation IDs to modules that do not depend on tracing.

## Forbidden

- Never use Brave as the default tracing bridge when OpenTelemetry was requested.
- Never require a trace UI (Jaeger, Tempo, Grafana) for a Collector-only setup.
- Never hardcode sampling below `1.0` in local demos without documenting why.
- Never create a custom `RestClient.builder()` for traced calls when the observed
  auto-configured `RestClient.Builder` bean is available.
