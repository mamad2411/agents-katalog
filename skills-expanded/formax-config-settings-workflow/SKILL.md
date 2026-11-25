---
name: formax-config-settings-workflow
description: Use when implementing or extending /config (storage, prompt injection, request params, UI-only toggles) with tests and strict UI parity.
---

# formax-config-settings-workflow

## Goal

Use this skill when changing runtime config merge semantics, `/config` persistence, or the current settings exposed by the config dialog.

## Read First

- `docs/contracts/config-settings-contract.md`
- `docs/environment-variables.md`
- `docs/contracts/prompt-tool-exposure-contract.md` when a setting affects prompt injection or request composition

These docs are canonical. If stable behavior changes, update them before or with code.

## Code Map

- **Config schema + merge semantics**
  - `packages/core/src/config/settings/schema.ts` (add fields + defaults; validate values)
  - `packages/core/src/config/settings/resolve.ts` (merge precedence + `sources` mapping)
  - `packages/core/src/config/settings/persist.ts` (patch read/write + `stripDefaultsFromPatch`)
- **Disk locations**
  - `packages/core/src/adapters/fs/configPaths.ts` (project/global config dirs)
  - `packages/core/src/adapters/fs/configFiles.ts` (load `config.json` patches)
  - `packages/core/src/config/config.ts` (final `RuntimeConfig` shape used by UI/runtime)
- **/config UI overlay**
  - `packages/core/src/tui/config/ConfigDialog.tsx` (reads effective config + writes patches)
  - `packages/core/src/tui/config/constants.ts` / `packages/core/src/tui/config/reducer.ts` / `packages/core/src/tui/config/ui.tsx`
  - `packages/core/src/screens/REPL.tsx` (mount overlay + reload runtime config on exit)
- **Runtime wiring (effects)**
  - Prompt injection: `packages/core/src/features/repl/controller/send/sendMainTurn.ts` + `packages/core/src/features/repl/controller/session/localCommandInjection.ts` + `packages/core/src/prompts/reminders/*`
  - Request parameters: `packages/core/src/chat/engine.ts` → `packages/core/src/streaming/**`
  - UI-only flags: `packages/core/src/screens/REPL.tsx` and small helpers under `packages/core/src/screens/repl/*`
- **Current `/config` subset**
  - `packages/core/src/features/commands/configDialogService.ts` currently owns `outputStyle`, `thinkingMode`, `verboseOutput`

## Current Behavior Checkpoints

- Classify each setting before coding:
  - prompt-affecting
  - request-parameter
  - UI-only
- Storage rule:
  - User scope -> `$FORMAX_CONFIG_DIR/config.json`
  - Project scope -> `<repo>/.formax/config.json`
  - Prefer sparse writes; do not persist defaults just because a dialog touched them
- Immediate effect:
  - `/config` saves are expected to reload effective runtime config in-process
  - avoid "restart required" behavior unless that is an explicit change
- Exit-message contract:
  - unchanged dialog -> `Status dialog dismissed`
  - changed setting -> `Set <field> to <value>` style subline

## Minimal Workflow

1. Classify the setting first: prompt-affecting, request-parameter, or UI-only.
2. Update the config settings contract first; if env names or classification changed, also update `docs/environment-variables.md`.
3. Change schema / resolve / persist before changing dialog wiring or runtime effects.
4. Preserve sparse writes and immediate in-process reload behavior.
5. Only output-style style changes may inject next-turn local command blocks; non prompt-affecting settings must stay out of model context.
6. Run the minimum regression set below before review.

## Minimum Regression

- `bun run test -- packages/core/src/config/settings/schema.test.ts packages/core/src/config/settings/resolve.test.ts packages/core/src/config/settings/persist.test.ts`
- `bun run test -- packages/core/src/features/commands/configDialogService.test.ts`
- `bun run test -- packages/core/src/tui/config/ConfigDialog.test.tsx` when dialog UI changes
- `bun run test -- packages/core/src/features/repl/controller/session/localCommandInjection.test.ts packages/core/src/features/repl/controller/send/sendMainTurn.test.ts` when prompt-affecting config changes
- `bun run test -- packages/core/src/screens/repl/thinkingBlock.test.tsx` when UI-only thinking visibility changes
- `bun run type-check` when config shape or runtime wiring changes

## Guardrails

- Do not add new config scopes or extra config files (`cache.json`, `runtime.json`, etc.) without an explicit decision.
- Do not inject next-turn prompt blocks for UI-only or request-only settings.
- Do not let `docs/environment-variables.md` and config behavior drift into two separate truths; names live there, merge/persist semantics live in the contract.
- Do not change dialog copy/spacing/colors unless explicitly requested.
- Add/extend targeted tests before refactoring config wiring; tests are not the whole spec, but they should lock current persistence semantics first.
