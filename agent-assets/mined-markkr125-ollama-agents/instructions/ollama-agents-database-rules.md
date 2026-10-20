---
applyTo: "src/services/database/**,src/views/settingsHandler.ts"
description: "Critical rules for the dual-database architecture (SQLite + LanceDB)"
---

# Database Architecture & Critical Rules

## Dual-Database Design

This extension uses **two separate databases**:

| Database | Technology | Purpose | Location |
|----------|------------|---------|----------|
| Sessions | SQLite (sql.js) | Session metadata (id, title, mode, model, timestamps) | `sessions.sqlite` |
| Messages | LanceDB | Message content + vector embeddings for semantic search | `ollama-copilot.lance/` |

**Critical**: Sessions and messages are stored separately. Any operation that clears one MUST clear the other to maintain consistency.

### SQLite `models` Table

The `models` table caches model metadata fetched from Ollama for offline fallback and capability display:

| Column | Type | Purpose |
|--------|------|----------|
| `name` | `TEXT PRIMARY KEY` | Model name (e.g. `qwen2.5-coder:7b`) |
| `size` | `INTEGER` | Model file size in bytes |
| `modified_at` | `TEXT` | Last modified timestamp from Ollama |
| `digest` | `TEXT` | Model digest hash |
| `family` | `TEXT` | Model family |
| `families` | `TEXT` | All families (JSON array string) |
| `parameter_size` | `TEXT` | Human-readable param count |
| `quantization_level` | `TEXT` | Quantization level (e.g. `Q4_K_M`) |
| `capabilities` | `TEXT` | JSON array of capability strings from `/api/show` |
| `enabled` | `INTEGER NOT NULL DEFAULT 1` | 1 = visible in dropdowns, 0 = hidden |
| `fetched_at` | `TEXT` | When this row was last refreshed |

`upsertModels()` replaces the entire table (`DELETE FROM models` + batch `INSERT`) on each refresh, so stale models are automatically removed.

### SQLite `checkpoints` Table

Tracks file-change groups created per agent execution (one checkpoint per user prompt):

| Column | Type | Purpose |
|--------|------|---------|
| `id` | `TEXT PRIMARY KEY` | UUID (`ckpt_<timestamp>_<random>`), created at start of each agent execution |
| `session_id` | `TEXT NOT NULL` | FK → sessions (CASCADE delete) |
| `message_id` | `TEXT` | Associated message (nullable) |
| `status` | `TEXT NOT NULL DEFAULT 'pending'` | `'pending'` → `'kept'` / `'undone'` / `'partial'` |
| `total_additions` | `INTEGER DEFAULT NULL` | Cached total added lines across all files (migration-added) |
| `total_deletions` | `INTEGER DEFAULT NULL` | Cached total deleted lines across all files (migration-added) |
| `created_at` | `INTEGER NOT NULL` | Timestamp |

### SQLite `file_snapshots` Table

Stores original file content captured BEFORE agent edits, enabling undo:

| Column | Type | Purpose |
|--------|------|---------|
| `id` | `TEXT PRIMARY KEY` | UUID |
| `checkpoint_id` | `TEXT NOT NULL` | FK → checkpoints (CASCADE delete) |
| `file_path` | `TEXT NOT NULL` | Workspace-relative path |
| `original_content` | `TEXT` | Content before edit (NULL after kept+pruned) |
| `action` | `TEXT NOT NULL DEFAULT 'modified'` | `'modified'` / `'created'` |
| `file_status` | `TEXT NOT NULL DEFAULT 'pending'` | `'pending'` / `'kept'` / `'undone'` |
| `additions` | `INTEGER DEFAULT NULL` | Per-file added line count (migration-added, NULL until stats computed) |
| `deletions` | `INTEGER DEFAULT NULL` | Per-file deleted line count (migration-added, NULL until stats computed) |
| `created_at` | `INTEGER NOT NULL` | Timestamp |
| **UNIQUE** | | `(checkpoint_id, file_path)` — INSERT OR IGNORE keeps only first snapshot |

**Snapshot lifecycle**:
1. `snapshotFileBeforeEdit()` uses INSERT OR IGNORE — only the first (true original) snapshot per file per checkpoint is stored
2. `updateFileSnapshotStatus()` flips `file_status` to `'kept'` or `'undone'`
3. `pruneCheckpointContent()` NULLs out `original_content` for kept files (saves storage)
4. Review service reads `file_snapshots` with `file_status = 'pending'` to build decorations
5. `updateFileDiffStats()` batch-updates `additions`/`deletions` on `file_snapshots` for a checkpoint
6. `updateCheckpointDiffStats()` caches `total_additions`/`total_deletions` on `checkpoints`

### Session Stats (`getSessionsPendingStats`)

The sessions panel shows `+N -N` badges per session. This is computed by `getSessionsPendingStats()` via a **two-level aggregation query**:

1. **Inner query** (per-checkpoint): For each checkpoint with pending files, sums `file_snapshots.additions`/`deletions`. If any files have non-NULL per-file stats, uses those sums; otherwise falls back to `checkpoints.total_additions`/`total_deletions`.
2. **Outer query** (per-session): Sums the per-checkpoint totals + file counts across all checkpoints in a session.

This two-level approach handles the transition period where some checkpoints have per-file stats and others only have checkpoint-level fallback totals. The `+0 -0` badge is hidden on the frontend via `v-if="(pendingAdditions ?? 0) > 0 || (pendingDeletions ?? 0) > 0"`.

**Refresh triggers** — all of these call `sendSessionsList()` → `getSessionsPendingStats()`:
- Agent/chat execution completes (`chatMessageHandler.ts` finally block)
- Keep/Undo file (`fileChangeMessageHandler.ts`)
- Keep All / Undo All (`fileChangeMessageHandler.ts`)
- Session delete, new session create
- First message in new session (title update)

See the full diff stats flow diagram in `extension-architecture.instructions.md` → "Diff Stats Flow".

## ⚠️ NEVER Auto-Delete User Data

**DO NOT** implement automatic deletion or recreation of the messages table. This includes:

- ❌ Auto-recreating tables on schema mismatch errors
- ❌ Auto-dropping tables on corruption detection
- ❌ Silent data deletion to "recover" from errors

**Why**: Automatic deletion destroys user chat history without consent. Users lose valuable conversation context and have no way to recover it.

**Instead**: Provide manual controls in Advanced Settings for destructive operations, with clear warnings via VS Code's native modal dialogs.

## Schema Mismatch Handling

LanceDB can throw errors like `Found field not in schema: <field_name>` when the table schema changes between versions.

**Correct approach**:
1. Log the error for debugging
2. Do NOT automatically recreate the table
3. Let the user manually trigger "Recreate Messages Table" from Advanced Settings if they choose to lose their data

## LanceDB Corruption Patterns

LanceDB stores data in `.lance` directories with metadata files referencing data files. Corruption can occur when:
- Data files are deleted but metadata still references them
- Extension crashes mid-write
- Filesystem issues

**Error signature**: `Not found: .../ollama-copilot.lance/messages.lance/data/<uuid>.lance`

**Handling**: LanceDB corruption is detected during `initLanceDb()` in `src/services/database/lanceSearchService.ts`. If initialization fails, search is disabled but the extension continues to function. Users can manually trigger "Recreate Messages Table" from Advanced Settings (`src/views/settingsHandler.ts` → `recreateMessagesTable()`) to clear and rebuild the table.

## LanceSearchService API (`src/services/database/lanceSearchService.ts`)

`LanceSearchService` owns all LanceDB interactions. `DatabaseService` delegates to it for message indexing and search.

| Method | Visibility | Purpose |
|--------|------------|---------|
| `startInit()` | public | Kicks off background LanceDB init (table open/create). Called once from `DatabaseService.initialize()`. |
| `ensureReady()` | public | Awaits `lanceInitPromise`. Returns `true` if table is usable. |
| `indexMessage(msg)` | public | Inserts a `MessageRecord` into LanceDB (with embedding + snippet). |
| `searchByKeyword(query, limit)` | public | FTS keyword search on content field. |
| `searchSemantic(query, limit)` | public | Vector cosine-similarity search using `generateEmbedding()`. |
| `searchHybrid(query, limit)` | public | Runs keyword + semantic in parallel, combines via RRF reranking. |
| `deleteSessionEntries(id)` | public | Deletes all LanceDB rows for a session. |
| `recreateSearchTable()` | public | Drops + recreates the messages table (manual "Recreate Messages Table"). |
| `close()` | public | Awaits background init, then nulls state. See "DatabaseService.close()" below. |
| `generateEmbedding(text)` | **private** | Trivial character-hash vector (deterministic, not semantic). |

## Message Ordering

Messages must have strictly increasing timestamps to ensure correct display order. The `getNextTimestamp(sessionId)` function in `src/services/database/sessionIndexService.ts` guarantees this by:
1. On first call for a session (or when switching sessions), querying the database for the max timestamp in that session
2. Caching the `lastTimestamp` and `lastTimestampSessionId` to avoid repeated DB queries
3. Returning `max(Date.now(), lastTimestamp + 1)` for each subsequent message

**Critical**: The timestamp must be fetched from the database on extension restart or session switch, because the in-memory `lastTimestamp` resets to 0. Without this, new messages could get timestamps lower than existing messages, causing them to appear out of order.

## Agent Message Persistence Order

During agent execution, messages must be saved to the database in the exact order they appear in real-time:
1. **User message** - saved immediately when received
2. **Assistant explanation** - saved BEFORE tool execution (if the LLM provides explanation text before calling tools)
3. **Tool messages** - saved as each tool completes
4. **Final summary** - saved after all tools complete

**Why this matters**: If assistant explanations are only saved at the end (after tools), they get timestamps later than the tools, causing incorrect display order when loading from history.

## DatabaseService.close() and LanceDB Background Init

**Critical**: `LanceSearchService.close()` must await the background `lanceInitPromise` before nulling out state. Without this, closing while LanceDB is still initializing in the background can leave corrupt/partial files that cause subsequent instances to fail.

```typescript
if (this.lanceInitPromise) {
  await this.lanceInitPromise.catch(() => { /* already logged */ });
  this.lanceInitPromise = null;
}
```

This prevents race conditions in tests where multiple instances share the same storage directory.

## Clearing All Data

When implementing "clear all data" functionality:
1. Drop/recreate LanceDB messages table via `DatabaseService.recreateMessagesTable()`
2. Clear SQLite sessions via `SessionIndexService.clearAllSessions()`
3. **Refresh the sessions list in the UI** by sending `loadSessions` with an empty array:
   ```typescript
   this.emitter.postMessage({
     type: 'loadSessions',
     sessions: [],
     hasMore: false,
     nextOffset: null
   });
   ```

All three steps are required - clearing databases without refreshing the UI leaves stale sessions visible.

## Webview Dialog Restrictions

Webviews run in a sandboxed iframe without `allow-modals`. This means:
- ❌ `confirm()` throws: "The document is sandboxed, and the 'allow-modals' keyword is not set"
- ❌ `alert()` and `prompt()` also fail

**Solution**: For confirmation dialogs, send a message to the extension backend and use VS Code's native `vscode.window.showWarningMessage()` with `{ modal: true }`:

```typescript
const result = await vscode.window.showWarningMessage(
  'This will delete all chat history. Continue?',
  { modal: true },
  'Delete'
);
if (result === 'Delete') {
  // proceed with deletion
}
```

## Session Storage Overview

- **Storage scope**: Data is stored per-workspace using `ExtensionContext.storageUri` with a fallback to `globalStorageUri` when no workspace is open.
- **Session index**: `SessionIndexService` (sql.js, offset pagination, sorted by `updated_at DESC`).
- **Messages**: LanceDB `messages` table only (no `sessions` table). Legacy LanceDB sessions are migrated to SQLite on startup.
- **Deletion**: `deleteSession()` removes from SQLite and deletes messages in LanceDB.

## Pagination

Session list uses offset-based pagination:

- Backend returns `{ hasMore, nextOffset }`.
- Webview requests `loadMoreSessions` with `{ offset }`.
