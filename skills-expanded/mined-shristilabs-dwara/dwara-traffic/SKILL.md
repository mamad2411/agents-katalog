---
name: dwara-traffic
description: Configure Dwara API gateway routing and traffic management - route matching precedence (exact/regex/prefix), listeners, rewrites and redirects, load balancing (round robin, least requests, ip_hash, maglev, peak-EWMA), passive and active health checks, retries with hedging, circuit breakers, timeouts, traffic splitting and canary analysis, sticky sessions, response caching, transforms, CORS/compression/limits, admission control and load shedding, WebSocket/gRPC/h3/L4 proxying. Use for any dwara.yaml work on listeners, routes, services, upstreams, or resilience behavior.
license: Apache-2.0
compatibility: Works in any agent harness supporting the Agent Skills spec. Needs dwara-cli on PATH for validate/explain/diff.
metadata:
  author: shristilabs
  repo: https://github.com/shristilabs/dwara
  docs: https://shristilabs.github.io/dwara/
  version: "0.1.1"
---

# Dwara traffic management

How requests flow: **listener** (TLS/protocol) -> **route match** (path
first, other criteria AND-ed after) -> **route action** (proxy / redirect /
respond / mock / ai) -> **service** (direct upstream, weighted split, or
sticky) -> **upstream pool** (balancer, health, retries, breaker, timeouts).

## The one rule everyone gets wrong: match precedence

Path resolution is fixed and independent of declaration order:

```
exact  >  regex  >  prefix
```

- Among `exact` (radix-tree, static segments beat `{param}` templates),
  among `prefix` the **longest** byte-prefix wins (`/v1` matches
  `/v1anything` - no segment boundary required), among `regex` the
  **first declared** wins (no specificity ranking; avoid `regex: /.*`
  catch-alls - they shadow every prefix route).
- One path resolves to **at most one route**. Non-path criteria (`methods`,
  `host`, `headers`, `query`, `cookies`, `accept`) are AND-ed *after* path
  resolution; a criteria miss is a **404 with no fall-through** to another
  candidate. Don't model "same path, different versions" as two routes.
- Debug with `dwara-cli explain --config dwara.yaml --method GET --path /x
  [--header ...]`; `dwara-cli lint` flags `regex-shadowed-by-exact` and
  `prefix-duplicate`.

Details + rewrite/redirect semantics:
[references/routing-and-matching.md](references/routing-and-matching.md).

## Balancing and pools

Six balancers (`round_robin`, `least_requests`, `random`, `ip_hash`,
`maglev`, `peak_ewma`), `hash_on` for cookie/header affinity at the pool
level, endpoint weights, passive (outlier) + active (HTTP probe) health,
DNS discovery, slow start, connection caps.

[references/upstreams-and-balancing.md](references/upstreams-and-balancing.md)

## Resilience

- **Retries**: attempts + exponential backoff + budget_percent +
  `retry_statuses` + `total_deadline_ms`; only before response headers;
  429-retries honor `Retry-After`.
- **Hedging**: speculative duplicate after `hedge_after_ms` to a *different*
  endpoint, loser cancelled; requires `buffer_max_bytes > 0`.
- **Breakers + health ejection** with half-open probing.
- **Admission control**: `max_concurrent_requests` + bounded
  priority-aware `admission_queue`; `load_shed_dry_run` to observe.
- **Traffic splitting**: weighted `split` targets, weight `0` = blue-green
  parking, auto-`canary_analysis` (exactly 2 targets) with promote/rollback
  metrics; **keep total weight constant when ramping** or requests
  reshuffle.

[references/resilience-and-admission.md](references/resilience-and-admission.md)

## Caching and request/response control

Route-level `cache` (keyed route+method+consumer+path+query+`vary`;
GET/HEAD only; `s-maxage`/`max-age`/`ttl_secs`; stale-while-revalidate;
coalescing), `transforms` (set/add/remove headers, query add),
`compression`, `cors`, `limits`, `security_headers`, `masking`
(fail-closed), `request_validation` (JSON-Schema body), purge via
`POST /cache/purge` (`{route}` | `{all}` | `{tag}` via upstream
`Cache-Tags` | `{url, prefix}`).

[references/caching-and-transforms.md](references/caching-and-transforms.md)

## Protocols beyond HTTP/1.1 plaintext

| Need | Surface |
| --- | --- |
| h2/h2c | listener `protocol` http/https; upstream `protocol: http2` (h2+TLS) or `h2c` (prior knowledge) |
| HTTP/3 ingress + upstream | `protocol: h3` — compiled into every build (listener with `tls` + string `alt_svc` like `h3=":8444"; ma=86400`; upstream over QUIC, TLS 1.3 always, trust via `trusted_ca_file`) |
| gRPC | zero-config proxying over h2 upstreams, trailers pass through |
| gRPC-Web | `grpc_web` route block (`enabled: true`, `transcoding: {enabled, descriptors[]}` with FileDescriptorSets) — config validates; request-path translation is scaffolded, verify in your build |
| WebSocket | route `websocket` block: `origins` (missing Origin = reject 403), `max_frames_per_sec`, `idle_timeout_s`, `max_frame_size_bytes` |
| L4 TCP/UDP | listener `protocol: tcp|udp` + `l4` block — compiled into every build; UDP LB is per-datagram source hash |
| Protocol translation | route `translation: {kind, graphql|soap}` for rest<->graphql and rest<->soap — config validates; request-path translation is scaffolded. JSON<->gRPC goes through `grpc_web.transcoding`, not `translation` |
| TLS everywhere | terminate (multi-SNI) / SNI passthrough; `pq: true` for post-quantum X25519MLKEM768 hybrid — compiled into every build (experimental, FIPS-incompatible) |

Runnable examples: [assets/traffic.yaml](assets/traffic.yaml).

## Quick decision table

| Goal | Minimal correct config |
| --- | --- |
| Route + strip `/v1` prefix | route `match.path.type: prefix` + `action.rewrite.type: strip_prefix` |
| Kill a flaky endpoint quickly | upstream `health` (consecutive_failures/eject_ms) - passive outlier detection |
| Survive slowness, not just errors | `retries.hedge` (hedge_after_ms + buffer_max_bytes) |
| Protect the origin | `breaker` + `connection_cap`/`max_pending` + route `priority` |
| Protect the gateway | `max_concurrent_requests` + `admission_queue` (+ `load_shed_dry_run` first) |
| Blue-green | `split` with one target at `weight: 0`, flip on release |
| Gradual rollout with auto-rollback | `split` + `canary_analysis` (exactly 2 targets, error_rate/latency metrics) |
