---
name: arch-debugging
description: 'Systematic root-cause debugging and troubleshooting across code, builds, runtime, and infrastructure. Covers the 4-phase investigation method (root cause → pattern → hypothesis → fix), error detection across logs and codebases, ops/infra troubleshooting, and robust error-handling design. Use for ANY technical issue: test failures, production bugs, unexpected behavior, performance problems, build failures, integration issues.'
---

# Debugging & Troubleshooting (composite skill)

Systematic root-cause debugging and error handling. Composed from: systematic-debugging,
error-detective, devops-troubleshooter, error-handling.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Random fixes waste time and create new bugs. Quick patches mask underlying issues.
Symptom fixes are failure. **Violating this process is violating the spirit of debugging.**

## When to use

ANY technical issue: test failures, production bugs, unexpected behavior, performance,
build failures, integration issues. **Especially** under time pressure, when a quick fix
seems obvious, after multiple failed attempts, or when the issue isn't fully understood.

## Phase 1 — Root cause investigation (before any fix)

1. **Read error messages carefully** — full text, code, context, not just the headline.
2. **Reproduce consistently** — run the failing path (specific test, verbose output).
3. **Check recent changes** — commits, uncommitted changes, specific files. Most bugs
   come from a recent change.
4. **Gather evidence in multi-component systems** — isolate which component fails:
   logs, metrics, state, recent deploys.
5. **Trace data flow** — where does the bad value originate? What called this with the
   bad value? Keep tracing upstream to the source. Fix at the source, not the symptom.

**Phase 1 checklist**: error messages understood, issue reproduced, recent changes
reviewed, evidence gathered, problem isolated to a component, root-cause hypothesis formed.
*Do not proceed until you understand WHY it's happening.*

## Phase 2 — Pattern analysis

1. **Find working examples** — similar working code in the same codebase.
2. **Compare against references** — read the reference implementation completely.
3. **Identify differences** — every difference between working and broken, however
   small; don't assume "that can't matter".
4. **Understand dependencies** — what components/config/environment/assumptions does it need?

## Phase 3 — Hypothesis and testing

1. **Form a single hypothesis** — "I think X is the root cause because Y." Be specific.
2. **Test minimally** — the smallest change that confirms/refutes the hypothesis.
3. **Evidence over intuition** — the test result, not the guess, decides.

## Phase 4 — Fix and verify

1. **Fix at the root cause**, not the symptom.
2. **Verify the fix** — the original repro passes; no regressions in related paths.
3. **Add a regression test** — the bug should never silently return.

## Error detection across logs and codebases

- **Search patterns**: stack traces, error classes, timeouts, panics, `null`/`None`/
  undefined, silent catches, swallowed errors.
- **Correlate across systems**: same error in different components → shared root cause
  (config, dependency, deployment).
- **Anomalies**: unusual log volumes, spikes in error rate, timeouts clustering.
- Distinguish **root cause** from **symptom**: an error surfacing in component A may
  originate in component B.

## Ops / infrastructure troubleshooting

- **Systematic checklist**: is the service up? port bound? config valid? recent deploy?
  resource limits (memory/disk/fd)? network path (DNS, TLS, firewall)? dependency healthy?
- **Bounded diagnostics**: check in order of cheapness — status, logs, config, connectivity,
  resources — and stop when the cause is found.
- **Rollback bias**: if a recent change is the most likely cause, verify the rollback
  hypothesis before deep debugging.

## Error-handling design (prevention)

When fixing or writing new code, apply robust error handling:
- **Handle errors explicitly** — no empty `catch`, no swallowing.
- **Typed errors** — distinguish recoverable vs fatal.
- **Meaningful messages** — what failed, where, how to fix.
- **Retries with backoff** for transient failures; circuit breaker for flaky deps.
- **Observability** — log the error with context (request id, state) at the right level.
- **Fail-closed** where correctness matters; fail-open where availability matters —
  choose deliberately.
- Never lose data or silently skip on partial failure.

## Output

A debugging session should produce: root cause (one sentence, evidenced), the minimal
fix, verification evidence (repro passes + no regressions), and a regression test.

## Related skills
- `arch-code-review` — review code for silent failures and error-handling gaps
- `arch-code-quality` — conventions for error handling and observability
- `arch-code-architecture` — system design decisions that prevent failure modes
