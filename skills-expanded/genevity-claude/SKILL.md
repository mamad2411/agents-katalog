# GENEVITY — Medical Longevity Center Website

## 🚨 CRITICAL: BRANCH POLICY — READ BEFORE ANY WORK 🚨

**v2 is LIVE on `main` / `genevity.com.ua`. Work on `develop`. Small, self-contained changes may ship to `main` via PR — the RoApp direct booking may not.**

- **ALL work happens on the `develop` branch.** Never commit/push directly to `main`.
- `main` is protected on GitHub (direct pushes blocked, PR required, force-push disabled) and auto-deploys to production (`genevity.com.ua`).
- `develop` auto-deploys to a Vercel preview URL (`genevity-git-develop-*.vercel.app`). Use this for everything: content, features, schema changes, experiments.

### What may ship to `main`

**Allowed —** small, self-contained side features and fixes: SEO/schema markup, metatags, copy and content, styling, analytics, bugfixes, admin-only tooling. Confirm with the user before each merge, then ship it.

**Not allowed —** the **RoApp direct booking** (online appointments written straight into RoApp: `src/lib/roapp/*`, `src/components/booking/*`, the `/booking` wizard and its API routes). It stays on `develop` until the client explicitly signs it off — a merge would make real patient appointments live.

### How to merge

Do **not** merge the whole `develop` branch: it carries the RoApp booking work. Cherry-pick the specific commits onto a branch cut from `origin/main`, open a PR against `main`, and merge that.

```
git checkout -b fix/<slug> origin/main
git cherry-pick <sha>
npm run build          # verify before opening the PR
gh pr create --base main
```

- Before any `git push`, `git commit`, or branch-changing command: verify the branch with `git branch --show-current`. If it says `main`, STOP and switch.
- Never push directly to `main` (`git push origin main`) — always go through a PR.
- After merging, verify on the live domain, not just the preview.

**Sanity:** single `production` dataset shared by both branches (intentional — the landing and v2 read the same content). Schema additions are safe since Sanity is schemaless at the API level.

## Project Overview
Medical clinic website for GENEVITY (Дніпро, Україна). Aesthetic medicine & longevity center.

## Tech Stack
- **Framework:** Next.js 16 (App Router, Turbopack)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS v4 (CSS-first config in `globals.css`)
- **Animations:** Framer Motion
- **i18n:** next-intl (Ukrainian default, Russian, English)
- **Fonts:** Cormorant Garamond (headings), Montserrat (body) via `next/font/google`

## Commands
- `npm run dev` — start dev server
- `npm run build` — production build
- `npm run lint` — ESLint

## Architecture

### Routing
- All routes under `src/app/[locale]/`
- Locale prefix: `as-needed` (no prefix for default `uk`)
- Sub-pages in `(pages)/` route group
- Path translations defined in `src/i18n/routing.ts`

### Key Directories
```
src/
├── app/[locale]/          # Pages & layouts
│   ├── (pages)/           # Sub-pages (pro-tsentr, poslugy, likari, blog, kontakty)
│   └── globals.css        # Design tokens & typography presets
├── components/
│   ├── layout/            # Header, Footer
│   ├── sections/          # Homepage sections (Hero, Services, FAQ, etc.)
│   └── ui/                # Reusable components (Button, SectionHeader, Icons)
├── i18n/                  # next-intl routing & request config
├── lib/                   # Framer Motion animation presets
└── messages/              # Translation JSON files (uk.json, ru.json, en.json)
```

### Design System
- Colors: `--color-main` (#8B7B6B taupe), `--color-champagne` (#FAF9F6), `--color-rosegold` (#C0CFD5)
- Typography classes: `.heading-1`, `.heading-2`, `.heading-3`, `.body-l`, `.body-strong`, `.body-m`, `.body-s`
- Spacing: section (120px), block (64px), element (32px), card (24px), inner (16px)
- Border radius: buttons (12px), cards (16px), pills (999px)

### Conventions
- All page components are `"use client"` (Framer Motion dependency)
- Translations via `useTranslations()` hook
- Animation presets from `@/lib/motion` (fadeInUp, staggerContainer, viewportConfig)
- Path alias: `@/` → `./src/`
- Ukrainian is the canonical/default language

### Current State
- Homepage: fully built with all sections
- Sub-pages: scaffolded with placeholder content (hardcoded Ukrainian text, not yet i18n-ized)
- Images: all placeholders (no real assets yet)
- No backend/CMS integration
- No Schema.org structured data yet
