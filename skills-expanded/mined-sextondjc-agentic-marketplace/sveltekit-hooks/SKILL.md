---
name: sveltekit-hooks
description: Use when implementing or reviewing SvelteKit hooks including handle, handleError, handleFetch, sequence, and server versus universal hook files.
---

# SvelteKit Hooks

## Specialization

Expert guidance for SvelteKit hooks. Covers `hooks.server.ts` and `hooks.ts` (universal), the `handle`, `handleError`, and `handleFetch` functions, the `sequence()` composition helper, `locals` population, and the role of hooks in authentication, logging, and request transformation.

## Trigger Conditions

- Adding authentication or session checks to every request.
- Populating `event.locals` for downstream use in load functions and actions.
- Customising error responses or logging unexpected errors.
- Transforming outbound `fetch` calls made by SvelteKit internally.
- Composing multiple `handle` functions without nesting.
- Diagnosing request interception issues or missing `locals` values.

## Scope Boundaries

In scope:

- `hooks.server.ts`: `handle`, `handleError`, `handleFetch`.
- `hooks.ts` (universal): `handle`, `handleError` (runs on both server and client).
- `handle({ event, resolve })`: request interception, `locals` population, response transformation.
- `sequence(...handlers)`: composing multiple `handle` functions in order.
- `handleError({ error, event, status, message })`: typed error logging and custom error shape.
- `handleFetch({ event, request, fetch })`: intercepting SvelteKit internal fetch calls.
- `event.locals` typing via `App.Locals` interface augmentation.

Out of scope:

- Error page rendering (covered by `sveltekit-errors`).
- Adapter-level middleware (covered by `sveltekit-adapters`).
- Load function implementation (covered by `sveltekit-load`).
- Route-level access control beyond `locals`-based pattern (that is application logic, not hooks concern).

## Inputs

- Authentication and session strategy.
- `locals` fields required by load functions and actions.
- Error reporting target (logger, monitoring service).
- Outbound fetch transformation requirements.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| `handle` implementation | `hooks.server.ts` with session/auth logic populating `event.locals` |
| `App.Locals` type | Interface augmentation with all required fields |
| `handleError` implementation | Typed error handler with logging and safe client message |
| `sequence` composition | Multiple handlers composed without manual nesting |
| Hooks quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Populate `locals` for one field | `event.locals.user` available in load functions |
| L2 Practical Delivery | Auth session check, error logging, and multi-handler composition | `handle`, `handleError`, and `sequence` all working in one hooks file |
| L3 Specialist Hardening | Resilient hooks with safe error messages and fetch transformation | Error shape is client-safe; internal fetch calls are correctly transformed |
| L4 Expert Standardisation | Hooks conventions for a project | `locals` field registry, error shape contract, and handler ordering policy documented |

## Workflow

1. Create `src/hooks.server.ts`; add `src/hooks.ts` only when universal (client + server) hook logic is required.
2. Implement `handle` to intercept every request: validate session/auth token, populate `event.locals`, then call `resolve(event)`.
3. When multiple `handle` concerns exist (auth, logging, CSP headers), implement each as a named handler and compose with `sequence(auth, logging, csp)`.
4. Augment the `App.Locals` interface in `src/app.d.ts` with all fields populated in `handle`.
5. Implement `handleError` to log unexpected errors with full context; return a client-safe `message` that does not expose internal detail.
6. Use `handleFetch` only when SvelteKit's internal fetch calls must be intercepted (for example, injecting auth headers for internal API calls during SSR).
7. Verify that `event.locals` fields are available in load functions and actions.
8. Run the hooks quality checklist.

## Hooks Quality Checklist

- [ ] `handle` always calls `resolve(event)`; no request is silently dropped without a proper response.
- [ ] `event.locals` is the single source of runtime request state for load functions and actions.
- [ ] `App.Locals` interface is augmented; no untyped `any` on `locals`.
- [ ] Multiple `handle` concerns are composed with `sequence`, not nested manually.
- [ ] `handleError` never exposes raw stack traces, SQL detail, or secret values in the returned message.
- [ ] `handleError` logs full error context server-side for observability.
- [ ] `handleFetch` is used only for cross-cutting fetch transformation, not per-request business logic.
- [ ] Universal `hooks.ts` is used only for logic that must run on both server and client.

## Security Notes

- Validate session tokens and populate `locals.user` in `handle`; all downstream code should trust `locals`, not re-read cookies.
- Never return raw `error.message` from `handleError` to the client; fabricate a safe message and log internally.
- CSP and security headers are well-placed in a `handle` handler; prefer this over adapter-level config when logic is dynamic.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| `handle` implementation | Workflow steps 2–3 |
| `locals` typing | Workflow step 4 |
| `handleError` safety | Workflow step 5 + Security Notes |
| `handleFetch` use case | Workflow step 6 |
| Composition with `sequence` | Workflow step 3 |
| Quality validation | Hooks Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
