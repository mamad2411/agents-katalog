---
name: formax-tool-ui-blocks-workflow
description: Implement or refactor Formax tool transcript UI using the Tool UI Blocks (C-lite) pattern (ToolUiBlocks renderer + blocks presenters) to avoid touching many tool presenter files; use when adjusting ⏺/⎿ spacing, indent rules, or migrating additional tools to blocks presenters with targeted Ink/Vitest tests and Codex review before commit.
---

# Formax Tool UI Blocks (C-lite) Workflow

## Goal

Stabilize and evolve the tool transcript UI with **minimal churn**:

- Centralize common formatting (⏺ spacing, ⎿/indent rules) in one renderer.
- Keep per-tool custom UI possible, but avoid “change one space → edit 20 files”.
- Migrate tools incrementally (dual-track: legacy React presenter + blocks presenter).

## Scope / non-goals

- Do not redesign tool semantics (e.g. “Read+Edit => Update”) unless explicitly requested.
- Do not run `bun run test:coverage` for this workflow; only run tests for touched files.

## Current building blocks

- Renderer: `packages/core/src/components/tool/ToolUiBlocks.tsx`
- Block types: `packages/core/src/components/tool/toolUiBlocksTypes.ts`
- Dispatch: `packages/core/src/components/tool/ToolRouter.tsx`
- Presenter typing helpers: `packages/core/src/shared/toolPresenterContracts.ts`
- Shared primitives:
  - `packages/core/src/components/ui/PulsingDot.tsx`
  - `packages/core/src/components/tool/ToolHeaderLine.tsx`
  - `packages/core/src/components/tool/ToolSubline.tsx`
  - `packages/core/src/components/tool/toolUi.ts`

## Workflow (repeatable loop)

## Migration prioritization template

When deciding which tools to migrate next, use this ordering to minimize risk and maximize payoff:

1. **Simple + high frequency**: pure renderers with stable output and no React hooks (e.g. `read`, `grep`, `glob`).
2. **Simple + formatting sensitive**: tools whose transcript format is often tweaked (indent/spacing), and currently cause multi-file churn.
3. **Moderate complexity**: presenters that assemble multiple lines but still have no hooks (e.g. `webSearch`, `webFetch`), migrate only after 1–2 is stable.
4. **Do not migrate yet**: anything that needs hooks/interaction or complex previews (e.g. approval/policy overlays, edit/write patch previews). Keep as React presenters until they’re explicitly refactored into “data shaping” + “rendering”.

**Rule of thumb**: migrate **2–4 tools per commit** and keep each commit testable with 1–3 focused test files.

### 1) Lock the behavior with tests first

Add or update targeted tests before refactoring:

- For spacing/indent rules: `packages/core/src/components/tool/ToolUiBlocks.test.tsx`
- For dispatch rules (legacy vs blocks): `packages/core/src/components/tool/ToolRouter.test.tsx`
- For a migrated tool: its `packages/core/src/tools/modules/<name>/presenter.test.tsx`

Prefer assertions on **plain-text frames** (via `ink-testing-library`) that verify:

- `⏺` has exactly one trailing space (`⏺ Read`, not `⏺Read` or `⏺  Read`)
- Subline uses the Claude-style prefix and indent rules (e.g. `  ⎿  ` + following content)
- No “double indent” artifacts for sublines

### 2) Apply changes in the centralized layer

If the change is “global formatting”, change it in one of:

- `PulsingDot.tsx` for bullet spacing
- `ToolHeaderLine.tsx` for header composition (dot + label + params)
- `ToolSubline.tsx` / `packages/core/src/components/tool/toolUi.ts` for subline prefix + indentation
- `ToolUiBlocks.tsx` for block-to-UI mapping and composition

Do not change dozens of tool presenters for global spacing changes.

### 3) Migrate a tool to blocks presenter (optional, incremental)

Only migrate tools that are “simple UI” (no hooks, no interactive UI) first.

Steps:

1. In `packages/core/src/tools/modules/<name>/presenter.tsx`, switch to blocks presenter:
   - Return `{ blocks: ToolUiBlock[] }`
   - Wrap with `createToolBlocksPresenter(...)`
2. Keep legacy presenters untouched for other tools.
3. Update that tool’s `presenter.test.tsx` to render the blocks output through `<ToolUiBlocks />`.

### 4) Run only the relevant tests

Run Vitest for the touched files only. Example:

```bash
bun run test -- packages/core/src/components/tool/ToolUiBlocks.test.tsx
bun run test -- packages/core/src/components/tool/ToolRouter.test.tsx
bun run test -- packages/core/src/tools/modules/<name>/presenter.test.tsx
```

### 5) Run Codex review before committing

Follow `AGENTS.md` -> `Review Profile (Single Source of Truth)`.
Fix high/medium findings; only take low-risk low findings when low-churn.

### 6) Commit

Use a conventional message, e.g.:

- `refactor(tool-ui): migrate grep to blocks presenter`
- `fix(tool-ui): keep single space after bullet`

## Gotchas / guardrails

- **Case-insensitive filesystem collisions (macOS)**:
  - Avoid having both `ToolUiBlocks.*` and `toolUiBlocks.*` with similar names that can be confused by tooling.
  - Prefer a distinct type filename like `toolUiBlocksTypes.ts`.
- **Avoid hidden whitespace from JSX formatting**:
  - For spacing-sensitive UI, prefer composing the full string (`{`⏺ `}`) rather than placing newlines/indentation inside `<Text>...</Text>`.
- **Hooks rule**:
  - Blocks presenters are plain functions; they must not call React hooks.
  - If a tool presenter needs hooks, keep it as a React presenter and consider a later refactor to split “data shaping” from “rendering”.
