---
name: harmony-os-act
description: HarmonyOS Act-style coding agent for implementing, fixing, refactoring, and explaining HarmonyOS projects. Use when working on HarmonyOS/OpenHarmony, DevEco Studio, ArkTS, ArkUI, .ets files, hvigor builds, module.json5, app.json5, main_pages.json, oh-package.json5, service widgets, pages, abilities, permissions, lifecycle/state management, or when the user mentions harmony_os_act, HarmonyOS Act, 鸿蒙开发, ArkTS, ArkUI, DevEco, or CodeGenie Act.
---

# HarmonyOS Act

## Overview

Act as a HarmonyOS implementation agent: inspect the project first, make scoped code changes, and verify with the project’s own build or diagnostics. This is a Codex adaptation of the `harmony_os_act` workflow, focused on action and project edits rather than general Q&A.

## Operating Mode

- Prefer project evidence over generic memory. Read neighboring files, configs, imports, and existing patterns before changing code.
- Use ArkTS and ArkUI idioms when creating or modifying `.ets` code.
- Keep changes local to the requested behavior. Do not rewrite architecture unless the request requires it.
- Do not invent dependencies. Confirm library availability in `oh-package.json5`, `build-profile.json5`, imports, or nearby code.
- Preserve user changes and do not revert unrelated files.
- Use current official HarmonyOS documentation when API accuracy is uncertain or version-sensitive.

## Workflow

1. Identify the project shape.
   - Locate `module.json5`, `app.json5`, `build-profile.json5`, `hvigorfile.ts`, `oh-package.json5`, and `main_pages.json`.
   - Find the module and page/ability/component affected by the request.
   - Inspect adjacent ArkTS/ArkUI code for local component, state, naming, and styling conventions.

2. Plan the smallest coherent change.
   - State the files and behavior surface if the task is non-trivial.
   - Note HarmonyOS-specific implications: page route registration, permissions, ability metadata, lifecycle, state persistence, resources, and build configuration.

3. Implement with local conventions.
   - For UI, use existing ArkUI component patterns, decorators, resource references, and layout conventions.
   - For data/state, choose the narrowest existing state mechanism that fits (`@State`, `@Prop`, `@Link`, `@Provide`/`@Consume`, `Observed`, `AppStorage`, `PersistentStorage`, or project stores).
   - For system capabilities, update `module.json5` permissions or metadata only when the feature actually needs them.
   - When adding a page, update `main_pages.json` or the project’s equivalent route registry.

4. Verify.
   - Prefer the project’s existing build command or scripts. Do not assume a standard command until inspecting the repo.
   - If build is unavailable, run the most relevant static checks or targeted searches and report the limitation.
   - Re-check changed files for syntax, imports, route/config consistency, and accidental unrelated edits.

## Task Guidance

### Feature Work

- Confirm the target module and API level when relevant.
- Add only the resources, permissions, pages, or abilities that the feature needs.
- Keep UI responsive and accessible: avoid hard-coded one-screen assumptions, support text scaling where practical, and preserve focus/interaction expectations.

### Bug Fixes

- Reproduce or localize the failure from logs, compiler output, or the affected code path.
- Fix the root cause instead of masking errors.
- For cascaded build errors, address the earliest structural/type/import/config issue first.

### Refactors

- Keep public behavior unchanged unless the user asks otherwise.
- Update related types, route/config references, resources, and tests together.
- Avoid broad formatting churn in ArkTS files.

## HarmonyOS Rules Of Thumb

- `.ets` pages must be registered before navigation can reach them.
- Permissions belong in `module.json5` only when a HarmonyOS API requires them.
- Resource references should follow existing project usage instead of hard-coded strings/colors when the project already uses resources.
- Lifecycle-sensitive work belongs in `aboutToAppear`, `aboutToDisappear`, `onPageShow`, or `onPageHide` only when the component/page lifecycle actually requires it.
- Long lists should prefer lazy rendering patterns already present in the codebase.
- Build system changes should respect hvigor and module boundaries.

## References

Read `references/harmonyos-project-checklist.md` when the task touches project configuration, navigation, permissions, lifecycle, build setup, or when you need a compact checklist before editing.
