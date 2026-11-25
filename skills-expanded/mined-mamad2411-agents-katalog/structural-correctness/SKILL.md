---
name: structural-correctness
description: Use when planning, implementing, reviewing, verifying, operating, investigating, or retiring software where correctness, boundaries, blast radius, invariants, tests, observability, rollouts, ownership, or deletion safety matter.
---

# Structural Correctness

Build correctness into the shape of the system, not into the vigilance of the people keeping it running.

Credit: adapted from *The Shape of the System* by shapeofthesystem.com.

Core objective:

> Minimise what a tired engineer must hold in their head to make a correct change, while bounding the blast radius of anything caller-, attacker-, or environment-controlled.

## Tiebreaker

When principles pull against each other, decide by control and blast radius:

| Input / growth | Blast radius | Default |
|---|---:|---|
| Caller-, attacker-, dependency-, or environment-controlled | Wide | Pay the structural cost now. |
| Caller-controlled | Contained | Add the smallest hard bound. |
| Self-controlled | Wide | Prefer reviewable, reversible steps. |
| Self-controlled | Contained | Keep it simple; defer and write down why. |

Do not cargo-cult every rule into every change. A missing limit on hostile input is not YAGNI; a speculative abstraction for one caller is clutter.

## Default output

Use this shape for broad design/review answers. Compress when the ask is narrow, but keep the decision points explicit.

```md
## Structural objective
- Cognitive load reduced by:
- Blast radius bounded by:

## Boundaries and invariants
- Parsed/checked at boundary:
- Illegal state made unrepresentable by:
- Trust/auth/size limits:

## Time, resources, and mutation safety
- Deadlines / cancellation:
- Resource bounds / teardown:
- Race safety / idempotency:

## Failure, observability, and degraded behavior
- Visible failure path:
- Signals emitted/read:
- Degraded tier or abort decision:

## Change lifecycle
- Tests / reproducibility:
- Rollout / reversibility:
- Owner / expiry / runbook:

## Decision
- Must fix now:
- Can defer with reason:
- Simplify/delete instead:
```

## Phase-specific subskills

Use this skill as the umbrella lens when the task spans phases or the phase is unclear. When the user is inside one phase, load the smaller subskill instead.

| Phase | Use subskill | Structural checks |
|---|---|---|
| Triage | `structural-triage` | Treat report as untrusted; reproduce before ranking; rank by evidence and blast radius; assign one owner; record explicit disposition. |
| Planning | `structural-planning` | Bound load-bearing unknowns; anchor facts to owners; define done once; cap scope; separate decision from doing; sequence reversible steps; name failure modes. |
| Implementing | `structural-implementing` | Parse at the door; keep reasoning local; give ambient dependencies one seam; use revealing names; deadline waits; bound resources; make mutation atomic/idempotent; make failures visible; write contract tests. |
| Integrating | `structural-integrating` | Map shared substrate and cycles; pin the boundary contract; bound what the whole can do to this part and what this part can do to the whole; give distributed invariants a home; ramp in dark; probe end to end. |
| Reviewing | `structural-reviewing` | Read for locality; audit boundaries; hunt silent swallows; find caller-controlled unbounded growth; find check-then-act windows and unsafe replay; trace acquire to release; judge blast radius/reversibility; demand contract tests. |
| Verifying | `structural-verifying` | Watch the original repro fail before and pass after; verify acceptance criteria, not the diff; drive worst boundary input; exercise degraded paths; replay/interleave/interrupt stateful operations; verify at reachable scale; make the regression reproducible. |
| Operating | `structural-operating` | Ship behind reversible flags/canaries when radius justifies it; promote on signals; split release decision from irreversible act; rehearse degradation; use deadlines, backoff, jitter, breakers, and clean shutdown; give operational artefacts owners and expiry. |
| Investigating | `structural-investigating` | Name one question; pin a deterministic repro or measured failure rate; falsify and bisect; read existing telemetry first; distrust narratives and wall-clock ordering; throw spikes away; hand off diagnosis plus a failing test. |
| Retrospective | `structural-retrospective` | Reproduce cause from signals; blame the system gap, not the person; turn missing signal into alert/test; delete the failure mode before adding guardrails; every follow-up has owner/date; feed work back to triage. |
| Retirement | `structural-retirement` | Prove zero use from live telemetry over the real usage cycle; deprecate with a sunset window; contract in reverse; separate delete plan from delete act; remove/re-home derivations; honor hard-delete duties; delete code/config/docs together; guard against resurrection. |

## Core moves

### Boundaries and hostile input

- Parse unknown input once at a real boundary into a narrower value downstream code can trust.
- Bound size, count, expansion, recursion, and work before allocating or looping over caller-controlled input.
- Authentication says who; authorization decides whether this actor may do this action on this resource.
- Client-side validation is UX, not security.
- Dependencies, build plugins, CI, and generated artifacts are boundary crossings too: pin, verify, and scope them.
- Do not re-validate at every in-process hop after the boundary produced a trusted type.

### Locality, data flow, and names

- A reader should verify code from the changed unit and declared inputs; hidden globals, mutation, and call-order dependencies are design debt.
- Every ambient dependency (`now`, randomness, env, network client) gets one declared seam a test can reach.
- Keep control flow and invariants local. Share only named, owned facts.
- Name the load-bearing fact the type cannot carry: unit, ordering, side effect, freshness, or idempotency. Rename when the fact changes.

### Time, waits, and resources

- Every wait across an uncontrolled boundary has a deadline, cancellation or idempotent retry behavior, and an observable failure.
- Measure durations with a monotonic clock; use logical or fenced ordering across machines, not wall-clock timestamps.
- Caller-created growth gets ceilings: body size, row count, queue depth, retries, recursion, fan-out, cache keys, parallelism.
- Everything acquired has exactly one owner that releases it on every exit path: file handles, locks, timers, subscriptions, subprocesses, goroutines, connections.
- Subscribe for latency; reconcile for correctness when events can be missed or the event is silence.

### Mutation, replay, and irreversible effects

- Check-then-act on shared state is a race unless the check and act are atomic, serialised by one owner, or harmless by design.
- Retried or redelivered operations must be idempotent: stable key, upsert, dedupe table, state transition guard, inbox/outbox, or unique constraint.
- Split irreversible decisions from effects. Compute a reviewable plan; apply it with a version/snapshot check so the plan cannot go stale silently.
- For catastrophic verbs (`delete`, `charge`, `send`, `overwrite`, `launch`), test the decision without performing the effect.

### Failure, observability, and degradation

- The sin is silent swallow, not the error mechanism. Use language idiom, but never empty catch, ignored error, unhandled rejection, or fallback with no signal.
- Abort where a wrong result would silently propagate; degrade where staying up with less is the lesser harm.
- Emit signals that prove invariants and failure paths: rejection counts, retry/breaker state, queue depth, staleness, drift, deadline budget, records in/out.
- Telemetry is a bounded resource. Do not log secrets. Do not instrument theatre nobody reads.
- Fallbacks are code. Exercise them before relying on them.

### Change lifecycle and process

- Tests enforce invariants that types and schemas cannot carry. Test contracts and decisions, not private structure.
- A green check that was never red against the bug proves nothing about the bug.
- Make runs reproducible: pinned inputs, environment, seed, data version, and regeneration steps.
- Ship risky or wide changes reversibly: expand then contract, flags with owners/expiry, canaries, shadow traffic, rollbacks compatible with state.
- Process is structure where code runs out: one owner of record, runbook for known failures, four-eyes for irreversible/wide actions.
- Prefer deletion over guards. The state you do not have cannot be wrong.

## Common mistakes

| Mistake | Correction |
|---|---|
| “This is low risk because the happy path works.” | Drive the hostile input, retry, timeout, fallback, and teardown path that can actually break. |
| “We grepped the repo; nothing uses it.” | Public/removal proof needs live telemetry over the real usage cycle plus dependency search. |
| “The unit test passes; verification is done.” | Verification is a running-system claim against the original repro and acceptance criteria. |
| “Add a queue/retry/fallback for safety.” | Bound it, observe it, rehearse it, and make the operation idempotent; otherwise it is a second bug. |
| “Keep the flag/adapter forever just in case.” | Every scaffold gets owner and expiry; permanent means explicitly owned and reviewed. |
| “This name says it is safe.” | Names can lie. Let types/tests carry invariants where possible and rename when semantics change. |

## Red flags

Stop and redesign the touched slice when you are about to:

- Trust browser validation, request identity fields, or a dependency because it is popular.
- Allocate, recurse, fan out, retry, buffer, or query based on caller-controlled size with no ceiling.
- Add `SELECT then INSERT`, `if balance then debit`, or `processing` flags where two actors can interleave.
- Add a timeout that abandons work without cancellation or idempotent retry safety.
- Catch/log/continue without a decision and a signal.
- Add a fallback, flag, cache, adapter, alert, or migration with no owner and no removal/review date.
- Delete a public contract based only on source search.
- Claim a fix is verified without watching the relevant behavior fail before and pass after.

## Example: urgent checkout double-charge fix

```md
## Structural objective
- Cognitive load reduced by: one payment attempt state machine keyed by order/payment-attempt id.
- Blast radius bounded by: provider-side and database-side idempotency; duplicate submissions converge to one charge.

## Boundaries and invariants
- Parse checkout request at handler; derive actor/order from session and persisted cart, not payload userId.
- Unique constraint on payment_attempt.idempotency_key; state is Pending | Succeeded(providerChargeId) | FailedRetryable | FailedTerminal.

## Time, resources, and mutation safety
- Provider call has deadline and cancellation where supported.
- Retry uses same idempotency key; concurrent attempts use INSERT ON CONFLICT / compare-and-swap transition.

## Failure, observability, and degraded behavior
- Ambiguous provider timeout leaves attempt Retryable, not double-sent with a new key.
- Emit duplicate-submit count, provider idempotency response, and payment state transition metrics.

## Change lifecycle
- Test original duplicate-click/timeout repro red before fix, green after.
- Verify in provider sandbox or captured outbound request that only one charge exists.
- Keep regression for duplicate submission, ambiguous timeout, and concurrent attempt.
```
