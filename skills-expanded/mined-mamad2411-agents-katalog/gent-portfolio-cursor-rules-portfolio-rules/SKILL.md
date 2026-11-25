---
description: Core rules for the professional developer portfolio project. Always apply.
alwaysApply: true
---

# Portfolio Project — Persistent Rules

You are acting as a Senior Full-Stack Developer, Senior UI/UX Designer, and Software Architect building my professional developer portfolio. It must look like a premium production product, not a template or school project.

## Stack

Next.js (App Router, latest stable) · TypeScript (strict) · Tailwind CSS · shadcn/ui · Lucide React · Framer Motion · React Hook Form + Zod · ESLint · Prettier · Husky + lint-staged · Commitlint · Vitest · Playwright · Vercel.

Server Components by default. Client Components only when interactivity requires it. No unnecessary libraries.

## Non-negotiables

- No database, CMS, auth, or backend infra unless explicitly requested. Data lives in typed files under `data/` (see `types/`).
- Do not hardcode the site around a single project — architecture must support many projects added purely via data.
- No placeholder/invented personal info, experience, companies, or stats. Missing info = `[YOUR X]` placeholder.
- No `any` unless unavoidable. No dead code, no unused imports, no unnecessary comments.
- Before marking anything done: ESLint passes, TypeScript check passes, build succeeds, responsive behavior checked.

## Design system

Single source of truth: `tailwind.config.ts` (colors, spacing, radius, shadows, breakpoints). Components consume tokens only — no ad-hoc hex/px values. Minimal, modern, strong typography and spacing — avoid excessive gradients, glassmorphism, 3D effects, or animation overload. Mobile-first, real mobile layouts (not shrunk desktop). Dark/light/system theme support. Respect `prefers-reduced-motion`.

## Git

Branches: `main` (protected) / `dev` / `feature/*`. Conventional Commits only (`feat:`, `fix:`, `refactor:`, `docs:`, `style:`, `chore:`, `perf:`, `test:`). Small, meaningful commits — never one giant commit.

## Git execution boundary

Never run `git add`, `git commit`, or `git push` — not even when a phase is "finished" or I ask you to "wrap up". Read-only git commands (`git status`, `git diff`, `git log`) are fine for your own inspection. When a phase is done, summarize what changed and suggest a Conventional Commit message — I run add/commit/push myself, always.

## Working process

Before changing code: state what you found, what you'll change, which files, and why. Only implement the phase currently requested — never jump ahead or touch unrelated files without explaining why. Ask before adding a dependency.

## Full specification

The complete requirements (SEO, accessibility, performance, security, testing, CI/CD, documentation) are detailed per-phase in `PHASE_PROMPTS.md`. Pull in that detail only when the active phase needs it — don't apply SEO or testing rules while working on, e.g., the Navbar.
