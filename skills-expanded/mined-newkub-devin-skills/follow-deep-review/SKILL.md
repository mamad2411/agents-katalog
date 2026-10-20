---
name: follow-deep-review
description: Enforce following deep-review-codebase — run/read findings before planning or changing anything
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - create-plan-in-dot-devin
  - report
  - suggest-next-action
---

## Goal

Ensure the next piece of work follows `/deep-review-codebase` — always have the latest findings first, and every action references real findings; never plan or change based on assumptions

## Scope

Use before `/create-plan-in-dot-devin`, implementation, or refactoring that needs evidence from review — aggregate findings from a `/deep-review-codebase` report or dimensional reviews already run

- See also: /deep-review-codebase, /deep-review-codebase

## Execute

### 1. Check Existing Findings

> Goal: find the latest review findings that already exist

1. Check whether recent deep-review-codebase findings exist for this scope (in-session report, report files, dimensional review results)
2. If findings are stale or not broad enough → run `/deep-review-codebase` on that scope
3. If dimensional findings are scattered → run `/deep-review-codebase` to consolidate them into a prioritized list

### 2. Extract Relevant Findings

> Goal: select only findings relevant to the work scope

1. Filter findings by scope: relevant files, domains, severity
2. Prioritize: Critical/High first — these findings must be included in the plan
3. Identify out-of-scope findings with a reason — never discard them silently

### 3. Follow Findings

> Goal: map findings to the work to be done

1. Every in-scope Critical/High finding must map to a task or constraint in the plan
2. Identify findings that block the main work — fix them first, or state a workaround
3. If findings conflict with the requirements → stop and `/ask-me`

### 4. Report

> Goal: summarize how the findings were used

1. Run `/report` with columns: `No.`, `Finding`, `Severity`, `Action`, `Mapped To`
2. Run `/suggest-next-action` — normally `/create-plan-in-dot-devin` or `/deep-review-codebase-then-fix`

## Rules

- Never start planning/implementation without the latest findings — if none exist, run `/deep-review-codebase` first
- Never cherry-pick only convenient findings — all Critical/High findings must be addressed or escalated
- Findings must be traceable — every action links back to its source finding
- This skill does not fix findings — it only collects them and enforces that the next work follows them

- Use /deep-review-codebase-then-fix if needed
- Use /loop-until-complete if needed

## Expected Outcome

- The latest findings are always ready before the main work starts
- Every in-scope Critical/High finding is mapped to the work
- The next task (`/create-plan-in-dot-devin`, implementation) has a clear evidence base
- The findings → actions mapping report is complete
