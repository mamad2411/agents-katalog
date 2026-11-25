---
name: fagan-inspection
description: Run a formal Fagan Inspection on the current change set with (if available) parallel domain reviewers and a single consolidated defect log + verification.
argument-hint: "[optional scope hints]"
disable-model-invocation: true
---

Run a formal **Fagan Inspection** on the current change set. Optimize for defect discovery and verification.

## A) Scope

- Prefer existing chat context for intent + acceptance criteria.
- If missing, derive scope from git: status, staged/unstaged diff, and PR-range diff vs base (`origin/main` or `origin/master`).
- Summarize impacted modules/files + externally visible behavior changes.

## B) Plan (you decide domains dynamically)

- Define **Entry Criteria** (must be true to start) and **Exit Criteria** (must be true to finish).
- Choose only the reviewer domains needed for this change (examples: correctness, security, performance, reliability, API/design, tests, docs, ops, data/migrations, concurrency, UI).
- If parallel subagents are supported, spawn one per domain; otherwise run domains sequentially.

## C) Preparation (domain reviews)

Each domain reviewer outputs defects in this schema:

- **Title**
- **Severity:** MAJOR | MINOR
- **Domain**
- **Location:** file:line or symbol
- **What/Why + Evidence/Repro**
- **Fix:** specific change
- **Verify:** test/command/scenario

## D) Inspection meeting (synthesis)

- De-duplicate, re-severity, prioritize.
- Produce a single defect log + rework plan.

## E) Rework + follow-up

- Only change code if permissions/approval mode allows; otherwise give patch-level edits.
- Fix MAJOR first; add/update tests/docs for behavior changes; re-run relevant checks/tests; confirm Exit Criteria.

## OUTPUT: Fagan Inspection Report (Markdown)

1. Scope & intent source (chat or git)
2. Entry/Exit criteria
3. Overview + top risks
4. Defect log (table: ID | Sev | Domain | Location | Title | Status | Fix/Next)
5. Rework summary (if applied)
6. Verification evidence (commands/tests)
