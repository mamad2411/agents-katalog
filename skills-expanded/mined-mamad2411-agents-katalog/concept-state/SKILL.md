---
name: concept-state
description: Design a concept's state — the local "micromodel" of data needed to support its actions. Each concept gets an independent state model to be merged later.
---

# Concept State

Design the state that supports a concept's actions. This is the concept's "micromodel" — a local data model designed independently.

## When to use

- After enumerating actions (Stage 4)
- When figuring out what data the concept needs to maintain

## Process

1. For each action, ask: what state must exist for this action to work?
2. Decompose the state into typed components, one per name. Each component has a name, an Alloy-style type, and a description.
3. Design the state independently of other concepts — it will be merged later (p. 58).
4. Keep the model minimal: only include state that is required by the actions.

## Artifact

```
StateComponent {
  name:        str   // camelCase noun
  type:        str   // Alloy-style notation; see below
  description: str
}
```

State is produced as a list of components: `StateComponent[]`.

## Alloy-style type notation

- `one X` — exactly one X
- `lone X` — zero or one X
- `set X` — unordered set of Xs
- `seq X` — ordered sequence of Xs
- `X -> Y` — total function from X to Y
- `X -> one Y`, `X -> lone Y`, `X -> set Y`, `X -> seq Y` — relations with the named multiplicity on the codomain

Decomposition rules:
- A "set of records, each holding fields F1, F2, …" decomposes into one `set` declaring the records exist, plus one `X -> Y` per field.
- Cross-concept references ("defined by User") become a relation whose codomain is the other concept's primary entity. Note in `description` that the type is owned elsewhere.

## Persistence

Persist on approval: add `state` to the accreting draft `concepts/<name>.json`. This is the last of the five fields; Stage 6 finalizes the file. See the `concept-design` skill's **Persistence protocol**.

## Validation

- Does every action have the state it needs?
- Is there state that no action uses? Remove it.
- Is the state independent enough to be merged with other concepts' state later?
