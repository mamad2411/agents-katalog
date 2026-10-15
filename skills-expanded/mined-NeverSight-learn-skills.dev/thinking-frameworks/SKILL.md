---
name: thinking-frameworks
description: >
  Multi-agent thinking frameworks for rigorous problem-solving and decision-making.
  Contains Dialectical (thesis-antithesis-synthesis), Six Thinking Hats (parallel
  perspectives), First Principles (strip to fundamentals), and Composition Patterns
  chaining frameworks together. Use whenever the user needs to evaluate competing
  approaches, make architecture decisions, challenge assumptions, modernize legacy
  systems, write RFP responses, run post-mortems, compare technologies, or do any
  multi-perspective analysis. Triggers on "think this through", "pros and cons",
  "tradeoffs", "should we use X or Y", "devil's advocate", "argue both sides",
  "from all angles", "what are we missing", "first principles", "rethink this",
  "why do we do it this way", "brainstorm", "go/no-go", "use dialectical",
  "run six hats", or any thinking framework reference.
---

# Thinking Frameworks for Agent Teams

## Overview

This skill implements structured thinking methodologies as multi-agent teams.
Each framework decomposes into specialized agent roles that produce stronger
outputs through cognitive diversity and structured tension.

**Four frameworks, five composition patterns, and a triage system.**

## Quick Selection: Which Framework?

Read this table first. Pick the framework, then read its reference file.

| Situation | Framework | Reference File |
|-----------|-----------|---------------|
| "Should we use X or Y?" | **Dialectical** | `references/dialectical.md` |
| "Evaluate this from every angle" | **Six Hats** | `references/six-hats.md` |
| "Why do we do it this way?" | **First Principles** | `references/first-principles.md` |
| "We're stuck, need a breakthrough" | **Collision-Zone** | (existing skill) |
| Complex multi-phase analysis | **Composition Pattern** | `references/composition-patterns.md` |
| "I don't know which framework to use" | **Cynefin Triage** | `references/composition-patterns.md` (Pattern 4) |

### Decision Logic

```
Is there a clear binary choice (X vs Y)?
  YES → Dialectical (3 agents: Advocate → Challenger → Integrator)

Do we need comprehensive, multi-stakeholder analysis?
  YES → Six Hats (7 agents: Blue orchestrator + 6 perspective agents)

Are we questioning inherited complexity or assumptions?
  YES → First Principles (3 agents: Archaeologist → Architect → Evaluator)

Are we stuck and need a creative breakthrough?
  YES → Collision-Zone (existing skill)

Is the problem too complex for a single framework?
  YES → Read composition-patterns.md for multi-framework orchestration

Not sure what we're dealing with?
  → Use the Cynefin Classifier (Pattern 4 in composition-patterns.md)
```

## Framework Summaries

### Dialectical Thinking (3 Agents)
**Core idea:** Truth emerges from structured intellectual conflict.

- **Advocate** builds the strongest case FOR a position
- **Challenger** systematically dismantles it and proposes an alternative
- **Integrator** transcends both into something stronger than either

Best for: binary decisions, architecture debates, RFP responses, technology selection.
Cycle time: fast (3 sequential agent calls).

**Read `references/dialectical.md` for the full process, output formats, and agent prompts.**

### Six Thinking Hats (7 Agents)
**Core idea:** Parallel thinking beats adversarial thinking for comprehensive coverage.

Six cognitive modes, each worn one at a time:
- 🔵 **Blue** (Process) — orchestrates the sequence, synthesizes results
- ⚪ **White** (Facts) — data, information gaps, confidence levels
- 🔴 **Red** (Intuition) — feelings, hunches, stakeholder sentiment
- ⬛ **Black** (Caution) — risks, failure modes, compliance gaps
- 🟡 **Yellow** (Optimism) — benefits, value, strategic positioning
- 🟢 **Green** (Creativity) — alternatives, wild cards, assumption challenges

Best for: go/no-go decisions, post-mortems, cross-functional analysis, project evaluation.
Cycle time: medium (7 sequential agent calls, some parallelizable).

**Read `references/six-hats.md` for hat sequences, output formats, and agent prompts.**

### First Principles Decomposition (3 Agents)
**Core idea:** Most complexity is inherited, not necessary. Strip to fundamentals, rebuild.

- **Archaeologist** digs through assumption layers to find bedrock truths
- **Architect** builds from ONLY those truths (never sees the original system)
- **Evaluator** compares the reconstruction against the original

The information barrier is critical: the Architect must never see the current
implementation. This prevents anchoring bias.

Best for: legacy modernization, architecture simplification, challenging "best practices."
Cycle time: medium (3 sequential, deep-thinking agent calls).

**Read `references/first-principles.md` for the full process, domain-specific patterns, and agent prompts.**

## Composition Patterns (Multi-Framework)

When a single framework isn't enough, composition patterns chain them together
with defined data flows and information barriers.

| Pattern | Sequence | Use When |
|---------|----------|----------|
| Decompose → Debate → Decide | FP → Dialectical → Six Hats | Legacy modernization |
| Collide → Ground → Validate | Collision → FP → Six Hats | Innovation under constraints |
| Assess → Explore → Commit | Six Hats → Dialectical (recursive) | Complex multi-stakeholder |
| Triage → Route → Execute | Cynefin → [auto-selected] | Don't know which framework |
| Parallel Perspectives | Dialectical (×N) → Six Hats | Comparing 3+ options fairly |

**Read `references/composition-patterns.md` for complete orchestration specs, data flow
rules, information barriers, and anti-patterns.**

## Claude Code Implementation

### Spawning Agent Teams with Task

Each agent in a framework runs as a Claude Code `Task` (subagent). The orchestration
pattern is always:

1. Load the relevant reference file for agent prompts
2. Spawn each agent sequentially, passing outputs forward
3. Enforce information barriers (some agents must NOT see certain data)
4. Final agent produces the recommendation

### Basic Task Pattern

```python
# Dialectical example
thesis = Task(
    prompt=f"{advocate_prompt}\n\nPROBLEM: {problem}",
    description="Dialectical: Build thesis"
)

antithesis = Task(
    prompt=f"{challenger_prompt}\n\nTHESIS:\n{thesis}",
    description="Dialectical: Challenge thesis"
)

synthesis = Task(
    prompt=f"{integrator_prompt}\n\nTHESIS:\n{thesis}\n\nANTITHESIS:\n{antithesis}",
    description="Dialectical: Synthesize"
)
```

### CLAUDE.md Integration

Add this block to any project's CLAUDE.md to enable thinking framework agent teams:

```markdown
## Thinking Frameworks

For complex decisions, use the thinking-frameworks skill:
- "Use dialectical analysis for [problem]" → Advocate → Challenger → Integrator
- "Run six hats on [problem]" → Blue orchestrates 6 perspective agents
- "Apply first principles to [problem]" → Archaeologist → Architect → Evaluator
- For multi-framework: read composition-patterns.md and select a pattern
```

### Context Management Rules

Each agent should receive:
1. Its role-specific system prompt (from the framework's reference file)
2. The problem statement
3. Outputs from previous agents in the chain
4. Optional domain context (project docs, policies, technical specs)

**Keep agent context intentionally focused.** What an agent CANNOT see is as important
as what it can see. The reference files specify information barriers for each framework.

## Practical Applications

| Application | Recommended Approach |
|------------|---------------------|
| Architecture Decision Records | Dialectical per ADR |
| Security & Compliance Planning | Six Hats: White→Black→Yellow→Green→Red |
| Legacy Modernization | Composition: Decompose → Debate → Decide |
| Incident Post-Mortems | Six Hats (Post-Mortem sequence) |
| Vendor Evaluation | Composition: Parallel Perspectives → Convergence |
| Challenging "Best Practices" | First Principles with domain-specific patterns |
| Innovation Under Constraint | Composition: Collide → Ground → Validate |

## Reference Files

Read the appropriate reference file BEFORE building agent prompts:

| File | Contents | When to Read |
|------|----------|-------------|
| `references/dialectical.md` | Full process, output templates, 3 agent prompts | Binary decisions, debates |
| `references/six-hats.md` | Hat details, sequences, 7 agent prompts | Comprehensive analysis |
| `references/first-principles.md` | Decomposition method, domain patterns, 3 agent prompts | Assumption challenging |
| `references/composition-patterns.md` | 5 patterns, data flows, barriers, anti-patterns, Cynefin classifier | Multi-framework orchestration |

## Red Flags That a Thinking Framework Is Needed

- "We've already decided" → Dialectical (challenge the decision)
- "Everyone agrees" → Six Hats (find what's missing)
- "That's how it's always been done" → First Principles (strip assumptions)
- "We've tried everything" → Collision-Zone (force novel connections)
- "It's too complex to change" → First Principles (separate necessary from inherited)
- "I don't know where to start" → Cynefin Triage (classify, then route)
