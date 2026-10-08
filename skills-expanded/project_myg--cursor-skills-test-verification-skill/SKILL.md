---
name: test-verification
description: Creates and runs unit, integration, smoke, and regression checks for the AI project management platform. Use when validating features, diagnosing failures, or preparing releases.
---

# Test Verification

## Trigger

Use this skill after implementation, before release, when CI fails, when a defect is reported, or when architecture changes affect shared contracts.

## Workflow

1. Identify the behavior and risk being validated.
2. Add or update focused tests for pure logic, API behavior, and critical pages.
3. Run the narrowest relevant test command first.
4. If a test fails, capture the command, failure, likely cause, and route the fix to development-execution.
5. Confirm the fix with the same test, then run the broader suite when release or shared behavior is affected.
6. Record unrun checks explicitly instead of implying they passed.

## Required Coverage

- Agent orchestration parses user goals into tasks and risks.
- Dashboard aggregation calculates progress, workload, bottlenecks, and risk counts.
- Core pages render without runtime errors.
- Health check endpoint returns a successful response.
- API routes validate inputs and return stable response shapes.
- Persistence and repository mappings preserve task status, priority, risk level, and dependencies once storage is enabled.

## Result Format

```markdown
## Validation
- Command:
- Result:
- Failures:
- Next Action:
- Unrun Checks:
```

## Test Gate

- P0 product acceptance criteria have unit, API, or smoke coverage.
- Failing commands are reproducible.
- Fixes rerun the original failing check.
- Release candidates run `npm run test`, `npm run lint`, `npm run build`, and relevant `npm run test:e2e`, unless a missing dependency is documented.
