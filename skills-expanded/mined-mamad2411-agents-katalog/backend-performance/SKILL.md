---
name: backend-performance
description: >-
  Measure and improve latency, throughput or resource use in server-side request handling, background processing or data access. Use when profiling or a server-side budget identifies a backend bottleneck.
---

# Backend performance

## When to use

In the `implementation` phase of a `refactor` or `feature` run that targets performance, once `profiling` has located
the bottleneck in server-side code. It always starts from a measurement.

## Required context

The baseline measurement and profile from `profiling`. Useful: the architecture context
(data stores, caches, remote services on the path) and the integrations context.

## Preconditions

- A baseline measurement and a profile exist.
- The metric is a percentile, not only an average: tail latency is what users feel under
  load.

## Procedure

1. **Classify the time** the profile shows: computing, waiting on storage, waiting on
   remote calls, waiting on locks or pools. Each class has different fixes.
2. **Look for the usual causes**, in this order, because they are common and cheap to
   confirm:
   - one query or remote call per item inside a loop, instead of one for the batch;
   - data loaded and then discarded: unused columns, unused relations, missing limits;
   - lookups the data store cannot serve from an index;
   - remote calls made one after another that do not depend on each other;
   - pools (connections, threads) too small for the load, so requests queue;
   - repeated work on unchanged input that a cache could serve.
3. **Fix one cause**, then measure again with `profiling`.
4. **For caching**, decide before writing it: what the key is, how entries are
   invalidated, how stale a result may be, what happens on a miss storm. A cache
   without an invalidation answer is a correctness bug waiting.
5. **For concurrency**, check shared state, ordering assumptions and limits on the
   collaborators you now call in parallel.
6. **Check the effect on collaborators**: a faster service can overload the next one.

## Tools

None. Measurement tools come from `profiling`.

## Rules

None beyond those that apply by scope; the measurement rule is enforced through
`profiling`.

## Verification

Required: `performance`. Recommended: `integration`, to show data access and remote
calls still behave the same.

## Evidence

Baseline and result measurements for the changed path.

## Completion criteria

- The measured percentile meets the target, measured as the baseline was.
- Cache invalidation and concurrency limits are stated for any cache or parallelism
  added.

## Failure modes

| Failure | Signal | Response |
|---|---|---|
| Stale data | Cache serves results that should have changed | Fix invalidation before keeping the cache |
| Load moved, not removed | Downstream latency or errors rise | Measure the collaborator; add limits |
| Average improved, tail did not | Median drops, high percentile unchanged | Profile the slow requests specifically |
| Contention introduced | Throughput drops under parallel load | Revisit shared state and pool sizes |

## References

None.
