---
name: ui-view-states-forms
description: "Design UI hierarchy, forms, loading, empty, error, permission, and optimistic states."
---

# UI View States And Forms

Design the view around user decisions, data states, permissions and feedback, not only around the happy-path mockup.

## Process

1. Identify the primary user goal, most important information, main action, destructive actions, and what should be visible first.
2. Model all relevant states before coding: first load, background refetch, empty, partial, permission denied, validation error, server error, network error, rate limit, offline, readonly, disabled, stale data and deleted entity.
3. Keep loading states proportional; use cached data plus small refresh indicators when possible, and match skeleton dimensions to final layout.
4. Make empty states explain why there is no data and provide a next action when the user can act.
5. Make errors actionable and distinguish validation, system, auth, conflict, rate-limit and network failures.
6. For forms, provide labels, field-level errors, keyboard support, double-submit protection, focus after submit errors, and no data loss after API errors.
7. For tables and lists, show only decision-relevant fields, provide mobile-friendly alternatives, and avoid hiding task-critical data in truncation.
8. For optimistic UI, implement rollback and avoid it for destructive, financial, backend-rule-heavy or conflict-prone operations.

## Information Hierarchy

- The most important information should be visible without searching.
- The primary action should be easy to find.
- Destructive actions should be visually distinct from primary actions.
- Secondary information should not compete with the main task.
- Related controls should be grouped as one decision.
- Do not put important information only in a tooltip.
- Do not hide validation errors outside the visible form area.

## View States

Plan:

- first load;
- background refetch;
- optimistic update;
- empty data;
- partial data;
- permission denied;
- validation error;
- server error;
- network error;
- rate limit;
- offline/degraded connectivity;
- readonly;
- disabled due to business rules;
- stale data;
- deleted entity.

## Forms

- Every field has a label; placeholder is not a label.
- Errors are close to and associated with the field.
- Error copy tells the user what to fix.
- Frontend validation does not replace backend validation.
- Required and optional fields are distinguishable.
- Submit is safe against double click.
- After submit error, focus moves to the first invalid field or an error summary.
- Destructive actions require confirmation or undo when hard to reverse.
- Long forms are split into meaningful decision sections.
- Do not reset user input after an API error.

## Tables And Lists

- Desktop table does not have to remain a table on mobile.
- Columns should match user decisions, not all available data.
- Sorting, filtering and pagination follow existing app patterns.
- Row click and row actions must not conflict.
- Long text needs controlled wrapping or truncation.
- Truncation must not hide task-critical information.
- Large lists need pagination, cursoring, infinite scroll with keyboard fallback, or virtualization.

## API And Cache States

- Separate initial loading from background loading.
- Keep visible data during background refresh and show a smaller refresh signal.
- Cache keys must include tenant/user/locale where relevant.
- Realtime events should update cache through explicit mapping.
- UI should not require request waterfalls when API can provide the needed data.
- Cache must not hide missing permissions.

## Optimistic UI

Use optimistic UI when success is likely, rollback is simple, and the result can be predicted locally.

Avoid or add extra safeguards for financial, destructive, backend-rule-dependent, conflict-prone or hard-to-rollback operations.
