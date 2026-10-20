---
description: Fault injection, parser chaos proofs, outbox idempotency, resilience
globs:
  - **/*_fault_test.go
  - **/fault_*.go
  - scripts/fault/**
  - scripts/test/**
alwaysApply: false
---

# Fault Tests and Resilience

## Purpose

Apply when adding failure modes, outbox handlers, parser security, stream admission, or resilience tests.

Reference: `development.mdc`, `parser.mdc`, `anti-slop.mdc`, `testing.mdc`.

## Fault test placement

| Location | Content |
| :--- | :--- |
| `*_fault_test.go` | Beside code under test |
| `fault_*` packages | Shared corpora/harnesses |
| `TestChaos_*` | Parser/wire security in `internal/ingestion/` |
| `scripts/fault/` | Resilience scripts (`run.sh`, `compose_fault_drill.sh`) |

## Outbox and payment idempotency

Prove under:

| Scenario | Expected behavior |
| :--- | :--- |
| Duplicate webhook delivery | Same event ID twice - no double-apply |
| Handler error mid-apply | Row stays pending, retries |
| PG txn failure after enqueue | No partial Redis side effect visible |
| Outbox replay of same row | Idempotency key / version check prevents double-apply |

Permanent failure path: mark failed + ops alert; not infinite retry loop.

## Hot-path write paths

Every new accept/spend/log path needs:

1. Fault test or chaos proof, OR
2. Explicit PR waiver citing risk and monitoring.

| Behavior | Test |
| :--- | :--- |
| Stream admission race | `TestStreamProducerAdmissionRaceWithoutReserve` |
| Reserve prevents full queue | `TestStreamProducerReservePreventsQueueFull` |
| Admission at 100% queue | `TestStreamProducerAdmissionReject` |
| Dual stream write fix | `TestUnifiedFilter_SetDeferStreamToProducer_DualStreamWriteFix` |
| Local quanta rollback | `TestUnifiedFilter_RollbackDebit_LocalQuanta` |
| Budget invariant | `AssertBudgetInvariant` in settlement tests |

## Parser security proofs

Required when touching HTTP/1 FSM, JSON budgets, protobuf wire, ORTB ingress, HPACK, TE.TE:

```bash
go test ./internal/ingestion/ -run=TestChaos_ParserSecurity -count=1 -v
go test ./internal/ingestion/ -run=TestChaos_CrossHop_NginxGnet -count=1
go test ./internal/ingestion/ -run='TestChaos_TE_TE|TestChaos_Proto_FieldBudget|TestChaos_HPACK' -count=1
bash scripts/fault/parser_chaos_drill.sh
```

Pass criteria:

- `differential_count=0` (edge vs gnet same verdict).
- Control cohort p99 < 80 ms under sustained chaos (`parser_chaos_load.sh`).
- `WorkerPoolRejectTotal` delta 0 during chaos load.
- Chaos tests log `fault_proof proof=closed` when fixed.

Slow-body DoS:

```bash
go test ./internal/ingestion/ -run=TestChaos_ParserSecurity_http1_incomplete_body -count=1 -v
bash scripts/fault/parser_slow_body_drill.sh
```

## Shard and Redis faults

- Shard 0 outage matrix: `data-layer.mdc`; gate `bash scripts/ci/static/state_shard_nil.sh`.
- `TestFault_NOSCRIPTStorm`, `TestFault_CHSpoolDiskBlock` in ingestion.
- Redis latency -> circuit breaker open -> 503 fail closed.
- `scripts/test/sentinel.sh`, `compose_fault_drill.sh` for compose-level drills.

## Load-test abort rules

Abort when (`core.mdc`):

- Control-cohort handler p99 > 80 ms for 30 s.
- Budget invariant violation (`current_spend > budget_limit`).
- `malformed.sh` / `parser_chaos_load.sh` enforce these.

## Alerts (examples)

| Alert | Threshold |
| :--- | :--- |
| `ad_management_outbox_oldest_pending_seconds` | > 30 s |
| Processor stream lag / PEL growth | Sustained increase |
| `ad_stream_producer_post_debit_rejected_total` | Sustained > 0 |
| Redis circuit open per shard | Sustained |
| `ad_broker_ingest_divergence_high` | Active during broker shadow |

## Resilience run wrapper

```bash
bash scripts/fault/run.sh
bash scripts/fault/resilience_fault_gates.sh /tmp/resilience-fault.log
```

Success logs `fault_proof fault=<name>`.

HTMX/UI faults: out of scope - JSON API only.

## Related rules

`control-plane.mdc`, `data-layer.mdc`, `hot-path.mdc`, `load-test-bpf.mdc`, `parser.mdc`.
