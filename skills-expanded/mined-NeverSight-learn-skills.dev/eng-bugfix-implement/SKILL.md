---
name: eng-bugfix-implement
description: Implement a surgical bug fix based on an existing Root Cause Analysis (RCA) document. Use when applying bug fixes, adding regression tests, and verifying bug remediation.
---

# Bugfix Implement

Apply a verified bug fix guided by a Root Cause Analysis (RCA) document.

## Process

### 1. Ingest RCA
1. Read the RCA document (e.g. `docs/rca/issue-<id>.md` or provided RCA summary).
2. Confirm the root cause, target files, and proposed fix strategy.

### 2. Confirm Failing State (Red Phase)
1. Write or run the reproduction test to observe the expected failure before applying fixes.

### 3. Apply Surgical Fix (Green Phase)
1. Modify the target files with minimal necessary diff.
2. Adhere strictly to existing coding styles and patterns.

### 4. Regression & Verification Gate
1. Run the new regression test to confirm the fix works.
2. Run the full project test suite to verify zero side-effect regressions.

---

## Completion Checklist

- [ ] Reproduction test passes green.
- [ ] No regression across entire test suite.
- [ ] Code changes are minimal, focused, and clean.

---

## Checkable Completion Criteria

- [ ] RCA document ingested; fix maps directly to its documented root cause.
- [ ] The red reproduction test turns green without weakening any assertion.
- [ ] Full regression suite passes after the fix lands.
