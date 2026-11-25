---
name: "architecture-radar"
description: "Automated technology trend scanning and architecture pattern extraction for the Engineering department. Monitors open-source trends, framework releases, and architecture patterns. Evaluates applicability to orchestrator stack, produces adoption recommendations, and feeds the engineering self-improvement loop. Use when evaluating new technologies, scanning for architecture patterns, planning tech radar updates, or running the engineering UAOP pipeline."
risk: low
tags: [engineering, architecture, research, trends]
created: 2026-03-23
updated: 2026-03-23
---

# Architecture Radar — Engineering Intelligence Engine

Automated tech trend scanning that keeps the Engineering department ahead of the curve. UAOP Stage 1 for Engineering.

## When to use

- Quarterly tech radar update
- Evaluating a new framework, library, or pattern
- Before major architecture decisions — "what's working elsewhere?"
- When a dependency is deprecated — "what's the replacement?"
- Sprint planning — "any new patterns that simplify what we're building?"

## When NOT to use

- Implementing a specific pattern (use `clean-architecture-python` or `api-design-patterns`)
- Security vulnerability scanning (use `threat-intelligence-feed`)
- Performance profiling (use `production-monitoring`)

## Pipeline

### Step 1: Scan Sources

```
SCAN TARGETS:
  Package ecosystems:
    - PyPI trending (Python): new releases for FastAPI, SQLAlchemy, Pydantic, pytest
    - npm trending (Node): Next.js, Tailwind, shadcn/ui updates
    - GitHub trending repos in Python/TypeScript (last 30 days)

  Architecture blogs & reports:
    - ThoughtWorks Technology Radar (quarterly)
    - InfoQ architecture trends
    - CNCF project maturity changes
    - Martin Fowler's blog, Architecture Notes

  Community signals:
    - HackerNews top posts (AI, Python, infrastructure)
    - Reddit r/python, r/devops, r/programming
    - Conference talks (NeurIPS, KubeCon, PyCon)

  Competitor tech:
    - LangChain/CrewAI/AutoGen changelog and release notes
    - How competitors solve problems we're facing
```

### Step 2: Evaluate Applicability

For each trend/pattern discovered:

```markdown
## Technology Evaluation: [Name]

**Category:** [Language/Framework/Pattern/Tool/Infrastructure]
**Maturity:** [Adopt/Trial/Assess/Hold] (ThoughtWorks terminology)
**Source:** [Where discovered, evidence grade A/B/C]

### What It Is
[One paragraph — what the technology does]

### Relevance to CoreMind
- Applicable to: [which components/services]
- Problem it solves: [specific CoreMind problem]
- Current solution: [what we use today]
- Improvement: [quantified if possible]

### Adoption Assessment
| Factor | Score (1-5) | Notes |
|--------|------------|-------|
| Problem fit | [X] | Does it solve a real CoreMind problem? |
| Maturity | [X] | Production-ready? Community support? |
| Migration cost | [X] | How hard to adopt? Breaking changes? |
| Team familiarity | [X] | Learning curve? |
| Maintenance burden | [X] | Long-term support outlook? |
| **Total** | [X/25] | Adopt if >18, Trial if >12, Assess if >8 |

### Recommendation
[ADOPT / TRIAL / ASSESS / HOLD] — [one sentence rationale]
```

### Step 3: Produce Radar Report

```markdown
# Architecture Radar — [Quarter] [Year]

## Summary
- Technologies scanned: [N]
- New recommendations: [N] Adopt, [N] Trial, [N] Assess, [N] Hold

## Adopt (Use in production)
[List with one-line rationale each]

## Trial (Prototype and evaluate)
[List]

## Assess (Research and monitor)
[List]

## Hold (Don't adopt, or phase out)
[List]

## Architecture Patterns Trending
| Pattern | Where Used | Applicability | Priority |
|---------|-----------|--------------|----------|

## Dependency Updates Due
| Package | Current | Latest | Breaking Changes | Priority |
|---------|---------|--------|-----------------|----------|
```

### Step 4: Self-Improvement Loop

```
MEASURE:
  - Adoption recommendations that improved quality/performance (hit rate)
  - Technologies adopted that caused problems (miss rate)
  - Time from trend detection to adoption decision

REINFORCE:
  - Sources that produced high-hit-rate recommendations
  - Evaluation criteria that predicted success

REGENERATE:
  - Update scanning scope based on stack changes
  - Adjust evaluation weights based on past adoption outcomes
```

## Cadence

```
WEEKLY:   Dependency update check (new versions, deprecations)
MONTHLY:  Technology scan (trending repos, blog posts, releases)
QUARTERLY: Full radar report with adoption recommendations
```

## Agents

| Agent | Role |
|-------|------|
| system-architect (L1) | Owns architecture decisions, approves adoptions |
| architect (L1) | Evaluates patterns, assesses trade-offs |
| backend-architect (L2) | Python/FastAPI/DB technology evaluation |
| frontend-architect (L2) | Next.js/React/CSS technology evaluation |
| ai-engineer (L2) | LLM/agent framework evaluation |
| deep-research (L2) | Executes trend scanning |
