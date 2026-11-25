---
name: grill-me
description: Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking before building, or uses any 'grill' trigger phrases.
disable-model-invocation: true
---

Interview me relentlessly about every aspect of this plan, decision, or idea until we
reach a shared understanding. Walk down each branch of the decision tree, resolving
dependencies between decisions one-by-one. For each question, provide your recommended
answer.

Ask the questions one at a time, waiting for feedback on each question before continuing.
Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it
up rather than asking. The *decisions*, though, are mine — put each one to me and wait
for my answer.

Do not act on it until I confirm we have reached a shared understanding.

## Question dimensions

Walk these facets in whatever order fits the plan, but make sure none is left unexamined:

- **Goal & success criteria** — What outcome defines "done"? How will we know it works?
- **Scope & boundaries** — What is explicitly in and out? What are we not building?
- **Assumptions & constraints** — What must be true for this to hold? What is fixed vs. flexible?
- **Dependencies & ordering** — Which decisions depend on which? Which must be resolved first?
- **Edge cases & failure modes** — What happens at the extremes? How does it degrade?
- **Alternatives considered** — What else could solve this? Why was it rejected?
- **Risk & reversibility** — What is hard to undo? Where is the blast radius if wrong?

## Convergence signals

Keep going until each of these is true:

- Every open branch of the decision tree has a recorded decision.
- Dependencies between decisions are resolved in a consistent order.
- The user explicitly confirms shared understanding.

Only then, and only on explicit user confirmation, proceed to act on it.
