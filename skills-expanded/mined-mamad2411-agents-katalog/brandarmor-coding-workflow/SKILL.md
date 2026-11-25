---
name: brandarmor-coding-workflow
description: 4-step AI coding workflow from @brandarmor.ai — Plan, Attack, Build, Verify — using two independent AI sessions so the builder never approves its own work, catching more bugs before shipping.
---

# 4-Step AI Coding Workflow
Catches More Bugs. The Builder Never Approves Its Own Work.
*From @brandarmor.ai*

Use 2 fresh AI sessions with different jobs:
- **Session A** — Plan + Build
- **Session B** — Attack + Verify

---

## Step 1 – Create the Plan (Session A)

```
Before writing code, inspect the repository and interview me one question at a time. Resolve the goal, constraints, edge cases and risks. Do not write code. When every decision is clear, save the approved plan to PLAN.md.
```

---

## Step 2 – Attack the Plan (Session B)

```
Read PLAN.md and inspect the repository in read-only mode. Challenge every assumption. Find security risks, missing edge cases, race conditions, breaking changes and unnecessary scope. Do not write code. For every problem, give one concrete fix. End with exactly one verdict: APPROVED or REVISE.
```

---

## Step 3 – Build the Approved Plan (Session A)

```
PLAN.md has been independently approved. Implement it exactly. Do not add features or expand scope. If the repository conflicts with the plan, stop and explain instead of guessing. Run the relevant tests, lint and type checks. Record changed files, commands, results and any deviations in BUILD_REPORT.md.
```

---

## Step 4 – Verify Before Shipping (Session B)

```
Compare the code diff against PLAN.md. Review every changed line. Look for security issues, regressions, broken contracts, unhandled errors and missing tests. Run the relevant tests, lint and type checks. Do not edit the code. End with VERDICT: PASS or VERDICT: FAIL. For every failure, include file, line, reason and exact fix.
```

---

## How It Works

```
Session A (Plan + Build) → PLAN.md → VERDICT → CODE DIFF → TEST REPORT → Session B (Review + Verify)
```

**Rule: The builder never approves its own work.**
