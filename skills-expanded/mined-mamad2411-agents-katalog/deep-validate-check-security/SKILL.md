---
name: deep-validate-check-security
description: Validate security dimension — input validation, auth, secrets, injection, rate limit
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - check-secrets
  - report
---

## Goal

Check the security dimension of `/deep-validate` — input validation, authn/authz, secrets, injection, rate limiting

## Scope

- Used when `/deep-validate` dispatches to the `security` dimension, or invoked standalone
- Read-only: record findings — fix via `/deep-review-codebase` fix workflows

## Execute

### 1. Check Input Handling

> Goal: every input path is validated/sanitized

1. Check input validation and sanitization
2. Check parameterized queries prevent SQL injection

### 2. Check Auth And Exposure

> Goal: auth is correct and no secrets leak

1. Check authentication and authorization patterns
2. Check there are no hardcoded secrets or API keys — run `/check-secrets` for a deep pass
3. Check API security and rate limiting — run `/deep-review-codebase` on newly exposed endpoints
4. Record findings with severity + evidence

### 3. Report

> Goal: return findings to the parent

1. Table: `No.`, `Finding`, `Severity`, `Location`, `Recommendation`
2. Security findings are always listed with Critical first

## Rules

- Confirmed hardcoded secret = Critical
- State a short exploit path in each finding — no generic flags
- Full deep security review → delegate to `/deep-review-codebase`

## Expected Outcome

- Findings of the security dimension with severity and evidence
