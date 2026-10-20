# Working Memory Module

This directory owns the working memory module — a session-scoped, agent-controlled scratchpad whose entries appear in the system prompt every turn.

- Unlike the `memory` module (persistent cross-session notes) and `knowledge` module (structured reference data), working memory is visible without explicit reads and is cleared when the session ends.
- Named entries can be persisted across sessions by marking them persistent; those are saved via `ModuleStorage`.
- `persistence.ts` owns the versioned persistent-entry envelope and one-time
  normalization of validated array storage. Corrupt or unsupported data is an explicit load
  failure; it must not become an empty scratchpad and later overwrite the
  operator's file. `ModuleStorage` supplies atomic replacement, while this
  module owns the schema and decoding policy.
- Live scratchpads belong to the existing session-environment resource owner,
  keyed by session and scope. Prompt and tool access use the same execution
  identity; missing identity or unavailable tool policy must not expose state.
- Persistent mutations merge affected keys into the latest scope file. Session
  teardown discards local state only; it must not delete durable entries.
- Contributes the `working-memory` skill (prompt guidance for managing entries).

## Boundaries

- Owns the session-scoped working-memory store implementation (`store.ts`); the
  module's tool runner and dynamic state provider delegate to it directly.
- Does not own persistent cross-session memory (that belongs in `memory/`) or structured reference entries (that belongs in `knowledge/`).
- Does not own conversation recall (that belongs in `history/`).
