---
description: Core QBook stack, structure, agent behavior, and git policy
alwaysApply: true
---

# QBook — Core Rules

## Stack
- Next.js 16, App Router (no `src/` directory)
- App routes at `app/`, UI components at `components/`
- Tailwind 4, shadcn/Base UI
- `next-themes` for dark mode (light + dark must receive equal attention)
- TypeScript strict mode
- Vercel deployment (push to main = auto-deploy to production)

## Coding Style
- Functional components only — no class components
- Prefer server components unless interactivity is needed
- One primary CTA per view (filled); secondary actions = outline/ghost
- Use existing design tokens from `app/globals.css` (`.qbook-type-*` scale)
- Geist UI font + Quicksand wordmark only

## Git Workflow
- Do NOT commit or push unless I explicitly ask or I run `/ship`
- Do NOT create branches or PRs unless I explicitly ask
- Use conventional commits: `type(scope): description`
- Do NOT use em-dashes or non-ASCII characters in commit messages
- Do NOT use PowerShell redirection operators (`>`, `>>`) — they produce UTF-16
- If a git hook or push fails, STOP and tell me. Do NOT retry or attempt to fix hooks.
- When `/ship` or I ask to commit: combine staging, committing, and pushing when possible:
  `git add -A && git commit -m "<message>" && git push`

## Agent Behavior
- Keep tasks scoped and incremental — do not refactor entire files unprompted
- If a command fails, stop and report. Do NOT enter retry loops.
- Prefer `@file` references over `@codebase` for targeted context
- When creating new components, follow existing patterns in `components/`

## File Structure Reference
- Foundations: `app/globals.css`, `app/(app)/layout.tsx`
- Shared components: `components/shared/`
- Booking components: `components/bookings/`
- Calendar: `components/calendar/`
- Profile: `components/profile/`
- Document/Print shell: `app/(document)/`
- UX spec: `docs/FRONTEND_UX_SPEC.md`
