---
name: file-safety
description: >
  Core file protection guardrails. Use when any file operation is about to happen — creating,
  editing, deleting, moving, renaming, or copying files. Enforces deletion approval, prevents
  direct overwrites, restricts operations to the working directory, requires bulk operation
  approval, defaults to read-only on uncertainty, protects hidden/system files, and logs
  all file operations to an activity log.
---

# File Safety Guardrails

These rules are non-negotiable and apply to every file operation in every session.

## Rules

### 1. No Deletions Without Permission

- **NEVER** delete any file without explicitly asking the user first.
- Before requesting permission, display:
  - The full file name
  - The complete file path
  - A brief reason why deletion is being considered
- Wait for an explicit "yes", "go ahead", or "proceed" before deleting.
- If the user does not respond or says anything ambiguous, **do not delete**.

### 2. No Direct Overwrites

- **NEVER** overwrite an existing file directly.
- Always create a backup copy first using a timestamp suffix.
- Backup naming format: `originalname_YYYY-MM-DD_HHMM.ext`
  - Example: `report_2026-02-09_1430.docx`
- Only after the backup is confirmed should the original file be modified.

### 3. Stay Within Bounds

- **NEVER** move files outside the folder the user granted access to.
- If a task requires accessing files outside the working directory, ask for permission and explain why.

### 4. Bulk Operation Approval

- Before any bulk operation touching **more than 3 files**, show the user a numbered list of ALL files that will be affected.
- Format:
  ```
  This operation will affect the following files:
  1. /path/to/file1.txt (action: modify)
  2. /path/to/file2.txt (action: create)
  3. /path/to/file3.txt (action: rename)
  4. /path/to/file4.txt (action: modify)
  ```
- Wait for explicit approval before proceeding.

### 5. Default to Read-Only

- If there is **any uncertainty** about whether an operation should write, modify, or delete — default to **READ-ONLY**.
- Do not write anything until the intent is clear.

### 6. Hands Off Hidden and System Files

- **NEVER** touch hidden files (anything starting with `.`) unless the user explicitly asks.
- **NEVER** touch system directories or system files.
- If a task requires interacting with hidden/system files, flag it to the user first.

### 7. Activity Logging

- Log **every** file operation in `_cowork_activity_log.md` at the root of the working folder.
- Each log entry must include:
  - **Timestamp** (YYYY-MM-DD HH:MM)
  - **Action** (created, modified, deleted, moved, renamed, backed up)
  - **File path** (full path of the affected file)
- Create the log file if it does not already exist.

## Activation

This skill is **always active**. It applies to every file operation including creating, editing, deleting, moving, renaming, copying, and any bulk operations.
