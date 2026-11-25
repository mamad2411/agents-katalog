---
name: ship
description: Pre-deploy gate, deploy, and smoke-test in one pass — runs build/checks, deploys (Vercel by default), then verifies the live URL actually works. For shipping with confidence.
argument-hint: [optional: target, e.g. "production" or "preview"]
allowed-tools: Bash, Read, Glob, Grep, WebFetch
---

Take the current project from "I think it's done" to "verified live." **Do not deploy until the pre-checks pass.** A broken deploy is not acceptable.

## Step 0 — Identify the deploy path
Check the project for its own deploy tooling first (vercel.json, netlify.toml, Dockerfile, a `deploy` script in package.json, CI config). **Default to Vercel CLI** if nothing else is specified. Confirm the target: **preview by default**, production only if the user said so (`$ARGUMENTS`).

## Step 1 — Pre-flight gate (block on failure)
Run only what the project actually has, in order:
- Install deps if needed — use the project's package manager (pnpm/npm/yarn per lockfile).
- **Typecheck / lint / build** — a passing build is the hard gate.
- **Tests** if present.
If any hard gate fails, **STOP and report the failure. Do not deploy.**

## Step 2 — Deploy
**Before a production deploy, confirm with the user first** — it's outward-facing and hard to undo. Preview deploys may proceed without asking. Run the deploy (`vercel` for preview, `vercel --prod` for production, or the project's own command) and capture the deployment URL. If the CLI needs login or project-linking, surface that to the user instead of hanging on the prompt.

## Step 3 — Smoke-test the live deployment
Never trust "deploy succeeded" alone. Hit the actual URL (WebFetch / curl):
- Main page returns 200 with real content (not an error/placeholder page).
- One or two key routes if obvious.

## Step 4 — Report
- Gate results (build/tests).
- Deployed URL + target.
- Smoke-test verdict: **Live and verified ** or **Deployed but smoke-test failed — investigate **.
Keep it tight. **Never claim "shipped" if the smoke test didn't pass.**
