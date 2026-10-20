# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Important: Next.js version

This project uses **Next.js 16.2.3**, which has breaking changes from earlier versions. APIs, conventions, and file structure may differ from training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

## Commands

```bash
npm run dev       # Start dev server (uses Turbopack)
npm run build     # Production build
npm run lint      # ESLint
```

### Prisma

```bash
npx prisma migrate dev       # Apply schema changes and regenerate client
npx prisma generate          # Regenerate client without migrating
npx prisma studio            # Open database GUI
```

The Prisma client is generated into `src/app/generated/prisma/` (not the default location). Schema lives at `src/prisma/schema.prisma`, migrations at `src/prisma/migrations/`.

## Architecture

### Data layer

All pages are async React Server Components — no API routes. Database access goes through `src/lib/db.ts`, which exports a singleton `db` (Prisma client using the `@prisma/adapter-pg` PostgreSQL adapter). Import as `import { db } from "../../lib/db"` and query directly in the page component.

### Routing

App Router under `src/app/`. Routes: `/` (home), `/contact`, `/experience`, `/experience/work`, `/experience/recommendations`. The experience sub-routes share a layout at `src/app/experience/layout.tsx`.

### Styling

Tailwind CSS v4 — **no `tailwind.config.ts`**. Theme tokens are defined via CSS custom properties in `src/app/globals.css` using `@theme inline`. Available colors: `background`, `foreground`, `muted`, `border`, `surface`, `accent`, `blue`. All dark-mode by default; there is no light/dark toggle.

### SVGs

SVG files are imported as React components (via `@svgr/webpack` in `next.config.ts` Turbopack rules). Type declarations are in `src/types/svg.d.ts`.

### Database models

- `Profile` — singleton row: name, headline, bio, location, avatarUrl, email, linkedinUrl, githubUrl
- `Experience` — work history entries ordered by `orderIndex`
- `Recommendation` — LinkedIn-style recommendations
- `Message` — contact form submissions (with `read` flag)
