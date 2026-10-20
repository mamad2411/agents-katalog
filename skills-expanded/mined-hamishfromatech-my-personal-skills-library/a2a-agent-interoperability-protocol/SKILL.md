---
name: a2a-agent-interoperability-protocol
description: Implement Google's Agent-to-Agent (A2A) protocol for cross-vendor agent discovery, task delegation, and secure collaboration. Covers Agent Cards, task lifecycle, authentication, and A2A-MCP complementarity. Use when building multi-agent systems that must interoperate across platforms, designing agent marketplaces, or architecting vendor-neutral agent ecosystems.
---

# A2A Agent Interoperability Protocol

## Overview

Google released the Agent-to-Agent (A2A) protocol in April 2025 as an open standard under the Linux Foundation and Apache 2.0 license. While MCP (Model Context Protocol) standardizes how a single agent accesses tools and context, A2A standardizes how agents discover, communicate, and collaborate with each other across vendor boundaries. The two protocols are complementary: MCP is the tool layer; A2A is the social layer.

A2A enables an agent built on Claude to delegate a subtask to an agent built on Gemini, which in turn might use a local Llama agent for sensitive data processing — all with structured task states, capability negotiation, and authenticated trust boundaries. For A-Tech, A2A is the interoperability backbone for the Builder's Club marketplace, Be Practical multi-agent workflows, and A-Coder's plugin ecosystem.

## When to Use

- Building agent marketplaces where third-party agents discover and hire each other
- Designing cross-platform multi-agent workflows (e.g., Claude agent + Google agent + local agent)
- Architecting vendor-neutral agent infrastructure that avoids single-provider lock-in
- Implementing agent reputation, identity, and trust networks at the protocol level
- NOT for single-agent systems or intra-process tool chaining (use MCP instead)

## The A2A-MCP Relationship

| Dimension | MCP (Anthropic) | A2A (Google + LF) |
|-----------|-----------------|-------------------|
| **Scope** | Agent ↔ Tool / Data source | Agent ↔ Agent |
| **Analogy** | USB port for peripherals | Wi-Fi mesh for devices |
| **Discovery** | Static server registry | Dynamic Agent Card directory |
| **Negotiation** | None (caller knows capabilities) | Yes (capability exchange via Agent Cards) |
| **State** | Stateless request/response | Stateful task lifecycle |
| **Authentication** | OAuth 2.0, API keys | Mandate signing, identity attestation |
| **Best for** | Tool access, context retrieval | Cross-vendor collaboration, task delegation |

**Integration pattern:**
```
User Intent
    → MCP (retrieve context, invoke tools)
    → A2A (discover specialist agent, negotiate task)
    → Agent B executes via its own MCP stack
    → A2A (return results, close task)
```

## Core Concepts

### Agent Card
Every A2A-compliant agent exposes an **Agent Card** — a JSON metadata document describing:
- **Capabilities:** What tasks the agent can perform (e.g., "code review," "security audit")
- **Interfaces:** Supported input/output schemas and formats
- **Authentication:** Required credentials and trust frameworks
- **Policies:** Rate limits, cost structures, data handling rules
- **Reputation:** Historical ratings, completion rates, audit scores

Agent Cards are hosted at a well-known URL (e.g., `/.well-known/agent.json`) and indexed by directories or registries. Discovery can be push (agent registers with directory) or pull (directory crawls known hosts).

### Task Lifecycle
A2A defines a five-state task lifecycle that both agents track:

| State | Meaning | Transition Trigger |
|-------|---------|------------------|
| **Submitted** | Task sent, awaiting acceptance | Agent B receives task |
| **Accepted** | Agent B commits to execution | Capability match confirmed |
| **Working** | Execution in progress | Agent B begins work |
| **Completed** | Final result delivered | Output validated and sent |
| **Failed** | Execution failed or rejected | Error, timeout, or capability mismatch |

Each state transition emits an event, creating an auditable trail for dispute resolution and reputation scoring.

### Message Types
A2A standardizes four message primitives:

1. **Task Assignment** — Delegation with goal, constraints, deadline, and budget
2. **Query / Status Poll** — Request for current state or intermediate output
3. **Negotiate** — Counter-offer on price, scope, or timeline before acceptance
4. **Escalate** — Human-in-the-loop trigger for ambiguous or high-stakes decisions

Messages carry cryptographic signatures (mandate signing in AP2-aligned implementations) to prove authorization chains.

## Security & Trust Architecture

### Authentication Layers
- **Identity:** DID (Decentralized Identifier) or X.509 certificates bound to agent runtime
- **Attestation:** TEE (Trusted Execution Environment) proofs for agents running in enclaves
- **Mandate Signing:** Human authorization cryptographically bound to agent-initiated actions (AP2 integration)

### Trust Boundaries
A2A operates across three trust zones:

| Zone | Risk Level | Controls |
|------|-----------|----------|
| **Intra-org** | Low | mTLS, internal PKI, short-lived tokens |
| **Partner mesh** | Medium | OAuth 2.0, contractual SLAs, reputation thresholds |
| **Open marketplace** | High | Full mandate signing, escrow, dispute arbitration, bonded deposits |

### Privacy Considerations
- Agents should negotiate data handling policies before accepting tasks
- PII and sensitive context should flow through MCP with local-first preference, not through A2A messages
- A2A itself carries metadata (who asked whom, when, for what) — this is audit data, not user data

## Practical Implementation for A-Tech

### Builder's Club Marketplace
1. Every Builder's Club agent publishes an Agent Card
2. A-Coder users browse/search capabilities via directory
3. Task delegation uses A2A with x402 micropayment settlement
4. Reputation accumulates from completion rates and peer reviews

### Be Practical Multi-Agent Workflows
- **Chapter Generation:** Planning agent (A2A) → Research agent (MCP + A2A) → Writing agent (MCP) → Editor agent (A2A review)
- **Cross-validation:** Security agent and UX agent independently review output via A2A consensus

### A-Coder Plugin Interoperability
- Third-party plugins expose Agent Cards describing IDE integration capabilities
- A-Coder discovers compatible plugins dynamically instead of hardcoding integrations
- Users compose custom IDE agent stacks without vendor lock-in

## Roadmap & Adoption Signals

| Milestone | Date | Significance |
|-----------|------|-------------|
| A2A announced | April 2025 | Google releases protocol with 50+ partners |
| Linux Foundation | April 2025 | Open governance under LF, Apache 2.0 |
| Anthropic acknowledgment | Mid-2025 | Industry consensus that A2A and MCP are complementary |
| Auth0 / Okta guides | July 2025 | Enterprise identity integration documented |
| A-Tech evaluation | Q2 2026 | Production readiness assessment for marketplace |

## Measurement Framework

| Metric | Target | How to Track |
|--------|--------|------------|
| Agent Card coverage | 100% of published agents | Registry scan |
| Cross-vendor task success rate | ≥ 90% | Task lifecycle logs |
| Average discovery-to-delegation time | < 30 seconds | Telemetry on directory queries |
| Dispute rate | < 2% | Arbitration case volume |
| Marketplace transaction volume | > $0 by Q3 | x402/AP2 settlement logs |

## Cross-References
- See `ai-agents-and-workflows/agentic-payments-protocol-ap2` for payment layer integration with A2A
- See `ai-agents-and-workflows/mcp-security-trust` for MCP-side tool security
- See `ai-agents-and-workflows/agentic-swarm-orchestration` for multi-agent topology design
- See `ai-agents-and-workflows/agent-reputation-identity-framework` for reputation scoring beyond protocol basics
- See `ai-agents-and-workflows/imf-agentic-payments-framework-2026` for compliance layer mapping

## Sources
- Google Developers Blog — "Announcing the Agent2Agent Protocol (A2A)" (April 9, 2025)
- A2A Protocol Official Documentation (a2a-protocol.org)
- Auth0 Blog — "MCP vs A2A: A Guide to AI Agent Communication Protocols" (July 2025)
- arXiv:2505.02279 — "A Survey of Agent Interoperability Protocols"
- Linux Foundation A2A Project Repository (github.com/a2aproject/A2A)
