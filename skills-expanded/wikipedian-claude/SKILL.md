# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Wikipedian is a Discord bot that provides a `/wikipedia` slash command for searching Wikipedia articles. It supports multiple languages (defaults to Japanese) and returns the first two paragraphs of matching articles. Written in TypeScript using Discord.js v14 and Cheerio for HTML parsing. Runs on the Bun runtime.

## Build & Run Commands

- `bun install` — install dependencies
- `bun run start` — run the bot (`bun run src/index.ts`)
- `bun run format` — format code with Biome (`biome format --write src/`)
- `bun run lint` — lint code with Biome (`biome lint src/`)
- `bun run check` — format + lint in one pass with Biome (`biome check --write src/`)
- Slash commands are automatically registered on bot startup (requires `.env` with `WIKIPEDIAN_CLIENT_ID` and `WIKIPEDIAN_TOKEN`)

- `bun test` — run all unit tests with Bun's built-in test runner (all tests use mocked fetch, no network access)

Biome is used for formatting and linting.

## Architecture

- **`src/index.ts`** — Discord bot entry point (client setup, command registration, event handlers)
  - **`registerCommands(clientId, token)`** — registers the `/wikipedia` slash command via Discord REST API
  - **`wikipedia_command(interaction)`** — extracts `word` and `language` options, splits comma-separated languages, calls `search_wikipedia()` in parallel via `Promise.all()`
  - **`main()`** — reads env vars, registers commands, creates Discord client, starts the bot. Guarded by `import.meta.main`.
- **`src/wikipedia.ts`** — core Wikipedia search logic, exported for testing
  - **`search_wikipedia(language, word)`** — validates the language code against a strict regex to prevent SSRF, constructs a Wikipedia URL with `encodeURIComponent` for the word, fetches the page, parses HTML with Cheerio (`.mw-parser-output p:eq(0)` and `p:eq(1)`), strips citation markers, and returns a formatted result
- **`src/__tests__/`** — tests using Bun's built-in test runner (`bun:test`)

## Environment

- Requires Bun runtime
- `.env` is auto-loaded by Bun (no dotenv needed): `WIKIPEDIAN_CLIENT_ID`, `WIKIPEDIAN_TOKEN`
- Deployment options: Kubernetes (`manifests/wikipedian.yaml`), Docker (`Dockerfile`), or direct Bun
