---
description: In-process RTB auction, SoA catalog, OpenRTB 2.6, budget CAS
globs:
  - internal/rtb/**
  - internal/openrtb/**
  - internal/ingestion/rtb*.go
  - internal/ingestion/openrtb*.go
alwaysApply: false
---

# RTB and OpenRTB Auction

## Purpose

In-process `RunAuction` on tracker. Targets: p99 < 15 us; candidates scanned p99 < 500; 0 allocs/op.

Reference: `traffic.mdc`, `tradeoffs.mdc`, `hot-path.mdc`, `architecture.mdc`.

## Ingress paths

| Path | Flow |
| :--- | :--- |
| `/track` | `applyRtbAuction` before main filter chain (mode-dependent) |
| `POST /openrtb/bid` | `openrtb_exchange.go` -> DFA parse -> `RunAuction` -> in-place bid response |

OpenRTB does **not** run full `FilterEngine` chain - dedicated exchange path only.

## Packages

| Package | Role |
| :--- | :--- |
| `internal/rtb/` | Auction core, SoA catalog, budget store |
| `internal/openrtb/` | Wire codec (no ingestion import) |
| `internal/ingestion/rtb_*.go`, `openrtb_*.go` | Tracker glue |
| `internal/controlplane/service_rtb.go`, `rtb_handlers.go` | Admin RTB API |

## Structure of Arrays (SoA) catalog

`catalogSnapshot` holds `[64]*CampaignAuctionRegistry` (geo shards). Each registry:

- Parallel slices: `CampaignIDs`, `Bids`, `CTRPPM`, `Reserves`, `DailyBudgets`, `GeoHashes`, `Weights`, `BoostPPM`, `DeviceMasks`, `CategoryMasks`, `DaypartMasks`, ...
- Bucket routing: `GeoBucketHash` + `GeoBucketStart` -> `GeoBucketSoA`; `TargetBucketKey` + `TargetBucketStart` -> `TargetBucketSoA`.
- `candidateBucketSoA`: columnar candidate indices for cache-friendly linear scan.
- `creativeCacheSoA`: creative metadata without per-candidate pointer chase.

Cold path rebuilds full snapshot; hot path:

```go
snap := registry.catalog.Load() // atomic.Pointer[catalogSnapshot]
```

No mutex on read; never mutate snapshot in place.

## Auction algorithm

| Rule | Detail |
| :--- | :--- |
| Geo partition | `req.GeoHash & 63` (64 shards, `geoShardMask`) |
| Bucket order | Presorted by effective score; early break below score floor |
| Winner | bid x CTR (PPM); tie-break weight then raw bid |
| Clearing | First/second price + reserve per campaign config |
| Scan budget | p99 < 500 candidates; reject unbounded catalog walks |

## Budget authority

| Knob | Behavior |
| :--- | :--- |
| `RTB_BUDGET_AUTHORITY=rtb` | `CheckAndSpendAll` CAS in auction loop; skip separate budget debit downstream |
| `BudgetStore` | `atomic.Pointer[budgetSlice]` per spend dimension |
| Shadow mode | `RunAuctionEval` logs winner without spend |

## OpenRTB 2.6 hot path

| Rule | Detail |
| :--- | :--- |
| Parse | DFA - no `encoding/json` on production bid path |
| Units | Micro-units throughout |
| Response | Fixed response header + in-place JSON body (`WriteBidHTTPResponse`) |
| Scan budgets | `ORTB_SCAN_MAX_BYTES`, `ORTB_MAX_QUOTE_CHECKS`; depth `OrtbMaxJSONDepth=32` |
| `json.Marshal` | Tests and cold admin paths only |
| Chunked body | Allowed on `/openrtb/bid` only (not `/track`) |

## Modes

| `RTB_MODE` | Behavior |
| :--- | :--- |
| `off` | Auction disabled |
| `shadow` | `RunAuctionEval` only; no spend or campaign rewrite |
| `live` | Rewrite `campaign_id`, real spend, bid response |

## Shadow to live runbook

1. `GET /api/v1/rtb/integration-profile`
2. `POST /api/v1/rtb/validate-bid-request` with `bid_request_min.json`
3. Soak `RTB_MODE=shadow`; gate `GET /api/v1/rtb/shadow-diff?window=1h` - low mismatch, no PG budget violations
4. Configure deals/floors via admin API
5. `RTB_MODE=live`; `RTB_BUDGET_AUTHORITY=redis`; set exchange QPS/no-bid mode
6. E2E: `go test ./tests/e2e/... -run 'RtbLive|OpenRTB26'`
7. Rollback: `RTB_MODE=shadow|off` before re-enable after incidents

Deferred: OpenRTB 3.0, multi-imp >1, gzip async lurl.

## Verification

```bash
make test-alloc-gate
go test ./internal/rtb/... -short -count=1
go test ./internal/ingestion/ -run=OpenRTB -short -count=1
bash scripts/ci/static/hot_path_static.sh
bash scripts/ci/static/escape_heap.sh
```

## Related rules

`data-layer.mdc`, `edge.mdc`, `hot-path.mdc`, `licensing.mdc`, `traffic.mdc`.
