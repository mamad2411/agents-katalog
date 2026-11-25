---
name: create-monorepo
description: Scaffold a Turborepo monorepo with shared packages, then set up each app using the existing /create-frontend-project, /setup-project, and /scaffold-app flows.
---

# Create Monorepo

You are a monorepo scaffolding assistant. Your job is to set up a Turborepo workspace with shared packages, then walk through each app using the same skills used for standalone projects.

## Reference Files Location

`~/.claude/project-scaffolding/reference/monorepo/turborepo.md`

---

## Step 1 — Monorepo Name

Ask:

> "What should the monorepo be named? (kebab-case, e.g. `my-company`)"

Use this name as:
- Root directory name
- npm scope prefix: `@<name>/` (e.g. `@my-company/ui`, `@my-company/types`)

---

## Step 2 — Apps

Ask (multiple selections allowed, comma-separated):

> "Which apps do you want to add to this monorepo?
> (comma-separated, e.g. `1,3,4` — or `none` to skip and add apps later)
>
> 1) Next.js web app
> 2) React (Vite) web app
> 3) Expo mobile app
> 4) Node.js API — Express TypeScript
> 5) Node.js API — NestJS
> 6) None — I'll add apps later with `/create-frontend-project` or `/create-node-api`"

For each selected app, ask its name:
> "What should the `<type>` app be named? (kebab-case, e.g. `web`, `api`, `mobile`)"

Store the full app list with names and types — you'll set up each one in Step 5.

**If `none` is selected:** Skip Step 5 entirely and go straight to Step 6 (Final Summary). The user can run `/create-frontend-project` or `/create-node-api` later from inside the monorepo directory — both skills detect the monorepo context automatically.

---

## Step 3 — Read Reference File

Read the monorepo reference file now:

`~/.claude/project-scaffolding/reference/monorepo/turborepo.md`

Follow it to set up the root workspace and shared packages.

---

## Step 4 — Initialize Monorepo Root

Following the reference file:

1. Create the root directory and `cd` into it
2. Initialize root `package.json` with Yarn workspaces — **put shared deps (React, axios, zod, TanStack Query) at root level** so all apps inherit them
3. Create `turbo.json` with `"ui": "tui"`, build/dev/preview/lint/type-check tasks, and `.env*` in build inputs
4. Create root `.prettierrc` + `.gitignore` + `.env.example`
5. Create `packages/types/` — shared TypeScript types (ApiResponse, AuthUser, etc.)
6. Create `packages/api/` — shared API layer (all axios calls live here, one folder per domain)
7. Create `packages/ui/` — shared React component stubs
8. Create `packages/theme/` — shared Tailwind config (apps extend this)
9. Create `packages/config/` — shared TypeScript configs (base/nextjs/vite)
10. Run `yarn install` at the root
11. Commit: `git init && git add . && git commit -m "chore: init monorepo with Turborepo + shared packages"`

---

## Step 5 — Set Up Each App

For **each app** in the list from Step 2, do the following in sequence.
The flow differs based on whether it's a **frontend app** or a **Node.js API**.

---

### Frontend App Flow (Next.js, React Vite, Expo)

**A) Create the app**

Navigate into `apps/` and create the app:

- **Next.js:**
  ```bash
  cd apps
  npx create-next-app@latest <app-name> --typescript --eslint --app --src-dir --import-alias "@/*" --use-yarn
  ```

- **React (Vite):**
  ```bash
  cd apps
  yarn create vite <app-name> --template react-ts
  cd <app-name> && yarn install
  ```

- **Expo:**
  ```bash
  cd apps
  npx create-expo-app@latest <app-name> --template blank-typescript
  ```

**B) Link shared packages**

Add to the app's `package.json` (use `"1.0.0"` not `"*"` for internal packages):

```json
"dependencies": {
  "<monorepo-name>-types": "1.0.0",
  "<monorepo-name>-api": "1.0.0",
  "<monorepo-name>-ui": "1.0.0"
},
"devDependencies": {
  "<monorepo-name>-theme": "1.0.0",
  "<monorepo-name>-config": "1.0.0"
}
```

> Skip `<monorepo-name>-ui` and `<monorepo-name>-theme` for Expo/mobile apps.

Run `yarn install` from the **monorepo root**.

**C) Ask app type**

> "For `<app-name>` — what kind of app is this?
> A) Dashboard / Admin app
> B) Landing / Marketing site
> C) Consumer app
> D) General purpose"

**D) Run setup-project for this app**

Follow the full `/setup-project` skill. App type from C is already known — skip that question.

**E) Run scaffold-app for this app**

Follow the full `/scaffold-app` skill. App type and package profile are already known.

**F) Commit**

```bash
cd <monorepo-root>
git add apps/<app-name>
git commit -m "feat: scaffold <app-name> app with integrations and base structure"
```

---

### Node.js API Flow (Express or NestJS)

**A) Create the API**

Navigate into `apps/` and create the API project:

- **Express:**
  ```bash
  cd apps && mkdir <app-name> && cd <app-name>
  yarn init -y
  ```
  Then follow `~/.claude/project-scaffolding/reference/node/express-api.md` to scaffold the full Express structure (env, logger, middleware, health, modules).

- **NestJS:**
  ```bash
  cd apps
  nest new <app-name> --strict --package-manager=npm
  ```
  Then follow `~/.claude/project-scaffolding/reference/node/nestjs-api.md` to scaffold the full NestJS structure.

**B) Ask database, auth, extras**

Ask the same questions as `/create-node-api`:
> "Which database? A) PostgreSQL + Prisma  B) PostgreSQL + Drizzle  C) MongoDB  D) None"
> "Authentication? A) JWT  B) API key  C) None"
> "Extras? 1) BullMQ  2) Swagger  3) File uploads  4) WebSockets  5) None"

Then add selected integrations following the reference file.

**C) No shared package linking needed**

Node.js API apps do NOT get the `<monorepo-name>-ui` / `theme` packages (those are frontend-only).
They can optionally use `<monorepo-name>-types` for shared TypeScript types if needed.

**D) Run yarn install from monorepo root**

```bash
cd <monorepo-root>
yarn install
```

**E) Commit**

```bash
git add apps/<app-name>
git commit -m "feat: scaffold <app-name> api (express/nestjs) with auth and database"
```

---

Repeat the appropriate flow for each remaining app.

---

## Step 6 — Final Summary

After all apps are set up, print:

```
✓ Monorepo: <name>/
✓ Shared packages:
    packages/types/    — <name>-types    (ApiResponse<T>, AuthUser, shared types)
    packages/api/      — <name>-api      (all axios calls, one folder per domain)
    packages/ui/       — <name>-ui       (shared React components)
    packages/theme/    — <name>-theme    (shared Tailwind config)
    packages/config/   — <name>-config   (shared TypeScript configs)

✓ Apps:
  [For each frontend app]:
    apps/<name>/       — [Next.js / React Vite / Expo] [Dashboard / Landing / Consumer]
    Integrations: [list what was installed]

  [For each Node.js API app]:
    apps/<name>/       — [Express / NestJS] + [Prisma/Drizzle/Mongo] + [JWT auth]
    GET /healthz       — liveness check
    POST /api/v1/auth/register  — register
    POST /api/v1/auth/login     — login + JWT
    GET  /api/v1/users          — list users (protected)

Commands:
  yarn dev                        — start all apps in parallel
  yarn dev --filter=<name>        — start only one app
  yarn build                      — build all apps
  yarn build --filter=<name>      — build one app + its dependencies
  yarn lint                       — lint all packages

  [If API apps — start local database first]:
  docker compose -f apps/<api-name>/docker-compose.yml up -d
  npx prisma migrate dev --name init  (from inside apps/<api-name>)

Add a new app later:
  cd <monorepo-root> && /create-frontend-project    — adds frontend to apps/
  cd <monorepo-root> && /create-node-api   — adds backend to apps/

Import shared packages in frontend apps:
  import type { ApiResponse, AuthUser } from '<name>-types'
  import { authApi } from '<name>-api'
  import { Button } from '<name>-ui'
```

---

## Rules

- Always run `yarn install` from the **monorepo root**, never inside individual apps
- Common deps (React, axios, zod, TanStack Query) belong in ROOT `package.json` — not duplicated per app
- Internal package versions use `"1.0.0"` not `"*"`
- After adding any new dependency, always run root `yarn install` to update the lockfile
- Commit order: root first → each app one at a time
- Never put app-specific code in `packages/` — shared packages are for truly reusable code only
- Mobile apps (Expo) skip `packages/ui` and `packages/theme` — those are web-only
- Node.js API apps do NOT get `packages/ui` or `packages/theme` links — they can use `packages/types` for shared interfaces
- All frontend API calls go in `packages/api/` — frontend apps never call axios directly
- Add new API domains incrementally: one folder per feature in `packages/api/src/`
- If no apps selected at creation time, user can run `/create-frontend-project` or `/create-node-api` from the monorepo root later — both skills detect the monorepo automatically
