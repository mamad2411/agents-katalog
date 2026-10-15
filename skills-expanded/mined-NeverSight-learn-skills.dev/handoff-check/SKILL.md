---
name: handoff-check

description: Check whether the current work should continue, be handed off, or have its context compacted or cleared. Use when a session is becoming long, context is getting noisy, or you are unsure whether to keep working in the current context.

metadata:

  disable-model-invocation: true

---

# Handoff Check

Should we keep going, hand off, or clear context?

This skill evaluates whether the current work should continue in the current context, be handed off to a fresh context, or have the current context compacted or cleared before continuing.

It is a **context health check**, not a task planner.

The goal is to prevent degraded work caused by excessive context, accumulated noise, stale assumptions, or a session that has grown beyond a useful working boundary.

## Assess the current context

Before answering, inspect the available context and current state of the work:

- What the user is trying to accomplish
- What has already been completed
- What is currently in progress
- Important decisions and constraints
- Open questions or unresolved work
- Relevant files, tools, and external resources
- Repeated, obsolete, or low-value context
- Whether the current context is still easy to reason about accurately
- Whether the remaining work can reasonably continue here

Pay particular attention to information that is still necessary for the next steps.

Do not treat context length alone as sufficient reason to hand off.

A long session can still be healthy when the relevant state is clear and easy to recover.

## Decide

Choose exactly one verdict:

### Continue

Use when the current context is still coherent, relevant, and sufficient to continue the work safely.

No handoff or context cleanup is needed yet.

### Compact

Use when the work should continue in the same overall session, but the context contains enough accumulated detail, repetition, or obsolete information that reducing it would improve reliability.

Recommend what information must survive the compaction.

The goal is to preserve the working state while removing unnecessary context.

### Handoff

Use when continuing in the current context is becoming counterproductive, or when the remaining work is better continued in a fresh context.

Recommend the minimum handoff package needed for the next context to resume correctly.

A handoff should preserve:

- Current objective
- Current state
- Completed work
- Remaining work
- Important decisions
- Constraints
- Relevant files or resources
- Immediate next step

Do not reproduce the entire conversation.

### Clear

Use when the current context is no longer useful for the task and there is no important state that needs to be preserved beyond a concise summary.

Recommend clearing the context only when doing so is unlikely to lose necessary information.

## Signals for handoff or cleanup

Treat these as warning signs:

- The conversation contains substantial obsolete or unrelated context.
- The same information is being repeated.
- Important decisions are difficult to locate.
- The current state is becoming ambiguous.
- The agent is relying on assumptions that were established many turns ago.
- The task has changed significantly from the original context.
- The context contains many failed approaches that are no longer relevant.
- A fresh context would make the remaining work easier to reason about.
- The remaining work has a clear boundary that can be handed off cleanly.

Do not recommend a handoff merely because the conversation is long.

## Context preservation

When recommending `Compact` or `Handoff`, identify the minimum state that must survive.

Prefer a concise state representation such as:

```text
Goal:
Current state:
Completed:
Remaining:
Decisions:
Constraints:
Files/resources:
Next step:
````

Do not preserve irrelevant conversation history.

Do not invent missing state.

## How to answer

Format every reply as:

1. **Verdict** — `Continue`, `Compact`, `Handoff`, or `Clear`.
2. **Why** — one short explanation of the current context state.
3. **Preserve** — the minimum information that must survive, when applicable.
4. **Next action** — the exact action to take now.

Stop after that.

## Important boundaries

* Do not perform the handoff itself unless explicitly asked.
* Do not compact or clear context yourself.
* Do not create a project plan.
* Do not decide that work is complete merely because a handoff is appropriate.
* Do not treat token count as the only signal.
* Do not discard important decisions, constraints, or current state.

## Maintenance

This skill should remain focused on deciding whether the current context is suitable for continued work.

Only update this file when its context-health criteria, verdicts, or output format need to change.