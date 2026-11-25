---
name: follow-service-signoz-setup-signoz
description: Prepare the SigNoz backend (cloud or self-hosted), install the OpenTelemetry SDK, and instrument the Bun/Node/TypeScript app so it can send telemetry — first-time setup only
related:
  - follow-service-signoz
---

## Goal

Prepare the SigNoz backend (cloud or self-hosted), install the OpenTelemetry SDK, and instrument the Bun/Node/TypeScript app so it can send telemetry — first-time setup only

## Scope

- Choose and prepare SigNoz Cloud or self-hosted via Docker/Foundry
- Install `@opentelemetry/api` and `@opentelemetry/auto-instrumentations-node`
- Set the minimum endpoint and ingestion key so telemetry can send
- Does not cover detailed service name, exporters, dashboards → use `workflows/config-signoz/SKILL.md`

## Execute

### 1. Check Prerequisites

> Goal: Identify the runtime and pick the deployment mode (idempotent)

1. Read `package.json` to identify the runtime (`bun`, `node`, TypeScript)
2. Check whether OTel packages or instrumentation already exist → if so, skip to verify
3. Decide `SigNoz Cloud` or `self-hosted` — self-hosted requires Docker
4. If there is no SigNoz account/endpoint → stop and tell the user

### 2. Prepare SigNoz Endpoint

> Goal: Get the correct endpoint and ingestion key

1. Cloud: prepare `https://ingest.<region>.signoz.cloud:443` and the ingestion key from the dashboard
2. Self-hosted: install via Foundry or Docker per `https://signoz.io/docs/install/docker/` — a local endpoint such as `http://localhost:4318`
3. Store the ingestion key in `/follow-secret-manager`, then inject it into env
4. Confirm the endpoint is reachable before instrumenting

### 3. Install OTel SDK

> Goal: Install auto-instrumentation

1. Install with `bun add @opentelemetry/api @opentelemetry/auto-instrumentations-node`
2. Set `NODE_OPTIONS=--require @opentelemetry/auto-instrumentations-node/register` for Node
3. For Bun/TS entries where the require hook does not work → use `import '@opentelemetry/auto-instrumentations-node/register'` as the first line of the entry instead
4. Set the minimum env: `OTEL_TRACES_EXPORTER=otlp`, `OTEL_EXPORTER_OTLP_ENDPOINT=<endpoint>`, `OTEL_SERVICE_NAME=<name>`

### 4. Verify Telemetry

> Goal: Confirm traces really reach the SigNoz UI

1. Run the app with instrumentation and send test requests
2. Open the SigNoz UI and check Services/Traces for the service name
3. If it does not appear within 5 minutes → check endpoint, ingestion key, protocol, then set `OTEL_LOG_LEVEL=debug`
4. If it still fails → do `resolve-errors` max 3 rounds, then stop and report

## Rules

- Limit the scope to Bun/Node/TypeScript only — for other runtimes check official docs
- Store the ingestion key in `/follow-secret-manager` — never hardcode or commit
- Use official docs (`learn` (web)/`webfetch`) as the primary source when unsure about an env var
- If telemetry cannot be confirmed within 3 rounds → stop and report

## Expected Outcome

- OTel SDK installed and the app runs with instrumentation
- Endpoint/ingestion key correct and secure
- Traces really appear in the SigNoz UI
