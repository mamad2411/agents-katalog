<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

# AI Persistent Instructions & Engineering Guidelines for Grova

Welcome AI Assistant! This document serves as the single source of truth for repository context, architecture, goals, tech stack, and development standards when contributing to **Grova**.

---

## 1. Project Overview & Core Goals

**Grova** is a modern, high-performance daily habit-building and goal-tracking SaaS platform designed to help individuals and teams maintain consistency, track long-term targets, and visualize progress through GitHub-style activity heatmaps.

### Key Objectives & Philosophy

- **Visual Progress & Heatmaps**: Transform daily work into 365-day color-coded contribution heatmaps and real-time streak stats.
- **Flexible Goal Mechanics**: Support `TOTAL_TARGET` (cumulative), `DAILY_RECURRING`, and `WEEKLY_RECURRING` goals across categories (Work, Study, Health, Mindfulness, Finance, Creative, Social).
- **Self-Hostable & Lightweight**: Simple, developer-friendly deployment with Vercel and Neon Serverless PostgreSQL.
- **Social & Accountability**: Follow users, share public activity feeds, and receive milestone notifications.

---

## 2. Technology Stack Architecture

| Layer                      | Technology                 | Key Usage / Details                                                                        |
| :------------------------- | :------------------------- | :----------------------------------------------------------------------------------------- |
| **Framework**              | Next.js 16 (App Router)    | Server Components default, Route Handlers, middleware (`proxy.ts`)                         |
| **UI Engine**              | React 19 & TypeScript 5    | Strict typing, Hooks, Server/Client component boundary                                     |
| **Styling**                | Tailwind CSS v4 + PostCSS  | Class utility formatting, Radix UI primitives, CVA, `clsx`, `tailwind-merge` (`cn` helper) |
| **Animation & Charts**     | Framer Motion & Recharts   | Micro-interactions, visual charts & performance graphics                                   |
| **UI Components & Toasts** | Radix UI & Sonner          | Accessible primitives (`Dialog`, `Dropdown`, `Tabs`, `Avatar`), toast alerts               |
| **Database & ORM**         | Neon PostgreSQL & Prisma 7 | Edge-ready serverless database with Prisma ORM client (`@/lib/db`)                         |
| **Authentication**         | NextAuth.js v5 (Auth.js)   | Server-side `auth()`, Prisma adapter (`@auth/prisma-adapter`), GitHub & Google OAuth       |
| **Validation**             | Zod v4                     | Schema validation for forms, APIs, and environment variables                               |
| **Package Manager**        | pnpm v10                   | Workspace & dependency management                                                          |

---

## 3. Directory Structure & Architecture Standards

```
Grova/
├── app/                      # Next.js App Router root
│   ├── (protected)/          # Auth-guarded routes (/dashboard, /goals, /analytics, /settings)
│   ├── [username]/           # Dynamic public user profile pages
│   ├── api/                  # REST/JSON API endpoint handlers
│   ├── explore/              # Community activity feed
│   ├── login/                # Authentication login page
│   ├── globals.css           # Global Tailwind CSS v4 styles & design tokens
│   ├── layout.tsx            # Root layout provider wrapper
│   ├── page.tsx              # Public landing page
│   └── proxy.ts              # Custom session middleware proxy
├── auth.ts                   # NextAuth.js v5 configuration & custom user adapter
├── components/
│   ├── ui/                   # Primitive reusable atomic UI components (Radix + Tailwind)
│   └── shared/               # Feature-specific shared components (Heatmap, Navbar, Sidebar, Logo)
├── lib/
│   ├── db.ts                 # Singleton Prisma Database Client
│   └── utils.ts              # Helper functions (`cn()`, streak calculations, username generation)
├── prisma/
│   └── schema.prisma         # PostgreSQL schema definition (User, Goal, DailyLog, QuickNote, etc.)
├── docs/                     # Project documentation & guides (DEPLOYMENT.md, etc.)
├── public/                   # Static public assets (images, icons, svgs)
└── scripts/                  # Utility scripts & maintenance tools
```

---

## 4. Engineering & Development Rules

### Component & React Standards

- **Server Components First**: Keep components as Server Components by default. Add `"use client"` only when managing state, effects, or browser event listeners.
- **Styling Utility Rules**: Always use the `cn()` helper from `@/lib/utils` for conditional tailwind class composition. Keep classes canonicalized.
- **Icons**: Import icons strictly from `lucide-react`.

### Database & Data Flow Rules

- **Prisma Client Usage**: Always import `db` from `@/lib/db`. Do not instantiate multiple `PrismaClient` instances.
- **Denormalized Counters**: Maintain `currentStreak`, `longestStreak`, `totalContributions`, and `completionRate` on the `User` model, and `completedAmount` on the `Goal` model for fast read performance.
- **Database Operations**: Run `pnpm db:generate` after modifying `prisma/schema.prisma`. Use `pnpm db:push` for database schema updates during dev.

### Authentication & API Security

- **Protecting Server Routes**: Authenticate user sessions in Server Components and Route Handlers using `await auth()`.
- **Middleware Routing**: Route guards are managed in `proxy.ts` (redirecting unauthenticated users from `/dashboard`, `/goals`, `/analytics`, `/settings`).

---

## 5. QA, Formatting & Validation Workflow

Before completing any feature, bug fix, or refactoring, ALWAYS execute the validation command to verify zero regressions:

```bash
pnpm validate
```

This script runs the full quality check suite:

1. `pnpm format:tailwind` (Enforces canonical Tailwind class order)
2. `pnpm format` (Auto-formats code with Prettier)
3. `pnpm lint` (Validates ESLint rules)
4. `pnpm type-check` (Strict TypeScript verification with `tsc --noEmit`)
5. `pnpm build` (Ensures production Next.js build succeeds)

---

## 6. Git Commit Message Standards

When generating git commit messages, enforce strict **Conventional Commits**:

**Format**: `<type>(<optional scope>): <imperative description>`

**Rules**:

1. `<type>` must be one of: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
2. Keep the first line concise (under 72 characters).
3. Use lowercase for type, scope, and description.
4. Do NOT end the subject line with a period.
5. Use imperative mood (e.g., `"add goal filtering"` rather than `"added goal filtering"`).

**Examples**:

- `docs(deployment): add self-hosting guide and update README links`
- `feat(goals): add category filter dropdown`
- `fix(streak): correct streak calculation on missing days`
- `chore(deps): update prisma client to 7.9.1`

---

## 7. AI Agent Operational Guidelines

1. **Source Control Constraints**: Do NOT stage, commit, or push git changes unless explicitly requested by the user.
2. **File Integrity**: Preserve docstrings, license headers, and existing function signatures unless refactoring is requested.
3. **No Unverified Assumptions**: Verify file paths, schema fields, and library APIs against actual codebase files before introducing changes.
4. **Verification**: Always run `pnpm type-check` or `pnpm validate` to confirm code correctness after modifications.
