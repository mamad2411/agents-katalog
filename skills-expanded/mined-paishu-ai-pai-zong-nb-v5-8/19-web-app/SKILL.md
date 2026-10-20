---
name: web-app
description: Build and improve API-driven web applications, dashboards, admin panels, SaaS tools, and browser-based product UI. Use for routing, app shell, auth-gated pages, data views, tables, filters, forms, responsive layouts, and production web UX.
---

# Web App

## Workflow

1. Identify routing, app shell, auth model, API data model, and state management.
2. Build usable screens first, not marketing pages, unless the request is a landing page.
3. Handle data states: loading, empty, error, stale, retrying, saving, and permission-limited.
4. Keep filters, search, pagination, sorting, and table density ergonomic.
5. Verify layout at mobile and desktop widths.

## Required Checks

- Avoid oversized hero sections in operational software.
- Keep navigation predictable and current location clear.
- Make destructive actions confirmable and reversible where possible.
- Do not put business logic only in UI when it belongs in API/backend validation.
- Keep URL state for shareable filters or tabs when the product needs it.

## Output

Summarize user workflow, UI states covered, API assumptions, and verification.
