# backend/src/shared — code both packages import

Logic and types the backend and the frontend must agree on, written ONCE.
The frontend imports these files by relative path
(`../../backend/src/shared/harnesses`); Vite bundles them and `tsc -b` checks
them. Before this folder each pair was hand-copied and kept "in lockstep" by
comments, and several had drifted.

## Rules

- **Relative imports only** — no `node:` builtins, no npm packages, anywhere in
  the graph reachable from here (including what `wireTypes.ts` re-exports).
  Pinned by `__tests__/sharedFolderBoundary.test.ts`.
- Must also compile under the frontend's stricter flags (`verbatimModuleSyntax`,
  `erasableSyntaxOnly`, `noUnusedLocals`): `import type` for types, no enums or
  parameter properties.
- A shared module the terminal-server reaches (today `harnesses.ts`, via
  `../harnesses.ts`) must be listed in `../terminalFingerprint.ts`.
- Something both sides need → put it here rather than copying it.

## Modules

- `workflowSplit.ts` - safe split configuration / POSIX-path normalization.
- `sourceAreas.ts` — production-source filtering, deterministic directory-area
  partitioning, `SourceArea` / `SourceAreasResult` and the planner scope preface.
- `harnesses.ts` — `AgentHarness` vocabulary + `PI_MODEL_PATTERN_RE` /
  `isPiModelPattern` (the `pi --model` shell-injection guard).
- `searchPattern.ts` — `wildcardRegexSource`: search query → regex source
  (graph filename pass and backend content search / ripgrep).
- `workflowVariables.ts` — the `{{name}}` grammar, `normalizeVariableName`,
  `USER_INSTRUCTIONS_VAR`.
- `terminalLabels.ts` — `shortLabel` for terminal tabs.
- `launchGuidance.ts` — `effortSuggestion`: evidence-backed effort hints for
  the workflow launch selects (each entry cites its benchmark result).
- `wireTypes.ts` — type-only re-exports (`export type { … } from`, nothing
  else) of the wire types `frontend/src/api/types/*` re-export instead of
  redeclaring: tasks, terminal registry, project init, git history, health
  (incl. `HealthUpdate`), harness-prompt / instruction-template editor entries,
  post-merge hooks, project env notes, merge / push / QA runs, folder browser,
  Pi models and providers, Codex models, workflows, workflow runs, user and global settings, recent Spec gaps,
  MCP server entries and Opengrep (status, packs, scans, graph, triage,
  reviews, project settings). Which
  frontend types are still hand mirrors, and why:
  `frontend/src/api/types/CLAUDE.md`.
- Adding one: its backend module — and every module reachable from it, inline
  `import('…')` types included — must be node-free and npm-free. If it isn't,
  move the TYPE into a node-free types module and re-export it from the old
  module so backend importers don't change (`McpSpawnScope` →
  `../mcp/spawnScope.ts`, `WorkflowRun` → `../workflowRuns/types.ts`,
  `HealthUpdate` → `../health/types.ts`, the `*EditorEntry` types → their
  `defs.ts`, the Opengrep wire types → `../opengrep/types.ts`,
  `GlobalSettings` → `../globalSettings/types.ts`, `McpServerEntry` →
  `../mcp/types.ts`, `PiProvider` → `../piModels/types.ts`). Never move
  runtime code for this. A wire shape the backend only infers (a route's
  object literal) gets a named type there and the function an explicit
  return type, so the two can't drift.
