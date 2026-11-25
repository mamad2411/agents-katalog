---
name: plan-tests
description: "Produces a test plan for a feature: the cases, the edge conditions, the data needed and which level each test belongs to."
disable-model-invocation: true
---

Write a test plan for: $ARGUMENTS

1. Read the code or spec for the feature, plus its callers and the data it touches. Note inputs, outputs, state changes, external calls and permissions.
2. List cases in four groups: normal paths, boundaries (empty, one, many, limit, limit plus one), failures (invalid input, timeouts, dependency down, duplicate requests, partial writes) and rules that depend on role, time or locale.
3. For each case give: a one-line description, the data it needs, the expected result, and the level (unit, integration, end-to-end) with a reason. Push cases down to the cheapest level that still catches the problem.
4. Identify what must be mocked or seeded and what needs a real service.
5. Mark each case with a priority: must have, should have, nice to have.
6. Note what is deliberately not tested.

Output a Markdown table per group followed by a short list of risks. Do not write test code or edit files. Ask which priority levels to implement first.
