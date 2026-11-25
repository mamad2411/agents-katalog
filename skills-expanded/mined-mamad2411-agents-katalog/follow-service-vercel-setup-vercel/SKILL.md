---
name: follow-service-vercel-setup-vercel
description: Install the Vercel CLI, authenticate, and link the project with Vercel — first-time setup before deploy
related:
  - follow-service-vercel
---

## Goal

Install the Vercel CLI, authenticate, and link the project with Vercel — first-time setup before deploy

## Scope

- Install the `vercel` CLI, `vercel login`, `vercel link`
- Create `.vercel/project.json` containing `orgId`/`projectId`
- If already linked → verify only; config env/vercel.json → `workflows/config-vercel/SKILL.md`; deploy → `/deploy-to-vercel`

## Execute

### 1. Check Prerequisites

> Goal: Confirm the project is ready and not yet linked

1. Check `package.json` for `vercel` already present, and see whether `.vercel/project.json` exists
2. If `.vercel/project.json` already exists → skip to the verify step
3. Add `.vercel` to `.gitignore` if it is not there

### 2. Install CLI

> Goal: Have the Vercel CLI ready to use

1. Run `bun add -D vercel` or use `bunx vercel` without installing
2. Verify the CLI works with `bunx vercel --version`

### 3. Authenticate

> Goal: CLI logs in to the Vercel account

1. Run `bunx vercel login` and let the user confirm via email/provider
2. Verify auth with `bunx vercel whoami`
3. For CI/CD → store `VERCEL_TOKEN` via `/follow-secret-manager`

### 4. Link Project

> Goal: Connect the project with a Vercel project

1. Run `bunx vercel link` in the project root, then pick the scope and project (new or existing)
2. Verify `.vercel/project.json` contains `orgId` and `projectId`
3. For CI → store `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` via `/follow-secret-manager`

### 5. Verify

> Goal: Setup is ready to deploy

1. Run `bunx vercel pull` to sync project settings/env to local
2. Do `/run-verify` for lint, typecheck
3. If verify fails → do `/resolve-errors` max 3 rounds, then stop and report
4. Success → do `/suggest-next-action`

## Rules

- Never commit `.vercel/` or `VERCEL_TOKEN`
- Use `bunx vercel` or a dev dependency — never rely on an unpinned global install
- Use official docs as the primary source — if unsure → see https://vercel.com/docs

## Expected Outcome

- Vercel CLI installed and authenticated
- Project linked with `.vercel/project.json`
- Ready for `workflows/config-vercel/SKILL.md` or `/deploy-to-vercel`
