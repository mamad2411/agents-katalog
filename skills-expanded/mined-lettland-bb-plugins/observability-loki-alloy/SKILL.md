---
name: observability-loki-alloy
description: Use when shipping logs to Loki via Grafana Alloy — pipeline config, label cardinality, LogQL, retention, multi-tenant.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: observability
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [observability-essentials, observability-opentelemetry, infra-prometheus-grafana, infra-docker-swarm]
---

# Observability Loki + Alloy

**Iron Law: labels are LOW cardinality (service, env, level, host). IDs, paths, user IDs go in the LOG LINE — `| json` extracts them at query time. Mixing the two is how you OOM Loki. Alloy supersedes Promtail and Grafana Agent — start there for any new pipeline.**

**Versions:** Loki LTS `3.5.x` · Loki Current `3.7.x` · Next `3.8.x` — _Loki 3 is current; v2 reached EOL early 2025. Pin minor.patch in prod._ Alloy LTS `1.4.x` · Alloy Current `1.7.x` — _Alloy is the supported successor to Promtail (deprecated Feb 2025) and Grafana Agent (EOL Nov 2025). New pipelines go to Alloy; existing Promtail/Agent installs should migrate._

## What each piece is

| Piece       | Role                                                                                                                 |
| ----------- | -------------------------------------------------------------------------------------------------------------------- |
| **Loki**    | log aggregation TSDB; indexed on labels, NOT log content                                                             |
| **Alloy**   | Grafana's single binary for logs/metrics/traces; HCL-like config; OTel-compatible; replaces Promtail + Grafana Agent |
| **LogQL**   | Loki's query language (PromQL-flavored, with line/label filters + extractors)                                        |
| **Grafana** | dashboards; Logs panel with Prometheus split-screen                                                                  |

The `ci` stack pipes Docker logs per Swarm node into Alloy → Loki on a manager → Grafana on the same stack.

## Alloy config — Docker → Loki

Declarative HCL-like (not YAML). Each `<kind> "<label>" {}` block is a component; outputs wire into next inputs.

```hcl
// /etc/alloy/config.alloy
logging { level = "info"; format = "json" }

discovery.docker "containers" {
  host = "unix:///var/run/docker.sock"
  refresh_interval = "10s"
}

discovery.relabel "containers" {
  targets = discovery.docker.containers.targets
  rule { source_labels = ["__meta_docker_container_name"]; regex = "/(.*)"; target_label = "container" }
  rule { source_labels = ["__meta_docker_container_label_com_docker_swarm_service_name"]; target_label = "service" }
  rule { source_labels = ["__meta_docker_container_label_com_docker_stack_namespace"]; target_label = "stack" }
  // High-card stays OUT — no container_id, no task_id
}

loki.source.docker "containers" {
  host       = "unix:///var/run/docker.sock"
  targets    = discovery.relabel.containers.output
  forward_to = [loki.process.parse.receiver]
  labels     = { host = constants.hostname }
}

loki.process "parse" {
  forward_to = [loki.write.default.receiver]
  stage.json   { expressions = { level = "level" } }       // extract field
  stage.labels { values      = { level = "" } }            // promote to label (bounded set)
  stage.drop   { expression  = "GET /healthz .* 200"; drop_counter_reason = "healthcheck_noise" }
}

loki.write "default" {
  endpoint {
    url = "http://loki:3100/loki/api/v1/push"
    tenant_id = "ci"                                       // X-Scope-OrgID
  }
  external_labels = { cluster = "ci-swarm-prod", region = "eu-west-1" }
}
```

Drop the raw `/var/run/docker.sock` mount for a read-only socket proxy (`tecnativa/docker-socket-proxy` with `CONTAINERS=1`) — see `Skill(infra-docker-swarm)` for the same warning re Prometheus's `dockerswarm_sd_configs`.

## Other sources Alloy can tail

| Component                | Source                                                                             |
| ------------------------ | ---------------------------------------------------------------------------------- |
| `loki.source.file`       | static files (`path = "/var/log/app/*.log"`)                                       |
| `loki.source.docker`     | Docker engine API                                                                  |
| `loki.source.kubernetes` | k8s pods via API server                                                            |
| `loki.source.journal`    | systemd journal                                                                    |
| `loki.source.syslog`     | syslog over TCP/UDP/TLS                                                            |
| `loki.source.api`        | accept push from app SDK (Loki push API)                                           |
| `otelcol.receiver.otlp`  | OTel logs — Alloy is a drop-in collector, see `Skill(observability-opentelemetry)` |

The OTel receiver is the right choice for apps that already emit OTLP logs (the SDK ships them; Alloy receives + forwards to Loki).

## Label cardinality — THE killer

Each unique label-value combination is a separate **stream** in Loki. Loki indexes streams, not content. Streams have hard storage cost; query latency degrades past ~100k active streams per tenant.

| Good label (bounded)                                                               | Bad label (unbounded)                                                                                      |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `service`, `env`, `level`, `host`, `cluster`, `pod` (k8s), `container` (small set) | `user_id`, `request_id`, `trace_id`, `session_id`, raw URL path, error message text, IP address, timestamp |

**The rule**: if you can enumerate it on a whiteboard, it's a label. If a fresh value appears per request, it's a log-line field — query-extract with `| json` at read time:

```logql
{service="api", env="prod"} |~ "ERROR" | json | user_id = "abc-123"
```

Same answer, no cardinality cost. Loki's design assumes the log line is rich JSON and labels are the routing index.

## LogQL — patterns you'll use

```logql
{service="api", env="prod"}                              # stream selector
{service="api"} |~ "error" != "deadletter"               # line filter (regex / substring)
{service="api"} | json | status >= 500                   # parser → field filter
{service="api"} | json | label_format trace_short=`{{slice .trace_id 0 8}}`
sum by (route) (rate({service="api"} | json | status =~ "5.." [5m]))
quantile_over_time(0.99, {service="api"} | json | unwrap duration_ms [5m]) by (route)
```

`|~` regex, `|=` substring, `!=`/`!~` negations. Line filters run BEFORE parsers — order cheap-first.

## Retention

```yaml
# loki-config.yaml (Loki side, not Alloy)
limits_config:
  retention_period: 30d
  retention_stream:
    - { selector: '{service="audit"}', priority: 1, period: 365d }
    - { selector: '{service="debug-spam"}', priority: 2, period: 3d }
compactor:
  retention_enabled: true
  retention_delete_delay: 2h
```

Retention is enforced by the **compactor**; without `retention_enabled: true`, `retention_period` is decorative. `retention_stream` policies evaluated by priority (lowest wins).

## Multi-tenant

`X-Scope-OrgID` header partitions data, limits, queries:

```hcl
loki.write "tenant_api"     { endpoint { url = "http://loki:3100/loki/api/v1/push"; tenant_id = "api" } }
loki.write "tenant_billing" { endpoint { url = "http://loki:3100/loki/api/v1/push"; tenant_id = "billing" } }
```

Grafana sets `X-Scope-OrgID` per datasource. With `auth_enabled: false`, tenants are ignored (everything goes to `fake`). Enable `auth_enabled: true` + put an auth proxy (nginx + basic auth, OIDC) in front.

## Migration from Promtail

| Promtail                              | Alloy                                    |
| ------------------------------------- | ---------------------------------------- |
| `scrape_configs:` + `static_configs:` | `local.file_match` / `discovery.*`       |
| `pipeline_stages:`                    | `loki.process` + `stage.*`               |
| `clients:`                            | `loki.write "<name>" { endpoint {...} }` |
| `positions:` file                     | implicit in `loki.source.file`           |

Bootstrap: `alloy convert --source-format=promtail --output=config.alloy promtail.yaml`. Audit output — discovery semantics differ. Grafana Agent → Alloy: `--source-format=static`.

## When Loki is the wrong tool

- **Full-text search at petabyte scale** — line filter is sequential scan within selected streams. Use Elasticsearch / OpenSearch.
- **Very high cardinality structured events** (analytics) — ClickHouse / BigQuery; Loki bills on cardinality.
- **Traces** — Tempo, not Loki.
- **Year+ archival for compliance** — query cost on old data is high. Tier to cheaper store + S3 lifecycle.

## Anti-patterns

- `request_id`/`trace_id` as a Loki label — each request is a new stream; Loki OOMs.
- Free-form log lines — can't `| json`; queries become regex grep. Emit JSON from the start.
- Promtail in 2026 — deprecated; migrate to Alloy.
- `retention_enabled: false` with `retention_period` set — logs never delete.
- Raw `/var/run/docker.sock` into Alloy (root-on-host) — use a socket proxy.
- One Alloy on a manager pulling from every worker via TCP — push (Alloy per node) scales; pull is SPOF.
- `auth_enabled: true` without auth proxy — anyone sets `X-Scope-OrgID` and reads anyone's logs.

## Red flags

| Thought                                    | Reality                                                                  |
| ------------------------------------------ | ------------------------------------------------------------------------ |
| "More labels = better queries"             | More labels = more streams = OOM. Labels are for routing, not search.    |
| "We'll regex-search all log content"       | Regex on petabytes is slow. Filter by label first, regex last.           |
| "Promtail still works, why migrate?"       | EOL Feb 2025. Security fixes stop. Migrate before you forget.            |
| "30 days retention is fine for everything" | Audit logs need longer; debug noise needs shorter. Per-stream retention. |

## Hand-off

For the metrics half of the same Grafana stack (Prometheus, recording rules, alerts; at-scale concerns in `references/prometheus-scale.md`): `Skill(infra-prometheus-grafana)`. For traces via the same Alloy binary as an OTel collector: `Skill(observability-opentelemetry)`. For the broader log-vs-metric-vs-trace pillar choice and structured logging primer: `Skill(observability-essentials)`. For the Docker Swarm context where this stack runs: `Skill(infra-docker-swarm)`.
