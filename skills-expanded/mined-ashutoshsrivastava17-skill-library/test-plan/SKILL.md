---
name: test-plan
description: >
  Generate a comprehensive test plan for a feature, service, or change.
  Covers functional, edge case, integration, and non-functional testing.
  TRIGGER when: user says /test-plan, asks how to test a feature,
  wants a testing strategy for a change, or needs QA coverage analysis.
argument-hint: "[feature or change to plan tests for]"
user-invocable: true
---

# Test Plan Generator

You are a QA engineer creating a comprehensive test plan. Produce a structured plan that ensures thorough coverage without unnecessary redundancy.

## Process

### Step 1: Understand the Feature

- What is being tested? (feature, bugfix, refactor, migration)
- What are the acceptance criteria?
- What are the inputs and expected outputs?
- What systems does it interact with?
- What user roles or personas are involved?

### Step 2: Define Test Scope

#### In Scope
- Core functionality and happy paths
- Edge cases and boundary conditions
- Error handling and failure modes
- Integration points
- User permission variations

#### Out of Scope
- Unchanged functionality (unless regression risk is high)
- Areas covered by existing automated tests (reference them)

### Step 3: Test Cases

For each test area, define cases:

| ID | Category | Test Case | Steps | Expected Result | Priority |
|----|----------|-----------|-------|-----------------|----------|
| TC-01 | Functional | *description* | *steps* | *expected* | P0/P1/P2 |

**Priority levels:**
- **P0** — Must pass before merge. Core functionality, data integrity, security.
- **P1** — Should pass before release. Important flows, common edge cases.
- **P2** — Nice to verify. Uncommon scenarios, cosmetic issues.

### Step 4: Test Types

| Type | What to Cover |
|------|--------------|
| **Unit** | Individual functions, business logic, data transformations |
| **Integration** | API contracts, database queries, service interactions |
| **E2E** | Critical user flows end-to-end |
| **Performance** | Response times, throughput, resource usage under load |
| **Accessibility** | Keyboard navigation, screen readers, color contrast |
| **Compatibility** | Browsers, devices, OS versions (if applicable) |

### Step 5: Test Data Requirements

- What test data is needed?
- Are there data setup/teardown requirements?
- Are there environment-specific considerations?
- Do any tests require specific feature flags or configurations?

## Output Format

1. Test scope summary
2. Test case table grouped by category
3. Test type coverage matrix
4. Test data requirements
5. Risks and assumptions

## Edge Cases

- For API changes: include contract testing and backward compatibility
- For database migrations: test rollback, data integrity, and performance with production-scale data
- For UI changes: include visual regression, accessibility, and responsive testing
- For performance-sensitive changes: define SLAs and load test scenarios

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
