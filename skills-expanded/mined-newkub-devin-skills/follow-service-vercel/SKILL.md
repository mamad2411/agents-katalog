---
name: follow-service-vercel
description: Deploy applications on Vercel with serverless and edge functions
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - deploy-to-vercel
  - watch-browser
  - resolve-errors
  - loop-until-complete

---

## Goal

Deploy applications on the Vercel platform with auto-build, preview deployments, serverless functions, and edge functions

## Scope
- For related skills: `open-web-for-config-secret`, `follow-service-vercel`, `deploy-to-vercel`

Covers installing the Vercel CLI, linking a project, configuring, building, deploying, environment variables, serverless/edge functions, and CI/CD

## Execute

### Workflows

| Topic  | Workflow |
|--------|----------|
| Setup  | `workflows/setup-vercel/SKILL.md` — Vercel CLI, login, link project |
| Config | `workflows/config-vercel/SKILL.md` — env vars, `vercel.json` config |
| Verify | `workflows/verify-connection/SKILL.md` — CLI auth, project linked, env vars complete |

Read `workflows/<name>/SKILL.md` per topic and follow the flow there — do not execute from this table directly

### 1. Install Vercel CLI

> Goal: Install and authenticate the Vercel CLI

Latest: `vercel@60.1.3` CLI, `@vercel/node` builder (verified 2026-09-26)

1. Run `bun add -D vercel`
2. Or use `bunx vercel` without installing
3. Run `bunx vercel login` to authenticate

### 2. Link Project

> Goal: Connect the project with Vercel

1. Run `bunx vercel link` in the project directory
2. Confirm the project settings
3. Or use `VERCEL_ORG_ID` and `VERCEL_PROJECT_ID` for CI/CD

### 3. Configure vercel.json

> Goal: Define the deployment configuration

`vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "src/index.ts",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "/src/index.ts" }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

### 4. Framework Presets

> Goal: Vercel supports auto-detection for frameworks

- Next.js: uses the `next` preset automatically
- Nuxt: uses the `nuxt` preset with SSR
- SvelteKit: uses the `sveltekit` preset
- Remix: uses the `remix` preset
- Astro: uses the `astro` preset
- Vite: uses the `vite` preset for a static build

### 5. Build And Deploy

> Goal: Build and deploy the application

1. Run `bun run build` or `nitro build` for Nitro projects
2. Verify the build succeeds and the output is ready
3. Run `bunx vercel deploy` for a preview deployment
4. Run `bunx vercel deploy --prod` for production
5. For Nitro: set the `vercel` preset in the nitro config, then run `nitro build` and `bunx vercel deploy --prebuilt`

### 6. Environment Variables

> Goal: Set environment variables

1. Run `bunx vercel env add KEY_NAME`
2. Or use the dashboard to manage variables
3. Use `vercel env pull .env.local` to sync to local
4. Define `NODE_ENV`, `API_URL`, and secrets

### 7. Serverless Functions

> Goal: Create serverless functions in the `api/` directory

`api/hello.ts`:
```typescript
import type { VercelRequest, VercelResponse } from '@vercel/node'

export default function handler(req: VercelRequest, res: VercelResponse) {
  res.status(200).json({ message: 'Hello from Vercel' })
}
```

### 8. Edge Functions

> Goal: Create edge functions for edge deployment

`api/edge.ts`:
```typescript
export const config = {
  runtime: 'edge'
}

export default async function handler(req: Request) {
  return new Response('Hello from Edge Function')
}
```

### 9. Watch Deployment

> Goal: Check the deployment with a browser preview

1. Do `/watch-browser fix` with the deployment URL
2. Verify the page loads successfully
3. Check console errors and network errors
4. Do `/resolve-errors` when a problem is found
5. Do `/loop-until-complete` until the deployment is live

### 10. CI/CD Deployment

> Goal: Set up automated deployment

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Vercel
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: oven-sh/setup-bun@v2
      - run: bun install
      - run: bunx vercel deploy --prod --token=${{ secrets.VERCEL_TOKEN }}
```

## Rules

### 1. Framework Detection

- Vercel auto-detects the framework from `package.json`
- Define `buildCommand` in `package.json` scripts or `vercel.json`
- Specify `outputDirectory`: `dist`, `build`, or `.next` per framework
- Use `bun install` for Bun projects

### 2. Build Process

- Always run `nitro build` before deploying Nitro projects
- Verify the build output succeeds
- Check the bundle size

### 3. Environment Variables

- Use the `vercel env` CLI or the dashboard
- Use `/follow-secret-manager` to manage `VERCEL_TOKEN` and secrets before syncing to Vercel or CI/CD
- Use `vercel env pull` to sync to local
- Never hardcode secrets

### 4. Functions

- Serverless functions live in the `api/` directory
- Edge functions use `runtime: 'edge'`
- Define `regions` in `vercel.json` when needed

### 5. Deployment

- Every PR creates a preview deployment automatically
- Use `bunx vercel deploy` for preview
- Use `bunx vercel deploy --prod` for production
- Set protection rules for production deployments
- Use `/watch-browser fix` for monitoring
- Do `/loop-until-complete` until the deployment is live

### 6. Advanced Configuration

- Define `rewrites` in `vercel.json` for URL routing
- Define `headers` for security and caching
- Use `crons` for scheduled functions
- Use `ignoreCommand` to skip builds


## Expected Outcome

- Application successfully deployed on Vercel
- Auto-build configuration supporting multiple frameworks
- Serverless and Edge functions working correctly
- CI/CD pipeline deploying automatically to both preview and production
- Environment variables managed securely
- Deployment live with no console or network errors

## Guide

Additional references:

- [references/vercel-overview.md](references/vercel-overview.md) — overview of the Vercel platform
- [references/vercel-website.md](references/vercel-website.md) — main Vercel links

