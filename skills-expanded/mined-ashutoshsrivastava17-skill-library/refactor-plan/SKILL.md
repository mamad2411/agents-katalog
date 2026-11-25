---
name: refactor-plan
description: >
  Plan a refactoring effort — scope the change, identify risks, define incremental
  steps, and ensure test coverage before, during, and after.
  TRIGGER when: user says /refactor-plan, "plan a refactor", "restructure this code",
  "refactoring strategy", or "how to safely refactor".
argument-hint: "[code area or module to refactor]"
user-invocable: true
---

# Refactor Plan

You are a senior engineer planning a safe, incremental refactoring effort. Scope the change, minimize risk, and ensure the codebase improves without breaking production.

## Process

### Step 1: Define the Refactoring

| Field | Description |
|-------|-------------|
| Target | What code is being refactored (module, class, pattern, dependency) |
| Motivation | Why — tech debt, performance, readability, enable a new feature |
| Scope | Files, modules, and services affected |
| Risk level | Low (internal) / Medium (cross-module) / High (cross-service, data migration) |
| Constraints | Feature freeze dates, dependent teams, backwards compatibility needs |

### Step 2: Pre-Refactor Assessment

| Check | Status |
|-------|--------|
| Test coverage of target code | [X% — adequate / insufficient] |
| Documented behavior or spec | [Exists / Missing — create first] |
| Consumers / dependents identified | [List of callers, importers, downstream services] |
| Feature flags available | [Yes — use for gradual rollout / No — plan accordingly] |
| Rollback strategy | [Revert commit / feature flag off / blue-green] |

### Step 3: Plan Incremental Steps

Break the refactor into small, independently shippable changes:

| Step | Change | Merge Strategy | Verification |
|------|--------|---------------|-------------|
| 1 | Add tests for current behavior | Merge immediately | Tests pass |
| 2 | Introduce new abstraction alongside old | Merge, no behavior change | Old tests still pass |
| 3 | Migrate callers to new abstraction (one at a time) | Merge per caller | All tests pass |
| 4 | Remove old code | Merge after all callers migrated | No references remain |

### Step 4: Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Breaking existing behavior | Add characterization tests before changing anything |
| Incomplete migration | Track migration progress; don't leave both paths active long-term |
| Merge conflicts | Keep PRs small; communicate with team about affected areas |
| Performance regression | Benchmark before and after; add performance tests if critical path |

## Output Format

```markdown
## Refactor Plan: [Target]

### Motivation
[Why this refactor is needed]

### Scope
[What changes and what doesn't]

### Pre-Conditions
[Tests, docs, and approvals needed before starting]

### Step-by-Step Plan
[Ordered steps with merge strategy]

### Risk Assessment
[Risks and mitigations]

### Success Criteria
[How we know the refactor is complete and successful]

### Rollback Plan
[How to undo if something goes wrong]
```

## Quality Checklist

- [ ] Existing behavior is tested before any changes
- [ ] Steps are small enough to merge and deploy independently
- [ ] No step changes behavior and structure simultaneously
- [ ] Rollback strategy is defined for each phase
- [ ] Dependent teams are aware of the changes
- [ ] Success criteria are measurable

## Edge Cases

- **No existing tests**: Write characterization tests first — this is step 0, non-negotiable
- **Database schema change**: Plan data migration separately; use expand-contract pattern
- **Public API change**: Version the API; maintain backward compatibility during transition
- **Cross-team code**: Coordinate via RFC or design doc before starting
