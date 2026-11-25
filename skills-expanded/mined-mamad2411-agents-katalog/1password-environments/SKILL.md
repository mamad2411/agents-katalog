---
name: 1password-environments
description: Use this skill when setting up 1Password Environments for local development to mount named secret sets as local .env files via FIFO pipes, configuring the .1password/environments.toml file with mount paths, installing agent hooks to validate environment files before AI coding assistant execution (Claude Code, Cursor, GitHub Copilot, Windsurf), or troubleshooting FIFO .env delivery issues. Not for secrets automation or SSH key management.
---

# 1Password Environments

Use this skill for local `.env` workflows powered by 1Password Environments.

## What this skill covers

- Mounting local `.env` destinations from 1Password Environments.
- Configuring `.1password/environments.toml` `mount_paths`.
- Validating mounts with the 1Password agent hook before command/tool execution.
- Troubleshooting FIFO mount issues.

## Core model

Mounted `.env` files are FIFO-backed. Secrets are provided on read and are not stored as plaintext on disk.

## Setup workflow

1. Create an Environment in 1Password and add variables.
2. Configure destination as a local `.env` file path.
3. Add project config:

```toml
mount_paths = [".env"]
```

4. Install agent hooks and enable pre-command validation.
5. Verify by reading the mounted file once.

## Gotchas

- Local mounted `.env` files are currently Mac/Linux only.
- FIFO mounts are not designed for concurrent readers.
- If your tooling aggressively watches `.env` files (for example Vite), ignore mounted env files in watch config to avoid restart loops.
- If `.1password/environments.toml` exists without `mount_paths`, hook falls back to default mode.
- If `mount_paths = []`, validation effectively allows all commands.
- Hook default mode is fail-open when 1Password database is unavailable.

## Vite compatibility

If mounted `.env` causes restarts, ignore it in `vite.config.ts` watch config.

## Companion skills

- `1password` for CLI install/sign-in, shell plugins, and service accounts.
- `1password-ssh` for SSH/Git flows.
- `1password-secrets-in-code` for CI/CD, SDK, and MCP wrapping.

## References

- [Local env files](references/local-env-file.md)
- [Agent hook validation](references/agent-hooks.md)
- [Template](assets/.1password/environments.toml.template)
