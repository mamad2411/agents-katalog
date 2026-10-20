---
name: sveltekit-server-endpoints
description: Use when implementing or reviewing SvelteKit +server.ts API endpoints including HTTP verb handlers, JSON responses, streaming, content negotiation, and server-side REST patterns.
---

# SvelteKit Server Endpoints

## Specialization

Expert guidance for SvelteKit `+server.ts` API routes. Covers named HTTP verb exports (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), `json()` and `text()` response helpers, streaming with `ReadableStream`, content negotiation, error handling, CORS headers, and the decision matrix for endpoints vs. form actions vs. load functions.

## Trigger Conditions

- Implementing a REST-style API route within a SvelteKit application.
- Exposing data to an external client (mobile app, third-party consumer) through a SvelteKit endpoint.
- Building a webhook receiver that processes an incoming `POST` and returns a structured response.
- Deciding between `+server.ts`, a form action, or a server load function for a given request shape.
- Streaming large or progressive responses from a SvelteKit server route.
- Adding CORS headers to a SvelteKit API endpoint.

## Scope Boundaries

In scope:

- `+server.ts` file placement and route resolution rules.
- Named HTTP verb exports: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`, `HEAD`.
- `RequestEvent` fields: `request`, `params`, `url`, `locals`, `cookies`, `fetch`.
- `json(data, init?)` and `text(body, init?)` from `@sveltejs/kit` for typed responses.
- `error(status, message)` from `@sveltejs/kit` for error responses.
- Streaming responses via `ReadableStream` and `new Response()`.
- Content negotiation: checking `Accept` header, returning different formats from one handler.
- CORS: setting `Access-Control-Allow-Origin` and handling `OPTIONS` preflight.
- `fallthrough` for delegating to lower-priority handlers.
- Co-locating a `+server.ts` with a `+page.svelte` and the routing priority rules.

Out of scope:

- Form actions (`+page.server.ts` `actions` export) — covered by `sveltekit-actions`.
- Load functions — covered by `sveltekit-load`.
- Adapter-level edge function deployment — covered by `sveltekit-adapters`.
- Authentication and session management — covered by `sveltekit-auth`.

## Inputs

- HTTP method and request shape (URL params, query params, JSON body, or multipart).
- Response format (JSON, text, binary, stream).
- CORS and authentication requirements.
- Error response contract expected by consumers.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Endpoint implementation | Named verb exports in `+server.ts` with correct `RequestEvent` destructuring |
| Response construction | `json()` or `text()` usage with correct status and headers |
| Error handling | `error()` calls for expected failures; try/catch for unexpected failures |
| CORS configuration | `OPTIONS` handler and `Access-Control-*` headers when cross-origin access is required |
| Endpoints quality checklist | Pass/fail against the checklist below |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Return JSON from a `GET` handler | Single `GET` export returns `json(data)` with correct status |
| L2 Practical Delivery | Full CRUD endpoint set with typed request/response | All HTTP verbs implemented; `error()` used for all failure cases |
| L3 Specialist Hardening | Streaming, CORS, and content negotiation | `ReadableStream` works; CORS preflight handled; `Accept` header respected |
| L4 Expert Standardisation | Define reusable endpoint conventions for a project | Handler factory pattern, shared error translation, response type registry documented |

## Workflow

1. Place the `+server.ts` file at the route path matching the URL structure (e.g. `src/routes/api/users/[id]/+server.ts`).
2. Export a named async function for each HTTP verb the endpoint supports (`GET`, `POST`, etc.).
3. Destructure `RequestEvent`: extract `params`, `url.searchParams`, `request`, and `locals` only as needed.
4. Parse and validate the request body (`await request.json()` for JSON, `await request.formData()` for multipart); fail fast on invalid input using `error(400, message)`.
5. Execute business logic; call services or data layers through `locals` or imported server-only modules.
6. Return `json(data, { status })` for JSON responses or `new Response(stream, { headers })` for streaming.
7. Use `error(status, message)` from `@sveltejs/kit` for expected failures (404, 403, 422); let unexpected errors propagate to `handleError`.
8. For cross-origin use, add an `OPTIONS` export and return appropriate `Access-Control-*` headers in all verb handlers.
9. For content negotiation, inspect `request.headers.get('accept')` and branch to return the appropriate format.
10. Run the endpoints quality checklist.

## Endpoints Quality Checklist

- [ ] Every `+server.ts` exports only the HTTP verbs it supports; no unused verb stubs.
- [ ] Request body is parsed and fully validated before business logic executes.
- [ ] `json()` or `text()` from `@sveltejs/kit` is used instead of `new Response(JSON.stringify(...))`.
- [ ] `error(status, ...)` is used for all expected failure cases; status code matches the semantic failure type.
- [ ] No secrets, stack traces, or internal identifiers are returned in error response bodies.
- [ ] CORS headers are set explicitly; `Access-Control-Allow-Origin: *` is only used when public access is intentional.
- [ ] `OPTIONS` handler exists whenever CORS headers are required.
- [ ] Streaming responses use `ReadableStream` with a controller that properly closes or errors.
- [ ] Authenticated endpoints validate `locals` identity before executing any action.
- [ ] Route co-location with `+page.svelte` is intentional and the routing priority is documented.

## Security Notes

- Always validate and sanitize all inputs received in `request.json()` or `request.formData()` — endpoint handlers are public entry points.
- Do not access `$env/static/private` or private secrets in universal (non-server) code; server endpoints run on the server only but confirm imports are server-safe.
- Restrict `Access-Control-Allow-Origin` to known origins; wildcard CORS on endpoints that read `cookies` or `Authorization` is a security defect (CORS + credentials requires explicit origin).
- Rate-limit mutation endpoints (`POST`, `PUT`, `PATCH`, `DELETE`) at the infrastructure layer; do not rely solely on application-layer validation.
- Do not expose internal IDs, schema details, or error stacks in 4xx/5xx responses.

## L4 Coverage Matrix

| Requested Outcome | Skill Section |
|---|---|
| Endpoint file placement | Workflow step 1 |
| HTTP verb exports | Workflow step 2 |
| Request parsing and validation | Workflow steps 3–4 |
| Response construction | Workflow step 6 |
| Error handling | Workflow step 7 |
| CORS | Workflow step 8 |
| Content negotiation | Workflow step 9 |
| Security | Security Notes + checklist |
| Quality validation | Endpoints Quality Checklist |

## References

See [references/source-catalog.md](./references/source-catalog.md) for active source tracking.
