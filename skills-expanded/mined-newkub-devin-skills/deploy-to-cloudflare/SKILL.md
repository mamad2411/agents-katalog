---
name: deploy-to-cloudflare
description: Deploy a project to Cloudflare Workers with wrangler until live, without Pages
argument-hint: "[scope]"
related:
  - follow-secret-manager
  - open-web-for-config-secret
  - run-deploy
---

## Goal

Deploy the application to Cloudflare Workers with wrangler, covering build, cleanup, watch, deploy, and fix until it succeeds. Do not use Cloudflare Pages.

## Scope

- Use Cloudflare Workers + `wrangler.toml` as the primary target
- For frontends (React/Vite/Solid/others), use Workers instead of Pages
- Support assets via `[assets]` in `wrangler.toml`
- Delete old Pages projects before deploying, if desired

## Execute

### 1. Detect Project Type

> Goal: Determine whether this is raw Workers or full-stack frontend + Workers

1. Check for `wrangler.toml`, `wrangler.jsonc`, `wrangler.json` files
2. If the file has `[[assets]]` or `[assets]` → frontend + Workers
3. If the file has `main = "worker/index.ts"` or `src/index.ts` → raw Workers
4. If no project exists yet → create `wrangler.toml` with `name`, `main`, `compatibility_date`, and `[assets]` (if there is a frontend)

### 2. Verify And Build

> Goal: Verify and build before deploying

1. Run `bun typecheck` and `bun run test`
2. Run `bun run build`
3. Verify that `dist/` or the build output contains `index.html` and static assets (if there is a frontend)
4. Check that the worker bundle builds successfully
5. Run `/deep-validate` before deploying

### 3. Authenticate

> Goal: Verify Wrangler auth

1. Run `wrangler whoami`
2. If not authenticated → use `/follow-secret-manager` or `/open-web-for-config-secret` to set `CLOUDFLARE_API_TOKEN`
3. For CI/CD, put `CLOUDFLARE_API_TOKEN` in GitHub/GitLab secrets

### 4. Clean Up Old Pages (Optional)

> Goal: Delete old Pages projects that are no longer needed

1. List old Pages projects with `wrangler pages project list`
2. Delete with the command:
   ```bash
   wrangler pages project delete <old-project-name> --yes
   ```
3. If there are old Workers to delete, use:
   ```bash
   wrangler delete <old-worker-name>
   ```
4. If no deletion is needed → skip this step

### 5. Configure wrangler.toml

> Goal: Configure Workers and get ready to deploy

1. Check that `name` in `wrangler.toml` matches the project name
2. Check that `main` points to the worker entrypoint
3. If there is a frontend, verify `[assets]`:
   ```toml
   [assets]
   directory = "dist"
   binding = "ASSETS"
   ```
4. If there is a D1 database, verify `[[d1_databases]]` is correct
5. Ensure `compatibility_date` is up to date

### 6. Deploy

> Goal: Push the deployment to Cloudflare Workers

1. For standard Workers (with or without a frontend):
   ```bash
   wrangler deploy
   ```
   or
   ```bash
   bun run deploy
   ```
2. If deploying via CI/CD, run the workflow and wait for the status
3. Record the deployment URL received

### 7. Watch And Fix

> Goal: Confirm it is live and working

1. Open the Workers URL or run `wrangler tail` to view logs
2. If it fails → check the logs for the root cause and fix the source
3. Repeat build and deploy until successful
4. Test the API endpoints and main pages

### 8. Commit And Push

> Goal: Sync with git

1. `git add -A` and `git commit`
2. `git push`
3. Record the deployment URL in `README.md` or docs

### 9. Report

> Goal: Summarize the results

1. Report the project type, worker name, URL, and status
2. List the environment and secrets used
3. If any old Pages projects were deleted, note them too

## Rules

- Use Cloudflare Workers as the primary target; do not use Pages for new deployments
- Use `/follow-secret-manager` to manage `CLOUDFLARE_API_TOKEN` before deploying
- Build successfully before deploying
- Use the `wrangler` CLI
- If there is a frontend, use `[assets]` in `wrangler.toml`, not Pages
- If it fails → check logs with `wrangler tail` or the deployed URL, then fix
- Do not commit before the deployment succeeds
- Use /run-deploy if needed

## Expected Outcome

- Deployed to Cloudflare Workers successfully
- The Workers URL works
- Git is synced
- No errors remain
