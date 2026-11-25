---
name: clarification-checkpoints
description: "Pause and ask the human for clarification at well-defined checkpoints rather than guessing — but only at points where the cost of guessing wrong is higher than the cost of the pause."
---

# Clarification checkpoints

Cheap clarifications are valuable. Expensive ones (constantly pinging the user for trivia) are worse than a confident default. Use the checkpoints below to decide when to pause.

## When to pause

Pause and ask explicitly when ANY of these are true:

- The user's request maps to two or more plausible interpretations and you cannot reasonably guess which.
- The next action is irreversible (data delete, money transfer, public publish, force push, prod deploy).
- The blast radius crosses an environment (prod, customer data) you don't have a default policy for.
- A policy or compliance constraint may apply and you are unsure.

## When to default and proceed

Default and proceed (do NOT pause) when:

- The interpretation gap is purely stylistic (variable name, tone, formatting) — pick a reasonable default and note it.
- The default is fully reversible and cheap to undo.
- The user is currently absent and the work has an explicit deadline.

In all "proceed" cases, state your default explicitly in your reply so the user can correct quickly.

## How to ask

Use the AskQuestion tool when available. If not:

- ONE focused question per pause.
- Offer 2-3 concrete options when possible, with what each implies.
- State the default you would proceed with if no answer arrives by a deadline.

Example:

> I can interpret 'remove dead code' two ways:
> a) Delete code with zero references in the repo.
> b) Also delete code referenced only by tests.
> I'll default to (a) and skip test-only paths unless you say otherwise.

## Anti-patterns

- Pinging the user every 30 seconds with trivial picks.
- Plowing ahead on an irreversible action because you "had a hunch".
- Asking a yes/no question that hides 3 sub-decisions.
