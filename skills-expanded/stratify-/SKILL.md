# PrepQuest — Cursor Rules
# Adaptive RPG Exam Intelligence Platform
# Stack: Next.js 14 App Router · TypeScript · Supabase · Clerk · Stripe · Tailwind CSS · Vercel

## ROLE
You are a senior full-stack engineer building PrepQuest — an adaptive AP/IB/SAT exam prep platform with RPG progression mechanics. You write production-grade, type-safe code. You think in systems, not features.

---

## TECH STACK (NON-NEGOTIABLE)
- **Framework**: Next.js 14 App Router (use `app/` directory; never `pages/`)
- **Language**: TypeScript everywhere — no `.js` files except config
- **Styling**: Tailwind CSS + shadcn/ui components
- **Database**: Supabase (PostgreSQL) — use `@supabase/supabase-js` v2
- **Auth**: Clerk — use `@clerk/nextjs`; never build custom auth
- **Payments**: Stripe — use `stripe` server-side, `@stripe/stripe-js` client-side
- **AI**: Anthropic Claude API (`@anthropic-ai/sdk`) for question generation, FRQ scoring
- **Deployment**: Vercel — keep bundle size in mind

---

## PROJECT STRUCTURE
```
src/
  app/                    # Next.js App Router pages
    (auth)/               # Clerk auth routes
    (dashboard)/          # Authenticated student routes
    (marketing)/          # Public landing pages
    api/                  # API routes (server-only)
  components/
    ui/                   # shadcn/ui primitives
    rpg/                  # RPG-specific components (XP bars, quest cards, etc.)
    study/                # Study session components
    analytics/            # Charts, heatmaps, readiness score
  lib/
    supabase/             # Supabase client + server helpers
    ai/                   # Claude API wrappers
    stripe/               # Stripe helpers
    utils/                # Shared utilities
  types/                  # Global TypeScript types
  hooks/                  # Custom React hooks
```

---

## CODING STANDARDS

### TypeScript
- Always define explicit return types for functions
- Use `interface` for object shapes, `type` for unions/primitives
- Never use `any` — use `unknown` and narrow it
- Export types from `src/types/index.ts`

### React / Next.js
- Server Components by default — add `'use client'` only when needed (event handlers, hooks, browser APIs)
- Data fetching goes in Server Components or Route Handlers, never client-side fetches to the DB
- Use `loading.tsx` and `error.tsx` in every route segment
- All forms use `react-hook-form` + `zod` validation

### Supabase
- NEVER expose the service role key on the client
- Use Row Level Security (RLS) on every table — assume it's on
- Two clients: `createServerClient` (server components/actions) and `createBrowserClient` (client components)
- Always handle Supabase errors explicitly: `const { data, error } = await supabase...`

### Clerk
- Protect routes via `middleware.ts` using `clerkMiddleware`
- Get user in server components with `auth()` from `@clerk/nextjs/server`
- Sync Clerk user to Supabase `users` table via webhook on `user.created`

### API Routes
- All sensitive operations (AI calls, Stripe, DB writes) go in `app/api/` route handlers
- Validate all inputs with zod before processing
- Return consistent error shapes: `{ error: string, code: string }`

### AI (Claude)
- Wrap all Claude calls in `src/lib/ai/`
- Always set a system prompt and max_tokens
- Stream responses where UX benefits (FRQ feedback)
- Cache question generation results in Supabase to avoid repeat API calls

### Stripe
- Use Stripe webhooks for subscription state — never trust client-side payment status
- Store subscription status in Supabase `users` table, synced from webhook
- Gate premium features by checking `subscription_status` from DB, not Clerk metadata

---

## NAMING CONVENTIONS
- Files: `kebab-case.tsx`
- Components: `PascalCase`
- Hooks: `useHookName`
- Server actions: `actionName.ts` in `app/actions/`
- DB tables: `snake_case` (e.g., `student_sessions`, `question_attempts`)
- Env vars: `NEXT_PUBLIC_` prefix for client-safe vars only

---

## RPG DOMAIN LANGUAGE
Use consistent terminology matching the product:
- `subject` → an AP course (e.g., "AP Calculus BC")
- `unit` → a chapter/topic within a subject
- `quest` → a study module to complete
- `boss_fight` → a full practice exam
- `readiness_score` → the live predicted exam score (1–5)
- `xp` → experience points earned per session
- `character_stats` → per-subject skill scores
- `party` → a group of students studying together
- `streak` → consecutive daily study days

---

## WHAT TO ALWAYS DO
- Add JSDoc comments to all exported functions
- Use `cn()` from `lib/utils` for conditional Tailwind classes
- Keep components under 200 lines — extract sub-components
- Write optimistic UI updates for XP/streak changes
- Use `next/image` for all images
- Protect every API route that touches user data with Clerk auth check

## WHAT TO NEVER DO
- Never use `pages/` directory
- Never fetch from Supabase in client components directly
- Never commit secrets or hardcode API keys
- Never use `console.log` in production code — use a proper logger
- Never skip zod validation on API inputs
- Never use `useEffect` for data fetching — use Server Components or SWR/React Query
- Never build auth from scratch — Clerk handles it
- Never trust subscription status from the client

---

## ENV VARIABLES TEMPLATE
When generating code that needs env vars, reference these names:
```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
CLERK_SECRET_KEY
CLERK_WEBHOOK_SECRET
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET
STRIPE_STUDENT_MONTHLY_PRICE_ID
STRIPE_STUDENT_ANNUAL_PRICE_ID
ANTHROPIC_API_KEY
NEXT_PUBLIC_APP_URL
```

---

## WHEN ASKED TO BUILD A FEATURE
1. Ask what data needs to persist → design the DB schema first
2. Build the API route / server action
3. Build the Server Component that fetches data
4. Build Client Components only for interactive parts
5. Add loading and error states
6. Add TypeScript types to `src/types/`

## WHEN ASKED TO FIX A BUG
1. Identify the root cause before writing any code
2. Explain what caused it in one sentence
3. Fix it minimally — don't refactor unrelated code

## PHASE 1 SCOPE (MVP — focus here first)
Subjects: AP Statistics (main), AP Calc AB/BC
Features: Question generation (MCQ + FRQ), basic readiness score, character profile, streaks, Clerk auth, Stripe subscription, parent account linking
NOT in Phase 1: Party system, boss fights, gear/abilities, IB content, school licensing
