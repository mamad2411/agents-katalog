---
name: builder-baseline-and-red
description: Use when starting an authorised implementation increment and proving the target behaviour is not already satisfied.
---

# builder-baseline-and-red

## Inputs
Accepted plan, explicit change authority, base revision, repository rules, criterion, environment, and proof seam.

## Procedure
1. Verify authority covers every intended code, test, migration, and configuration surface.
2. Run baseline checks and separate pre-existing failures from the criterion.
3. Write or select one public-seam check for the criterion; run it before implementation.
4. Accept RED only when it fails for the intended missing or wrong behaviour, not import, syntax, harness, or unrelated failure.

## Output
A pinned baseline and causal RED receipt with command, exit, failure, target, and criterion.

## Stop condition
Stop on missing authority, dirty/unknown base, unusable environment, unrelated RED, or already-green criterion that lacks an explained evidence path.
