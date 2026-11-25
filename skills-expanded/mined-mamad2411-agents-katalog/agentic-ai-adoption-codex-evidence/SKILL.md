---
name: agentic-ai-adoption-codex-evidence
description: Applies large-scale empirical evidence on agentic AI adoption patterns from OpenAI's Codex usage data (5× user growth in 6 months of 2026, 99.8% of OpenAI worker tokens on Codex) to inform product strategy, workforce planning, and workflow design. Use when planning agentic AI product rollout, estimating adoption curves, designing parallel agent workflows, measuring task complexity growth, or building skill/plugin ecosystems for agentic tools.
---

# Agentic AI Adoption: Evidence from Codex

## Overview

The first large-scale analysis of agentic AI adoption and use patterns, based on OpenAI Codex usage data across individual, organizational, and internal OpenAI populations. Reveals that agentic AI is rapidly replacing conversational AI for work, that intensive users organize around parallel agent workflows, and that task complexity is growing 10×. Based on Johnston, Holtz, Martin et al. (OpenAI/Columbia/Wharton/Duke, arXiv:2606.26959, June 2026).

## When to Use

- Planning agentic AI product rollout and adoption strategy
- Estimating adoption curves across different organizational populations
- Designing parallel agent workflow systems and concurrency management
- Measuring task complexity growth over time
- Building skill/plugin ecosystems for agentic tools
- Forecasting workforce restructuring from conversational to agentic AI
- Designing tiered SLOs for agentic vs conversational users
- NOT for evaluating specific model capabilities (this is adoption/usage data)
- NOT for small-scale or individual developer tooling decisions

## Core Process / Workflow

### 1. Calibrate Adoption Expectations by Population

Agentic AI adoption is rapid but highly uneven across populations:

| Population | Codex Active Users (28-day) | Codex Share of Output Tokens | Key Characteristic |
|---|---|---|---|
| Individual users | <1% | 16.5% | Small adoption, intensive users |
| Organizational users | 17.3% | 63.3% | Broader adoption, majority of tokens |
| OpenAI workers | ~100% | 99.8% | Near-universal, replaced ChatGPT |

**Pattern**: Technical roles adopt first, non-developer roles follow. Within OpenAI, engineers reached >90% Codex share by March 2026; legal/recruiting reached 75% by April 2026 (rapid catch-up after initial lag).

**Implication**: Adoption depends on context (file access, management expectations, workforce skills, review processes), not just model capability. Plan for organizational complements, not just tool deployment.

### 2. Track the Four Stylized Facts of Agentic AI Shift

**Fact 1 — Rapid but uneven shift**: 5× weekly active user growth in H1 2026. Smallest among individuals, largest among OpenAI workers. Measure by output tokens, not active users — intensive users dominate.

**Fact 2 — Delegated production, not consultation**: Users ask Codex to *do work* (debug, refactor, validate, configure, draft, analyze), not just provide advice. This contrasts with conversational AI usage where "asking" dominated.

**Fact 3 — Anchored in software but broadening**: Largest share is software work (implementation, understanding, validation, operations, management), but deepest adoption contexts extend to research, planning, communication, data analysis, recruiting, sales.

**Fact 4 — Intensive users organize around parallel workflows**: >10% of users manage 3+ concurrent agents weekly; 26.6% use skills. Intensive users shift from "assistant answering requests" to "workflow system where user delegates, monitors, reviews, coordinates."

### 3. Measure Task Complexity Growth

Task complexity (estimated human completion time) is increasing rapidly:

| Threshold | Dec 2025 | May 2026 | Growth |
|---|---|---|---|
| ≥1 hour tasks | 35.4% of users | 70.2% | ~2× |
| ≥8 hour tasks | 2.1% of users | 25.6% | **~10×** |

**Pattern**: First turn of a thread is >2× more likely to be the most complex task. Users delegate the broadest work initially, then refine with narrower requests.

**Implication**: Capacity planning must account for rapidly increasing per-task compute. Sizing based on early adoption data will underestimate future load.

### 4. Design for Parallel Agent Workflows

Concurrency patterns by population:

| Population | No Concurrent Turns | 5+ Concurrent Agents |
|---|---|---|
| Individual | 63.9% | rare |
| Organizational | 67.4% | rare |
| **OpenAI workers** | **10.7%** | **28.6%** |

**Long-running agents** (cumulative daily runtime):
- Median OpenAI employee: 2.5 hours/day of agent runtime
- P99 OpenAI employee: 71 hours/day (implies multiple concurrent agents running continuously)
- P99 grew 88% since April 2026
- External users: substantially lower, but upper tail growing (Org +25%, Individual +50%)

**Implication**: As adoption deepens, users shift to managing portfolios of parallel agentic work. Design for delegation, supervision, and coordination — not single-threaded assistance.

### 5. Build Skill/Plugin Ecosystems

Skill use is growing and differentiates adoption depth:

| Skill Source | What It Is | Individual % | Org % | OpenAI % |
|---|---|---|---|---|
| Preinstalled | Bundled capabilities | — | — | — |
| Curated | OpenAI-distributed standalone | — | — | — |
| Plugin | Bundled in plugin + app integrations | lower | medium | highest |
| Custom plugin | Recognized plugin, non-catalog | lower | medium | highest |
| Custom | User/org-specific workflows | lowest | medium | highest |

**Overall skill use**:
- Individual: 25.7% of active users
- Organizational: 30.4%
- OpenAI: 96.2%
- Growth: 5.4% (March 1) → 26.6% (June 11) — 5× in 3 months

**Key insight**: Custom skills are most valuable in high-context organizational environments where repeated tasks depend on organization-specific context, shared conventions, internal procedures. This is where the largest differentiation occurs.

### 6. Workforce Restructuring Implications

As AI shifts from consultation to delegation:

- Jobs increasingly involve directing, monitoring, integrating agent outputs
- Team composition, hiring needs, career ladders may shift
- Senior workers use agentic tools for planning, review, delegation (not just implementation)
- Non-technical roles adopt rapidly once frictions removed (legal went 0→75% in ~3 months at OpenAI)
- Output tokens growing 10×+ across all job functions at frontier (median legal worker: 13× more tokens June vs Nov 2025; median researcher: 50×)

**Measurement shift needed**: Active users, chats, message volume become less informative. Track: delegated task complexity, runtime, workflow reuse, concurrency, production output.

### 7. Product Strategy Patterns

**For agentic AI products**:
1. Optimize for delegated production, not consultation
2. Build concurrency as a first-class feature (threads as independent workspaces)
3. Invest in skill/plugin ecosystem early — it's the systematization layer
4. Measure output tokens, not just active users
5. Plan for rapidly increasing task complexity
6. Design for the shift from "assistant" to "workflow system"

**For organizational rollout**:
1. Technical roles first, then non-technical (expect 3-6 month lag)
2. Management expectations + training + review processes are the binding constraints
3. Custom skills encode organizational context — this is the moat
4. Senior workers adopt for planning/review, not just implementation

## References

- See [references/codex-adoption-evidence-base.md](references/codex-adoption-evidence-base.md) for full adoption data, task taxonomy, complexity metrics, and population comparisons.