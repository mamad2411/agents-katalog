---
name: customize-starter
description: Turn this React boilerplate into a real project. Use when starting a new project from this starter, renaming it, removing demo/starter content, or when the user mentions "customize starter", "rename project", "remove boilerplate demo", or "initialize from template".
---

# Customize Starter

Use this when a user is adapting this boilerplate into their own project. The
files that contain starter/demo content are listed below, so there is no need to
scan the whole repo. Edit only what the user asks for; confirm before deleting.

## 1. Rename the project

- `package.json` - update `name`, `version` (reset to `0.1.0`), and add a
  `description`.
- `index.html` - update the `<title>`.
- `src/config/env.ts` - the `appName` fallback defaults to `'React Boilerplate'`;
  change it to the new project name.
- `.env.example` (and the user's `.env.development.local` /
  `.env.production.local`) - set `VITE_APP_NAME` to the new project name.
- `docker-compose.yml` - update `image` and `container_name`
  (currently `react-boilerplate`).
- `README.md` - replace with the new project's README.

## 2. Remove the demo feature

The "home" feature is a placeholder example. To remove it:

- Delete `src/features/home/` (contains `components/HomePage.tsx` and
  `components/__tests__/HomePage.test.tsx`).
- `src/app/App.tsx` - it renders `<HomePage />`; replace with the real root.
- `src/i18n/locales/en/common.json` and `src/i18n/locales/ar/common.json` -
  remove the demo keys (`home.*`, `actions.increment`) and keep/add real ones.
  Keep keys in sync across every locale.

## 3. Set up analytics & monitoring

- `.env.development.local` / `.env.production.local` - fill in the GA4 and
  Sentry values for the new project:
  - `VITE_ANALYTICS_ENABLED=true`, `VITE_GA_MEASUREMENT_ID=G-…`
  - `VITE_SENTRY_ENABLED=true`, `VITE_SENTRY_DSN=https://…`
  - Optionally set `VITE_SENTRY_ENVIRONMENT`, `VITE_SENTRY_RELEASE`, sample
    rates, and `VITE_GA_DEBUG_MODE`.
- For Sentry source-map uploads in CI, set `SENTRY_AUTH_TOKEN`, `SENTRY_ORG`,
  and `SENTRY_PROJECT` as build-time secrets.
- See the `analytics-and-monitoring` skill for usage patterns.

## 4. Optional cleanup

- `public/vite.svg` - replace the favicon; update the `<link rel="icon">` in
  `index.html`.
- `.cursor/skills/customize-starter/` - delete this skill once the project is
  set up (it only applies to the starter).

## Keep (not starter junk - reusable infrastructure)

Do not remove these unless explicitly asked; they are the boilerplate's value:

- `src/app/providers/` - Helmet, React Query, Theme, Direction providers.
- `src/components/ThemeToggle.tsx`, `src/components/LanguageSwitcher.tsx`,
  `src/components/PageTitle.tsx`.
- `src/components/shadcn/` and `src/components/ui/` - design system (see the
  `add-shadcn-component` skill for the layering rules).
- `src/lib/` (`utils`, `analytics`, `monitoring`), `src/config/env.ts`,
  `src/i18n/config.ts`, `src/test/`.
- Tooling: `eslint.config.js`, `.prettierrc.json`, `.importsortrc`,
  `.lintstagedrc`, `.commitlintrc.json`, `.husky/`, `vite.config.ts`, tsconfigs.

## After customizing

Run `yarn typecheck && yarn lint && yarn test && yarn build` and fix anything
that broke (e.g. translation keys referenced by deleted code). Update
`README.md`, the locale files, and the `appName` fallback in `src/config/env.ts`
so they match the new project.
