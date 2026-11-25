---
name: generate-claude-md
description: Generate a CLAUDE.md file for the current project. Claude Code reads this automatically at the start of every session — it captures the full stack, folder conventions, critical rules, and commands so Claude never needs to re-discover the project setup.
---

# Generate CLAUDE.md

You are generating a `CLAUDE.md` file for this project. Claude Code reads this file automatically
at the start of every conversation in this directory. The goal is a **concise, accurate,
always-current** context file so Claude understands the stack without reading source files.

**Run this:** after scaffolding a new project, OR on any existing project to create/refresh it.

---

## Step 1 — Detect Project Type and Stack

### 1a. Framework
Check the project root:
- `next.config.*` → **Next.js**
- `vite.config.*` → **React (Vite)**
- `app.json` with `"expo"` key → **React Native (Expo)**
- `android/` + `ios/` without expo → **React Native (CLI)**
- `src/main.ts` with `@nestjs/core` in `package.json` → **NestJS**
- `src/app.ts` + `express` in `package.json` (no nest) → **Express**

### 1b. Read `package.json` and build the full stack profile

```
FRAMEWORK:        next | vite | expo | rn-cli | express | nestjs
APP_TYPE:         dashboard | landing | consumer | general | api
PKG_MANAGER:      yarn | npm             (yarn.lock present → yarn)
NODE_VERSION:     from engines.node, default "20"

UI_LIBRARY:       heroui | shadcn | tailwind-only | none
STATE:            redux | zustand | none
ROUTER:           built-in(next) | react-router | tanstack-router | expo-router | react-navigation | none
HTTP:             tanstack-query+axios | rtk-query | apollo | axios | native-fetch | none
AUTH:             nextauth | jwt-custom | jwt-api | none
FORMS:            rhf+zod | rhf+yup | formik+yup | none
I18N:             next-intl | react-i18next | expo-i18n | none
ANIMATIONS:       motion | none
TOOLING:          husky+commitlint | none

[Node API only]
DATABASE:         prisma | drizzle | mongoose | none
QUEUES:           bullmq | none
DOCS:             swagger | none
VALIDATION:       zod | class-validator | none
```

**Detection map** (check `dependencies` + `devDependencies`):

| Package | Profile flag |
|---|---|
| `@heroui/react` | UI_LIBRARY: heroui |
| `@radix-ui/react-*` OR `components.json` file exists | UI_LIBRARY: shadcn |
| `tailwindcss` (without above) | UI_LIBRARY: tailwind-only |
| `@reduxjs/toolkit` | STATE: redux |
| `zustand` | STATE: zustand |
| `react-router-dom` | ROUTER: react-router |
| `@tanstack/react-router` | ROUTER: tanstack-router |
| `expo-router` | ROUTER: expo-router |
| `@react-navigation/native` | ROUTER: react-navigation |
| `@tanstack/react-query` | HTTP: tanstack-query+axios (if axios also present) |
| `@reduxjs/toolkit` + createApi detected | HTTP: rtk-query |
| `@apollo/client` | HTTP: apollo |
| `axios` (without tanstack-query) | HTTP: axios |
| `next-auth` | AUTH: nextauth |
| `jsonwebtoken` (in non-nest) | AUTH: jwt-custom |
| `react-hook-form` + `zod` | FORMS: rhf+zod |
| `react-hook-form` + `yup` | FORMS: rhf+yup |
| `formik` | FORMS: formik+yup |
| `next-intl` | I18N: next-intl |
| `react-i18next` | I18N: react-i18next |
| `expo-localization` + `i18next` | I18N: expo-i18n |
| `motion` | ANIMATIONS: motion |
| `husky` | TOOLING: husky+commitlint |
| `@prisma/client` | DATABASE: prisma |
| `drizzle-orm` | DATABASE: drizzle |
| `mongoose` | DATABASE: mongoose |
| `bullmq` | QUEUES: bullmq |
| `@nestjs/swagger` OR `swagger-ui-express` | DOCS: swagger |
| `class-validator` | VALIDATION: class-validator |

### 1c. Read `name` from `package.json` — use as the project name in CLAUDE.md

### 1d. App type
- Already known if coming from `scaffold-app` or `setup-project` flow
- If running standalone, check for clues:
  - `src/features/dashboard*` or `admin` → dashboard
  - `src/app/(marketing)` or landing-style pages → landing
  - Otherwise: ask "What kind of app is this? A) Dashboard B) Landing C) Consumer D) General / API"

---

## Step 2 — Read the Template

Read `~/.claude/project-scaffolding/reference/templates/CLAUDE.md.template` to understand all
possible sections and their inclusion conditions.

---

## Step 3 — Generate CLAUDE.md Content

Using the detected stack profile and the template as a blueprint, write a clean `CLAUDE.md`
that includes **only** the sections relevant to this project. Rules:

- **No placeholder text** — if a package isn't installed, omit its section entirely
- **No blank rows in tables** — only list packages that are actually installed
- **No redundant rules** — only include Critical Rules for packages that need special import/usage guidance
- **Exact project name** in the heading — use the `name` from `package.json`
- **Exact commands** — use `yarn` or `npm` based on detected package manager

### Section inclusion guide

| Section | Include when |
|---|---|
| Stack table | Always |
| Installed Packages table | Always |
| Folder Layout | Always — use the correct variant for framework |
| Critical Rules → next-intl | I18N: next-intl |
| Critical Rules → HeroUI | UI_LIBRARY: heroui |
| Critical Rules → Motion | ANIMATIONS: motion |
| Critical Rules → Redux | STATE: redux |
| Critical Rules → NextAuth | AUTH: nextauth |
| Critical Rules → Prisma | DATABASE: prisma |
| Code Patterns → API calls | HTTP is anything other than native-fetch |
| Code Patterns → Forms | FORMS is not none |
| Code Patterns → Translations | I18N is not none |
| Commands → docker + prisma | DATABASE: prisma or drizzle |
| Commands → swagger | DOCS: swagger |
| Dev Skills → /add-translation | I18N is not none |
| Dev Skills block | Always (all projects benefit) |

---

## Step 4 — Write the File

Write the generated content to `CLAUDE.md` in the project root.

If a `CLAUDE.md` already exists, read it first and check:
- If it was manually edited with custom notes, preserve those notes under a `## Project Notes` section at the bottom
- Regenerate all the auto-detected sections above it

---

## Step 5 — Commit

```bash
git add CLAUDE.md
git commit -m "chore: generate CLAUDE.md — project context for Claude Code"
```

If the file already existed:
```bash
git commit -m "chore: update CLAUDE.md — refresh stack context"
```

---

## Step 6 — Confirm

Tell the user:

> "Generated `CLAUDE.md` in the project root.
>
> Claude Code reads this automatically at the start of every session in this directory —
> no need to explain the stack each time.
>
> To keep it current: re-run `/generate-claude-md` after adding new packages."

---

## Rules

- Always use the real project name from `package.json` — never "my-project" or "your-project"
- Use `yarn` or `npm` consistently throughout — match what's detected, don't mix
- The CLAUDE.md must be human-readable too — use clean markdown, no tool output noise
- Keep it under ~150 lines — it's loaded into every conversation, concise wins
- For monorepos: generate one CLAUDE.md at the root. Add a `## Apps` section listing each app and its type. The folder layout section describes the monorepo structure. Per-app rules go under their own `### <app-name>` subsection.
