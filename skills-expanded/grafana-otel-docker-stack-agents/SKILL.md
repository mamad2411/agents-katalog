# AGENTS.md

## Purpose

This repository is a minimal local observability stack for Grafana, OpenTelemetry Collector, Prometheus, Loki, and Tempo, orchestrated with Docker Compose.

Use this file for project-specific operating guidance. Read the config files directly for exact runtime behavior.

## Working Surface

- Main entrypoint: [docker-compose.yml](./docker-compose.yml)
- Collector config: [config/otelcol.yml](./config/otelcol.yml)
- Prometheus scrape config: [config/prometheus.yml](./config/prometheus.yml)
- Loki config: [config/loki.yml](./config/loki.yml)
- Tempo config: [config/tempo.yml](./config/tempo.yml)
- Grafana datasource provisioning: [config/grafana/provisioning/datasources/datasources.yml](./config/grafana/provisioning/datasources/datasources.yml)

## Common Commands

- Start the stack: `docker compose up -d`
- Stop the stack: `docker compose down`
- Recreate after config changes: `docker compose up -d --force-recreate`
- Inspect service state: `docker compose ps`
- Inspect logs for one service: `docker compose logs SERVICE`

## Architecture

- `otel-collector` is the ingestion entrypoint for OTLP over gRPC on `4317` and OTLP over HTTP on `4318`.
- The collector fans out telemetry by signal type:
  - traces -> Tempo via OTLP gRPC
  - logs -> Loki via OTLP HTTP
  - metrics -> Prometheus by exposing a scrape target on `9464`
- Prometheus scrapes only the collector endpoint defined in [config/prometheus.yml](./config/prometheus.yml).
- Grafana stores its application data in the `postgres` service, not in the container filesystem.
- Grafana is pre-provisioned with Prometheus, Loki, and Tempo datasources; datasource changes should usually be made in the provisioning YAML, not through the UI.

## Editing Guidance

- Keep service names stable unless you also update every dependent config reference. The current internal hostnames are shared across Compose and provisioning files.
- When changing ports or endpoints, update both the publishing service and every consumer config that references it.
- For stateful services that other containers depend on, prefer a real `healthcheck` plus `depends_on.condition: service_healthy` over startup ordering alone.
- For `postgres:18+`, mount the named volume at `/var/lib/postgresql`, not `/var/lib/postgresql/data`.
- Prefer editing mounted YAML files over adding container command-line flags unless the image already expects that pattern.
- Keep this repo minimal. Avoid introducing extra services, scripts, or app code unless the task explicitly requires it.

## Validation

- After editing Compose or YAML config, validate by starting the stack with `docker compose up -d`.
- Use `docker compose logs` for the touched service if startup fails.
- For Grafana provisioning changes, verify the datasources appear after Grafana restarts.

## Known Project Conventions

- Config files live under `config/` and are bind-mounted read-only into containers.
- This repo currently has no application source tree, test suite, or build system outside Docker Compose.