---
name: follow-service-instantdb
description: Install and use InstantDB as a real-time backend for frontend apps
argument-hint: "[scope]"
related:
  - follow-lib-react
  - follow-create-web
  - follow-lang-python
  - resolve-errors
  - update-references
  - suggest-next-action
  - use-scripts

---

## Goal

Install and use InstantDB as a real-time backend for frontend apps with schema, queries, transactions, auth, permissions, storage, and streams

## Scope

Used for:
- Creating or integrating InstantDB in a project with React, Next.js, SolidJS, Svelte, Vue, TanStack Start, or Python
- Defining schema, permissions, and client configuration
- Implementing real-time queries, transactions, auth, storage, presence, streams
- Using `instant-cli` for push/pull schema and managing apps

Not included:
- Creating UI components per framework (use `follow-lib-react`, `follow-create-web` (nextjs), etc.)
- Self-hosting (see official docs)

## Execute

### Workflows

> Goal: dispatch to the workflow matching the topic

- Setup: SDK install per framework, `instant-cli init`, db client → `workflows/setup-instantdb/SKILL.md`
- Config: `instant.schema.ts`, `instant.perms.ts`, env vars, push/pull → `workflows/config-instantdb/SKILL.md`
- Verify: app id valid, query responds, schema sync → `workflows/verify-connection/SKILL.md`

### 1. Detect Project

> Goal: Know the current framework and dependencies

1. Read `package.json` to identify the framework and package manager
2. Check whether the project uses `bun`, `npm`, `pnpm`, or `yarn`
3. If there is no `package.json` → stop and report

### 2. Install InstantDB

> Goal: Install the correct dependencies per framework

1. Install the client SDK per framework:
   - React: `bun add @instantdb/react`
   - Next.js: `bun add @instantdb/react`
   - SolidJS: `bun add @instantdb/solid`
   - Svelte: `bun add @instantdb/svelte`
   - Vue: `bun add @instantdb/vue`
   - TanStack Start: `bun add @instantdb/react`
   - Vanilla JS: `bun add @instantdb/core`
   - Python: `pip install instantdb` (used together with `follow-lang-python`)
Latest: `@instantdb/react@1.0.67` (verified 2026-09-12); the CLI package is named `instant-cli` (not `@instantdb/cli`, which does not exist on npm)

2. Install the CLI for dev: `bun add -D instant-cli` or use `npx instant-cli@latest`
3. Confirm the dependencies are in `package.json`

### 3. Initialize App

> Goal: Create the starting schema, perms, and env config

1. Run `npx instant-cli@latest init` (or `bunx instant-cli init`)
2. Select an Instant app or create a new one via the CLI
3. Check that `instant.schema.ts`, `instant.perms.ts`, `.env.local` were created
4. Confirm `NEXT_PUBLIC_INSTANT_APP_ID` or `VITE_INSTANT_APP_ID` is set

### 4. Define Schema

> Goal: Create a correct, type-safe data model

1. Read [references/instantdb-api.md](references/instantdb-api.md) and [references/instantdb-configuration.md](references/instantdb-configuration.md)
2. Edit `instant.schema.ts` to add entities, fields, links, rooms
3. Use `i.entity({ ... })`, `i.string()`, `i.boolean()`, `i.date()` per the docs
4. Mark `unique`, `indexed`, `optional` as needed
5. Run `npx instant-cli@latest push schema` to push to production

### 5. Create Client

> Goal: Create a usable db client in the project

1. Create `src/lib/instant.ts` (or a path suited to the project):
   ```ts
   import { init } from "@instantdb/react";
   import schema from "../../instant.schema";
   export const db = init({
     appId: process.env.NEXT_PUBLIC_INSTANT_APP_ID!,
     schema,
     useDateObjects: true,
   });
   ```
2. Change `@instantdb/react` to match the framework in use
3. Never hardcode app IDs or secrets in source code

### 6. Query And Transact

> Goal: Read and write data in real time

1. Use `db.useQuery({ todos: {} })` to read real-time data
2. Use `db.transact(db.tx.todos[id()].update({ ... }))` to write
3. Use `db.tx.<entity>[id()].delete()` for delete
4. Handle `isLoading`, `error`, `data` from `useQuery`
5. See more patterns in [references/instantdb-api.md](references/instantdb-api.md)

### 7. Setup Auth And Permissions

> Goal: Protect data with auth and rules

1. If using built-in auth: read [references/instantdb-configuration.md](references/instantdb-configuration.md) about magic codes and OAuth
2. Configure `instant.perms.ts` with `allow`/`bind` rules
3. Use `auth.id`, `auth.email` in permission rules
4. Run `npx instant-cli@latest push perms` when permissions change
5. If using Clerk/Firebase Auth → follow the official docs guides

### 8. Use Advanced Features

> Goal: Use InstantDB's extra features

1. Storage: use the `$files` entity and `db.storage.uploadFile`
2. Presence: use `db.rooms.usePresence`
3. Streams: use `db.rooms.useStream`
4. Admin HTTP API for server-side operations
5. If not used in this scope → skip this step

### 9. Validate

> Goal: Confirm the implementation works

1. Run `bunx tsc --noEmit` or `bun run build` to typecheck
2. Run the dev server and test real-time CRUD
3. Run `npx instant-cli@latest status` to check the app connection
4. If errors occur → do `resolve-errors` then revalidate

### 10. Update References

> Goal: Update references and summarize the next action

1. If links/rooms were added → update [references/instantdb-configuration.md](references/instantdb-configuration.md)
2. Do `update-references` for related skills
3. Do `suggest-next-action` to recommend the next step

## Rules

### 1. Source Of Truth
- Use official docs at `https://www.instantdb.com/docs` as the primary source
- If official docs conflict with training data → use the official docs
- Always state the installed version in `package.json`

### 2. Security
- Never hardcode `INSTANT_APP_ID`, API keys, or tokens in source code
- Use environment variables or a secret manager
- Define permissions before exposing sensitive data
- Never push schema/perms without reviewing a dry run

### 3. Type Safety
- Always use the `schema` parameter in `init({ schema })`
- Use generated types from `InstaQLEntity<typeof schema, "...">`
- Use `useDateObjects: true` when `Date` objects are wanted

### 4. Minimal Changes
- Do not rewrite the whole project just to integrate InstantDB
- Use the config files the project already has
- If more than 10 files must change → do `use-scripts`


## Expected Outcome

- Project has the InstantDB client installed per framework
- `instant.schema.ts` and `instant.perms.ts` are correct and pushed
- The `db` client is ready for queries and transactions
- Type-safe real-time CRUD works
- Auth and permissions defined per scope (if used)