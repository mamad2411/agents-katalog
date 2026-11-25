---
name: reviewer-decision-and-recheck
description: Use when issuing or updating a bounded review recommendation after evidence is complete or changes.
---

# reviewer-decision-and-recheck

## Inputs
Acceptance/risk findings, target identity, evidence cutoff, release constraints, and material-delta list.

## Procedure
1. Issue changes_requested, merge_candidate, or blocked for the exact target and inspected scope.
2. Keep merge recommendation separate from deployment/release gaps and human authority.
3. For each later code, test, fixture, environment, or evidence delta, decide whether it is material and rerun affected checks.
4. Supersede the old receipt rather than silently editing its history.

## Output
A revision-bound recommendation, release-gap register, and delta/recheck record.

## Stop condition
Recommendation never grants merge, deployment, release, publication, or risk acceptance.
