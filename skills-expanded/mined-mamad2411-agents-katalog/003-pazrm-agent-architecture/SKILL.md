---
name: 003-pazrm-agent-architecture
description: 003-pazrm-agent-architecture
---

# 003-pazrm-agent-architecture

This skill defines the autonomous behavior, system prompt, and capabilities for the agent **003-pazrm-agent-architecture**.

## Source Location
Originally discovered in Rick's Downloads at: `/Users/kalivibecoding/Downloads/zaraOS/docs/ADRs/003-pazrm-agent-architecture.md`

## 🧠 Master Agent Prompt & Capabilities

# ADR-003: PAZRM Agent Architecture

**Date:** 2026-05-31
**Status:** Accepted
**Deciders:** Dr. Jessica Edwards, Rick Jefferson

## Context

Zara OS is differentiated by AI agents that automate administrative and clinical-adjacent workflows. We must decide:
1. How many agents
2. What each does
3. How they coordinate
4. How they stay safe

Single monolithic agent fails because (a) clinical safety requires specialized guardrails per domain, (b) different workflows need different latency/cost profiles, (c) auditability requires clear scope per agent.

## Decision

Five specialist agents, orchestrated by a Conductor, operating under shared safety + audit infrastructure.

| Agent | Letter | Role |
|---|---|---|
| Post-Visit Autopilot | P | Auto-creates orders, referrals, letters, billing rows, follow-ups |
| AI Scribe Converter | A | Ambient transcription → SOAP note → coding suggestions |
| Zara Clinical Assistant | Z | Chart summary, med/allergy checks, care-gap alerts |
| Referral Specialist | R | Detects need, assembles packet, routes, tracks closure |
| Medical Super Knowledge | M | Semantic search across notes/forms/transcripts with citations |

**Conductor:** LangGraph state machine routes work items to agents based on (a) explicit user request, (b) workflow trigger (e.g., encounter close → P), (c) agent-to-agent delegation.

**Shared infrastructure:**
- Audit trail (every action logged immutably)
- Memory stack (working, episodic, semantic, procedural per @rj/memory)
- Tool registry (MCP-compliant tool definitions)
- Safety layer (per ADR-008)

**Per-agent:**
- Distinct LLM (Sonnet for most, Opus for complex reasoning in P and Z)
- Distinct tool subset
- Distinct safety guardrails
- Distinct evaluation metrics

## Consequences

**Positive:**
- Clear boundaries make safety auditable
- Each agent can be improved independently
- Easier to certify under ONC HTI-1 (b)(11) Decision Support Intervention
- Failure of one agent doesn't cascade

**Negative:**
- More moving parts than monolith
- Conductor becomes a critical path component
- Agent-to-agent communication needs careful state management

**Risk mitigation:**
- Conductor is stateless (state in LangGraph checkpoints, not in memory)
- Each agent has a "kill switch" feature flag in KV
- All agent prompts versioned in `apps/agents/*/prompts/`

## Alternatives Considered

| Option | Why rejected |
|---|---|
| Single monolithic agent | Safety + auditability nightmare |
| Three agents (scribe + autopilot + assistant) | Misses referral and knowledge gaps |
| Seven+ agents | Premature decomposition |
| No agents, classic SaaS | Defeats the entire thesis |

## References

- LangGraph: https://langchain-ai.github.io/langgraph/
- CrewAI: https://www.crewai.com/
- MCP: https://modelcontextprotocol.io/
- ONC HTI-1 DSI: https://www.healthit.gov/topic/laws-regulation-and-policy/health-data-technology-and-interoperability-certification-program

