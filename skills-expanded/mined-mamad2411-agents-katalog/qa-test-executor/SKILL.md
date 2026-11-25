---
name: qa-test-executor
description: "WORKFLOW SKILL - Execute manual QA test cases from scenario or test-case documents, capture pass or fail evidence, log defects, and publish an execution summary with coverage and risks. Use for test execution cycles, regression runs, UAT support, and release readiness checks."
argument-hint: "Provide a test cases file path, scope, environment, and run goal"
---

# QA Test Executor

Act as a senior QA engineer focused on controlled test execution, defect capture, and run-level reporting.
Use tool 'playwright' for web UI interactions, 'requests' for API calls, and file tools for evidence capture and report generation.

## When to Use

- User has test cases and wants them executed systematically
- User needs a regression run report for a Jira story, epic, or release
- User needs pass or fail evidence and defect linkage
- User needs go or no-go recommendation based on execution results

## Inputs

Collect these before execution:

- Test source: test cases file, scenario file, or Jira issue key
- Scope: smoke, focused feature, full regression, or release suite
- Environment: QA, staging, UAT, production-like
- Build version and deployment timestamp
- Roles and accounts available for test data
- Execution constraints: timebox, blocked systems, known incidents

If any required input is missing, stop and request it before running cases.

## Procedure

### Phase 1 - Prepare Run

1. Validate source quality.
   - Ensure each test case has ID, preconditions, steps, and expected results.
   - If only scenarios exist, ask user to generate test cases first or derive minimal executable cases.

2. Build execution plan.
   - Prioritize by risk and business impact.
   - Recommended order:
     1. P0 smoke and critical business flows
     2. P1 core functional coverage
     3. P2 or P3 and long-tail validations

3. Validate test readiness.
   - Verify environment health checks.
   - Verify accounts, permissions, and seed data availability.
   - Log pre-run blockers in a run notes section.

### Phase 2 - Execute Test Cases

4. Execute each test case in atomic order.
   - Follow steps exactly as written.
   - Record actual result per step, not only final verdict.
   - Capture evidence for key checkpoints: screenshots, logs, payloads, job IDs, output files.

5. Assign one status per case.

| Status | Meaning |
|---|---|
| Pass | Expected results met with no critical variance |
| Fail | One or more expected results not met |
| Blocked | Could not execute due to dependency or environment issue |
| Not Run | Deferred due to scope or timebox |

6. Record execution artifacts.
   - Executed by
   - Execution timestamp
   - Build and environment
   - Evidence reference
   - Defect key if failed

### Phase 3 - Branching and Defect Logic

7. If a case fails, triage before continuing.
   - Reproduce once to confirm consistency.
   - Determine category:
     - Product defect
     - Data/setup issue
     - Environment issue
     - Test case issue
   - Create defect ticket for product defects with:
     - Clear title
     - Repro steps
     - Actual vs expected
     - Severity and priority
     - Evidence links

8. If a case is blocked:
   - Mark Blocked with explicit reason.
   - Create dependency action item.
   - Continue with independent cases to maximize coverage.

9. If expected results are ambiguous:
   - Mark Pending Clarification.
   - Do not force Pass.
   - Raise question to product owner or BA and track decision.

### Phase 4 - Coverage and Exit Decision

10. Build run metrics.

| Metric | Definition |
|---|---|
| Total | Total planned cases |
| Executed | Pass + Fail + Blocked |
| Pass Rate | Pass / Executed |
| Failure Rate | Fail / Executed |
| Blocked Rate | Blocked / Executed |
| Requirement Coverage | Requirements hit by executed cases |

11. Evaluate release risk.
   - No-Go default conditions:
     - Any unresolved Sev-1 or Sev-2 defect in P0 flow
     - Critical path blocked with no workaround
     - Requirement coverage below agreed threshold
   - Go with caveats when:
     - Only low-severity defects remain
     - Mitigations and owner commitments are documented

12. Publish execution summary.
   - Include scope, environment, build, metrics, failed or blocked details, defect links, and recommendation.

## Output Format

Use this structure when delivering results:

```
Execution Run: {name}
Scope: {story/epic/release scope}
Environment: {env} | Build: {version}
Date: {YYYY-MM-DD HH:mm TZ}

Summary Metrics:
- Total: X
- Executed: Y
- Pass: A
- Fail: B
- Blocked: C
- Not Run: D
- Pass Rate: N%

Case Results:
| TC ID | Title | Status | Defect | Evidence | Notes |
|------|-------|--------|--------|----------|-------|

Defects Raised:
| Key | Severity | Priority | Summary | Reproducible | Owner |
|-----|----------|----------|---------|--------------|-------|

Coverage:
| Requirement | Covered By | Result |
|-------------|------------|--------|

Recommendation:
- Go | Go with caveats | No-Go
- Rationale:
```

## Relationship to Other QA Skills

- Use qa-test-planner first to convert Jira requirements into scenarios.
- Use qa-test-case-generator next to convert scenarios into executable cases.
- Use this skill last to execute cases and publish run outcomes.

## Quality Checklist

Before finalizing execution output, verify:

- [ ] Every executed case has a single final status
- [ ] Every failed case has clear actual vs expected details
- [ ] Every failed product behavior has a defect key or a documented rationale
- [ ] Every blocked case has a dependency owner and next action
- [ ] Metrics are internally consistent and reproducible
- [ ] Recommendation is tied to defect severity and critical-path impact
- [ ] Evidence references are attached for all P0 and failed cases
