# backend/src/userSettings

Per-project user settings stored at `<project>/.lattice/userSettings.json`.
`../userSettings.ts` is a re-export barrel over this folder, so every consumer
keeps importing from `'../userSettings.js'` and the public surface is unchanged.

## Files

- `types.ts` — the `UserSettings` schema (with all per-field commentary) plus
  the `StartupTerminal` and `TerminalDefaultHarness` types. **No I/O.** Add new
  settings fields here — the frontend uses this very type (re-exported via
  `../shared/wireTypes.ts`), so keep `types.ts` node-free: type-only imports
  from node-free modules (`../shared/harnesses.ts`, `../opengrep/types.ts`);
  `sharedFolderBoundary` enforces it.
- `storage.ts` — the path/storage layer: `settingsFile()`, `getUserSettings()`
  (read-or-`{}`), and `patchUserSettings()` (read-modify-write under the
  per-project `runExclusive('userSettings:<key>')` lock so concurrent disjoint
  patches don't clobber each other — see `serializeWrites.ts` and
  `__tests__/settingsPersistence.test.ts`). All paths are canonicalized via
  `canonicalProjectPath`. Also the **shape boundary** — see the invariant below.
  Writes use atomic temp-to-rename persistence. Display reads may fall back to
  defaults, but a PATCH rejects unreadable/corrupt existing state (incl. valid JSON that is not an object) and preserves
  its bytes; only ENOENT starts from empty settings.
- `features.ts` — feature-specific accessors layered on `getUserSettings`, each
  encoding a field's default semantics: `plannerSpecGapsIn` (default ON,
  planning briefs' recent implementer reports), `isClaudeMemoryDisabled`,
  `isPostMergeHookEnabled`, `isCodexYoloEnabled`, `isTaskAgentsLatticeMcpOnly`
  (+ its pure `taskAgentsLatticeMcpOnlyIn(settings)` for callers that already
  hold the settings) (all default ON — an absent field counts as `true`) and `isQaTerminalAutoCloseEnabled` (default
  OFF/stay-open — only explicit `true` opts in), `isKeepWorkflowStepTerminalsEnabled`
  (default OFF — only explicit `true` keeps a finished workflow agent step's
  pty alive; read by the workflow advance to pick `releaseWorkflowStepSession`
  over the kill, see `../workflowRuns/CLAUDE.md`), `isTaskAgentTypecheckEnabled`
  / `taskAgentTypecheckIn` and `isTaskAgentTestsEnabled` / `taskAgentTestsIn`
  (both default OFF — scoped type-checks / targeted test files respectively;
  boolean-only PATCH validation and malformed-value normalization in storage;
  see `../taskVerification.ts`),
  `getTaskWorktreeLfsContent` / `taskWorktreeLfsContentIn` (default
  `'pointers'` — anything but an explicit `'full'`, junk included, is pointer
  mode; see `../worktree/lfsMode.ts`). New "what does setting X mean
  for feature Y" helpers go here.

## Invariants

- `taskReview` defaults off (`taskReviewIn`); flag/re-run are opt-ins in Agent
  prompts. Reviewer harness defaults Codex, model gpt-6.1-sol (Claude:
  claude-sonnet-5-5), effort low. Rerun requires `taskReviewRerunHarness`;
  model/Pi-model/effort follow task launch policy. Storage validates enums
  (null clears optional fields), drops malformed stored values, and guards
  model strings like sibling fields. Completion gating is `../taskReview.ts`.

- `taskWritingRules` (absent = none) is trimmed, de-duplicated and cleared when
  empty in storage; PATCH validates at most 12 strings, 300 characters each.
  `plannerSpecGaps` defaults ON (`plannerSpecGapsIn` in `features.ts`); only
  `false` is stored. Both feed planning briefs via `../specGaps.ts`.
  `getUserSettingsStrict` rejects corrupt/unreadable files so optional brief
  enrichment can suppress itself on a failed read.

- **No taskCache import chain.** `storage.ts` imports `PROJECT_DIR_NAME` from
  `../taskCache/paths.js` (the leaf), **not** `../tasks.js` (which re-exports
  the whole task cache). userSettings is read at every spawn (the MCP registry
  at the spawn chokepoint), so it must stay free of that heavy chain. Keep new imports leaf-scoped.
- **A field the UI trusts field-by-field is coerced in `storage.ts`, on read
  AND on write.** These settings are not written only by the settings dialog:
  agents PATCH `/api/settings` directly, and the route hands the body through as
  `Partial<UserSettings>` — a TypeScript type that describes nothing at
  runtime. `startupTerminals` was stored verbatim as an agent-guessed
  `{name, command}` (no `id`, no `label`), and the dialog's `label.trim()` then
  threw on open, leaving that project's settings un-editable through the only UI
  that could have repaired the row (2026-08-26, interview_eci). So
  `normalizeUserSettings` runs in `getUserSettings` (a corrupt file heals on
  read) and on every incoming patch (a bad write never lands). It is a boundary
  guard, not a schema validator: add a field here only when a malformed value
  would break a consumer, and keep any minted identity **deterministic** — the
  frontend matches a live startup pty to its config by `id`, so an id that
  changed between reads would spawn a duplicate terminal on every reload. Pinned
  by `__tests__/startupTerminalsShape.test.ts`. The same guard covers the
  string-array fields (`deadCodeEntryGlobs`, `metricsIgnoredExts` — non-string /
  blank entries dropped, a non-array becomes absent; a string once made every
  `/api/scan` throw `globs.map is not a function`) and the plain-string fields
  (`postMergeHookPrompt`, `piModel`, `postMergeHookPiModel` — a non-string
  becomes absent). `userSettingsShapeError` lets `PATCH /api/settings` 400 such
  a value instead of silently healing it. Pinned by
  `__tests__/userSettingsFieldShapes.test.ts`.
- **Toggles for removed built-in MCP servers are stripped on read and on
  write** (`mcpOverrides`, `mcpHarnessOverrides.{codex,pi}`; ids in
  `mcp/retiredServers.ts`), so a stale `context7: true` can never switch on a
  custom server that later takes that id.
- **Default semantics live in the accessor, not the type.** A field being
  absent has a specific meaning per feature (memory-off-by-default,
  auto-close-off-by-default); encode that in `features.ts`, mirroring the
  opt-out/opt-in model documented on each field in `types.ts`.
