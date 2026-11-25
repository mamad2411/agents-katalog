---
name: touch_file
description: Recovery strategy when the Write tool fails to create a new file. Use this skill whenever a Write or Edit tool call fails with an error related to creating a new file — such as missing parent directories, permission issues, or "file not found" errors on files that don't exist yet. This skill does NOT apply to editing existing files that fail for other reasons. Trigger when you see Write/Edit errors on new file creation, when file creation fails unexpectedly, or when you get path-related errors trying to create files in nested directories.
user-invocable: false
allowed-tools:
  - Bash(mkdir *)
  - Bash(touch *)
---

# touch_file

When a Write or Edit tool call fails while trying to create a new file, recover by using `touch` via the Bash tool to create the empty file first, then retry the Write.

## Why this matters

The Write tool can fail when creating new files — often because parent directories don't exist, or the filesystem needs the file to be created differently. Rather than giving up or trying workarounds, a quick `mkdir -p` + `touch` reliably sets up the file path so the Write tool succeeds on retry.

## Recovery steps

When Write or Edit fails on a **new file** (not an existing one):

1. **Create parent directories** — run `mkdir -p <parent-directory>` via Bash to ensure the full directory path exists.
2. **Create the empty file** — run `touch <filepath>` via Bash.
3. **Retry the Write** — use the Write tool again with the same content. It should succeed now.

You can combine steps 1 and 2:

```bash
mkdir -p src/utils && touch src/utils/helpers.ts
```

## When this applies

- A Write tool call fails and the target file **does not already exist**
- The error mentions missing directories, file not found, or path issues
- You're trying to create a file in a nested directory structure

## Edge case: broken symlinks

If `mkdir -p` fails because a broken symlink occupies a path component (error like `No such file or directory` even though `mkdir -p` should create it), the symlink is pointing to a nonexistent target and blocking directory creation. **Do not remove it automatically** — the symlink may be there intentionally. Instead, tell the user what you found and ask how they'd like to proceed (e.g., remove the symlink, fix its target, or choose a different path).

## When this does NOT apply

- Edit or Write fails on a file that **already exists** — that's a different problem
- The error is unrelated to file creation (e.g., permission denied on an existing file, disk full)
