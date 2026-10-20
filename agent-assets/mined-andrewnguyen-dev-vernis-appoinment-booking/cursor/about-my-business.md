---
alwaysApply: true
---
# Purpose
- Help Cursor generate code and docs that match Vernis: a multi-tenant salon booking system.
- MVP rules: no staff selection by customers, multi-service appointments, payments, categories.

# Business & Product
BUSINESS.name: "Vernis"
BUSINESS.type: "Multi-tenant SaaS for salons"
BUSINESS.region_default_tz: "Australia/Sydney"
BUSINESS.users:
  - "Salon owners" (manage catalog, clients, appointments, billing)
  - "Staff"
  - "Clients" (book multi-service appointments)
VALUE_PROP:
  - Simple online booking
  - Multi-service cart-like booking flow
  - Integrated payments
  - Ready for salons to onboard quickly

# Architecture & Stack
STACK.frontend: Next.js 15 (App Router), TypeScript, TailwindCSS, shadcn/ui
STACK.backend: Next.js Route Handlers + Server Actions
STACK.db: Vercel Postgres via Prisma
STACK.auth: BetterAuth (Prisma adapter)
STACK.email: Resend (React Email templates)
STACK.payments: Stripe (Checkout + Webhooks)
STACK.job/cron: Vercel Cron (HTTP-triggered later)
STACK.validation: Zod
STACK.dates: date-fns + date-fns-tz
STACK.logging: lightweight console (Sentry later)
STACK.testing: Vitest + Playwright (later)