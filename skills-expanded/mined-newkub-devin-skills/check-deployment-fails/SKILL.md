---

name: check-deployment-fails
description: Check deployment failures from CI/CD and cloud (GitHub Actions, Cloudflare Workers)
argument-hint: "[limit]"
related:
  - resolve-errors
  - resolve-cicd
  - report
  - suggest-next-action
  - follow-service-vercel
  - follow-service-cloudflare
  - open-cloudflare-workers
  - run-deploy

---

## Goal

Check deployment and CI/CD failures from GitHub Actions and Cloudflare Workers, then summarize them

## Scope

Used to inspect all failures from CI/CD (GitHub Actions) and cloud deployment (Cloudflare Workers) without modifying or re-running anything

See also: /follow-service-vercel, /follow-service-cloudflare, /open-cloudflare-workers

## Execute

### 1. Verify Authentication

> Goal: check the auth of the tools used

1. Run `gh auth status` to check GitHub
2. Run `wrangler --version` to check Cloudflare
3. Run `wrangler whoami` when cloud status is needed
4. If not authenticated → do `/ask-me` to have the user log in

### 2. List CI/CD Failures

> Goal: collect GitHub Actions failures

1. Do `/resolve-github-actions-fails` to find failed workflow runs
2. Cap the count by `limit` (default 50)
3. Record: repo, workflow, branch, commit, event, started at, url

### 3. List Cloud Failures

> Goal: collect Cloudflare Workers failures

1. Do `/resolve-cloudflare-worker-fails` to find workers with deploy/health failures
2. Cap the count by `limit` (default 50)
3. Record: worker, type, latest deployment, status, errors

### 4. Aggregate Failures

> Goal: merge failures from all sources

1. Combine CI/CD and cloud data into one list
2. Mark the source type: `github-actions` or `cloudflare`
3. Sort by most recent occurrence

### 5. Build Report

> Goal: summarize into a table

1. Use `/report` with columns:
   - No.
   - Source
   - Name
   - Status
   - Time
   - URL / Notes
2. Break down sub-summaries per source: GitHub Actions count, Cloudflare count
3. State the total failure count

### 6. Suggest Next Action

> Goal: recommend the next steps

1. Do `/suggest-next-action` to suggest debug, re-run, watch, or fix
2. When there are Cloudflare failures → recommend `/resolve-cicd` or `/resolve-cloudflare-worker-fails`
3. When there are GitHub Actions failures → recommend `/resolve-github-actions-fails`

## Rules

### 1. Read Only

- Never re-run, cancel, delete, deploy, or modify anything
- Only query and report

### 2. Secret Safety

- Do not expose tokens, account IDs, or credentials in the output
- Use the existing `gh` and `wrangler` credentials

### 3. Rate Limit

- With large data, batch and paginate
- On API 429 responses, wait and retry

### 4. Scope

- Covers GitHub Actions and Cloudflare Workers by default
- For other sources such as Vercel or Railway, state them in the argument
- Use /run-deploy if needed
- Use /resolve-errors if needed


## Expected Outcome

- The list of deployment failures from CI/CD and cloud
- A table sorted by most recent occurrence
- Source, name, status, time, url/notes identified
- No deployment or workflow modified
