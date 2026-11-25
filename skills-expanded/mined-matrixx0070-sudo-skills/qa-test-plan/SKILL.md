---
name: qa-test-plan
version: 1.0.0
description: Write a focused test plan that scopes what will be tested, ranks risks, enumerates cases, and sets explicit entry and exit criteria.
author: matrixx0070
tags: [qa, test-plan, risk, coverage, criteria]
capabilities: []
---

## When to use

When a feature, release, or project needs a shared agreement on *what* gets tested, *how deeply*, and *when it's done* — before test execution starts. A test plan aligns QA, dev, and stakeholders on scope and risk so nobody discovers a gap at ship time.

**Not for:** writing individual test cases in detail (the plan lists them, it doesn't author each step), automation architecture (see qa-automation-strategy), or a one-line ad-hoc check. If there's no risk to negotiate and no stakeholder to align, skip the ceremony and just test.

## Method

1. **State scope explicitly** — list what IS in scope and what is OUT. The out-of-scope list prevents the most disputes. If scope is ambiguous, name the assumption and move on.
2. **Rank risks.** For each area, score likelihood × impact. Money, auth, data integrity, and external contracts default to High. Test effort follows risk — decision point: if an area is Low/Low, note it as "smoke only" rather than skipping silently.
3. **Enumerate test cases per area:** happy path, boundaries, error/failure paths, and any past bug. Reference case IDs; don't inline full steps.
4. **Pick test types per area** — decision point: pure logic → unit-level; seams and real dependencies → integration; a critical user journey → one end-to-end. Push cases to the cheapest layer that catches the defect.
5. **Define entry criteria** (what must be true to start: build deployed, test data seeded, environment green) and **exit criteria** (what must be true to stop: cases run, no open Critical/High, coverage of risk areas).
6. **List dependencies, environments, and owners** so blockers surface early.

## Example

```
Feature: password reset.
In scope: reset request, token validity, new-password rules, email delivery.
Out of scope: SSO login, account deletion.
Risk: token reuse (High), rate limiting (High), email copy (Low).
Cases: TC-01 valid reset, TC-02 expired token, TC-03 reused token,
       TC-04 weak password rejected, TC-05 rate-limit after 5 tries.
Entry: staging build v2.3, mailhog configured. Exit: all High cases pass, 0 open Critical/High.
```

## Pitfalls

- **No out-of-scope list** — every gap becomes a "you didn't test that" argument.
- **Flat risk** — treating a Low/Low banner the same as the payment path, wasting effort.
- **Vague exit criteria** — "tested enough" is not a criterion; tie exit to open-bug severity.
- **Plan as novel** — a 20-page document nobody reads. Keep it a skimmable table.

## Output format

```
Feature/Release: <name + build>
Scope — IN: <areas>   OUT: <areas>
Risk table: area | likelihood | impact | test depth
Test cases: ID | area | type (unit/integ/e2e) | priority
Environments & test data: <where, what seed>
Entry criteria: <checklist>
Exit criteria: <checklist tied to bug severity + risk coverage>
Dependencies & owners: <blockers, who owns each area>
```
