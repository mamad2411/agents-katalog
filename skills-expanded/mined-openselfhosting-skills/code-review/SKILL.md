---
name: code-review
description: "Reviews a code diff for correctness, regressions, security, data integrity, performance, and missing tests. Use when reviewing a pull request, patch, staged diff, or proposed code change; prioritize actionable findings over style opinions."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Code Review

## Goal
Identify material defects introduced by the change, supported by concrete evidence. Review the diff, not the author.

## Review procedure
1. Read repository instructions and understand the intent from the issue, PR description, or user request. If intent is unclear, state the ambiguity.
2. Inspect the complete diff and relevant surrounding code. Check the base revision and working-tree state; do not assume every changed line is new or owned by the author.
3. Trace affected flows from callers through validation, authorization, business logic, persistence, and outputs. Inspect call sites when public APIs, types, schemas, or behavior change.
4. Evaluate, where relevant:
   - incorrect results, edge cases, state and concurrency;
   - authentication, authorization, input handling, secrets, and trust boundaries;
   - backward compatibility and API/schema contracts;
   - data loss, transaction boundaries, retries, idempotency, and migrations;
   - resource use, query complexity, latency, and failure handling;
   - tests that are missing, weak, flaky, or disconnected from the changed behavior;
   - observability and operational impact.
5. Run targeted, safe checks if available. Do not modify the patch merely to make review easier. Avoid broad or destructive commands.
6. Validate each candidate finding against the code and intended behavior. Drop speculative issues, duplicates, and purely stylistic preferences unless a project rule makes them defects.

## Finding format
For each finding include:
- **Severity:** Critical / High / Medium / Low.
- **Location:** smallest useful file and line range in the changed diff, where possible.
- **Problem:** what will go wrong and under which condition.
- **Impact:** concrete consequence for users, data, security, or operations.
- **Evidence:** code path, example input, invariant, or test result.
- **Suggested fix:** a focused direction, not an unsolicited rewrite.

Order findings by severity. If there are no substantiated findings, say so and list residual risks or checks not run. Do not invent findings to fill a quota.

## Severity guidance
- **Critical:** likely widespread compromise, irreversible data loss, or service-wide outage.
- **High:** serious exploitable weakness, data corruption, or major common-path failure.
- **Medium:** meaningful defect with limited scope, a less common trigger, or an important missing guard.
- **Low:** minor correctness, robustness, or maintainability issue with modest practical impact.

## Rules
- Be precise and respectful; no personal judgments.
- Separate bugs from questions and optional improvements.
- Do not claim to have run tests, scanners, or builds unless you actually did.
- Never expose secret values in a review comment.
