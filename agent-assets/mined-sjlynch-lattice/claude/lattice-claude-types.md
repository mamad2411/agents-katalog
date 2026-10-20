# frontend/src/api/types

Domain-split TypeScript types for backend payloads. `index.ts` re-exports this
folder, and `../types.ts` is the legacy compatibility shim.

## Shared vs local

A wire type the backend declares in a node-free module is re-exported from
`backend/src/shared/wireTypes.ts` — never redeclared here (hand mirrors drift;
an audit found ten that had). Rules for what may go there:
`backend/src/shared/CLAUDE.md`.

- **Shared (re-export only):** `tasks.ts` (`Task`), `terminalTabs.ts`
  (`TerminalRecord` family), `git.ts`, `gitHistory.ts`, `health.ts` (incl.
  `HealthUpdate`), `harnessSystemPrompts.ts`, `instructionTemplates.ts`,
  `postMergeHooks.ts`, `projectEnv.ts`, `runs.ts`, `workflows.ts` (definitions,
  `WorkflowRun`, `SourceArea` / `SourceAreasResult`), `opengrep.ts` (status, rule packs,
  scan records / envelope, graph result, findings, triage, `SecurityReview` —
  all from `backend/src/opengrep/types.ts`), `scan.ts`'s `DirListing` family,
  and `settings.ts`'s `RecentSpecGap`, Pi model and `OpengrepSeverity` /
  `OpengrepProjectSettings` types. Outside this folder, `../globalSettings.ts`
  (`GlobalSettings`, `PiProvider` / `PiProviderModel`) and `../mcp.ts` (the
  `McpServerEntry` family) re-export theirs beside their fetch helpers. Local
  names may alias a backend name
  (`InstructionTemplate` = `InstructionTemplateEditorEntry`,
  `OpengrepRulePackStatus` = `RulePackStatus`).
- **Composed here from shared types** (the frontend genuinely differs):
  WS envelopes the endpoint adds outside the backend union — `idle` in
  `MergeRunEvent` / `PostMergeHookEvent`, `hello` in `WorkflowRunEvent`
  (`backend/src/ws/endpoints/`); `ProjectInitResult` (`{ ok: true } &` the
  backend result — the route adds `ok`); `RestoreSummary` (optional
  `relaunchedIds` for an older backend); `PushRunStatus` / `QaRunStatus`.
- **Frontend-only:** request/response wrappers and UI shapes
  (`WorkflowQueueEntry`, `WorkflowRunStartOptions`, `TerminalLaunchSettings`,
  `PostMergeHookSnapshot`, `ProjectEnvResponse`, …) and runtime values
  (`RUN_TESTS_*` minutes, `DEFAULT_METRICS_IGNORED_EXTS`) — `wireTypes.ts` is
  type-only, so keep those equal to the backend by hand.
- **Still hand mirrors** — their backend module reaches node, so check the
  backend when you touch one: `scan.ts`'s
  `GraphNode` / `ScanResult` / `SearchResult` (`scanner/`, `search.ts`),
  `PiProbeModel` (`piModels/probe.ts`). To share one, move the type into a
  node-free module first (as `HealthUpdate`, `EnvNoteInfo`, the `*EditorEntry`
  types, `WorkflowRun`, the Opengrep types, `UserSettings`, `GlobalSettings`
  and the MCP / Pi-provider types were) and re-export it from its old module.

## Conventions

- Where the backend always sends a field, use its required type rather than an
  optional local copy.
- Keep request/response shapes close to the API module that consumes them
  (`tasks`, `workflows`, `runs`, `settings`, etc.).
- Prefer explicit string unions that mirror backend types over loose `string`
  when the UI branches on values.
- Do not put fetch helpers here; runtime calls belong in `frontend/src/api/*.ts`.
- When adding a type file, export it from `types/index.ts` and ensure
  `frontend/src/api/CLAUDE.md`'s module list remains accurate if the domain is
  new.
