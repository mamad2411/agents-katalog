---
name: add-api-route
description: Add a new JobPilot API route or module the standard way - contracts schema, controller, service, response schema, optional web hook. Use for "add an endpoint", "new route", "new module".
---

# Add an API route

Follow the conventions in `.claude/rules/api.md` (response schemas, `z.date()`, global error
envelope). Steps:

1. Request schema: reuse or add in `packages/contracts` (or the module's `<name>.schema.ts`).
   Uuid path ids via `idParam`.
2. Response schema: model the service's return **exactly** in `<name>.schema.ts`, or use a
   shared envelope from `@/types/response`. Elysia strips fields not in the schema.
3. Route: in `modules/<name>/<name>.controller.ts`, add `body`/`query`/`params` as needed, the
   `response` success schema, a `detail` summary, and a `rateLimit(policy)` `beforeHandle`
   where the endpoint warrants one. No per-route error responses - they're declared globally.
4. Logic in `<name>.service.ts` (tsyringe `@singleton`; injected classes stay value imports).
   New module: mirror an existing one and mount its controller in `app.ts`.
5. Web side (if needed): Eden Treaty picks up types automatically; add query/mutation hooks
   under `apps/web/src/api/`.
6. Invoke the `verify` skill.
