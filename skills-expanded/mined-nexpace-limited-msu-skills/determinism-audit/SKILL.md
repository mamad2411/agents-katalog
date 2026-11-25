---
name: determinism-audit
description: Audits nondeterministic game behavior and flaky execution. Use when the same initial state and inputs produce different outcomes, a test fails intermittently or only under load, behavior differs by frame rate or machine, a replay diverges, or lockstep peers desynchronize. Establishes the required determinism boundary, reproduces and measures variance, isolates randomness, timing, async or thread ordering, state leakage, unordered iteration, and numeric drift, then reports verified causes and implements and stress-tests fixes only when requested.
---

# Determinism Audit

Define what must repeat, expose the first divergence, and distinguish a verified cause
from a lead.

## 1. Inspect the project and define the contract

Identify the engine or runtime, build and test commands, simulation loop, RNG ownership,
concurrency model, persistence, networking, and replay format. Determine whether the
request is an audit or includes authorization to change code.

Define the boundary before testing:

- the build and version;
- initial state and seed;
- ordered inputs and simulation ticks;
- same-machine, same-platform, or cross-platform requirement;
- whether replay, lockstep, or cross-version compatibility is required.

For replay, lockstep, or cross-platform work, read
[determinism-contracts.md](references/determinism-contracts.md).

## 2. Characterize the variance

Replay a known failing seed, input trace, test order, or schedule first. Otherwise repeat
the smallest failing case enough to expose its trigger conditions and estimate the
observed failure rate. Choose the sample from the observed rarity and risk rather than
using a universal minimum.

Record machine and platform, frame or tick rate, load, test order, external responses,
and every hidden input the contract does not hold fixed.

If the failure remains unreproduced, add logging or state snapshots and report the cause
as unverified. Authorized hardening of an independently confirmed unsafe construct is
still possible, but it is not a verified fix for the reported failure.

## 3. Locate the first divergence

Inspect and instrument these sources:

- **Randomness** — uncontrolled seeds, shared call-order coupling, random shuffles and
  simulation-affecting draws.
- **Time** — frame-count movement, variable simulation steps, wall-clock reads, timer
  precision, and unbounded catch-up.
- **Async and external events** — readiness races, network or storage responses, and
  events consumed in arrival order.
- **Threads and jobs** — shared writes, unordered reductions, and scheduler-dependent
  handoffs.
- **State leakage** — globals, singletons, caches, or persistent state surviving between
  runs, levels, and tests.
- **Iteration order** — order-sensitive work over unordered collections.
- **Numeric behavior** — accumulation drift, platform math differences, precision, and
  compiler or physics settings.

Compare state snapshots or checksums at meaningful ticks. The first differing tick is
more useful than the final wrong result.

## 4. Confirm the cause

Change one source of variance under controlled conditions and repeat:

- replay several explicit seeds and record RNG state;
- drive simulation with a fixed tick and the same ordered inputs;
- gate async work on readiness and sequence external events explicitly;
- reset state and control test order;
- stabilize iteration or reduction order;
- compare per-tick state to locate numeric drift.

Treat a source as confirmed only when the intervention repeatably changes or removes
the divergence. Correlation with one seed or one quiet run is a lead, not proof.

## 5. Report or fix

An audit reports the contract, reproduction rate, first divergence, confirmed causes,
unverified leads, and proposed fixes without editing code. When changes are authorized,
use the fix that matches the contract:

| Source | Fix direction |
|---|---|
| Simulation RNG | explicit state and purpose-specific deterministic streams; log state on failure |
| Time | fixed simulation tick with bounded catch-up; keep wall-clock time outside deterministic state |
| Async or external input | readiness gates plus deterministic event sequencing or recorded external input |
| Threads | defined data ownership and handoff points; deterministic ordering or reduction where results require it |
| State leakage | explicit initialization and teardown; pass owned state instead of retaining hidden state |
| Unordered iteration | stable keys and sorting when order affects results |
| Numeric drift | tolerance for assertions; quantization, fixed-point, or controlled math when results must match exactly |

Locks can remove data races but do not by themselves define result order. Epsilon
comparisons can stabilize assertions but do not make a simulation deterministic. Avoid
fixed sleeps, pass-until-green retries, and disabled tests; control the relevant clock,
event, or state instead.

## 6. Verify

Replay every known failing artifact, then stress the same conditions that exposed the
failure. Report before-and-after counts, sample conditions, and the determinism boundary.
Zero failures means none were observed in that sample, not that a rare failure is
impossible.

For replay or lockstep, compare state checksums at agreed ticks across the required
platforms and report the first divergence if any. Mark the result verified only within
the contract actually tested.

## Constraints

- Per-player variety is compatible with determinism. The same build, initial state,
  seed, ordered inputs, and simulation conditions must reproduce within the declared
  boundary.
- Report unconfirmed sources as leads rather than findings.
