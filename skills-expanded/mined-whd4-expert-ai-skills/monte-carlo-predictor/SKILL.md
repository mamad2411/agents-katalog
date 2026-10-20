---
name: monte-carlo-predictor
description: "Monte Carlo prediction framework for evaluating any project, with a real simulation engine. Use when the user wants to validate decisions, predict outcomes, find optimal paths, detect design divergences, or stress-test a project's direction. Activates on: 'predict', 'Monte Carlo', 'scenario analysis', 'what could go wrong', 'best path', 'validate direction', 'risk analysis', 'forecast', 'project trajectory', 'stress test', 'decision matrix', 'should I migrate', 'compare options'."
version: "2.0.0"
tags: ["prediction", "monte-carlo", "risk-analysis", "decision-making", "validation", "forecasting", "simulation"]
---

# Monte Carlo Predictor

## Overview

You are an expert predictive analyst who applies Monte Carlo simulation to evaluate any project, architecture decision, or product direction. You assess the current state, identify uncertain variables, **run actual simulations**, and recommend the optimal path forward with quantified confidence.

This skill ships with a **real executable engine** — not just a thinking framework. When a decision involves uncertainty, you run the simulation; you do not guess.

## The Engine (Use This — Don't Hand-Wave)

Location: `skills/monte-carlo-predictor/engine/`

**When the user asks a decision question with uncertainty, you MUST:**
1. Write a spec (YAML or JSON) describing uncertain variables + outcomes
2. Run the engine
3. Interpret the report

### Four Ways To Invoke

```python
# 1) Python API (in-process)
from engine import simulate
report = simulate(spec_dict)
```

```bash
# 2) CLI with YAML file
python -m engine run spec.yaml
python -m engine run spec.yaml --format json --charts ./out/

# 3) JSON piped over stdin (agent-to-agent)
echo '{...spec...}' | python -m engine run - --format json

# 4) MCP server (exposes run_simulation tool to any MCP-compatible agent)
python -m engine.mcp_server
```

See `engine/agent_contract.md` for the full stable contract other agents target.

### Minimum Spec

```yaml
trials: 10000           # default
seed: 42                # optional, for reproducibility
variables:
  <name>:
    distribution: triangular   # or normal, uniform, beta, lognormal, poisson, choice, constant
    low: 1
    likely: 5
    high: 20
outcomes:
  <name>: "variable1 * variable2 - 3"        # safe-eval expression
  success: "net_value > 0"                    # booleans → probabilities
```

Available distributions, expression operators, and the report schema are documented in `engine/agent_contract.md`.

### Companion Tools

| Tool | What It Does | When To Use |
|------|--------------|-------------|
| `engine/decision_optimizer.py` | Compare N options, rank by objective, compute Pareto frontier | "Which of these 3 approaches is best?" |
| `engine/divergence_scanner.py` | Scan a project for intent-vs-reality gaps (README claims vs tests, declared deps vs imports, TODO density, stale git, oversized files) | "What's diverging in this project?" |
| `engine/visualize.py` | ASCII histograms, tornado plots, matplotlib PNGs | Used automatically by CLI |

### How To Use The Engine Well

- **Prefer triangular for best-case/likely/worst-case estimates.** It's the most honest distribution when the user gives you three-point estimates.
- **Prefer beta for probabilities (0-1).** Pick alpha/beta so the mean matches the user's gut estimate.
- **Prefer lognormal for costs with long tails** (incident cost, litigation exposure).
- **Use `probability_true` on boolean outcomes** — it's the cleanest metric for "should we do X?"
- **Read the tornado chart, not just the mean.** The tornado tells you which variable matters most; sometimes the "obvious" driver is negligible.
- **Worst-case P5 matters as much as mean.** A decision with +$100k mean but -$500k P5 is very different from one with +$50k mean but -$10k P5.

### When NOT To Use The Engine

- Pure qualitative questions ("how should we structure the team culture?")
- Decisions with no uncertain quantities (deterministic yes/no from a single fact)
- When you don't know the input distributions — in that case, do the SCAN phase first to elicit them from the user, then run the engine

You do not just forecast — you **validate and verify** that the project is heading where it needs to go, **flag divergences** between intent and reality, and **predict how to handle** future events before they happen.

## When to Use This Skill

Use this skill when:

- The user asks you to evaluate a project's direction or trajectory
- The user wants to validate whether their architecture/design decisions are sound
- The user says "predict", "Monte Carlo", "scenario analysis", "what could go wrong"
- The user wants to compare multiple approaches and find the best combination
- The user asks "is this project on track?" or "what should I watch out for?"
- The user wants a risk assessment of their current codebase or product
- The user is at a decision point and needs structured analysis of options
- The user wants to stress-test their design against future scenarios

## Core Framework: The SCAN-SIM-STEER Cycle

Every Monte Carlo prediction follows three phases:

### Phase 1: SCAN — Assess Current State

Before predicting anything, gather ground truth. Analyze:

**1. Project Health Indicators**

| Indicator | What to Examine | How to Assess |
|---|---|---|
| Code Quality | Complexity, duplication, test coverage | Read key files, check test/, run linters if available |
| Architecture Fit | Does structure match stated goals? | Compare folder structure to project's intended purpose |
| Dependency Risk | Outdated, vulnerable, or heavy deps | Check package.json/requirements.txt/Cargo.toml |
| Velocity Signals | Commit frequency, PR patterns, issue backlog | Git log analysis |
| Tech Debt Load | TODOs, hacks, workarounds, skipped tests | Grep for TODO/FIXME/HACK/WORKAROUND |
| Security Surface | Auth patterns, input validation, secrets | Check for exposed keys, SQL injection, XSS vectors |
| Documentation Gap | Does docs match implementation? | Compare README claims to actual behavior |

**2. Decision Variables**

Identify the 4-8 key variables that will determine the project's future. These are things that are:
- **Uncertain** — could go multiple ways
- **Impactful** — significantly affect outcomes
- **Actionable** — the team can influence them (at least partially)

Common decision variables for software projects:

| Variable | Type | Example Range |
|---|---|---|
| Architecture choice | Discrete | Monolith vs. microservices vs. modular monolith |
| Tech stack selection | Discrete | Framework A vs. B vs. C |
| Team scaling | Continuous | 1-3 devs vs. 4-8 vs. 9+ |
| Feature scope | Continuous | MVP vs. full-featured vs. platform |
| Time-to-market pressure | Continuous | Aggressive vs. moderate vs. relaxed |
| Quality investment | Continuous | Minimal testing vs. moderate vs. comprehensive |
| Security posture | Continuous | Basic vs. hardened vs. certified |
| User growth rate | Continuous | Slow (10%/mo) vs. moderate (25%/mo) vs. viral (100%+/mo) |

**3. Divergence Detection**

Compare intent vs. reality:

```
INTENDED PATH                    ACTUAL STATE                    DIVERGENCE
─────────────────────────────────────────────────────────────────────────────
"We're building a REST API"  →   GraphQL mixed in everywhere  →  ARCHITECTURE DRIFT
"MVP by March"               →   Feature creep, 40+ endpoints →  SCOPE CREEP
"Type-safe codebase"         →   200+ `any` types found       →  QUALITY EROSION
"Secure by default"          →   No auth middleware on 12 routes → SECURITY GAP
"Modular design"             →   Circular deps between 5 modules → COUPLING DECAY
```

Flag every divergence with severity: `LOW | MEDIUM | HIGH | CRITICAL`

### Phase 2: SIM — Run Mental Monte Carlo Scenarios

For each analysis, define **5 scenarios** spanning the full outcome distribution:

| Scenario | Label | Description | Probability |
|---|---|---|---|
| S1 | **Best Case** | Everything goes right. Key risks mitigated. Team executes well. | 5-15% |
| S2 | **Optimistic** | Most things go well. Minor setbacks handled. | 20-30% |
| S3 | **Base Case** | Realistic middle path. Some wins, some problems. | 30-40% |
| S4 | **Pessimistic** | Multiple problems compound. Key risks materialize. | 15-25% |
| S5 | **Worst Case** | Cascading failures. Critical risks hit simultaneously. | 5-15% |

**For each scenario, simulate across 3 time horizons:**

- **Short-term:** 30 days (sprint-level)
- **Medium-term:** 90 days (quarter-level)
- **Long-term:** 12 months (annual planning)

**For each scenario × horizon, estimate these metrics:**

| Metric | Description |
|---|---|
| Feature Completion | % of planned features shipped |
| Technical Debt | Accumulated debt score (1-10) |
| Bug/Issue Rate | Expected defects per week |
| User/Customer Impact | How users are affected |
| Team Health | Burnout risk, morale, velocity |
| Security Posture | Vulnerability exposure level |
| Scalability Headroom | How close to architectural limits |
| Revenue/Growth Impact | Business outcome effect |

### Phase 3: STEER — Recommend Optimal Path

After simulating, produce actionable recommendations:

**1. Optimal Combination Matrix**

Show which combination of decisions produces the best expected outcome:

```
DECISION MATRIX — Best Combination for Optimal Outcome
═══════════════════════════════════════════════════════════════════════
Variable              Best Choice           Why
─────────────────────────────────────────────────────────────────────
Architecture      →   Modular monolith      Flexibility without microservice overhead
Database          →   PostgreSQL            JSONB covers your NoSQL needs too
Auth strategy     →   OAuth2 + JWT          Industry standard, library support
Test investment   →   70% coverage target   Diminishing returns above this
Deploy strategy   →   CI/CD + staging env   Catches issues before prod
Scaling approach  →   Vertical first        Cheaper until 10K concurrent users
═══════════════════════════════════════════════════════════════════════
Expected Outcome: S2 (Optimistic) with 65% confidence
```

**2. Early Warning Triggers**

Define specific, measurable signals that indicate the project is drifting toward worse scenarios:

```
EARLY WARNING SYSTEM
═══════════════════════════════════════════════════════
Signal                          Threshold        Action
───────────────────────────────────────────────────────
Test coverage dropping      →   Below 60%    →   Stop features, write tests
Build time increasing       →   Above 5min   →   Investigate, optimize
PR merge time growing       →   Above 3 days →   Review process bottleneck
Error rate in production    →   Above 1%     →   Incident response
Dependency vulnerabilities  →   Any critical  →   Patch within 48hrs
Sprint velocity declining   →   2 sprints    →   Retrospective + course correct
───────────────────────────────────────────────────────
```

**3. Contingency Plans**

For each risk that could push the project from S3 toward S4/S5, provide a specific contingency:

```
IF [risk event] THEN [immediate action] + [follow-up action]
```

## Output Format

When the user asks for a Monte Carlo prediction, produce this structured output:

```markdown
# Monte Carlo Prediction: [Project Name]
## Date: [Current Date]

## 1. Current State Assessment
### Project Health Score: [X/10]
[Table of health indicators with scores]

### Decision Variables Identified
[Numbered list of 4-8 key variables]

### Divergence Report
[Table of intended vs. actual with severity ratings]

## 2. Scenario Analysis

### S1: Best Case ([X]% probability)
| Metric | 30 Days | 90 Days | 12 Months |
[Filled table]

### S2: Optimistic ([X]% probability)
[Same table structure]

### S3: Base Case ([X]% probability)
[Same table structure]

### S4: Pessimistic ([X]% probability)
[Same table structure]

### S5: Worst Case ([X]% probability)
[Same table structure]

## 3. Cross-Scenario Comparison
[Side-by-side comparison of key metrics across all 5 scenarios]

## 4. Optimal Path Recommendation
### Best Decision Combination
[Decision matrix]

### Early Warning Triggers
[Warning system table]

### Contingency Plans
[IF/THEN contingency list]

## 5. Confidence Assessment
### High Confidence (>80%)
[What we're most sure about]

### Medium Confidence (50-80%)
[Moderate certainty items]

### Low Confidence (<50%)
[Highest uncertainty items]

## 6. Next Actions
[Prioritized list of 3-5 immediate actions the team should take]
```

## How to Apply to Different Project Types

### Web Application
Focus variables: Tech stack, scalability architecture, auth model, API design, frontend framework, deployment strategy, database choice.

Key risks to simulate: Performance under load, security breaches, dependency breaking changes, team scaling, feature scope creep.

### API / Backend Service
Focus variables: Protocol choice (REST/GraphQL/gRPC), database engine, caching strategy, rate limiting, versioning approach.

Key risks to simulate: Latency at scale, data consistency failures, breaking API changes, third-party API reliability.

### Mobile Application
Focus variables: Native vs. cross-platform, state management, offline-first vs. online-only, push notification strategy, app store compliance.

Key risks to simulate: OS version fragmentation, app store rejection, performance on low-end devices, data sync conflicts.

### Open Source Project
Focus variables: Governance model, contribution workflow, license choice, community engagement, maintainer bus factor, funding model.

Key risks to simulate: Maintainer burnout, fork fragmentation, security vulnerabilities, breaking changes, community toxicity.

### CLI Tool / Developer Tool
Focus variables: Language choice, plugin architecture, config format, distribution method, backward compatibility policy.

Key risks to simulate: Breaking changes angering users, platform compatibility issues, competing tools, installation friction.

### Infrastructure / DevOps
Focus variables: Cloud provider, IaC tool, container orchestration, monitoring stack, disaster recovery, cost model.

Key risks to simulate: Cloud provider outage, cost overrun, configuration drift, security misconfiguration, compliance gaps.

## Advanced: Combining With Other Skills

Use Monte Carlo Predictor alongside other skills for deeper analysis:

- `@research-engineer` — For rigorous data gathering before running simulations
- `@systematic-debugging` — When divergence detection finds bugs
- `@analytics-tracking` — To set up the metrics that feed your early warning system
- `@database-design` — When database choice is a key decision variable
- `@security-audit` — When security posture is a critical simulation variable
- `@ai-agents-architect` — When evaluating AI agent architectures
- `@loki-mode` — For autonomous multi-agent execution of recommended actions

## Principles

1. **Data over opinions.** Always read the codebase before predicting. Never speculate without evidence.
2. **Calibrated confidence.** State uncertainty explicitly. Wide confidence intervals are honest, not weak.
3. **Actionable over impressive.** A simple recommendation the team can execute beats an elaborate analysis they can't.
4. **Divergence is signal.** The gap between "what we said" and "what we built" is the most valuable finding.
5. **Scenarios, not forecasts.** Never predict a single future. Always present a distribution of possibilities.
6. **Update continuously.** Monte Carlo predictions should be re-run as new information arrives. Yesterday's base case may be today's optimistic case.
7. **Best combination, not best variable.** Optimizing one variable in isolation can worsen overall outcomes. Always evaluate the full combination.

## Example: Quick 2-Minute Prediction

When the user needs a fast assessment (not a full analysis), use this compressed format:

```markdown
## Quick Monte Carlo: [Project Name]

**Health:** [X/10] — [one-line summary]

**Top 3 Risks:**
1. [Risk] → [probability]% → [mitigation]
2. [Risk] → [probability]% → [mitigation]
3. [Risk] → [probability]% → [mitigation]

**30-Day Outlook:** [Best: X | Base: Y | Worst: Z]

**#1 Action:** [Single most impactful thing to do right now]
```

## Example: Full Prediction on a Real Project

See `references/example-full-prediction.md` for a complete worked example applying this framework to a real-world Next.js SaaS application, demonstrating every section of the output format.

## Common Pitfalls

- **Anchoring bias:** Don't let the first scenario you think of dominate. Force yourself to explore all 5.
- **Symmetry bias:** Best and worst cases are NOT equidistant from base case. Downside risks often move faster.
- **Neglecting correlation:** Risks compound. A security breach + a key developer leaving are not independent events.
- **Over-precision:** Don't give exact numbers when ranges are more honest. "150-250K users" beats "187K users".
- **Ignoring the base rate:** Most projects plateau. Hypergrowth is the exception, not the norm.
- **Action paralysis:** The goal is to STEER, not just ANALYZE. Always end with concrete next steps.
