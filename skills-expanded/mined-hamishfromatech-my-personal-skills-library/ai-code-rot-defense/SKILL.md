---
name: ai-code-rot-defense
description: Prevent, detect, and remediate AI-generated code rot before it compounds into architectural debt. Covers the stateless generation problem, duplication detection, design flaw screening, comprehension checkpoints, and sustainable AI-assisted development workflows. Use when integrating AI coding tools into production codebases, establishing code review protocols for AI-generated output, or measuring technical debt in AI-assisted teams. NOT for greenfield prototyping where speed matters more than longevity.
---

# AI Code Rot Defense

## Overview

AI coding assistants generate code at unprecedented speed, but studies show 62% contains design flaws or vulnerabilities, duplication increases 8×, and code reuse drops. This skill provides engineering protocols to capture AI productivity gains without accepting the hidden tax of layered software decay.

## When to Use

- Integrating AI coding tools into long-lived production codebases
- Establishing code review requirements for AI-generated contributions
- Measuring and tracking technical debt in AI-assisted development teams
- Designing CI/CD gates that catch AI-specific code quality issues
- Training developers on sustainable AI-assisted workflows

NOT for:
- One-off prototypes or hackathon projects
- Code expected to be discarded within weeks
- Situations where speed is the only metric that matters

## Core Process / Workflow

### Step 1: Establish the Stateless Generation Baseline

AI models generate code without memory of your codebase architecture. Each completion is statistically likely to:
- Re-implement existing utilities (duplication)
- Ignore established patterns (inconsistency)
- Miss cross-cutting concerns (security, error handling, logging)
- Optimize for local correctness over global coherence

**Baseline measurement:** Run duplication detection and architectural drift analysis on your codebase before introducing AI tools. This becomes your control group.

### Step 2: Implement the Four Defense Layers

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Generation-Time Guidance                           │
│ • Project-specific conventions in context (CONVENTIONS.md)    │
│ • Architecture decision records (ADRs) loaded into context  │
│ • Existing utility catalogs visible to the AI                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 2: Static Analysis Gates                              │
│ • Duplication detection (jscpd, Simian, PMD CPD)              │
│ • Cyclomatic complexity limits                              │
│ • Architecture fitness functions                            │
│ • Security scanners (SAST, dependency check)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 3: Human Review Protocol                              │
│ • AI-generated code labeled in PR                           │
│ • Reviewer checks: design intent, global coherence, tests     │
│ • "Why not existing?" question mandatory                    │
│ • Comprehension contract: reviewer explains the code back    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│ Layer 4: Runtime Monitoring                                 │
│ • Error rate telemetry by file age and generation source     │
│ • Performance regression detection                          │
│ • Refactoring frequency by module                           │
│ • Architectural drift scoring (monthly)                      │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Generation-Time Guidance Protocol

**CONVENTIONS.md template:**
```markdown
# Project Conventions for AI Assistants

## Utility Catalog
- Date formatting: use `utils/date.js::formatISO()` — never re-implement
- HTTP client: use `services/api.ts::authenticatedFetch()` — wraps auth, retries, logging
- Error handling: use `errors/AppError.ts` with structured codes

## Forbidden Patterns
- No direct `fetch()` calls outside `services/api.ts`
- No `console.log` — use `services/logger.ts`
- No inline SQL — use `repositories/` layer

## Testing Requirements
- Every new function must have ≥1 unit test
- Every bug fix must have a regression test
- Test files mirror source structure under `tests/`
```

**Context window strategy:**
- Load CONVENTIONS.md + top 5 utility files into context before generation
- Use RAG (Retrieval-Augmented Generation) to pull relevant existing code
- Update context when AI suggests code that violates conventions

### Step 4: Static Analysis Gates

**CI/CD pipeline additions:**

```yaml
ai-code-quality-gates:
  duplication:
    tool: jscpd
    threshold: < 3% duplication increase per PR
    fail_on: > 5% increase
  
  complexity:
    tool: sonarqube
    threshold: cyclomatic < 15 per function
    fail_on: > 20
  
  architecture:
    tool: archunit / dependency-cruiser
    rules:
      - no_cycles: true
      - layer_dependencies: [domain -> application -> infrastructure]
    fail_on: any violation
  
  security:
    tool: semgrep + snyk
    rules: [owasp-top-10, cwe-top-25]
    fail_on: high or critical
  
  ai-specific:
    tool: custom_linter
    checks:
      - "re-implements existing utility" pattern detection
      - "missing error handling" in AI-generated blocks
      - "hardcoded value" where config should exist
    fail_on: > 2 findings per PR
```

### Step 5: Human Review Protocol

**AI-generated PR labeling:**
- Auto-label PRs where >50% lines are AI-generated
- Require designated "AI code reviewer" approval

**Reviewer checklist:**
```
[ ] I understand what this code does and why
[ ] I can explain the design intent in one sentence
[ ] I checked if existing utilities could replace new code
[ ] I verified error handling covers edge cases
[ ] I confirmed tests exercise both happy path and failure modes
[ ] I checked for security implications (input validation, auth, injection)
[ ] I verified the code follows project conventions (CONVENTIONS.md)
[ ] I assessed whether this code will be easy to refactor in 6 months
```

**Comprehension contract:** The reviewer must be able to explain the code back to the author (or AI) in their own words. If they cannot, the code is not reviewed — it is rejected for clarification.

### Step 6: Runtime Monitoring

**Debt accumulation dashboard:**

| Metric | Baseline | Current | Delta | Alert Threshold |
|--------|----------|---------|-------|-----------------|
| Code duplication % | 4.2% | 5.1% | +0.9% | > 6% |
| Average cyclomatic complexity | 8.3 | 9.7 | +1.4 | > 12 |
| Test coverage | 78% | 74% | -4% | < 70% |
| Architectural rule violations | 2 | 7 | +5 | > 5/quarter |
| Mean time to refactor (days) | 14 | 23 | +9 | > 21 |
| Error rate by module age | 0.3% | 0.7% | +0.4% | > 0.5% |

**Monthly architecture review:**
- Run dependency analysis and visualize drift from target architecture
- Identify modules with highest AI-generation rate + highest error rate
- Schedule targeted refactoring for modules crossing alert thresholds

### Step 7: Sustainable AI-Assisted Workflow

**The 80/20 AI rule:**
- 80% of AI assistance on well-understood, bounded tasks (tests, boilerplate, documentation)
- 20% on novel, complex architectural decisions (with mandatory human design review)

**The comprehension checkpoint:**
Before accepting any AI-generated code block >20 lines, the developer must:
1. Read and understand every line
2. Identify the design pattern used
3. Name one way the code could fail
4. Confirm the code fits the existing architecture

**The refactoring budget:**
Allocate 15% of sprint capacity to refactoring AI-generated code from prior sprints. This is not overhead — it is maintenance of the AI productivity dividend.

## A-Tech Product Applications

### A-Coder
- Built-in duplication detection: warn when generated code mirrors existing utilities
- CONVENTIONS.md auto-loading from project root
- AI-generated code labeling in diff view
- Comprehension checkpoint: require developer acknowledgment before accepting large blocks

### Be Practical
- "Sustainable AI Coding" module in curriculum
- Code rot case studies: real-world examples of AI-generated technical debt
- Review protocol template for solo developers

### Builder's Club
- Open-source code rot detection tooling
- Community-maintained CONVENTIONS.md templates by language/framework
- Peer review pairing program for AI-assisted contributions

## References

- See [references/ai-code-rot-research.md](references/ai-code-rot-research.md) for academic and industry studies on AI-generated code quality.
- See [references/static-analysis-configuration.md](references/static-analysis-configuration.md) for tool-specific configuration templates.
- See [references/comprehension-checkpoint-protocol.md](references/comprehension-checkpoint-protocol.md) for the full comprehension contract implementation guide.
