---
name: backing-up-dev-machine
description: Backup and restore for the persistent-state layer of a managed dev machine — what to back up, what to rebuild instead, and restore order. Use when setting up backups, before risky changes or migrations, when asked what would be lost if the machine died, or when restoring agent state, repos, or container data.
---

# Backing up a dev machine

The managed layers (host manifest, chezmoi, devbox configs, overlays) are already
in git — a backup of `$SERVER_CONFIG_DIR`'s remote covers them. This skill
covers everything git deliberately does NOT hold.

## Back up

| State | Notes |
|---|---|
| `~/repos/` | uncommitted/unpushed work is the real exposure — `git status`/`git log @{u}..` across repos tells you how much |
| Agent state: `~/.claude/`, `~/.codex/`, similar | sessions, settings, history |
| Agent container homes (`~/.*-containers/`) | bind-mounted session state |
| Docker bind-mounted data dirs & named volumes with real data | databases via native dump, not filesystem copy of a running container |
| Secrets: `~/.ssh/` keys, tokens, `.env` files | encrypted backup or secret store — never the config repo |
| `/etc/.git` (etckeeper history) | contains sensitive material; backup target must be private |
| Migration/baseline inventories | tiny; also committed to server-config |

## Rebuild instead (do not back up)

Docker images and build cache; `~/.cache`; toolchains
(`~/.rustup`, `~/.nvm/versions`, devbox/nix store); `node_modules`,
`target/`; package-manager registries (`~/.cargo/registry`). All
reproducible from the managed layers.

## Mechanics

Any snapshotting tool works; restic-style incremental to an off-machine
target is the default choice. Whatever the tool, the include list above and
exclude list live in `$SERVER_CONFIG_DIR` and are commit-tracked. Run a
restore drill once: the migrating-dev-machine new-server path doubles as
the full restore procedure (staged copy → conflict reports → selective
apply).

Restore order: setting-up-dev-machine first (managed layers from git),
then restore backed-up state into place, then reinstall tools via
installing-dev-tools so runtimes match the new OS.
