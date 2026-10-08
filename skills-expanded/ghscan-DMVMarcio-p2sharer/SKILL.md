---
name: canonical-design
description: Enforces canonical component reuse, design system tokens, native host integration for mods/plugins, and backend utility centralization. Use this skill before creating or modifying visual components, game mods, or utility functions.
---

# Skill: Canonical Design & Code Reusability

## Scope
Enforces the "audit-before-creation" rule across user interfaces, host software extensions, and backend utilities.

## 1. Visual Interfaces (Web, Desktop, Mobile)
- **Prior Discovery**: Search the codebase for existing UI elements (buttons, dialogs, inputs, cards, tooltips) before authoring new ones.
- **Design Tokens**: Adhere strictly to defined color variables, spacing scales, typography standards, and transition constants.
- **Mandatory Componentization**: If a needed component does not exist:
  - Create it as a modular, parameter-driven, reusable unit in the project's canonical UI folder (`components/`, `views/common/`, `widgets/`).
  - Never write ad-hoc, throwaway visual primitives directly into feature screens.

## 2. Native Integration (Mods, Plugins, OS Utilities)
- **Authentic Integration**: Extensions and mods must blend seamlessly into the host environment.
- **Ban on Invasive Overlays**: Do not draw arbitrary floating windows or alien overlays unless explicitly demanded by the user.
- **Host System Hooks**: Prefer host application APIs, native menus, system dark/light mode hooks, and built-in dialog engines before crafting custom workarounds.

## 3. Backend, Core Logic & CLI Utilities
- **Centralized Helpers**: Do not implement duplicate helper functions (e.g., date formatters, sanitizers, serialization routines, HTTP clients) in local scopes.
- Search `utils/`, `helpers/`, `services/`, or `core/` first. Abstract any recurring logic into the canonical shared layer.