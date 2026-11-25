---
name: 6phase
description: Mandatory 6-phase development workflow — brainstorm, plan, develop, test, document, commit. Enforces structured, stack-agnostic delivery with approval gates.
---

# 6phase — Router

## Triage

Classify the task before any code:

| Signal | Track | Path |
|---|---|---|
| Bug fix, docs-only, config, ≤3 files, clear fix | **Fast** | P3 → P6 |
| New feature, arch decision, unclear reqs, multi-module, refactor | **Full** | P1 → P2 → P3 → P4 → P5 → P6 |

Any Full signal overrides all Fast signals. User can override in either direction.

Emit triage result:
```
## [6PHASE: TRIAGE → FAST | reason: ...]
## [6PHASE: TRIAGE → FULL | reason: ...]
```

## Phase Tracking

On entering each phase, emit:
```
## [6PHASE: Px-NAME]
```
Example: `## [6PHASE: P3-DEV]`

If you lose track, scan for the last `[6PHASE: Px-...]` marker to recover position.

## Gates

⛔ GATE: Do NOT proceed past P1 until user says "approved" or "go ahead."
⛔ GATE: Do NOT proceed past P2 until user says "approved" or "go ahead."
⛔ GATE: Do NOT proceed past P4 until user says "approved" or "go ahead."

## Phase Loading

You MUST read the phase file before doing any phase work:

| Phase | File |
|---|---|
| P1 Brainstorm | `phases/p1-brainstorm.md` |
| P2 Plan | `phases/p2-plan.md` |
| P3 Dev | `phases/p3-dev.md` |
| P4 Approve | `phases/p4-approve.md` |
| P5 Docs | `phases/p5-docs.md` |
| P6 Commit | `phases/p6-commit.md` |

## Fast Track

Fast-track tasks go P3 → P6 only. No design doc, plan, or docs phase.
Before P6, confirm: **"Tests pass: yes/no."** No formal test report needed.
P6 includes a one-line STATUS.md entry for traceability.

If the task turns out bigger than expected, escalate:
```
## [6PHASE: ESCALATE → FULL | reason: ...]
```
- Escalate to P1 if the problem is unclear or the approach is uncertain.
- Escalate to P2 if the problem is understood but needs a plan.
- Keep work already done; write design/plan to account for it.

## Session Resumption

On a new session for in-progress work, determine current phase:
- Design doc exists, no plan → P2
- Plan exists, implementation incomplete → P3
- Implementation complete, no test report → P4
- Test report exists, docs not updated → P5
- Everything done, not pushed → P6
- Nothing exists → new task, run triage
