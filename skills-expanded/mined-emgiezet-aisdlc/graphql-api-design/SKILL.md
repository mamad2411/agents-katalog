---
name: graphql-api-design
description: >
  The design rules for a GraphQL schema an agent can follow unattended — nullability as a
  contract, mutation input and payload shape, Relay connections, resolver cost and the N+1
  trap, where a domain error belongs, and what counts as a breaking schema change. Use when
  adding or changing a type, field, query or mutation, reviewing a schema diff, writing a
  resolver, or judging whether a schema change is safe to ship.
---

# GraphQL API Design

GraphQL moves the query planner into the client, so every schema decision is a promise about
what is always present and what is always cheap. A field added without thinking about its
nullability and its resolver cost is a production incident with a graph shape.

This skill is the *what the schema must look like*. Server wiring and the project's
verification commands live in its `.claude/rules/` files and its `graphql-api` playbook.

## The schema is the contract

One schema, one source of truth. The schema change and the resolver that satisfies it land in
the same commit — a field that exists in SDL with no resolver is a runtime null, not a stub.
Schema-first and code-first are a per-project choice made once; mixing both in one service is
the defect, because the deployed schema then stops matching the file under review. Read the
existing schema before adding a type — a type duplicating an existing one under a new name is
the graph equivalent of a second error envelope.

## Nullability

Nullable means *this can legitimately be absent, or this resolver can fail without failing the
query*. Non-null means *a resolver failure here nulls the whole parent chain* — errors propagate
up to the nearest nullable ancestor.

| Field | Nullability | Why |
|---|---|---|
| Scalar owned by the entity (`id`, `createdAt`) | `String!` | It exists whenever the parent does |
| Value resolved across a service or network boundary | `T` | A downstream outage must degrade, not erase the query |
| Owned collection | `[T!]!` | "None" is an empty list; the container always resolves |
| Collection where absent ≠ empty | `[T!]` | Only when the client must tell the two apart |
| Anything | never `[T]!` | A non-null list of nullable elements is almost always an accident |

Optional input fields are how a mutation stays extensible: a new **required** input field breaks
every existing caller.

## Naming

Types `PascalCase`, fields and arguments `camelCase`, enum values `SCREAMING_SNAKE_CASE`.
Mutations are `verbNoun` — `archiveAccount`, never `accountArchive`, `doArchive` or `setStatus`.
Each mutation owns one `<Mutation>Input` and one `<Mutation>Payload`. Booleans read as
assertions: `isActive`, `hasPendingTransfer`, not `active` or `pendingTransferFlag`.

## Mutations

One mutation is one business operation. A generic `updateAccount(input: JSON)` pushes validation
and authorization into the client and cannot be reviewed.

- Exactly one argument, `input:`, of the mutation's own input type — this is what makes adding
  an argument later a non-breaking change.
- The payload type carries the mutated entity **plus** the typed domain-error union. Never a
  bare scalar, a bare `Boolean`, or the entity alone: a domain failure then has nowhere to go.

```graphql
type Mutation { archiveAccount(input: ArchiveAccountInput!): ArchiveAccountPayload! }
input ArchiveAccountInput { accountId: ID!, reason: String }
type ArchiveAccountPayload { account: Account, errors: [ArchiveAccountError!]! }
union ArchiveAccountError = AlreadyArchived | AccountNotFound | InsufficientPermission
```

## Errors

| Failure | Where it goes |
|---|---|
| Insufficient funds, already archived, validation rejection | Typed member of the payload union; resolver returns normally |
| Not found, for an entity the caller may ask about | Typed member of the payload union, or a nullable field |
| Unauthenticated, unauthorized | Top-level `errors[]`, `extensions.code` = `UNAUTHENTICATED` / `FORBIDDEN` |
| Malformed query, unknown field, bad variable | Top-level `errors[]`, `extensions.code` = `BAD_USER_INPUT` |
| Downstream outage, timeout, unhandled panic | Top-level `errors[]`, `extensions.code` = `INTERNAL_SERVER_ERROR` |

`extensions.code` is a stable machine token; once shipped it never changes meaning. Expected
domain failures never go in `errors[]` — being in the schema is what lets clients handle them
exhaustively. Never let a stack trace or an internal message reach `errors[].message`.

## Pagination

Every list field that can grow is a Relay connection: `first`/`after`, `edges { node cursor }`,
`pageInfo { hasNextPage endCursor }`.

- Bounded `first`, stated default and maximum: **default 20, maximum 100**, unless the project
  already uses other numbers. Above the maximum is a top-level error with
  `extensions.code = "BAD_USER_INPUT"`, never a silent clamp.
- A plain `[T!]!` field is allowed only for a set with a hard upper bound — a currency list, a
  status set — and the bound goes in the field description.

## Resolver cost

The N+1 trap separates a working GraphQL API from a usable one: one query over 100 parents
becomes 101 round trips the moment a child field resolves per parent.

- Every field resolving across a collection uses a per-request DataLoader, batching by key.
- A field resolver that opens a database connection or issues an HTTP call per parent is a
  `blocker`, not a performance note.
- The server enforces a query depth limit and a complexity/cost limit, both with stated numbers
  (depth 10, cost 1000 are reasonable starting points), rejecting with `BAD_USER_INPUT`.
- Never expose a field whose cost is unbounded in the number of parents or in recursion depth.

## Evolution

| Change | Breaking? |
|---|---|
| Adding a field, a type, or an optional input field | no |
| Removing or renaming any field, type or enum value | yes |
| Output field non-null → nullable | yes |
| Output field nullable → non-null | no |
| Input field optional → required | yes |
| Input field required → optional | no |
| Adding a value to an *input* enum | no |
| Adding a value to an *output* enum | yes for exhaustive clients |
| Changing a field's type | yes |

Removal is a two-step change: mark `@deprecated(reason: "…, use X")`, keep the field resolving
for the stated window, then remove it as a separate announced change. A breaking entry in CI's
schema diff is a blocker until that window is recorded.

## Non-negotiable

1. **Never remove or retype a published field** in place.
2. **Never return an expected domain failure in `errors[]`** — it belongs in the payload union.
3. **Never add an unbounded list field**; a growable list is a connection.
4. **Never resolve a cross-entity field without a DataLoader.**
5. **Never expose an internal error message** through `errors[].message`.

## Review checklist

- [ ] Every new field's nullability is justified by ownership or a boundary crossing; no `[T]!`
- [ ] Types, fields, enum values and the `verbNoun` mutation name follow the naming rules
- [ ] Mutation takes one `input:` argument and returns a payload with the entity and its errors
- [ ] Domain failures are typed union members; only protocol failures are in `errors[]`
- [ ] Growable list fields are connections with a bounded, non-clamping `first`
- [ ] Every cross-entity field batches through a DataLoader; depth and cost limits are set
- [ ] Nothing published was removed, renamed or retyped without `@deprecated` and a window
