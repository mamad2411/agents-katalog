---
name: deep-validate-check-compliance
description: Validate compliance dimension — requirements fit, conventions, regulatory
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - report
---

## Goal

Check the compliance dimension of `/deep-validate` — fit with requirements/context, project conventions (`AGENTS.md`), and regulatory requirements

## Scope

- Used when `/deep-validate` dispatches to the `compliance` dimension, or invoked standalone
- Read-only: record findings — do not fix

## Execute

### 1. Check Requirements Fit

> Goal: the solution fits the requirements and context

1. Check the fit with requirements or context
2. Check the fit with capabilities or constraints
3. Check the fit with scalability or maintainability

### 2. Check Conventions And Regulatory

> Goal: aligned with the applicable standards

1. Check compliance with project conventions (`AGENTS.md`)
2. Check compliance with regulatory requirements if any — run `/deep-review-codebase` for a deep pass
3. Record findings with severity + evidence

### 3. Report

> Goal: return findings to the parent

1. Table: `No.`, `Finding`, `Severity`, `Location`, `Recommendation`

## Rules

- regulatory violation = Critical/High; convention drift = Medium/Low
- State the standard/rule used as the criterion in each finding

## Expected Outcome

- Findings of the compliance dimension with severity and evidence
