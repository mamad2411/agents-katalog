---
name: follow-service-instantdb-setup-instantdb
description: Install the InstantDB SDK per framework, run `instant-cli init` to link the app, and create the `db` client ready for query/transact — first-time setup only
related:
  - follow-service-instantdb
---

## Goal

Install the InstantDB SDK per framework, run `instant-cli init` to link the app, and create the `db` client ready for query/transact — first-time setup only

## Scope

- Install `@instantdb/<framework>` and `instant-cli`
- Create `instant.schema.ts`, `instant.perms.ts`, env app id
- Init the typed `db` client from env
- Does not cover detailed schema/permissions config → use `workflows/config-instantdb/SKILL.md`

## Execute

### 1. Detect Project

> Goal: Know the current framework and package manager

1. Read `package.json` to identify the framework (React, Next.js, SolidJS, Svelte, Vue, vanilla)
2. Identify the package manager (`bun`, `npm`, `pnpm`, `yarn`)
3. Check whether `instant.schema.ts` or `@instantdb/*` already exists → if so, skip to verify
4. If there is no `package.json` → stop and report

### 2. Install SDK And CLI

> Goal: Install the correct dependencies per framework

1. Install the client SDK per framework:
   - React/Next.js/TanStack Start: `bun add @instantdb/react`
   - SolidJS: `bun add @instantdb/solid`, Svelte: `bun add @instantdb/svelte`, Vue: `bun add @instantdb/vue`
   - Vanilla JS: `bun add @instantdb/core` — for other languages check official docs
2. Install the CLI with `bun add -D instant-cli` (the package is named `instant-cli`, not `@instantdb/cli`)
3. Confirm the dependencies are in `package.json`

### 3. Initialize App

> Goal: Link the Instant app and create config files

1. Run `npx instant-cli@latest init` (or `bunx instant-cli init`)
2. Pick an existing Instant app or create a new one via the CLI — if there is no account → stop and tell the user
3. Check that `instant.schema.ts`, `instant.perms.ts`, `.env.local` were created
4. Confirm the env app id is set — `NEXT_PUBLIC_INSTANT_APP_ID` or `VITE_INSTANT_APP_ID` per framework

### 4. Create Client And Verify

> Goal: Create the typed db client and smoke check it

1. Create `src/lib/instant.ts` (or a suitable path):
   ```ts
   import { init } from "@instantdb/react";
   import schema from "../../instant.schema";
   export const db = init({
     appId: process.env.NEXT_PUBLIC_INSTANT_APP_ID!,
     schema,
     useDateObjects: true,
   });
   ```
2. Change the import to match the framework in use — never hardcode the app id
3. Run the dev server and test basic `db.useQuery`
4. Do `/run-verify` — if it fails → `resolve-errors` max 3 rounds

## Rules

- Use official docs `https://www.instantdb.com/docs` as the primary source
- Never hardcode `INSTANT_APP_ID` or secrets in source code
- Always use the `schema` parameter in `init({ schema })` for type safety
- Do not rewrite the project — integrate into the existing structure
- When done, do `/suggest-next-action`

## Expected Outcome

- Framework SDK + `instant-cli` fully installed
- `instant.schema.ts`, `instant.perms.ts`, env app id created
- `db` client ready to use and query — verify passed
