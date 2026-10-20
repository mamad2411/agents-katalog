---
applyTo: "src/views/**,src/webview/**"
description: "Backend-to-frontend and frontend-to-backend message protocol for the chat webview"
---

# UI Component Communication

## Backend → Frontend Messages

| Message Type | Payload | Purpose |
|--------------|---------|---------|
| `init` | `{models, currentMode, settings, hasToken}` | Initialize UI with settings and model list |
| `settingsUpdate` | `{settings, hasToken}` | Push updated settings to webview |
| `showThinking` | `{message, sessionId}` | Show loading state for a session |
| `hideThinking` | `{sessionId}` | Hide loading state for a session |
| `startProgressGroup` | `{title, sessionId}` | Start collapsible group |
| `showToolAction` | `{status, icon, text, detail, filePath?, checkpointId?, startLine?, sessionId}` | Add/update action in group |
| `finishProgressGroup` | `{sessionId}` | Mark group complete |
| `requestToolApproval` | `{id, command, cwd, severity, reason, sessionId}` | Show terminal command approval card |
| `toolApprovalResult` | `{approvalId, status, output, command?, autoApproved?, sessionId}` | Update terminal command approval status |
| `requestFileEditApproval` | `{id, filePath, severity, reason, diffHtml, sessionId}` | Show file edit approval card with diff |
| `fileEditApprovalResult` | `{approvalId, status, autoApproved?, filePath, sessionId}` | Update file edit approval status |
| `sessionApprovalSettings` | `{sessionId, autoApproveCommands?, autoApproveSensitiveEdits?, sessionSensitiveFilePatterns?}` | Push per-session approval toggles |
| `streamChunk` | `{content, model?, sessionId}` | Stream assistant response (accumulated, not delta) |
| `streamThinking` | `{content, sessionId}` | Stream thinking content (accumulated, not delta) |
| `collapseThinking` | `{sessionId, durationSeconds?}` | Collapse the currently open thinking block (with optional accurate duration) |
| `thinkingBlock` | `{content, sessionId}` | Persisted thinking block (used in history rebuild) |
| `showWarningBanner` | `{message, sessionId}` | Show a warning banner in the chat (e.g., model lacks tool support) |
| `finalMessage` | `{content, model?, sessionId}` | Finalize response scoped to a session |
| `generationStarted` | `{sessionId}` | Mark session as generating |
| `generationStopped` | `{sessionId}` | Mark session as stopped |
| `addMessage` | `{message, sessionId}` | Append a message in a specific session |
| `loadSessionMessages` | `{messages, sessionId, autoApproveCommands, autoApproveSensitiveEdits, sessionSensitiveFilePatterns}` | Load messages + approval settings for a session |
| `clearMessages` | `{sessionId}` | Clear all messages for a session |
| `showError` | `{message, sessionId}` | Show error message in session |
| `connectionError` | `{error}` | Show connection error (non-session-scoped) |
| `addContextItem` | `{context: {fileName, content}}` | Add code context from editor selection |
| `loadSessions` | `{sessions, hasMore, nextOffset}` | Replace sessions list |
| `appendSessions` | `{sessions, hasMore, nextOffset}` | Append to sessions list |
| `updateSessionStatus` | `{sessionId, status}` | Update a single session's status indicator |
| `sessionDeleted` | `{sessionId}` | Confirm single session deleted |
| `sessionsDeleted` | `{sessionIds}` | Confirm batch session deletion (empty array = cancelled) |
| `deletionProgress` | `{completed, total}` | Batch deletion progress (10+ sessions) |
| `searchSessionsResult` | `{results, query, error?}` | Return session search results |
| `dbMaintenanceResult` | `{success, deletedSessions?, deletedMessages?, message?}` | Maintenance result |
| `recreateMessagesResult` | `{success, message?}` | Messages table recreation result |
| `connectionTestResult` | `{success, message}` | Connection test result |
| `bearerTokenSaved` | `{hasToken}` | Token save confirmation |
| `navigateToSettings` | `{isFirstRun}` | Navigate webview to settings page (first-run or manual) |
| `modelEnabledChanged` | `{models}` | Broadcast updated model list after enable/disable toggle |
| `capabilityCheckProgress` | `{completed, total}` | Progressive capability detection progress |
| `capabilityCheckComplete` | - | Capability detection finished |
| `filesChanged` | `{checkpointId, files: [{path, action}], status, sessionId}` | Show files-changed widget (standalone, not in thread) |
| `filesDiffStats` | `{checkpointId, files: [{path, additions, deletions}]}` | Update per-file +/- stats in widget |
| `fileChangeResult` | `{checkpointId, filePath, action, success, sessionId}` | Single file kept/undone — remove from widget |
| `keepUndoResult` | `{checkpointId, action, success, sessionId}` | Keep All / Undo All — remove entire widget block |
| `reviewChangePosition` | `{checkpointId, current, total, filePath?}` | Update "Change X of Y" counter + active file indicator in widget |

## Frontend → Backend Messages

| Message Type | Payload | Purpose |
|--------------|---------|---------|
| `ready` | `{sessionId?}` | UI initialized (triggers `init` response, optionally restores session) |
| `sendMessage` | `{text, context}` | User message |
| `stopGeneration` | `{sessionId}` | Cancel generation for a session |
| `selectMode` | `{mode}` | Change mode |
| `selectModel` | `{model}` | Change model |
| `newChat` | - | Create new session (reuses idle empty session if one exists) |
| `addContext` | - | Request code context from active editor selection |
| `loadSession` | `{sessionId}` | Load session |
| `deleteSession` | `{sessionId}` | Delete session (optimistic removal on frontend) |
| `deleteMultipleSessions` | `{sessionIds}` | Batch delete with modal confirmation |
| `searchSessions` | `{query}` | Search sessions by content |
| `saveSettings` | `{settings}` | Save settings |
| `testConnection` | `{baseUrl?}` | Test server connection (optionally apply URL first) |
| `saveBearerToken` | `{token, testAfterSave?, baseUrl?}` | Save bearer token (optionally test after) |
| `loadMoreSessions` | `{offset}` | Load more sessions (pagination) |
| `runDbMaintenance` | - | Run DB maintenance cleanup |
| `recreateMessagesTable` | - | Recreate LanceDB messages table |
| `toolApprovalResponse` | `{approvalId, approved, command?}` | Respond to terminal command approval |
| `setAutoApprove` | `{sessionId, enabled}` | Toggle auto-approve commands for session |
| `setAutoApproveSensitiveEdits` | `{sessionId, enabled}` | Toggle auto-approve sensitive edits for session |
| `updateSessionSensitivePatterns` | `{sessionId, patterns}` | Update session-level sensitive file patterns |
| `openFileDiff` | `{approvalId}` | Open file diff in VS Code editor |
| `refreshCapabilities` | - | Trigger background `/api/show` for all models |
| `toggleModelEnabled` | `{modelName, enabled}` | Enable/disable a model in SQLite |
| `keepFile` | `{checkpointId, filePath}` | Keep a single file's changes |
| `undoFile` | `{checkpointId, filePath}` | Undo a single file's changes |
| `keepAllChanges` | `{checkpointId}` | Keep all files in checkpoint |
| `undoAllChanges` | `{checkpointId}` | Undo all files in checkpoint |
| `requestFilesDiffStats` | `{checkpointId}` | Request +/- diff stats for widget (also triggers review session build) |
| `openFileChangeDiff` | `{checkpointId, filePath}` | Open diff view for a file |
| `openFileChangeReview` | `{checkpointId, filePath}` | Open inline review (CodeLens) for a file |
| `navigateReviewPrev` | `{checkpointIds}` | Navigate to previous change (hunk-level, cross-file) |
| `navigateReviewNext` | `{checkpointIds}` | Navigate to next change (hunk-level, cross-file) |
| `openWorkspaceFile` | `{path, line?}` | Open a workspace file in the editor, optionally at a specific line |
| `revealInExplorer` | `{path}` | Reveal a folder/file in the VS Code file explorer sidebar |

## Session-Concurrent Streaming

- Streaming, tool actions, and progress updates are routed with `sessionId`.
- The webview ignores updates that do not match the currently active session.
- Background sessions continue generating; switching sessions does not stop generation.
- The Stop button sends `stopGeneration` with the active `sessionId`.

## Chat View Backend Structure

Keep `src/views/chatView.ts` small and focused. Use these files for specific concerns:

## Files Changed Widget Message Flow

The files-changed widget lives in **standalone state** (`filesChangedBlocks` ref), not inside assistant thread blocks. Messages flow as:

```
Agent writes files
  → agentChatExecutor emits 'filesChanged' (persisted + posted)
  → webview handleFilesChanged() creates/merges standalone block
  → webview requests 'requestFilesDiffStats' for +/- counts
  → backend responds with 'filesDiffStats'

User clicks Keep/Undo on a file
  → webview posts 'keepFile'/'undoFile' (NO sessionId!)
  → chatView.handleKeepFile() resolves sessionId from sessionController
  → Persists 'fileChangeResult' + posts to webview
  → webview handleFileChangeResult() removes file from block
  → chatView calls sendSessionsList() to refresh session stats badge

User clicks Keep All / Undo All
  → webview posts 'keepAllChanges'/'undoAllChanges' (NO sessionId!)
  → chatView.handleKeepAllChanges() resolves sessionId from sessionController
  → Persists 'keepUndoResult' + posts to webview
  → webview handleKeepUndoResult() removes entire block
  → chatView MessageRouter → FileChangeMessageHandler calls sendSessionsList() to refresh session stats badge

User navigates changes (prev/next)
  → webview posts 'navigateReviewPrev'/'navigateReviewNext' with checkpointIds[]
  → ReviewNavMessageHandler calls reviewService.navigateChange(direction, checkpointIds)
  → Backend responds with 'reviewChangePosition' {current, total, filePath}
  → webview updates "Change X of Y" counter + highlights active file

Widget requests diff stats
  → webview posts 'requestFilesDiffStats' per checkpoint
  → FileChangeMessageHandler calls reviewService.startReviewForCheckpoint() (builds/merges session)
  → Backend responds with 'filesDiffStats' + 'reviewChangePosition'
```

**⚠️ The webview does NOT send `sessionId`** in keep/undo messages. The backend MUST resolve it via `this.sessionController.getCurrentSessionId()`. Without this, `persistUiEvent` silently skips (see Pitfall #13 in `copilot-instructions.md`).

**History restoration**: `timelineBuilder.ts` handles `filesChanged`, `fileChangeResult`, and `keepUndoResult` events by building/merging/removing standalone `filesChangedBlocks`. Multiple incremental `filesChanged` events with the same `checkpointId` must be **merged** (not duplicated) — see Pitfall #14.

**Fallback for missing `__ui__` events**: `chatSessionController.ensureFilesChangedWidget()` fires after `loadSessionMessages`. If no `filesChanged` `__ui__` event exists in the session's messages but the DB has pending checkpoints with pending file_snapshots, it posts synthetic `filesChanged` messages. This handles old sessions or sessions where `persistUiEvent` silently skipped due to undefined `sessionId` (Pitfall #13). See the full flow diagram in `extension-architecture.instructions.md` → "Diff Stats Flow".

- **`src/views/chatView.ts`**
  - Webview lifecycle + MessageRouter wiring only
  - Implements `WebviewMessageEmitter`
  - Routes all messages via `MessageRouter` to `IMessageHandler` implementations

- **`src/views/messageHandlers/`** (IMessageHandler implementations)
  - `chatMessageHandler.ts` — chat/agent mode: send, stop, mode/model switch
  - `sessionMessageHandler.ts` — session load/delete/search
  - `settingsMessageHandler.ts` — save settings, test connection, DB ops
  - `approvalMessageHandler.ts` — tool/file approvals, auto-approve toggles
  - `fileChangeMessageHandler.ts` — keep/undo files, diff stats
  - `modelMessageHandler.ts` — refresh capabilities, toggle models
  - `reviewNavMessageHandler.ts` — inline review prev/next navigation

- **`src/views/chatSessionController.ts`**
  - Session creation/loading/deletion
  - Session list + search + status updates
  - Current session state + message cache

- **`src/views/settingsHandler.ts`**
  - Read/save settings
  - Test connection + token handling
  - DB maintenance actions

- **`src/services/agent/agentChatExecutor.ts`** (orchestrator) + **`src/services/agent/agentToolRunner.ts`** (tool batch execution) + **`src/services/agent/agentStreamProcessor.ts`** (streaming) + **`src/services/agent/agentSummaryBuilder.ts`** (post-loop finalization)
  - Agent execution loop
  - Tool call parsing + execution
  - Progress group + tool UI updates (via emitter)

- **`src/views/toolUIFormatter.ts`**
  - Pure helpers mapping tool calls/results → UI text/icons

- **`src/views/chatTypes.ts`**
  - Shared view types + `IMessageHandler` + `ViewState`
  - `WebviewMessageEmitter` interface

**Rule:** Do not re-bloat `chatView.ts`. If a method exceeds ~50 lines or handles a distinct concern, create a new `IMessageHandler` class in `src/views/messageHandlers/`.

## Streaming Behavior

The backend sends **accumulated content** with each stream chunk, not incremental deltas:

```typescript
// Backend sends: "Hello", then "Hello World", then "Hello World!"
// NOT: "Hello", then " World", then "!"
handleStreamChunk({ content: 'Hello World!' }); // replaces, not appends
```

The `handleStreamChunk` handler **replaces** the text block content, it does not append.

### First-Chunk Gate

The backend applies a content gate before sending the first `streamChunk` to prevent incomplete markdown (like `**What`) from flashing in the UI:

- **First chunk**: Requires ≥8 word characters before sending. While gated, the spinner remains visible.
- **Subsequent chunks**: Sent with ≥1 word character (markdown renderer has enough prior context).
- **Thinking content** (`streamThinking`): No gate — sent immediately since it renders in a collapsible block, not inline markdown.
