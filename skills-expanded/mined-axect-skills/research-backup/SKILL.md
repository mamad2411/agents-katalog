---
name: research-backup
description: Back up untracked research report directories (outputs/, results/, report(s)/) from local projects into the locally synced Dropbox folder, organized by category/project. Discovers candidate directories that git does not track, keeps a registry under ~/.config/research-backup/, and mirrors additively with rsync (deletions are never propagated). Use when the user asks to back up research outputs or reports to Dropbox, register new report directories for backup, check what would change before backing up, or says backup outputs, research backup, outputs 백업, 결과 백업, 리포트 백업, 연구 백업, Dropbox 백업 모음. For single-file upload/download/share through the Dropbox API use the dropbox skill instead.
---

# Research Backup

Backs up the report/output directories that research projects keep outside git (`outputs/`, `results/`, `report/`, `reports/`) into the locally synced Dropbox folder. The Dropbox daemon handles the actual upload; this skill only writes files under `BACKUP_ROOT` with rsync, so backups are incremental and need no API credentials.

## Which Dropbox skill?

- `research-backup` (this skill): bulk, recurring backup of whole report directories into the local `~/Dropbox` sync folder. Requires the Dropbox client to be syncing this machine.
- `dropbox`: one-off upload/download/share of individual files through the Dropbox HTTP API. Works without a local sync client.

## How projects are separated

Sources are mirrored relative to `SCAN_ROOT` (default `$HOME/Documents/Project`), so the Dropbox side keeps the full `<category>/<project>/<dir>` layout:

    ~/Documents/Project/Research/MyProject/results  ->  ~/Dropbox/ResearchBackup/Research/MyProject/results

Same-named projects in different categories (e.g. two `pytorch_template` checkouts) never collide because the category directory is part of the destination path.

## Prerequisites (check before any operation)

1. `rsync` on PATH.
2. A locally synced Dropbox folder. Verify the parent of `BACKUP_ROOT` exists (default check: `test -d ~/Dropbox`). If it does not exist, tell the user the Dropbox client is not syncing this machine and stop; do not fall back to the API.
3. The Dropbox daemon must be running for local writes to reach the cloud. `backup.sh` only copies into `~/Dropbox`; the actual upload is asynchronous and done by the daemon. If `dropbox-cli` is on PATH (AUR package `dropbox-cli`), run `dropbox-cli status` to confirm the daemon is up and watch live progress. If it is missing or reports the daemon stopped, warn the user that the backup will be written locally but will not upload until the daemon starts, and recommend installing it (`paru -S dropbox-cli`).

## Config and registry

Both live under `~/.config/research-backup/` (override the directory with the `RESEARCH_BACKUP_CONFIG_DIR` env var; both files are auto-created with defaults on first run):

- `config`: shell KEY="value" lines. `SCAN_ROOT` (project root), `BACKUP_ROOT` (destination inside Dropbox, default `$HOME/Dropbox/ResearchBackup`), `DIR_NAMES` (basenames discover looks for, default `outputs results report reports`), `RSYNC_EXCLUDES` (optional space-separated rsync exclude patterns such as `*.ckpt wandb`).
- `registry`: one absolute source directory per line, `#` comments allowed. Backups run only over this file, never over a live scan, so the set of backed-up directories is always explicit. To stop backing a directory up, delete its line (already-uploaded files stay in Dropbox).

## Workflow

### 1. Discover (scan for new candidates)

    bash scripts/discover.sh

Scans `SCAN_ROOT` for `DIR_NAMES` directories and prints a `STATE GIT PATH` table:

- `NEW`: not in the registry and git does not track it (`ignored`, `untracked`, or `no-git`). Candidate for registration.
- `REGISTERED`: already in the registry.
- `TRACKED`: contains git-tracked files, so git already backs it up. Skipped, never registered.
- `MISSING`: registry entry whose directory no longer exists on disk.

Show the user the `NEW` rows and ask which to register (default: all of them). Then run:

    bash scripts/discover.sh --register

which appends every `NEW` path to the registry. To register a subset instead, append the chosen paths to `~/.config/research-backup/registry` directly, one per line.

### 2. Status (preview before syncing)

    bash scripts/backup.sh --dry-run --all

Same matching as a real backup but passes `-n` to rsync, printing `PEND <rel> N item(s) would sync` per directory. Use this when the user asks "what changed" or before a first large sync.

### 3. Backup

    bash scripts/backup.sh --all              # everything in the registry
    bash scripts/backup.sh MyProject          # entries whose path contains "MyProject" (case-insensitive)
    bash scripts/backup.sh Research/ AI_Project/   # multiple filters, OR-matched

Per-directory output is `OK <rel> N item(s) synced -> <dest>` or `up to date`, with a one-line summary at the end. Missing sources are warned and skipped, never fatal. Note: "synced" here means copied into the local `~/Dropbox` folder, not uploaded to the cloud yet; see step 4.

### 4. Verify cloud sync (recommended)

`backup.sh` only copies into the local `~/Dropbox` sync folder; the Dropbox daemon uploads to the cloud afterwards, asynchronously. After a backup, especially a large one, confirm the upload actually finished:

    dropbox-cli status        # "Up to date" when done; "Syncing N files" while still uploading

A backup reported `OK ... synced` while the daemon was stopped is sitting on local disk only and will upload once the daemon starts. If `dropbox-cli` is not installed, install it (`paru -S dropbox-cli`) or watch the Dropbox GUI.

## Safety rules

- Backups are additive: rsync runs without `--delete`, so deleting or renaming files locally leaves the old copies in Dropbox. This is intentional (the backup protects against accidental deletion). If the user explicitly wants the Dropbox side pruned to match local, do not add `--delete` yourself; tell them to clean the Dropbox folder manually or get their confirmation first and run a one-off `rsync -a --delete` for the specific directory they name.
- Never register a `TRACKED` directory; git already preserves it.
- Do not run `discover.sh --register` without showing the user the `NEW` list first, unless they asked for a fully automatic run.

## Exit codes

- 0: success
- 2: config invalid, `SCAN_ROOT` missing, or Dropbox sync folder absent
- 3: no registry entry matched the filter
- 5: at least one rsync invocation failed (stderr shows which)
- 64: usage error
- 127: rsync not installed
