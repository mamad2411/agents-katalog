---
name: follow-create-bot-line
description: Build a LINE bot with TypeScript/Bun — webhook, signature validation, rich menu
argument-hint: "[features]"
---

## Goal

Create a runnable LINE bot project with TypeScript/Bun, complete with webhook signature validation, message event handling, reply/push messages, rich menu, and deployment

## Scope

Use for building a LINE bot from scratch on Bun or Node.js; supports command bots, notifications, rich menus, and webhook deployments on Cloudflare/Railway/Vercel

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, following the conventions in `/update-devin-global-skills`
2. Run `/deep-review-codebase` to summarize the tech stack in use
3. Record the stack and library choices with reasons for later reference

### 2. Gather Requirements

> Goal: Collect information before building the bot

1. Ask the user about purpose, bot name, and type (notification, command, customer service)
2. Request `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET`, or guide the user to create them in the LINE Developers Console
3. Identify the runtime: `Bun` (default) or `Node.js`
4. Identify the deployment target: `Cloudflare Workers`, `Railway`, `Vercel`, or `VPS`

### 3. Setup Project

> Goal: Create the project structure

1. Use `/deep-review-codebase` or `/deep-review-codebase` to create `src/`
2. Create `src/index.ts`, `src/bot.ts`, `src/config.ts`, `src/handlers/`, `src/messages/`, `src/webhook.ts`
3. Create `package.json`, `tsconfig.json`, `.env.example`, `.gitignore`
4. Run `bun init` or `npm init` per the runtime

### 4. Install Dependencies

> Goal: Install the SDK and web server

1. Install the SDK: `bun add @line/bot-sdk`
2. Install the web server: `bun add hono` (default) or `express`
3. Install dev tools: `bun add -D @types/bun bun-types typescript`

### 5. Configure Bot And Webhook

> Goal: Connect to the LINE Messaging API

1. Create `src/config.ts` reading `LINE_CHANNEL_ACCESS_TOKEN` and `LINE_CHANNEL_SECRET` from the environment
2. Create `src/bot.ts` with `LineBotClient.fromChannelAccessToken({ channelAccessToken })` from `@line/bot-sdk` (v11+ — the legacy `Client`/`OAuth` are removed; use `messagingApi.MessagingApiClient` if you need a granular client)
3. Create `src/webhook.ts` with a `Hono` `POST /webhook` that validates `x-line-signature` with `validateSignature` over the raw body
4. Create `src/index.ts` as the entry point

### 6. Implement Handlers

> Goal: Handle message events

1. Create `src/handlers/message.ts` for `message` events (text, image, sticker, location)
2. Create `src/handlers/follow.ts` for `follow` / `unfollow` events
3. Create `src/handlers/postback.ts` for `postback` events
4. Use `client.replyMessage({ replyToken, messages })` or `client.pushMessage({ to, messages })` (request object in v11+) to send messages

### 7. Add Features

> Goal: Add features per the requirements

1. Create a rich menu or quick replies when needed
2. Use `Flex Message` for complex cards
3. Use `LIFF` for an in-app web view (optional)
4. Add middleware for logging, error handling, and rate limiting

### 8. Test Locally

> Goal: Test the bot before deploying

1. Run `bun dev` or `bun run src/index.ts`
2. Use `ngrok` or `cloudflared` to create a public URL for the webhook
3. Register the webhook URL in the LINE Developers Console
4. Test sending messages and check the logs
5. Run `/run-test` for unit tests of the handlers

### 9. Deploy

> Goal: Deploy the bot to production

1. For `Cloudflare Workers`: use `/deploy-to-cloudflare` with a `Hono` adapter
2. For `Railway/Vercel/VPS`: use `/deploy-to-railway` or `/deploy-to-vercel` with environment variables
3. Update the webhook URL to the production endpoint
4. Run `/ship`

## Rules

- Never hardcode `LINE_CHANNEL_ACCESS_TOKEN` or `LINE_CHANNEL_SECRET`; use `/follow-secret-manager` to manage channel secrets
- Use `@line/bot-sdk` as the default SDK (v11+ — fetch-based, no axios, use `LineBotClient` only)
- Use `Hono` as the default web server on Bun
- Always validate `x-line-signature` before parsing events
- Never commit `.env`
- Be TypeScript-first per `/follow-lang-typescript`

- Use /open-web-for-config-secret if needed
- Use /follow-create-bun-cli if needed
- Use /follow-create-sdk if needed
- Use /follow-create-web if needed
- Use /use-bun-native-api if needed
- Use /report table if needed

## Expected Outcome

- The LINE bot project runs with `bun dev`
- The webhook validates signatures correctly
- Message/follow/postback handlers work
- Reply/push messages and the rich menu are supported
- Ready to deploy with environment variables
