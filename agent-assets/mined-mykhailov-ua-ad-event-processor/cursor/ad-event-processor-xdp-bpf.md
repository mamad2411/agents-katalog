---
description: XDP/eBPF C hot path - map contracts, verifier bounds, token bucket math, test tiers
globs:
  - deploy/edge/xdp/**
  - cmd/edge-xdp/**
  - cmd/edge-bpf-sync/**
  - internal/edge/bpf*
  - internal/edge/*_bpf*
  - internal/edge/token_bucket*
alwaysApply: false
---

# XDP / BPF Hot Path

## Purpose

Apply when changing `deploy/edge/xdp/bpf/*.c`, `cmd/edge-xdp`, `cmd/edge-bpf-sync`, or Go loaders/tests in `internal/edge/` that load or assert BPF behavior.

This is the **NIC L4 program layer** (per-packet XDP on ingress). It is **not** tracker `/track` ingest (`hot-path.mdc`). It does not use gnet, `FilterEngine`, or Redis `EVALSHA`.

Reference: `edge.mdc` (operators, Redis sync, L7 fingerprint pipeline), `comments.mdc` (BPF header contracts), `anti-slop.mdc` (doc lie modes), `compliance.mdc` (license `ebpf_xdp_edge`).

**Forbidden import direction:** `internal/ingest` and tracker must not import `internal/edge` for BPF map access (`architecture.mdc`, `boundaries.mdc`).

## Layer budgets

XDP does not use `core.mdc` tracker p95/p99 (`ad_http_request_duration_seconds`). Use layer-local claims only.

| Surface | Target / rule |
| :--- | :--- |
| Per-packet map hot path | PERCPU in-place update on warm keys; no redundant `bpf_map_update_elem` |
| Blocklist lookup | Allow LPM before deny; host LRU before prefix LPM (`edge_filter.c` order) |
| Ringbuf reserve | Query fill % before `bpf_ringbuf_reserve`; sample or skip under pressure |
| Syn-cookie tail call | Rare path; full `bpf_csum_diff` on 20-byte IPv4 header acceptable until profiled |
| Userspace map writer | `edge-bpf-sync` only; XDP **lookup-only** on deny/allow maps |

Do not cite tracker microbenches or `make test-alloc-gate` as proof for `edge_filter.c` changes.

## Program layout

| Artifact | Role |
| :--- | :--- |
| `deploy/edge/xdp/bpf/edge_filter.c` | `xdp_edge_filter`, `xdp_syn_cookie`; maps, limits, ringbufs |
| `cmd/edge-xdp` | Attach to `INGRESS_INTERFACE`; wire `prog_array` tail call |
| `cmd/edge-bpf-sync` | Redis -> pinned maps; never called from XDP |
| `internal/edge/*_bpf*.go` | bpf2go loaders, `prog.Test`, fault tests |

Canonical module narrative: **file header comment** in `edge_filter.c` plus tables below. Edit header when contracts change (`comments.mdc`).

## Forbidden in BPF C (merge blockers)

| Category | Forbidden |
| :--- | :--- |
| Map writes on deny path | `bpf_map_update_elem` / `bpf_map_delete_elem` on blocklist/allow maps from XDP |
| PERCPU warm path | `bpf_map_update_elem` after successful `bpf_map_lookup_elem` on existing PERCPU_HASH/PERCPU_ARRAY slot |
| Unbounded loops | Parser loops over TCP options or packet bytes without fixed `#pragma unroll` or proven `off < bound` |
| First-byte option hacks | Assuming MSS is first TCP option (must TLV-walk NOP/EOL/MSS) |
| Global ICMP drop | `XDP_DROP` all `IPPROTO_ICMP` on ingress NIC (breaks PMTUD Type 3 Code 4 to this host) |
| Silent tail-call miss | `return try_syn_cookie(ctx)` or bare `XDP_DROP` bypassing `stat_inc` / `emit_violation` |
| Helper abuse | Unbounded `bpf_probe_read*`; loops without `data_end` checks on every pointer advance |
| Stack abuse | Large stack arrays; prefer map values or bounded unroll with verifier-friendly limits |
| Legacy tokens | `BidShard`, `espx`, ticket/milestone IDs in comments (`naming.mdc`) |
| Charset slop | Unicode dashes, emojis, `===` banners in comments (`comments.mdc`) |

## Required patterns

### Bounds and verifier

Every L3/L4 pointer advance:

1. Compare against `data_end` before dereference.
2. Derive lengths from header fields (`ihl`, `doff`); reject `doff < 5` before option walk.
3. Cap option walk iterations (current: 10 steps in `read_tcp_mss`).

Use `__always_inline` for per-packet helpers. Prefer `__builtin_memcpy` for fixed small copies.

### Map update matrix

| Map | Type | XDP update rule |
| :--- | :--- | :--- |
| `syn_ratelimit_v4`, `ratelimit_v4`, `rst_ratelimit_v4` | PERCPU_HASH | In-place via lookup pointer; `bpf_map_update_elem` **only** on first insert |
| `global_syn` | PERCPU_ARRAY | In-place only (key 0; no `update_elem`) |
| `syn_subnet_ratelimit_v4` | LRU_HASH | `bpf_map_update_elem` each hit; /24 key; known LRU lock under CGNAT flood |
| `blocklist_*`, `allow_*` | LRU / LPM | Lookup only in XDP |
| `violations`, `fingerprints` | RINGBUF | Reserve with backpressure; submit or silent skip documented in header |

**Not a race:** PERCPU shards are per-CPU; in-place mutation is safe. The anti-pattern is redundant `update_elem` cost, not lost updates.

### Token bucket (`token_bucket_consume_existing`)

Shared by `check_pps_limit` and `check_rst_limit`.

| Step | Formula / rule |
| :--- | :--- |
| Elapsed | `elapsed = now - last_ns`; cap at `NS_PER_SEC` |
| Refill | `added = (elapsed * rate) / NS_PER_SEC` (integer floor) |
| Credit time | If `added > 0`: `last_ns += (added * NS_PER_SEC) / rate`; clamp `last_ns <= now` |
| Consume | `tokens--`; **do not** set `last_ns = now` when `added == 0` |
| Drop | If `tokens == 0` after refill: `XDP_DROP` without updating `last_ns` |
| First insert | `bpf_map_update_elem` with `tokens = burst - 1`, `last_ns = now` |

**Rejected lie:** "`last_ns = now` on every pass causes 100% starvation above rate." Steady admission converges to ~`rate` after burst drain; the bug was **stricter-than-configured** limiting. Falsify with `TestTokenBucket_subintervalCredit_holdout`.

### IPv4 non-TCP (`drop_non_tcp_tracker`)

| Proto | Rule |
| :--- | :--- |
| UDP / SCTP | `XDP_DROP` only when `dest == TRACKER_INGRESS_PORT`; else `XDP_PASS` |
| ICMP | `XDP_PASS` Type 3 Code 4 (PMTUD); other ICMP types `XDP_DROP` |
| IPv6 non-TCP in `xdp_edge_filter` | `XDP_PASS` (no symmetric ICMP handler) |

### SYN-cookie (*intentional* trade-offs)

| Surface | Contract |
| :--- | :--- |
| Trigger | SYN / global / subnet limit breach + `CFG_FLAG_SYN_COOKIE` |
| Under limit | `XDP_PASS` to kernel stack; normal handshake |
| `emit_ipv4_synack` | TCP `doff=5`; `bpf_xdp_adjust_tail` strips ingress options |
| Outbound SYN-ACK | No MSS/WScale/Timestamp options; fixed `SYNACK_TCP_WINDOW` |
| Cookie generation | `gen_syncookie_ipv4` uses full ingress `tcph_len` |
| Tail call | `syn_cookie_tail_call` -> `prog_array[PROG_IDX_SYN_COOKIE]` |
| Tail-call miss | Fall through to `emit_violation` + `stat_inc` + `goto out` |

Holdouts: `TestFault_XDPSynCookieWithTCPOptions`, `TestFault_XDPSynCookieWithPayload` (assert `doff=5`).

**Deferred:** RFC 1624 incremental IPv4 checksum in `emit_ipv4_synack` until profiling shows need.

### LPM `BPF_F_NO_PREALLOC` (*intentional*)

`blocklist_v4/v6`, `allow_v4/v6` save RAM at idle; bulk `edge-bpf-sync` insert may allocate under load. Remove flag only with prod alloc-stall evidence.

### TCP MSS fingerprint (`read_tcp_mss`)

- TLV walk: NOP (1), EOL (0), MSS (2, len >= 4).
- Store **high byte** of MSS in fingerprint event (L7 contract in `edge.mdc`).
- Bounded unroll; must not assume MSS at offset 0.

## Return codes and observability

| Action | When | Stats / side effects |
| :--- | :--- | :--- |
| `XDP_PASS` | Allowlist, under limits, non-tracker UDP, PMTUD ICMP | `stat_inc` where applicable |
| `XDP_DROP` | Blocklist, limits, anomaly flags | `stat_inc` + `emit_violation` when ringbuf policy allows |
| `XDP_TX` | Syn-cookie SYN-ACK from `xdp_syn_cookie` | `XDP_STAT_SYN_COOKIE` |
| Tail-call success | Does not return to parent | Child program owns stats |

New drop reasons require: enum `xdp_stats` entry, Go `bpf_stats.go` mirror, and violation reason if autoban pipeline expects it.

## Verification tiers

Agents must name the tier in PR prose (`anti-slop.mdc`, `boundaries.mdc`).

| Tier | Command | Proves |
| :--- | :--- | :--- |
| **Math** | `go test ./internal/edge/ -short -run TestTokenBucket_ -count=1` | Token bucket refill/consume semantics |
| **Source holdout** | `go test ./internal/edge/ -short -run TestEdgeFilterRateLimitPerCPUHash_holdout -count=1` | PERCPU, `token_bucket_consume_existing`, `TCPOPT_NOP`, ICMP, tail-call symbols in `.c` |
| **BPF compile** | `make gen bpf-dev` or `make bpf-dev` | Clang/llvm BPF object builds; paste exit code |
| **Prog test** | `go test ./internal/edge/ -short -run TestXDP_ -count=1` | Needs CAP_BPF / `kernel.unprivileged_bpf_disabled` |
| **Fault** | `go test ./internal/edge/ -short -run TestFault_XDP -count=1` | Syn-cookie wire shape |
| **Compliance** | `bash scripts/ci/compliance.sh` | License and perimeter scripts |
| **Sealed smoke** | `make sealed-bpf-xdp-smoke` | Attach path on capable host |

**Banned claims without tier:**

| Claim | Requires |
| :--- | :--- |
| "Token bucket correct" | `TestTokenBucket_*` (not `TestXDP_pps` alone) |
| "BPF wired / compiles" | `make bpf-dev` exit code pasted |
| "ICMP/PMTUD safe" | `TestXDP_dropNonTCPOnTrackerPort/icmp_pmtud_pass` |
| "Mitigates residential fraud" | `anti-slop.mdc` doc lie row; listed L4 only |
| "Tracker p99 improved" | `load-test-bpf.mdc` / Prometheus; not XDP unit test |

Default agent verification on shared dev hosts: math + source holdout tiers; do not loop full `go test ./internal/edge/...` without operator ask (`anti-slop.mdc`).

## Holdout tests (required when behavior is non-obvious)

| Behavior | Test | Package |
| :--- | :--- | :--- |
| Token bucket credit vs legacy | `TestTokenBucket_subintervalCredit_holdout` | `internal/edge` |
| Refill period | `TestTokenBucket_refillInterval_matchesRate` | `internal/edge` |
| Above-rate convergence | `TestTokenBucket_sustainedAboveRate_converges` | `internal/edge` |
| `last_ns` invariant | `TestTokenBucket_lastNSInvariant` | `internal/edge` |
| Below-rate no drop | `TestTokenBucket_averageOfferedBelowRate_neverStarves` | `internal/edge` |
| PERCPU / symbol drift | `TestEdgeFilterRateLimitPerCPUHash_holdout` | `internal/edge` |
| Syn-ACK option strip | `TestFault_XDPSynCookieWithTCPOptions` | `internal/edge` |
| Syn-ACK payload strip | `TestFault_XDPSynCookieWithPayload` | `internal/edge` |

Weakening holdouts to green CI without fixing root cause is a boundary violation (`boundaries.mdc`).

## Test dishonesty (XDP-specific)

| Lie | Reality | Falsify |
| :--- | :--- | :--- |
| `prog.Test` without CAP_BPF | Skips or no object load | Paste skip reason; run math tier |
| Math sim = NIC timing proof | Go sim tests algorithm only | Name tier; load test separate |
| Source grep = runtime proof | Static contract only | Tier 3+ for wire behavior |
| "PERCPU race" on in-place write | Per-CPU shard isolation | `edge.mdc` / this file map table |
| Syn-cookie "full TCP" regression | `doff=5` is intentional | Holdout tests must keep asserting |

## Agent checklist (before merge)

| Step | Action |
| :--- | :--- |
| 1 | Edit `edge_filter.c` header trade-offs if contract changed |
| 2 | PERCPU path: in-place vs `update_elem` per map table |
| 3 | Token bucket touch: extend `token_bucket_sim_test.go`; cite holdout in PR |
| 4 | New TCP option parse: bounded unroll + `data_end` checks |
| 5 | New drop: `stat_inc` + violation or document intentional silent drop |
| 6 | Tail call: miss path through `goto out` with stats |
| 7 | Paste verification command + exit code for tier claimed |
| 8 | No tracker hot-path gates cited for BPF-only PR |

## Related rules

`anti-slop.mdc`, `architecture.mdc`, `boundaries.mdc`, `comments.mdc`, `compliance.mdc`, `core.mdc`, `edge.mdc`, `hot-path.mdc`, `load-test-bpf.mdc`, `testing.mdc`.
