---
applyTo: "src/extension.ts,src/config/**,src/services/**,src/types/**"
description: "Extension-level architecture: type system, service initialization, config pattern, OllamaClient API, terminal manager, and model compatibility"
---

# Extension Architecture & Service Patterns

## Type System — Three Message Interfaces

The codebase has **three different interfaces** for messages. Using the wrong one is a common mistake:

| Interface | File | Role | Fields |
|-----------|------|------|--------|
| `MessageRecord` | `src/types/session.ts` | **Database persistence** — the source of truth | `snake_case`: `session_id`, `tool_name`, `tool_input`, `tool_output`, `progress_title` |
| `ChatMessage` | `src/views/chatTypes.ts` | **View layer transfer** — enriched with UI metadata | `camelCase`: `toolName`, `actionText`, `actionIcon`, `actionStatus` |
| Ollama `ChatMessage` | `src/types/ollama.ts` | **API requests/responses** — wire format | `role`, `content`, `tool_calls?`, `tool_name?`, `thinking?` |

**When to use which:**
- Storing to or reading from the database → `MessageRecord`
- Sending to the webview via `postMessage` → `ChatMessage` (constructed by `chatSessionController.ts`)
- Sending to the Ollama API → `ChatMessage` from `src/types/ollama.ts` — includes `role`, `content`, and optionally `tool_calls` (assistant), `tool_name` (tool results), `thinking` (chain-of-thought)

**Gotcha**: `ChatSession` in `chatTypes.ts` is a **legacy type** — the real session record is `SessionRecord` in `types/session.ts`. Do not add new session fields to `ChatSession`.

**Gotcha**: `WebviewMessageEmitter` in `chatTypes.ts` is intentionally `any`-typed (`postMessage(message: any)`). The emitter is injected into `AgentChatExecutor`, `ChatSessionController`, and `SettingsHandler` — all post different message shapes. Do not try to make it generic/typed.

## Service Initialization Order

In `extension.ts → activate()`, a `ServiceContainer` groups all extension-wide service instances. Initialization is split into named helper functions for readability:

```
1. initCoreServices()
   ├─ getConfig()                    ← reads VS Code settings (snapshot)
   ├─ TokenManager(context)          ← creates secure storage accessor
   ├─ OllamaClient(baseUrl, token)   ← HTTP client (no connections yet)
   ├─ ModelManager(client)            ← model listing/caching
   ├─ getDatabaseService(context)     ← singleton accessor
   ├─ databaseService.initialize()    ← SQLite: EAGER (blocks activation)
   │                                    LanceDB: LAZY (background promise, via LanceSearchService)
   └─ Returns ServiceContainer with all services
2. registerFileDecorations()       ← pending edit badge + restore from DB
3. registerReviewService()         ← CodeLens + review navigation commands
4. fireAndForgetConnectionCheck()  ← non-blocking
5. registerStatusBar()             ← model selector status bar item
6. registerCompletionProvider()    ← inline completions (if model configured)
7. registerCommands()              ← selectModel, setBearerToken
8. registerChatView()              ← creates ChatViewProvider (owns ToolRegistry,
                                     TerminalManager, ChatSessionController,
                                     SettingsHandler, AgentChatExecutor internally)
9. registerModes()                 ← plan, agent, edit
10. checkFirstRun()                ← navigate to settings on first activation
```

**Key rule**: SQLite is ready after `initialize()` returns. LanceDB may still be initializing. Any code that needs LanceDB must call `await lanceSearchService.ensureReady()` which awaits the background promise.

## DatabaseService Singleton Pattern

```typescript
// First call — creates the singleton (must have context)
const db = getDatabaseService(context);

// Subsequent calls — returns existing singleton (context optional)
const db = getDatabaseService();

// Cleanup — must call on deactivate
disposeDatabaseService();
```

**Gotcha**: `disposeDatabaseService()` calls `close()` but **does not await it**. The `close()` method is async (awaits `lanceInitPromise`), but the dispose function fires and forgets. If you need clean shutdown (e.g., in tests), await `close()` directly.

**Embedding fallback**: `LanceSearchService.generateEmbedding()` (private) uses a trivial character-hash vector when no embedding model is configured — deterministic but semantically meaningless. Good for dedup, not for semantic search.

## Configuration Pattern — Snapshots, Not Reactive

`getConfig()` in `src/config/settings.ts` reads VS Code configuration **on every call** and returns a fresh `ExtensionConfig` object. It's a snapshot, not a live reference.

```typescript
const config = getConfig();   // reads ALL settings right now
const mode = getModeConfig('agent'); // shortcut for config.agentMode
const agent = getAgentConfig();      // shortcut for config.agent
```

## Build Output Directories

Three output directories exist. **Never edit files in these directories** — they are overwritten on every build.

| Directory | Build Tool | Contains | Source |
|-----------|-----------|----------|--------|
| `dist/` | **Webpack** | Extension bundle (`extension.js`) — this is the runtime entry point (`"main"` in `package.json`) | `src/**` (excluding `src/webview/`) |
| `media/` | **Vite** | Webview bundle (`index.html`, `chatView.js`, `chatView.css`) — loaded by `ChatViewProvider` | `src/webview/**` |
| `out/` | **tsc** (`tsconfig.test.json`) | Compiled test files — used **only** by `@vscode/test-electron` runner | `tests/extension/**` |

**Common mistake**: Editing `media/chatView.js` or `dist/extension.js` directly. These changes are silently lost on the next `npm run compile`.

**Settings scope rule**: Only `baseUrl` respects workspace vs global scope (uses `config.inspect()` to detect existing scope). All other settings are always saved to `ConfigurationTarget.Global`.

## Settings Mapping Asymmetry

The webview uses **camelCase** keys, VS Code configuration uses **dot-separated** keys:

| Webview Payload Key | VS Code Setting Key |
|--------------------|--------------------|
| `agentModel` | `agentMode.model` |
| `askModel` | `askMode.model` |
| `editModel` | `editMode.model` |
| `completionModel` | `completionMode.model` |
| `maxIterations` | `agent.maxIterations` |
| `toolTimeout` | `agent.toolTimeout` |
| `maxActiveSessions` | `agent.maxActiveSessions` |
| `sensitiveFilePatterns` | `agent.sensitiveFilePatterns` |
| `enableAutoComplete` | `enableAutoComplete` |
| `temperature` | `agentMode.temperature` |

Both `getSettingsPayload()` and `saveSettings()` in `settingsHandler.ts` manually map between these. When adding a new setting, **both** functions must be updated.

## OllamaClient API Patterns

### Streaming
Both `chat()` and `generate()` return `AsyncGenerator`. Responses are NDJSON (newline-delimited JSON). The NDJSON parser silently swallows parse errors.

### Error Hierarchy
```
OllamaError           ← base class (has statusCode)
├── ConnectionError   ← network failures (TypeError)
└── AuthError         ← HTTP 401
```

### Retry Policy
- **3 attempts** with exponential backoff (1s, 2s, 4s)
- **Auth errors (401) are never retried** — thrown immediately
- Only server errors (5xx) and connection failures trigger retry

### Base URL
Trailing slash is always stripped (both in constructor and `setBaseUrl()`).

### `testConnection()`
Returns `boolean`, not the error — swallows exceptions. The `SettingsHandler.testConnection()` wrapper sends results to the UI via `connectionTestResult` message.

## Terminal Manager (`src/services/terminalManager.ts`)

### Shell Integration Requirement
**Requires VS Code Terminal Shell Integration** (VS Code 1.93+, `vscode.env.shell`). On initialization, waits up to 5 seconds for shell integration to appear. If unavailable, throws a hard error. This drives the `engines.vscode: ^1.93.0` requirement in `package.json`.

### Session-Keyed Terminals
Terminals are **keyed by session ID**, not by command or CWD. One terminal per agent session, reused across commands. Terminals are auto-cleaned when VS Code closes them (via `onDidCloseTerminal` listener).

### Output Truncation
Output is hard-truncated to **100 lines** (15 head + 85 tail) with a `[N lines truncated]` marker. ANSI escape sequences and VS Code's `]633;` shell integration markers are stripped.

### Execution Caveat
`waitForCommandEnd()` relies on the `onDidEndTerminalShellExecution` event. If the event never fires (e.g., shell integration bug), the promise **never resolves**. There is no timeout.

## Model Compatibility (`src/services/model/modelCompatibility.ts`)

Reads **model capabilities from the Ollama `/api/show` endpoint** which returns a `capabilities` string array (e.g. `["completion", "vision", "tools", "insert"]`). The module maps those API strings to the UI-facing `ModelCapabilities` type:

| API value | `ModelCapabilities` field |
|-----------|--------------------------|
| `completion` | `chat` |
| `insert` | `fim` |
| `tools` | `tools` |
| `vision` | `vision` |
| `embedding` | `embedding` |

No regex arrays or name-based heuristics are used. Capabilities are populated by `OllamaClient.fetchModelsWithCapabilities()`, which calls `listModels()` then `showModel()` in parallel for all models, merging the `capabilities` array into each `Model` object.

### SQLite Model Cache

The model list (name, size, family, quantization, capabilities, `enabled` flag) is persisted in the SQLite `models` table. Key behaviors:

- **Offline fallback**: When Ollama is unreachable, the extension reads the last cached model list so dropdowns and the capabilities table remain populated.
- **Stale cleanup**: `upsertModels()` does `DELETE FROM models` then re-inserts all models from the latest Ollama response. Models removed from Ollama are automatically dropped.
- **Enable/disable**: Each model has an `enabled INTEGER NOT NULL DEFAULT 1` column. Disabled models are filtered out of `modelOptions` in the webview. Bulk "Enable All" / "Disable All" toggles loop through `modelInfo` and call `toggleModelEnabled()` for each.
- **Auto-save**: The Model Selection dropdowns (`ModelCapabilitiesSection.vue`) auto-save on change via `@change="autoSave"` — no explicit Save button.

## File Sensitivity (`src/utils/fileSensitivity.ts`)

### Pattern Evaluation: Last-Match-Wins
`evaluateFileSensitivity()` iterates the `sensitiveFilePatterns` object **in insertion order**. The **last matching pattern wins**:
```json
{ "**/*": true, "**/.env*": false }
```
- `**/*` matches everything → `true` (auto-approve)
- `**/.env*` matches `.env` → `false` (require approval) ← wins because it's last

**Value semantics**: `true` = auto-approve (NOT sensitive), `false` = require approval (sensitive). The boolean is inverted from what the key name "sensitive" suggests.

### Session-Level Overrides
Each session can have its own `sensitive_file_patterns` (stored as JSON string in the `sensitive_file_patterns` SQLite column). Session patterns take precedence over the global `agent.sensitiveFilePatterns` setting.

## Auto-Approve: Two Independent Toggles

| Toggle | DB Column | Controls |
|--------|-----------|----------|
| `auto_approve_commands` | `auto_approve_commands` | Terminal command execution |
| `auto_approve_sensitive_edits` | `auto_approve_sensitive_edits` | File edits to sensitive files |

These are stored per-session and toggled independently. **Critical severity commands always require approval** regardless of `auto_approve_commands` — this is enforced in `terminalApproval.ts`.

## Deactivation

`deactivate()` in `extension.ts`:
1. Resets all `generating` sessions to `idle` (so they don't appear stuck on reload)
2. Disposes `OllamaClient` (cancels pending HTTP)
3. Clears `ModelManager` cache
4. Calls `disposeDatabaseService()` (fire-and-forget, not awaited)

## PendingEditReviewService (`src/services/review/pendingEditReviewService.ts`)

Provides inline change review after the agent edits files — green/red line decorations, per-hunk CodeLens actions (Keep / Undo / ↑ / ↓), and cross-file hunk navigation.

The service is decomposed into focused sub-classes:

| File | Responsibility |
|------|----------------|
| `pendingEditReviewService.ts` | **Thin facade** — owns session state, events, lifecycle, and hunk keep/undo operations. Delegates to sub-classes below. |
| `reviewSessionBuilder.ts` | Constructs `ReviewSession` from DB checkpoint snapshots + `computeHunks()` diff logic |
| `reviewNavigator.ts` | Pure stateless navigation math — file/hunk/change traversal, position calculations |
| `reviewDecorationManager.ts` | VS Code editor decorations — gutter arrow, added/deleted highlights, file opening |
| `reviewCodeLensProvider.ts` | CodeLens provider for Keep/Undo hunk actions |
| `reviewTypes.ts` | Shared type definitions (`ReviewHunk`, `FileReviewState`, `ReviewSession`, events) |

### Lifecycle

```
Agent writes files → agentChatExecutor creates checkpoint + file snapshots
  → execute() returns { checkpointId } to handleAgentMode()
  → handleAgentMode() calls reviewService.startReviewForCheckpoint(checkpointId)
      → buildReviewSession([checkpointId])
          ├─ Sorts checkpoint IDs chronologically (oldest first)
          ├─ Reads file_snapshots from DB for each sorted checkpoint
          ├─ Filters to pending files only, deduplicates by path
          ├─ Diffs original_content vs current on-disk content (structuredPatch)
          ├─ Creates per-file decoration types + ReviewHunk[] arrays
          └─ Registers CodeLens provider (scheme: 'file')
      → Applies decorations to all visible editors that match reviewed files
      → Returns { current, total, filePath } change position
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **ReviewSession** | One active session at a time, tied to `checkpointIds: string[]` (multiple checkpoints across agent iterations). Contains array of `FileReviewState` and `currentFileIndex`. |
| **FileReviewState** | Per-file: URI, filePath, hunks[], decoration types, current hunk index |
| **ReviewHunk** | Contiguous diff region: `startLine`, `endLine`, `addedLines[]`, `deletedCount`, `originalText`, `newText` |
| **Auto-start** | `startReviewForCheckpoint()` is called automatically when agent finishes — decorations appear on already-open files without user action |
| **Manual start** | User clicks the review icon on a file in the widget → `openFileReview()` → opens file + applies decorations |
| **Hunk resolution** | `keepHunk()` removes the hunk from tracking. `undoHunk()` reverts the text via `editor.edit()`, then removes + shifts subsequent hunks by line delta. |
| **Change position** | `getGlobalChangePosition()` returns `{ current, total, filePath? }` — the current hunk index across ALL files (not per-file). The widget shows "Change X of Y" from this. |

### Multi-Checkpoint Support

When the agent runs multiple iterations (each creating a checkpoint), the review session accumulates ALL checkpoint IDs:

- `AssistantThreadFilesChangedBlock.checkpointIds: string[]` holds all checkpoints belonging to a widget
- `startReviewForCheckpoint()` merges new checkpoint IDs with existing ones: `[...new Set([...existing, ...new])]`
- `buildReviewSession()` sorts IDs chronologically before iterating (checkpoint IDs are `ckpt_<timestamp>_<random>`, so string sort = chronological order). This ensures file order in the review session matches the widget display.

### Concurrency: AsyncMutex (`src/utils/asyncMutex.ts`)

Multiple `requestFilesDiffStats` messages can arrive concurrently (one per checkpoint in the widget). Without synchronization, two concurrent `startReviewForCheckpoint` calls would race — each calling `closeReview()` (nulling `activeSession`), so the second call couldn't see the first's session to merge IDs.

**Solution**: A reusable `AsyncMutex` serializes all session-building operations:

```typescript
import { AsyncMutex } from '../../utils/asyncMutex';

private readonly mutex = new AsyncMutex();

await this.mutex.runExclusive(async () => {
  // Only one build runs at a time
});
```

Wrapped operations: `startReviewForCheckpoint`, `navigateChange` (only when rebuilding), `openFileReview`.

### Navigation Behavior

`navigateChange(direction, checkpointIds?)` handles forward/backward hunk traversal:

- **Does NOT rebuild on every call** — that would destroy the current navigation position (currentFileIndex, currentHunkIndex)
- **Only rebuilds when**: no active session exists, OR the active session is missing some requested checkpoint IDs
- When it does rebuild, it uses the `AsyncMutex` to serialize with other builds
- Navigation math is delegated to the stateless `ReviewNavigator` class — it computes target indices, the facade applies side effects (opening files, scrolling)
- Returns `{ current, total, filePath? }` for the widget's "Change X of Y" counter

### Widget ↔ Review Service Coupling

The files-changed widget and the review service both track file change state independently. They sync via events:

| Direction | Mechanism | When |
|-----------|-----------|------|
| Widget → Review | `fileChangeMessageHandler.handleKeepFile()` calls `reviewService.removeFileFromReview(filePath)` | User clicks Keep/Undo in widget |
| Widget → Review | `fileChangeMessageHandler.handleKeepAllChanges()` calls `reviewService.closeReview()` | User clicks Keep All / Undo All |
| Widget → Review | `fileChangeMessageHandler.handleRequestFilesDiffStats()` calls `reviewService.startReviewForCheckpoint()` | Widget requests diff stats — also builds/merges review session |
| Widget → Review | `reviewNavMessageHandler` calls `reviewService.navigateChange()` | User clicks prev/next in nav bar |
| Widget → Review | `fileChangeMessageHandler` calls `reviewService.openFileReview()` | User clicks review icon on a file row |
| Review → Widget | `onDidResolveFile` event → chatView persists + posts `fileChangeResult` | All hunks in a file resolved via CodeLens |
| Review → Widget | `onDidUpdateHunkStats` event → chatView posts `filesDiffStats` | Any hunk keep/undo changes +/- counts |
| Review → Widget | `reviewChangePosition` message posted after nav/open/stats | Updates "Change X of Y" counter + `activeFilePath` in widget |
| Review → Widget | `fileChangeMessageHandler.sendReviewPosition()` posts `reviewChangePosition` | After keep/undo single file — ensures counter reflects reduced hunk count |
| Agent → Review → Widget | `chatMessageHandler.onFileWritten` callback → `startReviewForCheckpoint` → `reviewChangePosition` | Each file written during agent loop updates counter + active file |

### Visible Editor Tracking in `startReviewForCheckpoint`

After rebuilding the review session, `startReviewForCheckpoint` iterates `vscode.window.visibleTextEditors` to find editors that match reviewed files:

1. Applies decorations to all matching visible editors
2. Sets `currentFileIndex` to the **focused** (`activeTextEditor`) editor if it matches a review file
3. Falls back to any visible editor that matches
4. This ensures `getChangePosition()` returns the correct `filePath` for the widget's active file indicator

This prevents the active file highlight from jumping to index 0 when the review session is rebuilt (e.g., when the agent writes a new file while the user is viewing a different one).

### Per-File Review Callback (`onFileWritten`)

During agent execution, `chatMessageHandler.ts` registers a per-write callback:

```typescript
this.agentExecutor.onFileWritten = (checkpointId: string) => {
  reviewSvc.startReviewForCheckpoint(checkpointId).then(() => {
    const pos = reviewSvc.getChangePosition(checkpointId);
    if (pos) {
      emitter.postMessage({ type: 'reviewChangePosition', checkpointId, ... });
    }
  });
};
```

This ensures:
- CodeLens decorations appear as each file is written (not just at the end)
- The widget's "Change X of Y" counter and `activeFilePath` stay current during multi-file agent iterations
- The callback is cleared (`onFileWritten = undefined`) after execution completes

### Session Stats Refresh After Keep/Undo

All four keep/undo handlers in `fileChangeMessageHandler.ts` (`handleKeepFile`, `handleUndoFile`, `handleKeepAllChanges`, `handleUndoAllChanges`) call `await this.sessionController.sendSessionsList()` after resolving the operation. This refreshes the sessions panel's `+N -N` badge so it reflects the updated pending file stats.

### ⚠️ sessionId Resolution in File Change Handlers

The webview's `keepFile`, `undoFile`, `keepAllChanges`, `undoAllChanges` actions do **not** include `sessionId` in the `postMessage`. The backend handlers in `fileChangeMessageHandler.ts` must resolve it:

```typescript
private async handleUndoAllChanges(checkpointId: string, sessionId?: string) {
  const resolvedSessionId = sessionId || this.sessionController.getCurrentSessionId();
  // ... use resolvedSessionId for persistUiEvent
}
```

Without this, `persistUiEvent()` silently drops the event (`if (!sessionId) return`), and session history will be missing the keep/undo result — the widget reappears on reload.

## Checkpoint & Snapshot Architecture

### Data Model

Checkpoints and file snapshots are stored in SQLite (not LanceDB):

**`checkpoints` table:**
| Column | Type | Purpose |
|--------|------|---------|
| `id` | `TEXT PRIMARY KEY` | UUID (`ckpt_<timestamp>_<random>`), created at start of each agent execution |
| `session_id` | `TEXT NOT NULL` | FK → sessions |
| `message_id` | `TEXT` | Associated message (nullable) |
| `status` | `TEXT` | `'pending'` → `'kept'` / `'undone'` / `'partial'` |
| `total_additions` | `INTEGER` | Cached total added lines across all files (migration-added) |
| `total_deletions` | `INTEGER` | Cached total deleted lines across all files (migration-added) |
| `created_at` | `INTEGER` | Timestamp |

**`file_snapshots` table:**
| Column | Type | Purpose |
|--------|------|---------|
| `id` | `TEXT PRIMARY KEY` | UUID |
| `checkpoint_id` | `TEXT NOT NULL` | FK → checkpoints (CASCADE delete) |
| `file_path` | `TEXT NOT NULL` | Workspace-relative path |
| `original_content` | `TEXT` | Content BEFORE agent edit (NULL after kept+pruned) |
| `action` | `TEXT` | `'modified'` / `'created'` |
| `file_status` | `TEXT` | `'pending'` / `'kept'` / `'undone'` |
| `created_at` | `INTEGER` | Timestamp |
| `additions` | `INTEGER` | Per-file added line count (migration-added, NULL until stats computed) |
| `deletions` | `INTEGER` | Per-file deleted line count (migration-added, NULL until stats computed) |
| **UNIQUE** | | `(checkpoint_id, file_path)` — INSERT OR IGNORE keeps first snapshot |

### Session Stats (`getSessionsPendingStats`)

The sessions panel shows `+N -N` badges per session. `getSessionsPendingStats()` computes these via a **two-level aggregation query**:

1. **Inner query** (per-checkpoint): For each checkpoint with pending files, sums `file_snapshots.additions`/`deletions`. If any files have non-NULL stats, uses those; otherwise falls back to `checkpoints.total_additions`/`total_deletions`.
2. **Outer query** (per-session): Sums the per-checkpoint totals across all checkpoints in a session.

This two-level approach handles the case where some checkpoints have per-file stats and others only have checkpoint-level totals.

### Checkpoint Lifecycle

```
1. Agent loop starts → createCheckpoint(sessionId) → returns checkpointId
2. Before each write_file/create_file → snapshotFileBeforeEdit()
   └─ INSERT OR IGNORE (only first snapshot per file per checkpoint is kept)
3. Agent loop ends → filesChanged payload with checkpointId sent to webview
4. User actions:
   ├─ Keep file → updateFileSnapshotStatus('kept') + pruneCheckpointContent()
   ├─ Undo file → revert file on disk + updateFileSnapshotStatus('undone')
   ├─ Keep All → mark all 'kept' + prune
   └─ Undo All → revert all + mark 'undone'
5. All resolved → updateCheckpointStatus('kept'/'undone'/'partial')
```

### Snapshot Content Pruning

After a file is **kept**, its `original_content` is set to `NULL` via `pruneCheckpointContent()`. This saves storage since the original is no longer needed for undo. Undone files retain `original_content` for debugging.

### Diff Stats Flow — `computeFilesDiffStats` & the filesChanged Widget

Diff stats (`+N -N` per file) flow through several paths depending on context. Understanding **when** stats are computed and **how** they reach the UI prevents long debugging sessions.

#### 1. Live Agent Flow (first computation)

```
Agent loop ends → agentSummaryBuilder.finalize()
  ├─ persistUiEvent(sessionId, 'filesChanged', {checkpointId, files, status:'pending'})
  └─ emitter.postMessage({type:'filesChanged', checkpointId, files, status:'pending', sessionId})
      → webview handleFilesChanged() creates standalone block in filesChangedBlocks
      → webview posts {type:'requestFilesDiffStats', checkpointId}
          → FileChangeMessageHandler.handleRequestFilesDiffStats()
              ├─ checkpointManager.computeFilesDiffStats(checkpointId)
              │   ├─ Reads file_snapshots from DB (original_content)
              │   ├─ Reads current file from disk
              │   ├─ structuredPatch() → counts +/- per file
              │   ├─ updateFileSnapshotsDiffStats() → saves per-file stats to DB
              │   └─ updateCheckpointDiffStats() → caches totals on checkpoint row
              ├─ emitter.postMessage({type:'filesDiffStats', checkpointId, files})
              └─ reviewService.startReviewForCheckpoint() → builds review session
```

#### 2. Session Restore (from history)

```
User clicks session in list → chatSessionController.loadSession()
  ├─ postMessage({type:'loadSessionMessages', messages})
  │   → webview handleLoadSessionMessages()
  │       ├─ buildTimelineFromMessages(messages)
  │       │   └─ TimelineBuilder processes __ui__ tool messages:
  │       │       handleFilesChanged(payload) → pushes to restoredFcBlocks
  │       │       build() → sets filesChangedBlocks.value = restoredFcBlocks
  │       └─ For each block with statsLoading && checkpointIds.length:
  │           vscode.postMessage({type:'requestFilesDiffStats', checkpointId})
  │           → same backend path as live flow (step 1 above)
  ├─ ensureFilesChangedWidget(sessionId, messages)  ← FALLBACK
  │   (only fires if NO __ui__ filesChanged event in messages)
  │   ├─ Queries getCheckpoints(sessionId) for pending/partial
  │   ├─ Queries getFileSnapshots(ckptId) for pending files
  │   └─ Posts synthetic {type:'filesChanged'} per checkpoint
  │       → webview live handleFilesChanged() creates block + requests stats
  └─ postMessage({type:'generationStopped'})
```

**Why the fallback?** Old sessions (created before `filesChanged` persistence was implemented), or sessions where `sessionId` was `undefined` at `persistUiEvent` time (Pitfall #13), have no `__ui__` filesChanged event in the DB. Without the fallback, the widget silently doesn't appear even though the checkpoint data exists.

#### 3. Review CodeLens Keep/Undo (recomputation)

```
User clicks Keep/Undo via CodeLens on a hunk
  → reviewService resolves hunk → emits onDidResolveFile
  → chatView.ts subscriber posts fileChangeResult + calls:
      computeFilesDiffStats(checkpointId) → recalculates all files
      → posts filesDiffStats to webview → widget updates +/- counts
```

#### 4. Hunk-Level Stats Update (real-time)

```
Any hunk keep/undo → reviewService emits onDidUpdateHunkStats
  → chatView.ts subscriber posts {type:'filesDiffStats', checkpointId, files:[{path, additions, deletions}]}
  → webview handleFilesDiffStats() updates single file in block
```

#### 5. Session List Badge Refresh

```
sendSessionsList()
  ├─ databaseService.listSessions()
  └─ databaseService.getSessionsPendingStats()  ← SQL query over checkpoints + file_snapshots
      → returns Map<sessionId, {additions, deletions, fileCount}>
      → merged into session list payload → webview shows +N -N badge
```

**Refresh triggers** — all call `sendSessionsList()`:
- Agent/chat execution completes (`chatMessageHandler.ts` finally block)
- Keep/Undo file (`fileChangeMessageHandler.ts`)
- Keep All / Undo All (`fileChangeMessageHandler.ts`)
- Session delete, new session create
- First message in new session (title update)
