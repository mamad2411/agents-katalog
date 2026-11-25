---
name: sveltekit-actions
description: Use when implementing or reviewing SvelteKit form actions including default and named actions, progressive enhancement with use:enhance, validation, and server-side mutation patterns.
---

# SvelteKit Actions

## Specialization

Expert guidance for SvelteKit form actions. Covers the `actions` export in `+page.server.ts`, default and named actions, `fail()` for validation errors, `redirect()` after success, `use:enhance` for progressive enhancement, and secure server-side mutation patterns.

## Trigger Conditions

- Implementing a form submission that mutates server state.
- Adding progressive enhancement to an existing HTML form.
- Returning validation errors and repopulating form fields without a full navigation.
- Deciding between form actions and a dedicated `+server.ts` endpoint.
- Diagnosing action routing mismatches or `use:enhance` callback behaviour.

## Scope Boundaries

In scope:

- `actions` export in `+page.server.ts`: `default` and named actions.
- `RequestEvent` fields inside actions: `request`, `params`, `locals`, `cookies`.
- `fail(status, data)` for returning validation errors with form state.
- `redirect(status, location)` for post-action redirects.
- `use:enhance` directive: default behaviour and custom callback override.
- `$page.form` and `$page.status` for reactive access to action results.
- CSRF protection defaults and when to assert `origin`.
- File upload handling via `request.formData()`.

Out of scope:

- Load functions (covered by `sveltekit-load`).
- REST-style `+server.ts` handlers (separate concern, not form actions).
- Client-side form library integration (out of SvelteKit core scope).
- Page rendering options (covered by `sveltekit-page-options`).

## Inputs

- Form fields and their validation rules.
- Mutation target (database record, session, external API).
- Progressive enhancement requirements.
- Success and error redirect / response requirements.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Action implementation | `actions` export in `+page.server.ts` with correct `RequestEvent` handling |
| Validation response | `fail()` calls with typed data; form errors surfaced in component |
| Progressive enhancement | `use:enhance` applied; custom callback documented where needed |
| Post-action navigation | `redirect()` or form result display pattern implemented |
| Actions quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Submit a form and handle the result on the server | Single default action processes a form and redirects |
| L2 Practical Delivery | Multi-action form with validation errors and progressive enhancement | Named actions, `fail()`, and `use:enhance` all work correctly |
| L3 Specialist Hardening | Secure, resilient actions with file upload and rate-aware mutation | CSRF origin check, file validation, and mutation idempotency documented |
| L4 Expert Standardisation | Define reusable action and validation patterns for a project | Action conventions, `fail()` type registry, and `use:enhance` policy documented |

## Workflow

1. Define the action name: use `default` for single-action pages, named actions for multi-action pages.
2. Parse `request.formData()` to extract field values; type and validate each field before use.
3. Apply business logic or mutation; wrap in try/catch to handle unexpected failures.
4. Return `fail(status, { field errors })` for validation failures; include original values for field repopulation.
5. Return `redirect(303, '/path')` after a successful mutation to implement the POST-Redirect-GET pattern.
6. In `+page.svelte`, access `$page.form` for action result data and render inline errors.
7. Add `use:enhance` to the `<form>` element for progressive enhancement; override the callback only when custom success/error behaviour is required.
8. When using named actions, set `action="?/actionName"` on each `<form>`.
9. Validate file uploads: check MIME type, size limit, and extension before processing.
10. Run the actions quality checklist.

## Actions Quality Checklist

- [ ] `request.formData()` is the only source of form values; query params are not used for mutations.
- [ ] Every field is validated before use; `fail()` returned for invalid input.
- [ ] `fail()` includes enough data to repopulate the form without a reload.
- [ ] Successful mutations always redirect (POST-Redirect-GET pattern).
- [ ] `use:enhance` is applied to all forms that should work without JavaScript.
- [ ] Custom `use:enhance` callbacks call `update()` unless full control of the result is intended.
- [ ] Named actions use `?/actionName` not bare `?actionName` in `action` attributes.
- [ ] File uploads validate MIME type, extension, and size before processing.
- [ ] No secrets or tokens are returned in `fail()` or action return data.
- [ ] `locals` is used to pass authenticated identity into action logic; cookies are not re-read directly.

## Security Notes

- SvelteKit provides CSRF protection by default; do not disable `checkOrigin` without explicit justification.
- Never trust form field values without server-side validation; client validation is advisory only.
- Limit file upload size in both the action and at the reverse-proxy layer.
- Do not expose internal error messages or stack traces in `fail()` response data.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Action definition | Workflow steps 1–3 |
| Validation and fail | Workflow step 4 + checklist |
| POST-Redirect-GET | Workflow step 5 |
| Form result display | Workflow step 6 |
| Progressive enhancement | Workflow step 7 |
| Named actions | Workflow step 8 |
| File upload safety | Workflow step 9 + Security Notes |
| Quality validation | Actions Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
