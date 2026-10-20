---
description: Rejected alternatives, hot-path strategy, verification evidence matrix
globs:
  - internal/ingest/**
  - internal/filter/**
  - internal/domain/**
  - pkg/broker/**
  - internal/rtb/**
alwaysApply: false
---

# Architecture Tradeoffs

## Purpose

When choosing architecture, prefer evidence in tree over new patterns. Invariants: `architecture.mdc`. SLAs: `core.mdc`.

Documents rejected production alternatives and the verification matrix for hot-path decisions already implemented in this repo.

## Rejected for production hot path

| Alternative | Why not (project-specific) |
| :--- | :--- |
| Jump Consistent Hash | Large remap on scale; `JumpHashSharder` = tests/benches only |
| Redis Cluster | `MOVED` breaks multi-key Lua on `{campaign_id}` hash tags; operator-led static slots instead |
| Kafka/NATS on `/track` | No atomic budget+accept in one appliance; footprint |
| Lua `XADD` in same script as debit | Holds Redis thread; split to Go `StreamProducer` + `budget-rollback.lua` |
| LISTEN/NOTIFY for outbox | Polling 20 ms chosen for reliability under load (`OutboxWorker`) |
| Dragonfly/Aerospike v1 | Redis masters + Sentinel sufficient for appliance SKU |

## Local quanta and broker

Goals: cut Redis stream RAM, crash-safe replay, controlled cutover with PEL drain.

Scope: append-only segments + gnet server - not general message bus. Budget/settlement may stay on Redis Streams until broker `_pg` path proven.

### Local quanta trade-off

Full-skip = zero sync `EVALSHA` for eligible traffic; eventual consistency on crash - `local-quota-refill.lua` / `local-quota-return.lua` reconcile. Coordinate stream keys when `StreamProducer` active (`fcap:ignored`) to prevent dual `XADD`.

### Broker trade-off

`CH_INGEST_SOURCE=broker`: mmap WAL via `pkg/broker`. Shadow mode (`BROKER_SHADOW_MODE=1`) before cutover. Divergence metric `ad_broker_ingest_divergence_high` must be quiet in shadow.

## unsafe.String and offload buffers

Tracker uses a **two-tier thread model** (`hot-path.mdc` **Tracker thread model**). gnet epoll discards the peek frame before filter runs.

| Surface | Lifetime rule |
| :--- | :--- |
| gnet peek frame | Tier A only; discarded after `SubmitOffload` |
| `OffloadHTTPPin` / worker arena | Tier B pinned worker until `releaseOffloadBuffers` |
| `evt` string fields | May alias pin/arena during synchronous `FilterEngine.Check` on Tier B |
| Response write | `cloneAsyncWriteBytes` before arena release; `string(req.Accept)` / `string(req.Origin)` for CORS |

**Rejected:** spawning `go func()` around `FilterEngine.Check` (breaks lifetime and zero-alloc contract). Cross-hop parity: `TestChaos_CrossHop_NginxGnet`.

## Verification matrix

Cite these tests when claiming behavior:

| Behavior | Test / gate |
| :--- | :--- |
| Admission race without reserve | `TestStreamProducerAdmissionRaceWithoutReserve` |
| Reserve prevents queue full | `TestStreamProducerReservePreventsQueueFull` |
| Dual stream write fix | `TestUnifiedFilter_SetDeferStreamToProducer_DualStreamWriteFix` |
| Post-debit rollback | `TestUnifiedFilter_RollbackDebit_LocalQuanta` |
| Deferred ingest no publisher | `TestTryAcquireStreamAdmission_holdoutDeferredNoPublisher`, `TestPublishAcceptedTrack_holdoutDeferredNoPublisher` |
| Static slot parity | `sharding_test.go`, `edge-slot-map.lua` |
| Budget invariant | `AssertBudgetInvariant` |
| UDS dial | `redis_uds_benchmark.sh` |

## Operator signals

| Metric | Interpretation |
| :--- | :--- |
| `ad_stream_producer_post_debit_rejected_total` | Should stay ~0; spike -> tune admission or capacity |
| `ad_broker_ingest_divergence_high` | Quiet in broker shadow; active in cutover = rollback |
| `ad_management_outbox_oldest_pending_seconds` | > 30 s = outbox backlog alert |

## Related rules

`architecture.mdc`, `data-layer.mdc`, `development.mdc`, `hot-path.mdc`, `parser.mdc`.
