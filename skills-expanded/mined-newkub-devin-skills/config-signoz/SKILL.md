---
name: follow-service-signoz-config-signoz
description: Set/edit OpenTelemetry configuration for SigNoz — service name, resource attributes, traces/metrics/logs exporters, and headers — without clobbering the existing env
related:
  - follow-service-signoz
---

## Goal

Set/edit OpenTelemetry configuration for SigNoz — service name, resource attributes, traces/metrics/logs exporters, and headers — without clobbering the existing env

## Scope

- Edit `OTEL_*` env vars for Bun/Node/TypeScript
- Separate config per environment (dev/staging/prod)
- Set headers (`signoz-ingestion-key`), protocol, and resource attributes
- Does not cover first-time install → use `workflows/setup-signoz/SKILL.md`

## Execute

### 1. Read Current Config

> Goal: Know the current env vars before editing

1. Read `.env*`, start scripts, and existing instrumentation entries
2. Do `/check-secrets env-vars` to identify missing or duplicated `OTEL_*` vars
3. Do `/deep-review-codebase` domain `review-config` across environments if needed
4. If there are no OTel packages yet → do `workflows/setup-signoz/SKILL.md` instead

### 2. Configure Service Identity

> Goal: Set service name and resource attributes so it is searchable in the UI

1. Set `OTEL_SERVICE_NAME=<service-name>` matching the real service name
2. Set `OTEL_RESOURCE_ATTRIBUTES=service.version=<version>` and additional attributes such as `deployment.environment=<env>`
3. Use the same name across all instances of one service — merge only the necessary keys

### 3. Configure Exporters

> Goal: Send all three signals — traces, metrics, logs

1. Set `OTEL_TRACES_EXPORTER=otlp`, `OTEL_METRICS_EXPORTER=otlp`, `OTEL_LOGS_EXPORTER=otlp` per the wanted signals
2. Set `OTEL_EXPORTER_OTLP_ENDPOINT=<endpoint>` — separate per-signal endpoints if needed
3. Cloud: set `OTEL_EXPORTER_OTLP_HEADERS=signoz-ingestion-key=<key>` — key from `/follow-secret-manager`
4. For Bun, always set `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`
5. Logs: use the OTLP logs exporter or route through an OpenTelemetry Collector per the architecture — see official docs

### 4. Verify

> Goal: Confirm all three telemetry signals really reach the UI

1. Restart the app with the new env and send test traffic
2. Check Traces, Logs Explorer, and Metrics Explorer in the SigNoz UI
3. If nothing appears → set `OTEL_LOG_LEVEL=debug` to see exporter errors, check headers/endpoint/protocol
4. Do `/run-verify` — if it fails → revert the keys just changed, do `resolve-errors`, then report the diff

## Rules

- Merge only the necessary `OTEL_*` keys — never overwrite the whole `.env`
- Store the ingestion key in `/follow-secret-manager` — never in a committed config file
- `service.name` must stay consistent across environments (separate with `deployment.environment`)
- Use official docs as the primary source — do `learn` (web) if unsure
- If telemetry cannot be confirmed within 3 rounds → stop and report

## Expected Outcome

- `OTEL_*` config complete and clearly separated per environment
- Traces, metrics, and logs appear in the SigNoz UI under the correct service name
- No secrets leaking into config files
