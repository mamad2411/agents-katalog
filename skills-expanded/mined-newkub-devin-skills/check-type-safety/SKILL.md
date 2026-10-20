---
name: deep-validate-check-type-safety
description: Validate type safety dimension — typecheck, any/ts-ignore, type flow
argument-hint: "[scope]"
related:
  - run-typecheck
  - deep-review-codebase
  - report
---

## Goal

Check the type safety dimension of `/deep-validate` — type errors, unnecessary `any`/`@ts-ignore`, and type flow from schema to UI

## Scope

- Used when `/deep-validate` dispatches to the `type-safety`/`types` dimension, or invoked standalone
- Read-only: record findings — do not fix types

## Execute

### 1. Run Typecheck

> Goal: all type errors with locations

1. Run `/run-typecheck` to check type errors
2. Record errors with file:line

### 2. Check Weak Types

> Goal: find type escapes that reduce safety

1. Check there are no unnecessary `any` — run `/deep-review-codebase` for a coverage metric
2. Check there are no `@ts-ignore` or `@ts-nocheck`
3. Check type inference is used correctly

### 3. Check Type Flow

> Goal: types flow continuously across the stack

1. Check type flow: schema → validation → API → UI
2. Flag points where the type chain breaks (manual re-declaration, unsafe casts)

### 4. Report

> Goal: return findings to the parent

1. Table: `No.`, `Finding`, `Severity`, `Location`, `Recommendation`

## Rules

- Necessary `any` (e.g. an untyped third-party boundary) should be annotated, not flagged
- Severity: real type error = High+, weak types = Medium/Low

## Expected Outcome

- Findings of the type safety dimension with severity and evidence
