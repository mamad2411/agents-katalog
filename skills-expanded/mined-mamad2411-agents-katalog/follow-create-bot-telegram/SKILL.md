---
name: follow-create-bot-telegram
description: Build a Telegram bot with TypeScript/Bun — grammy, commands, webhook/polling
argument-hint: "[features]"
---

## Goal

Create a runnable Telegram bot project with TypeScript/Bun, complete with command handling, middleware, sessions, error handling, and webhook/long-polling

## Scope

Use for building a Telegram bot from scratch on Bun or Node.js; supports command bots, conversational flows, notifications, and webhook deployments

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, following the conventions in `/update-devin-global-skills`
2. Run `/deep-review-codebase` to summarize the tech stack in use
3. Record the stack and library choices with reasons for later reference

### 2. Gather Requirements

> Goal: Collect information before building the bot

1. Ask the user about purpose, bot name, and type (notification, command, conversational)
2. Request `BOT_TOKEN`, or guide the user to create it via @BotFather
3. Identify the runtime: `Bun` (default) or `Node.js`
4. Identify the deployment mode: `long-polling` for dev or `webhook` for production

### 3. Setup Project

> Goal: Create the project structure

1. Use `/deep-review-codebase` or `/deep-review-codebase` to create `src/`
2. Create `src/bot.ts`, `src/index.ts`, `src/commands/`, `src/middleware/`, `src/handlers/`, `src/config.ts`
3. Create `package.json`, `tsconfig.json`, `.env.example`, `.gitignore`
4. Run `bun init` or `npm init` per the runtime
5. Use `/search-npm-libraries` to pick the main library (default recommendation: `grammy`)

### 4. Configure Bot And Handlers

> Goal: Connect to the Telegram Bot API

1. Install the chosen library, e.g. `bun add grammy`
2. Create `src/bot.ts` with the token from `Bun.env.BOT_TOKEN`
3. Create `src/index.ts` as the entry point
4. Create `src/commands/start.ts` and `src/commands/help.ts` as examples
5. Add middleware for logging, error handling, and rate limiting
6. If you need sessions → use the `grammy` session middleware or memory/redis

### 5. Add Features

> Goal: Add features per the requirements

1. Create handlers for messages, callback queries, and inline queries as needed
2. Use `bot.api.setMyCommands` to register slash commands
3. Use `/use-bun-native-api` instead of `node:*` when using Bun
4. Add type safety with TypeScript interfaces for context/dependencies

### 6. Test Locally

> Goal: Test the bot

1. Run `bun dev` or `bun run src/index.ts`
2. Test commands on Telegram
3. Check logs and error handling
4. Run `/run-test` for unit tests of the handlers

### 7. Deploy

> Goal: Deploy the bot to production

1. With long-polling: run `bun start` on a server or in a container
2. With webhook: set up an `express`/`hono`/`elysia` endpoint, then `webhookCallback`
3. Set environment variables on the host
4. Use `/deploy-to-cloudflare`, `/deploy-to-railway`, or `/deploy-to-vercel` per the target

## Rules

- Never hardcode `BOT_TOKEN`; use `/follow-secret-manager` to manage the token before injecting it into the app
- Use `grammy` as the default library on Bun
- Use long-polling for dev and webhook for production — the webhook path must include the token as a secret, e.g. `/webhook/${BOT_TOKEN}`; use `webhookCallback(bot, 'hono'|'express')`
- Token: create it via `@BotFather` → `/newbot`; always keep it in env
- Commands: register with `bot.api.setMyCommands([{ command, description }])`; for user state use the `session()` middleware
- Never commit `.env`
- Be TypeScript-first per `/follow-lang-typescript`
- Libraries: `grammy` (default), `gramio`, `node-telegram-bot-api` (v2 runs on Workers)

- Use /open-web-for-config-secret if needed
- Use /follow-create-cli if needed
- Use /follow-create-sdk if needed
- Use /follow-create-web if needed
- Use /report table if needed

## Expected Outcome

- The Telegram bot project runs with `bun dev`
- Command handlers, middleware, and error handling are complete
- Both long-polling and webhook are supported
- Ready to deploy with environment variables

## Guide

- `/deep-research` + `/follow-best-practice` — latest official docs/versions (not pinned in this file)
- `/follow-lang-typescript` — TypeScript best practices
- `/follow-create-bun-cli` — if the bot is a Bun CLI project
- `/search-npm-libraries` — pick a library per use case
