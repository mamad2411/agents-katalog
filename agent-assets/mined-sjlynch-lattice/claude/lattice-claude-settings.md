# backend/src/routes/settings

Sub-routers composed by `routes/settings.ts`. Paths are distinct, so mount order
is not significant within this folder.

- `userSettings.ts` — per-project `GET/PATCH /api/settings`; persists to the
  project's `.lattice/userSettings.json` via `userSettings.ts`.
- `specGaps.ts` — project-scoped `GET /api/spec-gaps`, recent implementer reports
  for the Agent prompts preview; selection/parsing lives in `../../specGaps.ts`.
- `projectEnv.ts` — read-only `GET /api/project-env`, exposing detected
  package-manager env notes used in task instructions.
- `instructionTemplates.ts` — editable prompt templates for task/merge/QA/push/
  post-merge/workflow prompts.
- `harnessSystemPrompts.ts` — read-only `GET /api/harness-system-prompts`: each
  harness's default system-prompt overview + the project's current Append/Replace
  override. Edits save through `PATCH /api/settings` (`harnessSystemPrompts`). See
  `backend/src/harnessSystemPrompts/`.
- `piModels.ts` — `GET /api/pi-models`; reads detected Pi models plus curated
  menu from global settings.
- `piEndpoints.ts` — `POST /api/pi-endpoints/probe`; OpenAI-compatible
  `/models` probe for Settings → Pi, answering `{models: [{id, contextWindow?}]}`.
- `codexModels.ts` — `GET /api/codex-models`; the Codex CLI's own model
  catalog cache (`../../codexModels.ts`), read-only.
- Keep per-project settings separate from machine-global settings; the latter
  live in `routes/globalSettings.ts`.
