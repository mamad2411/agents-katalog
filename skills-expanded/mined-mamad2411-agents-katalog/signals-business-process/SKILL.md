---
name: signals-business-process
description: Create, modify, diagnose, or review reusable Signals BusinessProcess commands, queries, calculations, state transitions, and orchestrations. Use for Auth/Validate/Handle lifecycle work, typed process results, child Continue composition and fault propagation, Core process placement and naming, direct-dispatch security, or extracting reusable behavior from Web or Worker code.
---

# Signals business process

## Purpose

Implement a focused, reusable Core use case through the supported synchronous Signals lifecycle.

Use the distributed or recurring skill when its lifecycle is the primary concern.

## Gather inputs

- Identify the use-case contract, callers, result shape, and expected faults.
- Identify actor and ownership rules and the direct-dispatch trust policy.
- Inventory all required input preconditions: root/shape, referenced-resource existence, caller access/ownership, current state, relationships/conflicts/limits, and other complex business rules.
- Classify child effects as required or optional and identify local and cross-system consistency requirements.

## Consult documentation

Read [business processes](../../docs/signals/business-processes.md), [process composition](../../docs/signals/process-composition.md), and [results/errors](../../docs/signals/results-and-errors.md). Open only the matching cards in [`patterns/index.md`](../../patterns/index.md) and one example from [`canonical-examples.md`](../../references/canonical-examples.md).

## Search

1. Search the operation/feature, existing process types, callers, `Continue` chains, result/error codes, ports, and tests.
2. Confirm whether an existing process already owns the use case or a reusable child.
3. Search the relevant host scan graph and names to avoid undiscovered processes or identity collisions.

## Implement

1. Place the descriptively named process in Core Processes, in its own matching `.cs` file, and use the smallest supported input arity/stable request object.
2. Keep Domain classes and records out of the process file and process class; define them in separate Domain source files.
3. Implement every required process precondition as a named rule specification, including repository-backed existence, access/ownership, state, and complex business validation.
4. Order dependent rules as root/shape → existence → access/ownership → current state → remaining business constraints. Use a scoped existence/access specification when disclosure policy requires it.
5. Invoke access/ownership specifications from `Auth` and preserve authorization semantics; run remaining pre-side-effect business specifications from `Validate`; execute the query/state change/orchestration in `Handle` only after both stages succeed.
6. Import only inward Core contracts through settable properties.
7. Return typed expected faults; never return null.
8. Compose independently reusable children with `Continue`/`ContinueWith`; inspect and propagate required faults immediately.
9. State fail-fast, compensating, or best-effort behavior. Put local atomic invariants behind one repository operation and durable cross-boundary recovery outside it.

## Avoid

- Do not call lifecycle methods directly in production orchestration or present a direct-stage unit test as pipeline proof. Do not parse HTTP, reference hosts/concrete adapters, or use `SystemBootstrapper` as a service locator.
- Do not validate only simple fields and leave required existence, access, state, relationship, conflict, or other business rules as inline `Handle` checks.
- Do not create a process for a private pure helper solely for DI.
- Do not use direct mediator dispatch for a logical child, ignore a result, read a faulted payload, or assume shared transactions.
- Do not use bare `List`, `Details`, `Add`, `Edit`, or `Sync` names in new work.

## Test

Use mediator execution to test stage short-circuiting, direct-dispatch security, every inventoried specification (including missing/inaccessible/invalid-state cases), validation before effects, typed faults, allowed port calls/mapping, child-fault propagation, success payload/metadata, and repeat/compensation/best-effort behavior. Add repository/provider boundary tests separately.

## Verify completion

- Confirm one recognizable Core use case owns the behavior and all dependencies point inward.
- Confirm every expected or child outcome and side-effect boundary is explicit.
- Confirm the process is discovered in required hosts, named safely, and verified through the pipeline.
- Confirm applicable items in [`definition-of-done.md`](../../agent/definition-of-done.md) pass.
