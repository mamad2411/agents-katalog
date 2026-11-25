---
name: agent-protocol-stack-2026
description: Navigate the six-protocol agent communication stack — MCP, A2A, AG-UI, A2UI, AP2, X42 — that defines how AI agents connect to tools, delegate to other agents, stream to user interfaces, sync persistent state, are managed/controlled, and govern cross-boundary trust. Covers each protocol's layer, problem solved, maturity, and how they compose into a complete multi-agent architecture. Use when building production multi-agent systems, choosing which protocols to adopt, designing agent infrastructure, or evaluating agent platform compatibility. NOT for single-agent tool access only (use mcp-enterprise-adoption-2026) or for agent-to-agent coordination alone (use a2a-agent-interoperability-protocol).
---

# The Six-Protocol Agent Stack (2026)

## Overview

In 2023, building an AI agent meant picking a model and writing prompts. In 2026, it means navigating a growing stack of communication standards that determine how your agent connects to tools, talks to other agents, surfaces results to users, is managed by infrastructure, and governs cross-boundary trust. Six protocols — **MCP, A2A, AG-UI, A2UI, AP2, and X42** — have become the connective tissue of modern AI systems.

This skill maps the full protocol stack so A-Tech can make informed adoption decisions, build protocol-compliant infrastructure, and position A-Coder and Builder's Club in the emerging agent ecosystem. It extends the existing individual-protocol skills (mcp-enterprise-adoption-2026, a2a-agent-interoperability-protocol) with the complete stack view and the newer interface, management, and governance protocols.

## When to Use

- Building production multi-agent systems that need to work across platforms
- Choosing which agent protocols to adopt and in what order
- Designing agent infrastructure (orchestration, monitoring, UI, governance)
- Evaluating agent platform compatibility and lock-in risk
- Building agent marketplaces or cross-organizational agent collaboration
- Designing A-Coder's agent plugin ecosystem and Builder's Club marketplace infrastructure

NOT for:
- Single-agent tool access only (use mcp-enterprise-adoption-2026)
- Agent-to-agent coordination alone (use a2a-agent-interoperability-protocol)
- Agentic payment protocols (use agentic-payments-protocol-ap2 — note: AP2 in this stack refers to Agent Protocol v2, a different standard from the payment protocol)
- Agent trust/security protocols (use agentic-trust-security-protocols-2026)

## The Six Protocols at a Glance

| Protocol | Layer | Primary Problem Solved | Maturity | Released |
|---|---|---|---|---|
| **MCP** | Tool access | Connecting agents to external tools and data | High (widely adopted) | Nov 2024 (Anthropic) |
| **A2A** | Agent coordination | Letting agents delegate tasks to other agents | High (gaining traction) | Apr 2025 (Google) |
| **AG-UI** | Interface streaming | Pushing agent output to a UI in real time | Medium (gaining adoption) | Early 2025 (CopilotKit) |
| **A2UI** | Interface state | Syncing agent state persistently with a UI | Emerging (formalized pattern) | 2025 |
| **AP2** | Agent management | Standardizing how systems control and query agents | Medium (developer tooling) | Evolution of Agent Protocol |
| **X42** | Trust & governance | Managing permissions for cross-boundary agent calls | Emerging (enterprise focus) | 2026 |

## Core Process / Workflow

### Step 1: Understand the Three Communication Problems

Modern agents face three distinct communication problems, each addressed by different protocols:

```
Problem 1: Tool and data access
    → How does an agent connect to external systems?
    → Solved by: MCP

Problem 2: Agent-to-agent communication
    → How does one agent delegate tasks to another?
    → Solved by: A2A

Problem 3: Agent-to-interface communication
    → How does an agent push state and output to a user interface?
    → Solved by: AG-UI (streaming) + A2UI (persistent state)

Cross-cutting:
    → How do systems manage and control agents? → AP2
    → How are cross-boundary calls governed? → X42
```

### Step 2: Evaluate Each Protocol

#### MCP — The Foundation Layer (Tool Access)

**What it does:** Standardizes how AI models connect to external tools, data sources, and services. Before MCP, each tool integration required custom code. MCP replaces this with a universal client-server architecture.

**How it works:**
- MCP server exposes resources, tools, and prompts
- MCP client (your agent) connects and discovers available capabilities
- Three core primitives: Resources (data), Tools (functions), Prompts (templates)
- Transport: JSON-RPC 2.0 over stdio or HTTP with SSE

**Adoption:** Claude, ChatGPT, Gemini, Cursor, dozens of other tools. An MCP server built today works with multiple AI clients without modification.

**For A-Tech:** A-Coder should expose an MCP server for its capabilities (code analysis, security scanning, refactoring) and consume MCP servers for external integrations. This makes A-Coder's features callable from any MCP-compatible client.

**Detailed implementation:** See mcp-enterprise-adoption-2026 skill.

#### A2A — The Coordination Layer (Agent-to-Agent)

**What it does:** Connects one agent to another. In multi-agent systems, a coordinator agent manages work and specialist agents execute tasks. A2A standardizes that contract.

**How it works:**
- **Agent Card:** JSON document an agent publishes describing itself (capabilities, task types, input formats, authentication, endpoints)
- Communication over HTTP: synchronous, streaming, or asynchronous responses
- Supports multi-turn interactions (agents exchange clarifying messages before completing tasks)

**A2A + MCP complementarity:**
```
Agent uses A2A → communicate with other agents (delegation, orchestration)
Agent uses MCP → connect to tools and external data
```
Google worked with Anthropic on interoperability from the start. They are designed to be complementary.

**For A-Tech:** Builder's Club marketplace should use A2A for agent discovery and delegation. An A-Coder agent can delegate a security review to a specialized audit agent via A2A, while both use MCP for their respective tool access.

**Detailed implementation:** See a2a-agent-interoperability-protocol skill.

#### AG-UI — The Streaming Interface Layer

**What it does:** Standardizes bidirectional, event-driven communication between AI agents and frontend applications. Solves the "cobbled together WebSockets/SSE" problem.

**How it works:** Typed event categories:
- **Text streaming events** — incremental text as agent generates
- **Tool call events** — when agent invokes a tool and when results return
- **State sync events** — agent state updates the frontend can render
- **Lifecycle events** — run start, run end, error, interrupt signals

**Key properties:** Framework-agnostic (React, Vue, plain JS), agent-side doesn't care about model/runtime.

**For A-Tech:** A-Coder's UI should implement AG-UI for real-time agent output streaming. This enables consistent rendering of agent activity across the IDE interface, regardless of which model or runtime is executing.

#### A2UI — The Persistent State Layer

**What it does:** Syncs persistent state between agent and UI. Where AG-UI handles the live output stream, A2UI handles the underlying state layer — what the agent knows, what tasks it's tracking, what decisions it's made.

**How it works:**
- Agent writes to a shared state schema
- UI subscribes to that state and re-renders
- Similar to React state management, but for agent-generated data

**For A-Tech:** A-Coder's project state (active tasks, agent memory, decision history) should be exposed via an A2UI-compatible state schema. This enables the UI to reflect agent state consistently and allows external tools to query agent state.

#### AP2 — The Management/Control Plane

**What it does:** Standardizes how external systems start, stop, query, and inspect agent processes. The control plane for agent infrastructure.

**Core endpoints:**
- Creating and managing agent runs
- Sending input and receiving output
- Querying agent state and execution history
- Managing memory and context windows

**Where it fits:** A2A handles agent-to-agent delegation. AP2 handles how humans and systems *supervise and control* the agents involved. Particularly relevant for debuggers, monitoring dashboards, orchestration platforms.

**For A-Tech:** A-Coder's agent monitoring and debugging infrastructure should implement AP2-compatible endpoints. This enables integration with standard agent observability tools and allows Builder's Club members to monitor their agents through standard interfaces.

#### X42 — The Trust and Governance Layer

**What it does:** Manages permissions for cross-boundary agent calls — how agents running in one environment safely invoke agents or capabilities in another, with appropriate access controls and audit trails.

**How it works:**
- Wraps inter-agent invocations in a permission model
- Signed requests, scoped tokens, execution logs
- Clear record of what was called, by whom, with what authorization

**Where it fits:** Enterprise deployments where compliance requirements make ad-hoc agent-to-agent calls impractical. Most relevant as multi-agent systems cross organizational lines.

**For A-Tech:** Builder's Club marketplace agent-to-agent transactions should implement X42-style governance. When a Builder's Club agent invokes a capability on another member's agent, signed requests and execution logs create the trust trail needed for commercial agent collaboration.

### Step 3: Adoption Strategy — Don't Adopt All Six at Once

**The practical path:**

```
1. START with the layer your current problem requires:
   - Agent needs external tools? → Learn MCP first
   - Coordinating multiple agents? → Add A2A
   - Building live UI on agent output? → Look at AG-UI
   - Need persistent state sync? → Add A2UI
   - Managing agent infrastructure? → Consider AP2
   - Cross-boundary governance? → Evaluate X42

2. SCALE from there — add protocols as your system grows
3. Most teams today need: MCP + A2A + one interface protocol
4. AP2 and X42 become relevant at scale / enterprise governance
```

**Maturity-weighted adoption:**
- **Build on (high maturity):** MCP, A2A
- **Adopt with confidence (medium maturity):** AG-UI, AP2
- **Watch and pilot (emerging):** A2UI, X42

### Step 4: The Complete Multi-Agent Architecture

A production multi-agent system that uses all six protocols:

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                         │
│  (AG-UI for streaming, A2UI for persistent state)        │
├─────────────────────────────────────────────────────────┤
│                  Orchestration Layer                      │
│  (A2A for agent-to-agent delegation)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ Agent A  │  │ Agent B  │  │ Agent C  │               │
│  │(coordinator)│ │(specialist)│ │(specialist)│            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│       │MCP          │MCP          │MCP                   │
├───────┼─────────────┼─────────────┼──────────────────────┤
│       ▼             ▼             ▼                      │
│  ┌────────┐   ┌────────┐   ┌────────┐                   │
│  │Tools & │   │Tools & │   │Tools & │                   │
│  │Data    │   │Data    │   │Data    │                   │
│  └────────┘   └────────┘   └────────┘                   │
├─────────────────────────────────────────────────────────┤
│              Management & Governance                      │
│  (AP2 for control, X42 for cross-boundary trust)         │
└─────────────────────────────────────────────────────────┘
```

### Step 5: A-Tech Application Matrix

| A-Tech Product | Protocol Stack Application |
|---|---|
| **A-Coder** | Expose MCP server (capabilities callable from any client). Consume MCP servers (external integrations). Implement AG-UI for real-time IDE streaming. A2UI for project state. AP2 endpoints for monitoring/debugging. A2A for delegating specialized tasks (security audit, test generation) to external agents. |
| **Be Practical** | A2A for multi-agent learning workflows (a tutor agent delegates to a assessment agent). AG-UI for interactive learning interfaces. X42 for governance when agents access external educational resources. |
| **Builder's Club** | Full marketplace stack: A2A for agent discovery/delegation, MCP for tool access, X42 for cross-boundary trust on commercial agent transactions, AP2 for marketplace monitoring. Agents list Agent Cards; consumers discover via A2A; transactions governed by X42. |

## Protocol Conflicts and Clarifications

**Important disambiguation:** "AP2" in this skill refers to **Agent Protocol version 2** (a management/control plane standard). This is *different* from **AP2** in the agentic-payments-protocol-ap2 skill, which refers to Google's **Agent Payments Protocol 2** (a payment authorization standard). Both are named "AP2" but serve entirely different layers. When researching or implementing, disambiguate by context:
- Agent Protocol v2 (management) → this skill
- Agent Payments Protocol 2 (payments) → agentic-payments-protocol-ap2 skill

**X42 vs. x402:** X42 in this skill is the trust/governance protocol for cross-boundary agent calls. x402 (in agent-to-agent-economy-operating-guide) is the HTTP payment protocol (402 Payment Required). Different protocols, different layers.

## Measurement Framework

| Metric | What It Measures | Target |
|---|---|---|
| Protocol coverage | Which of the 6 protocols are implemented | MCP + A2A minimum; add per use case |
| Cross-client compatibility | Number of AI clients that can use your MCP server | Increasing (Claude, ChatGPT, Gemini, Cursor, etc.) |
| Agent Card completeness | A2A Agent Card fields populated | 100% of required fields |
| Interface event coverage | AG-UI event types implemented | All 4 categories for full UI support |
| Cross-boundary audit trail | X42 signed request logs per transaction | 100% of cross-org agent calls |
| Management endpoint coverage | AP2 endpoints implemented | All 4 categories for full observability |

## Integration with Existing Skills

| Related Skill | Relationship |
|---|---|
| mcp-enterprise-adoption-2026 | Detailed MCP implementation; this skill provides the stack context |
| a2a-agent-interoperability-protocol | Detailed A2A implementation; this skill provides the stack context |
| agentic-trust-security-protocols-2026 | Trust protocols (Visa TAP, FIDO, KYA); X42 is the agent-to-agent governance complement |
| agentic-payments-protocol-ap2 | Payment protocol (different AP2); this skill's AP2 is the management protocol |
| agent-to-agent-economy-operating-guide | Agent marketplace platforms; this skill provides the protocol infrastructure |
| mcp-security-trust | MCP-specific security; this skill provides the broader protocol context |
| agent-experience-design-2026 | Agent UX design; AG-UI and A2UI are the protocol layer for agent UX |

## References

- See [references/six-protocol-stack-evidence.md](references/six-protocol-stack-evidence.md) for full protocol details, architecture patterns, and source extraction.