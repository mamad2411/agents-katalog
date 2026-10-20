---
name: memory-architecture-checklist
description: Treat LLM statelessness as a hard constraint — decide explicitly what state survives a turn, which storage tier holds it, and how it is evicted.
---

# Agent memory architecture checklist

An LLM call is stateless. Nothing carries between turns except what you put back into the context window. Continuity is an engineering decision, not a model feature — and provider-managed memory APIs delegate the storage, not the decision.

## Rules

- For every piece of state, decide explicitly whether it must survive the current turn. If it does not, keep it in-context and let it expire — do not persist it.
- Assign each surviving piece of state to exactly one storage tier:
  - **in-context** — cheap, volatile, lost on compaction or a new session
  - **external store** — database, vector store, or knowledge graph; durable and queryable, and entirely your responsibility to govern
  - **provider-managed memory API** — storage is delegated, but eviction and provenance are still yours to define
- Define an eviction policy for each tier before the first record is written. A store with no documented pruning strategy will grow unbounded.
- Never treat "the model will remember" as a design. It will not. If continuity matters, name the tier that provides it.
- Record the retention reason alongside the data: why this needs to survive, and the condition under which it stops being relevant.

## Decision checklist (per state item)

```text
What is it?            e.g. "user prefers pnpm"
Must survive turn?     no  -> in-context only, expires with session
                       yes -> choose a tier below
Tier?                  in-context | external store | provider-managed
Eviction?              TTL | supersede-on-change | manual review | never*
Provenance?            see memory-provenance
```

`never` is a deliberate choice that must be justified, not a default.

## Examples

```text
// BAD — relying on the model to "remember" without naming a tier
"The user prefers pnpm — the model will just remember that."

// GOOD — explicit tier assignment with eviction policy
What is it?      "user prefers pnpm"
Must survive?    yes (cross-session preference)
Tier?            external store (user profile record)
Eviction?        supersede-on-change (user updates preference)
Provenance?      user-stated, 2026-06-15
```
