---
name: deep-validate-check-cross-references
description: Validate cross-reference dimension — config, module refs, API contracts, docs
argument-hint: "[scope]"
related:
  - check-reference
  - update-references
  - deep-review-codebase
  - report
---

## Goal

Check the cross-reference dimension of `/deep-validate` — config/env refs, module references, API contracts matching implementation, docs matching code

## Scope

- Used when `/deep-validate` dispatches to the `cross-reference`/`refs` dimension, or invoked standalone
- Read-only: record findings — fix via `/update-references`

## Execute

### 1. Check Config And Env References

> Goal: the config/env the code references actually exist

1. Verify the config files and environment variables the code uses actually exist
2. Flag env vars the code references but that are missing from `.env.example` or config

### 2. Check Module And Contract References

> Goal: internal references and contracts match

1. Verify references between modules are correct — run `/check-reference` for a deep pass
2. Verify API contracts match the implementation — run `/deep-review-codebase` if there is an API surface
3. Verify dependencies do not conflict with existing versions

### 3. Check Docs References

> Goal: documentation matches the real code

1. Verify documentation matches the actual code
2. Flag docs that reference APIs/files that no longer exist

### 4. Report

> Goal: return findings to the parent

1. Table: `No.`, `Finding`, `Severity`, `Location`, `Recommendation`

## Rules

- A broken reference that breaks runtime = High; stale docs = Low
- Every finding names both sides of the reference (source → missing target)

## Expected Outcome

- Findings of the cross-reference dimension with severity and evidence
