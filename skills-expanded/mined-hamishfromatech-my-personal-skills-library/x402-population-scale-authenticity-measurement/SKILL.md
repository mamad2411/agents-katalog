---
name: x402-population-scale-authenticity-measurement
description: Applies the first population-scale measurement of x402 adoption and authenticity (Ling, Zhou, Wu & Wang, arXiv:2607.12575, POMACS 2026) as the GOODHART-METRIC-AUDIT pattern — over a 280-day Base window, 136.7M settlements worth $44.1M decompose into 21.2% provably fictitious (self-payment + closed loops), 63.8% operator-internal, and a genuine-economy bound of $187,861 (demonstrably reaches a nameable catalog service) to $20.26M (45.9%, not provably manufactured); the entire settlement count is reproducible for ~$355,583 in facilitator-sponsored gas, making settlement count a measure of the incentive to transact, not adoption. Use when [auditing on-chain or telemetry-based adoption metrics for manufactured traffic, designing attribution methodology for agent-payment claims, evaluating x402/ecosystem dashboards against vendor dashboards, or writing standards for measurable adoption claims]. NOT for [the value-side funnel and agentic-share bound — use x402-agentic-share-measurement — or DevEx metric overload — use devex-metrics-compass-120-metric-navigation].
---

# The Goodhart Audit: When a Settlement Count Measures Incentive, Not Adoption

## Overview
Ling, Zhou, Wu & Wang (arXiv:2607.12575) deliver the first peer-reviewable, population-scale measurement of agentic-payment adoption on x402/Base — and the finding inverts the ecosystem's headline metric: **settlement count is a Goodhart metric.** It measures the incentive to transact, not the adoption it is read as proving.

The method: identify settlements by intersecting the USDC AuthorizationUsed event (EIP-3009) with a two-source facilitator allowlist (Allium + x402scan: 30 facilitators, 129 relayer EOAs); resolve the true payer through the meta-transaction layer (relayer signs the transaction, not the payer); build a directed value-flow graph of settlements, funding, and sweep transfers; classify every settlement by what the chain can *prove*.

## When to Use
- Auditing any adoption metric that is cheap to emit and linked to standing rewards (leaderboards, token narratives, volume-indexed incentives)
- Designing attribution tests for agentic commerce, airdrop farming, engagement telemetry, or marketplace GMV
- Reconciling vendor dashboards that disagree by an order of magnitude (the paper documents exactly that disagreement among x402 trackers)
- NOT for: the TRM-style commerce-screen funnel and permissive/strict agentic-share bound (`x402-agentic-share-measurement` — complementary: that skill bounds agency, this one audits the metric itself)

## Core Process / Workflow

### The measured decomposition (280-day Base window)
- **136,708,672 settlements, $44,121,383.81 gross**; Solana adds 49.5M settlements (coarser unit, single-dominant facilitator) under a separate upper bound — never merged with Base
- **Tier C1 — fictitious (21.20% of count, 54.08% of value):** self-payment wallets (a single 2025-11 three-wallet campaign: 27.5M self-settlements, ceasing within the same two-second window) plus four provably closed clusters whose hub receipts sweep back to the funder to the dollar ($779,489 with $0.00 external outflow)
- **Tier C2 — internal settlement (63.78% of count, 16.82% of value):** funding-linked clusters (e.g., a funder seeds 337 fleet wallets, 31.55M settlements into its own hub, 98.34% of hub inflow returns to the funder); count and value are decoupled
- **Tier C3 — unattributed (15.02% of count, $12.84M):** genuine independent demand bounded between **$187,861.35** (demonstrably reaches a nameable catalog service) and the C2+C3 ceiling **$20,258,746.09 (45.92%)** — a two-order-of-magnitude uncertainty band
- **Concentration:** payer/recipient/value Gini all >0.98; one dominant facilitator per chain; the largest recipient takes 23.08% of Base settlements
- **Manufacture price:** reproducing the entire 136.7M-settlement count costs **~$355,583 in gas** (per-settlement ~8.46×10⁻⁷ ETH) — sponsors the gas; the count is near-free to manufacture
- **Dynamics:** the largest movements in the daily series are operator campaigns switching on/off (incl. a self-payment fleet on → off in two weeks); the facilitator's Jan 1, 2026 per-settlement fee caused the largest sustained fall — volume behaves as if priced at the subsidy; the x402 V2 release (Dec 11, 2025) moves the series **not at all**

### The audit standard (derive from the mechanism)
1. **Name the emission cost.** If a metric is subsidized (gas, credits, rewards) and rewarded (rankings, tokens), it can be manufactured near-free — demand the gas-per-action price before reading it as adoption.
2. **Classify by what the record proves, in tiers, not binary.** Fictitious (self-payment/closed loop) → internal (funding-linked cluster) → unattributed. Assert only the direction each tier supports.
3. **Value-closure over behavioral heuristics.** The one signal that survives an agentic setting (where genuine agents are bots, prices are dust, and funding is custodial) is whether value terminates outside the transactor's control cluster.
4. **Bound, don't point-estimate.** Report the genuine floor (nameable-service revenue) and ceiling (not-provably-manufactured) separately — on-chain data cannot place the truth inside the band.
5. **Test with event-study discipline.** Segment changes that align with operator actions vs external releases; a protocol release that fails to move the series is itself evidence the metric is decoupled from the release's purpose.

### The ecosystem read
The chain shows a star-forest, not a marketplace: near-zero reciprocity (0.025), near-bipartite, near-empty core, top-40 hubs' payer sets Jaccard 0.0036, 6–8 disconnected components. Time-of-day amplitude separates advertised-service payers (median 0.79, diurnal) from operator clusters (0.12, near-flat) at AUC 0.78–0.85 — machine-timed demand-independent traffic fills the count.

## References
- Nearest neighbors: `x402-agentic-share-measurement` (TRM funnel + agency bound — the value-side companion), `x402-demand-reality-check-2026`, `agent-payment-record-gap` (attribution is structurally unsolvable from the record alone — this paper is the measurement version of that argument), `x402-free-riding-attack-surface`, `erc8004-empirical-trust-reality-check-2026`, `devex-metrics-compass-120-metric-navigation` (the DevEx-side Goodhart family).
- Honest caveats: only C1 (21.2%) is *proven* manufactured; C2 verdicts rest on funding-linked clustering with a documented [72.38%, 84.98%] uncertainty band and multi-signal corroboration for the largest clusters (the single-signal remainder is at most 12.6%); C3's residual behavioral model (87.8% "manufactured-behaving") is an estimate, not validation, with stereotype-bias risk (genuine agent traffic and manufacture share signatures); the catalog-based $187,861 floor excludes off-catalog services; window is right-censored at 2026-06-23; the authors release the pipeline for re-measurement.

*Source: Ling, S., Zhou, Y., Wu, L., & Wang, C. (2026). "How Agentic Is Agentic Commerce? A Population-Scale Measurement of x402 Adoption and Authenticity." arXiv:2607.12575 (POMACS), full methodology + facilitator tables + appendices published with the paper.*