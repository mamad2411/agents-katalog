---
name: deploy-to-railway
description: Deploy an application to Railway with railway up until the deployment is live
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - deploy-to-cloudflare
  - deploy-to-vercel
  - run-deploy
  - run-build
  - resolve-errors
---

## Goal

Deploy the application to Railway with `railway up` until the deployment is live.

## Scope
- For related skills: `open-web-for-config-secret`, `deploy-to-cloudflare`, `deploy-to-vercel`, `run-deploy`

Covers CLI installation, project setup, deployment, deployment verification, and fixing errors.

## Execute

### 1. Install And Authenticate

> Goal: Install And Authenticate

Install the Railway CLI and set up authentication

Latest: `@railway/cli@5.62.1` (verified 2026-09-24) — install script `railway.com/install.sh` or npm global

1. Check whether the `railway` CLI exists; if not, install it with `bash <(curl -fsSL https://railway.com/install.sh)` or `bun add -g @railway/cli`
2. If not authenticated, run `railway login` (opens a browser for OAuth) or `railway login --browserless` for headless
3. For CI/CD, set `RAILWAY_TOKEN` or `RAILWAY_API_TOKEN` instead of interactive login
4. Verify authentication with `railway whoami --json`

### 2. Setup Project

> Goal: Setup Project

Set up the Railway project and service

1. Run `railway status --json` to check whether a linked project exists
2. If there is no linked project, choose one:
   - `railway up -y` to create a new project + service and deploy in one step
   - `railway link --project <name>` to link to an existing project
   - `railway init --name <name>` to create a new project
3. For a monorepo, set `rootDirectory` in service settings or use `railway up <path>`
4. Verify the link is correct with `railway status --json`

### 3. Configure Environment

> Goal: Configure Environment

Set up environment variables and domains

1. Use `/follow-secret-manager` to manage secrets, then inject with `infisical run --env=prod -- railway up` if using Infisical
2. If not using a secret manager: set environment variables with `railway variables set KEY=value --service <svc>`
2. Create `.env.example` to document the required variables
3. Set up a custom domain with `railway domain add <domain>` (if needed)
4. Verify variables with `railway variables list --json`

### 4. Deploy

> Goal: Deploy

Deploy the application to Railway

1. Run `/run-build` to build the application first (optional but recommended)
2. Run `railway up` to deploy in attached mode (streams logs)
3. For CI/CD, use `railway up --ci` or `railway up --detach`, then poll with `railway deployment list --json`
4. For agent-driven deploys, use `railway up -y` to skip prompts
5. Check the exit code: 0 = SUCCESS, 1 = FAILED

### 5. Watch Deployment

> Goal: Watch Deployment

Monitor the deployment until it is live

1. Check deployment status with `railway deployment list --json`
2. Wait until the status is `SUCCESS` (never report success before reaching this point)
3. If the status is `FAILED` or `CRASHED`, run `/resolve-errors`
4. Check the logs with `railway logs --lines 200`
5. Run `/watch-browser fix` with the deployment URL if a domain exists

### 6. Fix Errors

> Goal: Fix Errors

Fix any errors found

1. Run `/resolve-errors` when a problem is found
2. Identify the root cause from build logs or runtime logs
3. Fix the code according to the root cause
4. Run `railway redeploy` to redeploy without uploading new code (for config issues)
5. Or rerun `railway up` after fixing the code

### 7. Loop Until Live

> Goal: Loop Until Live

Repeat until the deployment is live

1. Use `/loop-until-complete` for repetition
2. Repeat the deploy and watch steps
3. Stop when the deployment status is `SUCCESS`
4. Confirm that no errors remain

## Rules

### 1. CLI Installation

- Install with `bash <(curl -fsSL https://railway.com/install.sh)` or `bun add -g @railway/cli`
- Check the version with `railway --version`
- Update with `railway upgrade` if a command is unrecognized

### 2. Authentication

- Use `railway login` for interactive auth (opens a browser)
- Use `railway login --browserless` for headless (device-code flow)
- Use `RAILWAY_TOKEN` for CI/CD (project-scoped)
- Use `RAILWAY_API_TOKEN` for CI/CD (account-scoped)
- `railway up` can sign up + deploy in one step

### 3. Deployment Modes

- Attached (default): `railway up` — streams logs until completion
- Detached: `railway up --detach` — returns immediately after queueing, poll with `railway deployment list --json`
- CI: `railway up --ci` — streams build logs only, exits when the build ends
- JSON: `railway up --json` — outputs JSON (implies CI mode)

### 4. File Handling

- Railway reads `.gitignore` by default
- Use `.railwayignore` for Railway-specific ignore patterns
- Use `--no-gitignore` to include ignored files
- Use `railway up <path>` to deploy a subdirectory
- Use `--path-as-root` to treat the path as the archive root

### 5. Verify Before Reporting

- Never report a successful deploy without checking the terminal status
- A returned `railway up --detach` means the build is queued, not successful
- Poll `railway deployment list --json` until the status is `SUCCESS` or `FAILED`
- exit code 0 = SUCCESS, exit code 1 = FAILED

### 6. Monorepo Support

- Set `rootDirectory` in service settings for a sub-app
- Use `railway up <path>` to deploy a subdirectory
- Each sub-app should be a separate service in the same project

### 7. CI/CD Integration

- Use `RAILWAY_TOKEN` for automated deployments
- Use `railway up --ci` in GitHub Actions
- Use the `deployment_status` event for post-deploy actions
- Automatically create PR environments with GitHub Actions

## Expected Outcome

- Railway CLI installed and authenticated successfully
- Project and service configured correctly
- Environment variables complete
- Deploy succeeds with status `SUCCESS`
- Deployment is live and working
- No build errors or runtime errors
- Custom domain works (if configured)
