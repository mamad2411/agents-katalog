---
name: bun-workflow
description: Use this skill when you need a Bun runbook (dev, build, lint, typecheck, tests, migrations, and verification steps).
---

# Bun Workflow Skill

Use this skill to run and verify a project locally.

## Core commands (if your project uses Bun)

- Dev server: `bun dev` (Next.js on :3000)
- Build: `bun run build`
- Lint: `bun run lint`
- Type-check: `tsc --noEmit`
- Drizzle migrations:
  - Generate from schema: `bunx drizzle-kit generate`
  - Apply: `bunx drizzle-kit migrate`
  - Studio: `bunx drizzle-kit studio`

## Notes

- Avoid mixing package managers within one project.
- Ensure env vars in `.env` (e.g., `DATABASE_URL`, your auth provider keys) before running.
- For tests, prefer targeted scripts first, then the full suite (whatever your `package.json` defines).

## Cost & performance verification (practical)

When you make changes intended to reduce Vercel cost/latency, always verify you didn’t trade correctness for speed:

- Run the full checks (`lint`, `typecheck`, `test`, `build`) and spot-check the affected routes.
- Watch for accidental over-revalidation (e.g., broad `revalidatePath`) and client bundle bloat (`'use client'` creep).

Reference:

- nextjs-cost-performance skill

## References

- Your `package.json`
- Your DB config/schema (if applicable)
