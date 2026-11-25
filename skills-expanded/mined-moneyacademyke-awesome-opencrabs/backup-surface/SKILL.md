---
name: backup-surface
description: Back up the unique reusable OpenCrabs surface to a sanitized local git workspace, with allowlist collection, secret scanning, restore support, and explicit approval before any GitHub push.
---

# OpenCrabs Surface Backup

Use this skill when the user asks to back up, restore, inspect, or prepare a GitHub backup of the unique reusable surface of this OpenCrabs instance.

## Goal

Create and maintain a sanitized backup snapshot of reusable OpenCrabs artifacts:

- skills
- slash commands
- dynamic tool definitions
- selected non-private brain files
- selected sideloaded project code

Do **not** back up runtime/private artifacts unless the user explicitly requests an encrypted workflow.

## Workspace

Backup workspace:

```text
~/.opencrabs/projects/opencrabs-surface-backup/files/
```

Snapshot output:

```text
~/.opencrabs/projects/opencrabs-surface-backup/files/snapshot/
```

Policy manifest:

```text
~/.opencrabs/projects/opencrabs-surface-backup/files/manifest.edn
```

## Hard safety rules

Never include:

- `keys.toml`
- `.env` or `*.env`
- SQLite/database files
- logs
- session transcripts
- memory logs
- channel attachments
- secrets directories
- virtualenvs
- build output
- node_modules

Use the allowlist in `manifest.edn`. Do not improvise a raw `git add ~/.opencrabs` backup. That is how private data leaks.

## Commands

Run all commands from the backup workspace with the `bash` tool:

```text
cd ~/.opencrabs/projects/opencrabs-surface-backup/files
```

### Collect

```text
bb backup:collect
```

Copies only allowlisted files into `snapshot/`.

### Scan

```text
bb backup:scan
```

Fails if the snapshot contains denied paths, oversized files, unreadable/binary files, or secret-looking patterns.

### Status

```text
bb backup:status
```

Shows snapshot file count and git status when initialized.

### Initialize local repo

```text
bb backup:init
```

Creates a local git repo in the backup workspace if missing.

### Commit locally

```text
bb backup:commit "backup opencrabs surface"
```

Runs scan first, then commits the sanitized snapshot locally.

### Restore

Dry run by default:

```text
bb backup:restore
```

Apply only when explicitly requested:

```text
bb backup:restore --apply
```

## GitHub push policy

Pushing to GitHub is an external side effect and requires explicit user approval every time.

Before pushing:

1. Run `bb backup:collect`.
2. Run `bb backup:scan` and require success.
3. Run `git status --short`.
4. Show the intended remote/repo name.
5. Ask for explicit approval to create or push the GitHub repo.

Recommended repo:

```text
opencrabs-surface
```

Recommended visibility:

```text
private
```

Do not push personal/private memory unless a separate encrypted backup workflow exists.

## Restore policy

Restore is non-destructive by default. `bb backup:restore` only prints what would be restored. Use `--apply` only after explicit user request.
