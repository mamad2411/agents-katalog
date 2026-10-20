---
name: follow-secret-manager
description: Manage secrets and environment variables safely with a secret manager (Infisical default)
argument-hint: "[scope]"
related:
  - open-web-for-config-secret
  - deploy-to-cloudflare
  - deploy-to-vercel
  - deploy-to-railway
  - follow-deploy
  - deep-review-codebase
  - follow-tool-github-actions
  - run-audit

---
## Goal

Set up and use a secret manager to handle secrets and environment variables in the project safely, without letting the AI or the codebase know the real secret values

## Scope

Use for every workspace that needs secrets management — local development, CI/CD, and production. Supports several secret managers, but Infisical is the recommended default

## Execute

### 1. Choose Secret Manager

> Goal: pick the right secret manager

Latest: `@infisical/cli@0.43.136`, `@infisical/sdk@5.0.2` (verified 2026-09-24)

1. Default: use Infisical per [references/infisical.md](references/infisical.md)
2. Self-hosted: use Infisical self-hosted or HashiCorp Vault
3. Cloud-native: AWS Secrets Manager, Azure Key Vault, GCP Secret Manager, Cloudflare Secrets
4. if the user does not specify → use Infisical: its free tier works well, has a full CLI/SDK, and supports OIDC

### 2. Install And Authenticate

> Goal: install the CLI and authenticate

1. install the CLI per the chosen secret manager
2. for Infisical:
   - `bun add -g @infisical/cli` or `brew install infisical` or `scoop install infisical`
   - log in: `infisical login`
3. for CI/CD use machine identity / OIDC instead of personal tokens
4. verify access with `infisical secrets` or the equivalent command

### 3. Initialize Project

> Goal: link the project to the secret manager

1. run `infisical init` in the project root
2. select the project and the default environment (dev, staging, prod)
3. set `.infisical.json` with `workspaceId` and `defaultEnvironment`
4. monorepo: run `infisical init` in each workspace that needs it
5. `.infisical.json` can be committed (no sensitive data)

### 4. Collect Secrets Without AI Reading Values

> Goal: identify the needed secrets and point the user to fill them in personally

1. read `.env.example` or the project requirements
2. use `/open-web-for-config-secret` to open:
   - external service URLs (Stripe, OpenAI, Cloudflare, etc.) for creating API keys
   - the secret manager dashboard URL for pasting values
3. have the user copy API keys from the service dashboard and paste them into the secret manager themselves
4. the AI never receives secret values directly from the user, unless the user wants to enter them in the dashboard themselves

### 5. Store Secrets In Secret Manager

> Goal: store the secrets in the secret manager

1. local/CLI: `infisical secrets set KEY=value --env=dev`
2. file-based: `infisical secrets set CERT=@/path/to/cert.pem --env=dev`
3. dashboard: open the secret manager page and fill in the values yourself
4. organize with `--path` and `--tags`
5. use secret referencing: `${KEY}` for values that reference each other

### 6. Use In Local Development

> Goal: inject secrets for local dev without a `.env`, and verify the real values are used and not overridden by local files

1. run `infisical run --env=dev -- <command>` — dev: `bun run dev`, auto-reload: `--watch`, multiple commands: `--command="bun run build && bun run start"`
2. if the project primarily uses npm → substitute `npm run`; monorepo root scripts: `"secrets:dev": "infisical run --env=dev -- turbo run dev"`, `"secrets:build": "infisical run --env=prod -- turbo run build"`
3. verify: run `infisical export --env=dev` against the required keys (check key names only, never print values)
4. check local files that may win over the injected env — `.dev.vars`, `wrangler.toml`/`wrangler.jsonc` `[vars]`, `.env`/`.env.local` — if they hold placeholder/localhost values → tell the user to fix or remove them
5. run the real dev command and check the startup log reports the required keys as set — if any are missing → `/open-web-for-config-secret`
6. report the verification result as a table `| No. | Key | Winning Source | Status | Action |`

### 7. CI/CD Without Long-Lived Tokens

> Goal: use OIDC or machine identity in CI/CD

1. GitHub Actions: use `Infisical/secrets-action` with OIDC
2. create a machine identity in Infisical
3. set the OIDC Discovery URL: `https://token.actions.githubusercontent.com`
4. set the Subject: `repo:<owner>/<repo>:<context>`
5. workflow example:
   ```yaml
   permissions:
     id-token: write
     contents: read
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v7
         - uses: Infisical/secrets-action@v1.0.17
           with:
             method: oidc
             identity-id: <identity-id>
             project-slug: <project-slug>
             env-slug: dev
   ```
6. other CI/CD: use a short-lived temporary `INFISICAL_TOKEN`, then revoke it after use

### 8. Platform Integrations

> Goal: every platform pulls secrets from the secret manager

- Cloudflare: `infisical run --env=prod -- wrangler deploy` — no need to keep `CLOUDFLARE_API_TOKEN` in the repo
- Vercel: sync with the Infisical Vercel integration or inject via CI
- Railway: use `infisical run` before `railway up`
- GitHub: sync or OIDC
- Docker: install the Infisical CLI in the image, then `infisical run` in `CMD`
- Kubernetes: Infisical Operator or sync into Kubernetes secrets

### 9. SDK For Production

> Goal: programmatic access without hardcoded credentials

- install the SDK: `bun add @infisical/sdk` (if the project primarily uses npm, use `npm install @infisical/sdk`)
- authenticate: `client.auth().universalAuth.login({ clientId, clientSecret })`
- fetch one secret: `client.secrets().getSecret({ environment, projectId, secretName })`
- fetch all: `client.secrets().listSecrets({ environment, projectId, expandSecretReferences: true })`
- never hardcode `clientId`/`clientSecret` — use env vars or OIDC

### 10. Rotate And Audit

> Goal: care for the secrets long term

- dual-phase rotation for zero downtime
- rotation schedule: database 30-90 days, API keys 60-90 days, cloud 90 days
- use dynamic secrets where possible
- review audit logs every month
- set alerts for unauthorized access
- use secret scanning to detect leaks in git

## Rules

### 1. Security First

- never hardcode secrets in the codebase
- never commit `.env` or `.env.local` with real values
- the AI should not know secret values unless necessary
- for very sensitive secrets, have the user fill values into the dashboard themselves

### 2. Prefer OIDC

- CI/CD always uses OIDC instead of long-lived tokens
- create separate machine identities per environment
- use least-privilege access

### 3. Local Development

- use `infisical run` instead of `.env` files
- `.infisical.json` is committable but holds no secrets
- if `.env.example` is needed, keep only key names, no values

### 4. Onboarding Flow

- use `/open-web-for-config-secret` to point the user to the right URLs
- never let the user paste values to the AI
- have the user paste values directly into the secret manager dashboard

### 5. When Not To Use

- if a project has very few secrets and a very small team, a `.env` carried via USB/secure channel and never committed is still acceptable
- if the secret manager is down and production is affected → plan a fallback

- Use /deploy-to-cloudflare if needed
- Use /deploy-to-vercel if needed
- Use /deploy-to-railway if needed
- Use /follow-deploy if needed
- Use /deep-review-codebase if needed
- Use /follow-tool-github-actions if needed (secret manager)
- Use /run-audit if needed

## Expected Outcome

- a secret manager fully configured
- secrets are not in the repo or directly on developer machines
- local dev uses `infisical run` or the equivalent
- CI/CD uses OIDC or machine identity
- every platform pulls secrets from the secret manager
- the AI does not need to see real secret values
- audit logs and rotation are in use
