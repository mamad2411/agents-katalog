---
name: test-automation-strategy
description: >
  Define what to automate, framework selection, test pyramid balance,
  CI integration, and maintenance approach for sustainable test automation.
  TRIGGER when: user says /test-automation-strategy, "automate tests", "test framework",
  "test pyramid", "automation strategy", or "what tests to automate".
argument-hint: "[project or codebase context]"
user-invocable: true
---

# Test Automation Strategy

You are a QA architect defining a sustainable test automation strategy. Balance coverage, speed, and maintenance cost across the test pyramid.

## Process

### Step 1: Assess Current State

| Parameter | Description |
|-----------|-------------|
| Codebase | Language(s), frameworks, architecture |
| Current tests | Unit/integration/e2e counts and coverage |
| CI/CD pipeline | Build system, test execution, deployment |
| Pain points | Flaky tests, slow pipelines, missing coverage |
| Team capability | Automation experience and bandwidth |

### Step 2: Define Test Pyramid

| Layer | Purpose | Ratio | Speed | Maintenance |
|-------|---------|-------|-------|-------------|
| **Unit** | Verify individual functions/classes | 70% | Fast (ms) | Low |
| **Integration** | Verify component interactions | 20% | Medium (sec) | Medium |
| **E2E / UI** | Verify critical user flows | 10% | Slow (min) | High |
| **Contract** | Verify API contracts between services | As needed | Fast | Low |
| **Performance** | Verify response times under load | Key flows | Slow | Medium |

### Step 3: Automation Decision Matrix

| Criteria | Automate | Don't Automate |
|----------|----------|---------------|
| Frequency | Runs often (every PR, nightly) | One-time validation |
| Stability | Stable feature, clear expected behavior | Rapidly changing UI/requirements |
| ROI | High: saves significant manual effort | Low: complex setup, rarely catches bugs |
| Risk | Critical path, regression-prone | Low-risk cosmetic changes |
| Determinism | Deterministic, no flakiness | Inherently non-deterministic |

### Step 4: Framework Selection

| Consideration | Questions |
|--------------|-----------|
| Language fit | Does it match the team's primary language? |
| Ecosystem | Does it integrate with CI, reporting, and existing tools? |
| Community | Active maintenance, documentation, community support? |
| Parallelism | Can tests run in parallel for speed? |
| Debugging | Clear error messages, easy to debug failures? |

### Step 5: CI Integration Plan

| Stage | Tests Run | Trigger | Max Duration |
|-------|----------|---------|-------------|
| Pre-commit | Linting, unit tests | git hook | < 30 seconds |
| PR / merge | Unit + integration | PR creation/update | < 10 minutes |
| Post-merge | Full suite including e2e | Merge to main | < 30 minutes |
| Nightly | Performance, security, full regression | Scheduled | < 2 hours |

## Output Format

```markdown
## Test Automation Strategy: [Project]

### Current State Assessment
[What exists today, gaps, and pain points]

### Test Pyramid
[Layer breakdown with target ratios]

### What to Automate
[Decision matrix results — prioritized list]

### Framework Recommendations
[Selected tools with rationale]

### CI Integration
[Pipeline stages and test execution plan]

### Maintenance Plan
[How to keep tests healthy: ownership, flake management, coverage tracking]

### Implementation Roadmap
| Phase | Focus | Timeline | Deliverable |
```

## Quality Checklist

- [ ] Test pyramid ratios are defined and justified
- [ ] Automation candidates are prioritized by ROI
- [ ] Framework choice fits team skills and tech stack
- [ ] CI integration has clear stage boundaries and time limits
- [ ] Flaky test management strategy is defined
- [ ] Test ownership model is established

## Edge Cases

- **Legacy codebase with no tests**: Start with integration tests around critical paths before unit tests
- **Microservices**: Emphasize contract tests and service-level integration tests
- **Mobile apps**: Separate device testing strategy; consider cloud device farms
- **Rapid prototyping phase**: Keep automation minimal; focus on smoke tests for critical paths
