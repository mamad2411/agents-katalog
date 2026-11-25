---
name: agent-fair-trade-agreement
description: Applies the Agent Fair-Trade Agreement (AFTA v1.0, TensorFeed.ai, May 2026) to design agent-commerce systems with code-enforced no-charge guarantees, signed receipts, and peer-to-peer federation. Use when building monetized MCP servers, agentic commerce platforms, or AI agent payment infrastructure; when designing AI agent marketplaces with trust guarantees; when building x402-based payment systems for autonomous agents; when creating federated agent payment networks without central brokers.
---

# Agent Fair-Trade Agreement (AFTA)

## Overview
AFTA is an open peer-to-peer standard for honest commerce between data publishers and autonomous AI agents. It defines four code-enforced no-charge guarantees, signed receipts as the audit rail, USDC on Base as the value rail, and a federation pattern that lets independently-operated sites share a credit ledger without a central broker. The standard is open; adoption is the certification.

## When to Use
- Building monetized MCP servers with per-tool pricing
- Designing agentic commerce platforms with trust guarantees
- Creating x402-based payment systems for autonomous agents
- Building federated agent payment networks
- Designing agent marketplaces with code-enforced fairness
- Creating AI agent service discovery with payment primitives

- NOT for human-facing payment systems (designed for agent-to-agent and agent-to-API)
- NOT for centralized marketplace platforms (AFTA is explicitly peer-to-peer)
- NOT as a replacement for x402 protocol itself (AFTA builds on x402)

## Core Process / Workflow

### 1. Publish the AFTA Manifest
Publish a JSON document at `/.well-known/agent-fair-trade.json` with:
- Publisher identity and source repository
- No-charge guarantees (at least 3 required: 5xx, stale data, schema validation)
- Receipt signing configuration (Ed25519 keys)
- Pricing transparency (credit costs, volume discounts)
- Data license (inference-only by default)
- Federation members (if participating)

### 2. Implement No-Charge Guarantees
Code-enforce at least three no-charge conditions:

1. **5xx errors:** Server errors do not charge a credit
2. **Stale data:** If data is older than the published freshness SLA, no charge
3. **Schema validation failures:** Invalid input does not charge

Optional but recommended:
4. **Circuit breaker trips:** Rate-limit violations return 429 with no charge

### 3. Issue Signed Receipts
Every paid or refunded call returns an Ed25519-signed receipt containing:
- Request hash, response hash
- Credits charged, credits remaining
- Freshness SLA, no-charge reason (if any)
- Agent-supplied nonce (prevents replay)
- Timestamp

### 4. Integrate x402 Payment Rail
- Publish `/.well-known/x402.json` declaring accepted payment methods
- Accept USDC on Base (or other declared rails)
- Implement the 402 challenge → payment → retry flow
- Support both credits-flow (batched) and per-call x402

### 5. Federation (Optional)
- Pairwise arrangement between two AFTA-adopting sites
- Shared credit ledger hosted on one site
- Validate-and-commit handshake with reservation IDs
- No central broker; peer-to-peer only

## Key Findings (AFTA v1.0, May 2026)

### The No-Charge Principle
The publisher does not charge when the service fails to deliver. This is code-enforced, not a policy. The boundary cases are documented in the manifest with pointers to source code.

### Signed Receipts as Audit Rail
Every interaction returns a cryptographically signed receipt. The agent can store and audit these later. A third party can verify any receipt against the publisher's published key. The publisher cannot rewrite history because receipts are signed at issue time and on-chain payments are immutable.

### Federation Without Centralization
AFTA is a peer agreement, not a marketplace. Two AFTA-adopting sites can federate by exchanging a shared secret and agreeing on a validate-and-commit handshake. After federation, a bearer token issued by either site works on both.

### Adoption as Certification
There is no AFTA central authority, no certification fee, no logo licensing. Any publisher can self-publish their AFTA manifest. Any third party can verify the publisher's claims by reading the manifest and the linked source code.

## A-Tech Value Alignment

| A-Tech Value | AFTA Alignment |
|---|---|
| **Open-source AI** | AFTA is an open standard; adoption is the certification; no proprietary gatekeeping |
| **Data privacy** | Receipts are cryptographically signed; on-chain settlement is immutable and auditable; inference-only licensing by default |
| **Financial freedom** | Peer-to-peer federation without brokers; no platform fees; agents earn directly |
| **Practical implementation** | Reference implementation at TensorFeed.ai; open source; deployable in hours |

## References
- See [references/afta-evidence-base.md](references/afta-evidence-base.md) for details.