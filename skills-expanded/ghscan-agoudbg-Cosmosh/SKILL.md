---
name: cosmosh-ui-patterns
description: Cosmosh renderer UI design and interaction workflow for implementing, refactoring, or reviewing React/Tailwind/Radix UI work in the Cosmosh Electron app. Use when touching packages/renderer UI, pages, layout, tabs, SSH terminal interactions, SFTP/browser-like workflows, settings surfaces, visual tokens, CSS/Tailwind classes, Radix wrappers, localization, or UI/UX documentation for Cosmosh.
---

# Cosmosh UI Patterns

Use this skill to keep Cosmosh UI work aligned with the product identity: a high-performance, high-information-density SSH/SFTP client for power users.

## Start Here

Before changing UI code:

1. Read `AGENTS.md`, `docs/README.md`, and `docs/developer/design/ui-ux-standards.md`.
2. Inspect the exact page/component being changed and at least one nearby established pattern.
3. Use `pnpm` for project commands and respect the existing package boundaries.
4. Keep implementation files, docs, and localization synchronized in the same task when behavior, UX standards, IPC, or runtime contracts change.

For detailed guidance, load only the reference you need:

- `references/design-system.md`: tokens, Tailwind, Radix wrappers, typography, density, icons, and styling rules.
- `references/interaction-workflows.md`: page workflows, tabs, SSH terminal interactions, settings, localization, docs sync, and validation.

## Default UI Workflow

1. Locate the feature owner.
   - Shared primitives: `packages/renderer/src/components/ui/*`.
   - Shared workbench layout: `packages/renderer/src/components/layout/*`.
   - App shell/tabs: `packages/renderer/src/App.tsx`, `packages/renderer/src/components/header/*`, `packages/renderer/src/lib/useTabs.ts`.
   - SSH terminal: `packages/renderer/src/pages/SSH.tsx`, `packages/renderer/src/pages/ssh/*`, `packages/renderer/src/components/terminal/*`.
   - Home/server organization: `packages/renderer/src/pages/Home.tsx`, `packages/renderer/src/components/home/*`.
   - Settings: `packages/renderer/src/pages/Settings.tsx`, `packages/renderer/src/pages/settings-registry.ts`.
2. Reuse an existing wrapper or style map before creating anything new.
3. Keep page code focused on feature state and composition; move reusable behavior into hooks or shared components when repetition becomes real.
4. Keep UI copy localized through renderer i18n helpers and resource files.
5. Validate loading, empty, disabled, error, hover, focus, active, and narrow viewport states.

## Hard Rules

- Do not introduce ad-hoc colors, shadows, blur, or radius values in feature code.
- Do not bypass Cosmosh UI wrappers with raw Radix primitives in pages.
- Do not use marketing-style landing-page layouts, low-density hero sections, or decorative UI that competes with terminal/server workflows.
- Do not remount runtime-heavy pages such as SSH/xterm sessions for visual-only state changes like tab reorder.
- Do not silently no-op unfinished actions; disable them with explicit feedback or present a clear coming-soon state.
- Do not change cross-process, IPC, backend runtime, persistent data, or security boundaries without an implementation brief and approval.

## Completion Checklist

Before finishing UI work:

1. Styling flows through tokens, CSS variables, Tailwind mappings, and wrappers.
2. Interactions are keyboard-accessible and preserve focus behavior.
3. Runtime-heavy views preserve state across tab order and layout-only changes.
4. UI strings are localized; user-visible copy is not hard-coded.
5. Required English and Chinese docs are synchronized when behavior or standards change.
6. Run targeted validation, normally `pnpm lint` and the relevant package/type/test command used by the repo.
