---
name: multica-setup
description: Install the Multica CLI, authenticate, and bootstrap the local daemon on a fresh machine. Use when the user mentions installing Multica, logging in, switching to a self-hosted server, configuring the server URL, or creating a new profile.
---

# Multica Setup

Bootstrap the `multica` CLI so the rest of the Multica skills can be used. The CLI is one binary that covers authentication, configuration, and the local agent daemon.

Official docs: https://github.com/multica-ai/multica/blob/main/CLI_AND_DAEMON.md

## When to use this skill

- First-time install on a machine.
- User reports `multica: command not found` or `multica auth status` fails.
- Switching between Multica Cloud and a self-hosted server.
- Setting up a second environment (e.g. staging) alongside production via profiles.
- Updating the CLI to a newer version.

## Install

Check first with `command -v multica`. If missing, pick one path:

```bash
# macOS / Linux, Homebrew (preferred)
brew install multica-ai/tap/multica

# macOS / Linux, no Homebrew
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash

# Windows PowerShell
irm https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.ps1 | iex
```

Self-hosting server on the same machine (requires Docker):

```bash
curl -fsSL https://raw.githubusercontent.com/multica-ai/multica/main/scripts/install.sh | bash -s -- --with-server
```

## One-command bootstrap

`multica setup` configures the CLI, opens a browser for OAuth, and starts the daemon.

```bash
multica setup                  # Multica Cloud
multica setup self-host        # Local self-hosted (http://localhost:8080 / :3000)
multica setup self-host --port 9090 --frontend-port 4000
multica setup self-host --server-url https://api.example.com --app-url https://app.example.com
```

After setup, the daemon runs in the background. Verify with `multica daemon status` and `multica auth status`.

## Step-by-step (when `setup` is not enough)

```bash
multica login                  # Browser OAuth, 90-day token, auto-adds all workspaces
multica login --token          # Paste a personal access token (headless / CI)
multica daemon start           # Start background daemon (logs to ~/.multica/daemon.log)
```

## Authentication checks

```bash
multica auth status            # Shows server, user, token validity
multica auth logout            # Removes stored token
```

## Configuration

Config lives in `~/.multica/config.yaml` (default profile) or `~/.multica/profiles/<name>/config.yaml`.

```bash
multica config show
multica config set server_url https://api.example.com
multica config set app_url https://app.example.com
multica config set workspace_id <workspace-id>
```

## Profiles (multiple Multica servers on one machine)

Each profile has its own config, token, daemon state, health port, and workspace root.

```bash
multica setup self-host --profile staging \
  --server-url https://api-staging.example.com \
  --app-url https://staging.example.com

multica daemon start --profile staging     # Runs in parallel with default
multica auth status --profile staging
```

All other commands accept `--profile <name>` the same way.

## Updating

```bash
multica update                             # Auto-detects install method
brew upgrade multica-ai/tap/multica        # If installed via Homebrew
multica version                            # Show current version + commit
```

## Verification checklist

After any setup flow, confirm all three succeed before handing off to another skill:

```bash
multica auth status                        # "Authenticated as <user>"
multica daemon status                      # "Running" with a PID
multica workspace list                     # At least one workspace, watched ones marked with *
```

If a workspace the user cares about is not watched, use the `multica-daemon` skill to `watch` it before assigning work.

## Gotchas

- The daemon does **not** run agents; it invokes locally installed agent CLIs (`claude`, `codex`, `gemini`, etc.). At least one of those must be on `PATH` or no runtime is registered.
- `multica login` creates a token tied to the currently configured `server_url`. Changing the server URL invalidates the token — re-run `multica login`.
- On macOS, the first daemon start may trigger a Gatekeeper prompt. Ask the user to approve it in System Settings.
- Tokens expire after 90 days. If commands start returning 401, re-run `multica login`.
