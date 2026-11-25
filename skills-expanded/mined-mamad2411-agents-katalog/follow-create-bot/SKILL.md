---
name: follow-create-bot
description: Build a bot for Slack, Discord, Telegram, LINE, or a GitHub App/bot with TypeScript/Bun
argument-hint: "<slack|discord|telegram|line|github|github-app> [features]"
related:
  - deep-review-codebase
  - follow-secret-manager
  - open-web-for-config-secret

---

## Goal

Build a bot for the specified platform — Slack, Discord, Telegram, LINE, or GitHub (App/bot) — with the right project structure, commands/events, and deployment

## Scope

- Use when creating a chat bot or a GitHub automation bot
- Follow `/deep-review-codebase` for runtime and dependencies

- SDKs: `discord.js`, `grammy`, `@slack/bolt`, `@line/bot-sdk`, `probot` — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (not pinned in files — per `/update-devin-global-skills`)
- Breaking: `@line/bot-sdk` v11 removed the legacy `Client`/`OAuth` — use `LineBotClient.fromChannelAccessToken()` or `messagingApi.MessagingApiClient` instead
- Breaking: `@slack/bolt` v5 requires Node.js ≥20, removes the `agent`/`clientTls` options and `WorkflowStep`/`app.step()` (use `app.function()`)
- Breaking: `discord.js` v14 deprecates the `ready` event → use `Events.ClientReady` (removed in v15)

## Execute

### 1. Select Platform

> Goal: Identify the platform and read its platform-specific details

| Platform   | Skill |
|------------|----------|
| Slack      | `/follow-create-bot-slack` — slash commands, events, Socket Mode |
| Discord    | `/follow-create-bot-discord` — commands, intents, gateway |
| Telegram   | `/follow-create-bot-telegram` — Bot API, commands, webhooks |
| LINE       | `/follow-create-bot-line` — Messaging API, webhook, reply |
| GitHub     | `/follow-create-bot-github` — GitHub bot, probot, webhooks |
| GitHub App | `/follow-create-bot-github-app` — app manifest, JWT auth, installation |

1. Read the platform from the argument — if unspecified → run `/ask-me`
2. Run `/deep-research` + `/follow-best-practice` to confirm the platform SDK's latest versions and patterns, then run `/deep-review-codebase`
3. Invoke the selected platform's skill and follow its flow — do not execute directly from this table

### 2. Setup Project

> Goal: Project structure ready to use

1. Create the project per the selected platform's skill
2. Install the SDK/dependencies with `bun add`
3. Keep tokens/secrets via `/follow-secret-manager` — never hardcode

### 3. Implement And Ship

> Goal: The bot really works and is ready to deploy

1. Implement commands/events per the platform's skill
2. Test locally (Socket Mode / polling / webhook tunnel)
3. Prepare the deploy target and document usage

## Rules

- Never commit tokens or webhook secrets
- Follow the platform's skill — never guess the API
- Use `/open-web-for-config-secret` to point the user to create the bot token themselves

## Expected Outcome

- A working bot for the chosen platform with correct structure and secrets management
