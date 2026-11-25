---
name: agentic-coding-prior-ai-exposure-moderation
description: Applies the first longitudinal causal study isolating how prior AI IDE exposure moderates the impact of adopting autonomous coding agents on velocity and quality. Use when designing agentic coding rollout strategies, evaluating when agents help vs harm, or deciding whether to introduce agents to teams already using AI assistants.
---

# Agentic Coding Prior AI Exposure Moderation

## Overview
The first causal evidence that autonomous coding agents deliver large velocity gains ONLY when they are a project's first AI tool; teams already using AI IDEs see minimal velocity benefits but equivalent quality degradation — a critical finding for rollout strategy.

## When to Use
- Designing phased agentic coding adoption across teams with varying AI maturity
- Evaluating whether to introduce autonomous agents to teams already using Copilot/Cursor
- Assessing the speed-maintainability trade-off when planning agent deployment
- NOT for individual developer productivity optimization
- NOT for model selection or benchmark comparison

## Core Process / Workflow

### 1. Assess Prior AI Exposure
Before introducing autonomous coding agents, audit existing AI tool usage:
- IDE-based assistants in use (Copilot, Cursor, Windsurf)
- Configuration artifacts in repositories (`.github/copilot`, `.cursor/`, etc.)
- Team self-reported AI familiarity and workflow integration depth

### 2. Predict Expected Impact Using the Exposure-Moderation Framework

| Scenario | Velocity Impact | Quality Impact | Recommendation |
|----------|----------------|----------------|----------------|
| Agent-first (no prior AI IDE) | +36% commits, +77% lines (large, front-loaded) | +18% warnings, +39% complexity (persistent) | Introduce with quality safeguards |
| IDE-first (prior AI IDE use) | +3% commits, -6% lines (minimal, short-lived) | +19% warnings, +43% complexity (persistent) | Deploy selectively; expect coordination overhead |

### 3. Deploy Quality Safeguards
Regardless of prior exposure, agent adoption persistently increases:
- Static-analysis warnings (~18% across both groups)
- Cognitive complexity (~39% across both groups, growing over time)

Required safeguards:
- Complexity-aware review of agent pull requests
- Routine refactoring scheduled after agent contributions
- Comprehensive automated test suites gating agent PRs
- Provenance tracking for all agent-generated changes
- Human oversight emphasis in review practices

### 4. Selective Deployment Strategy
For IDE-first teams, deploy agents for:
- Tightly scoped tasks with clear acceptance criteria
- New modules where coordination overhead is lower
- Exploratory/prototype work where maintainability is secondary

Avoid deploying agents for:
- Core architectural changes in mature, AI-saturated codebases
- Tasks requiring deep cross-file coordination in active repos
- High-stakes refactoring where complexity debt compounds

## Key Evidence
- Study: Agarwal, He & Vasilescu (CMU, MSR '26, arXiv:2601.13597v2)
- Method: Staggered difference-in-differences with matched controls on AIDev dataset
- 401 agent-first repos matched to 606 controls; 117 IDE-first matched to 73
- Quality metrics via SonarQube: warnings, cognitive complexity, duplication, comment density
- Replication package: github.com/shyamagarwal13/agentic-coding-impact

## A-Tech Alignment
- Open-source: findings apply to Cline/OpenCode and open-weight agent frameworks
- Data privacy: on-device/local-first agent deployment preserves privacy
- Financial freedom: prevents wasted investment on agents in AI-saturated contexts
- Practical implementation: immediately actionable deployment framework with exposure audit

## References
- See [references/evidence-base.md](references/evidence-base.md) for full statistical results, dynamic treatment effects, and comparison with prior Cursor IDE study.