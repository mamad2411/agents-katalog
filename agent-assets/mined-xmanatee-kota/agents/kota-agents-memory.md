# Memory Module

This directory owns persistent, searchable agent notes that survive across sessions.

- Owns the file-based `MemoryStore` implementation (`store.ts`) and registers
  it as the `default` memory provider at module load through the provider
  registry.
- Storage is scope-scoped under `.kota/memory.json`. Daemon/API and local-client
  access use the daemon scope owner's live directory selector. All in-process
  resolvers use one canonical `MemoryStore` per scope root so capture, retract,
  recall, routes, and clients cannot retain
  conflicting snapshots of the same file.
- `persistence.ts` owns the versioned file contract and legacy migration.
  Reads decode every record before it reaches `MemoryStore`; malformed or
  future-version data is an explicit store error and is never treated as an
  empty collection. Replacement writes are atomic. The daemon client parses
  responses with the generated daemon-contract decoder rather than asserting
  a handwritten transport type.
- `operations.ts` is the single orchestration owner for list/search/reindex
  results, including explicit semantic-unavailable and delete not-found
  outcomes. Local clients and HTTP routes call it directly. Routine daemon
  list/add/search/reindex transport is generated; only delete's HTTP 404
  transform remains module-authored.
- Contributes the `memory` tool in the `management` group, the `kota memory …` CLI commands, the `/api/memory` HTTP routes, and the `memory` skill.
- Telegram and terminal search consume the shared HTTP route and line renderer.
  Visual clients render the module's shared-UI contribution instead of owning
  memory-specific screens or routes.
- The `stores` shared-UI surface is the memory module's live contribution;
  knowledge and history add their own independently owned surfaces.

## Boundaries

- Does not own session-scoped working memory (that belongs in `src/modules/working-memory/`) or structured knowledge entries (that belongs in `src/modules/knowledge/`).
- The alternative SQLite-backed memory provider is in `src/modules/sqlite-memory/`, not here.
- The embedding-backed memory provider is in `src/modules/memory-semantic/`, which layers on top of this module's store.
- The base provider is keyword-only. Embedding-backed implementations declare
  `semanticSearchCapability`; absence means unavailable and requires no false
  support flag or placeholder methods.
