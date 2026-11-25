---
name: all-files
description: Run one task or workflow across every file in the project until all files are covered
argument-hint: "[scope]"
related:
  - deep-analyze
  - deep-validate
  - resolve-errors
  - refactor
---

## Goal

Work through every file in the project following the specified workflow

## Scope

Use `all-files` for the designated tasks and workflows only

## Execute

### 1. Discover Files

> Goal: Discover Files

1. Run `/deep-analyze` to inspect the structure.
2. Use `find_by_name` or `list_dir` to locate files by pattern.

### 2. Process Each File

> Goal: Process Each File

1. Read files in parallel with `read_file`.
2. Edit files sequentially with `edit` or `multi_edit`.
3. Apply the workflow relevant to each file.

### 3. Verify

> Goal: Verify

1. Confirm every file has been processed.
2. Run `/deep-validate` to check correctness.

## Rules

### 1. Processing Order

- Process foundation files first (config, types, utilities)
- Process files with complex dependencies later

### 2. Batch Operations

- Read files in parallel
- Edit files sequentially to avoid conflicts

### 3. Error Handling

- Record files that had problems
- Run `/resolve-errors` for files with issues

## Expected Outcome

- Every file in scope is fully processed