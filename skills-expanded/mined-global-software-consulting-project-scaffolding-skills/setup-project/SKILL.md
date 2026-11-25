---
name: setup-project
description: Interactively add integrations to an existing React (Vite), Next.js, or React Native project. Presents options filtered by project type and installs latest versions.
---

# Setup Project

You are a project setup assistant. Walk the user through adding integrations to their project one category at a time.

## Reference Files Location

All integration guides live at: `~/.claude/project-scaffolding/reference/`

- React guides: `~/.claude/project-scaffolding/reference/react/`
- Next.js guides: `~/.claude/project-scaffolding/reference/nextjs/`
- React Native guides: `~/.claude/project-scaffolding/reference/react-native/`

When the user selects an integration, **read the relevant reference file** with the Read tool before executing any steps. Follow those instructions exactly.

---

## Step 1 — Detect Project Type

Check the current directory for:
- `next.config.*` → **Next.js**
- `vite.config.*` → **React (Vite)**
- `app.json` or `expo.json` with `expo` key → **React Native (Expo)**
- `android/` and `ios/` directories without expo → **React Native (CLI)**

If unclear, ask: "Is this a React (Vite), Next.js, or React Native project?"

For React Native also detect: "Is this an Expo project or bare React Native CLI?"

---

## Step 2 — App Type

Ask (one question):

> "What kind of app is this?
> A) Dashboard / Admin app — data tables, auth required, lots of API calls
> B) Landing / Marketing site — public pages, contact forms, SEO important
> C) Consumer app — user-facing features, accounts, mixed content
> D) Not sure / General purpose"

**Store the answer** — use it to mark recommendations in every category below.

### What changes per app type:

| Category | Dashboard | Landing Site | Consumer App |
|----------|-----------|--------------|--------------|
| State management | ✅ Recommended | ⚠️ Usually not needed | ✅ Recommended |
| Auth | ✅ Required | ⚠️ Rarely needed | ✅ Recommended |
| HTTP / Server state | ✅ TanStack Query | ⚠️ Axios only is enough | ✅ TanStack Query |
| Forms | ✅ Needed for data entry | ✅ Contact / lead forms | ✅ Signup / profile forms |
| i18n | Optional | Optional | Optional |
| Routing | ✅ With protected routes | Basic pages only | ✅ With protected routes |

When presenting a category, add a one-line note like:
> _(Recommended for your Dashboard app)_ or _(Usually skipped for Landing sites)_

---

## Step 3 — Walk Through Categories

Present one category at a time. Wait for the user's answer before moving to the next.
Always show the app-type note before the options.

### React (Vite) Categories

---

**Category 1: UI Library**
> "Which UI library would you like to add?"
> A) HeroUI v3 + Tailwind v4
> B) shadcn/ui + Tailwind v4
> C) None (just Tailwind v4)
> D) Skip

Reference files:
- A → `reference/react/heroui-tailwind4.md`
- B → `reference/react/shadcn-tailwind4.md`
- C → `reference/react/tailwind4-only.md`

---

**Category 2: State Management**
> "Which state management would you like?"
> A) Redux Toolkit + redux-persist _(large apps, complex shared state)_
> B) Zustand _(simpler, great for most apps)_
> C) None
> D) Skip

App-type notes:
- Dashboard → "Recommended — you'll have shared UI state, user session, filters etc."
- Landing site → "Usually not needed for a landing site — consider skipping."
- Consumer / General → "Recommended if you have user accounts or shared state."

Reference files:
- A → `reference/react/redux-toolkit.md`
- B → `reference/react/zustand.md`

---

**Category 3: Routing**
> "Which router would you like?"
> A) React Router v7 _(standard, includes ProtectedRoute pattern)_
> B) TanStack Router _(fully type-safe routes)_
> C) Skip

App-type notes:
- Dashboard → "Required — you'll need ProtectedRoute for authenticated pages."
- Landing site → "Basic routing only — React Router v7 is fine, or skip if single-page."

Reference files:
- A → `reference/react/react-router.md`
- B → `reference/react/tanstack-router.md`

---

**Category 4: Server State / HTTP**
> "How would you like to handle server state and HTTP requests?"
> A) RTK Query _(if you chose Redux Toolkit)_
> B) TanStack Query + Axios _(caching, loading states, refetching — REST)_
> C) Axios only _(simple REST requests, no caching layer)_
> D) Apollo Client _(GraphQL — queries, mutations, subscriptions)_
> E) Skip

App-type notes:
- Dashboard → "TanStack Query recommended for REST; Apollo Client if your API is GraphQL."
- Landing site → "Axios only is usually enough — just a contact form submission."
- Consumer → "TanStack Query (REST) or Apollo Client (GraphQL) recommended."

Reference files:
- A → `reference/react/rtk-query.md`
- B → `reference/react/tanstack-query.md`
- C → `reference/react/axios.md`
- D → `reference/react/graphql.md`

Note: Only show option A if user chose Redux Toolkit in Category 2.

---

**Category 5: Internationalization (i18n)**
> "Would you like to add multi-language support?"
> A) Yes — react-i18next _(supports RTL languages like Arabic)_
> B) No / Skip

Reference files:
- A → `reference/react/i18n.md`

---

**Category 6: Authentication**
> "Would you like to add a base authentication setup?"
> A) Yes — JWT pattern with ProtectedRoute
> B) No / Skip

App-type notes:
- Dashboard → "Required — users must log in to access the dashboard."
- Landing site → "Usually not needed — skip unless you have a members area."
- Consumer → "Recommended — user accounts are typical for consumer apps."

Reference files:
- A → `reference/react/auth.md`

---

**Category 7: Forms**
> "Would you like to add form handling?"
> A) React Hook Form + Zod _(recommended — best TypeScript inference, lightweight)_
> B) React Hook Form + Yup _(chainable schema API, drop-in swap for Zod)_
> C) Formik + Yup _(explicit component-based API, widely used)_
> D) No / Skip

App-type notes:
- Dashboard → "Recommended — data entry forms, filters, settings."
- Landing site → "Recommended — contact form, newsletter signup."
- Consumer → "Recommended — signup, profile edit forms."

Reference files:
- A → `reference/react/forms.md` (follow Option A section)
- B → `reference/react/forms.md` (follow Option B section)
- C → `reference/react/forms.md` (follow Option C section)

---

**Category 8: Animations**

> _Skip this entire category if app type is Dashboard / Admin — animations don't belong in admin UIs._

For Landing / Consumer / General apps only:

> "Would you like to add page animations?
> A) Yes — Motion (Framer Motion v11) — subtle entrance and scroll animations for landing pages
> B) No / Skip"

App-type notes:
- Landing site → "Recommended — hero fade-in, section scroll reveals, card stagger make the page feel polished."
- Consumer → "Optional — good for onboarding screens or marketing sections."
- Dashboard → _(Do not show this category)_

Reference files:
- A → `reference/react/motion.md`

Store result as `ANIMATIONS: motion | none` — scaffold-app uses this to decide whether to animate landing page components.

---

**Category 9: Code Quality Tooling**
> "Would you like to add code quality tools?"
> A) Yes — Husky + commitlint + ESLint config
> B) No / Skip

Reference files:
- A → `reference/react/tooling.md`

---

**Category 10: CI/CD Workflows**
> "Which GitHub Actions workflows would you like to add? (comma-separated, e.g. `1,3,4` or `none`)"
> 1) CI — lint + typecheck + build on every PR _(essential — highly recommended)_
> 2) Dependabot — automated weekly dependency updates _(simple, zero setup)_
> 3) Renovate — smarter dependency updates with automerge + grouping _(more powerful than Dependabot)_
> 4) Bundle size check — tracks JS bundle size delta on every PR
> 5) CodeQL — security scanning _(free for public repos)_
> 6) Semantic Release — auto-versioning + changelog from conventional commits
> 7) Lighthouse CI — performance audits on PRs _(landing pages only)_
> 8) None

> Note: Choose either Dependabot (2) OR Renovate (3) — not both.
> Lighthouse CI (7) is only useful if this is a landing/marketing site.

**Before creating any workflow file, detect project context by reading `package.json`:**

| What to detect | How | Stored as |
|---------------|-----|-----------|
| Package manager | `"packageManager"` field contains "yarn" OR `yarn.lock` exists | `PKG: yarn \| npm` |
| Node version | `"engines": { "node": ">=20" }` — extract major version, default `"20"` | `NODE: 20` |
| Test script | `scripts.test` exists and is not the default placeholder | `HAS_TESTS: true \| false` |
| Monorepo | `turbo.json` exists in root | `MONOREPO: true \| false` |
| App name | `name` field in `package.json` | used as `--filter` in turbo commands |

Apply these values when generating workflow YAML (substitute `cache:`, install command, run commands, and turbo commands accordingly).

Reference files:
- 1 → `reference/workflows/ci.md` (follow the detection + generation instructions in that file)
- 2 → `reference/workflows/dependabot.md`
- 3 → `reference/workflows/renovate.md`
- 4 → `reference/workflows/bundle-size.md` (follow Option A — size-limit for React Vite)
- 5 → `reference/workflows/codeql.md`
- 6 → `reference/workflows/semantic-release.md` (only if commitlint was installed in Category 9)
- 7 → `reference/workflows/lighthouse.md` (only if app type is Landing/Marketing)

For each selected workflow: create the relevant file(s) and commit with `chore: add <name> workflow`.

---

### Next.js Categories

---

**Category 1: UI Library**
> "Which UI library would you like to add?"
> A) HeroUI v3 + Tailwind v4
> B) shadcn/ui _(built-in with create-next-app)_
> C) None (just Tailwind v4)
> D) Skip

Reference files:
- A → `reference/nextjs/heroui-tailwind4.md`
- B → `reference/nextjs/shadcn.md`

---

**Category 2: State Management**
> "Which state management would you like?"
> A) Redux Toolkit + redux-persist
> B) Zustand _(recommended for Next.js — SSR-safe)_
> C) None
> D) Skip

App-type notes:
- Dashboard → "Recommended — shared state for filters, sidebar, user session."
- Landing site → "Usually not needed — Next.js Server Components handle most data needs."
- Consumer → "Recommended for user session and UI state."

Reference files:
- A → `reference/nextjs/redux-toolkit.md`
- B → `reference/nextjs/zustand.md`

---

**Category 3: Internationalization (i18n)**
> "Would you like to add multi-language support?"
> A) Yes — next-intl _(recommended for Next.js, supports App Router + RTL)_
> B) No / Skip

Reference files:
- A → `reference/nextjs/next-intl.md`

---

**Category 4: Authentication**
> "Would you like to add authentication?"
> A) NextAuth.js v5 / Auth.js _(OAuth, credentials, magic links)_
> B) Custom JWT pattern
> C) No / Skip

App-type notes:
- Dashboard → "Required — choose based on your auth provider."
- Landing site → "Usually not needed — skip unless you have a members area."
- Consumer → "Recommended — NextAuth.js handles most consumer auth patterns."

Reference files:
- A → `reference/nextjs/next-auth.md`
- B → `reference/nextjs/auth-custom.md`

---

**Category 5: Server State / HTTP**
> "How would you like to handle data fetching?"
> A) TanStack Query + Axios _(client-side, caching — REST)_
> B) Axios only _(REST)_
> C) Native fetch _(Next.js built-in — recommended for server components)_
> D) Apollo Client _(GraphQL — supports both Server and Client Components)_
> E) Skip

App-type notes:
- Dashboard → "TanStack Query for REST; Apollo Client if your API is GraphQL (supports RSC + client components)."
- Landing site → "Native fetch is enough — server components handle most content."
- Consumer → "Mix of native fetch (server) + TanStack Query or Apollo (interactive client parts)."

Reference files:
- A → `reference/nextjs/tanstack-query.md`
- B → `reference/nextjs/axios.md`
- D → `reference/nextjs/graphql.md`

---

**Category 6: Forms**
> "Would you like to add form handling?"
> A) React Hook Form + Zod _(recommended — best TypeScript inference, client components)_
> B) React Hook Form + Yup _(chainable schema API)_
> C) Formik + Yup _(explicit component-based API, client components)_
> D) No / Skip

App-type notes:
- Dashboard → "Recommended — data entry, settings, filters."
- Landing site → "Recommended — contact form, lead capture."

Reference files:
- A → `reference/nextjs/forms.md` (follow Option A section)
- B → `reference/nextjs/forms.md` (follow Option B section)
- C → `reference/nextjs/forms.md` (follow Option C section)

---

**Category 7: Animations**

> _Skip this entire category if app type is Dashboard / Admin — animations don't belong in admin UIs._

For Landing / Consumer / General apps only:

> "Would you like to add page animations?
> A) Yes — Motion (Framer Motion v11) — subtle entrance and scroll animations for landing pages
> B) No / Skip"

App-type notes:
- Landing site → "Recommended — hero fade-in, section scroll reveals, card stagger make the page feel polished."
- Consumer → "Optional — good for marketing/onboarding sections."
- Dashboard → _(Do not show this category)_

Reference files:
- A → `reference/nextjs/motion.md`

Store result as `ANIMATIONS: motion | none` — scaffold-app uses this to decide whether to animate landing page components.

---

**Category 8: Code Quality Tooling**
> "Would you like to add code quality tools?"
> A) Yes — Husky + commitlint + ESLint config
> B) No / Skip

Reference files:
- A → `reference/nextjs/tooling.md`

---

**Category 9: CI/CD Workflows**
> "Which GitHub Actions workflows would you like to add? (comma-separated, e.g. `1,3,4` or `none`)"
> 1) CI — lint + typecheck + build on every PR _(essential — highly recommended)_
> 2) Dependabot — automated weekly dependency updates _(simple, zero setup)_
> 3) Renovate — smarter dependency updates with automerge + grouping _(more powerful)_
> 4) Bundle size check — per-page bundle breakdown on PRs _(Next.js specific)_
> 5) CodeQL — security scanning _(free for public repos)_
> 6) Semantic Release — auto-versioning + changelog from conventional commits
> 7) Lighthouse CI — performance audits on PRs _(landing pages only)_
> 8) None

> Note: Choose either Dependabot (2) OR Renovate (3) — not both.
> Lighthouse CI (7) only useful for Landing/Marketing apps.

**Before creating any workflow file, detect project context by reading `package.json`:**

| What to detect | How | Stored as |
|---------------|-----|-----------|
| Package manager | `"packageManager"` field contains "yarn" OR `yarn.lock` exists | `PKG: yarn \| npm` |
| Node version | `"engines": { "node": ">=20" }` — extract major version, default `"20"` | `NODE: 20` |
| Test script | `scripts.test` exists and is not the default placeholder | `HAS_TESTS: true \| false` |
| Monorepo | `turbo.json` exists in root | `MONOREPO: true \| false` |
| App name | `name` field in `package.json` | used as `--filter` in turbo commands |

Apply these values when generating workflow YAML (substitute `cache:`, install command, run commands, and turbo commands accordingly).

Reference files:
- 1 → `reference/workflows/ci.md` (follow the detection + generation instructions; always include the Next.js `.next/cache` step)
- 2 → `reference/workflows/dependabot.md`
- 3 → `reference/workflows/renovate.md`
- 4 → `reference/workflows/bundle-size.md` (follow Option B — nextjs-bundle-analysis)
- 5 → `reference/workflows/codeql.md`
- 6 → `reference/workflows/semantic-release.md` (only if commitlint was installed in Category 8)
- 7 → `reference/workflows/lighthouse.md` (only if app type is Landing/Marketing)

For each selected workflow: create the relevant file(s) and commit with `chore: add <name> workflow`.

---

### React Native (Expo) Categories

---

**Category 1: UI Library / Styling**
> "Which UI library/styling would you like?"
> A) NativeWind v4 + Gluestack UI v3 _(Tailwind + component library)_
> B) NativeWind v4 only _(Tailwind, bring your own components)_
> C) Gluestack UI v3 only _(component library, no Tailwind)_
> D) Skip

Reference files:
- A → `reference/react-native/nativewind-gluestack.md`
- B → `reference/react-native/nativewind.md`
- C → `reference/react-native/gluestack.md`

---

**Category 2: Navigation**
> "Which navigation setup would you like?"
> A) Expo Router v4 _(recommended — file-based, like Next.js App Router)_
> B) React Navigation v7 _(traditional stack + tabs)_
> C) Skip

App-type notes:
- Dashboard → "Expo Router recommended — easy to add protected route groups."
- Consumer → "Either works — Expo Router is simpler for new projects."

Reference files:
- A → `reference/react-native/expo-router.md`
- B → `reference/react-native/react-navigation.md`

---

**Category 3: State Management**
> "Which state management would you like?"
> A) Zustand _(recommended for React Native — simple, AsyncStorage persist)_
> B) Redux Toolkit + redux-persist
> C) None
> D) Skip

App-type notes:
- Dashboard → "Recommended — user session, shared filters."
- Consumer → "Recommended — user session and preferences."
- Landing / Simple → "Probably not needed."

Reference files:
- A → `reference/react-native/zustand.md`
- B → `reference/react-native/redux-toolkit.md`

---

**Category 4: HTTP / Server State**
> "How would you like to handle HTTP requests?"
> A) TanStack Query + Axios _(caching, loading states — REST)_
> B) Axios only _(REST)_
> C) Apollo Client _(GraphQL — queries, mutations, subscriptions)_
> D) Skip

App-type notes:
- Dashboard → "TanStack Query recommended for REST; Apollo Client if your API is GraphQL."
- Consumer → "TanStack Query (REST) or Apollo Client (GraphQL) recommended."
- Simple → "Axios only is enough."

Reference files:
- A → `reference/react-native/tanstack-query.md`
- B → `reference/react-native/axios.md`
- C → `reference/react-native/graphql.md`

---

**Category 5: Internationalization (i18n)**
> "Would you like to add multi-language support?"
> A) Yes — expo-localization + i18next _(RTL support for Arabic)_
> B) No / Skip

Reference files:
- A → `reference/react-native/i18n.md`

---

**Category 6: Forms**
> "Would you like to add form handling?"
> A) React Hook Form + Zod _(recommended — lighter, excellent TypeScript)_
> B) Formik + Yup _(simpler API, well established)_
> C) No / Skip

App-type notes:
- Dashboard → "Recommended — data entry screens."
- Consumer → "Recommended — signup, login, profile forms."
- Landing → "Only if you have a contact / signup screen."

Reference files:
- A → `reference/react-native/forms.md` (follow Option A section)
- B → `reference/react-native/forms.md` (follow Option B section)

---

**Category 7: Code Quality Tooling**
> "Would you like to add code quality tools?"
> A) Yes — ESLint (expo config) + Prettier + Husky
> B) No / Skip

Reference files:
- A → `reference/react-native/tooling.md`

---

**Category 8: CI/CD Workflows**
> "Which GitHub Actions workflows would you like to add? (comma-separated, e.g. `1,2` or `none`)"
> 1) CI — lint + typecheck on every PR _(essential — highly recommended)_
> 2) Dependabot — automated weekly dependency updates _(simple, zero setup)_
> 3) Renovate — smarter dependency updates with automerge + grouping _(recommended for RN — handles native dep grouping better)_
> 4) CodeQL — security scanning _(free for public repos)_
> 5) Semantic Release — auto-versioning + changelog from conventional commits
> 6) None

> Note: Choose either Dependabot (2) OR Renovate (3) — not both.
> Bundle size check and Lighthouse CI are not applicable to React Native.

**Before creating any workflow file, detect project context by reading `package.json`:**

| What to detect | How | Stored as |
|---------------|-----|-----------|
| Package manager | `"packageManager"` field contains "yarn" OR `yarn.lock` exists | `PKG: yarn \| npm` |
| Node version | `"engines": { "node": ">=20" }` — extract major version, default `"20"` | `NODE: 20` |
| Test script | `scripts.test` exists and is not the default placeholder | `HAS_TESTS: true \| false` |
| Monorepo | `turbo.json` exists in root | `MONOREPO: true \| false` |

Apply these values when generating workflow YAML (substitute `cache:`, install command, and run commands accordingly).

Reference files:
- 1 → `reference/workflows/ci.md` (follow the React Native / Expo variant)
- 2 → `reference/workflows/dependabot.md`
- 3 → `reference/workflows/renovate.md`
- 4 → `reference/workflows/codeql.md`
- 5 → `reference/workflows/semantic-release.md` (only if commitlint was installed in Category 7)

For each selected workflow: create the relevant file(s) and commit with `chore: add <name> workflow`.

---

### React Native (CLI) Categories

Same as Expo categories above, with these differences:
- Category 2: No Expo Router option — only React Navigation v7
- Category 5: Uses `react-native-localize` instead of `expo-localization`
- Read `reference/react-native/cli-differences.md` first for all CLI-specific notes

Reference files:
- CLI differences → `reference/react-native/cli-differences.md`

---

## Step 4 — Install Each Integration

For each selection the user makes:

1. **Read the reference file** using the Read tool
2. Follow the steps in that file exactly
3. After each integration: run `git add . && git commit -m "feat: add <integration-name>"`
4. Tell the user what was installed and any important notes

## Step 5 — Integrations Summary + Auto-continue to Scaffold

After all categories are done, print:

```
✓ Integrations installed:
  - [list each one added]

Now generating your app structure...
```

**Do NOT stop here. Immediately continue into the full `/scaffold-app` flow below.**

The app type from Step 2 is already known — pass it through directly (skip the app type question in scaffold-app Step 3).

---

## Step 6 — Run Scaffold App (inline — do not ask the user to run it separately)

Follow the complete `/scaffold-app` skill from Step 1 through to the end, including:

- Step 1: Detect project type (already known — skip detection, use what was found in Step 1 above)
- Step 2: Detect installed packages (read `package.json` — packages were just installed)
- Step 3: Confirm app type — **SKIP** (already known from Step 2 of setup-project)
- Step 4: Read the reference file for the detected project + app type combination
- Step 5: Execute the scaffold — create all folders, components, routing, types
- Step 6: Clean up Vite boilerplate (React Vite only)
- Step 7: Commit
- Step 8: Ask about optional extras (skeleton loading, toasts, error boundary, dark mode)

After extras are handled, print the final "All done" message:

```
✅ All done!

Project: [project-name]/
App type: [Dashboard / Landing / Consumer]

Integrations:
  [list each installed integration]

Structure created:
  src/
    components/   — shared UI components
    features/     — feature modules
    hooks/        — custom hooks
    utils/        — helpers (cn, formatDate, etc.)
    types/        — shared TypeScript types
    services/     — API layer
    [store/]      — state (if Redux/Zustand added)
    [i18n/]       — translations (if i18n added)

Commands:
  yarn dev              — start dev server
  yarn build            — production build
  yarn preview          — preview production build
  [npx expo start]      — React Native dev server

[If auth added]:
  Demo: admin@example.com / password

Start here:
  src/features/         — add your first feature module
  src/services/         — wire up your real API endpoints
```

---

## Rules

- Always install latest versions: `yarn add package@latest`
- Never hardcode version numbers in package installs
- Commit after each integration — clean git history
- If a step fails, stop and show the error — don't silently continue
- One category at a time — don't dump all questions at once
- Always show the app-type recommendation note before each category's options
