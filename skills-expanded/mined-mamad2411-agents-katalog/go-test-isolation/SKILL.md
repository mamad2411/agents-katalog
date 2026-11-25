---
name: go-test-isolation
description: Use when Go test work involves files, external dependencies, doubles, shared mutable or process state, goroutines, timers, fixture lifetime, or parallel execution, including repairing flaky or order-dependent setup. Skip pure deterministic calculations using only local inputs and ordinary assertions.
---

# Go test isolation

Make important observations repeatable without removing the dependency behavior
they need to verify. Use the smallest faithful fixture, with visible ownership
and control over work that can outlive a test body.

## Establish ownership and independent execution

Inspect the effective Go version, project conventions and the test's actual
boundary. Identify owned resources, borrowed resources and process-wide state.
Include setup failures, early assertions, descendants and background work.

- Give independent cases independent mutable data and paths. Use t.TempDir for
  owned filesystem fixtures and t.Cleanup for resources that must survive the
  test body and its descendants. A parent-body defer runs before its parallel
  children resume; it cannot release resources those children still need.
- Group parallel descendants when later parent assertions must wait for them.
  Keep named cases independently selectable with go test -run: parent setup
  and final assertions must not assume excluded siblings or table rows ran.
  Preserve useful persistence/lifetime checks using the expected work of the
  cases actually executed, or move the observation to its owning case. Derive
  expected values from the contract, not returned production values.
- Register cleanup as soon as ownership is acquired. On every exit path,
  release test gates, cancel and join started work before closing or deleting
  its borrowed resources. Bound joins and report the stalled operation. A
  timeout diagnoses non-cooperation; it does not terminate a goroutine.
- Keep process environment, working directory and global-default mutations
  serial, including ancestors. t.Setenv restores state but cannot make global
  mutation parallel-safe. Preserve unset versus present-empty values. Use an
  explicit filtered child environment when checking real process behavior.
- Separate build/tool subprocess setup from the executable's configuration.
  When filtering a builder's environment, preserve or deliberately supply its
  required cache/configuration instead of copying an absent override. A test
  runner's GOCACHE override is not an implicit test prerequisite. Check relevant
  setup with ordinary unset defaults while controlling application configuration.
- Parallelize only independent work. Shared replacement sequences can remain
  serial inside independent instance cases. Respect the project's effective
  loop-variable semantics rather than adding or removing captures by habit.

## Preserve the dependency boundary

Choose real dependencies, standard-library local fixtures, handwritten doubles
or existing project mocks according to the risk being observed. No universal
mocking framework, integration tag, database, container or leak package is
required. Keep production seams aligned with actual API/composition needs;
avoid exported hooks, interfaces or clock frameworks just to fit a test form.

Make a double preserve the relevant cancellation, error, ordering, body lifetime
and side-effect behavior. Account for automatic client/driver behavior when the
contract limits requests, targets or accepted responses: a redirected final 200
can hide a rejected initial status and extra requests. Test through the actual
client policy at that boundary without mutating shared caller configuration.
Instrument response bodies for ownership assertions;
use a real local HTTP server/transport when the claim needs request or network
cancellation behavior. Handler recorders and synthetic transports support
narrower observations. If a restriction forces a substitute, report that scope
and the unverified boundary. Database rollback cleans only transaction-owned
work, not separate commits, clients or background writes.

## Control events and verify reliability

Observe startup, in-flight blocking, cancellation and completion with explicit
events. Do not use a sleep to guess readiness or an immediate negative check
before the observer has started. When elapsed time is contractual, measure from
the promised event, justify tolerances and give slow schedules a useful failure
bound. A callback release gate is not automatically callback completion.

Return worker outcomes through synchronized channels/state; make Fatal/FailNow
assertions in the test goroutine. Bound processes and wait on their real results.
For Go1.22 use channels, contexts and owned timers. t.Context requires Go1.24;
stable testing/synctest.Test requires Go1.25 and suitable in-process work.
Virtual time does not control external sockets or child processes. Do not raise
the module minimum for preferred test helpers.

Read [isolation patterns](references/isolation-patterns.md) for subtest lifetime,
early-failure cleanup, boundary selection or version-specific timing decisions.
Check the relevant tests alone, important named children, and the full suite;
use race detection and bounded shuffle/repetition for exercised shared/concurrent
paths. Passing runs do not prove every schedule race-free or flake-free. Report
actual checks and material limits. Behavior-test guidance owns cases and oracles;
this skill owns the control and lifetime that make them trustworthy.
