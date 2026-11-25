---
name: verifiable-intent-agentic-trust-layer
description: Apply Mastercard's Verifiable Intent open-source framework — a cryptographic credential chain (SD-JWT + key binding + selective disclosure) that binds consumer identity, agent authorization, and transaction outcome into a single tamper-resistant record. Co-developed with Google, interoperable with AP2/UCP, built on FIDO/EMVCo/IETF/W3C standards. Use when designing agent transaction trust infrastructure, implementing authorization proof for agentic commerce, building dispute-resolution systems, or integrating with Mastercard Agent Pay / Google payment protocols. NOT for payment execution itself or for agent identity verification alone.
---

# Verifiable Intent: The Agentic Commerce Trust Layer

## Overview

On March 5, 2026, Mastercard — in collaboration with Google — open-sourced the Verifiable Intent specification and a reference implementation. Verifiable Intent (VI) is a cryptographic trust layer that links a consumer's identity, their specific instructions to an agent, and the outcome of the resulting transaction into a single tamper-resistant record. It creates a portable audit trail that any party can verify independently, making dispute resolution faster and cleaner. The framework is designed to be protocol-agnostic and interoperable with Google's Agent Payments Protocol (AP2) and Universal Commerce Protocol (UCP).

This is the technical infrastructure that makes transaction closure (see `transaction-closure-delegated-ai-governance`) cryptographically provable rather than trust-based.

## When to Use

- Designing agent transaction trust infrastructure for agentic commerce
- Implementing authorization proof that links human identity → agent authority → transaction outcome
- Building dispute-resolution systems that require cryptographic evidence
- Integrating with Mastercard Agent Pay's intent APIs
- Evaluating whether to adopt Verifiable Intent vs building a proprietary trust layer
- Designing privacy-preserving agent transaction records (selective disclosure)
- Building agent payment flows that need to satisfy merchant, issuer, and consumer verification needs simultaneously

NOT for:
- Payment execution infrastructure (use agentic-payments-protocol-ap2 or agent-pay-card-network-integration)
- Agent identity verification / Know Your Agent (use agent-reputation-identity-framework)
- Transaction closure governance philosophy (use transaction-closure-delegated-ai-governance)
- Card-network tokenization mechanics (use agent-pay-card-network-integration)

## Core Process / Workflow

### 1. The Three Trust Failures Verifiable Intent Solves

Agentic commerce breaks a core assumption of online payments: that a human is directly clicking "buy" on a trusted surface. Once software can browse, decide, and transact, three concrete failures emerge:

| Trust Failure | What Breaks | What VI Provides |
|---------------|-------------|------------------|
| **Merchant can't distinguish legitimate agent from bot** | No "the customer was here" signal | Credential chain proving agent is bound to a verified human |
| **No deterministic audit trail** | Disputes resolved by inference, not evidence | Tamper-resistant record binding identity + intent + outcome |
| **No portable proof of authority** | Agent authority locked to one platform | Portable credential that any merchant/network can verify |

### 2. The Three-Layer Credential Chain

Verifiable Intent is not an "agent header." It is a composable evidence object built as a layered SD-JWT credential chain with key binding and role-scoped selective disclosure.

```
Layer 1: IDENTITY BINDING
┌──────────────────────────────────────────────────┐
│ Issued by: Identity Issuer → Credential Wallet    │
│ Binds: user identity ↔ public key (cnf.jwk)       │
│ Format: SD-JWT, ES256, ~1 year lifetime           │
│ Discovery: JWKS                                   │
└───────────────────────┬──────────────────────────┘
                        │ sd_hash binding
                        ▼
Layer 2: PURCHASE INTENT
┌──────────────────────────────────────────────────┐
│ Signed by: user key from Layer 1                  │
│ Immediate mode: final checkout values             │
│ Autonomous mode: constraint-bearing mandate       │
│   + agent key binding                             │
│ Binds to Layer 1 via sd_hash                      │
└───────────────────────┬──────────────────────────┘
                        │ (Autonomous mode only)
                        ▼
Layer 3: AGENT FULFILLMENT
┌──────────────────────────────────────────────────┐
│ Signed by: agent key bound in Layer 2             │
│ Short-lived, key-bound SD-JWTs                    │
│ Split for privacy:                                │
│   L3a: network-facing payment mandate             │
│   L3b: merchant-facing checkout mandate           │
└──────────────────────────────────────────────────┘
```

**Why the L3 split matters:** The payment network and the merchant see different views of the same fulfillment. The network sees what it needs for payment authorization; the merchant sees what it needs for order fulfillment. Neither sees more than necessary. This is privacy by construction, not privacy by policy.

### 3. The Two Execution Modes

| Mode | Human Presence | Credential Flow | Use Case |
|------|---------------|-----------------|----------|
| **Immediate** | Human signs final checkout | L1 → L2 (final values) | Human-in-the-loop agent shopping |
| **Autonomous** | Human sets constraints up front; agent executes later | L1 → L2 (constraints + agent key) → L3a/L3b (fulfillment) | Delegated agent commerce (the production default) |

### 4. Selective Disclosure — Privacy by Construction

Verifiable Intent uses Selective Disclosure (SD-JWT) to share only the minimum information each party needs:

- **Merchant** sees: authorization proof, item specifications, delivery details — NOT the user's full identity or financial credentials
- **Payment network** sees: payment authorization, spend limit compliance — NOT the user's shopping preferences or agent reasoning
- **Agent** sees: constraints and fulfillment requirements — NOT the user's raw card credentials (tokenized)
- **Dispute resolver** sees: the full credential chain — only when a dispute is raised and evidence is needed

This aligns with A-Tech's privacy-first principle: the trust layer proves what needs to be proven without exposing what doesn't.

### 5. Constraint Validation

Constraints are first-class in the VI specification. Eight registered constraint types (spend limits, merchant restrictions, item specs, time windows, geographic scope, confirmation thresholds, reversibility, disclosure scope). The verifier must:

1. Support all registered constraint types
2. Validate fulfillment artifacts (e.g., merchant-signed checkout object) against constraints
3. Reject unknown constraint types in open mandates (they can silently unbound authority)
4. Operate in strictness modes: strict (unknown = fail) or permissive (unknown = warn)

**The opinionated design choice:** VI tries to turn "intent" into machine-checkable bounds. It makes the verifier do explicit constraint validation. This is what distinguishes it from a simple "agent header" — it is a composable evidence object that enforces authorization limits cryptographically.

### 6. Interoperability

Verifiable Intent is designed to be protocol-agnostic:

| Integration | Status | What it means |
|-------------|--------|---------------|
| Google AP2 (Agent Payments Protocol) | Compatible | VI provides the trust layer; AP2 provides the payment execution |
| Google UCP (Universal Commerce Protocol) | Compatible | VI provides intent proof; UCP provides the commerce protocol |
| Mastercard Agent Pay | Native | VI is part of the Agent Pay program; intent APIs integration expected |
| FIDO Alliance standards | Built on | Identity verification foundations |
| EMVCo standards | Built on | Payment industry standards |
| IETF standards | Built on | SD-JWT, JWT, JWKS |
| W3C standards | Built on | Web platform standards |

**Partner ecosystem (launch):** Google, Fiserv, IBM, Checkout.com, Basis Theory, Getnet. Open-sourced on GitHub with reference implementation at verifiableintent.org.

### 7. Comparison: Verifiable Intent vs Other Trust Approaches

| Approach | Layer | What It Proves | Limitation |
|----------|-------|---------------|------------|
| Verifiable Intent | Trust proof | Identity + intent + outcome bound cryptographically | New; adoption depends on partner uptake |
| Agent Pay tokenization | Payment credential | Agent is bound to a verified cardholder | Doesn't prove what the agent was instructed to do |
| Know Your Agent (Visa) | Agent identity | Agent provenance and ownership | Doesn't link to specific transaction intent |
| x402 | Payment protocol | Payment was authorized and settled | Doesn't carry intent or constraint evidence |
| AP2 | Payment protocol | Payment orchestration for agents | Trust layer is separate (VI fills this) |

**The complementary stack:** VI (trust proof) + AP2/x402 (payment execution) + KYA (agent identity) + Agent Pay (card network access) = complete agentic commerce trust infrastructure.

### 8. A-Tech Application Matrix

#### A-Coder
- **Agent-generated code authorization:** When A-Coder's agent generates code on behalf of a developer, the VI pattern applies: Layer 1 binds the developer's identity, Layer 2 binds the task constraints (scope, security requirements, dependency policies), Layer 3 records the agent's fulfillment (generated code + provenance). Disputes ("the agent introduced a vulnerability") can be resolved from the credential chain.
- **Privacy-first differentiator:** VI's selective disclosure aligns with A-Coder's local-first architecture — the trust proof travels with the transaction without centralizing user data.
- **Open-source integration:** Adopt the VI specification for A-Coder's agent transaction records. Contribute to the open-source reference implementation.

#### Be Practical
- **Curriculum module:** "Cryptographic trust for agentic commerce." The three-layer credential chain, selective disclosure, constraint validation, the interoperability map.
- **Exercise:** Design the VI credential flow for an agent that books travel. Which constraints go in Layer 2? What does the merchant see vs the payment network? How does a dispute get resolved?

#### Builder's Club
- **Reference implementation:** Open-source VI integration library for Builder's Club marketplace agents. Any agent in the marketplace can produce VI-compliant closure records.
- **Community standard:** Propose VI adoption as the trust standard for Builder's Club agent transactions. Agents that produce VI-compliant records get a "verified intent" badge.

## Cross-References

- **`transaction-closure-delegated-ai-governance`** — Defines what transaction closure means (the governance framework). This skill defines how to prove it cryptographically (the trust layer).
- **`agentic-payments-protocol-ap2`** — The payment protocol that VI interoperates with. AP2 executes payments; VI proves what was authorized.
- **`agent-pay-card-network-integration`** — Mastercard Agent Pay card-network integration. VI is the trust layer within the Agent Pay program.
- **`agentic-commerce-trust-design`** — The trust-gap diagnosis. VI is the technical infrastructure that closes the gap.
- **`agentic-trust-security-protocols-2026`** — The broader trust/security protocol landscape. VI is a specific implementation within that landscape.
- **`agent-reputation-identity-framework`** — Agent identity. VI binds human identity to agent authority; KYA frameworks establish agent identity. They compose.

## References

- See [references/vi-specification-details.md](references/vi-specification-details.md) for the credential format specification, constraint types, partner statements, and the VI vs Visa Trusted Agent Protocol comparison.