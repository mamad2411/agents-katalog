---
name: aspire-tech-upgrade
description: >
  Migrates PHP/Laravel Lumen API endpoints from landau-api-main to Fastify 5 (TypeScript)
  in aspire-fastify. Use this skill whenever the user wants to migrate an API controller,
  route file, or endpoint group from the legacy PHP backend — e.g. "migrate category.php",
  "convert the classrooms controller", "port the auth routes to Fastify", or "which endpoints
  from X are used in the frontend and need migrating". Also trigger when the user references
  any controller or route file in landau-api-main and wants to bring it into aspire-fastify.
  Trigger even if the user just says "migrate [controller name]" without mentioning Fastify.
---

# aspire-tech-upgrade

Orchestrates the full migration of PHP/Lumen API endpoints from `landau-api-main` to
`aspire-fastify` (Fastify 5 + TypeScript).

**Two non-negotiable rules:**
- `landau-api-main` is **READ-ONLY** — never modify or suggest modifying it.
- This skill **does not write Fastify code itself** — code generation is delegated to
  `fastify5-agent-skill` in Step 4. Read `references/sub-skill-calling.md` before that step.

---

## Workflow

Work through these 7 steps in order. The user typically names a PHP controller or route file
(e.g. `category.php`, `ClassroomController.php`).

---

### Step 1 — Identify: filter to frontend-used endpoints

The goal here is to avoid migrating dead endpoints — only what `aspire-next` actually calls.

1. Read the PHP file the user named. It will be in one of:
   - `landau-api-main/app/Http/Controllers/` — controller with methods
   - `landau-api-main/routes/` — route definitions referencing controllers
   If the user gave a controller name, also check the routes file to find the mapped paths.

2. List every route defined (HTTP method + path).

3. Search `aspire-next/actions/` for each path. A path is "used" if any action file calls it
   via `apiFetch()`. Also cross-reference the API Endpoints Reference table in
   `aspire-next/CLAUDE.md` as a quick lookup.

4. **Filter to only used endpoints.** Silently drop the rest.

5. Present the filtered list to the user before proceeding:
   > "Found N endpoints in `[file]`. X are called from aspire-next — migrating those:
   > - GET /category
   > - GET /category/{slug}
   > ..."

   Wait for a thumbs-up or correction before moving to Step 2.

6. **Multi-prefix check:** If the filtered endpoints span more than one URL prefix
   (e.g. a classroom controller that also defines `/enroll/{otp}`), flag this to the user:
   > "These endpoints span two prefixes — `/classroom/` and `/enroll/`. I'll register them
   > as two separate plugins. Let me know if you want them split into separate files too."

7. **Batch size check:** If there are more than 6 endpoints, suggest splitting by logical
   sub-group rather than doing everything at once:
   > "There are 13 endpoints here. I recommend migrating them in two passes — tests first,
   > then homework — so each commit stays focused. Shall I start with tests?"

---

### Step 2 — Analyse each endpoint

Read the PHP controller method for each endpoint in your filtered list. Extract:

| Field | What to capture |
|-------|----------------|
| Method + path | e.g. `GET /category/{slug}` |
| Auth | Is this route behind `auth` middleware? Which guard? |
| Path params | Names, types, validation (e.g. `$slug` used as string) |
| Query params | Any `$request->get(...)` or `$request->query(...)` calls |
| Body fields | Any `$request->input(...)` or `$request->json()` calls |
| DB queries | What models/tables are queried, filters, joins, eager loads |
| Business logic | Transformations, conditionals, error conditions |
| Response shape | Exact fields returned — match these to aspire-next TypeScript types |

For each endpoint, also open the corresponding `aspire-next/actions/` file and check the
TypeScript return type. **The Fastify response shape must match that type exactly.**

---

### Step 3 — Write the Migration Brief

Fill in the template at `references/migration-brief-template.md`.

The Brief is the complete hand-off to `fastify5-agent-skill`. It must be detailed enough
that no further PHP reading is needed during code generation. Include one section per endpoint.

---

### Step 4 — Delegate to fastify5-agent-skill

Read `references/sub-skill-calling.md` now and follow those steps exactly.

Do not write any Fastify route, TypeBox schema, or Drizzle query yourself — that is
`fastify5-agent-skill`'s job. Your role here is to feed it the Migration Brief and
collect the generated files.

---

### Step 5 — Validate the output

Review every generated file against this checklist. Fix anything that fails before continuing.

**TypeBox** (see `references/typebox-patterns.md` for patterns)
- [ ] All `params`, `query`, `body`, `headers` have TypeBox schemas
- [ ] Response defined for each status code returned
- [ ] Types use `Static<typeof Schema>` — no hand-written duplicate types
- [ ] No `Type.Any()` used to dodge typing

**Swagger**
- [ ] Every route has a `schema` block with `tags`, `summary`, `description`
- [ ] Request schema (params/query/body) referenced in the schema block
- [ ] Response schema referenced for each status code

**i18n**
- [ ] Every user-facing string goes through `i18next` — no hardcoded English in responses
- [ ] New i18n keys added to BOTH `src/i18n/locales/en/translation.json` AND `az/translation.json`

**Database**
- [ ] All DB access uses Drizzle ORM — no raw SQL strings
- [ ] Models imported from `src/models/`

**Auth**
- [ ] Routes behind PHP `auth` middleware have JWT verification in the Fastify handler
- [ ] `landau-token` header check is already global (handled by `aspireToken` plugin) — don't re-implement it

**Response shapes**
- [ ] Field names and types exactly match the TypeScript types in `aspire-next/actions/`
- [ ] No extra fields, no missing fields

See `references/project-structure.md` for where each new file should be placed.

---

### Step 6 — Register the route plugin

Find where existing routes are registered in `aspire-fastify/src/server.ts` (or `app.ts`)
and add the new plugin with the correct prefix:

```ts
await app.register(import('./routes/category'), { prefix: '/category' });
```

The prefix must match the base path used in `aspire-next/actions/`.

---

### Step 7 — Commit

Once all endpoints pass the checklist:

```
feat(aspire-fastify): migrate <domain> endpoints from landau-api

- Implemented: <METHOD /path, METHOD /path, ...>
- TypeBox validation: request + response
- Swagger docs added
- i18n messages: en, az
```

---

## Reference files

| File | Read at step |
|------|-------------|
| `references/sub-skill-calling.md` | Step 4 — how to invoke fastify5-agent-skill |
| `references/migration-brief-template.md` | Step 3 — fill this in for hand-off |
| `references/typebox-patterns.md` | Step 5 — TypeBox patterns and review checklist |
| `references/project-structure.md` | Steps 5 & 6 — file placement in aspire-fastify |
