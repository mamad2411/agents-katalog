---
name: ant-amp-kya-interoperability
description: Applies Ant International's Sept 9–10, 2026 open-sourcing of the Agentic Mobile Protocol (AMP) on GitHub with its global wallet/acquirer rollout and the simultaneous Know-Your-Agent (KYA) interoperability collaboration with Mastercard and Visa via MAS's BuildFin.ai — the first open-source agent-payment protocol at mobile-wallet scale, and the first cross-network agent-identity interoperability effort. Use when [designing agent payment flows into existing wallet rails, evaluating KYA/agent-identity interoperability across payment networks, assessing which agentic payment protocol layer to build against, or reviewing task-scoped agent authorization patterns]. NOT for [card-network tokenization mechanics (see agent-pay-card-network-integration), per-request HTTP settlement (see x402-production-checklist), or AP2 mandate design (see ap2-mpp-x402-protocol-stack-2026)].
---

# Ant AMP Open-Source + KYA Interoperability: The Wallet-Rail Agent Payment Layer

## Overview
Ant International's Agentic Mobile Protocol (AMP), launched April 2026 and now open-sourced on GitHub (github.com/ant-intl/AMP), gives AI agents trusted-actor status inside existing mobile wallet rails — Alipay+ connects 50+ wallets, 10+ national QR schemes, 150M merchants, 2B consumer accounts. The same week, Ant + Mastercard + Visa began collaborating on KYA interoperability through BuildFin.ai (the Monetary Authority of Singapore's platform), building on the SAFR framework. This is the mobile-wallet lane of agent payments — the complement to HTTP-native (x402), mandate-based (AP2), and card-network (Agent Pay) layers.

## When to Use
- Designing agent checkout that must reuse consumers' existing wallets (no new accounts, no re-linking)
- Evaluating KYA interoperability: one verified agent identity recognized across payment networks
- Comparing protocol layers: mobile wallets (AMP) vs HTTP settlement (x402) vs mandates (AP2) vs card rails (Agent Pay)
- Designing task-scoped agent authorization (authorize the task, not hand over the account)
- Building skill/agent monetization products that ride existing consumer payment rails

- NOT for card-network tokenization internals or stablecoin settlement design — see `agent-pay-card-network-integration`, `x402-production-checklist`

## Core Process / Workflow
1. **Design for task authorization, not account handover.** Under AMP, users authorize a task with explicit boundaries — budget (e.g. "US$300 or less"), scope ("specific dates only, 4.5+ rating"), payment source ("only a designated wallet"), and escalation conditions ("re-confirm if the final price goes over"). These conditions follow the task into execution and payment.
2. **Adopt the KYA pattern as the identity layer.** AMP's full-spectrum KYA framework establishes an agent's digital identity, certifies authorized capabilities, and drives an Agent Trust Rating controlling autonomy levels. The interoperability collaboration means an agent registered with one provider may be recognized by others — Yang: "If an agent registers with Ant, they don't need to register again with Visa, Mastercard."
3. **Size A2A settlement for nano-transactions.** AMP's high-frequency A2A settlement mechanism handles transactions as small as $0.000001 between agents with real-time accounting and clearing — the wallet-rail counterpart to x402's sub-cent settlement.
4. **Use AgentSafePay for agent-specific risk.** Money-back guarantee for merchants against agentic-specific failure modes (hallucinated intent, execution drift). Merchant-side protection is the consumer-trust unlock.
5. **Cut agent-wallet integration friction.** AMP claims 50% fewer steps to link a payment agent to a wallet — the integration-cost number to model when choosing a lane.
6. **Read the rollout as the adoption bar.** Phase I: 10 Alipay+ wallets (Alipay, AlipayHK, DANA, GCash, KakaoPay, MPay, TNG, TrueMoney, Toss, Starryblu — 1.5B user accounts) + 7 acquirers (Adyen, Allinpay, Checkout.com, Fiserv, Global Payments, Nuvei, Worldline). Phase I in 2026, expansion thereafter.

## Key Evidence
- **Sources:** Ant International press releases via Business Wire (Sept 9 and Sept 10, 2026); CNBC reporting on the KYA collaboration; The Next Web (Sept 11) on the payment-agent landscape; Cryptonomist (Sept 10).
- **Scale:** Alipay+ = 50+ mobile payment partners, 10+ national QR schemes, 150M merchants, 2B consumer accounts — the world's largest agentic payment network claim.
- **Regulatory anchor:** Built on MAS's Safeguards for Agentic Finance at Runtime (SAFR) framework; advanced through BuildFin.ai with Mastercard and Visa.
- **Consumer proof point:** Alipay app rolling out AI-assisted recurring purchases ("buy me a Starbucks iced Americano at 10 a.m. every day") — agent ordering + human payment confirmation.
- **Open source:** AMP SDK, source code, and docs on GitHub under an open-protocol posture designed from the start for cross-ecosystem use.

## Pairs-with
- `agent-pay-card-network-integration` (the card-network KYA/tokenization counterpart this interoperates with)
- `ap2-mpp-x402-protocol-stack-2026` (the mandate/settlement protocol map — AMP is the wallet lane)
- `x402-production-checklist` (seller-side ops; note KYA as step 5)
- `agent-settlement-protocol-asp-2026` (the commerce tier above settlement)
- `mcp-payment-support-specification`, `mcp-dual-identity-problem` (credential scoping)
- `agentic-commerce-trust-design` (trust architecture)

## A-Tech Alignment
- **Open source:** AMP itself is open-sourced — SDKs and docs adoptable by any wallet, acquirer, or developer; the protocol competition (AMP vs x402 vs AP2 vs Agent Pay) now has a fully open mobile-wallet entrant.
- **Privacy:** KYA is agent identity, not user surveillance; task-scoped authorization means users authorize tasks, not accounts — the least-privilege pattern for consumer agent payments.
- **Financial freedom:** agent-linked wallets keep consumers inside rails they already trust (2B accounts); A2A nano-settlement opens sub-cent skill monetization without new merchant accounts.
- **Practical:** the five-point AMP pattern (task-scoped authorization, KYA identity, trust-rated autonomy, merchant protection, wallet reuse) is a buildable checklist for any agent-commerce product.

## Honesty Caveats
- Phase I is announced rollout, not verified live volume — no transaction metrics published.
- KYA interoperability is an initiated collaboration with no published pilot scope, technical spec, or timeline — standards work, not a shipped product.
- AgentSafePay money-back guarantee is a vendor commitment; terms undisclosed.
- The $3–5T agentic-commerce-by-2030 figure is McKinsey projection, not measured volume.
- Cross-network interoperability depends on each network preserving its own verification processes — portability may be partial in practice.

*Sources: Ant International/Business Wire Sept 9–10, 2026; CNBC; The Next Web Sept 11, 2026; Cryptonomist Sept 10, 2026.*