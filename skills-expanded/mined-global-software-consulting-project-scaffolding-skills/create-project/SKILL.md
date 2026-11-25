---
name: create-project
description: Scaffold a new React (Vite), Next.js, or React Native project from scratch, then interactively add integrations. Always installs latest package versions.
---

# Create Project

You are a project scaffolding assistant. Your job is to create a fresh frontend project and then guide the user through adding integrations.

## Step 0 — Detect Environment

**Before asking anything**, check whether you are inside a Turborepo monorepo:

1. Look for `turbo.json` in the current directory or up to 3 parent directories
2. Also check for `package.json` with a `"workspaces"` field
3. Also check for an `apps/` directory alongside `packages/`

**If a monorepo is detected:**

Read the root `package.json` to get the monorepo name (from the `"name"` field).
List any existing apps in `apps/` so you can show the user what's already there.

Then ask:

> "You're inside the `<monorepo-name>` monorepo.
> Where do you want to create this project?
> A) Add as a new app in this monorepo (creates in `apps/<name>`, links shared packages)
> B) Create as a standalone project (creates in the current directory, independent)"

**If no monorepo is detected:** Skip this step entirely and proceed to Step 1 as normal.

**Store the result as `CONTEXT: monorepo | standalone`** — it affects Steps 3 and 4.

---

## Step 1 — Project Type

Ask the user (one question):

> "What type of project?
> A) React (Vite)
> B) Next.js
> C) React Native"

Wait for the answer before proceeding.

## Step 2 — Project Name

Ask:

> "What should the project be named?"

Use the name as-is (no spaces — remind user to use kebab-case if they use spaces).

## Step 3 — Create the Project

### If CONTEXT = monorepo:

Navigate into the `apps/` directory at the monorepo root first, then create the app there:

```bash
cd <monorepo-root>/apps
```

**Then create the app using the same commands as standalone (below), but from inside `apps/`.**

After creation, link the monorepo's shared packages by adding them to the new app's `package.json`:

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

> Skip `<monorepo-name>-ui` and `<monorepo-name>-theme` for React Native / Expo apps (web-only packages).

Then run `yarn install` from the **monorepo root** (not inside the app):
```bash
cd <monorepo-root>
yarn install
```

### If CONTEXT = standalone (or no monorepo):

Create in the current directory as normal.

---

### React (Vite):
```bash
yarn create vite <project-name> --template react-ts
cd <project-name>
yarn install
```

### Next.js:
```bash
npx create-next-app@latest <project-name> --typescript --eslint --app --src-dir --import-alias "@/*" --use-yarn
cd <project-name>
```

### React Native:

First ask:
> "Which setup would you prefer?
> A) Expo (recommended — managed workflow, easier setup, Expo Router)
> B) React Native CLI (bare, full native control)"

**If Expo:**
```bash
npx create-expo-app@latest <project-name> --template blank-typescript
cd <project-name>
```
Note: This installs with Expo SDK (latest). New Architecture is enabled by default in SDK 53+.

**If React Native CLI:**
```bash
npx @react-native-community/cli@latest init <ProjectName> --template react-native-template-typescript
cd <ProjectName>
```
Note: Project name must be PascalCase for CLI. New Architecture is mandatory in RN 0.82+.

After creation, tell the user which setup was chosen and any important notes.

## Step 4 — Initialize Git

### If CONTEXT = monorepo:

**Do NOT run `git init`** — the monorepo root already has a git repo.

Just stage and commit from the monorepo root:
```bash
cd <monorepo-root>
git add apps/<project-name>
git commit -m "feat: add <project-name> app to monorepo"
```

### If CONTEXT = standalone:

Run:
```bash
git init
git add .
git commit -m "chore: initial project scaffold"
```

(Skip `git init` if the project already has a repo — e.g., create-expo-app initializes one automatically.)

## Step 5 — App Type

Ask:

> "What kind of app is this?
> A) Dashboard / Admin app — data tables, auth required, lots of API calls
> B) Landing / Marketing site — public pages, contact forms, SEO important
> C) Consumer app — user-facing features, accounts, mixed content
> D) Not sure / General purpose"

Remember the answer — pass it into the setup flow so recommendations are tailored.

## Step 6 — Continue with Setup

Now follow the full `/setup-project` skill to walk the user through integrations.
The app type from Step 5 is already known — skip the app type question in setup-project and go straight to categories.

**The `/setup-project` skill automatically continues into scaffold-app at the end** — no separate command needed. The full flow (integrations → scaffold → extras → "All done") runs without any interruption.
