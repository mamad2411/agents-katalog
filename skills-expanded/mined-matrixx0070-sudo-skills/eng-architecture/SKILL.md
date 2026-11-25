---
name: eng-architecture
version: 1.0.0
description: Author or evaluate an Architecture Decision Record (ADR) that captures context, real options, honest trade-offs, and a defensible, reversible-when-wrong decision.
author: matrixx0070
tags: [architecture, adr, decisions, trade-offs, design, records]
capabilities: []
---

## When to use

Reach for this when a choice is expensive to reverse — a datastore, a framework, a service boundary, an auth model, a build-vs-buy call — or when someone will ask "why did we do it this way?" in six months. Also use it to grade an ADR someone else wrote.

**Not for:** reversible, local choices (a variable name, a private helper, a lint rule). If undoing it is a one-line diff, don't spend an ADR on it.

## Method

1. **State the decision in one sentence**, then the forces driving it: constraints, deadlines, team skills, existing systems, and non-functional targets (latency, cost, compliance).
2. **Enumerate at least three real options.** "Do nothing" and the obvious incumbent both count. If an option is a strawman you'd never pick, cut it and find a real one.
3. **Cost each option** with concrete pros, cons, risks, and rough effort/dollars/ops burden. Quantify where you can; a guessed number beats an adjective.
4. **Score against the forces from step 1.** If two options tie, the tiebreaker is reversibility — prefer the one you can back out of cheaply.
5. **Decide.** Write what you consciously give up and the signal that would make you reverse course.
6. **If the decision is hard to reverse and confidence is low**, ship a time-boxed spike or a reversible pilot first, then record the outcome — don't commit the org on a hunch.
7. **When evaluating an existing ADR**, verify options are non-trivial, trade-offs are honest, and the decision actually follows from the stated forces. If it doesn't, that mismatch is your finding.

## Example

Input: "Pick a queue for order events, ~2k msg/s, at-least-once, small team."

```
Decision: Use managed SQS for order events.
Forces: 2k msg/s, at-least-once OK, 3 engineers, no ops on-call for infra.
Options: SQS (managed, at-least-once, cheap ops) | Kafka (replay + high
  throughput, heavy ops) | Postgres table as queue (simple, caps ~500 msg/s).
Decision: SQS — meets throughput, near-zero ops.
Trade-off accepted: no log replay; if we need event sourcing later, revisit.
Revisit trigger: sustained >10k msg/s OR a replay requirement appears.
```

## Pitfalls

- **Retrofitting the decision** — writing the ADR to justify a call already made. Enumerate options before you pick.
- **Strawman alternatives** listed only to make the favorite win.
- **Vague trade-offs** ("more scalable") with no number, cost, or named downside.
- **No revisit trigger** — an ADR with no exit condition becomes dogma nobody dares question.

## Output format

```
# ADR-<n>: <Title>
Status: Proposed | Accepted | Superseded by ADR-<m>
Context: <forces, constraints, non-functional targets>
Options considered:
  | Option | Pros | Cons | Rough cost |
Decision: <chosen option + why it follows from the forces>
Trade-offs accepted: <what you gave up, explicitly>
Consequences: <follow-up work, migration, new ops duties>
Revisit trigger: <the signal that invalidates this>
```
