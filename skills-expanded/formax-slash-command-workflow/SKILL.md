---
name: formax-slash-command-workflow
description: Use when adding/modifying Formax slash commands (/permissions /agents /hooks /todos etc), especially output rendering (command sublines), overlay dismiss messages, and whether outputs are injected into the next LLM turn.
---

# Formax slash command workflow

## Goal

Use this skill when changing slash command discovery, dispatch, overlay dismissal output, or next-turn injection behavior.

## Read First

- `docs/contracts/slash-command-contract.md`
- `docs/contracts/semantics-contract.md` when command behavior crosses canonical UI messages or routing
- `docs/contracts/config-settings-contract.md` when the change touches `/config`

These docs are canonical. If stable behavior changes, update them before or with code.

## Code Map

### 1) Command discovery + dispatch
- `packages/core/src/features/commands/registry.ts`: command list/suggest/dispatch wiring
- `packages/core/src/features/commands/CommandStore.ts`: disk scanning + precedence (project overrides user)
- `packages/core/src/features/semantics/core/commandRouting.ts`: exact `/clear` / `/compact` and command-dispatch routing boundary

### 2) Command result contract (UI vs model)
- `packages/core/src/features/commands/contracts.ts`: `UiEffect` / `UiMessage` / `ModelEffect` shapes
- `packages/core/src/features/commands/adapter.ts`: maps command execution output → `CommandResult`
- `packages/core/src/features/repl/controller/send/send.ts`: consumed slash handling, `local_async`, and injected-block plumbing

### 3) Overlay dismissal “subline output”
- `packages/core/src/features/repl/controller/ui/overlays.ts`: overlay open/close + append “dismissed” sublines

### 4) REPL message plumbing + rendering
- `packages/core/src/features/repl/controller/send/send.ts`: applies `UiEffect.appendMessages` to `Msg`
- `packages/core/src/screens/REPL.tsx`: render `msg.ui.kind === 'command_subline'` as `⎿  ...` (no `⏺`)
- `packages/core/src/screens/REPL.slashSuggestions.test.tsx`: duplicate command selection / `preferredSlashSpecId`

## High-Signal Patterns

- Pattern A: one-line overlay dismissal
  - append a single assistant `Msg` with `ui.kind='command_subline'`
  - keep copy stable unless the user explicitly requests copy changes
- Pattern B: multi-line local output
  - split output into multiple `command_subline` rows
  - this is UI only; model injection remains separately controlled
- Pattern C: inject-but-don't-spam
  - when a command needs to inform the model, keep UI output minimal and preserve `recordForNextTurn` / injected-block behavior separately

## Minimal Workflow

1. Classify the change first: discovery / precedence, local UI output, next-turn injection, or overlay dismiss behavior.
2. Update the slash command contract first.
3. Preserve “show in UI” vs “inject into model context” as separate concerns; local output alone must not imply injection.
4. Use `command_subline` for Claude-style sublines; do not invent new message shapes.
5. Run the minimum regression set below before review.

## Minimum Regression

- `bun run test -- packages/core/src/features/commands/registry.test.ts packages/core/src/features/commands/CommandStore.test.ts packages/core/src/features/commands/adapter.test.ts packages/core/src/features/commands/contracts.test.ts`
- `bun run test -- packages/core/src/features/repl/controller/ui/overlays.test.tsx`
- `bun run test -- packages/core/src/features/repl/controller/send/send.test.ts packages/core/src/features/repl/useReplController.test.tsx`
- `bun run test -- packages/core/src/screens/REPL.slashSuggestions.test.tsx packages/core/src/screens/repl/inputHint.test.ts`
- `bun run type-check` when command shapes or routing plumbing changes

## Guardrails

- Do not add bespoke `commandSubLines`-style structures; use `Msg.ui.kind='command_subline'`.
- Do not change UI copy / spacing / colors as a side-effect of routing changes.
- Do not patch only overlay output if the real bug is discovery or dispatch precedence.
- If behavior is unclear, add or extend an Ink test first; tests are not the only spec, but they should lock the visible key path.
