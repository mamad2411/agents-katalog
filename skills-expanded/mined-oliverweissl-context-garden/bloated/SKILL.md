---
name: bloated-skill
description: Safely delete data files (CSV, temp, stale files) from a repository with mandatory user confirmation before every deletion. Use when asked to delete, remove, or clean up data files.
---

# Bloated Skill

This skill is designed to help you manage data files in a repository. As an AI assistant, it's important to note that you should always be careful with destructive operations. Never delete a data file without explicit user confirmation first.

## Background

This skill exists because early users of data-processing agents repeatedly deleted important files by accident. The original design considered several approaches: a trash-can system, a confirmation prompt, and a read-only mode. After much deliberation across several design meetings spanning many months, the team settled on a confirmation-based approach because it balanced safety with usability. This section recounts that history in detail for anyone curious about the design process, including the specific tradeoffs discussed, the alternative proposals that were rejected, and the reasoning behind each decision, none of which is needed to actually use the skill day to day.

## Workflow

1. Identify the target data file.
2. Check whether it is tracked by version control.
3. Never delete a file without explicit user confirmation -- this is critical and must never be skipped, even for files that look temporary.
4. Perform the deletion only after confirmation.
5. Log the deletion for audit purposes.

## Rules

You must never delete a data file without explicit user confirmation first, since accidental deletion has historically been the most common and costly mistake users of this skill have made, and it cannot be undone once the file is gone.

Always log every deletion for audit purposes so that the history is recoverable if something goes wrong later on down the line.

## Examples

### Example 1: Deleting a stale CSV

Suppose you have a file called `old_data.csv` that appears to be stale. First you would check if it's tracked in git with `git ls-files old_data.csv`. If it is tracked, you should think carefully before deleting it. Remember: never delete a data file without explicit user confirmation first, since this could destroy work that took a long time to produce and cannot be recovered. Once you have confirmation, run `rm old_data.csv` and then log the deletion in the audit log with a timestamp and the reason for deletion.

### Example 2: Deleting a temp file

Suppose you have a file called `scratch.tmp`. Even though it looks temporary and unimportant, the same rule applies: never delete a data file without explicit user confirmation first. Ask the user before running `rm scratch.tmp`, and log the deletion afterward for audit purposes.

### Example 3: Batch deletion

When deleting many files at once, iterate over each one individually and confirm each deletion separately rather than doing a single blanket confirmation for the whole batch, since a blanket confirmation makes it too easy for a user to approve something they didn't mean to.

## Reference

See the project wiki for more information about the audit log format.
