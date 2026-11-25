---
name: code-verification
description: |
  Verifies code changes with repository-native builds, tests, linters, formatters, and type checks.
  Use before completion or merge to gather command-backed evidence of correctness.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Code Verification

Use this skill to prove that a change works through the target repository's native quality gates.

## Workflow

1. Discover the project's documented commands and configuration; do not assume every ecosystem uses the same tools.
2. Run the narrowest relevant checks first, then the repository's build, tests, lint, formatter, and type checks as applicable.
3. Use `scripts/verify-pipeline.sh` as an optional baseline runner when it fits the repository. Run it from the target project root (or pass that root as its first argument); it detects common Node, Rust, and Python checks.
4. Record every command, result, skipped check, and environment limitation. Never report a skipped check as a pass.
5. Investigate failures, apply only necessary fixes, and rerun affected checks.

## Completion Standard

A verification result states what was executed, what passed or failed, and what could not be run. Static checks do not replace runtime validation for client-facing changes; use **runtime-devtools-audit** when appropriate.
