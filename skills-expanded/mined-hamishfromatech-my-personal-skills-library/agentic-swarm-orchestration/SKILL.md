---
name: agentic-swarm-orchestration
description: Design, deploy, and govern autonomous agent swarms for complex multi-step workflows. Use when building multi-agent systems, coordinating parallel AI agents, or scaling beyond single-agent architectures into swarms that mirror real engineering teams. NOT for simple sequential chains or single-task automations.
---

# Agentic Swarm Orchestration

## Overview
Multi-agent systems that mirror real engineering teams can cut debug time by 93% and compress cross-team delivery timelines. This skill operationalizes swarm intelligence for A-Tech products — from composed platform agents to autonomous marketplaces — with governance guardrails, reputation-weighted consensus, and bounded autonomy.

## When to Use
- Building systems with 3+ specialized agents that must collaborate
- Scaling from single-agent automation to team-like orchestration
- Designing fault-tolerant workflows where no single agent is a bottleneck
- Creating emergent intelligence greater than individual agent capability
- NOT for: simple sequential prompt chains, single-task wrappers, or proof-of-concepts without scaling intent

## Core Process / Workflow

### 1. Swarm Topology Selection
Choose the coordination pattern that matches your problem structure:

| Pattern | Structure | Best For | A-Tech Example |
|---|---|---|---|
| Hierarchical | Leader delegates to workers | Complex decomposition | Builder's Club incident commander |
| Mesh / Gossip | Peer-to-peer messaging | Fault tolerance, consensus | Multi-region deployment agents |
| Pipeline | Sequential handoffs | Deterministic workflows | Be Practical chapter generation |
| Market / Auction | Bidding for tasks | Resource optimization | A-Coder model selection router |
| Swarm / Foraging | Stochastic exploration | Search & discovery | Builder's Club contributor matching |

### 2. Agent Specialization Design
Define 3–6 agent roles with non-overlapping responsibilities:

1. **Orchestrator Agent** — Task decomposition, progress tracking, deadlock resolution
2. **Domain Specialist Agents** — Deep expertise in narrow areas (security, UX, data)
3. **Verifier / Critic Agent** — Output validation, consistency checks, edge case hunting
4. **Memory / Context Agent** — Shared state management, historical pattern retrieval
5. **Interface Agent** — Human communication, status reporting, escalation
6. **Meta-Agent** — Swarm health monitoring, topology adaptation, resource reallocation

### 3. Communication Protocol Layer
Standardize inter-agent messages using the A2A (Agent-to-Agent) pattern:

```json
{
  "message_type": "TASK_ASSIGNMENT | RESULT | QUERY | NEGOTIATE | ESCALATE",
  "sender_id": "agent-uuid",
  "receiver_id": "agent-uuid | BROADCAST",
  "payload": { /* domain-specific */ },
  "priority": 1-5,
  "ttl_seconds": 300,
  "requires_ack": true,
  "provenance_chain": ["prev-msg-uuid", "..."]
}
```

- All messages carry provenance for auditability
- Broadcast only for swarm-wide signals (consensus, termination)
- Negotiation messages enable auction-based task assignment

### 4. Consensus & Conflict Resolution
Implement weighted voting for decisions requiring agreement:

```python
def weighted_consensus(proposals, agents):
    """
    proposals: list of {content, proposer_id}
    agents: list of {id, reputation_score, expertise_vector}
    """
    scores = defaultdict(float)
    for p in proposals:
        for a in agents:
            similarity = cosine_similarity(a.expertise_vector, p.topic_vector)
            scores[p.content] += a.reputation_score * similarity
    return max(scores, key=scores.get)
```

- Tie-breaking falls to the agent with highest domain reputation
- Persistent disagreements escalate to human review via Interface Agent

### 5. Bounded Autonomy Governance
Establish autonomy levels per agent and per task type:

| Level | Description | Requires Human | Example |
|---|---|---|---|
| L0 — Fully Supervised | Every action approved | Yes, per action | Production deployments |
| L1 — Checkpoint Gates | Key milestones approved | Yes, per gate | Architecture changes |
| L2 — Budget-Limited | Autonomous within constraints | Only on budget breach | Token spending, API calls |
| L3 — Monitored | Fully autonomous, logged | Only on anomaly alert | Content generation, testing |
| L4 — Sovereign | Independent operation | No | Internal documentation, monitoring |

- Agents self-report their current autonomy level in every message
- Escalation triggers: confidence below threshold, novelty above threshold, safety-critical flag

### 6. Reputation & Incentive Loop
Track and evolve agent reputation using on-chain or verifiable off-chain records:

- **Reliability Score** — task completion rate × timeliness
- **Quality Score** — peer review ratings × verification pass rate
- **Collaboration Score** — responsiveness to queries × helpfulness ratings
- **Reputation Decay** — old contributions fade; recent behavior matters more

Portability: Reputation binds to verifiable credentials (see `agent-reputation-identity-framework`) enabling cross-platform reputation.

### 7. Failure Modes & Recovery
Build resilience into swarm topology:

| Failure | Detection | Recovery |
|---|---|---|
| Single agent crash | Heartbeat timeout | Redundant agent activation, state replay |
| Consensus deadlock | Timer + cycle detection | Escalation to meta-agent, random tie-break |
| Cascading error | Error rate threshold | Circuit breaker, partial rollback, human alert |
| Poisoned message | Signature validation | Quarantine agent, reputation penalty |
| Reward hacking | Outcome divergence | Cross-verification, ground-truth injection |

### 8. Measurement Framework

| Metric | Target | Measurement |
|---|---|---|
| Swarm throughput | Tasks/hour | Completed tasks / wall-clock time |
| Coordination overhead | <15% of total time | Message volume / task complexity |
| Fault recovery time | <30 seconds | Detection → restored throughput |
| Consensus accuracy | >90% | Correct decisions / total decisions |
| Human escalation rate | <5% | Escalated tasks / total tasks |
| Emergence score | New capability emerges | Qualitative: did swarm solve novel problem? |

## References
- See [references/swarm-frameworks-comparison.md](references/swarm-frameworks-comparison.md) for LangChain, Swarms Corporation, CrewAI, and AutoGen patterns.
- See [references/a2a-protocol-extraction.md](references/a2a-protocol-extraction.md) for Google's A2A specification and interoperability patterns.
- See `agent-reputation-identity-framework` for verifiable agent identity and cross-platform reputation.
- See `agentic-payments-protocol-ap2` for swarm-internal micropayments and agent-to-agent billing.
- See `agentic-platform-composed-systems` for platform engineering swarms and DevEx agent design.