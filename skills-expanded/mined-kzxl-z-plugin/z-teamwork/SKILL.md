---
name: z-teamwork
description: Multi-agent subagent team coordination with zero-collision file ownership contracts, parallel partitioning, and adversarial review gates.
---

# Z-Teamwork Subagent Protocol

## 1. Zero-Collision File Ownership Contract
Before launching subagents in parallel:
- Every file or directory MUST be assigned to exactly ONE subagent.
- Subagents are strictly forbidden from modifying files outside their assigned scope.

## 2. Partitioning Strategy
- **Worker 1 (Logic/Implementation)**: Focuses exclusively on production code files.
- **Worker 2 (Tests/Verification)**: Focuses exclusively on test files and benchmarks.
- **Lead / Reviewer Agent**: Integrates artifacts, runs build/test suite, and verifies invariants.

## 3. Adversarial Review Gate
Prior to concluding a task, the team must execute an adversarial pass:
- Test edge cases, negative inputs, and boundary data.
- Confirm zero regressions against baseline test suites.
- Verify atomic conventional commit format.
