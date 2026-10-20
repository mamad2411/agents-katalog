# CryptoCheck AI — Cursor rules

## MASTER LOOP (standing protocol for iterative work)
- Always-applied agent rule: `.cursor/rules/master-loop.mdc`
- Canonical human doc: `docs/MASTER_LOOP.md`
- Invoke with: MISSION / SCOPE / OUT OF SCOPE / N → Run the Master Loop.
- After each mission: run **Step 7 System Evolution** (proposals only) — subordinate to Step 2; capital-path advise-only is intentionally capped, not a defect.
- Product north star: replace the trader's daily work — autonomous financial OS, not another crypto platform. Features that still require manual search/compare/analyze/monitor are unfinished.
- Safety carve-out, One-Decision boundary, objective checks, and human checkpoint (never self-certified) apply to every loop automatically.

## FROZEN FILES — never edit these, ever
- lib/services/scanner-engine.ts
- lib/services/scanner/pipeline/run-institutional-scan.ts
- lib/sentinel/canonical-scan.ts
- programs/web4-launchpad/**  (on-chain — irreversible)

## PACKAGE BOUNDARIES — hard rules
- packages/* must have zero imports matching `from '@/'`
- packages/* must have zero imports matching `from 'next'`
- packages/signing — zero Solana or Supabase deps
- packages/ccai-connect — zero @/ imports, zero Next.js, zero Solana

## INJECTION POINTS (only safe places to add new logic to the scan path)
- I1: app/api/v1/scan/route.ts BEFORE normalizeScanBody  → add: auth, chain routing, audit
- I3: lib/services/scanner/execute-scan.ts AFTER Promise.all([enrich, dex]) → add: EVM metrics override
- I7: app/api/v1/scan/route.ts AFTER runInstitutionalScan BEFORE canonicalScan → add: fast-path return
- I9: execute-scan.ts dispatchInstitutionalWebhooks caller → add: flywheel events
- I12: app/api/neural-v4/route.ts → add: gateway delegation (deprecation path)

## ARCHITECTURE RULES
- The Data Flywheel (Redis, Supabase crons, webhooks) feeds the Neural Settlement Layer
- The Neural Settlement Layer (scanner, sentinel, swap-sim) is never imported by Terminal UI directly
- Terminal Ecosystem (dashboards, extension, copilot) must use CCAI Connect SDK or API routes only
- No direct canonicalScan import in any UI server component

## NAMING
- New Redis keys: prefix ccai:b2b: or ccai:rep: (not scan:v2: — that namespace is frozen)
- New Supabase tables: snake_case, prefix with domain (token_*, wallet_*, partner_*, signal_*)
- New API routes: /api/b2b/v1/* for B2B, /api/v1/* for consumer, /api/internal/* for server-only

## LATENCY RULES
- canonicalScan must never block a consumer API response — async only after Phase 3 lands
- Any new awaited call in the hot scan path needs a comment: // ~Xms estimated
- Target: P50 cached < 40ms, P50 uncached fast-mode < 150ms, P50 institutional < 500ms

## BEFORE ADDING A NEW NPM PACKAGE
- Check if the functionality exists in: lib/services/scanner/*, lib/cache/*, @cryptocheck/signing
- Never add a new HTTP client library — use native fetch
- Never add a new Redis client — reuse the existing ioredis instance from lib/cache/

## TEST REQUIREMENTS
- Every new API route needs a test in __tests__/api/<route-name>.test.ts
- Every new ChainDataPort implementation needs fixture-based enrichment tests
- Equivalence tests required when replacing existing scoring paths (see Phase 8)

## REVENUE DASHBOARD (`/dashboard/revenue/*`) — scan → safe swap
- New surface lives under `app/dashboard/revenue/*` + `lib/revenue-dashboard/*`. Do NOT fold into intelligence-terminal or `app/dashboard.tsx`.
- NEVER edit the frozen scanner core (`scanner-engine.ts`, `run-institutional-scan.ts`, `canonical-scan.ts`) or any MDC-frozen file. Consume scans ONLY via `lib/connect/scan-gateway.ts` (`assessRiskByMint`, `scanViaGateway`, API routes).
- NEVER rebuild swapping. All swaps go through `lib/trading/risk-gated-swap.ts` + `lib/trading/jupiter-client.ts` + existing `/api/trading/*` routes. Extend fee/UX layers only.
- MONEY SAFETY (every swap surface): non-custodial — user wallet signs; we never hold funds or keys. Simulate before send. Always show slippage limit + price-impact warning. Platform fee (`platformFeeBps`) as explicit line item before confirm. DANGER verdict → swap disabled behind friction-heavy typed confirmation (never auto-proceed). CAUTION → prominent amber warning. SAFE → normal flow.
- DATA INTEGRITY: no fabricated revenue, volume, or user counts. Render only real on-chain / fee-account / API data. Placeholders MUST carry visible `sample` tag (`rd-sample-tag`).
- COMPLIANCE: persistent "Not financial advice · DYOR" on trading surfaces + Terms / fee disclosure link slots (`COMPLIANCE_DISCLAIMER`, `FEE_DISCLOSURE_PATH`, `TERMS_PATH` in `lib/revenue-dashboard/constants.ts`).
- Shared contracts: `lib/revenue-dashboard/types.ts` (`ScanResult`, `SwapQuote`, `SwapResult`, `FeeRecord`, `PortfolioPosition`, `RevenueAlert`).
- New fee ledger Redis keys: prefix `ccai:rev:fee:` · Supabase tables: `revenue_fee_*` or `token_fee_*`
- New API routes for revenue dashboard: `/api/revenue/*` (server-only fee recording, admin aggregates)

## SIGNAL AGGREGATOR (Multi-Source → Master Feed → safe swap)
- Services: `services/ingestion` (legacy GramJS → raw stream; migrating to `SourceAdapter`), `services/pipeline` (parse + enrich / unified gate), `services/realtime` (WS gateway + history API). UI at `/dashboard/signals/*` + `lib/signal-aggregator/*`.
- Shared contracts: `@cryptocheck/signal-contracts` — legacy `NormalizedSignal` + **multi-source** `UnifiedSignal`, `SourceAdapter`, `SIGNAL_STREAM_UNIFIED` (see `unified-ingestion.ts`).
- **MULTI-SOURCE INGESTION (Prompt 0+):** Telegram + TxODDS (+ future) share one unified Redis Stream (`ccai:sig:stream:unified`) and consumer group (`ccai:sig:cg:gate`). Per-source ingress streams (`ccai:sig:stream:source:{tag}`) for burst isolation. Namespaced ids `{sourceTag}:{sourceRef}`; DB `UNIQUE (source_tag, source_ref)`; ingest SETNX `ccai:sig:dedup:id:{id}`.
- **SOURCE BOUNDARIES:** Source-specific connection/parsing ONLY in `SourceAdapter` implementations. Gate is source-aware internally (`token` → scan gateway; `match_event` → `SportsSignalEvaluator`), agnostic externally. Downstream feed + execution never branch on source except UI badges/filters.
- NEVER edit frozen scanner core (`scanner-engine.ts`, `run-institutional-scan.ts`, `canonical-scan.ts`). Token scans ONLY via `lib/connect/scan-gateway.ts` (`assessRiskByMint`).
- NEVER rebuild swapping. Jupiter risk-gated swap engine is **source-agnostic** and **byte-for-byte unchanged** — invoked only for actionable `token` signals. `match_event` signals NEVER enter the swap path.
- TXODDS: authorized hackathon access only; credentials from env; respect API terms; reconnect/backoff; raw packet in `rawPayload` for audit trail.
- TELEGRAM HYGIENE: PUBLIC allowlisted channels only. Always attribute `sourceTag` / `sources[]`. FloodWait backoff. No private/paid scraping.
- MONEY SAFETY (swap sheet): non-custodial; simulate before send; platform fee line item; DANGER gated — granting feed access never auto-arms Auto-Sniper.
- DATA INTEGRITY: no fabricated signals, odds, or source counts. Sample data MUST carry `sample: true`. Unresolvable token CAs → drop/flag.
- LATENCY: adapter XADD non-blocking; async-upgrade (`verdict: scanning` → upgrade in place); WebSocket push.
- New Redis keys: prefix `ccai:sig:` — unified `ccai:sig:stream:unified`, per-source `ccai:sig:stream:source:*`, dedup `ccai:sig:dedup:id:*`.
- New Supabase: `signal_*` tables + `source_tag` / `subject_type` on `signal_normalized` (see `20260702_multi_source_ingestion_foundation.sql`).
- New API routes: `/api/signals/*`; internal assess `POST /api/internal/signals/assess` (token path only).
- COMPLIANCE: `SIGNAL_COMPLIANCE` — informational signals, not endorsements; sports rows are not swap recommendations.
