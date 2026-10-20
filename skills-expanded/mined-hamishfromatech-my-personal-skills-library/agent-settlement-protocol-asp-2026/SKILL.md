---
name: agent-settlement-protocol-asp-2026
description: Applies the Agentic Settlement Protocol (Mohammadkhani, Khekade & Kakkad, arXiv:2609.02208, Sept 2 2026) — the first specification for refundable, delayed-fulfilment agent commerce on stablecoin rails — as the pattern skill for moving agent payments beyond one-shot x402 metered calls into real purchases with holds, refunds, and fulfilment verification. Use when [designing agent-payment flows for physical goods/services/bookings, evaluating x402-adjacent protocols for commerce, building marketplace or seller-side agent checkout, or assessing trust/exposure models in agentic payments]. NOT for [pure metered API billing (x402 exact suffices), authorization-mandate design (AP2), or general agent identity (ERC-8004)].
---

# Agentic Settlement Protocol (ASP): From Metered Calls to Real Purchases

## Overview
x402 solved metered access: one request, one atomic stablecoin payment, one round trip — perfect for data, tools, and inference. It structurally fails commerce. A purchase made on a person's behalf (a plumber visit, a physical order, a flight, a freelance deliverable) is **large, frequently cancelled, and should not become the seller's money until the seller has delivered**. The Agentic Settlement Protocol (arXiv:2609.02208, XDC AI; draft v0.6 Aug 31 2026) specifies that missing layer: how an on-chain authorize-and-capture escrow (the Commerce Payments Protocol primitive, already wired into x402 refund extensions) should be driven when fulfilment is decided by an off-chain system — any order, scheduling, invoicing, or booking engine — that has its own clock, hold semantics, and refund rules.

## When to Use
- Designing agent-mediated checkout for anything with inventory, slots, invoices, or bookings
- Evaluating whether an agent-payment stack can survive cancellations and non-delivery
- Building seller-side or platform-side agent commerce (Shopify-scale connectors)
- Assessing credit-exposure and trust models in any escrow-backed agent-payment design
- NOT for: per-request API metering; AP2-style mandate design; agent reputation scoring

## The Core Diagnosis: Two Independent Clocks

Every online business already runs a **fulfilment engine** — a hold-then-commit lifecycle:
| System | Hold | Commit | Refund authority |
|---|---|---|---|
| Order management (Shopify/Woo) | stock reservation timeout | shipment confirmed | returns policy |
| Service scheduling | slot hold expiry | appointment confirmed/completed | notice-period rules |
| B2B invoicing | invoice due date | acceptance | credit note/dispute |
| Freelance marketplace | delivery deadline | deliverable accepted | arbiter/partial acceptance |
| Travel (GDS/NDC) | ticketing time limit | ticket issued | fare rules |

The escrow and the engine are two distributed systems with independent clocks. If not coordinated: money held after stock released, or slot held after money returned. No payment-layer spec (x402, CPP, AP2, ACP) addresses this — the problem sits one layer up. **ASP is that layer.**

## The Five Contributions (the transferable mechanics)

1. **Three-deadline hold model (H1–H4).** Separate: *issuance deadline* (connector-enforced), *escrow expiry* (chain time), *engine inventory expiry* (wall clock), ordered `t_issue + M < t_h ≤ t_e − δ` with margin M = submission + inclusion + finality + clock drift. Result (Proposition 1): **no inventory is ever issued against funds the buyer can reclaim.** The H2 issuance gate refuses commit after t_issue; the vault itself reverts capture with attestation `issuedAt > t_issue` (H3) — safety enforced on-chain, not by operator discipline.
2. **Fulfilment-verification ladder (rungs D/C/A/S).** "Capture on fulfilment" is meaningless without saying *who asserts fulfilment*. D = on-chain verifiable (none) · C = connector-signed data commitment with challenge window (shipped orders, appointments, travel) · A = seller attestation, longer window (on-site services, invoices) · S = buyer acknowledgement/arbiter (freelance deliverables). Rung C is explicitly an *auditable data-commitment model*, not cryptographic fulfilment — the operator that captures without issuance signed a receipt for a record that doesn't exist, demonstrable within the challenge window. **The rung is part of the signed Offer, so the buyer agent knows the trust position before signing.**
3. **Engine-authoritative refunds + bounded exposure.** Refundable amount = whatever the engine's own rules compute (no flat window imposed). Refund liquidity order: seller vault → rolling reserve → settlement-delayed proceeds → operator pool. Per-seller controls (rolling reserve ρ, settlement delay, exposure cap, per-charge/daily caps, risk tiers) plus **atomic exposure reservation at Offer issuance** — without it, a seller at $90k of a $100k cap could take 100 concurrent $1k quotes to a $190k liability. Operator aggregate liability is bounded (Proposition 3): simultaneous default of all sellers + all in-flight capture failures ≤ λ·pool.
4. **Self-dealing-proof revenue share (Proposition 2).** Distributor share taken atomically at capture; if the distributor bears the full charge amount and its share s < 1, each self-referred charge is a net loss of f·amount·(1−s). Condition to watch: third-party subsidies (launch incentives) can flip the inequality.
5. **Single-currency invariant + normative interfaces.** One currency across deposit/capture/refund per charge — no swaps, oracles, or slippage in the settlement path. Full normative spec: x402 `asp` scheme, vault ABI (deposit/capture/void/reclaim/refund with events and errors), operator/connector APIs with the mandatory timeout rule (never retry a timed-out commit; call getHold), conformance levels (ASP-Lite/Core/Full) with a 17-case executable conformance suite.

## Deployment Shape (reference: ASP-Lite on XDC Network)
- USDC on XDC (ERC-3009 gasless authorizations); operator relayer pays gas
- Buyer = ERC-4337 smart account with on-chain per-charge/rolling spend caps (compromised-agent blast radius bounded); seller = counterfactually deployed smart account (no key needed pre-first-capture)
- ESC-4337-style pause roles: depeg pause halts deposit/capture; **reclaim is never pausable** — a pause can never strand buyer funds
- Platform-connector onboarding = days (one connector onboards every seller on a platform); direct integration 2–4 weeks

## Honest Caveats
- Design paper: no deployed measurements yet (gas, latency, expiry-race behavior); fault-injection evaluation plan specified, results to follow
- Operator trust at rungs A/S is challenge-window-bounded, not eliminated; multi-operator/arbiter-set designs are future work
- Partial capture (multi-leg itineraries) unspecified in this draft; on-chain charge metadata is public (privacy mitigations out of scope)
- Vendor-affiliated authors (XDC AI) — treat as a serious specification with a commercial stake, not neutral standards work

## Buyer-Agent Integration Checklist
- [ ] Parse the `asp` scheme in the x402 402 response; recompute offerId and reject on mismatch
- [ ] Verify offerSignature recovers to offer.signer; check signerAuthority against the seller registry
- [ ] Read the rung (D/C/A/S) and challenge/refund windows **before** signing — the Offer is the trust contract
- [ ] After deposit: poll statusUrl / subscribe to webhooks — a 200 means funds *held*, not paid; resource arrives at `captured`
- [ ] Plan for failure codes (OFFER_EXPIRED, TIMING_MISMATCH, H1_VIOLATION, EXPOSURE_CAP, TOKEN_PAUSED)
- [ ] Remember reclaim: after holdExpiresAt, anyone (including third parties on the buyer's behalf) can reclaim

## A-Tech Alignment
- **Open source:** x402-scheme-native, CPP-compatible, normative public spec + executable conformance suite — an open composable layer, not a vendor lock.
- **Privacy:** bounded blast radius via on-chain spend caps; KYA/identity left to registries (privacy of charge metadata flagged as an open gap — consistent with the library's stance).
- **Financial freedom:** makes the *seller* side of agentic commerce viable for small businesses (bounded operator exposure instead of unlimited refund liability; days-not-months onboarding); new revenue channel for solo developers building connectors.
- **Practical:** the two-clocks diagnosis, rung ladder, and buyer checklist transfer directly to any escrow-backed agent-payment design and to A-Tech content ("x402 pays for tokens — ASP pays for the plumber").

## Related Skills
- `x402-production-checklist` — the metered-layer seller checklist this complements
- `mcp-payment-support-specification` / `agent-economy-payment-protocols` — protocol-stack context
- `agentic-commerce-trust-design` / `verifiable-intent-agentic-trust-layer` — the mandate/consent layer ASP sits beneath
- `erc8004-empirical-trust-reality-check-2026` — the reputation caveat ASP's authors cite
- `transaction-closure-delegated-ai-governance` — closure-of-delegation framing for delegated spending