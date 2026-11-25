---
name: follow-lib-elysia-deploy-elysia
description: Deploy Elysia — bun build, production notes, platform targets
argument-hint: "[platform]"
related:
  - follow-lib-elysia
  - use-bun-native-api
  - follow-secret-manager
  - check-secrets
  - resolve-errors
---

## Goal

Prepare and deploy an Elysia app to production — `bun build`, env config and platform targets

## Scope

Use when deploying an Elysia API — covers production build, env vars, process management and platform notes (VPS, Docker, serverless that supports Bun)

## Execute

### 1. Prepare Production Config

> Goal: check config before deploying

1. Check the env vars the app uses — do `/check-secrets env-vars`; secrets via `/follow-secret-manager`, never commit
2. Verify the target's `Bun.version` supports the Elysia version used
3. Use `process.env.PORT` for the port — don't hardcode
4. Check CORS, error handling (`.onError()`) and logging are production-ready

### 2. Build

> Goal: build the app for production

1. Bun runs TypeScript directly — `bun run src/index.ts` is usable in production if the runtime has Bun
2. Bundle to cut cold start/image size: `bun build src/index.ts --target bun --outfile dist/index.js` — see the official docs for the latest flags
3. Compile to a single binary (optional): `bun build --compile src/index.ts --outfile app` — a standalone executable with no Bun install needed
4. Test the build output locally before deploying

### 3. Choose Deploy Target

> Goal: pick a platform that supports Bun

1. VPS/bare metal: install Bun then run `bun run` or the compiled binary — use a process manager (systemd, pm2) for restarts
2. Docker: base image `oven/bun` — multi-stage build to shrink the image
3. Platforms with native Bun support — see the official docs at `https://elysiajs.com` for the latest deploy guides
4. If a platform doesn't support Bun → use the compiled binary or Docker

### 4. Verify Deployment

> Goal: smoke test the production deployment

1. The health endpoint responds correctly (add `.get('/health', () => 'ok')` if missing)
2. Test the main routes and validation on the production URL
3. Check logs have no errors; secrets don't leak in responses
4. If broken → do `/resolve-errors` then report

## Rules

- Never commit secrets/env — always use `/follow-secret-manager`
- Use `process.env.PORT` — platforms assign the port themselves
- Use `--target bun` when building — Elysia is a Bun-first framework
- Always test the build output locally before pushing the deploy
- Use `/use-bun-native-api` for Bun runtime APIs (`Bun.serve`, `Bun.env`, flags)
- Use `/follow-lib-elysia` for the full reference

## Expected Outcome

- Production build (bundle or binary) runs
- Env vars/secrets handled correctly
- Deployed app answers the health check and main routes
- No secrets leaked in logs/responses
