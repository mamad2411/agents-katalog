# Whiskeyjack Starter

A thumb-first React app built on the Whiskeyjack design system, wired for one
web codebase delivered to desktop and mobile via Tauri.

> This file is the canonical set of conventions for this project, and is written
> to be tool-neutral: any coding agent that reads `AGENTS.md` gets the same
> rules. `.claude/` adds Claude-Code-specific tooling (agents, skills,
> path-scoped rules) on top.

## Stack

- React 18 + TypeScript, Vite
- `@whiskeyjack-net/design-system` – tokens, Tailwind preset, and components
- `@whiskeyjack-net/i18n` – the shared react-i18next bootstrap
- `@whiskeyjack-net/tauri` – the desktop/mobile app-shell layer (inert on web)
- Tailwind CSS (via the design-system preset), Phosphor icons
- `@fontsource-variable/inter` – self-hosted Inter Variable, the family the
  design-system tokens name (they fall back to `system-ui` without it)

## Commands

```bash
npm run dev      # dev server
npm run build    # tsc + vite build
npm run lint     # ESLint (run this before you consider a change done)
npm run check:versions  # package.json, tauri.conf.json and Cargo.toml agree
```

## Structure

```
src/
  main.tsx          # entry: Inter font, `tauri` marker class, BrowserRouter + i18n
  App.tsx           # routes
  index.css         # DS token + utility CSS, Tauri chrome CSS, Tailwind
  i18n/             # createI18n(locales) + locale JSON
  components/
    Layout.tsx      # the app shell (AppShell + header + nav + theme + Tauri chrome)
  pages/            # Home, Settings
scripts/
  check-versions.mjs  # the version agreement the updater relies on
```

## Finding a design-system component

Before writing a component, check whether the design system already has it.
`components.json` registers the `@whiskeyjack` namespace, so:

```bash
npx shadcn@latest search @whiskeyjack           # list every item with descriptions
npx shadcn@latest view @whiskeyjack/bottom-drawer
npx shadcn@latest add @whiskeyjack/bottom-drawer  # copy the source into src/
```

Two ways to consume a component, both valid:

1. **Import from the package** – `import { Button } from '@whiskeyjack-net/design-system'`.
   The default. You track the package version.
2. **Copy it in with the registry** – `npx shadcn@latest add @whiskeyjack/<name>`
   lands the source under `src/components/ui/` and you own it from there. Use
   this when the component needs project-specific changes.

Each registry item carries a usage note that the CLI prints on install; it says
which component to reach for and what to avoid hand-rolling. Read it.

## Conventions

- **Design-system first.** Reach for a DS component or hook before writing your
  own. Search the registry (above) rather than assuming something is missing.
- **Tokens via CSS variables.** `var(--color-accent-500)`, never a hardcoded
  hex or a raw Tailwind palette class. Token-surface changes belong in the
  Tailwind preset.
- **Phosphor icons only** (`@phosphor-icons/react`). The DS is icon-library-free
  and takes icon nodes as props, so pass them in.
- **All user-facing text is an i18n key.** Use `useTranslation()`, and add the
  key to every locale file in `src/i18n/locales/`.
- **The app shell is DS components** – `AppShell` / `AppHeader` / `HeaderNav` /
  `AppMain` / `MobileBottomNav`. Theme with `useTheme`; never hand-roll
  matchMedia listeners, dark-class toggling, or theme-color meta updates.
- **Tabbed content is always swipeable.** Any `TabBar` pairs with
  `useSwipeNavigation`.
- **Drawers are for interaction** – adding, editing, confirming. Read-only
  display content (stats, charts, detail views) belongs in the app's main
  chrome. Modal actions go in the drawer's sticky `footer`, most-destructive
  leftmost.
- **Buttons use the default 42px size** everywhere in the app. `size="lg"` is
  for hero CTAs only; avoid `size="sm"`.
- **En dashes (`–`), never em dashes (`—`)**, in UI copy and code comments alike.
- **State what a thing is.** Avoid contrastive-negation copy ("It's not X, it's
  Y", "not just X"). Factual absence is fine ("no email needed").
- **Accessibility is WCAG 2.1 AA**, inherited from the DS primitives: visible
  focus rings, focus trapping in overlays, 44px touch targets, reduced-motion
  respect, and labeled controls. Icon-only buttons need both `aria-label` and a
  matching `title`. Accessibility strings are translation keys too.
- **TypeScript strict.** Use the `@/` alias instead of deep relative imports.

## Theming

The default accent applies out of the box. To re-tint, either call
`applyAccentColor(hex)` at runtime (it derives the whole `--color-accent-*`
scale and picks a WCAG-legible foreground automatically), or override the
`--color-accent-*` variables in a `:root` block loaded after the token CSS. The
design system's README covers both under "Theming & accent".

## Before you finish a change

1. `npm run lint` – the conventions above that can be machine-checked are
   enforced there.
2. `npm run build` – `tsc` plus the production build.
3. Check any new user-facing string exists in every locale file.
4. `npm run check:versions` before tagging a release once `src-tauri/` exists.
