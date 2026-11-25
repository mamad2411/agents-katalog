---
name: agent-reputation-identity-framework
description: Build verifiable identity, portable reputation, and trust infrastructure for AI agents operating in multi-agent marketplaces and autonomous commerce. Covers DID standards, verifiable credentials, reputation scoring, session-key architectures, and cross-platform portability. Use when designing multi-agent systems, agent marketplaces, or autonomous payment networks where trust between unknown agents is required. NOT for single-agent tools operating within one trusted environment.
---

# Agent Reputation & Identity Framework

## Overview

As AI agents transact autonomously across platforms, swarms, and marketplaces, verifiable identity becomes foundational. An agent without identity cannot build reputation. Without reputation, no rational counterpart will transact. This skill provides the standards, architectures, and implementation patterns for creating portable, trustworthy agent identities that work across the emerging agentic economy.

## When to Use

- Designing a multi-agent marketplace where unknown agents must transact
- Building agent-to-agent payment infrastructure requiring authentication
- Creating a platform where agent reputation determines access or pricing
- Developing cross-platform agent portability (same agent, multiple environments)
- Establishing compliance frameworks for autonomous transactions under EU AI Act or similar

NOT for:
- Single-agent tools operating entirely within one organization's trust boundary
- Prototypes where manual API key management is sufficient
- Situations where all agents are operated by known, pre-vetted entities

## Core Process / Workflow

### 1. Establish the Identity Layer

Every agent receives a unique, cryptographically provable identity consisting of:

```
Agent Identity Stack:
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Decentralized Identifier (DID)                     │
│ • W3C DID v1.0 compliant                                   │
│ • Self-sovereign: no platform controls the identifier        │
│ • Resolvable to DID Document containing public keys        │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 2: Verifiable Credentials (VCs)                     │
│ • Cryptographically signed attestations about the agent    │
│ • Issued by trusted parties (platforms, auditors, users)   │
│ • Selective disclosure: agent reveals only what's needed   │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 3: Wallet / Smart Account                             │
│ • ERC-4337 compatible account abstracted wallet            │
│ • Session keys for delegated, bounded permissions          │
│ • Holds assets, signs transactions, pays for services      │
└─────────────────────────────────────────────────────────────┘
```

**Key standards:**
- W3C DID Core v1.0 — identifier specification
- W3C Verifiable Credentials Data Model 2.0 — attestation format
- ERC-4337 — account abstraction for Ethereum
- ERC-8004 — on-chain agent identity registration
- eIDAS 2.0 / EUDI Wallet — EU digital identity framework (mandatory deployment by year-end 2026)

### 2. Issue and Accumulate Verifiable Credentials

Credentials are the building blocks of reputation. Each successful interaction, audit, or certification adds a signed credential to the agent's wallet.

| Credential Type | Issuer | Use Case |
|-----------------|--------|----------|
| **Platform Verified** | Marketplace operator | Agent completed KYC, passed sandbox testing |
| **Task Completion** | Counterparty agent or user | Agent successfully delivered outcome X |
| **Security Audit** | Third-party auditor | Agent code reviewed, no critical vulnerabilities |
| **Performance Rating** | Automated metering | Agent maintained >99% uptime over 30 days |
| **Compliance** | Regulatory body | Agent meets EU AI Act transparency requirements |
| **Capability** | Certification authority | Agent certified for domain Y (medical, legal, financial) |

**Selective disclosure pattern:**
When Agent A approaches Agent B to transact, it presents only the credentials relevant to that transaction:
- For a data-processing task: platform verification + performance rating
- For a financial transaction: security audit + compliance credential
- For a creative task: capability credential + portfolio of task completions

### 3. Build the Reputation Scoring Model

Reputation is not binary. It is a multi-dimensional score that decays over time and adapts to context.

```
Reputation Dimensions:
┌─────────────────────────────────────────────────────────────┐
│ Reliability (40% weight)                                    │
│ • Task completion rate                                       │
│ • Uptime percentage                                          │
│ • Dispute resolution outcomes                                │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ Quality (30% weight)                                        │
│ • Counterparty satisfaction ratings                          │
│ • Output accuracy metrics                                    │
│ • Rework rate (how often output needs correction)          │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ Trustworthiness (20% weight)                                │
│ • Security audit recency and score                           │
│ • Compliance credential validity                             │
│ • Dispute history (zero vs. frequent)                      │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│ Speed (10% weight)                                          │
│ • Average time to task completion                            │
│ • Response latency for inquiries                             │
│ • Settlement speed (if handling payments)                  │
└─────────────────────────────────────────────────────────────┘
```

**Temporal decay:**
- Credentials older than 90 days lose 10% weight per month
- This incentivizes continuous operation and prevents "resting on laurels"
- Exception: security audits and compliance credentials carry full weight until expiry

**Context adaptation:**
- A medical coding agent's reputation in healthcare carries zero weight in creative writing
- Reputation scores are computed per-domain using only relevant credentials

### 4. Implement Session-Key Delegation

Agents must act autonomously, but users must retain control. Session keys provide the bridge.

**Architecture:**
1. User creates a smart account (ERC-4337) and deposits funds
2. User issues a session key to the agent with bounded permissions:
   - Spending cap per transaction ($50 max)
   - Spending cap per day ($500 max)
   - Approved counterparties only (whitelist)
   - Approved service categories only (APIs, compute, storage)
   - Time-bound expiry (24 hours, 7 days, or custom)
3. Agent operates within these bounds without requiring user approval for each action
4. User can revoke the session key instantly if behavior is suspicious

**Security model:**
- If agent is compromised, attacker gains only the session key's bounded permissions
- User's main wallet and full balance remain protected
- All agent transactions are traceable to the session key and auditable

### 5. Enable Cross-Platform Portability

An agent's identity and reputation should travel with it across platforms.

**Portable reputation flow:**
1. Agent operates on Platform A, accumulates credentials and reputation
2. Agent decides to offer services on Platform B
3. Agent presents DID + relevant VCs to Platform B
4. Platform B verifies credentials cryptographically (no need to trust Platform A)
5. Platform B assigns a starter reputation based on imported credentials, then refines with local performance

**Anti-gaming protections:**
- Credential issuers must be on a recognized trust registry
- Sybil resistance: creating 1,000 fake agents to pump ratings requires 1,000 separate DIDs and meaningful transaction histories
- Dispute arbitration: neutral third parties resolve reputation disputes, with outcomes recorded as credentials

### 6. Integrate with Payment Protocols

Identity and reputation enable payment. The layers connect as follows:

```
Transaction Flow:
1. Agent A discovers Agent B via A2A protocol auto-discovery
2. Agent A requests Agent B's DID Document + relevant VCs
3. Agent B presents credentials (selective disclosure)
4. Agent A verifies credentials + computes reputation score
5. If reputation > threshold, Agent A initiates transaction
6. Payment settled via x402 / AP2 / ACP based on negotiated terms
7. Upon completion, both agents issue task-completion VCs to each other
8. Reputation scores update in real time
```

## A-Tech Applications

- **A-Coder (IDE):** Agent mode uses portable identity to hire specialized agents from a marketplace (security auditor, test writer, documentation generator). Each agent arrives with verifiable credentials and a reputation score. The IDE auto-selects the highest-reputation agent for each task category.
- **Be Practical (Playbooks):** Chapter on "Trust in the Agent Economy" — how solo founders and small teams can build agent reputation from zero. The "first 10 credentials" playbook: completing free tasks for credential issuers, passing sandbox tests, and accumulating initial ratings.
- **Builder's Club (Community):** Open-source "Agent Passport" toolkit — DID creation, VC issuance, reputation scoring, and session-key management. Community-maintained trust registry of credential issuers. Benchmark: which reputation models best predict actual agent performance.

## Measurement Framework

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Credential verifications / day | Zero | >100 | DID resolver logs |
| Average reputation score of transacting agents | N/A | >0.7 (on 0–1 scale) | Reputation engine |
| Dispute rate | N/A | <2% | Arbitration records |
| Cross-platform agent migrations / month | Zero | >10 | Platform analytics |
| Session key revocations (security events) | N/A | <0.5% | Smart contract events |
| Time from discovery to first transaction | Hours | <5 minutes | A2A protocol telemetry |

## References

- See [references/did-standards-extraction.md](references/did-standards-extraction.md) for W3C DID Core, Verifiable Credentials Data Model 2.0, and eIDAS 2.0 mandate specifications.
- See [references/erc-4337-session-keys.md](references/erc-4337-session-keys.md) for account abstraction, session key implementation patterns, and security audit references.
- See [references/crossmint-platform-comparison.md](references/crossmint-platform-comparison.md) for platform comparison of agent identity and payment infrastructure providers in 2026.
