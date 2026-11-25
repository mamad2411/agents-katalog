---
name: brainstorm-architecture
description: "docs/plan/ARCHITECTURE.md: the stack and why, the folder layout, the modules and which agent owns each, how data flows through them, shared types and where they live, environment variables, integrations, deployment target, and the decisions with their reasons. Read when planning a new project or a change to how one is put together."
---

# ARCHITECTURE.md: how the project is put together

When four specialists build one project at once, each makes the choices
the others depend on: where shared types live, which folder is whose, how
the page gets its data, what the environment variables are called. Left
unwritten, the frontend reads `NEXT_PUBLIC_API_URL`, the backend serves on
a path nobody told it about, and two agents create `src/types.ts` and
`src/shared/types.ts`. This document fixes those choices once.

## 1. The template

```markdown
# Architecture

## Stack
| Layer | Choice | Why |
|---|---|---|
| Frontend | Next.js 15 (App Router), TypeScript, Tailwind | the user asked for Next |
| Backend | Next.js route handlers | one deployable; the API is small |
| Database | Postgres 16 with Drizzle | relational data (orders, items) |
| Hosting | <the user's: Coolify on their VPS> | |

## Layout
src/app/            pages and route handlers (fe: pages; be: src/app/api/**)
src/components/     shared UI components (fe, foundation wave)
src/server/         data access and business logic (be)
src/shared/types.ts types used by client and server (foundation; read-only after)
db/                 schema and migrations (db)
tests/              end-to-end tests (test)

## Modules
| Module | Owns | Owner |
|---|---|---|
| Catalogue | src/app/catalogue/**, src/server/products.ts | fe, be |

## Data flow
Browser → page (server component) → src/server/products.ts → Postgres.
Mutations: form → POST /api/cart/items → src/server/cart.ts → Postgres → revalidate /cart.

## Shared
- Types: src/shared/types.ts (Product, Cart, Order). Written in the foundation wave.
- Money: integer minor units with an ISO currency code.
- Dates: ISO 8601 in UTC on the wire; shown in the user's time zone.
- IDs: <uuid v7 | database serial>; slugs for public URLs.

## Environment
| Variable | Used by | Example |
|---|---|---|
| DATABASE_URL | server | postgres://… (never in the client) |

## Integrations
- <payments, email, storage: provider, what for, which module calls it>

## Decisions
- <date> Route handlers instead of a separate API service: one deploy, small API. Revisit if mobile clients come.
```

## 2. Choosing, and saying why

- **The stack is the user's** when they named one, and the project's when
  it exists: read `package.json`, `Cargo.toml`, `go.mod`,
  `pyproject.toml`, the framework config. A new project with no stated
  preference gets the plain default for its kind (a static site: plain
  HTML and CSS; an app with pages and data: the framework the project's
  language community uses most), named as a default in the Why column.
- **Why** is one short reason tied to the product, not a slogan.
- **Fewer moving parts** unless the product needs more: one deployable
  before two, the framework's own routes before a separate API service, a
  managed database before a self-run cluster. Say what would change the
  decision ("revisit if mobile clients come").

## 3. The layout is the ownership map

- Every folder in Layout names its owner, and those owners are the agents
  in `PLAN.md`. Two parts of one wave never own the same folder.
- Files everything imports (the router, root layout, shared types, the
  package manifest, the global stylesheet) belong to the foundation wave or
  to exactly one part, and are read-only for the rest.
- Keep the project's existing conventions in an existing codebase; the
  document describes them, it does not reorganise them.

## 4. The shared facts

The conventions every part must use the same way: money, dates, IDs,
errors, pagination, naming (`camelCase` in JSON, `snake_case` in SQL).
Write each once here; `API.md` and `ERD.md` follow them.

## 5. Decisions

A short log in the ADR spirit: the date, what was decided, why, and what
would reverse it. Read before revisiting a choice; add to it whenever the
user or a report changes one.

## Check it

- Every folder has one owner, matching `PLAN.md`.
- Shared types, money, dates and IDs are each defined once.
- Every environment variable is named, with who reads it and whether it is
  secret.
- Every stack choice has a reason; defaults are called defaults.

## Avoid

Stack choices the user did not make written as theirs; microservices for a
small product; two homes for shared types; environment variables named
differently by different parts; a layout that reorganises an existing
project; decisions without reasons.
