---
name: edit-only
description: Edit code without running any task or terminal
argument-hint: "[scope]"
related:
  - deep-review-codebase
  - update-references

---

## Goal

Define the rules for editing code without running any task or terminal

## Scope

Use this workflow when the task is code editing only, with no need to verify the result by running it

## Execute

### 1. Task Identification

> Goal: Confirm the task is a code-only edit

Run `/deep-review-codebase` to check import usage and export strategy, and confirm the task is a code-only edit

### 2. Code Modification

> Goal: Files are modified with file editing tools only

Use `edit` or `multi_edit` for modifying files and `write_to_file` for creating new files, then run `/update-references` to update all references

### 3. Validation

> Goal: Confirm no execution tools were invoked

Verify that no `run_command` was invoked, no background process was run, and no browser preview was opened

## Rules

### 1. Execution Restrictions

All execution tools are forbidden; perform only file editing operations

- Never run any `run_command`
- Never run background processes
- Never open `browser_preview`

### 2. File Operations

Use only file modification tools

- `edit` - edit existing files
- `multi_edit` - edit multiple points in one file
- `write_to_file` - create new files
- `read_file` - read files for verification

### 3. Quality Assurance

Maintain code quality per the standard

- Run `/deep-review-codebase` for the edits
- Keep consistency with the codebase
- Add comments when necessary

## Expected Outcome

- Code is edited without running any command
- Changes are saved to files correctly
- No process or terminal was run
- Code quality still meets the standard
