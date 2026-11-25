---
name: freeing-disk-space
description: Use when a Mac is running low on disk space or storage is full - "startup disk almost full", "only X GB left", "free up space", "what is eating my disk", "clean up my Mac", or /freeing-disk-space. macOS only.
---

# Freeing Disk Space (macOS)

Measure, then recommend; never guess. Rank findings by measured size and
reversibility, gate every deletion behind line-item approval, verify with df.

## Ground truth

- The real number is `Avail` from `df -h /System/Volumes/Data`. Finder and
  About This Mac add purgeable space, so they read tens of GB higher. Quote
  the df number and say which one you are quoting.
- Read-only scanning is pre-authorized. Nothing gets deleted, moved, or
  shrunk until the user approves specific line items.

## Survey pass

Start with a full top-level sweep so nothing named or unnamed escapes:
`du -xsm ~/* | sort -rn | head -20` and `du -xsm ~/.[!.]* | sort -rn | head -15`.
This is what catches sync folders (Dropbox, `~/Library/CloudStorage`), forgotten
archive dirs, and tool dotdirs (`~/.codex ~/.asdf ~/.npm ~/.cache ~/.ollama
~/.lmstudio ~/.docker`). Always use `-x` so du does not cross into mounts.

Then drill winners with `du -xsm <dir>/* | sort -rn | head`, always including:

- `~/Library/Caches` `~/Library/Application Support` `~/Library/Containers` `~/Library/Group Containers` `~/Library/Developer` (du of `~/Library` top-level first, these five are the usual winners)
- One-shot checks: `tmutil listlocalsnapshots /`, `brew cleanup -n`, iOS backups at `~/Library/Application Support/MobileSync/Backup`
- Skip `~/Library/Mobile Documents` (iCloud placeholders make sizes meaningless)
- Fully-synced sync-client folders (Dropbox, iCloud) are often the largest single item and are move-not-delete: flag for online-only offload, never rm

## Known heavyweights

| Finding | Reclaim with |
|---|---|
| Browser caches under `~/Library/Caches/` | Quit browser, `rm -rf` the cache dir; it regenerates. Never touch the browser's `Application Support` profiles (passwords, sessions) |
| Homebrew cache + old versions | `brew cleanup --prune=all -s` |
| iOS simulators (`~/Library/Developer/CoreSimulator`) | `xcrun simctl delete unavailable`, or `delete all` |
| Xcode `DerivedData`, `iOS DeviceSupport` | `rm -rf`; rebuilt on demand |
| `Docker.raw` in `~/Library/Containers/com.docker.docker` | `docker system prune -a` then shrink disk image in Docker settings; if Docker is unused, uninstall or purge data |
| VM bundles (UTM, Parallels) | Move the bundle to an external drive or delete inside the app |
| `node_modules` / venvs | `fd -HI -t d '^(node_modules|\.venv|venv)$' --prune . <code-dir> -x du -xsm {} \| sort -rn`; delete for inactive repos, rebuild with npm/uv |
| Time Machine local snapshots | `tmutil deletelocalsnapshots <date>` only if the listing showed any |
| Fully-synced Dropbox / iCloud folders | Make Available Online Only / Optimize Mac Storage (a move, not a delete) |
| Messages attachments | System Settings > General > Storage > Messages; warn that iCloud sync propagates deletions to all devices |

## Output contract

Present one ranked table: item, measured size, tier, exact command.
Tiers: (1) regenerable cache, (2) rebuildable artifact, (3) likely unused,
needs confirmation, (4) personal data, recommend move not delete.
End by asking which line items to execute. After executing approved items
only, show before and after `df -h` Avail as evidence.

## Common mistakes

- Quoting Finder free space, or mixing purgeable into the target.
- Deleting a browser's `Application Support` instead of its `Caches`.
- Recommending snapshot or iOS-backup purges without checking they exist.
- Clearing caches of running apps; quit the app first.
- Forgetting hidden dotdirs and `~/Library/Containers` (Docker, VMs, and Messages data live there).
