# Grova AI Guidelines & Project Rules

Refer to [AGENTS.md](AGENTS.md) for full project architecture, goals, tech stack, and engineering conventions.

## Core Directives
1. **Tech Stack**: Next.js 16 (App Router), React 19, TypeScript 5, Tailwind CSS v4, Prisma 7, Neon PostgreSQL, NextAuth.js v5 (Auth.js), Zod v4, pnpm.
2. **Server Components First**: Use Server Components by default. Include `"use client"` only for client interactivity.
3. **Database Client**: Always import `db` from `@/lib/db`.
4. **Validation Command**: Run `pnpm validate` before finalizing changes.
5. **Git Commits**: Enforce strict **Conventional Commits** (`<type>(<scope>): <description>`).
