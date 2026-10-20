---
description: Tracker ingest zero-alloc, parsers, gnet, FilterEngine, SoA, asm, chaos proofs
globs:
  - internal/ingest/**
  - internal/filter/**
  - internal/stream/**
  - internal/campaignmodel/**
  - internal/domain/sharding*
  - cmd/tracker/**
  - pkg/broker/**
  - deploy/nginx/lua/**
alwaysApply: false
---

# Hot Path - Tracker Ingest

## Purpose

Apply when changing `/track`, `/click`, `/tg/click`, `/openrtb/bid`, filters, parse, gnet, stream producer, local quanta, or edge-tracker alignment.

Reference: `parser.mdc`, `tradeoffs.mdc`, `architecture.mdc`. Anti-slop: `anti-slop.mdc`.

**Out of scope:** `deploy/edge/xdp/bpf/edge_filter.c` and `cmd/edge-xdp` are NIC L4 XDP programs, not tracker ingest. Full BPF C rules: `xdp-bpf.mdc`. Operator/sync context: `edge.mdc`. Tracker must not import `internal/edge` (`architecture.mdc`).

## SLA

Non-negotiable budgets: `core.mdc`. Financial rule: **fail closed** (503) - never accept spend without debit + stream reservation aligned.

## Forbidden on request path (CI-enforced)

Scripts: `hot_path_static_gate.sh`, `lint_go_hotpath_forbid_gate.sh`, `escape_heap_gate.sh`.

| Category | Forbidden |
| :--- | :--- |
| Runtime | `defer` inside hot loops (OK at function entry for rare cleanup only if proven 0-alloc) |
| Closures | Closures that escape or capture per-request variables in filter/parse loops |
| Boxing / format | `interface{}` boxing, `sync.Map`, `fmt.Sprintf`, string `+` concat |
| Context | `context.WithValue`, `context.WithTimeout`, `context.WithCancel` on request path |
| Metrics | Dynamic Prometheus label values computed per event in inner loops |
| Errors | `fmt.Errorf` on `/track` - use typed rejects (`filterRejectKind`, `NoBidReason`) |
| JSON | `json.Marshal` / `encoding/json` on production `/track` or OpenRTB bid response path |
| Transport | `net/http` server for tracker ingest (gnet only) |
| ML | Import `internal/fraud` ML inference - hot path reads `ml:score:boost:*` snapshot only |
| Cold I/O | Synchronous Postgres, ClickHouse, outbox, or external RPC from `processTrack()` or synchronous filter path |

See `architecture.mdc` for full hot/cold boundary.

## Allowed patterns

| Pattern | Project usage |
| :--- | :--- |
| `sync.Pool` | `Event`, buffers, eval wire, OpenRTB scratch (`handler.go` pools) |
| `unsafe.String` / `unsafe.Slice` | Only over `OffloadHTTPPin`/arena while pinned worker handler runs; copy `Accept`/`Origin` via `string()`; response via `cloneAsyncWriteBytes` before `releaseOffloadBuffers` |
| Prometheus | Pre-bound counters/histograms with fixed label sets |
| Stack buffers | `[N]byte` + `append` with known cap; `strconv.AppendInt` into reused buf |
| Monotonic time | `//go:linkname monotonicNano runtime.nanotime` - no `time.Now` in filter deadline loops |

## Data-oriented design (DoD)

Hot path favors **flat data, columnar layout, snapshot readers** over pointer graphs and interface dispatch.

### Structure of Arrays (SoA) - RTB catalog

`internal/rtb/catalog_shard.go`: `CampaignAuctionRegistry` stores parallel slices (`CampaignIDs`, `Bids`, `CTRPPM`, `GeoHashes`, `Weights`, ...). Bucket indices (`GeoBucketStart`, `TargetBucketStart`) point into `candidateBucketSoA` for cache-friendly scans.

| Rule | Detail |
| :--- | :--- |
| Cold rebuild | Builds new `catalogSnapshot`; publish via `atomic.Pointer[catalogSnapshot].Store` |
| Hot readers | Single `loadCatalog()` atomic load per auction - no locks |
| Bucket order | Presorted buckets by score; early break on score floor |
| Geo shard | `req.GeoHash & 63` - 64-way partition |
| Budget CAS | In `CheckAndSpendAll` when `RTB_BUDGET_AUTHORITY=rtb` |
| Bench target | 0 allocs/op in `RunAuction` bench; scan cap p99 < 500 candidates |

### Domain hot models

- `internal/campaignmodel` / hot `internal/domain`: **no struct tags** (no json/db/protobuf on hot structs).
- Registry: `atomic.Pointer` snapshot swap on catalog rebuild; load once per request loop.
- Pad contended atomics: `cpu.CacheLinePad` around MPSC queue heads, breaker counters.
- **Naming:** Follow `naming.mdc`. Avoid single-letter names or cryptic numbers in filter/auction loops.

### Sharding - StaticSlot + asm

Production: `StaticSlotSharder` only. `JumpHashSharder` = tests/benches only.

```
slot = CRC32C(campaign_id) & 1023
shard = slot_table[slot] // atomic.Value, zero-lock read
```

`internal/domain/sharding_amd64.s`: SSE4.2 `CRC32Q` on two `uint64` limbs of UUID - `NOSPLIT`, ~5.6 ns, 0 allocs. Non-amd64: `hash/crc32` Castagnoli table. Edge Lua must match (`edge-slot-map.lua`); parity tests in `sharding_test.go`.

Keys: `{campaign_id}` hash tag so multi-key Lua stays on one master. Never Redis Cluster `MOVED` on hot path.

## Parser and ingress security

Wire policy, budgets, edge parity, chaos commands: `parser.mdc`. Merge blocked without `TestChaos_CrossHop_NginxGnet` `differential_count=0`.

## Tracker thread model (canonical)

Two tiers. **Do not** document `FilterEngine.Check` as a detached goroutine. Canonical source: `cmd/tracker/doc.go`, `cmd/tracker/wire.go`, `internal/ingest/gnet/server.go`, `internal/ingest/trackwire.go`.

| Tier | Runtime | `LockOSThread` | Sync Redis `EVALSHA` | Returns when |
| :--- | :--- | :--- | :--- | :--- |
| **A — gnet epoll** | `gnet.OnTraffic` event loop (`WithLockOSThread(false)`) | No | **Forbidden** | After `SubmitOffloadToWorker` + `Discard` frame |
| **B — PinnedWorkerPool** | `Worker.start` goroutine per `MAX_WORKERS` | Yes | **Allowed** (sync on worker) | After full `runOffloadedRequest` path |

**Tier A (epoll) — allowed:** peek/parse HTTP, `PinParsedHTTPRequest`, copy bytes to worker arena, enqueue `ConnContext`, metrics.

**Tier A — forbidden:** `FilterEngine.Check`, `processTrack`, synchronous Redis, Postgres, ClickHouse.

**Tier B (pinned worker) — synchronous pipeline on one thread:**

```
runOffloadedRequest -> React -> parseTrackIngest
  -> tryAcquireStreamAdmission (TryReserve)
  -> processTrack -> FilterEngine.Check (incl. EVALSHA when not local-quanta full-skip)
  -> publishAcceptedTrack
  -> writeGnetTrackAccepted -> cloneAsyncWriteBytes -> AsyncWrite
```

- **No** `go func()` around `FilterEngine.Check` on `/track`. `FILTER_TIMEOUT_MS` is a monotonic deadline inside the same worker (`filterDeadlineExceededEvt`).
- Queue depth **8192 per worker** (not one global queue). Route by conn `WorkerID` (`SubmitOffloadToWorker`).
- `HTTP1OffloadBusy`: one in-flight offload per HTTP/1 connection.
- Queue full -> `WorkerPoolRejectTotal`, 503 overload (`TestFault_PinnedWorkerPoolSaturationSpike`).

**Buffer lifetime:**

| Buffer | Lifetime |
| :--- | :--- |
| gnet peek frame | Until `Discard` on epoll thread only |
| `OffloadHTTPPin` | Pinned worker handler (`PinParsedHTTPRequest` copies header/body slices) |
| Worker arena | Until `releaseOffloadBuffers` after response serialized |
| `evt` string fields | May reference pin/arena until Tier B handler returns |
| HTTP response bytes | `cloneAsyncWriteBytes` before arena release; `AsyncWrite` callback frees lease |

**Stale documentation (merge blocker if reintroduced):**

| Lie | Truth |
| :--- | :--- |
| `FilterEngine.Check` in detached goroutine | Sync on Tier B pinned worker |
| Pinned workers return to epoll immediately | **Epoll** returns after enqueue; **workers** block until path completes |
| Blocking Redis forbidden on pinned workers | Forbidden on **Tier A epoll** only; sync EVALSHA on Tier B is by design |
| `unsafe.String` lifetime <= gnet read frame | Lifetime <= pin/arena on Tier B worker; frame discarded before filter runs |

## gnet HTTP FSM

| Rule | Detail |
| :--- | :--- |
| HTTP/1.1 | DFA on ring buffer - no `net/http` per request |
| Offload | Tier A enqueues to `PinnedWorkerPool`; Tier B runs `React` |
| Queues | Per-worker MPSC, cache-line padded heads; default depth 8192 per worker |
| Sync filter | `TryReserve` then synchronous `FilterEngine.Check` on Tier B (incl. `EVALSHA` unless local-quanta full-skip) |
| Async write | `cloneAsyncWriteBytes` then `releaseOffloadBuffers`; `AsyncWrite` from gnet callback |
| Microbench ref | HTTP DFA ~539 ns; protobuf ~200 ns; spikes usually Redis/script contention not parse |

## Filter chain order

Architectural invariant: local filters before any Redis RTT (`architecture.mdc`). Execute cheapest first:

```
License -> Emergency Breaker -> Geo -> Schedule -> Segment -> Fraud boost snapshot -> Consent -> UnifiedFilter (Redis Lua)
```

| Rule | Detail |
| :--- | :--- |
| Deadline | `FilterDeadlineMono = monotonicNano() + timeout` at entry - **no wall clock** in filter loops |
| UnifiedFilter | Last: only requests that passed all local gates incur Redis RTT |
| Redis breaker open | 503 `filterRejectInfra` (fail closed) |
| Producer overload | 503 `filterRejectProducerOverload` **before** debit |

## Stream producer, admission, rollback

Layered strategy (`tradeoffs.mdc`):

1. `tryAcquireStreamAdmission` / `TryReserve` at `STREAM_PRODUCER_ADMISSION_PCT` (default 85%) **before** Lua debit.
2. `SetDeferStreamToProducer(true)` -> Lua stream key `fcap:ignored`; single Go writer (`StreamProducer` / `BrokerProducer`).
3. Post-debit enqueue fail -> `budget-rollback.lua` + local quanta ledger refund (200 ms rollback timeout).
4. Deferred mode (`fcap:ignored`) without `StreamProducer`/`BrokerProducer` -> 503 `filterRejectInfra` before debit; `publishAcceptedTrack` returns false if miswired after debit.
5. Local quanta full-skip (`LOCAL_QUOTA_MODE=live`): zero sync `EVALSHA` when eligible; coordinate stream keys to prevent dual `XADD`.

Monitor: `ad_stream_producer_post_debit_rejected_total` should stay ~0; spike = tune admission or capacity.

## Local quanta

- Refill via `local-quota-refill.lua`; debit in Go `TrySpendDebit` (~16 ns).
- Full-skip: local dedup + async publish; eventual consistency on crash - reconciled via refill/return scripts.
- With `StreamProducer`: defer local-quanta stream lane to `fcap:ignored` - one writer.

## BCE, pools, escape analysis

- Length check before indexed loop; `_ = buf[len(buf)-1]` BCE hint when compiler cannot prove bounds.
- Return objects to `sync.Pool` on **all** exit paths (parse reject included).
- After hot-path edits: `make test-alloc-gate`; `go test -run='^$' -bench=. -benchmem ./internal/ingestion/...`.
- `go build -gcflags=-m` on hot packages - no new escapes above `scripts/ci/baselines/escape_hot_path_heap_lines.count`.
- objdump spot-check: no `panicIndex`, `newobject`, `json.*` in inner parse/filter loops.

## GC and runtime tuning (tracker)

- `GOGC=300`, `GOMEMLIMIT` ~700MiB on tracker; processor `GOGC=100`.
- Pre-allocate pools and mmap buffers (GeoIP); avoid per-request heap growth.

## Transport optimizations

- Redis UDS when co-located: `REDIS_ADDRS` unix socket path; dial p50 gate `scripts/perf/redis_uds_benchmark.sh`.
- CPU isolation: `CPU_ISOLATION_ENABLED=1`; verify `scripts/ops/cpu_isolation.sh verify`.

## Verification

| Step | Command |
| :--- | :--- |
| Alloc gate | `make test-alloc-gate` |
| Hot static | `bash scripts/ci/static/hot_path_static.sh` |
| Escape heap | `bash scripts/ci/static/escape_heap.sh` |
| Stream admission | `go test ./internal/ingestion/ -run='TestStreamProducer\|TestUnifiedFilter_SetDefer\|TestUnifiedFilter_Rollback' -v` |
| Perf claim | `AD_EVENT_PROCESSOR_BPF_PROBE=1 bash scripts/test/load/malformed.sh business` (`load-test-bpf.mdc`) |

PR: no new `interface{}` on `/track`; new write paths need fault proof (`fault-tests.mdc`).

## Test and bench honesty

Agents must not claim production hot-path behavior from unit mocks alone. Full lie catalog: `anti-slop.mdc` **Hot path dishonesty**.

| Claim | Requires |
| :--- | :--- |
| Filter/debit/stream | Redis testcontainers or fault test; not `mockRedisClient` only |
| Broker-primary | `TestFault_BrokerShadowCutover_*` + divergence metrics |
| `/track` p99 | Load test / Prometheus; not `BenchmarkUnifiedFilter_Check_mock` |
| Admission/rollback | Named holdout tests in `anti-slop.mdc` table |
| CI green | State tier: `test-fast` vs `test-integration` vs `test-fault` vs `test-alloc-gate` |

## XDP NIC path (not tracker ingest)

Separate layer: `xdp-bpf.mdc` (map contracts, token bucket math, verifier bounds, verification tiers). Do not apply tracker alloc/escape gates to `edge_filter.c`.

Claiming tracker p99 or Redis filter behavior from XDP tests is a boundary violation (`boundaries.mdc`).

## Related rules

`anti-slop.mdc`, `architecture.mdc`, `core.mdc`, `data-layer.mdc`, `edge.mdc`, `load-test-bpf.mdc`, `parser.mdc`, `rtb.mdc`, `xdp-bpf.mdc`.
