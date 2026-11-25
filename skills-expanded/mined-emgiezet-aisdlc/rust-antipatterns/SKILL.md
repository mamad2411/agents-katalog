---
name: rust-antipatterns
description: Forbidden Rust patterns — unsafe without safety comment, unwrap in library code, unchecked integer arithmetic. Applies when editing Rust files.
paths: ["**/*.rs"]
user-invocable: false
---

# Rust anti-patterns — do not write these

Checks run automatically after each edit. Findings reference the IDs below.

## Errors
- AP-RS-SEC-001 — Every `unsafe` block must have a `// SAFETY:` comment explaining the soundness invariant.
- AP-RS-SEC-003 — Validate raw pointers before dereferencing; prefer safe references; document the safety invariant.
- AP-RS-SEC-004 — Avoid `mem::transmute`; use `From`/`Into` or `bytemuck`; document layout guarantees in SAFETY comments.
- AP-RS-SEC-005 — Use `str::from_utf8(&bytes)?` instead of `from_utf8_unchecked`; propagate the validation error.

## Warnings
- AP-RS-SEC-002 — Return `Result`/`Option` from library functions; use `.unwrap()` only in tests or `main`.
- AP-RS-PERF-001 — Use `checked_add`/`checked_mul` for size/offset arithmetic; never rely on silent wrapping.
- AP-RS-MAINT-001 — Add `#[serde(deny_unknown_fields)]` to structs that deserialise external input.

Details for any ID: `reference/<ID>.md`
