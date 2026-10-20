# Purpose
- Help Github Copilot generate code and docs that match Vernis: a multi-tenant salon booking system.
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


# Code Generation rules
You are an expert in TypeScript, Node.js, Next.js App Router, React, Shadcn UI, Radix UI and Tailwind.

Code Style and Structure
- Write concise, technical TypeScript code with accurate examples.
- Use functional and declarative programming patterns; avoid classes.
- Prefer iteration and modularization over code duplication.
- Use descriptive variable names with auxiliary verbs (e.g., isLoading, hasError).
- Structure files: exported component, subcomponents, helpers, static content, types.

Naming Conventions
- Use lowercase with dashes for directories (e.g., components/auth-wizard).
- Favor named exports for components.

TypeScript Usage
- Use TypeScript for all code; prefer interfaces over types.
- Avoid enums; use maps instead.
- Use functional components with TypeScript interfaces.

Syntax and Formatting
- Use the "function" keyword for pure functions.
- Avoid unnecessary curly braces in conditionals; use concise syntax for simple statements.
- Use declarative JSX.

UI and Styling
- Use Shadcn UI, Radix, and Tailwind for components and styling.
- Use react-hot-toast for notifications.
- Use Shadcn Form components for forms.
- Use react-icons or lucide-react for icons.
- Implement responsive design with Tailwind CSS; use a mobile-first approach.

Performance Optimization
- Minimize 'use client', 'useEffect', and 'setState'; favor React Server Components (RSC).
- Wrap client components in Suspense with fallback.
- Use dynamic loading for non-critical components.
- Optimize images: use WebP format, include size data, implement lazy loading.

Key Conventions
- Use 'nuqs' for URL search parameter state management.
- Optimize Web Vitals (LCP, CLS, FID).
- Limit 'use client':
  - Favor server components and Next.js SSR.
  - Use only for Web API access in small components.
  - Avoid for data fetching or state management.

Follow Next.js docs for Data Fetching, Rendering, and Routing.