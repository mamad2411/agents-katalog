---
name: mcp-dual-identity-problem
description: Design SaaS products for the dual-identity problem — when both human users and AI agents consume the same product through MCP servers. Covers agent-vs-human traffic asymmetry (10-100x load), identity attribution, rate-limit governance, cost attribution, and the hybrid pricing transition. Use when designing MCP-enabled SaaS products, building agent identity models, setting rate limits for agent traffic, or architecting per-agent cost attribution and audit trails.
---

# MCP Dual-Identity Problem

## Overview

When a SaaS product exposes an MCP server, it gains a second consumer: the AI agent acting on behalf of a human user. Agents and humans have radically different traffic patterns, cost profiles, and rate-limit needs. Human-paced pricing models (per-seat, flat subscription) break under agent traffic because agents can make 500 tool calls in 10 seconds while a human makes 50-200 actions per day. This skill provides the design framework for products that serve two personas — human and agent — simultaneously.

## When to Use

- Designing an MCP server for an existing SaaS product
- Building agent identity, authentication, and attribution systems
- Setting rate limits that distinguish agent traffic from human traffic
- Architecting per-agent, per-tool, per-workflow cost attribution
- Transitioning from per-seat pricing to hybrid agent-aware pricing
- Designing audit trails that separate human actions from agent actions
- Building MCP gateway infrastructure (auth, rate limiting, cost logging)

NOT for:
- Choosing MCP pricing models in the abstract (use mcp-server-monetization-2026)
- Gateway aggregation platform selection (use mcp-gateway-monetization)
- General agent interoperability protocols (use agent-protocol-stack-2026)

## Core Process / Workflow

### Step 1: Understand the Traffic Asymmetry

The fundamental problem is that agent traffic scales with task complexity, not user count.

| Dimension | Human User | AI Agent |
|---|---|---|
| **Actions per day** | 50-200 | 500+ in seconds |
| **Traffic pattern** | Steady, session-paced | Bursty, task-complexity-driven |
| **Integration** | One-time, stable | Dynamic discovery, single-use, forget |
| **Customer relationship** | One company, one contract | Agent acts for person, team, or another agent |
| **Rate-limit impact** | Individual | One agent can throttle an entire team |

**Key insight:** The same infrastructure bears the same database queries, compute, and egress — but 10x to 100x the load. The bill lands somewhere.

### Step 2: Design the Dual-Identity Model

Answer four design questions before writing code:

1. **Does the product treat agent actions as the user's actions, or as separate?**
   - Merged identity: agent acts *as* the user. Simpler, but no attribution.
   - Separate identity: agent is a first-class non-human identity (NHI). More complex, but enables per-agent billing, rate limits, and audit.

2. **How is cost and usage attributed between human and agent?**
   - If merged: all usage rolls up to the human seat. Cannot distinguish agent-driven cost.
   - If separate: per-agent metering, per-tool cost, per-workflow attribution. Enables FinOps for agents.

3. **Can the system tell, from a single API call, whether a human or an agent triggered it?**
   - This is the minimum viable audit requirement.
   - If no, the audit trail is compromised and cost attribution is impossible.

4. **What happens when one agent's actions affect other users?**
   - The 3am scenario: one agent pulls 90 days of messages, blows through the team API rate limit, and four other employees can't use the product at 9am.
   - Design rate limits that are per-agent, not just per-team.

### Step 3: Transition Pricing from Per-Seat to Hybrid

Three pricing models are emerging for MCP-enabled products. The recommendation for 2026: start with usage-based per-call, design the contract to move to outcome-based later.

| Model | How It Works | Best When | Weakness |
|---|---|---|---|
| **Per-call (tool invocations)** | Charge per agent tool call | Value scales with call frequency | Rewards vendor for agent inefficiency (retries, loops) |
| **Re-wrapped seats** | Agent bundled into human seat add-on ($30-$150/user/mo) | Procurement familiarity, short-term revenue | Doesn't fix unit economics; one seat does the work of three |
| **Outcome-based** | Pay per successful job completion | Value tied to verifiable outcome | Defining and arbitrating the outcome is hard |

**Hybrid recommendation:** Base subscription (covers human + baseline agent usage) + variable usage component (per-call for agent traffic above threshold) + outcome component (for high-value verifiable results).

### Step 4: Build the MCP Gateway Layer

Underneath the MCP servers, a governance layer handles the messy parts. This is being built by Kong, Tyk, MintMCP, Arcade, TrueFoundry, and Microsoft (AI Gateway in Foundry).

**Gateway responsibilities:**
- Authentication (agent identity tokens vs human credentials)
- Rate limiting (per-agent, per-tool, per-workflow — not just per-account)
- Cost attribution (per-call, per-outcome, per-agent session)
- Audit logging (human vs agent action separation)
- Agent discovery and dynamic onboarding

**The PM measurement opportunity:** The gateway is where the data lives. Per-agent, per-tool, per-workflow cost. Per-call latency. Per-outcome success rates. The same data that lets a CISO sleep at night lets a PM answer: "What did our agents cost this month, by workflow, by outcome?" — the question their CFO has been asking for two years.

### Step 5: Design for the Dual-Persona Roadmap

Treat the agent as a second persona in product design:

- **Wireframes show the human user.** The agent is the missing persona.
- **Identity model supports both.** Human SSO + agent OAuth with NHI.
- **Rate limits are per-identity-type.** Human-paced defaults, agent-paced tiers.
- **Audit trails distinguish origin.** Every action tagged human or agent.
- **Pricing reflects both consumers.** Seat for human, usage for agent, outcome for value.
- **Documentation serves both.** Human docs for the user, machine-readable specs for the agent.

## The Mobile-First Analogy

This is the same kind of foundational design choice the industry made when mobile apps appeared. Some treated mobile as a thin wrapper. Some redesigned around mobile-first. The ones who redesigned won. The agent identity problem is the 2026 version of that fork.

## A-Tech Application

### A-Coder
- Expose an MCP server for agent-accessible features (codebase search, refactoring tools, test generation)
- Implement separate agent identity tokens (NHI) distinct from human user accounts
- Per-agent rate limits and cost attribution dashboards
- Hybrid pricing: human seat subscription + agent usage metering + outcome component (successful builds, resolved issues)

### Be Practical
- Module on "Designing Products for Agent Consumers" covering dual-identity, traffic asymmetry, and hybrid pricing
- Case study: how per-seat pricing breaks under agent traffic and how to fix it

### Builder's Club
- Workshop on building MCP gateway infrastructure
- Agent identity and FinOps for agents as a marketplace category opportunity
- Open-source agent cost attribution toolkit

## Cross-Skill Connections

- `mcp-server-monetization-2026` — The four pricing models (this skill adds the dual-identity design layer upstream of pricing)
- `mcp-gateway-monetization` — Gateway aggregation platforms (this skill adds the product-design and identity model)
- `agent-protocol-stack-2026` — Full protocol stack including MCP (this skill is the product-design consequence)
- `agentic-commerce-pricing-consolidation-2026` — Outcome-based pricing market validation (this skill explains why per-seat breaks)
- `hybrid-ai-pricing-architecture` — Hybrid pricing implementation (this skill explains the agent-traffic driver)
- `agent-reputation-identity-framework` — Agent identity and reputation (this skill extends to MCP dual-identity)
- `agentic-trust-security-protocols-2026` — Non-human identity security (this skill adds the product-design dimension)

## References

- See [references/dual-identity-design-framework.md](references/dual-identity-design-framework.md) for the full design questionnaire, gateway architecture patterns, and the mobile-first transition analogy.