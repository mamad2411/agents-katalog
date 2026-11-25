---
name: x402-agentic-share-measurement
description: Applies TRM Labs' Sept 9, 2026 on-chain measurement of x402 agent-payment volume as the AGENTIC-SHARE-BOUND pattern — the first rigorous on-chain attempt to separate genuine agentic commerce from ordinary automation on the leading agent-payment rail, finding that of ~$52.7M settled via known facilitators since May 2025 (198.9M transactions), screening removes roughly half, and the surviving ~$25.6M of "screened commerce" is only 0.6%–7.5% likely agentic under strict vs. permissive attribution tests, because scripts and agents leave identical on-chain records. Use when [auditing claims about agent-economy adoption, designing attribution tests for machine-originated transactions, briefing on the gap between x402 volume headlines and agentic reality, or setting honesty standards for agent-payment metrics]. NOT for [payment-protocol mechanics — use ap2-mpp-x402-protocol-stack-2026 — or the daily-value drawdown — use x402-demand-reality-check-2026].
---

# Who Is Actually Paying? The Agentic-Share Bound

## Overview
TRM Labs ("Who's Actually Paying? Measuring AI Agent Payments Onchain," Sept 9, 2026) performs the measurement the whole x402 ecosystem lacked: what fraction of settled volume is *agentic*? Their answer is a bound, not a point estimate — 0.6% (strict) to 7.5% (permissive) of screened commerce — because on-chain, a scheduled script and an agent are indistinguishable. This is the missing complement to the library's volume-tracking and demand-reality skills: those measured how much and which direction; this measures *who*.

## When to Use
- Auditing any headline like "205M agent payments" or "$53M agentic commerce settled"
- Designing attribution tests for machine-originated payment flows (agent registries, facilitators, merchants)
- Briefing teams on why transaction-count milestones ≠ agentic adoption
- NOT for: protocol mechanics (use `ap2-mpp-x402-protocol-stack-2026`); value-curve drawdowns (use `x402-demand-reality-check-2026`); discovery bottlenecks (use `x402-discovery-bottleneck-2026`)

## Core Process / Workflow

### The attribution funnel (replicable method)
1. **Universe:** ~$52.7M across 198.9M settlement transactions mediated by known x402 facilitators since May 2025 (Base, Solana, Polygon).
2. **Commerce screens (three):** remove self-payment addresses; remove bulk flows from one or two payers; remove sellers with fewer than ten distinct buyers. → ~half of settled volume falls away → ~$25.6M "screened commerce."
3. **Agency attribution — two bounds, not one number:**
   - **Permissive test:** payer broadcast by a facilitator, sub-dollar average amounts, varied (not fixed) prices.
   - **Strict test:** permissive criteria PLUS sustained multi-month pattern AND (registered in ERC-8004 agent registry OR paid >1 seller).
   - Result: **0.6%–7.5%** of screened commerce appears agentic.
4. **Structural observations:** 99.6% of value settled in USDC (the agentic economy on public rails is, today, a stablecoin economy); monthly agentic volume roughly $5K–$11K; composition shifted from late-2025 speculation (meme-minting) → concentration in a single payment contract (H1 2026) → AI services returning mid-2026 through an agent-payment router.

### Why attribution breaks (the three structural causes)
- **Ownership is unverified.** On-chain registries (ERC-8004) are voluntary; most participants don't register.
- **No human in the loop.** Agent signs; facilitator broadcasts; no confirmation step exists for controls to attach to.
- **Value and volume decouple.** Payments sit below every value threshold and above every count threshold simultaneously — controls calibrated for human-scale payments miss them from both directions.

### The honest-metrics standard (the transferable rule)
For any "agent economy" claim, demand the funnel, not the headline: universe → screens → permissive bound → strict bound. If a builder reports only the universe number, they're reporting *rail usage*, not *agentic commerce*. TRM's framing to internalize: "The rail already works. What is needed is accurate registration, counterparty reputation an agent can check on its own, and monitoring built for volume rather than value."

### Design implications for merchants
- Headline x402 volume is "mostly not customers" — attracting agent traffic needs machine-readable endpoints, per-call pricing, and discoverability without human-facing pages.
- KYA (know-your-agent) before trusting agent payers; reconcile every settlement hash to a SKU/cost center (see `x402-production-checklist`).

## References
- Nearest neighbors: `x402-demand-reality-check-2026` (the daily-value drawdown — this skill adds the *who* bound to its *how much*), `agentic-token-metrics-openrouter` (count milestones), `x402-free-riding-attack-surface` (the security layer — now with a formal flaw taxonomy from the May 2026 paper), `erc8004-empirical-trust-reality-check-2026` (registration rates), `agent-payment-record-gap` (the record layer under authorization), `x402-discovery-bottleneck-2026`.
- Honesty caveats: agency cannot be read off a transaction — the 0.6–7.5% band is a *modeling bound* with explicit assumptions (e.g., single-purpose agents paying one service repeatedly would be classified as scripts, potentially understating agentic share); facilitator-based universe excludes self-verified settlement paths; categories are TRM's groupings of identifiable merchants.

*Source: TRM Labs, "Who's Actually Paying? Measuring AI Agent Payments Onchain," Noah Hodge, Sept 9–10, 2026 (trmlabs.com). Corroborating context: Coinbase's Sept 2026 disclosure of 205M x402 transactions / ~$53M / 200K sellers (AgentRisk via DEV Community, Sept 9, 2026).*