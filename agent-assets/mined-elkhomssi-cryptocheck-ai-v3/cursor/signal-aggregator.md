---
description: Multi-Source Ingestion — Telegram + TxODDS → unified pipeline → Master Feed
globs:
  - services/ingestion/**
  - services/pipeline/**
  - services/realtime/**
  - lib/signal-aggregator/**
  - packages/signal-contracts/**
  - app/dashboard/signals/**
  - app/api/signals/**
---

# Multi-Source Ingestion Engine

## Architecture (Prompt 0+)
- **Adapters** implement `SourceAdapter` (`packages/signal-contracts/src/unified-ingestion.ts`) — ONLY place for source-specific connect/parse.
- **Unified queue:** `ccai:sig:stream:unified` + consumer group `ccai:sig:cg:gate`.
- **Burst isolation:** per-source streams `ccai:sig:stream:source:{telegram|txodds}` fan in before unified.
- **Envelope:** `UnifiedSignal` with `id = {sourceTag}:{sourceRef}`, `subjectType` discriminator.

## Gate dispatch (Prompt 3 — do not implement in Prompt 0)
| subjectType | Path |
|-------------|------|
| `token` | `lib/connect/scan-gateway.ts` → Sentinel (frozen core untouched) |
| `match_event` | `SportsSignalEvaluator` (new module — never imports scanner core) |

## Execution (frozen)
- Jupiter risk-gated swap: **unchanged**, **token-only**. `match_event` → feed render only, no swap.

## Reuse (mandatory)
- Scans: `scan-gateway.ts` only for tokens
- Swaps: `risk-gated-swap.ts` + `jupiter-client.ts`
- Fees: `FeeRecord` from revenue dashboard

## Package boundaries
- `packages/signal-contracts` and `services/*` — zero `@/` and zero `next` imports

## TxODDS
- Hackathon-authorized access only; env credentials; API terms; `rawPayload` retained for audit

## Telegram
- Public allowlisted channels; attribution; FloodWait backoff

## Integrity
- No fabricated data; `sample: true` on seed rows; SETNX dedup on `ccai:sig:dedup:id:{id}`

## Latency
- Adapter XADD non-blocking; async-upgrade verdict; WebSocket push
