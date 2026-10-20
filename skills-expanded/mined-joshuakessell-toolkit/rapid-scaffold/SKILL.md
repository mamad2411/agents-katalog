---
name: rapid-scaffold
description: Scaffold a deployable web app skeleton in minutes. Use when starting a new project under time pressure, when the user says kickoff, scaffold, new app, walking skeleton, or get something deployed fast.
---

# Rapid Scaffold

Goal: a deployed hello-world at a public URL before any feature code exists. Everything else is negotiable.

## Default stack (deviate only if the assignment forces it)

- Next.js (App Router) + TypeScript + Tailwind. `pnpm create next-app@latest <name> --ts --tailwind --app --src-dir --no-eslint --use-pnpm --yes`
- shadcn/ui only if the UI needs real components: `pnpm dlx shadcn@latest init -d` then add components on demand, never all at once.
- If the assignment is API-only or realtime-heavy, Joshua's Fastify + Drizzle patterns are fair game — but Next.js API routes cover 90% of rapid builds with zero extra deploy config.

## Sequence

1. Scaffold, `git init`, first commit immediately.
2. `gh repo create <name> --private --source=. --push` (private unless told otherwise).
3. Deploy the untouched skeleton NOW: `vercel --prod --yes`. Confirm the URL loads before writing any feature code. This proves the entire pipeline while stakes are zero.
4. Env vars: add via `vercel env add` the moment a secret exists. Never hardcode; never discover a missing env var at the worst possible moment.

## Parallel interleave for the opening minutes

Classify before launching; never leave the user idle during a long command:

| Command | ~Time | Mode | Meanwhile (user) |
|---|---|---|---|
| `pnpm create next-app` | 60-90s | blocking | `vercel login` (URL flow) |
| `git init` + first commit | 2s | fast | — |
| `vercel --prod --yes` (first) | 45-90s | blocking (need URL) | provision the DB: Neon project → copy DATABASE_URL |
| `pnpm add drizzle-orm pg …` | 20-40s | blocking | add DATABASE_URL in the Vercel dashboard |
| `pnpm dev` | continuous | ALWAYS background | — |
| `shadcn add <components>` | 10-20s | fast | — |
| later deploys | 45-90s | background-safe once URL is known | click-test the previous deploy |

The pattern generalizes: anything continuous runs in the background; anything long and
blocking gets a one-line "meanwhile:" pulled from the human-task queue built at kickoff.
Doc lookups and exploration go to subagents concurrently — only distilled answers enter
the main thread.

## Anti-patterns under time pressure

- Do not hand-roll config (eslint flat configs, custom webpack, monorepo tooling). Defaults ship.
- Do not add a database before the core loop works with in-memory state, unless persistence IS the assignment.
- Do not install a component library, an ORM, and an auth provider speculatively. Each addition must be pulled in by a task on the MVP list.
- SQLite/in-memory beats Postgres when the demo only needs a short-lived demo. State the tradeoff in one plain sentence rather than silently under-engineering.
