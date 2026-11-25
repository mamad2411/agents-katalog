---
name: verify-against-spec
description: Verifies an implementation against its spec criterion by criterion. It maps every acceptance criterion to tests and code, fills coverage gaps with reproduction scripts, lists deviations that are not criteria, and writes a verification report. Use it whenever the user asks to check the implementation against the spec, which criteria are met or not, whether the work is complete, or for a coverage or compliance report before review or merge.
---

# Verify against spec

Passing tests are not the goal. The question is "is every promise in the spec kept, and how do we know".

## 1. Collect evidence

1. Run the full check and record the result.
2. List every test name with a verbose reporter, for example `npx vitest run --reporter=verbose` or `pytest -v`.
3. For each acceptance criterion, find the tests that cover it and the code that implements it.

## 2. Classify each criterion

| Level | Meaning |
| --- | --- |
| Suite, full | A test in the suite covers every part of the criterion |
| Suite, partial | Tests cover part of it; you checked the rest with a script now |
| Logic tested, entry point manual | The logic has tests; you checked the command or script around it by hand |
| Manual only | The spec says it is manual, or no automated check is possible |
| ❌ Not met | The behavior differs from the criterion |

Be strict. A test that checks the ids in a list does not cover "shows id, customer, total and state".

## 3. Check the gaps with a script

Change no source file and make no commit in this step. New tests come after the user says yes. For every partial criterion, write a small script in `.scratchpad/<slug>/scripts/verify-gaps.*` that exercises the missing part (for example through the test client of the framework). Build the app the way the test setup does (seed data, test secrets) so the script sees the same state. Run it and record the result. Keep the script. It is the starting point for new tests.

Check command-line and startup criteria with real commands against a scratch database.

## 4. Look beyond the criteria

Compare the spec's other sections with the code: architecture, code layout, error pages, environment variables, scripts. List deviations with a traffic light (`traffic-light-findings`).

## 5. Report

Write `.scratchpad/<slug>/verification-report.md`:

```markdown
# Verification report: implementation vs spec

## Summary          counts per level, criteria not met
## How it was verified
## Detail per criterion   tables by area: AC | Result | Evidence
## Deviations (not criteria)
## Recommended test gaps  the partial criteria, as test proposals
```

In the chat, give the summary, the deviations and the recommendation. Offer to turn the gaps into tests.
