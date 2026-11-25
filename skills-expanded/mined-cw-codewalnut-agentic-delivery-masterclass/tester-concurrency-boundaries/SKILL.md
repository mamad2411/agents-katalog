---
name: tester-concurrency-boundaries
description: Use when an acceptance claim or risk depends on simultaneous attempts, ordering, uniqueness, or exactly-once effects.
---

# Test concurrency within a named boundary

## Inputs
Concurrency invariant, exact target, synchronisation method, worker count, store/process topology, and required state and side-effect assertions.

## Procedure
1. Name the process, worker, store, transaction, and integration boundary the environment can exercise.
2. Synchronise attempts at the contested operation; verify the synchronisation is effective.
3. Assert outcomes, final state/version, uniqueness, and every required or forbidden side effect.
4. Repeat enough to expose instability while retaining commands, seeds, timing controls, and receipts.
5. List unexercised boundaries such as multiple workers, database isolation, crash recovery, publication, delivery, or consumer deduplication.

## Output
A bounded concurrency receipt plus explicit unsupported dimensions.

## Stop condition
Stop when topology is unknown, synchronisation is ineffective, results are unstable without a reproducible account, side effects cannot be inspected, or the claim exceeds the environment.
