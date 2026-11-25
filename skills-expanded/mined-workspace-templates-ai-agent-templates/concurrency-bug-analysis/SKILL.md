---
name: concurrency-bug-analysis
description: Finds races, deadlocks and lost updates by mapping shared state and lock order, then proposes the narrowest lock, queue or atomic operation that fixes them.
---

# Concurrency bug analysis

Reason first, then reproduce, then fix. A fix without a reproduction is a guess.

## Steps

1. Build the map. List every piece of shared mutable state (globals, singletons, caches, rows, files) and every thread, task, worker or request path that touches it. Mark each access as read or write.
2. Look for the usual shapes:
   - Check-then-act: `if (!exists) create`, `if (stock > 0) stock--`.
   - Read-modify-write without atomicity: `count = count + 1`, or a SQL `SELECT` then `UPDATE`.
   - Lock-order inversion: A takes lock 1 then 2, B takes 2 then 1.
   - Holding a lock across I/O or a callback.
   - Publishing an object before it is fully built; unsynchronized lazy init.
   - Shared iteration while another path mutates the collection.
3. Write the interleaving that breaks it as numbered steps for two actors. If you cannot write the interleaving, the finding is not proven; drop it.
4. Reproduce with a stress test: many parallel callers in a loop, a forced yield or sleep between the check and the act, or the language's race detector (`go test -race`, ThreadSanitizer, or the equivalent).
5. Choose the narrowest fix, in this order: remove the sharing; use an atomic or database operation (`UPDATE ... SET n = n + 1`, compare-and-swap, unique constraint); a queue that serializes writes; a lock held for the shortest code, with one global lock order.
6. Re-run the stress test many times and confirm the failure is gone.

## Rules

- Never add `sleep` or retries as the fix.
- Do not hold locks while calling unknown code.

## Report

The interleaving, the evidence, the fix, the test, and the remaining shared state you could not prove safe.
