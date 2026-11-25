---
name: code-health-mcp-integration
description: Integrate code quality and maintainability metrics into agentic coding workflows using MCP-based safeguards. Covers AI readiness assessment, pre-commit gates, refactoring loops, and AGENTS.md workflow orchestration. Use when setting up agentic coding teams, preventing AI-generated technical debt, or scaling AI-assisted engineering to production.
---

# Code Health MCP Integration

## Overview

Agentic AI coding delivers 2–3× speedups, but speed amplifies both good design and bad decisions. Studies show agents consume up to 50% more tokens on unhealthy code, and AI-generated code often mirrors the quality flaws of its training data. CodeScene's Code Health MCP Server (February 2026) demonstrated that embedding code quality metrics directly into the MCP tool layer transforms agentic speed into sustainable engineering outcomes.

This skill provides the operational patterns to make code health a first-class citizen in agentic workflows.

## When to Use

- Setting up agentic coding teams where long-term maintainability matters
- Preventing AI-generated code from compounding into architectural debt
- Scaling AI-assisted engineering from prototypes to production codebases
- Designing MCP tool ecosystems with quality guardrails
- NOT for throwaway prototypes or one-off experiments

## Core Insight: Agents Lack Objective "Good"

AI agents cannot reliably assess maintainability or change risk inside a real codebase. Three failure modes:

1. **Self-harm mode** — Agents write code they cannot reliably maintain later
2. **Spaghetti compliance** — Agents happily modify unhealthy code, producing unlikely-to-be-correct results
3. **Verification blindness** — Agents cannot objectively verify whether a refactoring improved or merely rearranged complexity

The solution: expose code health as measurable MCP tools that agents can query, act upon, and optimize for.

## The Six Patterns

### Pattern 1: Assess AI Readiness

Before assigning agents to a codebase, measure its health. Peer-reviewed research shows AI performs best on code with a Code Health score of at least 9.5 (ideally 10.0). Lower scores predict higher token burn, more errors, and fragile changes.

**Action:** Run a Code Health assessment on every module before agent assignment. Flag modules below 9.5 for human-led refactoring first.

```
Workflow: Assess → Flag → Refactor → Re-assess → Assign Agent
```

### Pattern 2: Safeguard Generated Code

AI code must be safeguarded at three MCP tool levels:

| Level | Tool | When It Runs |
|-------|------|--------------|
| Continuous | `code_health_review` | As each snippet is generated |
| Pre-commit | `pre_commit_code_health_safeguard` | On uncommitted/staged files |
| PR pre-flight | `analyze_change_set` | Full branch vs base ref check before PR |

When health regresses, the MCP tool kicks the agent into a refactoring loop automatically.

### Pattern 3: Refactor to Expand AI-Ready Surface

Legacy functions that are too large or complex for reliable AI work should be broken into smaller, cohesive units. Use the `code_health_review` → plan → refactor → re-measure workflow.

**Payoff:** Higher Code Health, clearer intent, larger surface where agents can operate safely.

### Pattern 4: Encode Principles in AGENTS.md

Individual MCP tools are not enough. Agents need workflow guidance to combine tools into coherent sequences.

**AGENTS.md contents:**
- Pull risk forward with `code_health_review`
- Safeguard changes via pre-commit and PR pre-flight checks
- Enter refactoring loops when health regresses

This turns engineering principles into executable guidance.

### Pattern 5: Use Coverage as Behavioral Guardrail

Strict coverage gates on Pull Requests make any attempt to delete tests immediately visible. Use coverage as a **regression signal**, not a vanity metric.

**Configuration:**
- Set thresholds high enough that regressions surface early
- Combine with Code Health safeguards for structure + behavior protection

### Pattern 6: Automate End-to-End

With agents iterating at high speed, manual verification becomes the bottleneck. Complement unit tests (~99% coverage) with end-to-end tests that exercise the packaged product in realistic scenarios.

**Example:** Build distributable → create test repo → inject code smells → invoke product → verify detection

## Implementation Blueprint

```yaml
# AGENTS.md (simplified)
agent_workflows:
  code_change:
    steps:
      - tool: code_health_review
        target: modified_files
      - condition: score < 9.5
        action: enter_refactoring_loop
      - tool: pre_commit_code_health_safeguard
        target: staged_files
      - tool: analyze_change_set
        target: branch_vs_base
        gate: must_pass_before_pr
      - condition: coverage_regression
        action: block_pr
```

## A-Tech Application

| Product | Implementation |
|---------|---------------|
| **A-Coder** | Ship Code Health MCP server as built-in quality layer; every agent mode queries health before and after edits |
| **Be Practical** | Teach the six patterns in curriculum; students learn agentic coding with discipline, not just speed |
| **Builder's Club** | Open-source CodeHealth MCP server template; community-contributed language-specific rules |

## Measurement Framework

| Metric | Target | Tracking Method |
|--------|--------|----------------|
| Code Health pre-agent | ≥9.5 | Automated assessment on module entry |
| AI-generated code health | ≥9.0 | Post-generation MCP review |
| PR blocked by health regression | <5% | PR gate analytics |
| Token burn on unhealthy code | -50% | Compare before/after refactoring |
| End-to-end test pass rate | ≥95% | CI/CD pipeline |

## Key Sources

- CodeScene — "Agentic AI Coding: Best Practice Patterns for Speed with Quality" (Adam Tornhill, Feb 2026)
- CodeScene — "Unhealthy code is burning your token usage" (2026): Agents consume up to 50% more tokens on unhealthy code
- CodeScene — "Making Legacy Code AI-Ready: Benchmarks on Agentic Refactoring" (2026)
