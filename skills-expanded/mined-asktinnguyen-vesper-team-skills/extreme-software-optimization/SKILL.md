---
name: extreme-software-optimization
description: "Use for a one-lever measured pass on a profiled performance hotspot: preserve correctness, change one thing, benchmark before/after, account for noise, and keep only proven improvements."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [optimization, performance, benchmarking, correctness, refactoring]
    related_skills: [profiling-software-performance, repeatedly-apply-skill, code-optimization-agent-skills]
    source: "https://x.com/doodlestein/status/2059715849196564726"
    note: "Clean-room Hermes-compatible implementation from public workflow description."
---

# Extreme Software Optimization

## Overview

Use this skill to optimize code only after profiling has identified a real bottleneck. The process is intentionally strict: preserve behavior, change one lever at a time, benchmark before and after, and keep only optimizations with demonstrated value.

The goal is not clever code. The goal is faster software with proven behavioral equivalence.

The leading word is **one-lever measured pass**: choose one measured hotspot, change one optimization lever, prove correctness, prove speedup, then keep or revert.

Step completion gates:

- Target selected when the hotspot, workload, metric, and profiling evidence are named.
- Guardrail complete when tests, goldens, invariants, or manual checks can fail on behavioral drift.
- Baseline complete when command, environment, input, iterations, units, and raw numbers are recorded.
- Hypothesis complete when exactly one lever is chosen and the expected metric movement is stated.
- Keep/revert complete when the delta exceeds measurement noise and maintainability remains acceptable.

## When to Use

Use when:

- `profiling-software-performance` has produced a ranked hotspot.
- A benchmark or workload exists.
- The user wants speedups without regressions.
- A performance change needs rigorous evidence.

Don't use when:

- No baseline exists.
- Correctness cannot be checked.
- The proposed change is speculative and unmeasured.
- The code path is not relevant to the target workload.

## Optimization Protocol

1. **Select one target**
   - Choose one measured hotspot from the profiling report.
   - State why it is the highest-value target.
   - Define the target metric: latency, throughput, CPU, memory, allocations, startup, bundle size, cost, etc.

2. **Prove current behavior**
   - Run existing tests.
   - Add or identify focused tests for the hotspot.
   - Capture golden outputs, snapshots, invariants, or property tests if behavior is subtle.
   - If there is no guardrail, create one before optimizing.

3. **Record baseline**
   - Run the benchmark/workload before changes.
   - Record exact command, environment, input size, iterations, and numbers.
   - Keep raw numbers in notes so deltas can be audited.

4. **Form a hypothesis**
   - Explain why the change should improve the measured hotspot.
   - Classify the lever: algorithmic complexity, data structure, caching, batching, allocation reduction, IO reduction, query/index change, concurrency, serialization, compile/build option, etc.

5. **Make one focused change**
   - Avoid drive-by refactors.
   - Keep the diff small enough to review.
   - Preserve public API and documented behavior unless explicitly allowed.

6. **Verify equivalence**
   - Re-run correctness tests and golden/invariant checks.
   - Compare outputs where applicable.
   - If behavior changes unexpectedly, revert or isolate the change.

7. **Benchmark again**
   - Run the same workload under comparable conditions.
   - Repeat enough to reduce noise.
   - Compute before/after delta.

8. **Adversarial simplification review**
   - Review the branch as an adversary before accepting the pass.
   - Ask: did the optimization add layers, indirection, cleverness, duplicate logic, hidden state, brittle caches, or policy drift?
   - Look for opportunities to reduce layers, remove complexity, and increase reliability while maintaining the original intent and measured win.
   - Ensure repo-wide policies from `AGENTS.md`, README, tests, lint, typing, style, and architecture conventions are still maintained.

9. **Decide keep/revert**
   - Keep only if improvement is real, correctness holds, repo policies hold, and the simplification review does not reveal unacceptable complexity.
   - Revert if the gain is noise, risk is too high, code becomes unmaintainable, repo policies are violated, or tests fail.
   - Document tradeoffs.

## Optimization Levers

Consider, in order of evidence:

- Better algorithmic complexity.
- Avoid repeated work with safe memoization/caching.
- Reduce allocations and copies.
- Batch IO/database/network calls.
- Add or improve database indexes only with query-plan evidence.
- Replace linear scans with maps/sets/tries/indices where semantics permit.
- Move invariant computation out of loops.
- Stream instead of materializing large data.
- Use concurrency only when it reduces the measured bottleneck without race risk.
- Tune serialization/parsing only when profiles show it matters.
- Use lower-level optimizations last, after algorithmic wins.

## Output Standard for Each Pass

For every optimization pass, report:

- Target hotspot and profiling evidence.
- Correctness guardrails used or added.
- Baseline metric.
- Hypothesis.
- Change summary.
- Correctness verification results.
- After metric.
- Delta and confidence.
- Adversarial review findings: complexity removed, layers reduced, reliability improved, repo-wide policies maintained, and original intent preserved.
- Keep/revert decision.
- Remaining risk.

## Stop Conditions

Stop optimizing when:

- The current hotspot no longer dominates.
- Further gains are below measurement noise.
- Correctness guardrails are insufficient and cannot be improved safely.
- The next change would require product/API tradeoffs.
- Time/budget is exhausted.
- The user asked for a fixed number of passes and they are complete.

## Acceptance checklist and common pitfalls

1. **Optimizing without tests.** Create guardrails first.
2. **Changing multiple things.** One focused lever per pass makes attribution possible.
3. **Trusting microbenchmarks over user workload.** Microbenchmarks are useful only if tied to the real hotspot.
4. **Ignoring maintainability.** A tiny speedup that makes the code fragile is usually a regression.
5. **Confusing throughput and latency.** Optimize the metric the user cares about.
6. **Claiming isomorphism by inspection.** Use tests, golden outputs, or invariants.

## Verification Checklist

- [ ] Target comes from measured profiling evidence.
- [ ] Correctness guardrails exist before the change.
- [ ] Baseline is recorded.
- [ ] One focused change was made.
- [ ] Correctness checks passed after the change.
- [ ] Same benchmark/workload was re-run.
- [ ] Delta is reported with units and percent.
- [ ] Adversarial review checked for unnecessary layers, complexity, reliability risks, repo-policy drift, and original-intent drift.
- [ ] Keep/revert decision is explicit.
