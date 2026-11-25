---
name: test-driven-development
description: Use when implementing a code task so the test is written or updated before production code and proves the requested behavior.
---

# Test-driven Development

## Red-Green-Refactor
1. Pick one REQ/task.
2. Write or update the smallest failing test first.
3. Run it and record the failing command/output.
4. Implement the minimum production change.
5. Run the targeted test, then the broader suite.
6. Refactor only with tests green.

Do not add production behavior that is not covered by a requirement or regression test.

