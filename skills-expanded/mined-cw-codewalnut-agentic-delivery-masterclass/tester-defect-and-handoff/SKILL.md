---
name: tester-defect-and-handoff
description: Use when failures need minimal reproduction and all claims need coverage classification for Reviewer.
---

# tester-defect-and-handoff

## Inputs
Execution receipts, exact target/environment identity, and material-delta record.

## Procedure
1. Reduce each failure to the smallest reproducer that still demonstrates the acceptance or risk breach.
2. Record expected, actual, preconditions, command, exit, and target identity.
3. After a repair, require a new exact target and rerun the reproducer plus affected evidence.
4. Classify every claim supported, failed, blocked, or unassessed; list confidence limits.

## Output
A `tested`, `failed`, or blocked Reviewer handoff with reproducible defects and claim-level evidence.

## Stop condition
A changed expectation needs owner approval; a changed target invalidates earlier evidence until rerun.
