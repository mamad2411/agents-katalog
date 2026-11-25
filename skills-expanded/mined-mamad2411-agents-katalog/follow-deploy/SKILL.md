---
name: follow-deploy
description: Set up complete deployment configuration and CI/CD
argument-hint: "<cloudflare|vercel|railway|verify> [scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - follow-tool-github-actions
  - follow-service-cloudflare
  - follow-service-vercel
  - deploy-to-railway
  - run-deploy
---

## Goal

Set up deployment configuration and a CI/CD pipeline for automated deployment

## Scope

Set up deployment for Vercel, Cloudflare, Railway, and other platforms, with CI/CD

## Execute

### 1. Select Platform

> Goal: choose the platform best suited to the project type and requirements

Choose the platform best suited to the project

1. Determine the project type and requirements
2. Choose the appropriate platform:
   - Cloudflare Workers/Pages: run `/follow-service-cloudflare`
   - Vercel: run `/follow-service-vercel` and `/deploy-to-vercel`
   - Railway: run `/deploy-to-railway`
3. Verify the platform configuration is ready

### 2. Setup Environment Variables

> Goal: configure environment variables completely for deployment

Set up environment variables for deployment

1. Create `.env.example` for the required environment variables
2. Use `/follow-secret-manager` to manage secrets before deploying to the platform
3. Set environment variables in the platform:
   - Cloudflare: use `wrangler secret put`
   - Vercel: use the Vercel dashboard or CLI
   - Railway: use `railway variables set KEY=value` or the Railway dashboard
3. Verify the environment variables are complete and correct

### 3. Setup CI/CD

> Goal: set up GitHub Actions for automated deployment

Set up GitHub Actions for automated deployment

1. Run `/follow-tool-github-actions` to configure GitHub Actions
2. Choose workflows as needed:
   - Base CI/CD: `ci.yml` (lint, typecheck, test)
   - Deployment: `deploy-staging.yml`, `deploy-production.yml`
   - Security: `codeql.yml`, `dependabot.yml`
3. Set up Renovate for dependency updates
4. Set up Release-it for automated releases (if needed)

### 4. Setup Platform-Specific Configuration

> Goal: configure the config files for the chosen platform

Set up configuration for the chosen platform

- Cloudflare: configure `wrangler.jsonc` for Workers/Pages
- Vercel: configure `vercel.json` or `next.config.js`
- Railway: configure `railway.json` or environment variables

### 5. Test Deployment

> Goal: test deployment in the staging environment before production

Test deployment in the staging environment

1. Deploy to the staging environment
2. Verify the deployment succeeded
3. Test that the application works
4. Check the logs for errors

### Workflows

> Goal: dispatch to the platform workflow based on the argument

| Platform  | Workflow |
|-----------|----------|
| `cloudflare` | `workflows/deploy-cloudflare/SKILL.md` — delegates to `/deploy-to-cloudflare` |
| `vercel`    | `workflows/deploy-vercel/SKILL.md` — delegates to `/deploy-to-vercel` |
| `railway`   | `workflows/deploy-railway/SKILL.md` — delegates to `/deploy-to-railway` |
| `verify`    | `workflows/verify-deploy/SKILL.md` — post-deploy verify: URL, version, health, logs, rollback |

1. If the argument names a platform → read `workflows/deploy-<platform>/SKILL.md` and follow the flow there — do not execute from this table directly
2. If no platform is given → follow steps 1-5 to choose a platform first

## Rules

### 1. Platform Selection

- Choose the platform by project type and requirements
- Cloudflare: best for edge computing and serverless
- Vercel: best for Next.js and React applications
- Railway: best for full-stack applications that need a database

### 2. Environment Variables

- Environment variables must be set up completely
- Use `/follow-secret-manager` to manage all secrets before deploying
- Use `.env.example` to document the required variables
- Never hardcode secrets in code
- Use the platform's secrets management

### 3. CI/CD

- A base CI/CD workflow is required (lint, typecheck, test)
- Deployment workflows must separate staging and production
- Security workflows are required for production
- Dependency updates are required (Renovate)

### 4. Platform Configuration

- Configuration must be correct for the platform
- Proper error handling is required
- Proper logging is required
- Proper monitoring is required

### 5. Testing

- Deployment must be tested in staging before production
- Verify that the application works
- Check the logs for errors

- Use /open-web-for-config-secret if needed (deploy)
- Use /run-deploy if needed

## Expected Outcome

- Platform configuration fully set up
- Environment variables fully set up
- CI/CD pipeline runs automatically
- Deployment works in the staging environment
