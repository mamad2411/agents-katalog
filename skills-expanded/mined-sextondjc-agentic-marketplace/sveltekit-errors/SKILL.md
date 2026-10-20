---
name: sveltekit-errors
description: Use when implementing or reviewing SvelteKit error handling including +error.svelte pages, the error helper, handleError hook, expected versus unexpected errors, and error boundaries.
---

# SvelteKit Errors

## Specialization

Expert guidance for SvelteKit error handling. Covers `+error.svelte` boundary pages, the `error()` helper for expected HTTP errors, `redirect()` as a non-error control flow mechanism, the `handleError` hook for unexpected errors, the distinction between expected and unexpected errors, and nested error boundary inheritance.

## Trigger Conditions

- Implementing a custom error page for a route or the whole application.
- Throwing typed HTTP errors from load functions or actions.
- Distinguishing expected errors (4xx) from unexpected errors (5xx) in responses.
- Configuring `handleError` to log unexpected errors with safe client messages.
- Diagnosing missing error pages or unhandled error propagation.

## Scope Boundaries

In scope:

- `+error.svelte`: the error boundary component for a route segment.
- `error(status, message)` from `@sveltejs/kit`: throws an expected HTTP error.
- `redirect(status, location)` from `@sveltejs/kit`: redirects as part of load or action control flow.
- `$page.error` and `$page.status`: reactive access to error data in `+error.svelte`.
- `handleError` in `hooks.server.ts`: intercepts unexpected errors; shapes the client-facing message.
- `App.Error` interface augmentation for typed error shapes.
- Nested `+error.svelte` boundaries and inheritance from parent layout error pages.
- The difference between `error()` (expected, typed, logged at info) and unexpected exceptions (caught by `handleError`, logged as errors).

Out of scope:

- Hook implementation beyond error handling (covered by `sveltekit-hooks`).
- Form action validation errors via `fail()` (covered by `sveltekit-actions`).
- Monitoring and alerting integration (application-level concern).

## Inputs

- Routes that need custom error page design.
- Expected error status codes and messages.
- Unexpected error logging and monitoring requirements.
- `App.Error` fields required beyond the default `message`.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| `+error.svelte` implementation | Error boundary component at the correct route level |
| `error()` usage | Correct `error()` throws in load functions and actions |
| `handleError` implementation | Safe client message returned; full error logged server-side |
| `App.Error` augmentation | Typed error shape in `src/app.d.ts` |
| Error handling checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Show a custom 404 page | Root `+error.svelte` renders for unknown routes |
| L2 Practical Delivery | Full error boundary hierarchy with typed errors and logging | Expected and unexpected errors handled; nested boundaries correct |
| L3 Specialist Hardening | Safe, observable error handling with typed `App.Error` | No internal detail in client messages; all unexpected errors logged with context |
| L4 Expert Standardisation | Error handling policy for a project | Status code map, `App.Error` schema, and boundary placement guide documented |

## Expected vs. Unexpected Errors

| Type | Source | Client Behaviour | Server Logging |
|---|---|---|---|
| Expected | `error(status, message)` thrown in load or action | Status and message shown; `+error.svelte` renders | Logged at info level |
| Unexpected | Unhandled exception reaching the framework | Generic safe message shown; `+error.svelte` renders | Logged at error level by `handleError` |
| Redirect | `redirect(status, location)` thrown | Browser follows redirect; no error page | Not logged as error |

## Workflow

1. Create a root `src/routes/+error.svelte` as the catch-all error boundary; display `$page.status` and `$page.error.message`.
2. Add nested `+error.svelte` files at route segments that need custom error treatment (for example, a dedicated 404 for the `/products` section).
3. In load functions and actions, throw `error(status, message)` for expected failure conditions (404 not found, 403 forbidden, 400 bad request).
4. Never throw raw `Error` instances for expected conditions; use `error()` so SvelteKit can distinguish them.
5. Augment `App.Error` in `src/app.d.ts` with any fields beyond `message` needed in `+error.svelte`.
6. Implement `handleError` in `hooks.server.ts`: log full error with context; return a client-safe `message` (and any additional `App.Error` fields).
7. In `+error.svelte`, access typed error data via `$page.error`; render status-appropriate UI.
8. Test each expected error code path in development; verify the correct `+error.svelte` boundary activates.
9. Run the error handling checklist.

## Error Handling Checklist

- [ ] A root `+error.svelte` exists to catch all unhandled errors.
- [ ] `error()` is used for all expected HTTP error conditions in load and actions.
- [ ] Raw `throw new Error(...)` is not used as a substitute for `error()` in expected failure paths.
- [ ] `handleError` never returns raw stack traces, SQL detail, or secrets in the client message.
- [ ] `App.Error` is augmented if `+error.svelte` needs fields beyond `message`.
- [ ] Nested `+error.svelte` boundaries are used only when section-specific error UI is required.
- [ ] `$page.status` is used to render status-appropriate error messages (404 vs. 500).
- [ ] All unexpected error paths are tested in staging; `handleError` logging verified.

## Security Notes

- Always return a generic, user-safe message from `handleError`; log full detail server-side only.
- Do not include database error messages, file paths, or user PII in client-facing error data.
- Use `error(403, 'Forbidden')` rather than exposing why access was denied (information leakage).

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Error page placement | Workflow steps 1–2 |
| Expected errors | Workflow steps 3–4 + Expected vs. Unexpected table |
| `handleError` safety | Workflow step 6 + Security Notes |
| `App.Error` typing | Workflow step 5 |
| Nested boundaries | Workflow step 2 |
| Quality validation | Error Handling Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
