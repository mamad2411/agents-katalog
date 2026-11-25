---
name: planner-impact-and-invariants
description: Use when aligned approved inputs need repository impact, reuse, contract, and consistency decisions before slicing.
---

# Map impact and invariants

## Inputs
Matching approved PRD/Design revisions, authorised repository scope, current interfaces, service/data ownership, runtime topology, and repository rules.

## Procedure
1. Verify input revisions, approval receipts, Design readiness/not-required state, Engineering owner, and repository scope; stop on mismatch.
2. Inspect existing seams, contracts, owners, analogous paths, and engineering standards before proposing structure.
3. Map affected components, interfaces, schemas, security boundaries, consumers, and operational owners with locators and exclusions.
4. Define allowed actors, source/target states, refusal outcomes, idempotency identity and fingerprint, replay/conflict behaviour, expected-version semantics, and where latest state is read.
5. Enumerate mutations and side effects that must succeed or fail together. Name the actual process, store, transaction, and service boundary.
6. For distributed work, address durable uniqueness, transaction scope, outbox/publication, crash recovery, reconciliation, and consumer idempotency.
7. Separate verified facts, choices, risks, teaching shortcuts, and business questions; return business ambiguity.

## Output
An aligned impact map, reuse/contract decisions, invariant register, consistency-boundary record, assumptions, and blockers.

## Stop condition
Stop when required scope is unavailable, ownership conflicts, atomicity cannot be reasoned about, or an invariant would depend on guessed Product or Design policy.
