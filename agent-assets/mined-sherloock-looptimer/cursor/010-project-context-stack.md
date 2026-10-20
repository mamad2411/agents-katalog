---
description: TIMER project context and preferred tech stack/library choices.
alwaysApply: false
---

## Project context
- This project is **TIMER** (workout timer).
- Users create custom timers with intervals, loops, and advanced sequences.

## Tech stack (preferred)
- Next.js App Router + React + TypeScript
- TailwindCSS + Shadcn UI (preferred) + Radix only when needed
- Lucide icons
- React Hook Form + Zod
- Prisma + Prisma Studio
- `@tanstack/react-query`

## Syntax / conventions
- Prefer import aliases (`@/`) over deep relative paths.
- Always merge Tailwind classes with `cn`.
- Use `!!x` instead of `Boolean(x)`.
- Toasts: include an `id`, e.g. `toast.success(\"...\", { id: \"...\" })`.
- If using `useSearchParams()`, wrap it in a Suspense boundary (separate component + `<Suspense fallback={...}>`).
