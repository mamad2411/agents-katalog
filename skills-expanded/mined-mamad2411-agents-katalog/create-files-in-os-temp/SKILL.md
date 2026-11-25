---
name: create-files-in-os-temp
description: Create temporary files or directories in the OS temp directory
argument-hint: "[scope]"
related:
  - cleanup-files-in-computer
  - cleanup-files-in-project
  - create-new-project-in-drive-d

---

## Goal

Create temporary files or directories in the OS temp directory (`%TEMP%` on Windows, `/tmp` on Unix) without touching the project

## Scope

Use when creating test files, scratch files, or temporary output that doesn't need to live permanently in the workspace

## Execute

### 1. Determine Temp Path

> Goal: Identify the OS temp directory

1. On Windows: use `$env:TEMP` or `%TEMP%`
2. On macOS/Linux: use `$TMPDIR` or `/tmp`
3. Create a sub-directory for the task if needed, e.g. `temp-<project>-<timestamp>/`
4. Determine the full path for the output

### 2. Create Temp Files

> Goal: Create the files or directories as needed

1. Create directories with `New-Item -ItemType Directory -Path <path>` or `mkdir -p <path>`
2. Create files with `write` or `New-Item -ItemType File -Path <path>`
3. Use meaningful file names, with a prefix or suffix marking them as temp
4. If you need multiple files → create them in the same temp directory

### 3. Use Temp Files

> Goal: Work with the temporary files

1. Reference temp files by absolute path
2. When passing them to external tools → send the path as an argument
3. If a file must be kept before cleanup → copy it into the workspace first
4. Do not create sensitive data in temp without protection

### 4. Cleanup

> Goal: Remove temp files when the work is done

1. If the files are no longer needed → delete with `Remove-Item -Recurse <path>` or `rm -rf <path>`
2. If the user wants to keep them → copy into the workspace before deleting
3. Check that the temp directory has no unused leftovers

## Rules

### 1. Temp Only

- Create files in the OS temp directory only
- Do not create files in the project root without need
- Do not overwrite the user's existing files in temp without telling them

### 2. Naming

- Use a prefix or suffix such as `devin-temp-`, `-tmp`
- Include a timestamp if there are multiple rounds
- File names must have no spaces or special characters that break commands

### 3. Security

- Do not expose secrets in temp files
- If there is sensitive data → delete it immediately after use
- Do not create temp files in a shared temp that is generally readable when the content is sensitive

- Use /cleanup-files-in-computer if needed
- Use /cleanup-files-in-project if needed
- Use /create-new-project-in-drive-d if needed

## Expected Outcome

- Temporary files or directories are created in the OS temp
- The absolute paths of the temp files are correct
- The files are usable as intended
- Files are cleaned up or copied back to the workspace as agreed
