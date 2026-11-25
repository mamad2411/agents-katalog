---
name: frontend-development
description: Use when building or structuring a React/Next.js + TypeScript + Tailwind frontend, choosing libraries, or wiring design tokens. Provides the opinionated blessed-library stack and the React-vs-Next decision, all on-token to DESIGN.md and accessible to WCAG AA.
---

# Frontend Development

**Announce at start:** "I'm using claude-engineer:frontend-development to build the frontend on the blessed stack."

## React vs Next.js (default decision)
- **Next.js (App Router)** for marketing/content sites and content+app hybrids (SEO, RSC, server data).
- **Vite SPA (React)** for dashboards/SaaS behind auth and design-system/library work (no SEO need).
- Rule of thumb: anonymous crawler needs real content, or you need a server data layer → Next.js; everything behind a login and API-bound → Vite SPA.

## Blessed libraries (June 2026 defaults - full table + versions in `references/frontend-stack.md`)
| Need | Default |
|---|---|
| UI primitives | shadcn/ui (own the code) over Radix/Base UI |
| Styling | Tailwind CSS v4 (`@theme`) + cva + tailwind-merge + clsx |
| Server/data state | TanStack Query (or Next server components/actions) |
| Client state | Zustand |
| Forms + validation | react-hook-form + Zod |
| Routing (non-Next) | React Router (TanStack Router if TS-first) |
| Tables | TanStack Table |
| Charts | Recharts (via shadcn charts) |
| Animation | motion (ex-Framer Motion) |
| Icons | lucide-react (+ custom typed SVG icons) |
| Toasts / cmd palette / DnD / upload | Sonner / cmdk / dnd-kit / react-dropzone + presigned uploads |

## Non-negotiables
1. **On-token only** - consume DESIGN.md tokens via Tailwind `@theme`/CSS vars; no hardcoded values (`claude-engineer:design-system`).
2. **TypeScript strict** - full strict flags (see reference); no `any` escapes.
3. **WCAG AA by construction** - semantic HTML, keyboard nav, focus management, ARIA, reduced-motion. This is a hard gate (`claude-engineer:testing-and-quality`).
4. **Tested** - Vitest + React Testing Library for components; Playwright for E2E flows.
5. **Monorepo placement** - apps in `apps/`, shared UI/config in `packages/` (`claude-engineer:monorepo-and-tooling`).

**Full detail:** read `references/frontend-stack.md` (project structure, exact versions, tsconfig strict flags, ESLint flat config, token wiring, a11y checklist) on demand.

## Red flags - STOP
- Reaching for a library outside the blessed list without a reason recorded in `docs/conventions.md`.
- Inline styles / magic numbers instead of tokens.
- Building an interactive component that isn't keyboard-operable.
