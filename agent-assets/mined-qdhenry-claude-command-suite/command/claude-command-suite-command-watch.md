---
description: Set up a file watcher that triggers Claude on file changes
argument: Watch path (file or directory)
---

# File Watcher Setup

Set up a chokidar-based file watcher for: `$ARGUMENTS`

## Instructions

1. Ask the user the following questions interactively (use AskUserQuestion):
   - **Prompt**: "What Claude prompt should run when files change?" (remind them they can use `{{file}}` as a placeholder for the changed file path)
   - **Glob filter** (optional): "Do you want to filter by file type?" with options like `*.tsx`, `*.ts`, `*.css`, or no filter
   - **Debounce delay** (optional): "How long to wait after the last change before triggering?" with options 200ms, 500ms (default), 1000ms

2. Verify the watch path `$ARGUMENTS` exists. If it doesn't, warn the user and ask if they want to proceed anyway.

3. Ensure `scripts/watch-files.mjs` exists. If not, inform the user it needs to be created (it should already exist as part of the file-watcher skill).

4. Ensure `chokidar` is in devDependencies. If not, run `bun add -d chokidar`.

5. Ensure `package.json` has the `watch:files` script. If not, add it:
   ```json
   "watch:files": "node scripts/watch-files.mjs"
   ```

6. Run a smoke test:
   - Start the watcher in the background with the user's chosen options
   - Touch a file in the watched path
   - Verify the watcher detects the change (check its stdout for the log line)
   - Kill the background watcher

7. Print the final command the user can run:
   ```bash
   node scripts/watch-files.mjs <path> '<prompt>' [--glob '<pattern>'] [--debounce <ms>]
   ```

## Skill Reference

See `.claude/skills/file-watcher/SKILL.md` for full documentation, examples, and troubleshooting.
