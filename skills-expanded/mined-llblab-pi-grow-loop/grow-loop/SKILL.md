---
name: grow-loop
description: Meta-protocol for visible, scope-locked skill loops while another bounded pass remains useful. Use for grow-loop or requests combining loop with a skill, such as active drying loop, drying loop, or brain storm loop. Grow loop advances project capability through while-true; drying loop reduces carrying cost through active-drying; other skill loops retain that skill's purpose and permissions. Also use for concrete multi-slice outcomes that benefit from validated continuation checkpoints. Do not activate for standalone skills without loop intent, ordinary one-shot work, informational mentions of loops, unrelated plans, or work with no safe useful next pass.
---

# Grow Loop

Own one decision: after one bounded invocation of the selected skill, either schedule exactly one next visible invocation with `grow_loop` or stop with proof.

```text
lock scope and skill → run one bounded invocation → consume handoff → decide once
  ├─ continue: call grow_loop once, then end the turn
  └─ stop: do not call grow_loop; return proof
```

Do not own implementation details. The selected skill owns its bounded pass; `while-true` is the default for project growth. `grow_loop` owns only idle-deferred runtime scheduling.

There is no goal object, budget, cycle count, hidden process, background agent, or slash-command control surface. For generic prompts such as `go`, `continue`, or `do it`, infer intent from context; explicit protocol names remain exact overrides.

## Entrypoint Routing

Apply lexical intent before execution-shape inference:

- Explicit standalone `while-true` selects only the portable worker. Do not activate Grow Loop or call `grow_loop` from its handoff unless the user later requests Grow Loop continuation.
- Explicit `grow-loop` or `grow loop` selects this meta-protocol with `while-true` for project growth.
- A request combining `loop` with a skill selects this meta-protocol with that skill: `active drying loop` and `drying loop` select `active-drying`; `brain storm loop` selects `brain-storm`. Resolve names and aliases from available skills, not a runtime keyword matcher. Mentioning a loop in code, quoting an example, or discussing this protocol is not an execution request.
- A standalone skill request without loop intent runs one bounded pass and stops; do not silently promote `active drying` or `brain storm` into a loop.
- The combined `while true | grow loop` prompt is reserved for internal continuation of an already selected sequence; it resumes the locked skill, not necessarily `while-true`.
- When no protocol is named, use ordinary one-shot execution for a coherent change even when it needs multiple internal steps. Use Grow Loop for a concrete outcome that benefits from multiple independently validated slices, plan reconciliation, and operator-visible checkpoints.

Natural routing into Grow Loop requires a concrete outcome or scope, safe actionable or preparable work, and no one-shot instruction. Project growth through `while-true` also requires a truthful backlog that exists or can be bootstrapped. Other skill loops use their own evidence and do not need a backlog merely to loop. The distinction is the value of independent checkpoint boundaries, not task size or a confirmation ritual. Routing happens before invoking the selected skill; it never escalates itself.

Growth expands useful capability; drying reduces carrying cost and accidental complexity while preserving capability and guarantees. These are complementary directions, not an automatic alternating cycle. Other skills retain their own purpose: a `brain storm loop` may narrow questions or converge a design, but cannot turn unanswered questions into invented user decisions or implementation approval.

## Scope Lock

Lock the project, directory, file, issue, task, or scoped outcome selected by the user. Conversation context may supply it only when it identifies the next safe slice precisely.

Load the selected skill from its declared location and pass it the locked scope. If it is missing or ambiguous, request the smallest missing input; do not substitute another skill.

For `while-true`, that skill alone resolves and validates the canonical open-work surface, including any `Canonical open work:` declaration. Retain the surface returned in its handoff; do not run a second discovery algorithm here. Other skills keep their own source-of-truth and validation rules; do not wrap them in `while-true` or impose its plan protocol.

Ignore unrelated repositories, temporary or generated directories, dependencies, caches, archives, and stale plans.

Keep the selected scope, skill, and any declared work-surface ownership stable across iterations. Re-select only when the user redirects the work or verified reality proves another surface governs the same scope. A stale or moved declaration requires repair or an explicit ambiguity stop, not harvesting other available work to preserve momentum.

Include the selected skill, scope, and next useful slice in each checkpoint handoff so the unchanged runtime prompt can recover them from conversation context, including after compaction. If that selection cannot be recovered, stop rather than defaulting to `while-true`.

If no trustworthy scope exists, do not invoke the worker or call `grow_loop`; request the smallest missing input.

## Intent Precedence

Interpret the latest context in this order:

1. Latest user direction or change of scope.
2. Explicit continuation-break intent or durable stop marker.
3. Worker evidence, safety gates, and blockers.
4. Remaining useful work within the selected skill and scope.

Any user prompt except the runtime's exact expected continuation prompt exits the runtime rhythm and is authoritative context, including operator input injected through another extension. Decide whether it means answer, stop, restart, continue, or change direction; do not infer continuation from available work alone.

Escape remains baseline Pi behavior, not a Grow Loop control. Treat it as a continuation break only when session context exposes that intent or a durable stop marker.

If a queued `while true | grow loop` prompt arrives after continuation-break intent, do no repository work, run no validation for momentum, and do not call `grow_loop`. Acknowledge the break and provide the current stop proof when useful. Resume only after explicit restart intent clears the stop context.

## Continuation Checkpoint

After one selected-skill invocation, consume its result without redoing its analysis. For `while-true`, use its [Handoff](../while-true/SKILL.md#handoff). For another skill, retain a compact checkpoint: selected skill and scope, what changed or was proven, validation or evidence, next useful slice, blockers, and a signature of material results. Reuse its native report rather than requiring a new artifact or parallel backlog. The selected skill owns domain evidence; this Skill owns the continuation decision.

A useful invocation must change an artifact, increase validation confidence, narrow a blocker or design question, improve plan truth, or remove a risky assumption. Drying must demonstrate lower carrying cost with preserved obligations, not just fewer lines; brainstorming must reduce uncertainty, not generate endless variants. Respect the selected skill's natural boundaries, approval gates, and requests for user input. Do not schedule around a question that requires the user's answer.

The `while-true` worker may batch independent low-coupling tasks into one validation cohort; Grow Loop evaluates the cohort handoff as one checkpoint and does not reinterpret its batching. Otherwise treat the invocation as a possible no-op.

Compare the checkpoint signature with the previous invocation. A repeated signature with only unchanged reads, checks, or blocker restatement is terminal no-op evidence.

## Decide Once

### Continue

Continue only when every condition holds:

- Latest user intent permits continuation and no stop marker is active.
- The locked scope, selected skill, and any governing work surface remain trustworthy.
- The previous invocation produced useful evidence.
- A high-value `local-actionable` or useful `gated-but-preparable` slice remains.
- Continuing crosses no destructive, publishing, credential, account, external, or approval gate.
- The checkpoint signature is not a repeated no-op.
- Validation has not regressed enough to require a strategy change or human decision.

Approval- or externally gated scopes may continue only through safe preparation that materially reduces future risk. Stop when preparation is exhausted; never cross the gate.

When all conditions hold, call `grow_loop` exactly once, then end the turn. Omit `after_seconds` for the default 3-second operator-interrupt delay, or increase it from 3 up to 3600 when continuation should wait for known asynchronous work. Never shorten the 3-second minimum because it preserves the operator's chance to redirect the next iteration. Choose a longer delay from concrete evidence about expected remaining duration, use the one-hour limit only for genuinely long-running work, and reassess after every wake so the next delay tracks the latest state rather than mechanically repeating the previous value. The tool waits until Pi is idle with no pending messages, shows the configured countdown, and sends the next visible `while true | grow loop` prompt only if the session remains idle.

### Stop

Stop and do not call `grow_loop` when any condition holds:

- User intent means stop, answer, wait, or change direction.
- Scope or selected skill is missing, ambiguous, redirected, or untrustworthy.
- Work is complete or no high-value actionable or preparable slice remains.
- Remaining work is gated and useful preparation is complete.
- The checkpoint signature repeats.
- Validation requires a strategy change or human decision.
- Continuing would be unsafe, destructive, speculative, or outside scope.

Stopping with exact evidence is progress. Do not schedule speculatively and do not call `grow_loop` more than once per decision.

## Stop Proof

Return a compact terminal handoff:

- Locked scope, selected skill, and what was closed or narrowed.
- Validation or evidence proving the state.
- Terminal checkpoint signature in concise form.
- What remains done, gated, or non-actionable.
- Exact input or state change that would make restart useful, if any.

## Invariants

1. Scope and selected skill remain locked; internal continuation never silently changes the skill.
2. The selected skill owns bounded execution; Grow Loop consumes its evidence and owns continuation only.
3. User intent outranks repository availability.
4. Each checkpoint produces one decision and at most one `grow_loop` call.
5. Safe preparation may approach a gate but never cross it.
6. Repeated no-op evidence stops the loop.
7. No trustworthy scope or evidence means no continuation.
8. Explicit protocol naming overrides automatic routing; the worker never self-escalates.
