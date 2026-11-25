---
name: follow-create-bot-github-app
description: Build a real GitHub App — manifest, JWT auth, installation, webhooks
argument-hint: "[features]"
---

## Goal

Build a GitHub App actually registered with GitHub (not a bot wrapper): app manifest, private key auth, webhook endpoint, permissions, and installation flow

## Scope

Use for building a GitHub App from scratch with TypeScript/Bun — covers app registration, JWT auth, installation tokens, webhook handlers, and event subscriptions — if you only need a simple bot running through Actions, use `/follow-create-bot-github`

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, following the conventions in `/update-devin-global-skills`
2. Run `/deep-review-codebase` to summarize the tech stack in use
3. Record the stack choice with reasons for reference

### 2. Gather Requirements

> Goal: Know what the app must do

1. Ask the user: app name, purpose (checks, PR automation, issue triage, sync), and the events to subscribe to
2. Identify the required permissions per least-privilege: `issues`, `pull_requests`, `checks`, `contents`, `metadata`
3. Identify the runtime: `Bun` (default) or `Node.js`
4. Identify the hosting: webhook endpoint (Workers/Vercel/Railway) or self-hosted

### 3. Register GitHub App

> Goal: Have complete app credentials

1. Open the GitHub App creation page with `/open-web`, or guide the user to `Settings → Developer settings → GitHub Apps → New`
2. Or use the app manifest flow: POST the manifest JSON, then redirect the user to receive a `code` → exchange it for credentials
3. Store `APP_ID`, `PRIVATE_KEY` (PEM), `WEBHOOK_SECRET`, `CLIENT_ID`, `CLIENT_SECRET`
4. Use `/follow-secret-manager` for storage — never commit or log the private key

### 4. Setup Project

> Goal: Project structure ready with auth

1. Use `/search-npm-libraries` to pick a library: `@octokit/app` (low-level) or `probot` (framework) — default `probot` for event-driven bots
2. Create `src/app.ts`, `src/index.ts`, `src/handlers/`, `src/config.ts`
3. Create a webhook endpoint that verifies signatures with `WEBHOOK_SECRET` (HMAC-SHA256)
4. Use `/follow-lang-typescript` for type-safe payloads

### 5. Implement Handlers

> Goal: Handlers wired to the subscribed events

1. Create a handler per event: `issues.opened`, `pull_request.opened`, `check_suite.requested`, etc.
2. Use installation tokens via `octokit` from the context — never personal access tokens
3. Write responses: comments, check runs, PR reviews, status updates
4. Add error handling and idempotency (GitHub may redeliver webhooks)

### 6. Test Locally

> Goal: Test before a real install

1. Run `bun dev` and tunnel the webhook with `cloudflared` or Smee.io
2. Test auth: JWT generation → installation token → API call
3. Run `/run-test` for handlers using mock payloads from `test/fixtures/`

### 7. Install And Deploy

> Goal: The app works on real repos

1. Deploy the webhook endpoint with `/deploy-to-cloudflare`, `/deploy-to-railway`, or `/deploy-to-vercel`
2. Update the webhook URL in the app settings
3. Install the app on the target repo/org via the installation URL
4. Verify: trigger a real event and watch the app respond

## Rules

- Never hardcode `APP_ID`, `PRIVATE_KEY`, `WEBHOOK_SECRET` — use `/follow-secret-manager`
- Always use installation tokens — never a PAT in place of the app identity
- Request permissions per least-privilege only
- The webhook handler must verify the signature and ack within the timeout (GitHub retries if slow)
- Handlers must be idempotent — GitHub may redeliver events
- Never commit `.env`, `.pem`, or app credentials

- Use /open-web-for-config-secret if needed
- Use /report table if needed

## Expected Outcome

- The GitHub App is registered with complete, secure credentials
- The webhook endpoint verifies signatures and handles events per the subscription
- The app installs on a repo/org and responds to real events
- Ready to deploy and extend with more handlers
