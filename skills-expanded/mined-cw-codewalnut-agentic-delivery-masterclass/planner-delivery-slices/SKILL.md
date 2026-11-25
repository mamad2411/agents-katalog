---
name: planner-delivery-slices
description: Use when a technical approach must become dependency-ordered, independently provable implementation increments.
---

# planner-delivery-slices

## Inputs
Impact/invariant record, accepted scope, and delivery constraints.

## Procedure
1. Prefer narrow vertical slices that cross needed layers and produce observable behaviour.
2. Give each slice blockers, changed surfaces, owner, criterion links, pre-proof or RED, GREEN proof, and safe stop.
3. Use expand-migrate-contract for wide compatibility changes that cannot land as one green slice.
4. Keep Product or Design decisions outside technical tasks and route them back.

## Output
A dependency graph of reviewable increments sized for one bounded implementation context.

## Stop condition
Stop when a slice cannot be verified independently and no explicit integration boundary is accepted.
