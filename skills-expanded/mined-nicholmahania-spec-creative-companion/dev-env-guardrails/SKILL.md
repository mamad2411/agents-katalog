---
name: dev-env-guardrails
description: Terminal and environment guardrails for running scripts, builds, and dev servers. Use this skill whenever executing terminal commands in a development context — starting dev servers (npm run dev, vite), running builds, executing Node scripts, or doing backend verification. Trigger for any session involving shell commands against a project, not just when the user mentions the terminal or Node versions.
---

# Terminal & Environment Guardrails

Rules for how commands get run, so the environment stays predictable and the session stays responsive.

## Node Environment

- Always use **Node 24+** for script execution and builds.
- **Never** trigger scripts on deprecated Node 20 (or older) runtimes.
- Check the active version (`node -v`) at the start of any session that will run Node, before the first script executes — not after something fails mysteriously.
- If the environment only offers an older Node, say so and resolve it (nvm/version manager, or flag to the user) rather than silently running on the deprecated runtime.

## Terminal Execution

- When running local development servers (`npm run dev`, `vite`, similar long-running processes): **do not block the active shell session** unless multi-session routing is available. Launch them in the background (e.g., `&` with output redirected to a log file) so the session can keep working.
- Run backend verification commands (curl checks, health probes, test queries) in the background or as quick non-blocking calls — verify smoothly without freezing the working shell.
- After backgrounding a server, confirm it actually started (check the log or probe the port) before building on the assumption that it's up.
- Keep track of what's running: before starting a server, check whether one is already bound to the port; kill stale processes deliberately, never by side effect.

## Config Discovery

- Before claiming a `.env` or config file can't be found, list hidden files (`ls -la`) in the project root and likely config directories — dotfiles are invisible to a plain `ls`, and "missing" configs are usually just hidden.
- Parse runtime keys **read-only**: reference the variable names and structure as needed, but never modify, regenerate, or reorder the user's local keys, and never print secret values into output or logs.
- If a config is genuinely absent, say what was checked and where, then ask — don't fabricate a replacement file.
