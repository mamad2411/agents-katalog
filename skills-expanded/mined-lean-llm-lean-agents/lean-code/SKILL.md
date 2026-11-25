---
name: lean-code
description: "Load lean-code for all coding-related tasks: implementing, fixing, refactoring, reviewing, testing, or optimizing code."
---

# Lean Code

## Core
Solve the full task with minimal clear code. Prefer removing work, then project code, platform APIs, installed dependencies, then new code. Detect stack, installed runtime/toolchain and targets; use matching docs and repo scripts/wrappers. Keep conventions; no unsolicited upgrades, dependencies or generated-file edits. Avoid speculative features, options, types, config and one-use abstractions. Trace a failing path; fix its owner, not each symptom. Preserve behavior, compatibility, validation, security, errors, data integrity, accessibility and thread ownership; favor clarity over compressed tricks. Regression-test nontrivial changes: positive/negative/failure paths, deterministic fixtures/cleanup, real integration where mocks cannot prove behavior. Compilation isn't proof. Mark shortcuts `shortcut: <limit>; revisit when <trigger>`. Report `STATUS` (`PASS|UNVERIFIED|BLOCKED|FAILED`), paths, exact check commands/exits, tested artifacts and unrun checks/risks; never invent verification or measurements.

## Required lean pass after coding
Review the working diff and nearby callers: **same behavior, fewer lines or moving parts?** Simplify, then rerun affected checks. Remove dead branches, duplicate conditions/loops, needless state, arguments, wrappers and boilerplate; inline trivial one-use helpers when clearer. Preserve public APIs/behavior unless explicitly changing them. For performance only: profile a representative baseline, test one hypothesis, correctness-check and remeasure at the same load. Report scenario/environment, commands, repetitions and uncertainty; stop at noise, don't infer real-world gains from microbenchmarks.

## Dedup & shared behavior
When **2+ real objects/classes** repeat a rule, give it one reusable owner: existing method, focused utility/service or composition. Use **inheritance/base class** only for genuine *is-a* relationships with stable shared state, lifecycle and behavior; share protected logic where appropriate. Prefer composition/strategy for unrelated objects or differing behavior. No deep inheritance, god helpers, speculative frameworks or one-use abstractions. Don't merge lookalike code with different semantics.

## Safety gate
Smaller LOC is a **tie-breaker**, not permission to degrade clarity, complexity, ordering, errors, compatibility or thread ownership. Keep scope local; check affected callers/tests and before/after behavior. If equivalence is uncertain, keep the clear working version. Validate untrusted input and permissions at boundaries; protect secrets, paths, auth and serialization. Where applicable, parameterize SQL, preserve transactions/rollback and retry idempotency. Use contextual, secret-free logs; diagnose failures rather than masking them. In review-only tasks, **propose** simplifications; never edit without authorization.

## Technical Debt
Address evidenced friction in touched code, not unrelated cleanup. Split oversized utilities into cohesive modules/folders with clear ownership when tangled dependencies, cycles or duplication impede changes. Use the smallest root-cause fix; avoid micro-modules and sweeping rewrites. For measured build bottlenecks, use supported incremental compilation, caching or module isolation; compare before/after timings and validate clean builds to catch stale-cache errors. Apply the safety gate to affected contracts, callers and regressions. Defer broader debt with concrete impact and a revisit trigger, not unexplained TODOs.

## Async & responsiveness
Keep blocking file/network I/O and heavy independent CPU work off latency-sensitive threads. Prefer supported async I/O and bounded CPU worker pools; lazy-load deferrable work where appropriate. Parallelize independent work, not dependencies; preserve semantics, ordering and lifecycle. Bound concurrency and queues with backpressure and cancellation; propagate failures, release resources/locks on all paths and drain required writes at shutdown. Apply callback/results to state/UI on the owning thread through platform-supported schedulers; respect thread-affine APIs. Avoid unbounded tasks and needless async/context switches: async is not inherently faster, and not every operation needs it.
