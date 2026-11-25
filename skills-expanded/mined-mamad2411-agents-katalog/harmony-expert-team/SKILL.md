---
name: harmony-expert-team
description: HarmonyOS expert-team workflow for project-aware HarmonyOS/OpenHarmony work. Use when the user wants a Harmony specialist group for ArkTS, ArkUI, DevEco Studio, hvigor builds, .ets pages/components, routing, module.json5/app.json5/main_pages.json, service widgets/cards, meta services, UI generation, debugging, refactoring, Q&A, or end-to-end Harmony app delivery. Coordinates harmony-os-ask, harmony-os-act, generate-ui-code, and service-widget.
metadata:
  short-description: HarmonyOS expert team router
---

# Harmony Expert Team

Use this skill as the expert-team entry point for HarmonyOS and OpenHarmony tasks. It coordinates the companion skills in this bundle instead of replacing them.

## Expert Roles

- `harmony-os-ask`: technical Q&A, concept explanation, API guidance, build-error diagnosis, and project-aware investigation when the user mainly wants an answer.
- `harmony-os-act`: implementation, bug fixing, refactoring, project wiring, route/config updates, permissions, lifecycle/state management, and build verification.
- `generate-ui-code`: ArkUI page/component generation from requirements, screenshots, sketches, design specs, or product flows.
- `service-widget`: HarmonyOS service widgets/cards, meta-service cards, `form_config.json`, card resources, widget names, save/preview flows, and widget debugging.

## Routing

Classify the task before acting:

1. Use `harmony-os-ask` when the user asks "why/how/what should I do", wants analysis, or asks about ArkTS/ArkUI/HarmonyOS concepts without asking for code edits.
2. Use `harmony-os-act` when the user asks to implement, fix, refactor, migrate, wire routing/config, handle permissions, or touch project files.
3. Use `generate-ui-code` when the main output is a HarmonyOS ArkUI page, component, `.ets` UI implementation, generated page from a screenshot, or UI-to-code workflow.
4. Use `service-widget` when the task mentions service widget, meta service, card, widget config, `form_config.json`, or card preview/save/build behavior.
5. For mixed tasks, run the flow in phases. Example: `harmony-os-ask` to diagnose, then `harmony-os-act` to fix, then `generate-ui-code` or `service-widget` for UI/card specifics.

## Project-First Workflow

When a task depends on a local HarmonyOS project:

1. Inspect the project shape before editing. Locate `module.json5`, `app.json5`, `build-profile.json5`, `hvigorfile.ts`, `oh-package.json5`, and `main_pages.json` when present.
2. Identify the affected module, page, ability, component, resources, route registry, permissions, and build scripts.
3. Read nearby `.ets` files and existing resource/style patterns before creating new code.
4. Prefer existing project conventions over generic examples.
5. Keep edits scoped to the requested behavior and preserve unrelated user changes.
6. Verify with the project’s available build/check command. If a build is not practical, run the best targeted static checks and explain the limit.

## Harmony Delivery Checklist

For implementation tasks, make sure the final work accounts for:

- ArkTS imports, decorators, state ownership, and component lifecycle.
- ArkUI layout, stable dimensions, long text, loading/empty/error/disabled states, and accessibility basics.
- Route registration in `main_pages.json` or the project’s route registry when adding a page.
- `module.json5` permissions or metadata only when the API actually requires them.
- Resource references for strings, colors, dimensions, media, and widget assets when the project uses resources.
- JSON/JSON5 syntax, file references, and hvigor/module boundaries.

## Output Style

- Be explicit about which expert path you selected and why.
- Separate confirmed project facts from assumptions.
- When editing files, summarize changed files, verification commands, and any remaining risks.
- When answering without edits, keep the answer concrete and Harmony-specific, with short ArkTS/ArkUI snippets only when useful.
