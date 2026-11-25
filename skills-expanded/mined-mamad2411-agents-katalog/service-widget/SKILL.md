---
name: service-widget
description: Service Widget-style HarmonyOS service widget and meta-service card builder. Use when creating, modifying, explaining, or debugging HarmonyOS service widgets/cards, widget layouts, card resources, widget configuration, form_config.json, widget names, card abilities, static resources, logic insertion, preview/save flows, or when the user mentions Service Widget, serviceWidget, ServiceWidget, meta service, 元服务卡片, 服务卡片, 万能卡片, or CodeGenie Service Widget.
---

# Service Widget

## Overview

Create or modify HarmonyOS service widgets and card-related project files. Focus on valid widget configuration, generated ArkTS/card code, resources, and safe insertion into the target project.

## Workflow

1. Locate the widget context.
   - Inspect module structure, existing card/widget files, `form_config.json`, resources, abilities, and build files.
   - Determine whether the request is for a new widget, a modification, generated code explanation, or debugging.

2. Define the widget contract.
   - Confirm widget size, name, target page/action, displayed data, refresh behavior, and resources.
   - Use a valid service widget name: start with a letter, use letters/digits/underscores, and keep it short enough for project conventions.
   - Check for name collisions before adding files.

3. Implement.
   - Follow existing card/module patterns and resource organization.
   - Add or modify widget layout code, logic code, static resources, and config together.
   - Keep generated code deterministic and easy to merge into the project.
   - Avoid hard-coded user-specific absolute paths.

4. Verify.
   - Validate JSON/JSON5 config syntax and file references.
   - Check resource paths, widget name consistency, and ability/config linkage.
   - Run the project’s available build/check command when practical.

## Widget Quality Rules

- Keep the widget glanceable. Prioritize one primary value or action.
- Design for the configured size. Do not assume a full app-page layout inside a widget.
- Ensure text handles truncation and localized length.
- Use existing resources and theme conventions where possible.
- Keep business logic separate from presentation when the project already separates them.

## References

Read `references/service-widget-checklist.md` when adding a widget, changing widget config/resources, or debugging save/preview/build issues.
