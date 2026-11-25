---
name: scaffold-app
description: Scaffold a production-ready folder structure, base components, routing, types, and env setup for an already-configured React (Vite), Next.js, or React Native project. Run after /setup-project.
---

# Scaffold App

You are a project scaffolding assistant. Your job is to generate the full production-ready app structure — folders, base components, routing, types, and environment setup — based on what the project already has installed.

**Run this after `/setup-project`** (or on any project where packages are already configured).

---

## Step 1 — Detect Project Type

Check the current directory for:
- `next.config.*` → **Next.js**
- `vite.config.*` → **React (Vite)**
- `app.json` with `expo` key → **React Native (Expo)**
- `android/` + `ios/` without expo → **React Native (CLI)**

---

## Step 2 — Detect Installed Packages

Read `package.json` (and `package.json` in the project root if monorepo). Build a profile:

```
UI_LIBRARY:        heroui | shadcn | tailwind-only | none
STATE_MANAGER:     redux | zustand | none
ROUTER:            react-router | tanstack-router | expo-router | react-navigation | none
HTTP_CLIENT:       tanstack-query+axios | axios | native-fetch | none
I18N:              react-i18next | next-intl | i18next | none
AUTH:              nextauth | jwt-custom | none
FORMS:             react-hook-form | formik | none
ANIMATIONS:        motion | none
```

Detect by checking `dependencies` and `devDependencies` for:
- `@heroui/react` → heroui
- `@radix-ui/react-*` or `components.json` file → shadcn
- `tailwindcss` without above → tailwind-only
- `@reduxjs/toolkit` → redux
- `zustand` → zustand
- `react-router-dom` → react-router
- `@tanstack/router` → tanstack-router
- `expo-router` → expo-router
- `@react-navigation/native` → react-navigation
- `@tanstack/react-query` → tanstack-query
- `axios` → axios
- `next-intl` → next-intl
- `react-i18next` → react-i18next
- `next-auth` → nextauth
- `react-hook-form` → react-hook-form
- `formik` → formik
- `motion` → motion

---

## Step 3 — Confirm App Type

If coming from `/create-frontend-project`, the app type is already known — skip this question.

Otherwise ask:
> "What kind of app is this?
> A) Dashboard / Admin app
> B) Landing / Marketing site
> C) Consumer app (user-facing, accounts)
> D) General purpose"

**If Dashboard / Admin is selected, ask one more question:**
> "What layout style do you want for the dashboard?
> A) Sidebar navigation (left sidebar + main content area — most common for admin panels)
> B) Top navigation bar (sticky top nav + full-width content — cleaner for data-heavy apps)"

Store the answer as `LAYOUT_STYLE: sidebar | topnav` and use it in Step 5.

---

## Step 4 — Read the Reference File

Based on project type + app type, read the reference file:

| Project Type | App Type | Reference File |
|---|---|---|
| React (Vite) | Dashboard / Consumer | `~/.claude/project-scaffolding/reference/scaffold/react-dashboard.md` |
| React (Vite) | Landing / General | `~/.claude/project-scaffolding/reference/scaffold/react-landing.md` |
| Next.js | Dashboard / Consumer | `~/.claude/project-scaffolding/reference/scaffold/nextjs-dashboard.md` |
| Next.js | Landing / General | `~/.claude/project-scaffolding/reference/scaffold/nextjs-landing.md` |
| React Native | Any | `~/.claude/project-scaffolding/reference/scaffold/react-native-app.md` |

**Read the file now with the Read tool before proceeding.**

---

## Step 5 — Execute the Scaffold

Follow the reference file exactly. For every file it specifies:

1. Create the directory if it doesn't exist
2. Write the file with the content from the reference
3. **Adapt component code** to the detected package profile:
   - If `heroui` (React Vite only):
     - **Wrap app with `HeroUIProvider` in `src/main.tsx`** (CRITICAL — React Vite only, required for HeroUI styles)
       ```tsx
       import { HeroUIProvider } from '@heroui/react'
       // wrap: <HeroUIProvider><App /></HeroUIProvider>
       ```
     - Use HeroUI `Button` instead of plain `<button>` in layout/marketing components
     - Use HeroUI `Card`, `CardBody` for feature cards and pricing cards
     - Use HeroUI `Navbar`, `NavbarBrand`, `NavbarContent`, `NavbarItem` for the site header
   - If `heroui` (Next.js):
     - **HeroUI v3 has NO provider** — do NOT add HeroUIProvider anywhere
     - Import and use HeroUI components directly in client components (`'use client'`)
     - Use HeroUI `Button`, `Card`, `CardBody`, `Navbar` components directly
   - If `shadcn`: use shadcn/ui `Button`, `Card` components
   - If `tailwind-only` or `none`: use plain HTML + Tailwind classes
   - If `redux`: use Redux store patterns in auth/app hooks
   - If `zustand`: use Zustand store patterns
   - If `react-hook-form`: use RHF in form components
   - If `formik`: use Formik in form components
   - If `i18n` detected (next-intl):
     - Use `t()` for all user-visible strings
     - **CRITICAL: Replace ALL `import Link from 'next/link'` with `import { Link } from '@/i18n/navigation'`** — this makes every link locale-aware automatically (e.g. Arabic → `/ar/about`, English → `/about`)
     - **CRITICAL: Replace ALL `import { useRouter } from 'next/navigation'` with `import { useRouter } from '@/i18n/navigation'`**
     - `src/i18n/navigation.ts` must exist (created by next-intl setup step) — it exports locale-aware `Link`, `useRouter`, `usePathname`, `redirect`
   - If `i18n` detected (react-i18next): use `t()` for all user-visible strings
   - If `ANIMATIONS: motion` AND app type is **Landing or Consumer**:
     - **React (Vite):** Wrap key landing sections with `motion.div` from `motion/react` — use `initial/whileInView/viewport` for scroll-triggered reveals. Apply to: Hero headline + subtext, Features section cards (stagger), Pricing section cards (stagger), CTA banner. Import pattern: `import { motion } from 'motion/react'`
     - **Next.js:** Create `src/components/ui/FadeIn.tsx` as a `'use client'` wrapper (see `reference/nextjs/motion.md`). Wrap Hero, Features, Pricing, CTA sections with `<FadeIn>` in server page components. For stagger grids (feature cards, pricing cards), create a `'use client'` component that uses `motion.div` with `variants` + `staggerChildren`.
     - Keep animations minimal: fade-in (opacity 0→1) + slide-up (y: 24→0), duration 0.4–0.5s, ease-out. CTA buttons get `whileHover={{ scale: 1.03 }}`.
     - **Never add animations if app type is Dashboard / Admin** — even if `motion` is installed.
4. **If app type is Dashboard**, apply the `LAYOUT_STYLE` choice:
   - If `LAYOUT_STYLE = sidebar`:
     - Use `AppShell` with `<Sidebar />` on the left (default in reference)
     - If heroui: use the HeroUI Sidebar variant from the reference's "HeroUI Variants" section
   - If `LAYOUT_STYLE = topnav`:
     - Use `AppShell` with `<TopNav />` at the top (top nav variant from reference)
     - Replace `AppShell.tsx` content with the top nav version
     - Create `TopNav.tsx` instead of `Sidebar.tsx`
     - If heroui: use the HeroUI TopNav variant from the reference's "HeroUI Variants" section
5. Skip files that duplicate what's already set up (e.g. if axios.ts already exists in `src/lib/`, skip it)

---

## Step 6 — Clean Up Vite Boilerplate

For React (Vite) projects, remove the default boilerplate:
- Delete `src/App.css` (unless it has custom styles)
- Clear `src/App.tsx` content (replace with the router entry point from reference)
- Keep `src/index.css` (contains Tailwind imports)
- Delete `public/vite.svg` and `src/assets/react.svg` if unused

---

## Step 7 — Commit

```bash
git add .
git commit -m "feat: scaffold app structure — folder layout, base components, routing, types"
```

---

## Step 8 — Optional Extras

After scaffolding is complete, ask:

> "Want me to add any of these extras? (comma-separated or 'none')
> 1) Skeleton loading components (recommended — prevents layout shift on data load)
> 2) Toast notifications via sonner (recommended — user feedback for API calls)
> 3) Error boundary (recommended — prevents full app crash from one component error)
> 4) Dark mode toggle button
> 5) None"

Then add what was selected on top of the already-scaffolded structure.

For heroui adaptation of selected extras:
- If skeleton extras selected: use HeroUI `Skeleton` component (from `@heroui/react`) instead of plain CSS pulse

---

## Step 9 — All Done

After extras are handled (or skipped), print:

```
✅ All done!

Project: [project-name]/
App type: [Dashboard / Landing / Consumer]

Structure created:
  src/
    components/   — shared UI components
    features/     — feature modules
    hooks/        — custom hooks
    utils/        — helpers (cn, formatDate, etc.)
    types/        — shared TypeScript types
    services/     — API layer
    [store/]      — state (if Redux/Zustand detected)
    [i18n/]       — translations (if i18n detected)

Commands:
  yarn dev              — start dev server
  yarn build            — production build
  yarn preview          — preview production build
  [npx expo start]      — React Native dev server

[If auth detected]:
  Demo: admin@example.com / password

Start here:
  src/features/         — add your first feature module
  src/services/         — wire up your real API endpoints
```

Then ask:

> "Want me to start the dev server now?
> A) Yes — start it now (runs in the background, output will appear here)
> B) No — I'll run it myself"

**If A — start it now:**

Run the correct dev command for the project type **in the background** (so it doesn't block the conversation):

- React (Vite): `yarn dev` (from the project directory)
- Next.js: `yarn dev` (from the project directory)
- React Native (Expo): `npx expo start` (from the project directory)
- React Native (CLI): `npx react-native start` (from the project directory)

Use the Bash tool with `run_in_background: true`. After launching, tell the user:

> "Dev server started in the background.
> Open: http://localhost:5173 (Vite) or http://localhost:3000 (Next.js)
> Output will appear in this conversation when the server is ready."

**If B — user runs it themselves:**

Show the exact command to copy-paste:

> "Run this in your terminal from the project directory:
> ```
> cd [project-name]
> yarn dev
> ```"

---

## Step 10 — Generate CLAUDE.md

After the dev server question is resolved, **always** generate `CLAUDE.md` without asking.

Follow the complete `generate-claude-md` skill from Step 1 through Step 6:
- The stack profile is already fully known from Step 2 of this scaffold flow — skip re-detection
- The app type is already known — pass it through directly
- Write `CLAUDE.md` to the project root, commit it

Tell the user after generating:

> "Generated `CLAUDE.md` — Claude will read this automatically at the start of every future session in this project. No need to explain the stack again."

---

## Rules

- Never overwrite files that already have meaningful content — check first with Read tool
- Always adapt component code to the detected UI library
- If i18n is detected, all user-facing strings must use translation keys (add keys to locale files too)
- Create `.env.example` with all variables documented but empty values
- One commit at the end — not per file
- Tell the user what was created and the key files to start editing
