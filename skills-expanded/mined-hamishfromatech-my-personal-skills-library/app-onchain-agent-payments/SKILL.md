---
name: APP-onchain-agent-payments
description: Applies the OKX Agent Payments Protocol (APP) — the April 2026 open whitepaper that expands agent payments from a single HTTP 402 response to a full commercial relationship via four intents (charge, escrow, session, upto) plus a stateful Broker over any transport (HTTP/IM/QR) — to design autonomous agent commerce. Use when building agent-to-agent or agent-to-merchant settlement flows requiring escrow, metered billing, splits, or dispute windows, or when choosing between x402, MPP, AP2, and APP for agent payments. NOT for simple one-shot per-request micropayments (x402 already covers that) or card-network checkout flows.
---

# Agent Payments Protocol (APP): The Commercial-Relationship Envelope

## Overview
OKX OnchainOS, *Agent Payments Protocol* whitepaper v1.0 (released April 2026): the first agent-payment spec whose unit of interaction is **a full commercial relationship, not a single HTTP response**. Four intents — charge, escrow, session, upto — cover the lifecycle of a deal (discover counterparty → negotiate scope and price → escrow funds → meter consumption → settle → dispute → split revenue → close billing), with humans intervening by exception rather than at every step.

## When to Use
- Building agent commerce that needs escrow (freelance work, delivery acceptance windows), streaming metered billing (per-token LLM calls), or capped pre-authorization ("at most 5,000 tokens")
- Adding platform fees, creator royalties, referral cuts to agent settlements (first-class splits primitive)
- Deploying agent commerce over messaging (XMTP, Telegram, Discord, Slack) where no HTTP endpoint exists — the A2A shape
- Choosing payment protocols across x402/MPP/AP2/ACP/APP for an agent stack
- NOT for simple one-shot per-request micropayments (x402 handles these; APP defers to it inside its scope)
- NOT for fiat-anchored, chargeback-via-bank flows (card rails serve a different design center)

## Core Process / Workflow
1. **Compose from MPP's EVM grammar**: APP's wire format is a superset of the MPP EVM challenge/credential envelope — "MPP EVM + four intent envelopes + Broker orchestration + cross-IM/HTTP transport."
2. **Choose the intent per commercial shape**:
   - `charge` — one-shot instant transfer (fixed-price goods, one-shot API calls, tips)
   - `escrow` — funds held between commit and release; dispute window; optional external arbitrator
   - `session` — deposit-backed streaming channel; monotonically increasing vouchers; settle at close
   - `upto` — pre-authorized metered deduction with a signed cap + signed usage report; neither side can unilaterally inflate the bill
3. **Adopt the Broker role** (stateful, any operator can implement it): mints paymentIds, produces challenge structures (URL/card/QR/raw deliveries), verifies credentials, broadcasts on-chain, exposes status polling.
4. **Choose the deployment shape**: A2MCP (agent pays a priced HTTP service via an MCP tool) or A2A (agent pays another agent over IM with no HTTPS endpoint required).
5. **Compose splits into settlement** (declared up front; routed in the same step as the primary payment — no post-hoc accounting) and leave dispute resolution pluggable.
6. **Separate signing from custody**: hot key for per-turn signing, cold wallet holds the deposit — the protocol encodes this separation so the funded wallet never signs per-turn.
7. **Reuse audited primitives**: charge/session/upto reduce to off-chain EVM signatures; escrow requires an on-chain custody contract (the audited exception).

## Positioning vs the Stack
- **x402**: single HTTP 402 round-trip, stateless, HTTP-native. APP defers to it in-scope; extends beyond into IM/QR/offline transport and multi-step relationships.
- **MPP**: the EVM wire-format substrate APP consumes directly; "integrating MPP EVM is integrating APP charge."
- **AP2**: authorization mandates (Google, FIDO); APP targets stablecoin-native final settlement with protocol-level escrow.
- **ERC-8004**: agent identity registry — optional, surfaces naturally on delivery cards.
- Key structural contrast: x402 Facilitator = stateless, one-request; APP Broker = stateful, spans days/months of a relationship.

## Pairs with
`agentic-payment-protocol-convergence-2026`, `x402-production-checklist`, `x402-demand-reality-check-2026`, `agent-settlement-protocol-asp-2026`, `ap2-mpp-x402-protocol-stack-2026`, `mcp-payment-support-specification`, `agent-fair-trade-agreement`

## A-Tech Alignment
- **Open source**: open protocol, no required vendor, no proprietary SDK; any team can implement a compliant Broker. OKX's OnchainOS is one runtime, not the only one.
- **Data privacy**: escrow + dispute + upto cap prevent unilateral billing; the signed cap cannot be reused elsewhere — programmable spend limits as the privacy/consent surface.
- **Financial freedom**: sub-cent stablecoin settlement + first-class splits (platform fees, creator royalties, referral bounties at settlement time, not post-hoc) directly serve solo builders and marketplaces.
- **Practical**: the four-intent taxonomy (one-shot / escrowed / streaming / capped) is the cleanest commercial-shape taxonomy in the library — immediately usable in protocol-selection content.

*Source: OKX OnchainOS, Agent Payments Protocol Working Group, whitepaper v1.0, April 2026.*