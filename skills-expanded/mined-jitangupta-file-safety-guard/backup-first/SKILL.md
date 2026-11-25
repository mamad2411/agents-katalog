---
name: backup-first
description: >
  Automatic file backup before any modification. Use when a file is about to be edited,
  modified, or transformed. Creates timestamped backup copies in a _backups/ folder,
  manages backup rotation (max 3 per file), and provides post-task summaries of
  all modifications and backups created.
---

# Backup First

No file should ever be changed without a backup existing first.

## Rules

### 1. Create Backup Before Every Edit

- Before editing any file, create a backup copy in a `_backups/` subfolder inside the current working folder.
- The backup must be created and confirmed **before** any modifications begin on the original file.

### 2. Backup Naming Format

Use this exact format: `originalname_backup_YYYYMMDD_HHMM.ext`

Examples:
- `index.html` → `_backups/index_backup_20260209_1430.html`
- `styles.css` → `_backups/styles_backup_20260209_1430.css`
- `report.docx` → `_backups/report_backup_20260209_1430.docx`

### 3. Maximum 3 Backups Per File

- Keep a maximum of **3 backups** per original file.
- When creating a 4th backup, delete only the **oldest** backup for that specific file.
- Do not delete backups belonging to other files.

### 4. Session Startup Check

- At the **start of every session**, check if the `_backups/` folder exists in the working directory.
- If it does not exist, create it immediately.
- This check should happen before any file work begins.

### 5. Post-Task Summary

After completing any task that involved file modifications, show the user a summary:

```
✅ Task complete
─────────────────────────────
Files modified:    X
Backups created:   X
Backup location:   _backups/
─────────────────────────────
```

## Activation

This skill activates when:
- A file is about to be edited or modified
- A new session begins (for the startup check)
- A task involving file changes is completed (for the summary)
