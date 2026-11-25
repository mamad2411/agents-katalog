---
name: migrating-dev-machine
description: Migrates an existing dev machine into the managed pattern — either in place on the same machine, or from an old server to a fresh new one (inventory, staged home copy, three-way dotfile merge, selective package reinstall). Use when moving to a new server/VM, upgrading Ubuntu by rebuild, adopting server-config/chezmoi/devbox on a machine that already has state, or decommissioning an old box.
---

# Migrating a dev machine

Two paths:

- **New server** (old box → fresh box): see [reference/new-server.md](reference/new-server.md)
- **In place** (same machine, adopt the managed pattern): see [reference/in-place.md](reference/in-place.md)

Both start with the same inventory. Run `scripts/machine-inventory.sh` on the
machine whose state you want to capture; it writes
`~/machine-inventory-<date>/` covering: system info, `apt-mark showmanual`,
apt history commandlines (the authoritative record of what was typed),
modified dpkg conffiles, custom system paths, services/timers/cron,
non-APT tool locations and per-manager package lists, and Docker
containers/volumes/mounts.

## Safety rules (non-negotiable)

- Provider snapshot of every involved machine **before** any change.
- Never rsync with `--delete` into a live home directory — only into a
  staging copy.
- Never overwrite `.ssh/` blindly: union `authorized_keys`, keep both
  private keys under distinct names, keep the working key working.
- Never restore wholesale: `/etc/passwd|group|shadow`, `/etc/machine-id`,
  `/etc/ssh/ssh_host_*`, `/etc/netplan`, `/etc/fstab`, `/etc/cloud`,
  `/etc/apt` — these identify the old machine. Re-add third-party apt
  repos from current instructions, not copied files (`apt-key` is gone).
- Keep the old machine's disk/snapshot until the new one has survived
  normal use plus one full backup cycle.

## Core principles

- **Copy state, reinstall runtimes.** Config, history, project data, and
  caches come across in the home copy; executables and toolchains (nvm,
  rustup, claude, codex, devbox...) are reinstalled so installers recreate
  a consistent install for the new OS. Apply one rule to all tools — don't
  special-case Rust.
- **Packages:** reinstall from an approved list derived from apt history
  `Commandline:` entries cross-checked against `apt-mark showmanual` —
  never replay the full manual list (it contains cloud-image packages) and
  never reproduce the old dependency graph.
- **Docker:** migrate compose files, `.env`s, bind-mounted data, named
  volumes with real data. Do not migrate images, build cache, or stopped
  disposable containers — rebuild/pull.
- As you rebuild, record every step in `$SERVER_CONFIG_DIR` (see
  setting-up-dev-machine) so the *next* migration is a controlled rebuild,
  not forensics. Commit the inventory dir into
  `$SERVER_CONFIG_DIR/inventories/`.

## Scripts

- `scripts/machine-inventory.sh` — capture full machine inventory (run on old machine)
- `scripts/home-conflicts.sh STAGED_OLD_HOME [LIVE_HOME]` — old-only /
  shared-differences / new-only reports between a staged home copy and the
  live home
