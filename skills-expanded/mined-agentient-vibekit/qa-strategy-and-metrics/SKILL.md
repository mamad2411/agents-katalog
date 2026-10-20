---
name: qa-strategy-and-metrics
version: "1.0"
description: >
  Testing pyramid, quality metrics, and technical debt management strategies.
  PROACTIVELY activate for: (1) Designing testing strategy, (2) Evaluating code quality metrics,
  (3) Managing technical debt, (4) Analyzing test coverage approaches, (5) Calculating complexity.
  Triggers: "testing strategy", "testing pyramid", "quality metrics", "technical debt", "cyclomatic complexity", "maintainability", "coverage principles"
core-integration:
  techniques:
    primary: ["systematic_analysis"]
    secondary: ["structured_evaluation"]
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# QA Strategy and Metrics Skill

## Metadata (Tier 1)

**Keywords**: strategy, testing pyramid, quality, metrics, technical debt, complexity, maintainability, coverage principles

**File Patterns**: N/A (conceptual skill)

**Modes**: code_review, testing_frontend, testing_backend

**Activation**: Conceptual queries about testing strategy, quality metrics, or technical debt.

---

## Instructions (Tier 2)

### Testing Pyramid

```
       E2E (5-10%)
    Integration (15-20%)
  Unit Tests (70-80%)
```

**Rationale**:
- **Unit**: Fast (ms), cheap, high confidence in individual components
- **Integration**: Moderate speed (seconds), tests component interactions
- **E2E**: Slow (seconds-minutes), expensive, fragile, but validates real workflows

**Anti-Pattern**: Inverted pyramid (too many E2E tests)
- Slow CI/CD pipeline
- Flaky tests due to external dependencies
- High maintenance burden

### Cyclomatic Complexity (CC)

**Formula**: CC = E - N + 2P
- E = edges in control flow graph
- N = nodes
- P = connected components

**Interpretation**:
- 1-5: Low risk, straightforward logic
- 6-10: Moderate complexity, well-structured
- 11-20: Complex, consider refactoring
- 21+: Very complex, MUST refactor

**When to refactor**:
- Function has CC > 15
- Function has multiple responsibilities
- Difficult to write tests (need many mocks)

### Code Coverage Metrics

**Statement Coverage**: % of code lines executed
**Branch Coverage**: % of decision paths taken (if/else, switch)
**Function Coverage**: % of functions called

**Critical Insight**: 100% coverage ≠ 100% tested
- May miss edge cases
- May not test error handling
- May not validate business logic

**Focus Areas**:
- Error handlers (try/except, catch)
- Boundary conditions (null, empty, max)
- Complex conditionals

### Maintainability Index (MI)

**Formula** (simplified):
```
MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
```
- HV = Halstead Volume (code complexity)
- CC = Cyclomatic Complexity
- LOC = Lines of Code

**Ranges**:
- 85-100: Highly maintainable
- 65-84: Moderately maintainable
- 0-64: Difficult to maintain

### Technical Debt

**Formula**: Debt = (Cost to Fix) * (Impact if Not Fixed)

**Types**:
1. **Code Debt**: Poor structure, duplication
2. **Test Debt**: Low coverage, missing tests
3. **Documentation Debt**: Missing/outdated docs
4. **Architectural Debt**: Design constraints

**When to Pay Down**:
- High-traffic code paths
- Before major refactoring
- Security-sensitive areas
