---
name: dwara-operations
description: Operate a running Dwara API gateway - enable and call the mTLS admin API (config GET/PATCH, entity CRUD with ETags, cache purge, credentials, analytics), hot reload and config generations, zero-downtime binary upgrade, observability (metrics, access logs, OTLP export), rate limiting and quotas, embedded analytics and exports, synthetic monitoring, replay debugging, and 503/429/reload troubleshooting. Use for any task against a running gateway or its admin API, or when triaging gateway behavior.
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec. Admin API calls need curl with client certificates; scripts assume bash.
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.0"
---

# Dwara operations

The gateway is operated through three planes:

1. **Config plane** - the YAML file (hot-reloaded) or `PATCH /config`.
2. **Admin plane** - the mTLS admin API (default `127.0.0.1:2019`, off
   unless an `admin:` block exists).
3. **Observability plane** - `/metrics` on every listener, structured JSON
   logs on stdout, optional OTLP export.

## Enabling the admin API

```yaml
admin:
  bind: 0.0.0.0:2019
  tls:
    cert_file: /certs/server.crt     # ALL THREE FILES MANDATORY -
    key_file: /certs/server.key      # missing client_ca_file is rejected
    client_ca_file: /certs/client-ca.crt
  # api_tokens: { tokens: [ { token_hash: <sha256-hex>, role: admin|readonly } ] }
  # rbac: { bindings: [ { cert_fingerprint: <sha256-of-DER>, role: admin } ] }
  # audit: { enabled: true }
```

Every call needs a client certificate chaining to `client_ca_file`
(+ `Authorization: Bearer` if api_tokens are configured). Dev-only escape
hatch: `DWARA_ADMIN_DEV=1` plaintext loopback - never in production.

```sh
curl --cert client.crt --key client.key --cacert server.crt \
     https://127.0.0.1:2019/health
```

Full endpoint table incl. entity CRUD ETag rules:
[references/admin-api.md](references/admin-api.md).

## The operating loop

```sh
dwara-cli status [--admin URL]    # one-shot: readiness, generation, health
dwara-cli top                     # live LB/breaker view
curl .../stats?format=prometheus | grep -E 'breaker|active_requests'
```

Health-check script bundling the essentials:
[scripts/dwara-doctor.sh](scripts/dwara-doctor.sh).

## Reloads and upgrades

| Job | Mechanism |
| --- | --- |
| Apply config change | Save the file (watcher) or `SIGHUP` or `PATCH /config` - one pipeline, atomic generation swap; failures keep the previous generation serving |
| Verify what's live | `GET /runtime_info` / `GET /config` (`x-dwara-config-generation` header) |
| Compare candidates | `dwara-cli diff old.yaml new.yaml` |
| Upgrade the binary with zero downtime | `SIGUSR2` hand-off (`dwara-cli upgrade`); old process drains, new binds same ports; failure keeps old serving |
| Drain & stop | `SIGTERM` (bounded by `DWARA_SHUTDOWN_TIMEOUT_SECS`) |

Details + systemd notes: [references/lifecycle.md](references/lifecycle.md).

## Observability

- `/metrics` on every listener: Prometheus text. Families to know:
  `requests_total`, `request_duration_seconds`, `breaker_state`,
  `endpoint_health`, `active_requests`, `config_generation`,
  `rate_limited_total`, `dwara_slo_burn_rate`, `dwara_policy_dry_run_total`,
  `dwara_waf_total`, `dwara_ai_*`, `dwara_admission_queued_total`.
- Access log line per request with `request_id` + outcome flags
  (`rate_limited`, `broken`, `shed`); echoed as `X-Request-Id`.
- OTLP: `DWARA_OTLP_ENDPOINT` (+ `DWARA_OTLP_METRICS_INTERVAL_SECS`, 15s
  default); the gateway appends `/v1/traces` and `/v1/metrics`.
- Full env-var table: [references/observability.md](references/observability.md).

## Rate limits and quotas (traffic control the operator owns)

- Local rate limits are config-only (`policies[].rate_limit` /
  `rate_limits[]` with `selector: [ip, credential, route]`, stacked windows
  must all admit). Every decision - allow or deny - stamps
  `X-RateLimit-Limit/-Remaining/-Reset`; denials add `Retry-After`.
  Reserved paths are exempt from `global_policies` limits.
- Quotas are **consumer daily/monthly caps** (`consumers[].quotas`, UTC
  windows) enforced through the state store - `DWARA_STATE_DB` must be set
  or quotas are not enforced. `GET /quotas/usage` reports counters.
- Distributed (Redis) limiter/quota stores are enterprise.

## Analytics

`analytics:` block = embedded SQLite request analytics: per-granularity
rollups with retention, header/claim-sourced custom dimensions, live
sketches (`/analytics/live`), ML insights (`/analytics/forecast`,
`/analytics/anomalies`), scheduled CSV/JSON usage exports, and an NDJSON
firehose (`analytics_stream`, webhook sink today). Plus event `webhooks[]`
(breaker/ejection/config events) and `synthetic` route probes feeding
alerting. Details in the observability reference.

Replay debugging: `dwara replay capture --duration 60s --output trace.dwara`
(ring buffer, secrets redacted, <=10 min) then
`dwara replay run --trace trace.dwara [--diff]` offline - MATCH/DIVERGENCE
table against a candidate config.

## Troubleshooting index (docs-site playbooks)

| Symptom | Start with |
| --- | --- |
| 503s | upstream health/ejection/breaker state - `GET /health`, `breaker_state` |
| 429s | disambiguate by error `code`: rate limit vs quota vs `ai_budget_exceeded` |
| Reload didn't apply | failed validation keeps old generation; logs list every issue |
| High latency | access-log `duration_ms`; pool/queue/upstream attribution |
| TLS handshake failures | `dwara_tls_handshake_failures_total`; chain/CA problems |
| AI request failures | OpenAI-shaped error envelope; pipeline phase codes |

## Standing rules

- Never PATCH a redacted config back - `GET /config` output contains
  placeholders that 400 on write. Edit the file, reload.
- `PATCH /config` is **full-document** replacement; dry-run compile happens
  automatically, atomic write only on success.
- Entity CRUD (`/routes`, `/services`, `/upstreams`, `/consumers`,
  `/policies`) carries `ETag` - send `If-Match` for optimistic concurrency
  or accept last-write-wins.
- Admin RBAC roles: `admin` and `readonly` - give humans readonly, agents
  the narrowest role that works.
