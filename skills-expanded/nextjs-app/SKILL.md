---
name: nextjs-app
description: Bootstrap a new Next.js (App Router, TypeScript) web app with current packages and no deprecated APIs. Use when the user wants to start, scaffold, or set up a new Next.js project, a React web app, a SaaS or dashboard or landing page on Next.js, or asks to "create a new nextjs app". Handles private, open-source, and private-plus-open-source variants, Prisma and Postgres, next-auth, Tailwind, and shadcn or Mantine.
---

# nextjs-app

Bootstrap a new Next.js web app the way this owner builds them: App Router,
TypeScript strict, current stable packages, no deprecated APIs, a clean feature
structure, and the house git and CI workflow.

First read these shared rules (they override anything you remember):
`../shared/house-rules.md`, `../shared/no-ai-attribution.md`,
`../shared/git-and-ci.md`, `../shared/docs-and-context.md`,
`../shared/hardening.md`, and (for public repos) `../shared/open-source-docs.md`.

## Step 0. Get the brief, then ask the variant questions (hard stop)

This is a hard stop. Do not run any scaffolding command until the user has
answered.

First, get the project brief: one paragraph on what the app does, its main
features, target users, and any hard constraints. If the user has not given one,
ask for it. The brief drives naming, the route groups, and the data model.

Then present the variant choices below, wait for the answers, and build. If a
choice has multiple options, ask; do not assume. Ask in one batch.

1. Repo visibility: private, open-source (public), or private-plus-open-source
   (a private product with a separate public core or SDK). See
   `references/variants.md`.
2. Data layer: Prisma + Postgres (default), a different DB, or none yet.
3. Auth: next-auth v5 (default), Clerk, or none yet.
4. UI kit: shadcn/ui + Tailwind (default), Mantine, or plain Tailwind.
5. Deploy target: Vercel (default) or self-host (Docker).
6. Package manager: pnpm (default) or npm.

If the user already answered some of these in their prompt, do not re-ask.

## Step 1. Verify environment and current versions

- Check Node (`node -v`, want the current LTS or newer) and the package manager.
- Run `scripts/check-latest.sh` to get live stable versions from npm. Pin those,
  not versions from memory. See `../shared/house-rules.md` rule 2.
- Pull current Next.js docs before writing framework code
  (`../shared/docs-and-context.md`). Recent Next.js ships docs in
  `node_modules/next/dist/docs/`; read the relevant guide and obey deprecation
  notices.

## Step 2. Scaffold with the official CLI

Use the official generator so you inherit its current defaults:

```
pnpm create next-app@latest <name> --typescript --app --eslint --tailwind --src-dir --import-alias "@/*"
```

Adjust flags to the answers. Let the CLI pick the current Next major; do not
force a version you remember. After it runs, read `references/stack.md` for the
exact dependency set to add and `references/structure.md` for the folder layout.

## Step 3. Apply house structure and conventions

- Folder layout, data layer, auth, and server-action patterns:
  `references/structure.md`.
- Dependency set and why each is chosen: `references/stack.md`.
- Variant-specific setup (LICENSE, README tone, monorepo split, secret
  handling): `references/variants.md`.
- Production hardening so the shipped app does not leak secrets or internals:
  `../shared/hardening.md`.

## Step 4. Git, CI, docs, security

- Initialize git, set the branch model, and wire CI and auto-merge per
  `../shared/git-and-ci.md`.
- Write the CI workflow and quality gates from `references/quality-gates.md`.
- Add `docs/` and README per `../shared/docs-and-context.md`.
- For a public repo, ship the full open-source docs set (LICENSE, CONTRIBUTING,
  CODE_OF_CONDUCT, SECURITY, issue and PR templates, CHANGELOG via release-please)
  per `../shared/open-source-docs.md`, and run the open-source hard gate in
  `../shared/no-ai-attribution.md` before the first push.
- Gitignore `.env*`, add `.env.example`. Never commit secrets.

## Step 5. Verify before declaring done

Run the quality gates in `references/quality-gates.md` (typecheck, lint,
production build, and a dev-server smoke check). Report real results. If a build
fails, fix it or say so with the output. Do not claim done on an unbuilt app.
