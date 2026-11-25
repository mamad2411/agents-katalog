---
name: implicit-state-machines
description: Audit a codebase for hidden state machines in boolean clusters, status strings, nullable state, async flows, timers and scattered conditionals. Use when reviewing an application for impossible states, unclear transitions, concurrency risks, or safe UX/DX/agent-experience improvements.
license: MIT
metadata:
  version: "1.1.0"
  tags: "state-machines refactoring ux dx ax vibecoding code-quality"
---

# Implicit State Machines

**Find the state machines your app is already running by accident. Make them explicit, safe, testable and boring.**

## The mission

> Find the implicit state machines in this application. Make evidence-based decisions that improve user experience (UX), developer experience (DX), and agent experience (AX), while preserving existing behavior and avoiding unnecessary change.

This skill is a systematic audit and safe-improvement workflow—not an instruction to convert every boolean into a state machine.

1. **Find candidates systematically.** Use `references/detection-signals.md` and inspect the surrounding code before drawing conclusions.
2. **Make the lifecycle understandable.** Record states, events, transitions, guards, effects, ownership, and invariants.
3. **Improve all three experience layers.** A change must have a clear benefit for UX, DX, and AX, or explain the trade-off.
4. **Preserve behavior.** Characterize existing behavior, migrate incrementally, and verify the result. Never promise that regressions are impossible.

## What counts as an implicit state machine

A lifecycle is implicit when behavior depends on a phase, but that phase is encoded indirectly or distributed across code. Common examples:

- Boolean clusters that represent one lifecycle (`isLoading`, `isError`, `isSuccess`, `isRetrying`). N booleans allow up to 2^N combinations, even when only a few combinations make sense.
- `status`, `step`, `mode`, or `phase` strings repeated across files without one authoritative definition.
- Nullable-value combinations used to infer state (`data && !error`, `!user && !loading`).
- Refs or module variables used as lifecycle flags (`hasSubmitted.current`, `isMounted`, `didInit`).
- Timers, retries, debounces, and counters that determine what event is allowed next.
- Multi-step workflows spread across components or services: onboarding, checkout, authentication, uploads, payment, and forms.
- Backend lifecycles represented by loosely controlled status columns or timestamp-null checks.
- Agent/tool loops with hidden phases such as planning, awaiting approval, executing, retrying, and recovering.

A candidate is not automatically a defect. Confirm that the values describe one lifecycle and that the lifecycle affects behavior. A standalone toggle—such as whether a tooltip is open—is usually just a boolean.

## The Three-Lens Gate

| Lens | Ask | Evidence of improvement |
|---|---|---|
| **UX** | Can the user see contradictory, stuck, confusing, or unrecoverable states? | Deliberate loading, empty, success, failure and retry behavior; preserved input; accessible status feedback. |
| **DX** | Can a developer understand the lifecycle without tracing scattered setters? | One clear state owner, semantic names, explicit transitions, useful tests and diagnostics. |
| **AX** | Can a coding agent identify allowed changes and verify them safely? | Discoverable state/event definitions, explicit invariants, transition tables, deterministic tests and local conventions. |

AX means **agent experience** here. Accessibility is part of UX and must still be considered.

## Safety contract

These rules are mandatory:

1. **Audit before editing.** Discovery, ranking, and modeling are read-only. Do not edit while still trying to understand the lifecycle.
2. **Protect the working tree.** Inspect repository instructions and status first. Never discard, reset, stash, overwrite, or reformat unrelated user work.
3. **Characterize behavior first.** Add or identify tests for existing behavior before changing a complex or consequential lifecycle. Include quirks that callers may rely on.
4. **One machine per change.** Keep changes focused, reviewable, and individually revertible.
5. **Preserve contracts.** Keep public APIs, component props, function signatures, route behavior, event names, persistence formats, and visual output unchanged unless a change is explicitly approved and necessary.
6. **Use compatibility adapters.** When replacing legacy flags, derive old values from the new state during migration. Remove the adapter only after all readers and writers have moved.
7. **Do not invent states.** Derive states and transitions from code, tests, and observed behavior. Record ambiguity as an open question.
8. **Treat concurrency as behavior.** Consider request identity, stale responses, cancellation, duplicate events, idempotency, cleanup, retries, and out-of-order events. A reducer that ignores an event does not prevent the side effect that already ran.
9. **Ask before risky contract changes.** Stop before changing public APIs, database schema/migrations, persisted data shapes, analytics event names, security boundaries, or untestable behavior that cannot be characterized.
10. **Verify honestly.** Run the repository's relevant tests, type check, lint, and build where available. Report exact commands and outcomes. Never claim zero regressions or checks that were not run.

## Workflow

### Phase 0 — Orient (read-only)

- Identify language, framework, application boundaries, state-management conventions, and major workflow entry points.
- Read repository instructions, relevant source, tests, package scripts, routing, persistence, and async/data-fetching layers.
- Inspect the working tree and record existing changes.
- Identify baseline checks and pre-existing failures when practical.
- Confirm the requested scope: whole application, feature, workflow, or supplied snippet.

### Phase 1 — Hunt (read-only)

Use `references/detection-signals.md`. Inspect candidates across components, hooks, stores, services, routes, jobs, database models, mobile view models, and agent loops. For each candidate record:

- File and symbol (with line ranges when available).
- Evidence: flags, status strings, nullable combinations, effects, timers, retries, or transition handlers.
- The observed behavior the values control.
- Whether it is a true lifecycle or a false positive.

Cast a wide net, then discard isolated toggles and unrelated values.

### Phase 2 — Rank

Rank candidates qualitatively. Do not invent precision or performance measurements.

- **Impact:** Critical / High / Medium / Low.
- **Evidence confidence:** High / Medium / Low.
- **Change risk:** High / Medium / Low.
- **Action:** Fix now / add a confirming test / plan / leave alone.

Prioritize data integrity, user-visible failure, security, and correctness before stylistic cleanup. A high-impact, low-confidence suspicion should usually become a test, not an immediate refactor.

### Phase 3 — Model (still read-only)

For each consequential candidate, write down:

- **States:** mutually exclusive phases and the data each phase carries.
- **Events:** user actions, responses, timers, external events, and failures.
- **Transitions:** current state + event → next state, including ignored or rejected events.
- **Guards:** conditions that permit or block a transition.
- **Effects:** I/O, rendering, navigation, persistence, cleanup, and cancellation.
- **Invariants:** what must always be true.
- **Ownership and lifetime:** source of truth, initialization, reset, persistence, cancellation, and termination.
- **Impossible or ambiguous states:** combinations currently reachable, and behavior that cannot be inferred safely.

Use a transition table or Mermaid `stateDiagram-v2`. Do not invent product behavior when the source is unclear.

### Phase 4 — Choose the lightest representation

| Situation | Prefer |
|---|---|
| A few exclusive phases with limited history | Discriminated union, enum, sealed type, or equivalent |
| Many events and pure transition logic | Reducer or explicit transition function with exhaustive matching |
| Nested/parallel states, history, timers, orchestration or visualization requirements | Statechart library, only when its complexity is justified |
| Server-owned workflow (orders, jobs, payments) | Status enum + centralized transition policy + database constraints where appropriate |
| Python | `Enum` + dataclasses + `match`, or a small typed transition function |
| Swift / Kotlin / Rust | Associated-value enum, sealed class, or enum + exhaustive `match` |

Default to the simplest option already supported by the codebase. Do not add a dependency merely to make the design look formal.

### Phase 5 — Lock current behavior

Add or improve characterization tests before changing consequential behavior. Cover normal paths and important quirks. Tests should describe the current contract and become the regression baseline. If behavior cannot be tested or observed, disclose that limitation and do not silently change it.

### Phase 6 — Refactor incrementally (only when implementation is requested)

1. Add the explicit state model and transition logic beside the existing implementation.
2. Keep legacy readers working through derived compatibility adapters where necessary.
3. Migrate writers to dispatch semantic events.
4. Migrate readers to use the explicit source of truth.
5. Handle stale async results, abort/cancellation, duplicate side effects, cleanup, and retry semantics as appropriate.
6. Remove obsolete flags and adapters only when no consumers remain.
7. Run focused checks after each step. Stop and reassess if behavior changes unexpectedly.

Do not claim a reducer alone prevents network requests, timers, writes, or other effects. Guard or cancel the effect at its source, and validate response identity before committing asynchronous results.

### Phase 7 — Verify

Check, where relevant:

- Every intended state and transition, including invalid or ignored events.
- Initial, loading, empty, success, failure, retry, cancellation, reset, and timeout paths.
- Duplicate submissions and out-of-order asynchronous responses.
- Navigation away/back, remount, refresh, and persisted-state restoration.
- Cleanup of listeners, subscriptions, timers, and requests.
- UI output, accessibility semantics, keyboard/focus behavior, and status announcements.
- Public APIs, events, routes, persistence formats, and compatibility adapters.
- Relevant unit, integration, end-to-end, lint, type-check, and build commands.

### Phase 8 — Report

Use `references/report-template.md` for the full report. Always separate verified evidence from inference and disclose what was not tested.

## Required report

For a meaningful repository audit, include:

1. **Executive readout** — overall condition and the most important decision.
2. **State-machine inventory** — workflow, owner/location, states, events, confidence.
3. **Transition model** — a table or state diagram for the most consequential flows.
4. **Findings** — severity, evidence, likely failure, UX/DX/AX impact, confidence, and risk.
5. **Decision** — what to change, what to preserve, and why.
6. **Implementation summary** — changed files and compatibility notes, only when code was changed.
7. **Verification** — commands, outcomes, gaps, and residual risks.
8. **Left alone / open questions** — sound code that was not changed and unknowns that need product or maintainer input.

## Anti-patterns

- Turning every boolean into a state machine.
- Introducing XState or another dependency for a three-state fetch with no need for it.
- Big-bang rewrites or unrelated formatting churn.
- Changing visual behavior while claiming the refactor is behavior-preserving.
- Assuming that ignoring a reducer event cancels an already-started side effect.
- Hiding a new state behind a string literal scattered across files.
- Declaring success without running or reporting the relevant checks.

## Direct refactor mode

When the user asks for a code-first refactor rather than a repository-wide audit, use the same safety gates and deliver the concise sequence: diagnosis, relevant refactored code or focused patch, UX/DX/AX breakdown, and verification. The repository also ships a dedicated `vibe-refactor-protocol` skill for agents that support multiple skill folders.

## Completion standard

A successful audit makes hidden behavior visible and decisions safer. It does not require every candidate to become a formal state machine, a new dependency, or a refactor. Prefer a small, evidenced improvement—or an explicit decision to leave sound code alone—over architecture for architecture's sake.
