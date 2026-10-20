# TIMER project — agent overrides

Project-specific rules (shared rules are loaded via opencode.json instructions).

## Project context

- **TIMER**: workout timer app; users create custom timers with intervals, loops, and advanced sequences.
- Next.js App Router, React, TypeScript, TailwindCSS, Shadcn UI, Lucide, React Hook Form + Zod, Prisma, TanStack Query.

## Conventions

- Prefer `@/` import aliases; merge Tailwind classes with `cn`.
- Do **not** extract Tailwind class strings into constants; keep classes inline in JSX.
- Use `!!x` instead of `Boolean(x)`; toasts must include an `id`.
- Wrap `useSearchParams()` in a Suspense boundary (separate component + `<Suspense>`).

## When applying rules

- State which rule file(s) you applied (short names are fine).
