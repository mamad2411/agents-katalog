---
name: imf-agentic-payments-framework-2026
description: Apply the IMF's authoritative three-layer model for integrating agentic AI into payment systems. Covers the Intent/Orchestration, Control/Authorization, and Settlement layers with protocol mappings, risk classification matrix, and mitigation strategies. Use when designing agentic payment architecture, evaluating regulatory risk, or advising on compliant agent commerce infrastructure.
---

# IMF Agentic Payments Framework 2026

## Overview

In April 2026, the IMF published Note 2026/004, "How Agentic AI Will Reshape Payments" — the first authoritative multilateral framework for reconciling probabilistic agentic AI with deterministic payment infrastructure. The note introduces a three-layer conceptual model that separates adaptive decision-making from rule-based authorization and legally final settlement. For A-Tech, this framework is the compliance and architecture reference for building any agent-initiated payment or commerce system.

The core tension: payment infrastructures (RTGS, card networks, instant payment platforms, DLT settlement) operate deterministically — predictable rules, binary outcomes, legal finality. Agentic AI systems rely on probabilistic reasoning and adaptive decision-making. The IMF framework resolves this not by eliminating either property, but by concentrating probabilistic reasoning upstream while preserving deterministic controls downstream.

## When to Use

- Designing agentic payment architecture for A-Coder plugins, Be Practical services, or Builder's Club marketplace
- Evaluating regulatory risk in agent-initiated commerce across jurisdictions
- Advising on compliant agent commerce infrastructure for enterprise clients
- Mapping existing payment workflows to the three-layer model for audit or certification
- Building risk registers for agentic AI products with financial transaction components

NOT for:
- Treating the framework as prescriptive regulation (it is a normative analytical lens, not law)
- Ignoring the probabilistic nature of agentic systems
- Designing systems that bypass deterministic authorization and settlement layers

## The Three-Layer Model

The IMF proposes a strict functional separation:

```
Layer 1: Intent and Orchestration (Probabilistic)
    ↓ structured intent
Layer 2: Control and Authorization (Deterministic)
    ↓ authorized instruction
Layer 3: Settlement (Deterministic, legally final)
```

### Layer 1 — Intent and Orchestration
Translates high-level user objectives into structured, machine-readable instructions. No authorization or execution occurs here.

**Capabilities:**
- Reasoning, planning, search, negotiation
- Multi-agent coordination
- Dynamic adaptation to context

**Key standards:**
| Standard | Function |
|----------|----------|
| **MCP** | Standardizes agent access to external data and tools |
| **A2A** | Enables interoperability among agents from different vendors |
| **x402** | Embeds payment requirements in HTTP requests for automatic negotiation |
| **UCP (Google)** | Shared grammar for discovery, comparison, and post-purchase logic |
| **ACP (OpenAI/Stripe)** | Buyer-agent-merchant commerce protocol |

**Industry pilots:**
- Visa Intelligent Commerce: agent-initiated shopping under predefined limits
- Mastercard Agent Suite: "Know Your Agent" frameworks with network tokens
- PayPal Cymbio: independent agents using PayPal's transaction graph and secure vaults

**Rule:** Everything produced at Layer 1 is *proposed intent*. It does not become a payment instruction until it passes Layer 2.

### Layer 2 — Control and Authorization
Enforces deterministic constraints on whether proposed actions may proceed. This is the trust boundary.

**Core mechanism: AP2 mandates**
- Cryptographically verifiable mandates specifying scope, limits, actor identity, and permitted conditions
- Binds agent-initiated actions to explicit user consent rather than model-generated inference
- Extensions: x402 for stablecoin integration; OAuth 2.0 / OpenID Connect for agent identity verification

**Deterministic controls:**
- Issuer rules, AML/CFT filters, velocity checks
- Sanctions screening, tokenization rules, dispute guardrails
- Programmable wallets (ERC-4337, ERC-6900) enforcing spend limits and counterparty restrictions
- ERC-8004: on-chain registries for agent identity, validation, and reputation

**Authorization model shift:**
Traditional payments require transaction-level instructions from the account holder. Agent-initiated payments use *structural, mandate-based* authorization. Individual transactions may not correspond to explicit per-transaction instructions — instead, they operate within a pre-approved scope. This raises traceability, consent, and liability questions that existing legal frameworks were not built to address.

**Rule:** Anything accepted at Layer 2 becomes an authorized payment instruction eligible for deterministic execution in Layer 3. Anything rejected is routed back to Layer 1 for revision.

### Layer 3 — Settlement
Executes authorized instructions with irrevocable legal finality.

**Components:**
- RTGS systems, instant payment networks, card network clearing engines
- Central bank digital currency platforms
- DLT-based settlement rails
- Smart contract wallets (ERC-4337) for conditional execution

**Principle:** Layer 3 is non-probabilistic by design. It takes only instructions that have passed deterministic controls in Layer 2 and executes them without modification, optimization, or reinterpretation. Agentic algorithms do not operate here.

**Why this matters:** Legal finality, systemic stability, and auditability depend on this separation. If probabilistic reasoning bleeds into settlement, the foundations of the payment system become unstable.

## Mapping the Payment Journey

| Payment Function | Problem Addressed | Technologies | Layer(s) |
|------------------|-------------------|--------------|----------|
| Intent management | Enable agents to reason over user objectives, constraints, preferences | LLMs, MCP, ACP | L1 |
| Agent coordination | Allow multiple agents to exchange plans, negotiate, delegate | A2A, multi-agent orchestration | L1 |
| Commerce workflow | Standardize discovery → comparison → offer → prepare for authorization | UCP | L1 + L2 |
| Delegation/authorization | Prove agent is authorized to act with scope-limited permissions | AP2, OAuth 2.0, OpenID Connect | L2 |
| Agent identity (KYA) | Identify and authenticate software agents as distinct actors | ERC-780, ERC-8004, AP2 credentials | L2 |
| Real-time compliance | Detect anomalies, sanctions risk, policy violations before authorization | ML fraud systems, mandate constraints | L2 |
| Programmable settlement controls | Encode agent permissions, guardrails into digital money/wallets | ERC-4337, ERC-6900, ERC-1812 | L2 |
| Platform-specific execution | Allow agents to initiate payments inside ecosystems | AP2, x402 | L2 + L3 |
| Programmable money rails | Support agent-driven payments with conditions and guarantees | DLT, smart contracts | L3 |
| Traditional payment rails | Plug into regulated systems | RTGS, cards | L3 |
| Liquidity management | Optimize liquidity across payment systems | RTGS, stablecoins | L3 |

## The Risk Classification Matrix

The IMF identifies twelve risk categories and maps each to its source, cost bearer, and market-failure justification:

| Risk | Primary Source | Who Bears Cost | Market Failure? |
|------|--------------|---------------|---------------|
| Instruction gap (structural vs. transactional authorization) | Account holders delegating broad mandates; AI agents executing without transaction-level instructions | Account holders (unexpected payments); PSPs (disputes); payment systems (operational strain) | Yes. Information/control asymmetry; misalignment between legal authorization and agentic execution |
| Opacity of agent decision-making | AI developers designing non-interpretable models; platforms integrating agents | Users (lack of redress); PSPs (compliance failures); supervisors (reduced oversight) | Yes. Information asymmetry and unverifiable decision processes |
| High-speed machine-time execution | AI agents/platforms optimizing speed; inadequate throttling | PSPs and payment systems (operational overload); end users (error propagation) | Yes. Externalities from speed amplification and coordination effects |
| Authorization traceability failures | PSPs relying on mandate-based auth without robust auditability | PSPs (liability); users (disputed payments); courts/regulators (uncertainty) | Yes. Legal infrastructure mismatch; incomplete contracting |
| Ambiguous liability allocation (agency-based) | Account holders, PSPs, system operators under outdated liability assumptions | PSPs and users (litigation, losses); payment systems (reputational risk) | Yes. Legal uncertainty and incomplete allocation |
| Product liability from autonomous behavior | AI model providers, integrators deploying adaptive systems | PSPs, platforms, or users depending on interpretation; potentially model providers | Yes. Existing product liability not designed for adaptive post-deployment behavior |
| Correlated agent behavior (herding) | Homogeneous models and shared optimization across agents | Payment systems (liquidity stress); PSPs (settlement delays); end users (failed payments) | Yes. Coordination externalities and systemic risk |
| Intraday liquidity stress | Agents optimizing timing/liquidity; PSPs failing to impose constraints | Payment systems; central banks (liquidity backstops); participants | Yes. Systemic liquidity externalities |
| Cybersecurity and attack surface expansion | Platforms integrating agents with multiple tools/APIs; weak access controls | Users (fraud); PSPs (losses); payment systems (disruptions) | Yes. Security externalities and under-investment |
| DLT settlement without legal finality | System designers deploying DLT without statutory settlement recognition | Users and intermediaries (reversals, insolvency); legal system | Yes. Legal infrastructure gap and jurisdictional fragmentation |
| Regulatory blind spots (KYA, supervision) | Regulators lagging technological change; platforms operating across borders | Financial system (loss of trust); regulators (oversight failure) | Yes. Public good nature of supervision and cross-border coordination |

## Market Experimentation: 2026 Snapshots

| Initiative | Actor | Mechanism | Fee Structure |
|------------|-------|-----------|---------------|
| **Instant Checkout** | OpenAI + Stripe | Agentic Commerce Protocol (ACP) | **4% transaction fee for autonomous agent-led conversions** |
| **Rufus / "Buy for Me"** | Amazon | Delegated purchasing via Rufus assistant | Standard merchant fees |
| **Universal Commerce Protocol** | Google | Native checkout within Search AI Mode and Gemini | Merchant acquiring infrastructure |
| **Intelligent Commerce / Agent Suite** | Visa + Mastercard | Network-level tokenization and KYA frameworks | Network interchange |
| **Cymbio acquisition** | PayPal | Trust layer for agentic web; merchant-of-record preservation | Standard PayPal fees |

## Mitigation Strategies

### Systemic Measures
- **Human-in-the-loop:** Transaction thresholds requiring human approval; supervisory dashboards; manual override mechanisms
- **Kill switches:** Layered governance with distributed (not centralized) control; graduated responses; clear authority and auditability
- **Architectural separation:** Probabilistic decision-making and deterministic execution must remain separated

### Private Sector Measures
- Agent-ready card products with embedded spending controls and real-time budget management
- Global agent registries with identity verification, reputation scoring, and fraud monitoring
- Dispute resolution frameworks tailored to AI-initiated transactions with clear liability allocation
- Open protocol standards for interoperability across AI platforms
- Real-time access to clean, consistent data mapped holistically
- Robust cybersecurity: strong authentication, scoped authorization, secure API governance

### Public Sector Measures
- **Know Your Agent (KYA):** Mandated verifiable identities for financial bots linked to legal entities
- Real-time monitoring systems detecting anomalies in agent behavior and transaction flows
- AI activity logs and audit trails with automated alerts for abnormal behavior
- Regulatory sandboxes for testing agentic payment systems before full deployment
- Regulatory harmonization to prevent fragmentation and spillover
- Singapore's Model AI Governance Framework for Agentic AI: risk assessment, agent power limits, human accountability at checkpoints, technical controls, transparency and education

## A-Tech Applications

### A-Coder (IDE Plugin Marketplace)
- **Layer 1:** Agent discovers plugins via MCP; constructs purchase intent with user-defined constraints (budget, category, quality)
- **Layer 2:** AP2 mandate authorizes plugin spending up to user-defined limit; trust badge verification (Gold/Silver/Bronze); automated compliance check
- **Layer 3:** x402 stablecoin settlement for per-call billing; traditional rails for subscription tiers; instant finality with programmable spending controls

### Be Practical (Playbooks)
- **"The Agentic Payment Compliance Playbook"** — Map any agent commerce idea through the IMF three-layer model
- **Case study:** How the 4% OpenAI/Stripe fee structure affects solo founder pricing
- **Risk register template:** The 12-category IMF risk matrix applied to small-team agent products
- **Jurisdiction checklist:** Where mandate-based authorization is recognized vs. ambiguous

### Builder's Club
- **Open-source IMF framework toolkit:** Reference implementation of the three-layer model for community projects
- **KYA registry prototype:** Decentralized agent identity and reputation system
- **Compliance working group:** Track regulatory sandbox openings and AI governance frameworks globally
- **Architecture reviews:** Evaluate member projects against the Layer 2 deterministic control requirement

## Measurement Framework

| Metric | Target | Measurement |
|--------|--------|-------------|
| Layer separation compliance | 100% of payment workflows | Architecture audit |
| Mandate coverage | 100% of agent-initiated transactions | AP2 mandate logs |
| Traceability audit pass | 100% | Quarterly compliance review |
| Deterministic control enforcement | 100% of Layer 3 instructions | Settlement log review |
| Cross-border protocol compliance | All applicable jurisdictions | Legal review |
| Agent registry participation | 100% of paid agents | Registry analytics |
| Kill switch response time | < 60 seconds | Drill testing |
| Dispute resolution time | < 7 days | Support metrics |

## A-Tech Values Alignment

| Value | How This Framework Serves It |
|-------|------------------------------|
| **Open-Source AI** | AP2 and x402 are open protocols; community can build compliant infrastructure without vendor lock-in |
| **Data Privacy** | Mandate-based authorization gives users granular control over what agents can spend; local settlement options preserve transaction privacy |
| **Financial Freedom** | Open agent commerce protocols lower barriers to building payment-enabled agent services; solo developers can compete on equal infrastructure |
| **Practical Implementation** | The three-layer model is immediately applicable to any A-Tech product with agent-initiated transactions; provides an audit-ready architecture |

## Cross-References
- See `ai-agents-and-workflows/agentic-payments-protocol-ap2` for AP2 mandate schemas, x402 V2 integration, and MPP session architecture
- See `ai-agents-and-workflows/agentic-commerce-2026` for protocol landscape comparison and microtransaction economics
- See `ai-agents-and-workflows/agentic-commerce-trust-design` for the trust conversion gap and merchant legitimacy framework
- See `ai-agents-and-workflows/mcp-security-trust` for supply-chain security and server authentication in agent infrastructure
- See `privacy-and-trust/agentic-ai-zero-trust-compliance` for zero-trust security architecture applied to agents
- See `monetization-and-revenue/mcp-server-monetization-2026` for meter-first engineering in agent-accessible tool billing

## Sources
- IMF — "How Agentic AI Will Reshape Payments" (Note 2026/004, April 2026): Three-layer model, risk matrix, protocol mapping, mitigation strategies
- BCG — "Agentic AI, Digital Currencies and Real-Time Transactions Reshape Global Payments Landscape" (September 2025)
- BIS — "The Use of Artificial Intelligence for Policy Purposes" (2025): AI agents managing liquidity in RTGS systems
- Google — "Universal Commerce Protocol" (developers.google.com/merchant/ucp, January 2026)
- Stripe — "Supporting Additional Payment Methods for Agentic Commerce" (2026): 4% agent-led conversion fee
- FinRegLab — "The Next Wave Arrives: Agentic AI in Financial Services" (2025)
- Gartner — "Agentic AI Will Autonomously Resolve 80 Percent of Customer Service Issues by 2029" (March 2025)
- World Economic Forum — "AI agents could be worth $236 billion by 2034 — if we get trust right" (January 2026)
