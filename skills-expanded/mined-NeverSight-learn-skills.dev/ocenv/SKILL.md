---
name: ocenv
description: Implement and maintain the OpenClaw env setup used on this machine. Use when asked to set up, debug, or explain how env variables and secrets should work for OpenClaw, shells, and token-dependent CLIs. Covers the canonical `.env.tpl` to `.env` sync flow, 1Password secret references, installing the packaged `env-sync.sh` script into `/root/.openclaw/env-sync.sh`, and loading `/root/.openclaw/.env` from `/root/.profile` so normal shells and OpenClaw-spawned CLI processes inherit the env by default. Also use when debugging why a token is in `.env` but not available to commands, or when re-implementing this env solution on another machine.
always: true
emoji: 🔐
---

# OpenClaw Env Setup

Use this skill to implement the env pattern used on this machine.

## Canonical files

Use these paths:

- `/root/.openclaw/.env.bootstrap`
- `/root/.openclaw/.env.tpl`
- `/root/.openclaw/.env`
- `/root/.openclaw/env-sync.sh`
- `/root/.profile`

Keep the env files and sync script together in `/root/.openclaw/`.

## Desired behavior

The system should work like this:

1. Secret references live in `/root/.openclaw/.env.tpl`.
2. `/root/.openclaw/env-sync.sh` injects those refs into `/root/.openclaw/.env`.
3. `/root/.profile` loads `/root/.openclaw/.env` automatically.
4. New shells and normal CLI processes inherit the env by default.

Prefer this simple model over wrapper commands unless the user explicitly asks for tighter secret isolation.

## Packaged script

This skill should include a packaged sync script under `scripts/env-sync.sh`.

When implementing the setup on a machine, install that script to:

- `/root/.openclaw/env-sync.sh`

Set it executable after install.

## Template and sync flow

Use `.env.tpl` for 1Password references such as:

```bash
GITHUB_TOKEN="op://Vault/Item/password"
```

Expected installed script at `/root/.openclaw/env-sync.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

set -a
source /root/.openclaw/.env.bootstrap
set +a
op inject -f -i /root/.openclaw/.env.tpl -o /root/.openclaw/.env
chmod 600 /root/.openclaw/.env
printf 'Wrote /root/.openclaw/.env\n'
```

If sync fails, check the 1Password item name and field name first.

## Profile loading

`/root/.profile` should load the live env file near the top:

```bash
if [ -f /root/.openclaw/.env ]; then
  set -a
  . /root/.openclaw/.env
  set +a
fi
```

Keep this before sourcing `.bashrc`.

## Why this model exists

This setup is intentionally simple:
- one canonical template
- one generated runtime env file
- one sync script
- one default shell loading path
- one runtime home under `/root/.openclaw/`

Avoid adding helper wrappers like `ocenv` or `withocenv` unless the user explicitly prefers them. The current standard is default env inheritance through `/root/.profile`.

## Validation

After implementing or changing the setup, verify:

1. `/root/.openclaw/env-sync.sh` exists and is executable.
2. `/root/.openclaw/env-sync.sh` succeeds.
3. `/root/.openclaw/.env` contains the expected variable names.
4. `bash -lc 'echo ${GITHUB_TOKEN:+set}'` shows the token is available.
5. `sh -lc 'echo ${GITHUB_TOKEN:+set}'` also shows it is available.
6. A token-dependent CLI works without wrapper commands.

## Troubleshooting

If a token exists in `.env` but commands cannot see it:
- check whether `/root/.profile` is sourcing `.env`
- check whether the command path actually launches a shell that reads the profile
- check whether the token value is valid, not just present

If sync fails:
- check the 1Password item name and field name in `.env.tpl`
- check that `/root/.openclaw/.env.bootstrap` contains what `op inject` needs
- check that `/root/.openclaw/env-sync.sh` is the installed current version

Interpret common GitHub failures this way:
- `401 Bad credentials` means the token value is wrong, expired, or revoked
- `403` usually means the token is valid but under-scoped or blocked by org policy

## Default recommendation

When reproducing this setup on another machine:
- keep secrets canonical in `/root/.openclaw/.env.tpl`
- install the packaged sync script to `/root/.openclaw/env-sync.sh`
- sync to `/root/.openclaw/.env`
- auto-load `/root/.openclaw/.env` from `/root/.profile`
- prefer simple default inheritance over per-command wrappers
