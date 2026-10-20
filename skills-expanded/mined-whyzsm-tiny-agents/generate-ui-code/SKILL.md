---
name: generate-ui-code
description: Generate UI Code-style HarmonyOS ArkUI page and component generator. Use when creating or modifying HarmonyOS UI from requirements, screenshots, sketches, descriptions, product flows, or design specs; when adding ArkTS .ets pages/components, resources, routing, tabs, lists, forms, cards, preview pages, or page-generation workflows; or when the user mentions Generate UI Code, page_generate, harmonyPage, Harmony Page, 生成页面, 生成UI代码, ArkUI page generation, or CodeGenie page generation.
---

# Generate UI Code

## Overview

Create or modify HarmonyOS ArkUI pages from UI requirements. Produce usable `.ets` code that fits the target project’s structure, routing, resources, and design conventions.

## Workflow

1. Understand the target.
   - Determine whether the user wants a new page, a component, or a modification to an existing screen.
   - Inspect nearby `.ets` files, resource usage, routing, and theme conventions.
   - For screenshots or vague specs, infer layout hierarchy, data states, controls, and interactions.

2. Design the ArkUI structure.
   - Choose existing project components before inventing new abstractions.
   - Map layout into ArkUI containers such as `Column`, `Row`, `Stack`, `List`, `Grid`, `Tabs`, and reusable components.
   - Define stable responsive dimensions and spacing. Avoid brittle absolute positioning unless the existing codebase requires it.

3. Implement.
   - Use ArkTS declarative UI idioms and existing imports/style patterns.
   - Use resources for strings/colors/dimensions/media when the project already does.
   - Include expected states: loading, empty, error, disabled, selected, and content overflow when applicable.
   - When adding a new page, register it in `main_pages.json` or the project’s route registry.

4. Verify.
   - Run the project’s build/check command when available.
   - Re-check imports, component decorators, route registration, resource references, and JSON5 syntax.
   - If visual verification is possible, inspect the rendered screen or preview; otherwise state the verification limit.

## UI Quality Rules

- Match the product domain. Operational tools should be dense and scannable; consumer pages can be more expressive.
- Keep text inside containers and support long labels.
- Use icons, toggles, segmented controls, sliders, tabs, menus, and form controls where the interaction calls for them.
- Prefer clear information hierarchy over decorative effects.
- Avoid one-note palettes and generic gradient-heavy pages.
- Respect HarmonyOS interaction expectations and accessibility basics.

## References

Read `references/arkui-page-generation-checklist.md` when generating a page from scratch, matching a screenshot, or touching navigation/resources.
