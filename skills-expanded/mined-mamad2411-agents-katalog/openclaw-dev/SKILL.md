---
name: openclaw-dev
description: Use when developing, configuring, running, or diagnosing OpenClaw instances, including local startup, config files, slash/plugin extensions, host diagnostics, tunnels, and provider troubleshooting.
---

# OpenClaw Dev

## Quick Start

Prefer the official OpenClaw CLI and repository documentation:

- Repository: `https://github.com/openclaw/openclaw`
- Docs: `https://github.com/openclaw/openclaw/tree/main/docs`

If local source is needed, use `/workspace/openclaw` by convention:

```bash
git clone https://github.com/openclaw/openclaw /workspace/openclaw
```

## Workflow

1. Identify whether the task is startup, configuration, extension work, host diagnostics, or public endpoint exposure.
2. Inspect the active `openclaw.json` and state directory before changing behavior.
3. Prefer OpenClaw's built-in CLI, slash commands, plugin system, and config reload behavior.
4. For endpoint exposure, verify DNS, tunnel connectivity, routing, and then UI or agent behavior.
5. Keep credentials out of documentation, logs, examples, and committed config.

For integration boundary decisions, read `references/openclaw-agent-driven-architecture-analysis.md`.

## Common Commands

Start a local gateway:

```bash
openclaw gateway --force
```

Run a local agent prompt with an explicit config file:

```bash
OPENCLAW_CONFIG_PATH="$HOME/.openclaw/openclaw.json" openclaw agent --local --agent main -m "ping" --json
```

Inspect a session:

```bash
openclaw sandbox explain --session "<session-id>" --json
```

## Diagnostics

- Check the process, listening ports, config path, state directory, and latest logs.
- Do not rely only on process name; OpenClaw may run under a Node.js process.
- If config changes appear ignored, confirm the active `OPENCLAW_CONFIG_PATH` and whether the running instance reloaded the expected file.
- For provider failures, check model name, base URL, API key presence, and request headers. Do not write real API keys or private base URLs into the skill.
- For Telegram or similar polling channels, avoid running multiple instances with the same bot token; concurrent polling commonly causes conflict errors.

## Host Setup

On a new Debian or Ubuntu host:

1. Install the runtime dependencies required by the current OpenClaw documentation.
2. Install or build OpenClaw using the official instructions.
3. Create or copy the intended `openclaw.json`.
4. Start one instance and verify logs before adding tunnels or background services.

## Public Endpoint Options

- Cloudflare Tunnel: good for a quick public HTTPS endpoint.
- Tailscale Serve/Funnel: good for private networks or controlled public exposure.
- Reverse proxy: good when a host already has Nginx, Caddy, or another gateway.

Choose the simplest option that matches the deployment environment.
