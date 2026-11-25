---
name: builder-bounded-change
description: Use when implementing one approved increment from a causal RED or equivalent agreed pre-proof.
---

# builder-bounded-change

## Inputs
Pinned baseline/RED receipt, one plan increment, and repository instructions.

## Procedure
1. Change only surfaces named by the increment and authority.
2. Implement only enough to satisfy the criterion and preserve accepted invariants.
3. Run the focused check after each coherent change; use the failure to choose the next edit.
4. Record any newly required scope, policy, Design, contract, migration, or configuration change as a deviation instead of absorbing it.

## Output
A minimal diff for one increment, focused GREEN, and an exact deviation list.

## Stop condition
Stop before any change outside authority or accepted plan. Do not weaken the expectation merely to obtain green.
