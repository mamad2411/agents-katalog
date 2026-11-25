# AGENTS.md
Prescriptive instructions for AI coding agents (Claude Code, Copilot, Gemini CLI, etc.) — short, deterministic, and tied to PRD.md.

> Important: This document is authoritative for agents. Any change to core platform decisions (DB provider, Auth provider, backend-ai introduction) requires updating PRD.md first and explicit human approval.

--------------------------------------------------------------------------------
1. QUICK SUMMARY
--------------------------------------------------------------------------------
Project: Personal web portfolio (public site) + Admin dashboard (CRUD for CV sections). Frontend: Next.js (App Router, SSG/ISR). Backend: Next.js API routes (serverless) or NestJS if scale requires. No backend-ai for MVP.

Primary anchors: PRD.md and DESIGN.md (use those tokens & acceptance criteria).

--------------------------------------------------------------------------------
2. MUST-RUN COMMANDS (copy-paste exact)
--------------------------------------------------------------------------------
# Prereqs (one-time)
corepack enable
corepack prepare pnpm@latest --activate
# Alternative to opt into pnpm 12 (if you want Rust rewrite channel)
# pnpm self-update next-12

# Create repo skeleton (once)
mkdir portfolio-repo && cd portfolio-repo
pnpm init -w -y
git init

# Create workspaces (exact)
pnpm dlx create-next-app@latest frontend -- --typescript --eslint --app --use-pnpm
pnpm dlx create-nestjs@latest backend --package-manager=pnpm --typescript
mkdir -p packages/shared

# Install (root workspace)
pnpm install

# Dev / build / test / lint (root)
pnpm -w dev
pnpm -w build
pnpm -w start
pnpm -w test
pnpm -w lint

# Prisma migrations (backend)
# set DATABASE_URL in env first
cd backend
pnpm prisma migrate dev --name init
pnpm prisma generate

# Security hardening (must after upgrade)
# Ensure Next.js upgraded to patched release if running Next.js <= 16.3.2:
# npm install next@16.3.3
# or pin engines.node: "24.x" in package.json for Vercel compatibility

--------------------------------------------------------------------------------
3. STRUCTURE (feature-based — REQUIRED)
--------------------------------------------------------------------------------
project-root/
  frontend/
    src/
      features/
        <feature>/
          components/
          hooks/
          services/
          types/
          <feature>.test.ts
    design/
    public/
  backend/
    src/
      features/
        <feature>/
          controller/
          service/
          repository/
          <feature>.test.ts
    prisma/
      schema.prisma
  packages/
    shared/
      src/
        schemas/
        types.ts
  .github/workflows/
  AGENTS.md
  PRD.md
  DESIGN.md

Rules:
- repository/ is the only layer that talks to DB.
- controller/ must be thin (validation + mapping).
- DTO/Zod schemas live in packages/shared and imported by both sides.

--------------------------------------------------------------------------------
4. FINAL TECHNOLOGY DECISIONS (do not change without PRD approval)
--------------------------------------------------------------------------------
- Node: 24.x (LTS) — production target. See Node release schedule.
- Package manager: pnpm >= 12 recommended (opt-in channel for v12).
- Frontend: Next.js (App Router; SSG/ISR).
- Language: TypeScript ^6.
- Styling: Tailwind CSS + shadcn/ui. Motion: Framer Motion.
- Backend: Next.js API routes (serverless) OR NestJS + Prisma + PostgreSQL.
- DB: PostgreSQL (managed).
- Storage: Supabase Storage or S3 + CDN.
- Auth: Supabase Auth (email/password) or NextAuth configured with Supabase.
- CI: GitHub Actions.
- Observability: Sentry (errors) + basic analytics.

--------------------------------------------------------------------------------
5. VERSION NOTES & SECURITY (validate before deploy)
--------------------------------------------------------------------------------
- Node 24 is the recommended LTS for production builds; pin engines.node to "24.x". citeturn2search2
- pnpm 12 is a recent Rust-rewrite release (opt-in); using pnpm 12 may require `pnpm self-update next-12` on developer machines/CI. Validate lockfile compatibility in CI. citeturn1search0
- Next.js emergency security patches (Aug 2026) fixed critical RCEs in 15.5.24 and 16.3.3 — **if** your project uses Next.js, ensure version >= 16.3.3 before public deploy (especially if you enable image optimization/AVIF). Upgrade immediately if affected. citeturn0search6turn0search1
- TypeScript 6.0 is current major; ensure CI toolchains support `tsc@^6`. citeturn0search0

--------------------------------------------------------------------------------
6. CONVENTIONS (strict)
--------------------------------------------------------------------------------
- Language for UI and comments shown to humans: Bahasa Indonesia.
- File/folder naming:
  - React components: PascalCase.tsx
  - Utilities/modules: kebab-case.ts
  - Variables/functions: camelCase
- Single source of truth for tokens: DESIGN.md.
- Controller thin → Service heavy → Repository sole DB access.
- All strings surfaced to user must be i18n-ready (id-ID default).
- All runtime secrets via env / platform secret store (no .env in repo).

--------------------------------------------------------------------------------
7. TESTING (mandatory)
--------------------------------------------------------------------------------
- Unit: Vitest (frontend + backend). Minimum coverage: 60% core modules.
- Integration: Supertest/Vitest for API routes.
- E2E: Playwright for critical flows (add project → upload media → publish → public view).
- PR rule: `pnpm -w test` must pass before merge.
- Add test stubs for every new feature; failing tests block merge.

--------------------------------------------------------------------------------
8. SECURITY & DATA (rules)
--------------------------------------------------------------------------------
- Never commit credentials or .env to repo.
- Session cookie: HttpOnly + Secure; do not store tokens in localStorage.
- Sanitize all rich-text with DOMPurify before rendering.
- File uploads max: 10MB per image (enforced server-side).
- Rate-limit auth endpoints; block after 5 failed attempts (exponential backoff).
- Audit logs: every admin write action (who, when, what) stored and immutable.

--------------------------------------------------------------------------------
9. BOUNDARIES — DO NOT DO WITHOUT PERMISSION
--------------------------------------------------------------------------------
Ask human approval before:
- Changing DB provider (Postgres).
- Replacing Auth provider.
- Adding new top-level dependency (especially native modules).
- Introducing backend-ai or LLM storing user data externally.
- Changing Node major (>24) or engines.node in package.json.

Forbidden actions (never):
- Commit secrets / credentials.
- Force-push to main or production.
- Drop existing production migrations without documented rollback & approval.

--------------------------------------------------------------------------------
10. PROTOCOL FOR CHANGES (every change must follow)
--------------------------------------------------------------------------------
1. Create feature branch `feat/<area>-short-desc`.
2. Run lint & tests locally (`pnpm -w lint` & `pnpm -w test`).
3. If DB schema changes: add Prisma migration + run restore test locally.
4. Describe affected files and rationale in PR body; include migration plan and rollback steps.
5. At least 1 reviewer and CI green before merge.

--------------------------------------------------------------------------------
11. GIT WORKFLOW
--------------------------------------------------------------------------------
- Trunk-based preferred (short-lived feature branches).
- Commit messages: Conventional Commits.
- PR must include checklist: lint, tests, migration, docs.
- No direct pushes to main.

--------------------------------------------------------------------------------
12. SAFETY CATEGORIES (one-line rules)
--------------------------------------------------------------------------------
- ALWAYS allowed: read files, run tests, run lint, run dev.
- ASK FIRST: add dependency, change DB provider, alter engines.node.
- NEVER: commit secrets, force push main, drop migrations in prod.

--------------------------------------------------------------------------------
13. QUICK REFERENCE — useful links
--------------------------------------------------------------------------------
Node releases / schedule: Node.js Releases. urlNode.js Releasesturn2search2  
pnpm v12 announcement / notes. urlpnpm 12 Release Notesturn1search0  
Next.js security advisory / guidance (Aug 2026). urlNext.js security release (Aug 2026)turn0search6  
TypeScript 6.0 release notes. urlTypeScript 6.0 Releaseturn0search0

--------------------------------------------------------------------------------
14. HOW AGENTS SHOULD BE USED
--------------------------------------------------------------------------------
- Agents implement tasks (scaffold, tests, small PRs) only within feature branches.
- Agents must include in PR description: files changed, tests added, manual QA steps, and potential impacts.
- Agents must not merge PRs; humans approve all merges.

--------------------------------------------------------------------------------
END OF AGENTS.md
