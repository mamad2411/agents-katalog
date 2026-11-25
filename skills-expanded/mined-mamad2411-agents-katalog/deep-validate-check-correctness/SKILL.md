---
name: deep-validate-check-correctness
description: Validate correctness dimension — requirements, logic, edge cases, error handling
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - report
---

## Goal

Check the correctness dimension of `/deep-validate` — meets requirements, correct logic, complete edge cases, no missing error handling

## Scope

- Used when `/deep-validate` dispatches to the `correctness` dimension, or invoked standalone
- Read-only: record findings with severity — do not fix code

## Execute

### 1. Check Against Requirements

> Goal: confirm the code meets the requirements

1. Run `/deep-review-codebase` to check correctness
2. Check correctness against the principle or standard
3. Verify it works per the requirements and has no errors

### 2. Check Logic And Edge Cases

> Goal: logic covers the edge cases

1. Check that logic and edge cases are handled
2. Check that error handling is complete
3. Record findings with severity (Critical/High/Medium/Low) + evidence (file, line)

### 3. Report

> Goal: return findings to the parent

1. Table: `No.`, `Finding`, `Severity`, `Location`, `Recommendation`
2. Always note what is already correct

## Rules

- Every finding must have evidence (file path, line number)
- Separate "violates a requirement" from "style issue" — style goes to `check-quality`

## Expected Outcome

- Findings of the correctness dimension with severity and evidence
