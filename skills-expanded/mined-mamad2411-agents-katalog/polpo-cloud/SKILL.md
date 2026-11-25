---
name: polpo-cloud
description: Deploy and manage AI agents on Polpo Cloud using the CLI. Use when the user wants to deploy agents, manage API keys, configure LLM provider keys (BYOK), check project status, or any Polpo Cloud infrastructure task. Triggers on "polpo deploy", "polpo cloud", "polpo CLI", "deploy agent", "BYOK", "LLM keys", "polpo login".
---

# Polpo Cloud CLI

## Install

```bash
npm install -g polpo-ai
```

## Authentication

```bash
# Login via browser (recommended)
polpo login

# Verify
polpo cloud-status

# Logout
polpo logout
```

### Non-interactive login

For CI/CD, scripts, or when browser login is not available, set the `POLPO_API_KEY` environment variable before running `polpo login`. Get your key from polpo.sh → API Keys.

```bash
export POLPO_API_KEY="..."
polpo login
```

**Do not hardcode API keys in source code or commit them to version control.**

Credentials stored at `~/.polpo/credentials.json`.

## Deploy Agents

Deploy syncs local `.polpo/` config to the cloud project.

```bash
# From project root (must have .polpo/ directory)
polpo deploy
```

This uploads:
- Agent configurations (from `polpo.json` or `.polpo/config.json`)
- Skills
- Memory

Creates the project automatically on first deploy if none is linked.

## Managed AI Gateway

Polpo includes a managed AI gateway with free credits — no LLM key setup needed to get started. Your agents can use any supported model out of the box.

## BYOK (Bring Your Own Key)

Optionally set your own LLM provider API keys per project. Keys are AES-256-GCM encrypted at rest.

```bash
# Set a key (interactive — prompts securely for the key value)
polpo byok set <provider>

# List keys (masked)
polpo byok list

# Delete a key
polpo byok delete <provider>
```

Supported providers: `openai`, `anthropic`, `xai`, `google`, `groq`, `openrouter`, `cerebras`, `mistral`.

You can also set keys via the dashboard at polpo.sh → LLM Keys. **Do not hardcode LLM keys in source code or commit them to version control.**

## Project Management

```bash
# List projects
polpo projects list

# Create a project
polpo projects create my-project

# View cloud project status
polpo cloud-status
```

## Stream Logs

```bash
# Stream real-time logs from the project
polpo cloud-logs [--follow] [--tail 50]
```

## Workflow: First Deploy

1. Sign up at `polpo.sh`
2. Create a workspace and project (onboarding handles this)
3. `polpo login` (opens browser for approval)
4. Create `.polpo/` directory with agent config
5. `polpo deploy`
6. Use `POST /v1/chat/completions` with `agent: "name"` to chat

No LLM keys needed — the managed gateway covers you with free credits.

## Dashboard

Available at `polpo.sh` after signup:
- **Overview**: project stats
- **Agents**: view/manage agent configs
- **Sessions**: chat history with agents
- **Skills**: installed agent skills
- **Memory**: project + per-agent memory
- **Webhooks**: event notification endpoints
- **API Keys**: manage data plane keys
- **LLM Keys**: BYOK provider keys (optional)
- **Settings**: project configuration

## API Base URL

- **Cloud**: `https://api.polpo.sh`
- **Local development**: `http://localhost:3890` (default `polpo start` port)

See [references/cli-commands.md](references/cli-commands.md) for the full CLI reference.
