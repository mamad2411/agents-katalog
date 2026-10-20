# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Also read `AGENTS.md` — auto-generated codebase context (components, models, tokens, complexity scores).

## Project

Hashmark (hashmark.md) — SaaS that scans codebases and generates AI context files for every coding tool. One scan, every format, always in sync.

Three deliverables in one monorepo:
- **Web App** (root `src/`): Next.js 16 App Router — landing page + full dashboard (auth, billing, scan engine)
- **CLI** (`packages/cli/`): `hashmark-cli` scanner engine — 27 scanners, 8 output formats
- **GitHub Action** (`packages/action/`): auto-sync context files on push

## Commands

```bash
# Web App (Next.js)
pnpm dev              # Dev server (Turbopack)
pnpm build            # Production build (runs prisma generate first)
pnpm lint             # ESLint (Next.js core-web-vitals + typescript)
pnpm type-check       # TypeScript check (tsc --noEmit)

# Database (uses dotenv-cli to load .env.local)
pnpm db:push          # Push Prisma schema to Postgres
pnpm db:generate      # Generate Prisma client
pnpm db:studio        # Open Prisma Studio
pnpm db:seed          # Seed database (demo user, repo, scan, files)

# CLI (separate workspace package)
cd packages/cli && pnpm build     # Build with tsup (ESM + DTS)
cd packages/cli && pnpm dev       # Watch mode
cd packages/cli && node dist/cli.js --format all  # Run locally, all 8 formats

# GitHub Action (separate workspace package)
cd packages/action && pnpm build  # Build with tsup
```

## Setup

```bash
pnpm install
cp .env.example .env.local   # Then fill in values
pnpm db:push                 # Create database tables
pnpm db:seed                 # Optional: seed demo data
pnpm dev
```

Required env vars: `DATABASE_URL`, `AUTH_SECRET`, `AUTH_GITHUB_ID`, `AUTH_GITHUB_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `GITHUB_WEBHOOK_SECRET`.

## Stack

- **Next.js 16.1.6** (App Router) + TypeScript 5.9 + Tailwind v4
- **Prisma 6** + Postgres (Supabase/Neon)
- **NextAuth v5 beta** (GitHub OAuth, PrismaAdapter) — `src/lib/auth.ts`
- **Stripe** (subscriptions, webhooks) — `src/lib/stripe.ts`
- **Octokit** (GitHub API) — `src/lib/github.ts`
- **FABRK** (`@fabrk/components`, `@fabrk/design-system`) — dashboard UI primitives
- **pnpm workspace** — packages are independent, built with tsup

## Architecture

**Web App** (`src/`): Path alias `@/*` → `./src/*`. Prisma singleton at `src/lib/db.ts`. Root layout uses Geist Mono font. ESLint config at `eslint.config.mjs` (flat config). Root tsconfig excludes `packages/` — each package has its own.

**Pages** (10 routes):
- `(marketing)`: `/` (landing), `/pricing`, `/login`
- `(dashboard)`: `/dashboard` (overview), `/dashboard/repos`, `/dashboard/billing`, `/dashboard/settings`
- `(dashboard)`: `/dashboard/[repoId]` (intelligence), `/dashboard/[repoId]/files`, `/dashboard/[repoId]/history`

**API Routes** (9 endpoints):
- Auth: `/api/auth/[...nextauth]`
- Billing: `/api/billing/checkout`, `/api/billing/portal`, `/api/billing/webhook`
- Repos: `/api/repos` (list GitHub repos)
- Scans: `/api/scan/[repoId]` (trigger), `/api/scan/[repoId]/latest` (poll), `/api/scan/[repoId]/download` (ZIP)
- Webhooks: `/api/webhooks/github` (auto-sync on push)

**CLI engine** (`packages/cli/`): Entry is `src/cli.ts` (uses `cac` for arg parsing). Scanners in `src/scanners/` each export a scan function. `src/generator.ts` produces AGENTS.md. `src/formats/` has per-tool generators that all consume a `ScanResult` type. The format factory in `src/formats/index.ts` has `generateFormat()` for one format and `generateAllFormats()` for all. Config loaded from `hashmark.config.json` / `.hashmarkrc` / legacy `agentsmith.config.*`.

**Database**: 8 Prisma models — User, Repository, Scan, GeneratedFile, CustomRule + 3 NextAuth models. Enums: Plan (FREE/PRO/TEAM), ScanStatus, FileFormat, RuleScope. Schema at `prisma/schema.prisma`.

## Key Patterns

- **Route Groups**: `(marketing)` for public pages, `(dashboard)` for authenticated
- **Server Components by default**: Only add `"use client"` when needed
- **Server Actions**: For mutations (connect repo, trigger scan, install GitHub Action)
- **API Routes**: For webhooks (Stripe, GitHub), polling, file downloads
- **Scan polling**: `useScanPolling` hook polls `/api/scan/[repoId]/latest` every 3s, calls `router.refresh()` on completion
- **Plan gating**: Server-side in actions + client-side `UpgradeGate` component. FREE = 1 repo, no custom rules, no scan history, no auto-sync
- **Parallel data fetching**: `Promise.all` in server components for concurrent DB queries
- **Loading/error states**: Every dashboard route has `loading.tsx` (skeleton UIs) + `error.tsx` (error boundaries with retry)
- **Breadcrumbs**: Auto-generated from pathname via `DashboardBreadcrumbs` in shell wrapper

## Design Rules

- Dark terminal aesthetic: zinc-950 background, zinc-50 foreground, zinc-800 borders
- Monospace font: `font-mono` everywhere
- Headings: UPPERCASE
- Buttons: UPPERCASE with `>` prefix (e.g., `> CONNECT REPO`)
- The `#` symbol is the brand motif
- Radius: 0 (sharp corners, terminal style)
- Use semantic tokens over hardcoded values: `bg-background` not `bg-zinc-950`, `text-accent` not `text-emerald-500`

### FABRK Components (use these, don't build from scratch)

- `DashboardShell` — Full layout (sidebar + mobile responsive + user section + sign out)
- `DashboardHeader` — Page title with optional subtitle + actions slot
- `PageHeader` — Swiss-style header with tabs, search, and actions
- `StatsGrid` — Responsive KPI grid (2/3/4 columns)
- `TierBadge` — Plan indicator (FREE/PRO/TEAM with icons)
- `EmptyState` — Empty state with icon, title, description, action
- `Badge` — Status/label badges with variants
- `Button` — Primary/outline/ghost/destructive, loading state, `asChild`
- `Input` — Form inputs
- `Breadcrumb*` — Breadcrumb primitives (Breadcrumb, BreadcrumbList, BreadcrumbItem, BreadcrumbLink, BreadcrumbPage, BreadcrumbSeparator)

### Dashboard Components (24 total in `src/components/`)

- **Dashboard**: `dashboard-shell-wrapper`, `dashboard-breadcrumbs`, `billing-actions`, `connect-repo-dialog`, `files-page`, `intelligence-page`, `repo-card`, `repo-sub-nav`, `repos-page`, `rule-card`, `rule-dialog`, `scan-history-page`, `settings-page`, `trial-banner`
- **Landing**: `cli-section`, `footer`, `formats`, `hero`, `how-it-works`, `pricing-table`
- **Shared**: `login-card`, `oauth-buttons`, `status-badge`, `upgrade-gate`

## Output Formats (8 total)

| Format ID | File | AI Tool |
|-----------|------|---------|
| `agents-md` | `AGENTS.md` | Universal (20+ tools) |
| `claude-md` | `CLAUDE.md` | Claude Code |
| `cursorrules` | `.cursorrules` | Cursor (legacy) |
| `cursor-mdc` | `.cursor/rules/*.mdc` | Cursor (new, multi-file) |
| `copilot-md` | `.github/copilot-instructions.md` | GitHub Copilot |
| `windsurf-rules` | `.windsurfrules` | Windsurf |
| `gemini-md` | `GEMINI.md` | Google Gemini CLI |
| `cline-rules` | `.clinerules` | Cline / Roo Code |

Each generator lives in `packages/cli/src/formats/<name>.ts` and takes `(scan: ScanResult, customRules: string[])`.
