---
description: Nginx/OpenResty edge, Lua DFA, tracker alignment; XDP operators -> xdp-bpf.mdc for BPF C
globs:
  - deploy/nginx/**
  - deploy/edge/**
  - internal/edge/**
  - cmd/edge-xdp/**
  - cmd/edge-bpf-sync/**
alwaysApply: false
---

# Edge - Nginx Lua and XDP

## Purpose

Edge: OpenResty/nginx ingress + optional XDP L4 filter. BPF C hot path: `xdp-bpf.mdc`. Compliance: `compliance.mdc`. Parser alignment: `parser.mdc`, `hot-path.mdc`.

## Listeners

| Listener | Protocol |
| :--- | :--- |
| :8180 | HTTP/1.1 |
| :443 | H2/H3/H1.1 ALPN |

Dev certs: `deploy/nginx/certs/generate-dev-certs.sh`. Perimeter timeouts: `client_body_timeout` / `client_header_timeout` **5s**.

## TLS server persona (T15)

Edge `:443` must present a **Mozilla Intermediate** TLS stack so passive scanners cannot fingerprint a non-standard protection intermediary from cipher order alone.

| Surface | Policy |
| :--- | :--- |
| Cipher profile | `deploy/nginx/snippets/ssl_server.conf` — Intermediate suite; `ssl_prefer_server_ciphers off` |
| Baseline | `deploy/nginx/baselines/tls_server_persona.manifest` — do not drift without manifest update + audit |
| HTTP/2 | `http2 on` on TLS listener (`nginx.conf`); H2 SETTINGS frame parity with Chrome is research-tier (`P4-H2-FRAME-DYNAMICS`) |
| kTLS | `ssl_conf_command Options KTLS` when kernel supports offload (`scripts/test/edge/ktls_smoke.sh`) |
| Forbidden | Custom `ssl_ciphers` reorder in prod without manifest review; weak ciphers prepended |

Verify:

```bash
bash scripts/test/edge/tls_server_persona_audit.sh --config
bash scripts/test/edge/tls_server_persona_audit.sh --holdout
TLS_PERSONA_LIVE=1 bash scripts/test/edge/tls_server_persona_audit.sh --live
```

CI: `bash scripts/ci/lint/configs.sh` runs config + holdout. Live openssl artifact: `var/ci/tls_persona/openssl_tls12_fingerprint.sha256`.

## L7 pipeline (`access-check.lua`)

```
Per-campaign RL (edge_rl) -> circuit breaker -> generational blacklist -> ASN bypass -> body DFA -> fraud tier -> upstream trackers
```

Log phase (`edge-circuit-log.lua`): upstream 5xx increments `{bucket}:errs` in `circuit_breaker` SHM (pairs with access-phase totals).

## ngx.shared zones (`nginx.conf`)

| Dict | Size | Writer | Invalidation pattern |
| :--- | :--- | :--- | :--- |
| `edge_rl` | 50m | access incr | TTL bucket keys `{campaign}:{tier}:{bucket}` |
| `edge_config` | 4m | worker 0 timer 5 s | Generational `_asn_ver`; ASN stamps last; RL numerics retain on Redis null |
| `blacklist_cache` | 10m | worker 0 + quarantine thread | Generational `_bl_ver`; full sync stamps `b:{ip}` then `_bl_ver`; incremental reuses ver |
| `slot_map` | 2m | worker 0 timer 10 s | Write `s:0..1023`, then `routing_epoch`, then `version` last |
| `node_weights` | 512k | worker 0 timer 10 s | Zero stale `w:*`, write JSON weights, `peer_count` last |
| `tcp_fp_cache` | 4m | worker 0 timer 2 s | Per-key TTL 3600 s; `ngx.null` skipped on HMGET |
| `circuit_breaker` | 10m | sync failures + log phase | Sliding `{bucket}:total` / `:errs`; ratio gate in access |
| `edge_metrics` | 10m | access incr | Monotonic counters only |
| `sentinel_cache` | 5m | Redis connect path | TTL 5 s on `m:{master_name}` |
| `healthcheck` | 1m | upstream healthcheck | resty.upstream.healthcheck |

Forbidden on sync timers: `dict:get_keys` full scan (removed from `edge-config.lua`; use generation counters).

## Config mirror (`edge-config.lua`)

Redis `config:values` HMGET every 5 s into `edge_config`:

| Field group | SHM keys | On Redis null / HDEL |
| :--- | :--- | :--- |
| RL numerics | `limit_per_min`, `window_ms`, `rl_pct_*`, `retry_*_sec` | Retain prior (fail-open) |
| ASN CDN / mobile | `asn_*:{asn}` generation stamps | Bump `_asn_ver` without restamp -> stale |
| Route flags | `edge_expose_click`, `edge_expose_openrtb` | `dict:delete` -> env fallback |

Prometheus gauges (via `edge-metrics.lua`): `ad_event_processor_edge_asn_cdn_entries`, `_asn_mobile_entries`, `ad_event_processor_edge_config_free_bytes`.

## Blacklist L7 (`edge-blacklist-sync.lua`)

Generational model (reference for ASN and slot-map ordering):

| Key | Role |
| :--- | :--- |
| `_bl_ver` | Active generation; access blocks when `b:{ip} == _bl_ver` |
| `_bl_count` | Deduped estimate; full `sync()` sets exact count; incremental adds only new IPs at current ver |
| `_bl_sync_ts` | Stale gate `EDGE_BL_STALE_SEC` default 30 s |
| `b:{ip}` | Generation stamp; stale stamps fail-open pass |

Incremental quarantine: `stamp_ips(..., bump_version=false)`; unblocked IPs are not deleted from SHM.

## Prometheus (`/edge/metrics`)

Content handler: `edge-metrics.lua`. Prefix `ad_event_processor_edge_*`. Blacklist gauge reads `_bl_count` and `_bl_sync_ts` from `blacklist_cache`.

Verify:

```bash
bash scripts/test/edge/lua_tests.sh unit
bash scripts/test/edge/lua_tests.sh compliance
```

## Tracker ingress schema (`TRACKER_INGRESS_SCHEMA`)

Must match tracker config:

| Mode | Edge behavior | Tracker parse |
| :--- | :--- | :--- |
| `openrtb_3` (default) | Read `request.item[0].id` | OpenRTB path |
| native track | Scan `campaign_id` in body | `ParseTrackRequestJSON*` / vtproto |

## POST /track edge-tracker parity (mandatory)

| Rule | Edge (`edge_track_policy.lua`) | Tracker (`http1TrackEdgePolicy`) |
| :--- | :---: | :---: |
| `Content-Length` required | yes | yes |
| Chunked rejected | yes | yes |
| Duplicate/obfuscated `TE` rejected | yes | yes |

Chunked allowed on `POST /openrtb/bid` only.

Verify: `go test ./internal/ingestion/ -run=TestChaos_CrossHop_NginxGnet` - `differential_count=0`.

Implementation pairs: `http1TrackEdgePolicy` <-> `deploy/nginx/lua/edge_track_policy.lua`; `http1IngressCanonical` for differential tests.

## Shard selection (must match Go)

```
slot = crc32(campaign_id) & 1023
shard = slot_table[slot]
```

`edge-slot-map.lua` uses same Castagnoli CRC32C table as `sharding_amd64.s` / Go fallback. Control pushes slot table via outbox -> Redis shard 0 -> edge reload.

## GET /click

- Query-only; strict UUID `campaign_id`.
- Gate: `EDGE_EXPOSE_CLICK` (404 when off on edge).
- Tracker serves redirect on :8181-8184 regardless of edge flags.

## Tarpit

`EDGE_TARPIT_ENABLED=true` on nginx edge only; capped duration; never on billing/settlement paths.

## XDP (license `ebpf_xdp_edge`)

Not on `single_vps` SKU. Hot path must not import `internal/edge`.

### Flow

```
control outbox -> Redis shard 0 -> edge-bpf-sync -> BPF maps -> edge-xdp drop -> Nginx -> tracker
```

Pin dir default: `/sys/fs/bpf/ad-event-processor`.

### Blocklist maps

| Map type | Content |
| :--- | :--- |
| LRU HASH | Host keys (`/32`, `/128`) on deny maps |
| LPM TRIE | CIDR prefixes |
| PERCPU HASH | `syn_ratelimit_v4`, `ratelimit_v4` (per-CPU shards; no LRU lock under spoofed-IP flood) |

Lookup: host HASH before prefix LPM. Allowlist before deny.

Ringbuf backpressure (`bpf_ringbuf_query`): fingerprint events sampled above 60% fill; violations prioritize SYN/global/subnet over PPS sampling.

Scale: LPM `max_entries=786432`. Incremental sync via `blacklist:changelog:{add,remove}` ZSETs on shard 0; full `SMEMBERS` at startup + every 5 min.

### Binaries

| Binary | Role |
| :--- | :--- |
| `edge-xdp` | CAP_BPF + CAP_NET_ADMIN attach; silent drop at NIC |
| `edge-bpf-sync` | Redis -> maps; `SYNC_INTERVAL=5s` default |

Control never writes kernel maps directly. Requires BTF, modern kernel. Not a substitute for L7 parser budgets.

**BPF C contracts** (maps, token bucket, syn-cookie, ICMP, verifier, verification tiers): `xdp-bpf.mdc`. Long-form narrative also in `deploy/edge/xdp/bpf/edge_filter.c` header.

### OS fingerprint

Edge forwards `X-TCP-TTL`, `X-TCP-WINDOW`, `X-TCP-MSS`, `X-TCP-SIG`, and optional `X-TCP-SIG-V2` from `edge-tcp-fp-sync` / Redis staging. **XDP emit of `tcp_opt_trace` is deferred** (distant backlog); ops may seed `tcp_opt_trace` via `internal/edge.Record` or `redis-cli HMSET` until bpf-sync ships. CDN/L4 LB: set `OS_FINGERPRINT_MISMATCH_ENABLED=false`, `TCP_SYN_SIG_ENABLED=false`, and `TCP_SYN_OPT_CORPUS_ENABLED=false` or accept skip metrics.

Redis staging per client IP (`edge:tcp_fp:ip:{ip}` HASH, TTL 1h):

| Field | Source | Edge cache key | Tracker header |
| :--- | :--- | :--- | :--- |
| `tcp_hash` | XDP `hash_tcp_syn_fields` (or manual seed) | `h:{ip}` | `X-TCP-SIG` (8-char hex) |
| `tcp_opt_trace` | XDP option walk (**deferred**) or `edge.Record` / ops seed | `o:{ip}` | `X-TCP-SIG-V2` (comma tokens, max 512 B) |
| `ttl` | SYN IP TTL | `t:{ip}` | `X-TCP-TTL` |
| `window` | SYN window | `w:{ip}` | `X-TCP-WINDOW` |
| `mss` | SYN MSS high byte | `{ip}` | `X-TCP-MSS` |
| `seen_at` | Unix timestamp | not cached on nginx | n/a |

`X-TCP-SIG-V2` wire: lower-case comma-separated SYN option tokens (`nop,nop,mss:1460,sackok`). Tracker hashes via `pkg/tcpsynopt` and matches `tcp_syn_opt_corpus` when `TCP_SYN_OPT_CORPUS_ENABLED=true` (default off). Invalid trace on nginx: header omitted (fail-open).

Connection timing (cold `rtt_split_tunnel`; no hot signal):

| Field | Source | Tracker header | CH column |
| :--- | :--- | :--- | :--- |
| SYN RTT | nginx `$tcpinfo_rtt` (µs → ms) | `X-RTT-SYN-MS` | `rtt_syn_ms` |
| TTFB app | nginx `$connection_time` (s → ms) | `X-TTFB-APP-MS` | `ttfb_app_ms` |
| split delta | `ttfb_app_ms - rtt_syn_ms` on tracker | n/a | `rtt_split_delta_ms` |

Recent index: `edge:tcp_fp:recent` ZSET; member `{ip}:{tcp_hash_hex}`.

### Rollback

Stop bpf-sync -> stop edge-xdp; Nginx Lua blacklist remains.

## Verification

```bash
bash scripts/test/edge/lua_tests.sh unit
bash scripts/test/edge/tls_server_persona_audit.sh --config
bash scripts/ci/compliance.sh
go test ./internal/edge/... -count=1
go test ./internal/ingestion/ -run=TestChaos_CrossHop_NginxGnet -count=1
```

XDP/BPF C verification: `xdp-bpf.mdc` **Verification tiers**.

## Related rules

`compliance.mdc`, `data-layer.mdc`, `hot-path.mdc`, `licensing.mdc`, `parser.mdc`, `traffic.mdc`, `xdp-bpf.mdc`.
