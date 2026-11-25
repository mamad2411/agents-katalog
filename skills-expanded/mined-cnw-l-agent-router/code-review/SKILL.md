---
name: code-review
description: Use for review, PR review, audit, self-review, and regression-risk work. Prioritizes bugs, regressions, missing tests, architecture drift, redundancy, security risk, and verification gaps.
---

# Code Review Adapter

Use Superpowers review workflows as the default methodology.

## Route

- Review or audit request: use `superpowers:requesting-code-review`.
- Review feedback to address: use `superpowers:receiving-code-review`.
- Security/privacy/trust-boundary risk: also use `security-review`.
- Branch, PR, CI, or GitHub review comments: use `pr-workflow`.

## Findings Policy

Report findings first, ordered by severity. Focus on real bugs, regressions, security/privacy risks, broken contracts, missing tests, unnecessary complexity, duplicate logic, and target-state violations. If no issues are found, say so and mention remaining verification gaps.
