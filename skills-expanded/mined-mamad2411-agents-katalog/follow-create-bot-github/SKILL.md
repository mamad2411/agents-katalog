---
name: follow-create-bot-github
description: Build a GitHub bot with GitHub Apps or Probot — webhooks, events, deploy
argument-hint: "[features]"
---

## Goal

Build a GitHub bot with GitHub Apps or the Probot framework, with webhook reception, event handling, and deployment to production

## Scope

Use for building a GitHub bot with TypeScript/Bun/Node.js — covers app registration, webhooks (issues, pull requests, push), auth, tests, and deployment

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, following the conventions in `/update-devin-global-skills`
2. Run `/deep-review-codebase` to summarize the tech stack in use
3. Record the stack and library choices with reasons for later reference

### 2. Choose Stack

> Goal: Pick the stack that fits the use case

1. Use Probot when you want a framework with built-in webhook handling and `context.octokit`
2. Use `@octokit/app` + `@octokit/webhooks` when you want full control or a serverless deploy
3. Use `follow-create-bun-cli` if the bot is a Bun CLI + server
4. Use `follow-create-web` if the bot has a dashboard or configuration UI

### 3. Setup Project

> Goal: Create the project structure and dependencies

1. Create the `{bot-name}/` directory
2. Create `package.json` with `name: github-bot-{name}`
3. Install dependencies per stack:
   - Probot: `bun add probot @probot/adapter`
   - Octokit: `bun add @octokit/app @octokit/webhooks @octokit/rest`
   - Serverless: `bun add @octokit/app`
4. Create `tsconfig.json` with `strict: true`
5. Create `.env.example` with `APP_ID`, `PRIVATE_KEY`, `WEBHOOK_SECRET`, `WEBHOOK_PROXY_URL`

### 4. Register GitHub App

> Goal: Register the GitHub App correctly

1. Go to GitHub Settings > Developer settings > GitHub Apps > New GitHub App
2. Set the Homepage URL, Webhook URL, and Webhook Secret
3. Select permissions per the events the bot will use, e.g. `issues`, `pull_requests`, `contents`
4. Subscribe to events such as `issues`, `pull_request`, `push`
5. Download the private key and save the `APP_ID`
6. Install the app on the desired repositories or organization

### 5. Implement Webhook Handlers

> Goal: Implement the bot's event handlers

1. Create `src/index.ts` as the entry point
2. Create `src/handlers/` split by event type:
   - `issues.ts`
   - `pull-request.ts`
   - `push.ts`
3. Use the Probot pattern:
   ```ts
   import { Probot } from "probot";
   export default (app: Probot) => {
     app.on("issues.opened", async (context) => { ... });
   };
   ```
4. Or use `@octokit/webhooks`:
   ```ts
   import { Webhooks } from "@octokit/webhooks";
   const webhooks = new Webhooks({ secret: Bun.env.WEBHOOK_SECRET });
   webhooks.on("issues.opened", async ({ payload }) => { ... });
   ```
5. Separate business logic from webhook wiring → `src/domain/`
6. Wrap handlers in `try/catch` and log errors

### 6. Add Local Development Proxy

> Goal: Test webhooks locally

1. Use Smee (smee.io) as the webhook proxy
2. Set `WEBHOOK_PROXY_URL` in `.env`
3. Run `bun run dev` or `bunx smee -u <url> -p 3000`
4. Test with real events from GitHub

### 7. Add Tests

> Goal: Test handlers without running a real GitHub App

1. Create `test/handlers/` with webhook payload fixtures
2. Use `nock` or `msw` to mock Octokit API calls
3. Run `bun test`
4. Check idempotency and error handling

### 8. Deploy

> Goal: Deploy the bot to production

1. Choose a platform:
   - Cloudflare Workers: use `follow-service-cloudflare`
   - Vercel Functions: use `follow-service-vercel`
   - Railway/Render/Fly.io: use `follow-deploy`
   - VPS/Container: use Docker + `bun start`
2. Set environment variables on the platform
3. Update the Webhook URL in the GitHub App settings
4. Check the health endpoint `/health` or `/`

### 9. Ship

> Goal: Deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Naming

- Use `github-bot-{name}` for bot-specific projects
- Use `probot-{name}` for Probot-based ones
- The GitHub App name in GitHub settings should match the repo name

### 2. Security

- Keep `PRIVATE_KEY`, `WEBHOOK_SECRET` in environment variables / a secret manager
- Never hardcode secrets in source code
- Use `WEBHOOK_SECRET` to verify the signature of every webhook
- Use `crypto.timingSafeEqual` when comparing signatures

### 3. Webhooks

- Reply 200 OK to GitHub immediately, then process async
- Handle idempotency with the `delivery` ID
- Tolerate GitHub retries without repeating work
- Limit permissions to the least actually needed

### 4. Error Handling

- Log errors with context (event, repository, action)
- Never expose stack traces or secrets in HTTP responses
- Provide a fallback handler for unhandled events

### 5. Testing

- Test every handler with fixtures
- Mock all Octokit API calls
- Test error paths

- Use /use-github-ship-bots if needed

## Expected Outcome

- The GitHub App is registered correctly and installed on the target repos
- Webhook handlers work both locally and in production
- Tests pass for every event type
- Secrets are managed securely
- The deploy is live with a health endpoint

## Examples

```text
my-github-bot/
├── src/
│   ├── index.ts
│   ├── handlers/
│   │   ├── issues.ts
│   │   ├── pull-request.ts
│   │   └── push.ts
│   ├── domain/
│   │   └── auto-label.ts
│   └── github/
│       └── client.ts
├── test/
│   └── handlers/
│       └── issues.test.ts
├── package.json
├── tsconfig.json
├── .env.example
└── README.md
```

## Guide

- `follow-create-bun-cli` — Bun CLI setup
- `follow-service-cloudflare` — Cloudflare Workers deploy
- `follow-service-vercel` — Vercel deploy
- `follow-deploy` — deployment configuration
- `follow-tool-github-actions` — GitHub Actions CI/CD
- [Probot Docs](https://probot.github.io/docs/)
- [GitHub Apps Docs](https://docs.github.com/en/apps)
