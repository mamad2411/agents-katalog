# History Module

This directory owns conversation history — the persistent record of past sessions across KOTA.

- Owns the file-based `ConversationHistory` store (`history.ts`, `history-utils.ts`) and the scope-scoped store resolver.
- Registers itself as the history provider during `onLoad` via the typed `HISTORY_PROVIDER_TOKEN` (re-exported from `#core/modules/provider-registry.js`) and exposes scope-scoped lookup through `HISTORY_SCOPE_PROVIDER_TOKEN`. Core resolves stores through provider seams; there is no ambient global-history singleton or production reset hook.
- Storage is scope-scoped under `.kota/history`. Daemon/API and local-client
  access use the daemon scope owner's live directory selector.
- Protocol payload types (`ConversationData`, `ConversationRecord`, `ConversationMessage`) live in `#core/modules/provider-types.js`. This module re-exports them from `history-utils.ts` for module-internal convenience only.
- Registers `conversation_recall` in the `management` tool group and contributes the `history` skill (prompt guidance for when and how to use recall).
- Owns the `history` CLI commands (`kota history …`) in `cli-commands.ts` and CLI helpers (interactive REPL, pipe mode, option parsing) in `cli.ts`.
- Owns the `/api/history` HTTP routes (kota serve) and the `/history`,
  `/history/:id` daemon-control routes contributed via
  `KotaModule.controlRoutes`. The two GETs run under capability scope `read`;
  the DELETE under `control`. Detail reads share the `history-detail.ts`
  helper and return an explicit metadata, bounded-window, or full-state
  view; malformed detail query parameters fail at the route/client boundary.
- `operations.ts` owns list/show/delete/search/reindex orchestration and its
  not-found and semantic-unavailable result arms. Local clients and routes
  call it directly. Routine daemon list/discovery/search/reindex transport is
  generated; show/delete retain only genuine detail-query and HTTP 404
  transforms.
- Telegram and terminal search consume the shared HTTP route and line renderer.
  Visual clients render the module's shared-UI contribution instead of owning
  history-specific screens or routes.
- The module contributes its own live history-store shared-UI surface rather
  than entering a daemon-owned store catalog.

## Boundaries

- Does not own the memory or knowledge stores (those belong in `memory/` and `knowledge/`).
- The embedding-backed history provider is in `src/modules/history-semantic/`,
  which layers on top of this module's store. Modules that consume the history
  store at runtime (currently `history-semantic`) must list `history` in their
  KotaModule `dependencies` so the loader orders onLoad correctly.
- The base provider is keyword-only. Embedding-backed implementations declare
  `semanticSearchCapability`; callers never infer support from implementation
  identity or require placeholder semantic methods.
- CLI-launched sessions use configured autonomy explicitly. Missing session-autonomy config is a boundary error, not a hidden fallback.
- Core must not import from `#modules/history/*`; depend on the neutral provider
  protocol and let this module register its implementation.
- Generated history entries retain their originating continuity owner across
  saves. Resume selects that owner so newer checkpoints and explicit resets
  remain authoritative; only legacy entries without a binding seed a lineage.

Native-stop recovery is explicitly host-local and requires the canonical scope,
exact fenced execution, operator stop confirmation and retained evidence. It
uses core conversation locks; it does not reset identities or delete transcripts.
