---
alwaysApply: true
---

FOR FRONTEND DEVELOPER

Tech stack:

- Next.js 16
- React 19
- Tailwind CSS v4
- TypeScript

Rules:

- Always use App Router
- Never use pages router unless requested
- Use Tailwind v4 syntax (`@import "tailwindcss"`)
- Prefer server components
- Prefer server actions over API routes
- Avoid deprecated APIs
- If old code appears, migrate it to modern patterns

## Rules

- Always use **"use client"** when a component includes interactivity (onClick, useState, etc.).
- Import shadcn/ui components from `@/components/ui`.
- Do NOT hardcode colors; always use Tailwind variables like `bg-primary`, `text-foreground`, etc.
- Always define variants using `cva`.
- Follow tweakcn theme style: **modern-minimal**, clean spacing, rounded-xl corners, and subtle hover transitions.
- Component must be **fully typed** with TypeScript.

## Context

The main UI folders are:

- `src/components/ui/` → shadcn UI primitives (Button, Card, Input, Dialog, etc.)
- `src/components/layout/` → Navbar, Footer, Sidebar
- `src/components/templates/` → reusable section blocks (Hero, FeatureGrid, Testimonials)
- `src/app/` → Next.js routes and pages
- `src/lib/utils.ts` → includes `cn()` helper
- `styles/tweakcn.css` → imports theme from tweakcn.com

## Goals

When a developer requests:

- **"create a new component"** → generate it following the shadcn pattern.
- **"update component style"** → refactor with tweakcn theme variables.
- **"use existing UI"** → automatically import from `@/components/ui`.
- **"build a full section"** → combine UI primitives into templates.

## Style Guidelines

- Keep components minimal, composable, and accessible.
- Use Tailwind spacing scale: `p-4`, `px-6`, `gap-4`, etc.
- Use `motion.div` (framer-motion) for subtle animations when needed.
- Keep JSX readable, avoid inline styles.
- Always export named components (no default export).
- Follow file naming pattern: lowercase kebab-case, e.g. `feature-grid.tsx`.

## Output Format

Always return:

1. Full `.tsx` file code block.
2. Short explanation of design choice.
3. Import path for usage.
