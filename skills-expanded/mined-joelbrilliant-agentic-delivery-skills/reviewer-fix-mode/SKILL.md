---
name: reviewer-fix-mode
description: Defines strict review-then-fix authority for reviewers. Use when a reviewer is allowed to repair findings after review, when avoiding reviewer-as-stealth-builder drift, or when verifying that fixes stay limited to documented findings.
---

# Reviewer Fix Mode

## Overview

Use this skill when reviewers are allowed to fix issues they find.

Reviewer-fix mode is useful, but only if the review happens first and the fix scope is locked to documented findings.

## When to Use

- A reviewer may patch issues after review.
- A review found clear defects and the owner authorises direct repair.
- A strict harness lets reviewers fix after documenting findings.
- You need to stop reviewer scope drift.
- Orchestrator must final-sign off reviewer fixes.

## Non-negotiable Sequence

1. **Review first.** Write findings before editing.
2. **Declare mode.** Say reviewer-fix mode is starting.
3. **Fix only documented findings.** No opportunistic cleanup.
4. **Verify fixes.** Run targeted tests and relevant smoke checks.
5. **Report separately.** Keep review findings and fix evidence distinct.
6. **Return to orchestrator.** Reviewer does not self-merge by default.

## Finding Format

```text
### HIGH-1: [summary]
- Evidence: file.py:LN
- Regression analysis: if X changes, which test catches it?
- Fix scope: exactly what may change
```

## Fix Report Format

```text
## Reviewer-fix mode report

### Fixed findings
- HIGH-1: [what changed]

### Changed files
- path/file.py

### Verification
- command: result
- runtime/API/browser proof: result

### Out of scope
- [things noticed but not fixed]

### Remaining risk
- [none / listed]
```

## Allowed Fixes

Allowed:

- direct bug fixes for documented findings;
- regression tests for documented findings;
- small refactors required to fix the finding;
- docs updates that explain changed behaviour.

Not allowed without orchestrator approval:

- new features;
- design/product changes;
- broad formatting;
- architecture rewrite;
- unrelated test cleanup;
- changing public contracts beyond the finding.

## Orchestrator Final Check

The orchestrator checks:

- every fix maps to a documented finding;
- no unrelated files changed;
- tests prove the regression mode;
- production-shaped path is covered if relevant;
- reviewer did not silently become second builder.

## Stop Conditions

Stop and return to orchestrator if:

- a fix requires new scope;
- the finding is ambiguous;
- tests reveal adjacent unrelated failures;
- design direction changes;
- reviewer cannot verify the fix.
