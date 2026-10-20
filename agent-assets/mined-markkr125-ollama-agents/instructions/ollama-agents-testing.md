---
applyTo: "tests/**"
description: "Testing guidelines, test harness setup, existing test coverage catalogs, and webview test rules"
---

# Testing Guidelines

## Build Validation (Required)

- After making code changes, ensure the project still compiles successfully.
- Use `npm run compile` to verify the extension and webview build.
- Run `npm run lint:all` to check ESLint, docs structure, and naming conventions.

## Automated Testing (Required)

This repo uses two complementary test harnesses:

1) **Extension host tests (integration-ish)**
- Runner: `@vscode/test-electron` + Mocha
- Command: `npm test`
- Location:
  - Test harness + mocks: `tests/extension/`
  - Test suites: `tests/extension/suite/`
    - `tests/extension/suite/agent/` for agent tool tests (toolRegistry, readFile)
    - `tests/extension/suite/utils/` for pure utilities (toolCallParser, commandSafety, toolUIFormatter)
    - `tests/extension/suite/services/` for service-level integration tests

2) **Webview tests (fast unit/component)**
- Runner: Vitest + jsdom + Vue Test Utils
- Command: `npm run test:webview`
- Location: `tests/webview/`
- Config: `tests/webview/vitest.config.ts`

To run everything locally (recommended before pushing): `npm run test:all`.

## Post-Change Test Requirements (Non-Negotiable)

After **any** code or test change, run the appropriate test suite(s) before considering the work done:

| What changed | Command | Why |
|---|---|---|
| `src/webview/**` only | `npm run test:webview` | Fast Vitest tests for webview logic |
| `src/**` (non-webview) only | `npm test` | Extension host tests (launches VS Code, runs Mocha) |
| Both, or unsure | `npm run test:all` | Runs both harnesses sequentially |
| New test files added | `npm run test:all` | Verify new tests actually run and pass in the correct harness |

**Common mistake**: Creating extension host test files (under `tests/extension/`) but only running `npm run test:webview`. The new tests compile (`tsc --noEmit`) but are never executed. Always run `npm test` when adding/changing extension host tests.

**Common mistake**: Running `npx tsc -p tsconfig.test.json --noEmit` and assuming tests pass. Type-checking only validates types — it does NOT execute the tests. A test can compile cleanly and still fail at runtime.

## ⚠️ Both Harnesses Are Mandatory (Non-Negotiable)

When a feature or bug fix spans both backend (`src/services/`, `src/agent/`, `src/views/`, `src/utils/`) and frontend (`src/webview/`), **BOTH** test harnesses must receive new tests. This is the most commonly neglected rule.

### The Rule

> **If your change touches backend logic AND has UI implications, you MUST write tests in BOTH `tests/extension/` (Mocha) AND `tests/webview/` (Vitest).** Skipping either harness is not acceptable.

### Why This Matters

- **Vitest-only coverage** catches webview rendering/state bugs but misses backend logic errors (wrong data emitted, wrong persistence, wrong tool execution).
- **Mocha-only coverage** catches service/utility bugs but misses how the UI consumes the data (duplicate entries, wrong state transitions, parity mismatches).
- **Type-checking is not testing.** `tsc --noEmit` passing does NOT mean behavior is correct.

### Concrete Examples

| Change | Extension host test (Mocha) | Webview test (Vitest) |
|--------|-----------------------------|-----------------------|
| New tool verb ("Created"/"Edited") | `toolUIFormatter.test.ts`: verify `getToolSuccessInfo` returns correct verb for `_isNew` flag | `ProgressGroup.test.ts`: verify component renders correct text; `parity.test.ts`: verify live === restored |
| New agent tool | `toolRegistry.test.ts`: tool registered, executes correctly | `parity.test.ts`: tool action events produce correct timeline |
| New message type | Handler test in `tests/extension/suite/`: verify correct `postMessage` + `persistUiEvent` | `messageHandlers.test.ts` or `parity.test.ts`: verify handler produces correct blocks |
| File edit approval flow change | Service test: verify approval emission sequence | `parity.test.ts`: verify live/restored parity for the new flow |
| New setting | `settingsHandler.test.ts`: verify setting read/write | `SettingsPage.test.ts`: verify UI binds to setting correctly |

### Enforcement Checklist

Before marking a task as done, verify:

- [ ] Extension host tests cover the backend logic (`npm test` passes)
- [ ] Webview tests cover the UI/state behavior (`npm run test:webview` passes)
- [ ] Both test suites are actually **executed** (not just compiled)
- [ ] `npm run test:all` passes end-to-end

## What to test with Vitest vs `@vscode/test-electron`

Use the two harnesses for different risk profiles:

**Prefer Vitest (tests/webview) when:**
- You're testing UI "business logic" that should be fast, deterministic, and not depend on VS Code.
- The target lives in `src/webview/scripts/core/*` (state/actions/computed) or a Vue component with clear props/events.
- You want tight coverage on edge cases that are painful to validate via a full VS Code host.

Good Vitest targets:
- `src/webview/scripts/core/actions/` (barrel: `index.ts`): debounced search, context packaging for send, tool/approval UI updates, message/thread merging behavior.
- `src/webview/scripts/core/computed.ts`: header/title selection, derived counts, tool timeout conversions.
- Vue components with important contracts:
  - `src/webview/components/chat/components/CommandApproval.vue`: editable command only when `status === 'pending'`; approve sends edited command.
  - `src/webview/components/SessionsPanel.vue`: pagination (`loadMoreSessions`) + selection (`loadSession`) + loading flags.

**Prefer `@vscode/test-electron` (tests/extension) when:**
- You need real VS Code APIs (`vscode`), extension activation, commands, view registration, or storage URIs.
- You're validating backend/service behavior (SQLite sessions, LanceDB messages, ordering/maintenance, tool execution).
- You want to cover multi-module integration flows end-to-end (even if the UI is mocked).

Good `@vscode/test-electron` targets:
- Extension activation and message routing (`ChatViewProvider` → controllers/services).
- `DatabaseService` invariants (timestamps strictly increasing; maintenance never deletes sessions; delete cascades).
- Mocked Ollama/OpenWebUI HTTP interactions (streaming NDJSON, retry, connection test) using the local mock server.

**Rule of thumb:**
- If the bug would show up as "wrong state / wrong UI rendering / wrong postMessage payload", write Vitest.
- If the bug would show up as "VS Code integration broken / storage broken / commands missing / streaming broken", write `@vscode/test-electron`.

**High-ROI next webview tests to add (Vitest):**
- Sessions UI: `SessionsPanel.vue` pagination and selection behavior (load more, click session, correct postMessage payloads).

## Existing test coverage (Vitest)

The following test suites exist in `tests/webview/`:

**`timelineBuilder.test.ts`** (31 tests) - Tests the `buildTimelineFromMessages` function:
- Block-based structure: user messages, assistant threads, text block merging
- UI event replay: `startProgressGroup`, `showToolAction`, `finishProgressGroup`
- Command approval flow: `requestToolApproval`, `toolApprovalResult`, skipped status
- **File edit approval flow**: `requestFileEditApproval`, `fileEditApprovalResult`
- Full workflow matching live/history parity
- Edge cases: implicit groups, orphan approvals, invalid JSON handling
- **Critical**: finishProgressGroup converts pending/running actions to success
- **Live/history parity tests**: `showToolAction` update-in-place behavior (same text, different text, pending→running→success)
- **Thinking blocks**: `thinkingBlock` event creates collapsed thinking blocks in thread, multiple blocks, empty content
- **showError event**: Creates error action in progress group, works within existing groups
- **Chunked read_file**: `startLine` preserved on chunk actions, `filePath` without `checkpointId` for reads, `list_files` detail with basePath preserved

**`messageHandlers.test.ts`** (24 tests) - Tests live message handlers:
- Streaming handlers: `handleStreamChunk` creates/updates text blocks
- Progress group handlers: start/show/finish progress groups
- Approval handlers with live/history parity: both progress group action AND approval card
- **Critical contract test**: `complete workflow produces same structure as timelineBuilder`
- **Critical contract test**: `file edit approval workflow produces same structure as timelineBuilder`
- **Connection test result**: `handleConnectionTestResult` populates model options, syncs model selection, preserves models on error
- **Settings update**: `handleSettingsUpdate` does not clear model options
- **Thinking block handlers**: `handleStreamThinking` creates/updates thinking blocks, `handleCollapseThinking` collapses them, new thinking after collapse creates new block
- **Warning banner handler**: `handleShowWarningBanner` sets banner state, ignores wrong session
- **Chunked read_file handlers**: `startLine` and `filePath` passthrough, no `checkpointId` on read actions, multiple chunks create separate action items

**`actions.test.ts`** (10 tests) - Tests UI actions:
- Debounced search behavior
- Auto-approve toggle/confirm
- Context packaging for send (posts sendMessage, clears input/context)
- Stop generation when already generating
- Progress group creation
- Assistant message/thread creation
- Highlight snippet wraps query terms in `<mark>`
- Settings actions: `saveBearerToken` includes baseUrl (race avoidance), empty token no-op, `testConnection` includes baseUrl

**`computed.test.ts`** (4 tests) - Tests derived state:
- Temperature display formatting

**`CommandApproval.test.ts`** (2 tests) - Tests Vue component:
- Editable command input only when status is `pending`

**`MarkdownBlock.test.ts`** (4 tests) - Tests Vue component:
- Renders markdown content via computed property
- Updates when content prop changes
- Caching behavior prevents unnecessary re-renders

**`ProgressGroup.test.ts`** (24 tests) - Tests Vue component:
- **`isCompletedFileGroup` guard** (REGRESSION): Flat view only for file edits with `checkpointId`; read actions (no `checkpointId`) render as normal progress groups; running groups never render flat; mixed actions require ALL to have `checkpointId`
- **Flat write group rendering** (REGRESSION): Write/modify groups render flat in running state; spinner shown for running actions, checkmark for completed; no duplicate action entries per file; chevron hidden when no filename; non-write groups (e.g. "Reading files") never render flat when running
- **File click handling**: Click with `checkpointId` opens diff view; click without (read action) opens file at `startLine`; click without `startLine` opens at undefined
- **Tree listing**: Renders `├`/`└` connectors, full path tooltip, folder click → `revealInExplorer`, file click → `openWorkspaceFile`, summary strips basePath from display
- **Action rendering**: Title display, detail text, `has-listing` class for multi-line detail

**`SettingsPage.test.ts`** (19 tests) - Tests settings page composable + component:
- **Composable (`useSettingsPage`)**: bearer input, temperature input, tool timeout input, recreate messages table delegation, dismiss welcome, session patterns sync (immediate, reactive, defaults)
- **Component**: welcome banner visibility + dismiss, navigation sections rendering + click + active class, page visibility based on `currentPage`, recreate messages button, test connection button, model options in select dropdowns

**`parity.test.ts`** (19 tests) - Tests live/history structural parity:
- Ensures that live message handlers and `timelineBuilder` produce identical timeline structures for the same event sequences
- **Chunked read_file parity**: Verifies that chunked `read_file` actions with `startLine` and `filePath` produce identical structures in live handlers vs `timelineBuilder`, and that `checkpointId` is absent (not misidentified as file edits)
- **REGRESSION: write_file single action**: Verifies exactly one action per file write (running → success merge), no duplicates, live === restored
- **REGRESSION: edit verbs**: Verifies "Editing" → "Edited" verbs for existing files (not "Write"/"Added"), live === restored
- **REGRESSION: multi-file write batch**: Verifies N files produce exactly N actions (not 2N), live === restored

**`core/filesChanged.test.ts`** (30 tests) - Tests files-changed widget state management:
- **ONE-widget merging**: single block creation, merging across checkpoints, dedup files, dedup checkpointIds
- **Diff stats**: `handleFilesDiffStats` populates per-file `additions`/`deletions`, recalculates totals
- **Per-file keep/undo**: single file removal, block removal when last file resolved, checkpointId cleanup
- **Bulk keep/undo**: per-checkpoint removal, full block removal, undo variant, failed keepAll no-op
- **Actions**: `keepAllChanges`, `undoAllChanges`, `keepFile`, `undoFile` postMessage payloads
- **Timeline builder merging**: two-checkpoint merge into one block, keepUndoResult removes checkpoint, all resolved removes block, fileChangeResult removes single file
- **REGRESSION: session restore**: requests diff stats for each checkpointId on restore, `statsLoading=true` on pending blocks
- **REGRESSION: safety net stats**: re-requests stats for old checkpoint files without stats, skips files that already have stats
- **REGRESSION: nav uses change-level counter**: `reviewChangePosition` updates `currentChange`/`totalChanges`, nav bar hidden until set, hunk-level not file-level count, nav actions post `checkpointIds` array
- **REGRESSION: re-edit stats refresh**: `handleFilesChanged` re-requests stats when all incoming files already exist (agent re-edits same file); verifies `requestFilesDiffStats` posted; stale totals trigger refresh; handles overlapping re-edit + new file combo; no re-request when incoming set is empty

## Existing test coverage (Extension Host)

The following test suites exist in `tests/extension/suite/`:

**`utils/toolCallParser.test.ts`** (24 tests) - Tests tool call parsing robustness:
- Basic parsing: XML and bracket format tool calls
- Balanced JSON extraction: nested objects, deeply nested content
- Alternative argument names: `arguments`, `args`, `params`, `parameters`
- Top-level arguments: when LLM puts args at root level
- Alternative tool name fields: `name`, `tool`, `function`
- Incomplete tool calls: LLM cutoff handling, missing closing braces
- Edge cases: escaped quotes, newlines, surrounding text, empty args
- Smart quote normalization: Unicode U+201C and U+201D to regular quotes

**`agent/toolRegistry.test.ts`** (17 tests) - Tests tool execution:
- read_file: accepts `path`, `file`, `filePath` arguments
- write_file: accepts multiple path formats, writes JSON and special characters
- list_files: lists workspace root correctly
- get_diagnostics: accepts multiple path argument names
- Tool registration: verifies all expected tools are registered

**`agent/readFile.test.ts`** (13 tests) - Tests streaming file I/O helpers:
- `CHUNK_SIZE` is 100
- `countFileLines`: small file, single-line no trailing newline, empty file (0 lines), 200-line file, nonexistent file rejects with ENOENT
- `readFileChunk`: first chunk of multi-line file, second chunk, full file range, single-line range, early stop (does not read beyond `endLine`), nonexistent file rejects, exactly `CHUNK_SIZE` lines, `CHUNK_SIZE + 1` lines boundary

**`utils/toolUIFormatter.test.ts`** (29 tests) - Tests tool UI text generation:
- `getProgressGroupTitle`: single read shows filename, multiple reads show comma-separated, >5 reads → "Reading multiple files", deduplication, `file` arg variant, read+write → "Modifying files", search/write/list/command titles, empty args fallback
- `getToolActionInfo`: read/write/list/search/unknown tool text, startLine line range in detail, empty detail without startLine
- `getToolSuccessInfo`: read returns filePath + line count, read with startLine returns range + startLine, write returns filePath, list_files includes basePath tab-separated, search reports match count, command reports exit code
- **REGRESSION: `_isNew` flag**: `write_file` with `_isNew=true` → "Created", `_isNew=false` → "Edited", omitted → "Edited" (default), `create_file` → "Created"

**`services/sessionIndexService.test.ts`** (8 tests) - Tests SQLite session/message CRUD:
- Session creation/update/listing with pagination
- Message CRUD with tool fields (tool_name, tool_input, tool_output)
- getNextTimestamp returns strictly increasing values
- Foreign key constraint prevents orphan messages
- CASCADE delete: deleteSession removes messages
- clearAllSessions removes all sessions and messages

**`services/databaseService.test.ts`** (3 tests) - Tests database facade:
- Message timestamps are strictly increasing and persist across restart
- Maintenance returns zero orphans (FK prevents them)
- deleteSession removes session and cascades to messages

**`services/databaseServiceDeletion.test.ts`** - Tests session deletion edge cases:
- Session deletion cascades to messages via FK constraint
- Re-deletion of already-deleted session is safe

**`services/databaseServiceExports.test.ts`** - Regression test for module exports:
- `getDatabaseService` is exported as a function (guards against stale webpack builds)
- `DatabaseService` class is exported

**`services/agentFileEditHandler.test.ts`** (10 tests) - Integration tests for file edit handler:
- **REGRESSION: Single running action (no duplicates)**: New file emits exactly ONE `showToolAction(running)` with "Creating" verb; existing file uses "Editing" verb; sensitive file with auto-approve still only ONE running action; sensitive file with manual approve produces ONE running + ONE pending, no extras
- **`_isNew` flag**: Set to `true` for non-existent files, `false` for existing files
- **postMessage/persistUiEvent parity**: Every posted event has a matching persisted event with correct sessionId; sensitive file approval flow persists all event types
- **Deferred content generation**: Uses `description` to generate content via LLM when `content` is missing; uses provided `content` directly when present

**`utils/commandSafety.test.ts`** - Tests terminal command safety analysis:
- Dangerous command detection (rm -rf, sudo, etc.)
- Platform-specific filtering

**`services/fileChangeMessageHandler.test.ts`** - Tests file change handler:
- **REGRESSION: requestFilesDiffStats recomputes from disk**: Stats are always fresh (recomputed from `original_content` vs current disk), not cached; verifies per-file + checkpoint totals update
- **REGRESSION: re-edit stats freshness**: When agent re-edits a file, `requestFilesDiffStats` returns updated stats matching the new content
- **REGRESSION: review position after keep/undo**: `handleKeepFile` and `handleUndoFile` post `reviewChangePosition` after removing file from review; counter decrements; zero hunks → no position sent

## Webview test rules (important)

- The webview runtime provides `acquireVsCodeApi()`. Our webview state module calls it **at import-time** in `src/webview/scripts/core/state.ts`.
- Therefore, tests MUST stub `acquireVsCodeApi` before importing any webview core modules.
  - This is handled centrally in `tests/webview/setup.ts` via Vitest `setupFiles`.
- Prefer testing logic in `src/webview/scripts/core/*` (state/actions/computed) over directly testing `src/webview/scripts/app/App.ts`.
  - `App.ts` wires `window.addEventListener('message', ...)` and is intentionally more integration-heavy.
- When asserting message sends to the extension, assert calls to the stubbed `postMessage` function.
- Keep tests deterministic: use `vi.useFakeTimers()` for debounced functions (e.g. search) and `vi.setSystemTime()` when IDs/timestamps are time-based.

## Debugging Tests

### Running a Single Test or Suite

**Extension host tests (Mocha):**
```bash
# Run a specific test file by grep pattern
npm test -- --grep "toolCallParser"

# Run tests matching a describe/it name
npm test -- --grep "should parse XML format"
```

**Webview tests (Vitest):**
```bash
# Run a specific test file
npm run test:webview -- tests/webview/core/timelineBuilder.test.ts

# Run tests matching a name pattern
npm run test:webview -- -t "should merge text blocks"

# Verbose output (shows each test name)
npm run test:webview -- --reporter verbose
```

### Debugging with Breakpoints

**Extension host tests**: Use the VS Code debugger with the "Extension Tests" launch configuration (see `.vscode/launch.json`). Set breakpoints in `tests/extension/suite/**` or in `src/**` — the debugger attaches to the VS Code Extension Host process.

**Webview tests**: Use the "Debug Webview Tests" launch configuration which runs Vitest in debug mode. Breakpoints work in both test files (`tests/webview/**`) and source files (`src/webview/**`).

### Common Test Failures & What They Mean

| Error | Cause | Fix |
|-------|-------|-----|
| `acquireVsCodeApi is not defined` | Test imports a webview module but `tests/webview/setup.ts` didn't run first | Ensure `setupFiles` includes `'./setup.ts'` in `tests/webview/vitest.config.ts` |
| `Cannot find module 'vscode'` | Extension test can't find VS Code APIs | Ensure you're running via `npm test` (which uses `@vscode/test-electron`), not `node` or `ts-node` directly |
| Extension tests hang indefinitely | Shell integration not available (CI, headless) or `waitForCommandEnd()` never resolves | Check that the test runner has a display (Xvfb in CI); add timeouts to terminal-dependent tests |
| `vi.resetModules()` doesn't clear state | Modules imported before `resetModules()` keep old references | Call `vi.resetModules()` then re-import the module via dynamic `import()` inside the test |
| Test passes alone but fails in suite | Shared mutable state between tests (e.g., `state.ts` refs) | Use `beforeEach` to reset state; use `vi.resetModules()` for module-level singletons |
| `SQLITE_CONSTRAINT: FOREIGN KEY` | Test tried to insert a message without creating the parent session first | Always call `createSession()` before `addMessage()` — FK constraints are enforced |
