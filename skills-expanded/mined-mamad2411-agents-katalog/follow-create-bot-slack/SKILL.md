---
name: follow-create-bot-slack
description: Build a Slack bot with TypeScript/Bun — slash commands, events, Socket Mode
argument-hint: "[features]"
---

## Goal

Create a runnable Slack bot project with TypeScript/Bun, complete with slash commands, event handlers, interactivity (buttons, modals), and Socket Mode or an HTTP endpoint

## Scope

Use for building a Slack bot from scratch on Bun or Node.js; supports notification bots, slash command workflows, interactive messages, and workspace integrations

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, following the conventions in `/update-devin-global-skills`
2. Run `/deep-review-codebase` to summarize the tech stack in use
3. Record the stack and library choices with reasons for later reference

### 2. Gather Requirements

> Goal: Collect information before building the bot

1. Ask the user about purpose, bot name, and type (notification, slash commands, interactive)
2. Guide the user to create a Slack App at api.slack.com/apps, then request `SLACK_BOT_TOKEN` (`xoxb-...`), `SLACK_SIGNING_SECRET`, and `SLACK_APP_TOKEN` (`xapp-...` if using Socket Mode)
3. Identify the runtime: `Bun` (default) or `Node.js`
4. Identify the connection mode: `socket-mode` for dev or `http` (Events API endpoint) for production

### 3. Setup Project

> Goal: Create the project structure

1. Use `/deep-review-codebase` or `/deep-review-codebase` to create `src/`
2. Create `src/app.ts`, `src/index.ts`, `src/commands/`, `src/events/`, `src/actions/`, `src/config.ts`
3. Create `package.json`, `tsconfig.json`, `.env.example`, `.gitignore`
4. Run `bun init` or `npm init` per the runtime
5. Use `/search-npm-libraries` to pick the main library (default recommendation: `@slack/bolt`)

### 4. Configure Bot And Handlers

> Goal: Connect to the Slack API

1. Install with `bun add @slack/bolt`
2. Create `src/app.ts` with `new App({ token, signingSecret, socketMode, appToken })`
3. Create `src/index.ts` as the entry point calling `app.start()`
4. Create `src/commands/` with an example `app.command('/hello', ...)`
5. Create `src/events/` with examples `app.event('app_mention', ...)` and `app.message(...)`
6. Add error handling with `app.error()` and the ack pattern (call `ack()` before processing)

### 5. Add Features

> Goal: Add features per the requirements

1. Create `src/actions/` for `app.action()`, `app.view()` (modals), and `app.shortcut()`
2. Use Block Kit (`blocks`) for rich messages
3. Use `/use-bun-native-api` instead of `node:*` when using Bun
4. Add type safety with TypeScript interfaces for payloads and dependencies

### 6. Test Locally

> Goal: Test the bot

1. Run `bun dev` or `bun run src/index.ts`
2. In HTTP mode → tunnel with `cloudflared` or ngrok, then set the Request URL in the Slack App
3. Test slash commands, mentions, and interactive actions in a Slack workspace
4. Run `/run-test` for unit tests of the handlers

### 7. Deploy

> Goal: Deploy the bot to production

1. With Socket Mode → run `bun start` on a server or container with outbound access
2. With HTTP mode → expose the endpoint, then set the Event/Interactivity Request URL
3. Set environment variables on the host
4. Use `/deploy-to-cloudflare`, `/deploy-to-railway`, or `/deploy-to-vercel` per the target

## Rules

- Never hardcode `SLACK_BOT_TOKEN`, `SLACK_SIGNING_SECRET`, `SLACK_APP_TOKEN`; use `/follow-secret-manager` before injecting them into the app
- Use `@slack/bolt` as the default library on Bun/Node
- Use Socket Mode for dev and an HTTP endpoint for production
- Every listener must call `ack()` within 3 seconds before doing heavy work
- Never commit `.env`
- Be TypeScript-first per `/follow-lang-typescript`

- Use /open-web-for-config-secret if needed
- Use /follow-create-bot-discord if needed
- Use /report table if needed

## Expected Outcome

- The Slack bot project runs with `bun dev`
- Slash commands, event handlers, and interactive actions cover the requirements
- Both Socket Mode and the HTTP endpoint are supported
- Ready to deploy with environment variables
