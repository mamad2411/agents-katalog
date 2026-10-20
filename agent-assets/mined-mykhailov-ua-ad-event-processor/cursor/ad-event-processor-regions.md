---
description: Enterprise multi-region, region-proxy WAL, import boundaries
globs:
  - pkg/regionproxy/**
  - cmd/region-proxy/**
  - internal/controlplane/*region*
  - internal/controlplane/operation_lease*
alwaysApply: false
---

# Multi-Region (Enterprise)

## Purpose

**Not appliance SKU.** Requires Enterprise license (`features.multi_region`), compose profile `multi-region`. Pilot: `multi_region: false` in `deploy/vendor/sku.yaml`.

## Components

| Piece | Path | Role |
| :--- | :--- | :--- |
| `region-proxy` | `cmd/region-proxy`, `pkg/regionproxy/` | Regional WAL ingress, quorum book/ack, uplink |
| Regional processor | `cmd/processor` + `MULTI_REGION_ENABLED=1` | Spend sync -> region-proxy |
| Global control | `cmd/control` | `IngestRegionProxyBatch`, operation leases, global PG |

```bash
docker compose -f deploy/compose/docker-compose.yaml --profile multi-region up -d
```

## Environment (regional cell)

| Variable | Purpose |
| :--- | :--- |
| `MULTI_REGION_ENABLED=1` | Regional processor mode |
| `REGION_CODE` | Cell identifier |
| `REGION_PROXY_ADDR` | region-proxy listen |
| `GLOBAL_SPEND_BATCH_MIN` | Min batch before flush (default 100) |

WAL: append-only (`pkg/regionproxy/wal/`), group commit, `Recover()` discards torn records. Quorum via `pkg/regionproxy/quorum` + operation leases.

## Import boundaries

| Rule | Detail |
| :--- | :--- |
| Hot ingestion | `internal/ingestion` (non-`_test`) must **not** import `pkg/regionproxy` |
| Processor | Wires region-proxy client only when `MULTI_REGION_ENABLED=1` |
| Control plane | `operation_lease.go` uses quorum when Enterprise multi-region enabled |

## Resilience drill

```bash
bash scripts/test/multi_region_resilience_drill.sh
```

Prove:

- p99 < 80 ms baseline
- >= 12 `mr_*` fault proofs
- Quorum partition handling
- `AssertBudgetInvariant` Redis vs PG +/-1 micro-unit

E2E: `tests/e2e/region_proxy_uplink_test.go`, `region_proxy_ingress_test.go`.

## Related rules

`architecture.mdc`, `boundaries.mdc`, `data-layer.mdc`, `fault-tests.mdc`, `licensing.mdc`.
