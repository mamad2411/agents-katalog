---
alwaysApply: false
---

# Project

- Framework: Next.js (App Router) + TypeScript
- Node: >=20
- Data: Prisma (schema at prisma/schema.prisma)
- Auth/Billing: Clerk, Paddle
- Docs generators: `npm run ai:docs` (schema/api/components)

# Conventions for AI

- Prefer existing utilities over new deps.
  - Database: `src/utils/database/*`
  - Paddle: `src/utils/paddle/*`
  - Emails: `src/utils/email/send-email.ts` and `src/emails/*`
  - API types: `src/lib/api.types.ts`
- API: Use App Router handlers under `src/app/api/**/route.ts`.
  - Validate inputs with `zod`
  - Return typed responses; reuse helpers in `src/lib` and `src/utils`
- UI: Use components in `src/components/*` and UI primitives in `src/components/ui/*`

# Commands

- Dev: `npm run dev`
- Build: `npm run build`; Start: `npm run start`
- Lint/format: `npm run lint && npm run prettier:check` (fix: `npm run lint:fix && npm run prettier`)
- Prisma:
  - After schema change: `npm run db:generate && npm run db:push`
  - For iterative dev: prefer `db:push`; create proper migrations when stabilizing: `npm run db:migrate`
- Docs: After changing schema, API routes, or components: `npm run ai:docs`

# Guardrails

- Do not introduce new packages unless necessary.
- Do not hardcode secrets; use `.env` (add new vars to `.env.example` if introduced).
- Use absolute paths in commands in automated steps.
- Keep edits focused; update related docs if behavior or contracts change.

# Checklists

- Added API route? Handle auth if needed, update docs via `ai:docs`.
- Changed Prisma schema? generate + push, verify impacted utils, update docs.
- Sending emails? Use `send-email.ts` and existing templates in `src/emails/*`.
- Working with Paddle? Use helpers in `src/utils/paddle/*` (don’t call SDKs directly elsewhere).

# References

@prisma/schema.prisma
@src/lib/api.types.ts
@src/utils/email/send-email.ts
