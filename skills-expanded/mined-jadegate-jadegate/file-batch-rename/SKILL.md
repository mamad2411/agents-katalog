---
name: file-batch-rename
description: Safely batch rename files in a directory using regex patterns. Includes dry-run preview, collision detection, and automatic rollback on failure. Zero network access required.
---

# File Batch Rename SOP

Safely batch rename files in a directory using regex patterns. Includes dry-run preview, collision detection, and automatic rollback on failure. Zero network access required.

## When to Use

- User wants to batch rename
- User wants to rename files
- User wants to file rename
- Keywords: file, batch, rename, regex, local

## Required Parameters

- **directory** (string): Target directory containing files to rename
- **pattern** (string): Regex pattern to match filenames
- **replacement** (string): Replacement string (supports regex groups like $1, $2)

## Optional Parameters

- **dry_run** (boolean): If true, only preview changes without executing (default: True)
- **file_filter** (string): Glob pattern to filter files, e.g. '*.jpg' (default: *)
- **recursive** (boolean): Whether to process subdirectories (default: False)

## Output

- **renamed_count** (number): Number of files renamed
- **skipped_count** (number): Number of files skipped (no match)
- **preview** (array): Array of {old_name, new_name} pairs
- **dry_run** (boolean): Whether this was a dry run

## Security

- Sandbox level: strict
- Max execution time: 60000ms
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `list_files` -> 11 steps -> Exit: `return_preview`, `return_executed`, `abort_no_files`, `abort_collision`
