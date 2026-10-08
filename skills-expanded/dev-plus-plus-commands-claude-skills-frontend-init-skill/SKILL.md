---
name: frontend-init
description: "Initialize or refresh frontend component and template inventory using the dev++ workflow. Use when the user invokes /frontend-init or asks to scan frontend routes, pages, reusable UI, templates, state patterns, or frontend API clients."
---

# frontend-init

Initialize or refresh frontend inventory for the requested scope.

Use any text supplied after the slash command as the requested frontend path, route, feature, domain, or empty whole-frontend scope.

Rules:
- Scan routes, pages, shells, layouts, navigation, components, templates, forms, lists, dialogs, toasts, charts, states, style tokens, icon systems, i18n patterns, and frontend API clients.
- Identify reusable components, recurring UI patterns, and template candidates.
- Document loading, empty, error, disabled, permission, and conflict state patterns.
- Check how frontend API payloads and response usage map to backend contracts.
- Prefer existing docs. If none exist, propose `docs/ai-context/frontend/`.
- Do not edit files until the user explicitly approves the exact docs location and write plan.
- Output reusable assets found, template opportunities, gaps, risks, and questions.
