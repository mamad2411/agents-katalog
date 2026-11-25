---
name: skill-dev-verification
description: Decide Code Done using critical checks, component test policy, scope compliance, and >=80% dev verification score.
category: workflow
---

# Skill: Dev Verification

Use after coder outputs are collected.

## Code Done formula

```text
critical_checks_passed = 100%
score = passed_applicable_checks / total_applicable_checks
code_done = score >= 0.80 and critical_checks_passed and no_open_blocker
```

## Evidence required

```text
acceptance criteria mapping
changed files and scope check
test results or manual verification notes
critical check results
known risks
handoff readiness
```

## Rules

```text
Critical failure overrides score.
Do not create test files when policy forbids them.
Report DEV_BLOCKED when evidence is missing for critical checks.
```

## Reuse and convention verification

Dev Verification must check whether coder outputs respected reusable assets and project conventions.

Check:

- Reusable assets from task-analysis.yaml were used or explicitly waived with reason.
- New helpers do not duplicate known assets from common/generics.md or component_deep_intelligence.
- Shared reusable assets were changed only inside approved scope.
- Project conventions and anti-patterns were addressed in coder-results.yaml.

If duplicate helper risk is high or shared asset scope is violated, return NEEDS_FIX or DEV_BLOCKED depending on severity.

## Runtime verification

Code review alone is NOT sufficient for Code Done. At least one runtime method must be executed and evidence recorded.

### Accepted verification methods

| Method                            | When required                     | Minimum evidence                            |
| --------------------------------- | --------------------------------- | ------------------------------------------- |
| **Build / compile**               | Always                            | Build command + zero-error output           |
| **Unit test run**                 | When test files exist             | Command + pass/fail count                   |
| **API test (curl / HTTP client)** | HTTP endpoints added or changed   | curl command + response body / status code  |
| **UI smoke test**                 | Frontend feature changed          | Step-by-step walkthrough or screenshot path |
| **Log / output inspection**       | Background job, CLI, queue worker | Log snippet showing expected behavior       |
| **Integration test**              | Cross-service interaction changed | Request trace or integration output         |

### Rules

```text
Build check is always required; it alone does not count when runtime behavior changed.
At least one method must produce concrete evidence (command output, log snippet, screenshot).
If service is not runnable (missing env, DB not up), record DEV_BLOCKED with
  blocker_reason: "not_runnable" — do not claim DEV_DONE.
Never claim DEV_DONE on code review alone when any runtime behavior changed.
```
