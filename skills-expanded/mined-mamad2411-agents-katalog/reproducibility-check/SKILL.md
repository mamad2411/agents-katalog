---
name: reproducibility-check
description: Use before claiming an experiment improved results, before sharing numbers, or when another person needs to rerun or trust the outcome
---

# Reproducibility Check

No performance claim without attached evidence.

## Claim Gate

Before saying "this is better" or "the bug is fixed", verify:

1. exact command or launcher entrypoint
2. config path or config diff
3. seed or seed set
4. commit hash
5. dataset version or split
6. checkpoint or artifact path
7. metric table that supports the claim

Read `references/evidence-checklist.md` when you need the full checklist.

## Rules

- Single-run improvements are provisional unless the user explicitly accepts single-run evidence.
- If the comparison is not apples-to-apples, say so plainly.
- If you cannot reproduce the exact setup, do not present the number as established.
- Include uncertainty, not just the best score.

## Minimum Reporting Standard

State:

- what changed
- what stayed fixed
- what metric moved
- how many runs or seeds support it
- what still needs confirmation
