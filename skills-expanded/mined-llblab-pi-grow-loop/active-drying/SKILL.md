---
name: active-drying
description: Evidence-driven refinement that lowers carrying cost per unit of useful capability and frees budget for growth. Use for active-drying, drying, post-growth cleanup, architectural distillation, semantic density, cost-of-change reduction, or making a project leaner beyond DRY. Two modes — guard during growth and refinement after it. Examines models, ownership, state, contracts, dependencies, effects, runtime work, tests, tooling and user surfaces without weakening behavior or guarantees.
---

# Active Drying

Expose the project's muscle: useful capability, explicit invariants and clear ownership. Remove water: accidental mass that consumes attention, change effort, validation, runtime or operations without earning its cost. Reshape what remains so the same capability stands on less machinery. Deduplication is the floor, not the goal.

The objective is **lower carrying cost per unit of useful capability**, not fewer lines or maximum abstraction. Prefer deleting the reason for complexity to exist over rearranging it. Semantic density means a reader recovers behavior and invariants from fewer independent concepts and fewer places — never compressed syntax, hidden conventions or clever code.

Drying banks surplus; it does not decide what new capability to buy with it.

## Authority and Composition

This is an optimization lens, not an execution controller. The active task contract owns permissions, scope, validation, budget and stopping. Preserve applicable architectural, security and domain constraints; use existing project conventions and native validation methods. Do not require another workflow, duplicate its protocols or invent new authority.

When an enclosing workflow controls the agent's goal, backlog, sequencing or continuation, leave those responsibilities with it. Apply drying within the assigned slice and return the result; do not create a second scheduler, parallel backlog or cleanup loop. Without an enclosing controller, complete the bounded request and stop.

Preserve required behavior, public contracts, data, compatibility, accessibility, security, failure handling and operational guarantees unless explicitly authorized otherwise. These are constraints, not costs that savings can offset. Distinguish refinement from product removal, migration and defect repair. Preserve unrelated work and user-owned changes; authorization to refactor does not permit destructive working-tree cleanup, history rewrites or data deletion.

Review-only work stays read-only. A direct request to dry authorizes scoped implementation only within the active contract, not capability removal. Do not replace removed code with a larger process, framework or reporting system.

## Modes

Select from intent; state the mode only when it prevents ambiguity. Mode selects the lens, not permissions.

- **Guard — during growth:** compare proposed abstractions, state owners, dependencies, extension points and configuration knobs with a simpler adequate form. Each addition must name the present requirement it satisfies. Stay within the feature's affected closure; do not derail delivery or reopen settled decisions without new evidence.
- **Refinement — after growth:** find and implement the strongest justified improvements in the requested project or subsystem when authorized. Work in coherent, independently verifiable slices, not a repository-wide rewrite. Without an explicit target, use the active project's current work as the boundary and say so.

An audit applies either mode without mutations. Neither mode requires changes when the existing design wins.

## 1. Establish Obligations, Cost and Evidence

Read project instructions, current work and the implementation before diagnosing. Trace affected behavior through callers, contracts, configuration, tests and operational paths. For project-wide requests, map responsibility areas before choosing a slice; deeper inspection follows actual dependencies.

Establish a compact baseline:

- **Capability and invariants:** what users, callers and operators rely on; which safety, error, compatibility, lifecycle and performance guarantees must survive.
- **Ownership:** where state, policy and contracts are defined; which copies are authoritative, derived, cached or historical.
- **Carrying cost:** concepts a reader must load, coordinated edit sites per supported change, state copies kept in sync, runtime work, validation and operational burden.
- **Pressure evidence:** recurring fixes, conversion ladders, synchronized fields, measured work and, when available, churn and co-change history. Distinguish observed cost from inferred risk; co-change is evidence, not proof of one responsibility.
- **Evidence boundary:** what can be inspected and validated now, and what remains unknown.

**Investigation must earn its cost too.** Start with cheap discriminating checks. Deepen analysis only when plausible surplus, impact radius or the cost of being wrong justifies it. Prefer evidenced recurring costs, disputed ownership and risky synchronization, or measured bottlenecks over cosmetic opportunities; let the project's actual constraints decide priority. Reuse valid evidence instead of repeatedly surveying the repository.

History is useful, not mandatory. A traced change path, ownership argument or type invariant can demonstrate cost without telemetry. Appearance alone cannot. Do not force speculative savings into a numerical score or spend more proving a minor gain than it can plausibly repay.

Do not infer dead code from one search with no hits. Check exports, dynamic registration, configuration, serialization, generated consumers, platform/feature variants and supported external use. One visible caller does not make a public contract private. Unknown usage calls for investigation or deferral, not deletion.

## 2. Find the Cause, Not Just the Repetition

Use relevant lenses as search heuristics within scope, not a mandatory repository-wide checklist. Surface material opportunities, reasons to keep complexity and validation gaps. “Not inspected” is not “clean”; exhaustive coverage is not the deliverable.

- **Paths and duplication:** can one supported path replace competing implementations, half-retired paths or unnecessary stages without losing a distinct promise? Consolidate shared meaning at its owner, not matching syntax. Local repetition can cost less than coupling independent policies.
- **Representation:** can a better model remove branches, flags, sentinels, conversion ladders or invalid states? Close the gap between representable and permitted states at the owner instead of repairing it at every consumer. Keep genuinely different concepts distinct.

```ts
// Consumers must reconstruct the relationship between status and payloads.
type LooseJob<R, E> = { status: 'pending' | 'done' | 'failed'; result?: R; error?: E };
// The relationship is explicit; external inputs still require validation.
type Job<R, E> =
  | { kind: 'pending' }
  | { kind: 'done'; result: R }
  | { kind: 'failed'; error: E };
```

- **State and lifecycle:** can derivation remove synchronization and invalidation work? Preserve caches, persistence, historical snapshots and redundancy that serve demonstrated latency, recovery, audit or correctness needs. Derived current state is not automatically a substitute for historical truth.
- **Boundaries and contracts:** do boundaries follow independent reasons to change? Would merging expose one cohesive responsibility, or extraction isolate a real policy, invariant, dependency or lifecycle? Do flags, callbacks and exports express supported variation, or hide an unnecessarily generic mechanism? Preserve compatibility and operational escape hatches that still have a job.
- **Machinery and dependencies:** which wrappers, adapters, registries or libraries remove more complexity than they introduce? Prefer existing capabilities; do not replace mature dependencies with home-grown equivalents to lower a count.
- **Idiomatic expression:** use established constructs and standard APIs for the project's supported versions, including conventional data flow, resource management and error handling. Respect justified local conventions; avoid fashion, cosmetic uniformity and brevity for its own sake.
- **Idempotent effects:** distinguish retrying the same logical request from intentionally starting a new operation. Prefer existing set/upsert/reconcile or idempotency mechanisms at the owning boundary over bespoke deduplication. Preserve explicitly non-idempotent behavior. For affected retryable paths, verify repeats, partial failure and relevant concurrent retries; an upsert alone does not prove end-to-end idempotency. Do not invent global caches, deduplication stores or exactly-once guarantees without a demonstrated requirement and supporting mechanism.
- **Work and flow:** can an algorithm, query, representation or pipeline remove repeated work, allocation, I/O, conversion or coordination? Account for costs across callers, startup, memory, build time and services, not just the edited function.
- **Failure and operations:** place validation, retries, fallbacks, logging and recovery at the correct boundary. Prove redundancy before removing checks; trust-boundary validation, useful context and diagnosability are muscle.
- **Tests and evidence:** express current invariants, meaningful input classes and supported regressions rather than obsolete implementation structure. Consolidate fixtures only with equivalent protection. Never delete failing checks or lower the bar to manufacture a gain.
- **Tooling and documentation:** replace hand-synchronized scripts, settings and contradictory instructions with a canonical source where it pays. Retire stale paths only with consumers accounted for. Follow existing documentation and packaging conventions.
- **User and operator surfaces:** check task order, concepts, states, setup, delivery and recovery. Do not shift implementation complexity onto people, hide errors, remove access or gratuitously replace established interaction patterns.

Inspect interactions: deduplication can worsen ownership; caching trades runtime work for state; a smaller API can spread branching across callers. A trade-off may pay, but relocation alone is not a saving. Optimize the whole affected path while preserving its constraints.

## 3. Admit Only Reforms That Pay

For each material candidate, establish:

- **Pressure and location:** the demonstrated cost or risk, and where it originates.
- **Move:** delete, derive, narrow, merge, re-represent, extract or reuse. Prefer one change at the owning model or boundary over many symptom edits. Compare with leaving the code alone.
- **Preservation:** required behavior, guarantees and consumers of the old shape.
- **Ledger:** carrying cost before → after, new costs and risks, one-time investigation, implementation, migration and validation effort, and plausible payback over the project's actual change horizon. Account for expected failure costs and uncertainty where evidence supports them; never trade mandatory guarantees for estimated savings. Keep unlike costs visible; avoid false precision. Uncertain speculative payback defers the candidate.
- **Falsification:** the check, traced path, representative change or measurement that could show the proposal wrong or not cheaper. Challenge the preferred design with the strongest plausible keep-as-is case.

Keep this implicit for obvious local changes; use a short note for material trade-offs, not a scoring sheet. A reform may add lines and still pay, or delete lines and still cost. Structural reasoning can justify a maintenance gain; performance claims require measurement.

**Counterfeit savings do not count:** compressed syntax, hidden conventions, weakened guarantees, deleted checks, unaccounted cost relocation or hypothetical future flexibility. Elegance is a hypothesis, not evidence. **No-op is a valid winner.** A candidate blocked by evidence, compatibility, data or safety questions blocks itself, not unrelated safe reforms.

### Decomposition Test

Before adding or removing a boundary:

1. **Owner:** can the responsibility be named precisely, with explicit exclusions?
2. **Locality:** does a real supported change or invariant require fewer coordinated edits or less cross-boundary knowledge?
3. **Interface:** is it narrower and more stable than the internals it hides? Passing most of the host's state and callbacks is relocation, not separation.
4. **Direction:** does dependency flow remain clear and acyclic, without reach-through or a new shared bucket?
5. **Payback:** does isolation, reuse, testing or clarity repay navigation, wiring, indirection and transition costs on the relevant horizon?

A second consumer is one justification, not the only one: an existing safety rule, volatile dependency or independent lifecycle can earn a boundary. A long file alone cannot. Merge units that change together only when the split protects nothing; do not force domain and orchestration together to cut file count.

## 4. Cut in Verifiable Slices

Choose a coherent slice with a clear preservation boundary and decisive validation. Batch low-coupling reforms that share it; sequence dependent ones. Exclude speculative redesign, formatting churn and unrelated repairs.

- **Pin before cutting:** use existing checks first. Where protection is missing, establish the smallest permitted baseline through characterization tests, snapshots, replay, recorded effects or another native evidence method. Do not impose a new test framework. Distinguish required behavior from observed defects; do not silently canonize or repair a defect outside scope.
- **Bound the oracle:** replay or output hashes establish agreement only for the exercised inputs and observed effects. Determinism does not make sampled input coverage exhaustive. Include contract-relevant outputs, state, errors, events, side effects and lifecycle; equal final state alone proves none of the omitted guarantees. Claim a total oracle only for an explicitly bounded domain and observation surface with justified coverage.
- Prefer incremental transformations that keep the project runnable. A broader refactor is justified only when smaller cuts cannot remove the cause. If preservation cannot be established and risk is material, defer the candidate.
- Update affected callers, tests, configuration and docs. Retire superseded scaffolding when authorized; leave no accidental competing sources of truth. Required compatibility adapters may remain with clear ownership.
- Reuse valid analysis and validation; refresh what the change invalidates. If verification rejects a transformation, revise or undo only that task's change. A cleaner diff never excuses changed semantics.

No deletion percentages, line budgets, abstraction quotas or fixed pass counts. No minification, code golf, opaque metaprogramming, universal helpers or architecture for its own sake.

## 5. Prove Preservation and Surplus

Green checks do not establish architectural improvement; structural arguments do not establish behavioral preservation. Show both with the applicable required checks:

- **Preservation:** exercise relevant accepted/rejected inputs, edge states, errors, compatibility, side effects and lifecycle. Follow contracts through call sites. Disclose pre-existing failures and remaining uncertainty.
- **Surplus:** show concrete before → after: several policy decisions become one owner, synchronized fields become a derivation, a supported change touches fewer boundaries, or a stage disappears. Account for new costs and verify nothing was merely hidden or relocated.
- **Measurement:** any speed, memory, I/O, startup, build or bundle claim needs a representative workload and comparable baseline. Fewer lines or a plausible complexity estimate is not a measured speedup. Separate measured results from structural expectations.
- **Comprehension:** walk one real use case and one relevant change through the retained design. A reader should locate policy, state transitions and failures without chasing aliases or hidden conventions.

Use independent review for consequential changes when available and worthwhile; reconcile evidence, not votes. Update existing context surfaces where reality changed, without documentation ceremony.

## Stop and Handoff

Stop at an evidenced local fixed point: the slice preserves its obligations, retained reforms show concrete surplus, and no known material in-scope candidate can be justified and safely validated at worthwhile cost. This is not proof of global optimality or exhaustive inspection. Do not reshuffle a sound design because another arrangement is possible.

When task bounds, budget, missing evidence or an owner decision stop progress, report the limit instead of claiming the project is dry. Do not recycle a rejected candidate without new evidence or a materially different mechanism. An enclosing controller decides whether another slice runs; finishing this slice does not authorize extending or terminating its loop.

Report only useful signal, scaled to the work:

- **Scope and mode:** what was examined; slice versus project-wide assessment.
- **Before → after:** material reforms and carrying-cost changes; counts support, never replace, the explanation.
- **Preserved and checked:** retained contracts, validation performed and remaining limits; measured gains separate from structural ones.
- **Freed budget:** which change class got cheaper, concepts no longer need loading, or work no longer runs — without inventing quantified savings or spending them on new features.
- **Kept or deferred:** complexity that still earns its place and candidates blocked by evidence, compatibility, economics or scope.

If nothing pays, say so with the decisive reason. Successful drying can leave more explicit code and fewer concepts; it never trades a stronger project for a smaller diff.
