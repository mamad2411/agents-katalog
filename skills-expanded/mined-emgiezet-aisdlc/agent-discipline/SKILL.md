---
name: agent-discipline
description: Always-on agent behavior rules: linter suppression policy, required test gates, test deletion, remote scripts and look-alike packages, credential handling, scope discipline.
user-invocable: false
---

# Agent discipline — always-on rules — do not write these

Enforced by pre-write and pre-bash policies. Full text on invocation.

## Blockers
- AP-AGENT-001 — Suppression comments require ≥10-char justification; bare suppressions are blocked pre-write.
- AP-AGENT-004 — curl | sh is always blocked; an install whose name resembles a popular package needs confirmation.
- AP-AGENT-005 — Reading `.env*`, private keys, and credential files is denied; find values via safe alternatives.
- AP-AGENT-006 — Use placeholder values in code examples; real credentials must never appear in written files.

## Errors
- AP-AGENT-002 — Weakening a required test gate needs human review; linter thresholds are recorded, not gated.
- AP-AGENT-003 — Fix failing tests by correcting the code; never skip, mark incomplete, or delete tests to clear CI.
- AP-AGENT-009 — Pin new dependencies to an explicit stable version; never use `@latest` or loose ranges.

## Warnings
- AP-AGENT-007 — Restrict edits to the lines required by the task; do not reformat or refactor out of scope.
- AP-AGENT-008 — Before calling any framework API, verify the version-specific docs via Context7.
- AP-AGENT-011 — Resolve a finding by establishing its guarantee (parse, narrow, test the failure path), not by moving a cast or renaming a check.

Details for any ID: `reference/<ID>.md`
