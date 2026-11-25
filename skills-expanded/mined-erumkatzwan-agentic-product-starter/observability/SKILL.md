---
name: observability
description: Use when adding a feature that should be measured, when debugging a problem in Dev, SYST or Prod, when connecting Grafana Cloud or Sentry for an environment, or on request ("add metrics", "why is it slow", "set up monitoring"). Covers OpenTelemetry in the backend, the local Grafana stack, dashboards and crash reporting.
---

# Observability

Read [ADR-0008](../../../docs/adr/0008-observability.md) and `observability/README.md` first.

## 1. Run the stack locally

```bash
docker compose -f observability/docker-compose.yml up -d
cd backend && dotnet run --project src/AgenticProduct.Api --launch-profile Dev
```

Grafana: <http://localhost:3000> (admin / admin). Use **Explore → Tempo** for a slow or failing request, then jump to its logs.

## 2. Instrument a new feature

Ask: "How will we know this feature works and is used?" Then:

1. **Product metric.** Add a counter (events) or histogram (durations, sizes) to `backend/src/AgenticProduct.Api/Observability/AppMetrics.cs`.
   * Name: `app.<noun>.<verb in past tense>` or `app.<noun_plural>`, lower case with dots and underscores, for example `app.orders.placed`.
   * Tags: a few low-cardinality values only (`result`, `plan`, `platform`). Never user IDs, emails or free text.
2. **Call it** where the event happens (endpoint or service), and cover it with a test that listens with `MeterListener` (see `ObservabilityTests.cs`).
3. **Logs:** use `ILogger` with message templates (`"Order {OrderId} placed"`), never string concatenation, never personal data.
4. **Traces:** incoming requests and `HttpClient` calls are traced already. For a slow internal step, add an `ActivitySource` span named after the step.
5. **Dashboard:** add a panel to `observability/grafana/dashboards/api-overview.json` (or a new dashboard), filtered with `job=~"$service", deployment_environment_name=~"$environment"`. Prometheus names: dots become underscores and counters end in `_total` (`app_orders_placed_total`).
6. Run the stack, click through the feature, and check the panel shows data. CI's **Observability smoke test** runs every dashboard query and fails on empty ones, so add traffic for new endpoints to `.github/workflows/observability.yml`.

## 3. Connect an environment

* **Backend → Grafana Cloud:** set `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` and `OTEL_EXPORTER_OTLP_HEADERS` as secrets on the host (steps in `observability/README.md`). Import the dashboards.
* **Apps → Sentry:** one Sentry project per app, one DSN per environment, set at build time. No DSN means reporting is off.

Never commit endpoints with tokens, DSNs for Prod, or Grafana API keys.

## 4. Review checklist

- [ ] New user-facing behaviour has a metric and a dashboard panel
- [ ] No personal data in spans, tags or logs
- [ ] Tag values are low-cardinality
- [ ] Errors are logged once, where they are handled, with the exception attached
- [ ] Observability smoke test is green
