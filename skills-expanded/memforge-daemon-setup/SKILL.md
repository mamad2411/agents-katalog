---
name: memforge-daemon-setup
description: Install, configure, verify, repair, or remove the MemForge local daemon as a managed macOS or Linux user service. Use when a user asks to enable local collection, connect a daemon to self-hosted or Cloud MemForge, check daemon readiness, troubleshoot setup, or uninstall the service. Do not use for workspace routing or source configuration.
---

# MemForge Daemon Setup

Use the supported `memforge` CLI. Never create or edit launchd plists, systemd
units, Keychain entries, or daemon JSON files directly. Do not use `sudo`.

## Boundary

This skill owns the host-side CLI installation and daemon user-service
lifecycle. It does not bind repositories to workspaces, configure Sources, or
trigger a sync. Use `memforge-setup` separately for workspace routing.

The service remains server-directed: setup proves connectivity, while Source
schedules and sync actions create the work the daemon later leases.

## Inspect first

Run read-only checks before proposing a mutation:

```bash
uname -s
command -v memforge || true
command -v uv >/dev/null && uv tool list || true
command -v pipx >/dev/null && pipx list || true
memforge target list
memforge daemon status
```

Skip commands that require a missing `memforge` executable. Determine whether
an existing install is managed by `uv tool` or `pipx`; preserve that package
manager when upgrading. Treat these as separate observed states:

- CLI missing or too old to expose `memforge setup` and `memforge daemon`.
- Target configured or absent.
- Native service installed, running, stopped, or absent.
- Local runtime running or stopped.
- Server-observed connection online, offline, or unconfigured.

Do not treat an online heartbeat as proof that a newly replaced process started;
`memforge setup` owns the fresh-heartbeat fence.

## Confirm the mutation

Before changing the machine, show the user:

- package install or upgrade, if needed;
- exact MemForge origin and target name;
- macOS LaunchAgent or Linux systemd user service;
- that a hosted token is entered through a hidden terminal prompt and stored in
  the OS keyring;
- that no root service, cron entry, or plaintext token file will be created.

Ask for confirmation unless the current request already explicitly authorizes
that exact installation and target. Changing to a different origin or removing
an existing service always needs its own explicit authorization.

Never ask the user to paste a token into chat, place it in a command argument,
or display it. The default token variable is `MEMFORGE_API_TOKEN`. Use an
existing token environment variable without printing it and pass
`--token-env VARIABLE` only when the user chose a different variable,
or run setup in a user-visible TTY so the user can answer the hidden prompt. If
no secure interactive path exists, stop and give the user the exact setup
command to run locally.

## Install or upgrade the CLI

Use an isolated tool environment, not system Python. MemForge is in beta and
installers skip beta releases unless asked, so keep the pre-release options, or
the install stops at the older stable release:

```bash
uv tool install --python 3.12 --prerelease allow memforge-ai
uv tool upgrade --prerelease allow memforge-ai
```

or, when the user already uses pipx:

```bash
pipx install --python python3.12 --pip-args=--pre memforge-ai
pipx upgrade --pip-args=--pre memforge-ai
```

Afterward require both commands to exist:

```bash
memforge setup --help
memforge daemon --help
```

## Configure and install the daemon

Resolve the origin explicitly with the user. Use
`http://127.0.0.1:8765` for the ordinary local self-hosted service, or the exact
HTTPS origin for Cloud/custom domains. Do not infer edition from DNS.

Run setup with the confirmed origin so a previously saved active target cannot
silently select another service:

```bash
memforge setup --api-url ORIGIN
memforge setup --api-url ORIGIN --target-name USER_CHOSEN_NAME
```

When the user did not choose a target name, omit `--target-name`; setup uses the
declared edition's stable `local` or `cloud` name. Show a user-chosen name in the
mutation preview before passing it.

Setup discovers `/.well-known/memforge`, validates the declared edition,
authentication, API base, and health route, stores a hosted token only in the
OS keyring, installs the native user service, and waits for a strictly newer
server-observed heartbeat. Do not reproduce those steps manually.

## Verify completion

Run:

```bash
memforge daemon check
memforge daemon status
```

Success requires all of the following, without triggering a Source sync:

- `daemon check` exits zero and reports `healthy`;
- native service is running;
- local runtime is running;
- server connection is `online`.

When both native and runtime PIDs are available, matching values are useful
additional evidence but are not required on platforms that do not expose a
native PID. Report the installed distribution version when package-manager
metadata provides it, plus target origin and edition, service manager, and
connection state. Never report credentials, Keychain account identifiers, or
raw local state.

## Conditional operations

For setup failure, an unhealthy daemon, lifecycle commands, target/token
changes, or uninstall requests, read
[references/operations.md](references/operations.md) before acting.
