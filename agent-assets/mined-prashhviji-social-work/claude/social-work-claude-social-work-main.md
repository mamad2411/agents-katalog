# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"The Device" is a full-stack Next.js application for managing solar-powered, offline adaptive learning kiosks deployed in rural India. It has two main surfaces:
- **Marketing portal** — public-facing pages (landing, about, gallery) under the `(marketing)` route group
- **Management dashboard** — teacher/admin tools for tracking students, devices, villages, submissions, and reports under the `(dashboard)` route group

## Commands

```bash
npm run dev          # Start dev server (http://localhost:3000)
npm run build        # Production build
npm run lint         # ESLint
npx prisma migrate dev --name <name>   # Create/apply migration
npx prisma generate  # Regenerate Prisma client
npx prisma db seed   # Seed demo data
```

**Windows note:** Stop the dev server before running `prisma generate` — the Next.js process locks the Prisma query engine DLL and causes `EPERM` errors.

## Tech Stack

- **Next.js 16** (App Router) with **Supabase Auth** (email/password)
- **TypeScript**, **Tailwind CSS v4**, **shadcn/ui** (new-york style, components in `src/components/ui/`)
- **PostgreSQL** via **Prisma** (schema at `prisma/schema.prisma`)
- **Zustand** + **React Query** for state management (provider in `src/components/providers.tsx`)
- **Recharts** for charts, **Framer Motion** for animations

## Architecture

### Route Groups

- `src/app/(marketing)/` — public pages with `MarketingNav` and footer. Pages: landing (`page.tsx`), about, gallery.
- `src/app/(dashboard)/` — authenticated views with `DashboardSidebar` (fixed 256px left sidebar). Pages: dashboard, students, students/[id], devices, devices/[id], villages, teachers, submissions, submissions/[id], reports, courses, courses/[subjectId], my-submissions, my-submissions/new.
- `src/app/login/` — standalone login page with Supabase email/password auth.
- `src/app/api/` — API routes: `submissions` (POST), `submissions/[id]` (PATCH for teacher review).

### Authentication & Role-Based Access

Middleware (`src/middleware.ts`) enforces role-based routing:
- **ADMIN** — all pages
- **TEACHER** — dashboard, students, devices, submissions, reports
- **STUDENT** — dashboard, courses, my-submissions

### Key Domain Models (Prisma)

Village → Device → Student → StudentProgress (per SkillNode). Subjects contain a tree of SkillNodes (self-referential `parentId`). Students submit project work via Submissions, reviewed by Users (teachers/admins). Devices track SyncEvents and PowerLogs.

### Design System

Custom "Earth & Sun" theme defined in CSS variables:
- **Ochre** (`#C8893A`), **Terracotta** (`#B84C27`), **Forest** (`#2D5016`)
- **Fonts:** `Fraunces` for headings (`--font-heading`), `DM Sans` for body (`--font-body`)
- shadcn/ui components use CSS variables for theming (`cssVariables: true`)

### Path Aliases

`@/` maps to `src/` (configured in `tsconfig.json`).

## Demo Credentials

- Admin: `admin@project.org` / `admin123`
- Teacher: `teacher@project.org` / `teacher123`
- Student: `student@project.org` / `student123`
