---
name: fynd-extension
description: |
  Guides development and debugging of Fynd extensions using the FDK (Fynd Development Kit)
  with Node.js and Express. Covers backend layout, webhooks, company-scoped config, error handling,
  frontend panel patterns, security, and common patterns for catalog, custom, and platform-scoped
  extensions. Use when working on any Fynd extension, FDK, Fynd Platform APIs, partner panel,
  extension webhooks, or @gofynd/fdk-extension-javascript.
---

# Fynd Extension (FDK) — Rules and context for the AI

When working on a Fynd extension codebase, follow these rules and use this context so your suggestions stay correct and consistent with FDK.

## Rules (always apply)

1. **Company context:** Every Fynd Platform API call must be scoped to a company. Obtain `companyId` from the request (`x-company-id` header, `company_id` in query/body, or your DB) and use `getPlatformClient(companyId)` — never call platform APIs without a company-scoped client.

2. **Route mount order:** Custom webhooks and extension API routes must be mounted **before** `fdkExtension.fdkHandler`. If you add a new route, place it before the FDK handler in the server file so it is not swallowed by the catch-all.

3. **Fynd API access:** Use only `fdkExtension.getPlatformClient(companyId)` to get a client for Fynd Platform APIs (catalog, order, application, etc.). Do not construct API clients manually.

4. **Webhook handler signature:** Handlers in `webhook_config.event_map` must use the signature `(event_name, request_body, company_id, application_id)`. Scope all DB writes and API calls using these arguments.

5. **Inbound webhooks:** POST routes receiving callbacks from external systems must be mounted before `fdkHandler`. Resolve `companyId` from the payload or DB before calling `getPlatformClient(companyId)`; return 4xx if unresolvable.

6. **Extension-owned entities:** When listing platform entities that belong to the extension (e.g. schemes, accounts), filter by `extension_id === process.env.EXTENSION_API_KEY`.

7. **Single backend entrypoint:** FDK is configured once in a single module (e.g. `backend/fdk.js`) via `setupFdk()`. The server imports this module and mounts `fdkHandler`, `platformApiRoutes`, `partnerApiRoutes`, and the webhook route. Do not duplicate setup.

8. **Application-scoped vs company-scoped APIs:** Use `platformClient.catalog.*` for company-wide operations (master catalog). Use `platformClient.application(applicationId).catalog.*` for storefront-specific data. Always resolve `application_id` from the request when using app-scoped APIs.

9. **Error responses:** Return consistent `{ message: string }` JSON for all errors. Handle `getPlatformClient` failures with 401. Validate required fields before processing. See [error-handling.md](references/error-handling.md).

## Common mistakes (avoid)

- **Forgetting `await`** on `getPlatformClient(companyId)` — it returns a Promise, not a client.
- **Storing business data in FDK session storage** — session storage is for OAuth tokens only. Use your own DB.
- **Hardcoding company IDs** — always read from the request.
- **Creating multiple FDK instances** — import the single module everywhere.
- **Mounting routes after `fdkHandler`** — they will never be reached.
- **Calling `getPlatformClient` in `callbacks.install`** — the token may not be stored yet.
- **Returning extension data without filtering** — always filter by `extension_id` before responding.
- **Throwing errors in webhook handlers** — catch internally; Fynd expects a timely 200.
- **Calling Fynd APIs from the frontend** — all platform calls go through the extension backend.

## Quick context

- **Package:** `@gofynd/fdk-extension-javascript` (Express: `@gofynd/fdk-extension-javascript/express`).
- **FDK exports:** `fdkHandler`, `getPlatformClient(companyId)`, `platformApiRoutes`, `partnerApiRoutes`, `webhookRegistry`.
- **Routers:** Platform routes under `/api`; partner routes under `/apipartner`; extension-specific routes under `/apibasic` or your own prefix.
- **Frontend panel:** Loaded in an iframe at `<BASE_URL>/company/:company_id`. Frontend calls extension backend with `x-company-id` header.
- **Env vars required:** `EXTENSION_API_KEY`, `EXTENSION_API_SECRET`, `EXTENSION_BASE_URL`, `FP_API_DOMAIN`.

## When adding or changing behavior

- **New API route:** Add a router, mount before `fdkHandler`; read `companyId`, call `getPlatformClient(companyId)`, wrap in try/catch. See [code-examples.md](references/code-examples.md).
- **New Fynd webhook:** Add event to `webhook_config.event_map` with `{ handler, version }`; implement handler with `(event_name, request_body, company_id, application_id)`.
- **New inbound webhook:** Add POST route before `fdkHandler`; verify signature if available; resolve `companyId`; call `getPlatformClient(companyId)`. See [security.md](references/security.md).
- **Frontend changes:** Extract `companyId` from URL path; pass `x-company-id` header on every backend call. See [frontend-panel.md](references/frontend-panel.md).
- **Extension-specific logic:** Attach to the appropriate router; filter platform results by `extension_id`.

## References (load when needed)

- [references/code-examples.md](references/code-examples.md) — Concrete code patterns for all common operations.
- [references/fdk-setup.md](references/fdk-setup.md) — FDK setup, env vars, route order, lifecycle callbacks.
- [references/webhooks.md](references/webhooks.md) — Webhook registration, handlers, and inbound webhook rules.
- [references/extension-patterns.md](references/extension-patterns.md) — Rules by extension type (catalog, platform-scoped, custom).
- [references/error-handling.md](references/error-handling.md) — Error response patterns, middleware, and wrappers.
- [references/frontend-panel.md](references/frontend-panel.md) — Extension panel UI, company context, API calls.
- [references/security.md](references/security.md) — HMAC verification, input validation, CORS, secrets.
