---
name: x402-production-checklist
description: Use when accepting x402/HTTP-402 payments from AI agents, building USDC micropayment rails for APIs, deciding between x402 MPP AP2 ACP for agent payment, or auditing agent-payment settlement flows for correct network token and facilitator configuration.
---

# x402 Production Checklist (Seller Side, Sept 2026)

**Sources:** Stablecoin Insider, "How to Accept x402 USDC Payments from AI Agents" (Sept 2, 2026); The API Economy (Sept 1, 2026); Inriver protocol guide (Aug 31, 2026); Blockchain.News protocol comparison (Aug 27, 2026). The first wave of x402 seller-side operational guidance as the protocol moved from demo to production.

## Protocol Stack Context (who does what)

| Protocol | Backer | Layer | Status |
|---|---|---|---|
| **x402** | Coinbase → x402 Foundation (Linux Foundation, July 14 2026, 40 members incl. Visa/Mastercard/Amex/Stripe/Adyen/Fiserv/Google/AWS/Shopify/Cloudflare) | Per-request settlement over HTTP 402 | Operational |
| **MPP** (Machine Payments Protocol) | Stripe + Tempo (mainnet March 18 2026) | Session-based machine spending (locked limit, batch settle) | Live; Visa card specs contributed |
| **AP2** (Agent Payments Protocol) | Google + 60 partners (Sept 2025); v0.2 donated to FIDO Alliance April 2026 | Authorization mandates (Intent/Cart/Payment) | Production-ready; "Human Not Present" in v0.2 |
| **ACP** | OpenAI + Stripe | Checkout structuring (ChatGPT Instant Checkout) | Retired Instant Checkout Mar 2026; spec remains |
| **UCP** | Google + 20+ retailers (NRF 2026) | Full-journey commerce | Available |

**They compose, they don't compete.** x402 handles one-shot settlement; MPP handles sessions; AP2 proves authorization; ACP/UCP structure the shopping flow. A mature agent speaks several.

## Scale Reality Check

- x402 last-30-days (late Aug 2026): ~75.4M transactions, $24.24M volume, ~22K sellers, ~$0.32 avg/tx. First-year totals: 165–180M payments, ~$47.5M cumulative.
- Agentic token consumption crossed human token consumption on OpenRouter in Feb 2026; by Aug 2026 ~7.3T tokens/7-day average.
- McKinsey: $3–5T agent-orchestrated commerce by 2030; Juniper: $8B in 2026 → $1.5T by 2030. Wide ranges — trajectory real, magnitude unsettled.

## Seller-Side Implementation Checklist (the actionable core)

1. **Network:** start with Base mainnet (`eip155:8453`); Circle native USDC contract `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`. Never book a bridged wrapper (USDC.e/USDbC) or clone ticker as dollars.
2. **Facilitator:** production CDP (`https://api.cdp.coinbase.com/platform/v2/x402`) for mainnet. **Never reuse the x402.org testnet facilitator URL on mainnet routes** — the single most common misconfiguration.
3. **`accepts` payload:** `scheme` (exact / upto / batch-settlement), price, CAIP-2 network, `payTo` you control. A 402 advertising the wrong `payTo` is unpaid work waiting to happen.
4. **Verify before revenue:** confirm settlement hash + token contract + amount + destination before booking. A 200 without verified settlement = free resource delivery.
5. **KYA (know-your-agent):** settlement proves money moved, not who moved it. Run agent allowlists/mandate checks before treating a repeating agent as trusted revenue.
6. **Reconcile every hash to a SKU/cost center** — the seller-side mirror of buyer-side spend ledgering.
7. **No chargebacks on settled USDC.** Wrong `accepts` config = unpaid work or cloned-USDC acceptance with no card-network reversal. Every control must be preventive, not remedial.

## Strategic Reading

- **The payment mechanics are becoming commodity; identity, authority, and auditability are where differentiation lives.** Facilitators are the trust-critical chokepoint (whoever verifies payment can verify identity too).
- **The unsolved layer is trust, not payment:** "The agent did it" is not a defense under the GENIUS Act, MiCA, or EU AI Act. An accountable operator is assumed behind every automated transaction.
- **Sub-cent economics only work at machine scale:** a tenth of a cent is irrelevant to humans but a viable economic unit for agents (1B paid requests/day @ $0.001 = $1M/day).

## Cross-Links

- `agentic-payment-protocol-convergence-2026`, `agent-economy-payment-protocols`, `mcp-payment-support-specification` — protocol family
- `agent-pay-card-network-integration` — card-rail counterpart
- `real-time-metering-ai-agent-revenue`, `agent-ready-api-monetization-pattern` — monetization patterns x402 implements
- `erc8004-empirical-trust-reality-check-2026` — the reputation/identity layer x402 lacks
- `kimi-cloud-revshare-watch` — distribution-layer revshare; x402 is the per-request counterpart

## A-Tech Fit

- **Open source:** x402 is an open standard under Linux Foundation with open reference implementations — no vendor lock-in for A-Tech's agent-payment recommendations.
- **Financial freedom:** the seller checklist is a direct revenue-enablement path for solo/small developers selling API access to agents (one of the few genuinely new revenue channels in 2026).
- **Privacy:** wallet-based identity + KYA requirements intersect with A-Tech's privacy posture — flag that settlement ≠ identity and that KYA data is itself sensitive.
- **Practical:** the seven-step checklist is deployable in a week (testnet → mainnet flip) for any API provider in A-Tech's orbit.