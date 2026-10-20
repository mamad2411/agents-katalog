---
name: all-this-patterns
description: Find all patterns in scope and apply the changes for every pattern completely
argument-hint: "[patterns...]"
related:
  - search
  - rename
  - update-references
  - use-scripts
  - follow-parallel
  - report
  - suggest-next-action
  - ask-me
---

## Goal

Search for multiple patterns in scope, then apply the changes, edits, or updates for each pattern completely.

## Scope

Use when the user wants to fix every match of several patterns, such as renaming a function across all files, rewording across every skill, or updating a format across every repo.

## Execute

### 1. Define Patterns

> Goal: Know everything to search for and fix

1. Take the list of patterns and actions from the argument
2. If unclear → run `/ask-me`
3. Determine scope: files, skills, directories, or repo

### 2. Find All Matches

> Goal: Find every matching location

1. Use `/search-files-patterns` to find every match
2. Use `grep` or `ast-grep` when you need precision
3. Record the list with file path, line number, and context

### 3. Plan Changes

> Goal: Plan all the changes

1. Group matches by pattern
2. Choose a strategy: bulk edit, script, or manual
3. If there are multiple files, use `/use-scripts`
4. For renames, use `/rename` (supports batch file rename by pattern)
5. To switch skills in sequence, use `/follow-your-suggestion`

### 4. Apply Patterns

> Goal: Fix every match according to the patterns

1. Do a dry run first if it is destructive
2. Edit batch by batch, or all at once with `/follow-parallel`
3. Verify that no files outside the scope are damaged
4. If high-risk → ask the user to confirm first

### 5. Update References

> Goal: Update cross-references

1. Run `/update-references` if there are renames or moves
2. Check for broken references

### 6. Validate

> Goal: Confirm everything was applied completely and correctly

1. Run `grep` or `review` to check that no old matches remain
2. Run `/run-check` if it is code
3. Run `/deep-validate` if needed

### 7. Report

> Goal: Summarize the results

1. Run `/report table` with columns: `No.`, `Pattern`, `File`, `Match`, `Action`, `Status`
2. Run `/suggest-next-action`

## Rules

- Do a dry run before large changes
- Do not apply without user confirm if high-risk
- Every edit must have a clear pattern
- If there are renames, update references immediately
- Do not damage files outside the scope

## Expected Outcome

- A list of every match grouped by pattern, along with the action applied
- No old matches left
- References fully updated
- A clear status report
