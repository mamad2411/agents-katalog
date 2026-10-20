---
name: rest-graphql-contract
description: Designs and builds REST and GraphQL API contracts (resources/schema, versioning, pagination, errors, status codes, OpenAPI/SDL) when implementing a new endpoint or service surface for clients.
when_to_use: User is building or evolving a REST endpoint or GraphQL schema, adding versioning/pagination/error formats, or writing OpenAPI/SDL. This is building the contract; reviewing an existing API design diff is api-design-review.
---

## When to Use

Building or evolving a client-facing API surface where the **contract** is the deliverable:

- New REST endpoint(s) or a new GraphQL schema/type/query/mutation.
- Adding pagination, filtering, sorting, versioning, or an error format to an existing surface.
- Writing or extending OpenAPI (`openapi.yaml`) or GraphQL SDL (`schema.graphql`).

Not this skill: reviewing a diff of an already-designed API (use `api-design-review`), or pure internal-only RPC with no external clients.

**Pick REST vs GraphQL first:** REST for resource-shaped CRUD, file/binary, CDN-cacheable reads, and webhook/callback surfaces. GraphQL when clients need to compose nested data from one round-trip and field sets vary per screen. Don't run both for the same data unless a client genuinely needs each.

## Steps

1. **Inventory before designing.** Grep the repo for an existing spec (`openapi*.{yaml,json}`, `*.graphql`, `schema.gql`) and existing route/resolver files. Match their conventions (casing, error shape, envelope) instead of inventing a parallel style. Note the framework (Express/Fastify/Nest, Apollo/graphql-yoga, etc.) — the contract artifact format follows it.

2. **Model the surface.**
   - REST: nouns + plural collections (`/orders`, `/orders/{id}/items`). Verbs live in HTTP methods, not paths — no `/getOrder`, `/createOrder`. Sub-resources max ~2 levels deep; beyond that, flatten with query params. Use `kebab-case` or lowercase paths, but field names match the codebase JSON convention (usually `camelCase`).
   - GraphQL: object types + `Query`/`Mutation`/`Subscription` roots. Mutations are verbs (`createOrder`), one input object arg (`input: CreateOrderInput!`) and a payload type return (`CreateOrderPayload`) so you can add fields/userErrors later without a breaking signature change. Avoid nullable list-of-nullable `[Order]` — prefer `[Order!]!` unless null elements are meaningful.

3. **Versioning + backward-compat.**
   - REST: version in the URL prefix (`/v1/...`) for the public major; reserve header/media-type versioning only if already in use. Additive changes (new optional field, new endpoint) = no bump. Removing/renaming a field or changing its type/required-ness = breaking → new major. Deprecate with `Deprecation`/`Sunset` headers before removal.
   - GraphQL: never version the endpoint. Add fields freely; deprecate with `@deprecated(reason: "use X")` and keep the old field resolving. Never remove an enum value or change a field's type/nullability in place.

4. **Pagination, filtering, sorting (pick one and document it).**
   - **Cursor** (default for feeds, large/mutating sets, GraphQL): opaque base64 cursor, `first`/`after` (and `last`/`before` if reverse needed). GraphQL → Relay Connections (`edges{node,cursor}`, `pageInfo{hasNextPage,endCursor}`). Never expose offset for infinite scroll — it skips/dupes rows on concurrent writes.
   - **Offset** (`page`/`pageSize` or `limit`/`offset`): only for small, stable, jump-to-page admin tables. Cap `pageSize` (e.g. ≤100) and reject above it — unbounded page size is a DoS vector.
   - Filtering: explicit query params (`status=open&minTotal=50`) or a typed `filter` input — never a raw query string clients build. Sorting: `sort=createdAt` / `sort=-createdAt` (leading `-` = desc), validate against an allowlist of sortable fields.

5. **Error model (decide before writing a single handler).**
   - REST: status codes carry meaning — `400` malformed, `401` unauthenticated, `403` authenticated-but-forbidden, `404` not found, `409` conflict/duplicate, `422` semantic validation fail, `429` rate-limited, `5xx` server. Body uses RFC 9457 `application/problem+json`: `{type, title, status, detail, instance}` plus a stable machine `code` and an `errors[]` array for per-field validation. One envelope shape for every error across the whole API.
   - GraphQL: HTTP is `200` even on logical errors. Use the `errors[]` array with a stable `extensions.code` (`UNAUTHENTICATED`, `FORBIDDEN`, `BAD_USER_INPUT`, `NOT_FOUND`). For *expected* domain failures (validation, business rules), return them as a typed `userErrors: [UserError!]!` field on the mutation payload — keep the top-level `errors` array for unexpected/system failures only.

6. **Avoid N+1 and over/under-fetching.**
   - GraphQL: every resolver that fetches a related entity per-parent goes through a DataLoader (batch + per-request cache). Add depth limiting and a query cost/complexity guard so a deeply nested query can't melt the DB. Don't resolve a list field with a `.map(async ...)` of single fetches.
   - REST: offer sparse fieldsets (`?fields=id,status,total`) and bounded expansion (`?expand=customer`) instead of either dumping every relation or forcing N follow-up calls.

7. **Idempotency + validation for writes.**
   - `POST` that creates = accept an `Idempotency-Key` header; store key→result and replay the same response on retry (network retries must not double-charge/double-create). `PUT`/`DELETE` are idempotent by definition — same request twice = same end state, `DELETE` on already-gone returns `204`/`404` consistently (pick one).
   - Validate request bodies against the schema *before* business logic (JSON Schema / zod / GraphQL input types). Validate your responses against the same contract in tests so the spec can't silently drift from the code.

8. **Emit the contract artifact + examples.** Produce the OpenAPI YAML or `.graphql` SDL as a real file in the repo, with at least one request/response example per operation (including an error example). Wire it so it's generated-from or validated-against the code, not hand-maintained in parallel.

## Common Errors

- **HTTP 200 with `{"error": ...}` in the body** (REST) — breaks every client's status-based handling and all middleware/retry logic. Use the real status code.
- **Offset pagination on a live feed** — page 2 silently skips or repeats rows when items are inserted/deleted between calls. Use cursors.
- **GraphQL N+1 from a naive resolver** — looks fine on 1 record, fires hundreds of queries on a list. Always DataLoader for child resolvers; verify by counting DB queries on a list query, not a single-item one.
- **Breaking change shipped as "additive"** — making a previously-optional field required, narrowing a type, or removing an enum value breaks existing clients even though you only "changed" something. Tightening is breaking; only loosening/adding is safe.
- **Unbounded list / no `pageSize` cap** — a client (or attacker) requests everything and OOMs the server. Always cap and reject over-limit.
- **Mutation returns the bare entity** (GraphQL) — you can't add `userErrors` or extra fields later without a breaking change. Return a payload wrapper type from day one.
- **Inconsistent error envelope** — `404` returns one shape, `422` another, GraphQL a third. Clients write three parsers and miss cases. One shape per protocol, everywhere.
- **Idempotency ignored on create** — a retried `POST` double-creates. If the operation has side effects, support `Idempotency-Key`.
- **Spec drifts from code** — hand-written OpenAPI that no longer matches handlers. Generate from code or contract-test the running server against the spec.

## Verify

- [ ] Contract artifact exists as a file (`openapi.yaml` / `schema.graphql`) and **lints clean** (`spectral lint`, `redocly lint`, or `graphql validate` / schema builds without error).
- [ ] Every operation has a request example, a success example, and at least one error example.
- [ ] Error shape is identical across all status codes (REST) / all `extensions.code`s present (GraphQL); validation errors are per-field.
- [ ] List endpoints/connections cap page size and the cap is enforced (request over the limit returns a 4xx / error, not a giant payload).
- [ ] A list GraphQL query is run and DB query count is O(1)-ish per relation, not O(n) (DataLoader confirmed); depth/cost limit rejects an over-deep query.
- [ ] A create operation replayed with the same `Idempotency-Key` returns the original result and creates only one record.
- [ ] Request and response bodies are validated against the schema in a test — sending a malformed body returns the documented `400`/`422`, and a response that violates the spec fails the test.
- [ ] Diff against the previous contract version is verified additive-only (no removed/renamed/retyped/newly-required field) unless a major version bump is intentional.
