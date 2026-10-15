---
name: guild-shared
description: Authenticate and configure the Guild CLI before operating milestones, iterations, or tickets. Use when the user asks to use guild CLI, configure API access, or work with Guild resources via terminal or agent.
metadata:
  requires:
    bins: ["guild"]
    cliHelp: "guild --help"
---

# guild-shared

## Overview

The `guild` CLI is a thin HTTP client for the Adventurer Public API. It does not access the database directly. All operations require a valid API key and project ID.

## When to use

- Before any `guild milestone`, `guild iteration`, or `guild ticket` command.
- When the user wants to automate Guild workflows from the terminal or from an agent.
- When unsure about global flags or auth setup.

## Prerequisites

- API reachable at default `https://api.adventurer-next.36node.com`, or locally (`--api-url http://localhost:3002`).
- API key from Guild Web (Settings → API Keys), **or** username/password (`POST /auth/@login`).
- `guild` installed globally or via `npx @adventurer-tech/guild-cli`.

## Setup

```bash
npm install -g @adventurer-tech/guild-cli

# Password login (Guild account)
guild auth login --username <username> --password '<password>'

# Or API key from Guild Web → Settings → API Keys
guild auth login --api-key <key>

guild config init --project-id <projectId>
guild auth status
```

Default API: `https://api.adventurer-next.36node.com`. Local dev: `--api-url http://localhost:3002`.

## Config locations

| File | Contents | Commit? |
| --- | --- | --- |
| `~/.config/guild/credentials.json` | `apiKey`, optional `apiUrl` | Never |
| `.guild/config.json` | `projectId`, optional `apiUrl` | Yes |

Override per invocation: `--project-id`, `--api-url`.

## Output

Default JSON: `{ "ok": true, "data": ... }`. On failure, `{ "ok": false, "error": { "code", "message" } }` and exit code 1.

Use `--pretty` for indented JSON.

## API custom verbs

Non-CRUD actions use `POST …/@verb` for ticket state (publish, unpublish, close, reopen) and `POST …/actions/@verb` for workflow (take, untake, submit, approve, reject). Sub-resources use `PUT`.

## Help

When parameters are unclear, run help first:

```bash
guild --help
guild auth --help
guild config --help
```

## Security

- **Never** write API keys into repo files, skills, or commit messages.
- **Never** echo or log the `x-api-key` header.

## Install skills

```bash
npx skills add adventurer-tech/guild-skills -y -g
```
