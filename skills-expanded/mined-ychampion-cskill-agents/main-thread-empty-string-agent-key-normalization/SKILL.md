---
name: main-thread-empty-string-agent-key-normalization
description: "Normalize the main thread to a concrete empty-string key so agent-scoped state maps treat main and forked threads uniformly."
metadata:
  author: ychampion
---

# SKILL: Main-Thread Empty-String Agent Key Normalization
**Domain:** multi-agent  
**Trigger:** Apply when thread-scoped state is keyed by agent identity, but the main thread has no explicit agent ID and still needs stable map behavior.
**Source Pattern:** Distilled from reviewed multi-agent coordination and child-runtime patterns.

## Core Method
Convert the main thread's missing agent identifier into a concrete sentinel key before interacting with shared maps. Using one normalized value such as `''` lets the main thread participate in the same per-agent state structure as forked agents without special branching at every lookup or write. This keeps map semantics uniform and ensures the main thread's state is stable across reads, inserts, and resume paths.

## Key Rules
- Normalize missing main-thread IDs at the boundary where the key is derived, not later at individual map operations.
- Use one stable sentinel for the main thread so every lookup and write resolves to the same slot.
- Keep forked agents on their real IDs; the sentinel is only for the thread that lacks an explicit identifier.
- Build the rest of the state logic on the normalized key so the map layer does not need separate main-thread code paths.

## Example Application
If an attachment pipeline tracks which announcements each agent has already seen, derive `agentKey` from `agentId ?? ''` before looking up the sent-state map. The main thread then uses the empty-string slot consistently, while spawned agents continue using their concrete IDs.

## Anti-Patterns (What NOT to do)
- Do not let `undefined` flow directly into some map operations and a fallback value into others; that splits one logical thread across multiple keys.
- Do not create separate ad hoc main-thread branches for every state lookup when one normalized sentinel key will unify the behavior.
