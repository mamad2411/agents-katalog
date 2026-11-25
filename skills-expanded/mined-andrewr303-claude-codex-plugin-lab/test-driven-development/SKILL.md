---
name: test-driven-development
description: Use when adding behavior, fixing bugs, or changing logic where a focused failing test can be written first.
---

# Test Driven Development

Use red/green/refactor where it gives leverage.

## Loop

1. Define the smallest behavior slice.
2. Write or identify a failing test that expresses the behavior.
3. Run it and confirm it fails for the expected reason.
4. Implement the minimal fix.
5. Run the test and confirm it passes.
6. Refactor only after green.
7. Run adjacent checks proportional to risk.

## Rules

- Do not weaken or delete meaningful assertions to get green.
- Do not mock the behavior under test so completely that the test proves nothing.
- Prefer focused tests before full suites.
- If no automated test is feasible, write a deterministic manual check and label it manual.
- For bug fixes, preserve the failing input as a regression case when possible.

