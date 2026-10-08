---
name: ipo-verify-findings
description: Re-check previously reported implementation-review findings after targeted fixes, verify resolution without reopening a broad review, and determine archive readiness.
argument-hint: "[change-id] [finding-ids-or-report-path]"
---

# IPO Verify Findings

Perform a narrow, report-only verification pass after targeted fixes to findings produced by `ipo-review-implementation` or another independent review.

This skill exists to keep review loops bounded. It verifies known findings and regressions; it is not a new zero-base review.

## Guardrails

- Do not modify files.
- Do not fix findings.
- Do not edit OpenSpec artifacts or architecture documents.
- Do not archive the change.
- Do not create commits, push, or open a PR.
- Do not reopen unrelated LOW/style issues.
- If a new regression directly caused by the fixes is discovered, report it.
- If an unrelated BLOCKER/HIGH issue is unavoidably discovered, report it, but do not broaden the review further.

## Inputs

Use `$ARGUMENTS[0]` as the change id when supplied.
The remaining arguments may contain finding ids or a path to a saved review report.

The finding descriptions must be available from at least one of:

- the current conversation/context;
- a user-provided review report file;
- an explicitly supplied text block.

If only finding IDs are provided and their descriptions are unavailable, ask the user to provide the prior review report. Do not guess what an ID meant.

## Verification procedure

### 1. Load governing context

Read:

1. root `AGENTS.md`;
2. the approved OpenSpec change artifacts relevant to the findings;
3. only the architecture/ADR/contract sections needed to evaluate those findings.

Do not reload unrelated architecture documents.

### 2. Establish the fix diff

Inspect the diff introduced since the reviewed state when that state can be identified. Otherwise inspect the current feature diff and focus only on files/symbols referenced by the findings and their direct fix dependencies.

### 3. Verify each finding independently

For every requested finding:

- restate the governing requirement briefly;
- inspect the exact implementation and tests relevant to it;
- run focused non-mutating verification commands when useful;
- determine whether the original problem is fully closed.

Use only these statuses:

- `RESOLVED` — the original problem is fully addressed and verification supports the result;
- `PARTIALLY RESOLVED` — meaningful progress exists but at least one part of the original requirement remains unsatisfied;
- `NOT RESOLVED` — the original issue remains materially present;
- `WITHDRAWN` — the original finding was based on an incorrect interpretation of the normative architecture/spec and should not be fixed.

A finding may be `WITHDRAWN` only when exact normative evidence demonstrates that the review finding itself was wrong.

### 4. Check regressions caused by fixes

Inspect only the fix-adjacent behavior for regressions such as:

- contract generalization across types;
- validation ownership moving into the wrong layer;
- test fixtures being changed to non-normative shapes merely to pass tests;
- new redundant state/correlation fields;
- weakened validation;
- scope expansion;
- behavior changes unrelated to the accepted finding.

Classify new regressions with `BLOCKER`, `HIGH`, `MEDIUM`, or `LOW` and give a precise location.

### 5. Verification evidence

Run the smallest useful verification set for the findings. If the fixes affect persistence/integration behavior, include the relevant real database tests when available.

Do not claim checks passed when they were skipped or unavailable.

## Output format

For each finding:

```text
IR-001 — RESOLVED | PARTIALLY RESOLVED | NOT RESOLVED | WITHDRAWN
Evidence:
- <implementation evidence>
- <test/architecture/spec evidence>
```

Then provide:

```text
## New regressions
None
or

ID: REG-001
Severity: BLOCKER | HIGH | MEDIUM | LOW
Location:
Problem:
Why it matters:
Suggested direction:

## Verification
- <checks and outcomes>

## Archive readiness
READY FOR ARCHIVE
| NOT READY FOR ARCHIVE
```

Return `READY FOR ARCHIVE` only when:

- every requested BLOCKER/HIGH/MEDIUM finding is `RESOLVED` or `WITHDRAWN`;
- no new BLOCKER/HIGH/MEDIUM regression is present;
- required focused verification passes or any unavailable verification is explicitly accepted by the user.

LOW findings do not automatically block archive unless they represent a user-declared release gate.
