---
name: follow-create-bot-discord
description: Build a Discord bot with TypeScript/Bun — slash commands, auto-load, intents
argument-hint: "[features]"
---

## Goal

Create a runnable Discord bot project with TypeScript/Bun, complete with slash commands, event handlers, auto-loaded commands, and a modular architecture

## Scope

Use for building a Discord bot from scratch on Bun or Node.js; supports slash commands, buttons, select menus, modals, context menus, and deployment

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and patterns, following the conventions in `/update-devin-global-skills`
2. Run `/deep-review-codebase` to summarize the tech stack in use
3. Record the stack and library choices with reasons for later reference

### 2. Gather Requirements

> Goal: Collect information before building the bot

1. Ask the user about purpose, bot name, target guilds, and the commands needed
2. Request `DISCORD_TOKEN`, `APPLICATION_ID`, and `GUILD_ID`, or guide the user to create an app in the Discord Developer Portal
3. Identify intents: `GatewayIntentBits.Guilds`, `GuildMessages`, `MessageContent`, etc.
4. Identify the deployment target: local dev or server/serverless

### 3. Setup Project

> Goal: Create the project structure

1. Use `/deep-review-codebase` or `/deep-review-codebase` to create `src/`
2. Create `src/index.ts`, `src/client.ts`, `src/commands/`, `src/events/`, `src/handlers/`, `src/types.ts`, `src/config.ts`
3. Create `package.json`, `tsconfig.json`, `.env.example`, `.gitignore`
4. Run `bun init` or `npm init`
5. Use `/search-npm-libraries` to pick a library (default `discord.js` or a lightweight wrapper)

### 4. Configure Bot And Commands

> Goal: Connect to the Discord API

1. Install the library, e.g. `bun add discord.js`
2. Create `src/client.ts` with the token, intents, and a `Client` instance
3. Create `src/index.ts` as the entry point
4. Create `src/types.ts` for the `Command` interface (`data: SlashCommandBuilder; execute: ...`)
5. Create `src/deploy-commands.ts` to register slash commands with Discord
6. Create `src/commands/ping.ts` as an example

### 5. Auto-Load Commands And Events

> Goal: Auto-load commands/events from directories

1. Use `Bun.Glob` or `readdirSync` to scan `src/commands/`
2. Store commands in a `Collection<string, Command>` on the client
3. Use `client.on(Events.InteractionCreate)` to route slash commands, buttons, and modals
4. Use `client.once(Events.ClientReady)` to log the login (the `ready` event is deprecated in v14 and removed in v15)
5. Add `src/events/` for `clientReady`, `interactionCreate`, and `messageCreate` as needed

### 6. Add Features

> Goal: Add features per the requirements

1. Create slash commands with `SlashCommandBuilder`
2. Support buttons, select menus, modals, and context menus when needed
3. Use `/use-bun-native-api` instead of `node:*` when using Bun
4. Add guards/middleware for permission checks and rate limiting
5. Use `Interaction` types for type safety

### 7. Test Locally

> Goal: Test the bot

1. Run `bun run deploy-commands` to register commands
2. Run `bun dev` or `bun run src/index.ts`
3. Test slash commands in a guild
4. Check logs and error handling
5. Run `/run-test` for unit tests

### 8. Deploy

> Goal: Deploy the bot to production

1. Use `bun start` on a server or in a container
2. Set `DISCORD_TOKEN` and `APPLICATION_ID` on the host
3. If serverless → use `/deploy-to-cloudflare` or `/deploy-to-railway` per the target

## Rules

- Never hardcode `DISCORD_TOKEN`, `APPLICATION_ID`, `GUILD_ID`; use `/follow-secret-manager` to manage secrets
- Use `discord.js` as the default library on Bun
- Always provide a `deploy-commands` script for registering slash commands
- Never commit `.env`
- Be TypeScript-first per `/follow-lang-typescript`
- Use intents per least privilege — `GatewayIntentBits.Guilds` is required for slash commands; `GuildMessages`/`MessageContent` only when reading messages
- Bot app: create it in the Discord Developer Portal → `Bot` tab → `Reset Token`; invite via `OAuth2 → URL Generator` with scopes `bot` + `applications.commands`
- Slash commands: build with `SlashCommandBuilder`, register guild-level (`Routes.applicationGuildCommands`) during dev because it is faster, and global (`Routes.applicationCommands`) in production

- Use /open-web-for-config-secret if needed
- Use /follow-create-cli if needed
- Use /follow-create-sdk if needed
- Use /follow-create-web if needed
- Use /report table if needed

## Expected Outcome

- The Discord bot project runs with `bun dev`
- Slash commands auto-load and work
- Event handlers are split into modules
- Ready to deploy with environment variables

## Guide

- `/deep-research` + `/follow-best-practice` — latest official docs/versions (not pinned in this file)
- `/follow-lang-typescript` — TypeScript best practices
- `/follow-create-bun-cli` — if the bot is a Bun CLI project
- `/search-npm-libraries` — pick a library per use case
