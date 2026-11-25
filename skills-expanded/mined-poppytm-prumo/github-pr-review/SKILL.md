---
name: github-pr-review
description: Rigorous code review heuristics, architectural conformance, security inspection, constructive feedback, and gh pr review automation
---
# GitHub Pull Request Review & Quality Assessment

## 1. Architectural Alignment & Clean Code
Verify that proposed changes conform to repository design invariants, dependency directions, and domain boundaries. Reject premature abstractions and unneeded architectural complexity.

## 2. Exhaustive Test Coverage Verification
Ensure every new code path, error handling branch, and edge case is backed by deterministic automated unit or integration tests. Reject PRs claiming completion without tests.

## 3. Security & Boundary Inspection
Scrutinize inputs, data sanitization, authentication boundaries, and secret handling. Verify that no escape hatches or unchecked suppressions are introduced.

## 4. Constructive & Actionable Feedback
Format review comments clearly: state the concern, explain the architectural why, and provide a concrete proposed code suggestion using GitHub suggestion blocks.

## 5. Performance & Resource Management
Identify potential memory leaks, N+1 database queries, unindexed queries, blocking I/O calls in event loops, and missing timeouts on external network requests.

## 6. Backward Compatibility & Contract Safety
Verify that public APIs, database schemas, and configuration contracts maintain compatibility or provide safe, versioned migration paths.

## 7. Automated gh CLI Review Operations
Execute review operations via CLI: gh pr review --comment -b 'Feedback', gh pr review --request-changes -b 'Blocking concerns', or gh pr review --approve -b 'Approved with evidence'.

## 8. Review Gate Enforcement
Strictly enforce repository governance review rules: verify that independent security verifiers approve High/Critical risk PRs before merge.

## 9. Conversation Resolution Discipline
Require all review comments and inline threads to be explicitly resolved before approving. Do not resolve threads with pending unresolved technical concerns.

## 10. Evidence-Based Approval Verdict
Issue approval only when build artifacts, CI green gates, test reports, and review criteria are documented and satisfied.
