---
name: phxstack-forward-implementation-first
description: Keep implementation and focused validation ahead of administrative metadata. Use for staged, generated, long-running, or multi-agent work where tracking artifacts obstruct delivery.
---

# phxstack-forward-implementation-first

Use this as a companion discipline for long-running or staged work. It does
not replace the phxstack router or an active workflow, and it does not bypass
an approved spec, substantive verification, or explicit approval to push.

## Decision rule

Before each action, classify it as one of:

1. **Semantic implementation**: build or connect a producer, consumer,
   adapter, runtime path, schema, fixture, or final output.
2. **Focused validation**: test the changed dependency cone through behavior,
   schema, counts, samples, conservation, consistency, nontruncation, or
   measured resources.
3. **Administrative bookkeeping**: generate or repair hashes, locks, receipts,
   dashboards, certification markers, progress metadata, or presence-only
   records.

Choose categories 1 and 2. Skip category 3 unless the developer asks for it,
the artifact is part of the product, or an external contract requires it. If
bookkeeping blocks a path without protecting correctness, remove that
dependency from the path.

## Phxstack fit

- Treat the approved `.phxstack/specs/<slug>.md` as implementation intent and
  workflow state. Keep it current when the active `phxstack-build` workflow
  requires step completion, but never treat its status, file presence, or a
  marker as evidence that the behavior works.
- Keep `phxstack-check` validation. Tests, reproductions, benchmarks,
  end-to-end runs, and inspected output are evidence, not bookkeeping.
- Keep `phxstack-push`'s developer approval and repository safety checks. This
  discipline does not authorize commits, pushes, deployments, or destructive
  changes.
- Keep durable project knowledge that a phxstack skill explicitly owns. Do not
  invent a second state store, receipt format, or certification surface.

## Hard constraints

- Build the producer and consumer before polishing status or certification
  surfaces.
- Do not generate, repair, compare, or propagate administrative hashes.
- Do not create or wait on filesystem locks for workflow bookkeeping.
- Do not rerun unchanged work only to regenerate a receipt or marker.
- Do not invalidate valid output because an administrative record is missing,
  stale, or incompatible.
- Do not move a forward cursor backward for an administrative metadata change.
- When one producer or consumer changes, replay only its smallest affected
  dependency cone.
- Do not claim a capability works because its file exists. Run the changed
  cone and inspect the result.
- Publish valid output after focused validation. Do not add a review cycle when
  no defect remains.

## Forward cursor and manual execution

A stage may move backward or be replayed only when at least one real condition
holds:

- its input meaning changed;
- its target or pinned revision changed;
- its output is malformed, truncated, nonconserving, internally inconsistent,
  or incompatible with its consumer;
- an observed run disproves the earlier static result; or
- the changed producer's declared dependency cone requires replay.

Missing or stale administrative metadata is not a reason. When an authorized
stage is blocked only by a receipt, certification marker, progress record,
administrative hash, or lock:

1. Run the exact stage manually.
2. Validate its output with the focused checks below.
3. Publish valid output atomically.
4. Continue from the forward cursor.
5. If within the task scope, remove or downgrade the administrative-only gate
   in the execution path. Otherwise report the gate and the smallest needed
   change without expanding the task.

Do not refuse an authorized manual run because the full pipeline cannot issue
a receipt. Do not send the developer to another agent or tool to get around
bookkeeping owned by the current workflow.

## Focused validation

Use the checks that match the change:

- runtime behavior and exit status;
- schema and type validity;
- exact input, output, accepted, rejected, and unknown counts;
- deterministic first, middle, and last samples;
- identity and partition conservation;
- join consistency and flag polarity;
- nontruncation and bounded diagnostic output; and
- wall-clock time and peak memory for material stages.

Hashes may identify inputs or revisions, but they never grant correctness,
execution, or roadmap credit. Keep product integrity checks, input and
revision identity, and execution records that carry the command, input,
result, and checked expectation. Their absence blocks only the claim they
support; it does not invalidate unrelated earlier stages.

## Execution discipline

- Run one heavy process at a time: a compiler, full test suite, large data job,
  benchmark, or long scan.
- Use parallel lanes only for useful, bounded, non-overlapping light work when
  the runtime supports it. Do not manufacture work to occupy a lane.
- The root lane owns heavy execution, publication, cursor movement, acceptance,
  and conclusions. Verify delegated output before using it as an input.
- Forward progress does not wait for every independent lane to finish. Consume
  a completed result when its dependency is reached and local checks pass.
- If a heavy run exposes a defect, fix that stage before rerunning its cone.
- If the next action is bookkeeping-only, select the next unresolved producer,
  consumer, adapter, or output instead.

## Status reporting

Report implemented behavior and measured output first. Keep workflow or
infrastructure progress separate from evidence about the output. Follow the
active phxstack skill's report format; never use administrative completion as
a substitute for working capability.
