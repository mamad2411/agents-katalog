---
name: robust-by-construction
description: The engineering invariant bar — what "good" means for systems built by this harness. Use as a checklist during design, as the audit criterion for adversarial-review, and as the source of linter/CI rules to mechanize. Not a style guide; these are correctness and safety properties.
---

# Robust-by-construction: the invariant bar for systems built by this harness

BLUF: «works on my machine» is not the bar. The bar is: every failure surfaces, every wait has an escape, every operation is safe to repeat, and every rule that can be mechanized is mechanized. Prose is the last resort for what cannot be encoded.

## (a) Fail-fast / error-as-data

**No system error is swallowed.** A false «success» on a failed operation is a security defect — the caller proceeds as if state was mutated when it was not.

Rules:
- Every error is propagated to ONE global handler (the observability sink). The handler decides: log + continue, degrade gracefully, or halt. Individual nodes do not make this call — they emit the error and let the global module handle it. This is «error-as-data»: a process does its work and emits its outcome (including failure) as structured data; it does not silently absorb failures.
- Degraded operation is the goal of failure handling, not suppression. A degraded state must be distinguishable from a healthy state by the system's own telemetry.
- Enforce mechanically: `forbidigo` (Go) or equivalent linter rule blocking bare error discards (`_ = err`, `if err != nil { return }` without propagation).

Mirabilis example: the proxy lifecycle failure on first-launch was masked by a swallowed dial error — the TUI showed a connected state while the proxy was dead. The fix added error propagation to the observability sink and a health-check that distinguished «proxy not yet started» from «proxy running».

## (b) No-hang / no-race

**Every I/O, sync, and wait has a hard escape.** «It will eventually complete» is not a correctness argument for a user-facing system.

Rules:
- Every blocking call carries a `context` deadline (or timer) AND/OR a forced unblock path (close the fd, kill the process group, cancel the context). Both, where possible.
- Long-lived resources (file locks, PTY handles, proxy processes) are owned for the session, not for a single call. Ownership means: created once, explicitly released on session teardown, never released by GC.
- Subscriptions (event listeners, channels, callbacks) are registered once per session, not re-created per event. Re-creation per event is a leak path.
- Enforce mechanically: the race detector (`-race`) runs in CI on every branch; goroutine leak detectors (e.g. `goleak`) in test teardown.

Mirabilis examples:
- The flock GC bug: a Go `flock` object had no explicit `Close()` — the GC could drop the lock silently mid-session. Fix: explicit `defer f.Close()` at the point of acquisition, owned by the session context.
- The PTY deadlock: a synchronous size-change notification ran on the Bubble Tea render loop; if the child process was unresponsive, the UI hung permanently. Fix: a goroutine with a 500ms deadline and a forced unblock if the deadline fires.

## (c) Idempotency contract: Check → Run → Check

**Every operation that mutates state is safe to repeat.** The pattern is:

1. **Check** — verify preconditions and current state.
2. **Run** — execute the mutation.
3. **Check** — verify postconditions hold.

This is not defensive boilerplate; it is the contract that makes operations composable, retryable, and automatable. Encode it as a reusable test harness (a function called in both unit tests and integration tests), not as prose in a README.

For provisioning operations (create-if-not-exists, configure-if-not-configured): the full idempotency contract means running the operation twice in the test harness and asserting the state is identical after both runs, not just that the second run does not error.

## (d) Single observability sink

One place in the system aggregates all errors, events, and metrics. There is no «local error logging» that bypasses the sink. Rationale: two error sinks produce two incomplete pictures; debugging requires correlating them; correlation requires the single sink.

The sink is the dependency injection point — in tests, replace it with a recorder; in production, replace it with the real telemetry backend. This is the ports-and-adapters pattern applied to observability.

## (e) Ports and adapters — replaceable nodes

**Swapping a node = one file + one registration line.** No other file changes.

Rules:
- Domain logic has zero imports from infrastructure (no database, no HTTP, no filesystem in the core). Infrastructure imports the domain; never the reverse.
- The dependency edge graph is enforced mechanically: `depguard` (Go) or equivalent. A PR that introduces a forbidden import fails CI, not code review.
- The benefit at fleet scale: an [agent-fleet-orchestration](../agent-fleet-orchestration/SKILL.md) node is exactly a ports-and-adapters node — a frozen contract (the port) and a contained implementation (the adapter). The architecture and the orchestration pattern are the same thing.

Mirabilis example: the engine (port interfaces) and the Bubble Tea v2 TUI (adapter) were separate compilation units. Swapping the TUI for a headless adapter in tests required no engine changes — the port interface was the only coupling. `depguard` enforced that the engine never imported `bubbletea`.

## (f) Mechanize-the-mechanizable

**A rule goes to prose only if no check can hold it.** Otherwise: linter, CI gate, hook, test.

Decision table:

| Rule type | Mechanism |
|---|---|
| Import graph constraint | `depguard` / `import-boundary` linter |
| Forbidden call pattern | `forbidigo` / `semgrep` rule |
| Build/compile correctness | CI build step |
| Race safety | `-race` in CI |
| Schema/contract compliance | generated types / compile-time check |
| Idempotency | parameterized test harness |
| Approval gate | `auto-critic.sh` hook |
| Verification gate | `verification-gate.sh` hook |

The cost of a prose rule that could be mechanized: it degrades silently (nobody re-reads the prose), it produces inconsistent enforcement (humans miss it, agents miss it), and it accumulates into a doc that nobody trusts. Mechanized rules degrade loudly (CI fails) and are self-enforcing.

Mirabilis examples: `forbidigo` blocked bare error discards from being committed; `depguard` blocked engine↔TUI import inversions; the PTY and proxy lifecycle rules were encoded as integration tests that failed before the fixes and passed after.

## Output contract

Applying this skill to a design or a review produces:
1. Per-property checklist with pass / fail / cannot-verify-without-execution per item.
2. Mechanization candidates: which failing checks can become linter/CI/hook rules (with the specific tool and rule).
3. Gaps that cannot be mechanized: prose invariants, with a stated reason why no check can hold them.

Counter: for a prototype or throwaway script where failure isolation, lifecycle correctness, and idempotency are explicitly out of scope — state that in one line and skip. The bar applies to any system intended to run in production or to be maintained by others.

---
Provenance: distilled from the 2026-06-12 mirabilis rewrite — four production blockers found in adversarial review (proxy lifecycle, flock GC, PTY deadlock, dead-code twin) each map to one of the properties above; the mechanization examples (forbidigo, depguard, goleak) were enforcement tools applied during the session.
