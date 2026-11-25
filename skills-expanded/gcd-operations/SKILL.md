---
name: gcd-operations
description: "Use for iOS/macOS concurrency problems involving dispatch queues, locks, or thread safety. Triggers on: deadlocks (sync on main, nested sync, ABBA lock ordering), thread explosion from too many DispatchQueue.global() calls, data races flagged by Thread Sanitizer (TSan), DispatchGroup enter/leave imbalance, DispatchSource timer leaks, lock selection (NSLock vs OSAllocatedUnfairLock vs os_unfair_lock), reader-writer barriers, AsyncOperation subclasses, dispatchPrecondition usage, and OperationQueue throttling. Also use when migrating GCD patterns to Swift Concurrency actors. Apply whenever someone asks about thread-safe properties, concurrent access to shared state, or sees TSan warnings in Apple platform code — even if they don't say 'GCD' or 'concurrency.'"
metadata:
  version: 1.0.3
---

# GCD & OperationQueue Concurrency

Enterprise-grade concurrency skill for Grand Central Dispatch and OperationQueue. Opinionated: prescribes serial queues by default, target queue hierarchies, labeled queues, `NSLock`/`OSAllocatedUnfairLock` for synchronization, barrier-based reader-writer on custom concurrent queues, and OperationQueue for dependency graphs. Apple has **not deprecated any core GCD APIs** — GCD remains appropriate for parallelism, system I/O, and performance-critical paths. This skill covers correct usage, deadly bug prevention, and coexistence with Swift Concurrency.

## Concurrency Layers

```text
Application Layer    -> OperationQueue for dependency graphs, cancellation, throttling.
Dispatch Layer       -> Serial queues for state protection, concurrent+barrier for R/W.
Synchronization      -> NSLock / OSAllocatedUnfairLock for short critical sections.
System I/O           -> DispatchSource (timers, file monitoring), DispatchIO (non-blocking file I/O).
Thread Pool          -> GCD manages threads. App targets 3-4 well-defined queue subsystems.
```

## Quick Decision Trees

### "Which queue type should I use?"

```
Do you need mutual exclusion (protecting shared state)?
+-- YES -> Serial queue (default). Simplest, safest.
+-- NO  -> Is this independent parallel work (image processing, batch transforms)?
    +-- YES -> Concurrent queue (custom) with barrier for any writes.
    +-- NO  -> Do you need dependency graphs, cancellation, or throttling?
        +-- YES -> OperationQueue with maxConcurrentOperationCount.
        +-- NO  -> Serial queue. When in doubt, serial.
```

### "Which lock should I use?"

```
Which lock?
+-- iOS 16+ -> OSAllocatedUnfairLock (Apple's safe wrapper)
+-- iOS 18+ / Swift 6 -> Mutex from Synchronization framework
+-- Any iOS -> NSLock (safe, simple, recommended by Apple DTS)
NEVER: os_unfair_lock as direct Swift stored property (memory corruption).
NEVER: DispatchSemaphore as a mutex (no priority donation).
```

### "Which QoS should I use?"

```
Is the user waiting and watching?
+-- Immediate response (animation, touch) -> .userInteractive
+-- User-triggered, blocking progress    -> .userInitiated
+-- Long-running with progress bar       -> .utility
+-- Invisible to user (prefetch, sync)   -> .background
WARNING: .background QoS may be halted entirely in Low Power Mode.
```

## Workflows

### Workflow: Review Existing Concurrency Code

**When:** First encounter with a codebase using GCD/OperationQueue.

1. Scan for deadlock patterns using detection checklist (`references/deadlocks.md`)
2. Scan for data race patterns (`references/data-races.md`)
3. Check for thread explosion indicators: `DispatchQueue.global()` scattered throughout, many independent queues, no `maxConcurrentOperationCount` (`references/thread-explosion.md`)
4. Verify lock correctness (`references/thread-safety.md`)
5. Check OperationQueue subclasses for missing KVO/state management (`references/operation-queue.md`)
6. Create `refactoring/` directory with per-feature plans and severity-ranked findings (`references/refactoring-workflow.md`)
7. Execute fixes in phase order: Critical → Thread Safety → Queue Architecture → OperationQueue → Monitoring

### Workflow: Add Thread-Safe Collection

**When:** Need concurrent read/exclusive write access to shared state.

1. Create a custom concurrent queue with descriptive label
2. Implement reads via `queue.sync { return value }`
3. Implement writes via `queue.async(flags: .barrier) { mutate }`
4. Verify barrier is on **custom** queue, never global (`references/thread-safety.md`)
5. Add `dispatchPrecondition` assertions at boundaries
6. Test with `DispatchQueue.concurrentPerform` under Thread Sanitizer

### Workflow: Create AsyncOperation Subclass

**When:** Need OperationQueue with async work (network, disk I/O).

1. Override `isAsynchronous`, `isExecuting`, `isFinished` with thread-safe KVO (`references/operation-queue.md`)
2. Never call `super.start()` -- it marks the operation finished immediately
3. Check `isCancelled` at start, call `finish()` if cancelled
4. Call `finish()` from **every** completion path
5. Check dependency cancellation in `main()` -- cancelled deps satisfy dependencies, they don't block
6. Test with Thread Sanitizer enabled

### Workflow: Migrate GCD Pattern to Swift Concurrency

**When:** Modernizing specific GCD patterns. Not all patterns should migrate.

1. Identify the pattern category (`references/migration.md`)
2. Easy: `DispatchQueue.main.async` -> `@MainActor`, `DispatchGroup` -> `TaskGroup`, serial queue -> `actor`
3. Keep as GCD: `concurrentPerform`, `DispatchIO`, `DispatchSource`, concurrent+barrier reader-writer
4. Bridge callbacks with `withCheckedThrowingContinuation` -- resume **exactly once** on every path
5. Never use `DispatchSemaphore.wait()` in any async context

## Code Generation Rules

<critical_rules>
Whether reviewing, generating, or refactoring concurrent code, every output must be **thread-safe, deadlock-free, and production-ready**. ALWAYS:

1. Label every `DispatchQueue` with reverse DNS naming including subsystem
2. Use serial queues for state protection -- concurrent only when reads vastly outnumber writes
3. Use `defer { group.leave() }` immediately after every `group.enter()`
4. Use `OSAllocatedUnfairLock` (iOS 16+), `NSLock` (any iOS), or `Mutex` (Swift 6+) for short critical sections -- never `os_unfair_lock` as a direct stored property
5. Use `dispatchPrecondition(condition:)` before sync dispatch and UI updates
6. Use `[weak self]` in repeating timer handlers and stored closures
7. Cancel `DispatchSource` timers in deinit (resume first if suspended)
8. Override `isAsynchronous`, `isExecuting`, `isFinished` with KVO in async Operations
9. Set `maxConcurrentOperationCount` on OperationQueues -- never leave unlimited for blocking work
10. Never call `DispatchQueue.main.sync` from any code that might run on the main thread
11. Before generating concurrent code, output a brief `<thought>` analyzing potential deadlocks, races, and retention.
</critical_rules>

## Fallback Strategies & Loop Breakers

<fallback_strategies>
When fixing concurrency bugs, you may encounter cascading issues. If you fail to fix the same issue twice, break the loop:

1. **Deadlock in sync dispatch:** Replace `sync` with `async` and restructure the call site to use a completion handler or continuation. Why: eliminating `sync` eliminates the entire deadlock category — async dispatch never blocks the caller.
2. **Thread explosion from blocking work:** Wrap blocking calls in Operations with `maxConcurrentOperationCount = 4` instead of trying to make GCD limit threads. Why: GCD's thread pool grows unboundedly when work items block — OperationQueue is the only reliable throttle.
3. **Data race under TSan:** If concurrent queue + barrier is proving fragile, fall back to `NSLock` protecting a plain property. Why: barrier correctness requires remembering to use the barrier flag on every write and the exact same queue for every access — a lock has a simpler mental model with fewer ways to get wrong.
</fallback_strategies>

## Confidence Checks

Before finalizing generated or refactored concurrent code, verify ALL:

```
[] No deadlock risk -- no sync on main, no nested sync on same queue, no ABBA chains
[] No thread explosion -- maxConcurrentOperationCount set, no scattered global() calls
[] No data races -- shared mutable state protected by queue, lock, or actor
[] Queue labels -- every queue has reverse DNS label with subsystem name
[] Barrier correctness -- barriers on custom concurrent queues only, never global
[] Group balance -- every enter() has defer { group.leave() }
[] Timer safety -- [weak self], cancel in deinit, resume before dealloc if suspended
[] Lock safety -- no os_unfair_lock as stored property, no semaphore as mutex
[] Operation KVO -- async operations override isExecuting/isFinished with thread-safe KVO
[] Main thread -- UI updates verified with dispatchPrecondition(.onQueue(.main))
[] Swift Concurrency coexistence -- no semaphore.wait() in async contexts
[] Background tasks -- endBackgroundTask called on every path
```

## Companion Skills

> **Before refactoring GCD code to Swift Concurrency:** load the swift-concurrency skill to understand actor isolation and Sendable constraints. Migration without that context leads to subtle bugs.

| Scenario | Companion skill | Apply when |
|---|---|---|
| Migrating GCD patterns to `async/await` or actors | `skills/swift-concurrency/SKILL.md` | Converting completion handlers, replacing DispatchQueue with actors, adopting Swift 6 |
| GCD used in UIKit MVVM ViewModels | `skills/uikit-mvvm/SKILL.md` | Refactoring Massive ViewControllers, extracting ViewModels, setting up Combine bindings |

## References

| Reference | When to Read |
|-----------|-------------|
| `references/rules.md` | Do's and Don'ts quick reference: priority rules and critical anti-patterns |
| `references/queue-creation.md` | Queue types, QoS selection, target queue hierarchies, queue labeling |
| `references/deadlocks.md` | The 5 deadlock patterns, prevention with dispatchPrecondition, lock ordering |
| `references/thread-safety.md` | Lock selection (NSLock, OSAllocatedUnfairLock, Mutex), reader-writer barrier, @Atomic trap, singletons |
| `references/thread-explosion.md` | Thread explosion causes, priority inversion, thread starvation, throttling strategies |
| `references/dispatch-primitives.md` | DispatchGroup, DispatchWorkItem, DispatchSemaphore, DispatchSource timers, DispatchIO |
| `references/operation-queue.md` | AsyncOperation base class, KVO state management, cancellation, dependency graphs |
| `references/data-races.md` | Value type COW races, memory management, main thread violations, real-world fixes |
| `references/debugging.md` | Thread Sanitizer, dispatchPrecondition, Instruments, os_signpost, testing strategies |
| `references/migration.md` | GCD to Swift Concurrency mapping, what to migrate vs keep, bridging with continuations |
| `references/refactoring-workflow.md` | `refactoring/` directory protocol, per-feature plans, PR sizing, verification checklist |
