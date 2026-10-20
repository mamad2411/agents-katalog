---
name: assistant-to-agent-brownfield-onboarding
description: Applies the first controlled comparison of IDE-integrated assistants vs LLM-based agents during brownfield onboarding (Appelt & Glauben, PACIS 2026) to design agent adoption strategies that balance productivity gains against human agency risks. Use when introducing agentic coding tools to existing developer teams, measuring the shift from active collaboration to passive supervision, or designing guardrails against over-reliance and skill erosion.
---

# Assistant-to-Agent Brownfield Onboarding

## Overview
The first controlled experiment comparing an IDE-integrated assistant (GitHub Copilot Ask) with an LLM-based agent (GitHub Copilot Agent) during brownfield onboarding found agents cut task completion time by 61.7% and workload by 57.4% — but interaction data revealed a shift from active collaboration to passive supervision, raising over-reliance and skill-erosion concerns.

## When to Use
- Introducing agentic coding tools to an existing developer team (brownfield, not greenfield)
- Measuring the productivity-vs-agency tradeoff when upgrading from copilot to agent
- Designing guardrails against passive supervision and over-reliance
- Evaluating whether to deploy agents for onboarding/new-hire tasks
- Comparing assistant vs agent interaction patterns using the SPACE framework
- NOT for greenfield/new-project tasks (the study is specifically about brownfield onboarding)
- NOT for evaluating agent-only workflows without a copilot comparison baseline

## Core Process / Workflow

### 1. The Study Design

**Source:** Appelt & Glauben, Technical University Darmstadt, PACIS 2026 (PACIS2026-1974)

- 24 developers in a controlled experiment
- Task: brownfield onboarding (working with an existing codebase)
- Two conditions:
  - **Assistant:** GitHub Copilot Ask (IDE-integrated, conversational help)
  - **Agent:** GitHub Copilot Agent (autonomous, edits code directly)
- Measurement: SPACE framework (productivity, workload, interaction patterns, prompt behavior)

### 2. The Headline Results

```
Metric                          Copilot Agent vs Copilot Ask
─────────────────────────────────────────────────────────
Task completion time            -61.7%  (agent is 61.7% faster)
NASA-TLX workload               -57.4%  (agent reduces workload by 57.4%)
Code correctness                No significant improvement
Interaction pattern             Active collaboration → Passive supervision
```

**The paradox:** Massive productivity and workload gains, but code correctness did not improve. The agent does the work faster with less effort, but not better.

### 3. The Shift from Active Collaboration to Passive Supervision

The most important finding is qualitative, not quantitative:

**With Copilot Ask (assistant):**
- Developer actively writes code
- Uses AI for suggestions, explanations, syntax help
- Remains in the loop: reviews, adapts, integrates
- Active collaboration pattern

**With Copilot Agent (agent):**
- Developer prompts and supervises
- Agent edits code directly
- Developer reviews the agent's output (rather than writing code)
- Shift to passive supervision pattern

**Why this matters:**
- Passive supervision reduces cognitive load (explains the 57.4% workload reduction)
- But passive supervision also reduces the developer's engagement with the code
- Over time, this pattern risks skill erosion: developers who supervise but do not write lose deep code comprehension
- The productivity gain is real; the agency cost is real

### 4. The Productivity-Agency Tradeoff Framework

```
         HIGH PRODUCTIVITY
              ↑
              │
    Agent ────┼──── Optimal Zone
    (fast,    │    (high productivity,
     passive) │     active engagement)
              │
    ──────────┼──────────────→ HIGH AGENCY
              │
    Low       │    Assistant
    effort,   │    (slower,
    low value │     active)
              │
         LOW PRODUCTIVITY
```

**The challenge:** Move from "Agent" (high productivity, passive) to "Optimal Zone" (high productivity, active engagement) without sacrificing the 61.7% time savings.

### 5. Designing Guardrails Against Passive Supervision

```markdown
## Agent Adoption Guardrails

### 1. Maintain Writing Requirement
- Require developers to write at least one component manually per agent-assisted task
- Use the agent for scaffolding, not for complete implementation
- Pattern: "Agent drafts → Developer reviews and modifies → Agent refines"

### 2. Comprehension Checkpoints
- After agent completes a task, ask the developer to explain what the agent did
- Use Bloom's Taxonomy: can they recall, understand, analyze the generated code?
- If they cannot explain it, require manual review before accepting

### 3. Progressive Agent Autonomy
- Week 1: Agent suggests, developer applies all changes
- Week 2: Agent applies with per-file approval
- Week 3: Agent applies with bulk approval
- Week 4: Full agent autonomy (only if comprehension checks pass)

### 4. Alternate Agent and Assistant Use
- Use agents for boilerplate, tests, documentation (low-comprehension-risk tasks)
- Use assistants for core logic, algorithms, business rules (high-comprehension-risk tasks)
- The interaction type should match the task's comprehension requirements

### 5. Skill Maintenance Protocol
- Periodic "no-agent" sessions to maintain manual coding skills
- Code review without agent assistance to maintain critical evaluation
- Pair programming sessions to maintain collaborative coding patterns
```

### 6. The SPACE Framework Application

The study uses the SPACE framework to measure outcomes:

| SPACE Dimension | Copilot Ask (Assistant) | Copilot Agent (Agent) | Implication |
|-----------------|-------------------------|----------------------|-------------|
| Satisfaction & well-being | Lower (more effort) | Higher (less effort) | Agent improves perceived experience |
| Performance | Slower | 61.7% faster | Agent delivers measurable speed |
| Activity | Active coding | Passive supervision | Agent shifts activity pattern |
| Communication & collaboration | Active AI dialogue | Supervisory prompts | Agent reduces collaboration depth |
| Efficiency & flow | Moderate | Higher (less interruption) | Agent preserves flow but reduces engagement |

### 7. Brownfield Onboarding-Specific Findings

This study is specifically about **brownfield onboarding** — working with an existing, unfamiliar codebase. This is the most common real-world scenario for new hires and team transfers.

**Why brownfield matters for agent adoption:**
- Greenfield (new projects): developers build mental models from scratch — agents can scaffold without harming comprehension
- Brownfield (existing code): developers must understand existing code — agents that write code for them may prevent mental model formation

**The risk for new hires:**
- New hires using agents for brownfield onboarding may complete tasks faster
- But they may not develop the deep codebase understanding that experienced developers have
- This creates a comprehension debt that surfaces later when debugging or extending

### 8. Interaction Pattern Taxonomy

| Pattern | Description | Comprehension Risk |
|---------|-------------|-------------------|
| Active collaboration | Developer writes, AI suggests | Low |
| Guided generation | Developer specifies, AI implements | Medium |
| Supervised generation | Developer prompts, agent implements, developer reviews | High |
| Passive supervision | Developer prompts, agent implements, developer accepts | Very high |
| Full autonomy | Developer delegates, agent completes without review | Extreme |

The study found that Copilot Agent use shifted developers from "Active collaboration" to "Supervised generation" or "Passive supervision" — moving right on this taxonomy.

## References
- See [references/brownfield-onboarding-evidence-base.md](references/brownfield-onboarding-evidence-base.md) for full evidence: study design, statistical results, SPACE framework analysis, interaction pattern taxonomy, comparison with adjacent research, and A-Tech alignment analysis.