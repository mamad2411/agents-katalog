Add a new HTTP endpoint to the PollObject Durable Object.

The user will describe what the endpoint should do. Use $ARGUMENTS as the description.

Steps:
1. Read `src/durable-objects/poll-object.ts` in full to understand the existing SQL schema, helper methods, and routing pattern inside `fetch()`.
2. Read `src/types/slack.ts` to understand what data shapes are available.
3. Decide the HTTP method (GET for reads, POST for writes) and path (e.g. `/my-endpoint`).
4. Add the route inside the `switch` (or if/else chain) in `PollObject.fetch()`:
   - Parse the request body with `await req.json()` for POST, or `new URL(req.url).searchParams` for GET
   - Run SQL using `this.ctx.storage.sql.exec(...)` — use parameterized queries
   - Return `Response.json({ ... })` with the result
5. Update the caller in `src/index.ts` (or the relevant handler file) to call the new endpoint via `stub.fetch(new Request(...))`.
6. Add or update TypeScript types in `src/types/slack.ts` if new request/response shapes are needed.

Constraints:
- Always use parameterized SQL (never string interpolation) to avoid injection
- Keep SQL schema additions backward-compatible — add columns with `ALTER TABLE ... ADD COLUMN` if needed
- Return consistent JSON shapes: `{ ok: true, ...data }` on success, `{ ok: false, error: "..." }` on failure
- Use tabs for indentation, 140 char line width (Prettier config)

The endpoint to add: $ARGUMENTS
