---
name: implementation-quality
description: "Use for non-trivial code changes after the plan is confirmed. Enforces target-state implementation: minimal necessary scope, existing patterns, no avoidable MVP residue, no duplicate logic, synchronized callers/tests/types/errors/config, and verification."
---

# Implementation Quality Adapter

Default mode is target-state implementation, not throwaway MVP.

## Before Editing

- Identify the impact set: edit files, callers, tests, configs, docs.
- Find same-pattern project code.
- Verify API/library facts when needed.
- Pick the smallest complete implementation path.

## During Editing

- Implement the confirmed target design directly.
- Avoid temporary glue, duplicate logic, speculative abstraction, and core TODOs.
- Keep changes integrated across callers, tests, types, errors, and config.
- If the task must be staged, each stage must be coherent and aligned with the final architecture.

## Before Completion

- Re-read the diff.
- Remove avoidable redundancy.
- Run or report the relevant verification.

