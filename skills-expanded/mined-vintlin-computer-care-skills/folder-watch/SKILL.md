---
name: folder-watch
description: Use when watching a folder for file changes to run commands on edit, restart a local service, trigger a backup, send a notification, or debug file-change automation on macOS or Linux.
---

# Folder Watch

## Overview

Folder watchers should be explicit about what is watched, what command runs, where logs go, and how failures are reported. Prefer reversible local automation before installing persistent agents.

## Workflow

1. **Define watched paths and ignore rules.** Exclude noisy temporary files (swap files, build artifacts, `.DS_Store`) by extension or glob. Debounce or filter aggressively — do not restart a service on every transient write.
2. **Choose the watcher.** Prefer `watchexec` when available; fall back to a simple polling script otherwise. Always set an explicit working directory (`--workdir` or `cd`). On macOS avoid Linux-only flags like `find -newermt` — use `stat -f %m` or a portable alternative.
3. **Decide event handling.** Choose debounce (coalesce rapid changes), restart (kill and re-run on each event), or queue.
4. **Capture stdout/stderr to a log file.** Make the log path explicit.
5. **Add notification only after the command is reliable.** Keep credentials out of skill files and scripts — use environment variables, keychain, or a local secret manager. Include command, exit code, log path, and changed file in notifications. Avoid sending sensitive file contents.
6. **Test with a harmless file change before enabling persistent automation.** Do not install a launchd or systemd watcher until a foreground test succeeds end-to-end.

## Quick Examples

Run a command after changes:

```bash
watchexec --restart --watch ./src --ext py -- 'python script.py'
```

Debounce noisy changes:

```bash
watchexec --debounce 2s --watch ~/Downloads -- 'echo changed'
```

Portable recent-file check for macOS:

```bash
find . -type f -maxdepth 2 | while read -r file; do
  mtime=$(stat -f %m "$file" 2>/dev/null || stat -c %Y "$file" 2>/dev/null || echo 0)
  now=$(date +%s)
  [ $((now - mtime)) -le 60 ] && printf '%s\n' "$file"
done
```
