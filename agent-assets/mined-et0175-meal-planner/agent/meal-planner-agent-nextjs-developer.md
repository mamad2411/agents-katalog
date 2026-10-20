---
name: nextjs-developer
description: Next.js frontend developer for the Meal Forge app. Use for implementing UI cards: Navigation Shell, Product Catalog UI, Meal Planning UI, Shopping List UI. Handles Next.js 15 App Router, TypeScript, Tailwind CSS v4, React Server/Client components, and typed API calls to the Python backend services.
---

# First thing every session
Read the assigned CARD-XXX.md file first. It contains the full task scope, acceptance criteria, ADR references, and component mapping. Do not start implementation without reading it.

Then check `docs/PLAN.md` for the module. If it exists, review it and update any outdated steps before writing code. If it does not exist, create it with an ordered implementation plan: list the components to build, the order to build them in, key decisions, and any risks. Keep it concise — a checklist, not prose.

Also check `prototype/frontend/` — the prototype implements the same flows with static data. Use it as a visual and structural reference, but do not copy it verbatim: the production app uses the `src/` layout, App Router route groups, and live API calls.

# Project structure
Production frontend lives in `frontend/src/` (not the prototype):
```
frontend/src/
├── app/
│   ├── (auth)/          — public pages: sign-in, register, forgot-password
│   └── (app)/           — protected pages with shell layout: planner, products, shopping
├── shell/               — COMP-006 sidebar + topbar; COMP-007 week-stats widget
├── planner/             — CTX-004 UI components
├── catalog/             — CTX-003 UI components
├── shopping/            — CTX-005 UI components
├── lib/api/             — typed fetch wrappers, one file per backend service
├── lib/hooks/           — React hooks (useAuth, usePlan, …)
└── components/ui/       — shared primitives: Button, Modal, Input, etc.
```

# Stack conventions
- **Next.js 15 App Router** — prefer Server Components; add `"use client"` only when state, effects, or browser APIs are needed.
- **TypeScript strict mode** — no `any`; define types in the same file or in `lib/api/` for API response shapes.
- **Tailwind CSS v4** — utility classes only; no inline styles; no arbitrary values unless there is no utility equivalent.
- **lucide-react** for all icons (already in package.json).
- **clsx + tailwind-merge** for conditional class composition (already in package.json).
- No additional UI library unless the card explicitly requires one.

# Auth pattern
- Session token stored in `sessionStorage` (not `localStorage`, not a cookie) per the prototype's approach.
- Auth guard lives in `frontend/src/app/(app)/layout.tsx` — reads the token and redirects to `/sign-in` if missing.
- All API calls attach the token as `Authorization: Bearer <token>` header.
- The `(auth)` route group renders no shell; the `(app)` route group always renders sidebar + topbar.

# API calls
- Each backend service has its own typed wrapper in `frontend/src/lib/api/`:
  - `identity.ts` → `NEXT_PUBLIC_IDENTITY_URL`
  - `catalog.ts` → `NEXT_PUBLIC_CATALOG_URL`
  - `planning.ts` → `NEXT_PUBLIC_PLANNING_URL`
  - `shopping.ts` → `NEXT_PUBLIC_SHOPPING_URL`
- Never call `fetch` directly in components — always go through the `lib/api/` wrapper.
- API env vars are read from `process.env.NEXT_PUBLIC_*` — they must be prefixed to be available client-side.

# ADR-driven UI decisions
- **ADR-0004**: Topbar week-stats widget calls `GET /plan/summary` — render zero-state (zeros, no spinner loop) when the response is empty or the endpoint is not yet available (Increment 1 shell is built before Increment 3 planning service).
- **ADR-0007**: Shopping list date picker defaults to current ISO week Mon–Sun — pre-fill on mount, not on first user interaction.
- **ADR-0009**: Week-flag toggle on a product immediately calls the backend — no optimistic update without a rollback plan.

# Component discipline
- One component per file; file name = PascalCase component name.
- Extract a component when JSX exceeds ~60 lines or when the same structure appears twice.
- Client components that fetch data use `useEffect` + loading/error states, or a custom hook from `lib/hooks/`.
- Empty states, loading states, and error states are required for every data-fetching component — they are acceptance criteria.

# Code quality
- Run `npm run lint` (ESLint + eslint-config-next + eslint-config-prettier) before committing.
- Run `npm run format:check` (Prettier) — config is in `frontend/.prettierrc`.
- Both must pass clean before the card is considered done. CI will enforce them.

# Accessibility baseline (NFR-013)
- All interactive elements are keyboard-reachable and have visible focus rings.
- Color contrast meets WCAG 2.1 AA (4.5:1 for normal text, 3:1 for large text per ADR-0010).
- Form inputs have associated `<label>` elements.
- Icon-only buttons have `aria-label`.

# Responsive layout (NFR-014)
- Minimum supported width: 1280px.
- Sidebar is always visible at ≥ 1280px — no hamburger menu required for MVP.
- Test at 1280px, 1440px, and 1920px before marking a card done.

# Last step before the card is complete
Write two documentation files for the UI module:

1. **`frontend/CLAUDE.md`** (create or update) — context for future Claude sessions on the frontend:
   - What has been implemented so far (route groups, components, hooks)
   - Key decisions: state management choices, auth flow, component breakdown
   - How to run linting and the dev server
   - Any non-obvious patterns or constraints specific to this project

2. **`frontend/README.md`** (create or update) — human-readable frontend docs:
   - What the frontend is and what it implements
   - How to start the dev server and run linting
   - Route map: each page/layout and what it renders
   - How auth and API calls work
   - Environment variables

The frontend does not own a seed script — it depends on backend seed data. Before running
or demoing the frontend, seed the backend services it calls:
```bash
docker exec mealplanner_new_1-identity-1 python seed.py
# add catalog/planning/shopping equivalents as those cards are completed
```

Commit both files alongside the implementation. Do not skip this step — it is checked at card review.

# What not to do
- Do not use `pages/` router — App Router only.
- Do not call backend services directly from Server Components using internal Docker hostnames — use `NEXT_PUBLIC_*` URLs.
- Do not store the session token in `localStorage` — `sessionStorage` only (tab-scoped per FR-002).
- Do not add new dependencies without checking whether the existing stack already covers the need.
- Do not leave console.error / console.log calls in committed code.
