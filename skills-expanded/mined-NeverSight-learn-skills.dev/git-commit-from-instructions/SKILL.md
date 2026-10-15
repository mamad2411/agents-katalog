---
name: git-commit-from-instructions
description: Use when a user asks to create a git commit from staged changes or only agent-authored edits while following repository commit-message instructions.
---

## Purpose

Generate a compliant commit message from instruction files, then commit only the intended scope.

This skill is documentation-first and agent-agnostic. It works as an overlay on top of the host workflow.

## Use when

- The user says "commit staged changes" or equivalent.
- The user says "commit only what you changed" or equivalent.
- The user asks to follow repository commit instructions for commit message format.
- The user requests language-specific commit messages.

## Do not use when

- The user asks for history rewriting, squashing, rebasing, or force pushes.
- The user asks to include unrelated changes from the working tree.
- The repository does not have a clear commit scope yet.

## Inputs

- Requested mode: `staged-only` or `agent-only`
- Current git status and staged diff
- Current task context (for detecting agent-authored files)
- Language signals from user input
- Instruction files:
  - `references/git-commit-instructions.ko.md`
  - `references/git-commit-instructions.md`

## Outputs

- One commit that matches the requested scope
- Commit message following selected language instruction
- Clear stop reason if scope or instruction selection is ambiguous

## Interoperability

- Overlay-only: preserve host workflow ownership.
- Do not require Codex-only features or paths.
- Use standard git operations available across agent environments.

## Mode Rules

### `staged-only`

Use already staged changes as the entire commit scope.

1. Inspect staged changes and verify there is at least one staged file.
2. Build the commit message from the selected instruction file.
3. Commit staged changes only.

In this mode, never stage or unstage files unless the user explicitly asks.

### `agent-only`

Commit only files authored by the agent in the current task.

1. Detect candidate files from task context plus current git status.
2. Stage only those candidate files.
3. Verify staged scope contains only agent-authored changes.
4. Build the commit message from the selected instruction file.
5. Commit only that scoped staging set.

If a file mixes user edits and agent edits and safe separation is not possible, stop and ask the user how to proceed.

## Language Selection Rules

Always resolve instruction language in this order:

1. Explicit commit language request in user input.
2. Input language detection from the current request.
3. Default to English.

Examples of explicit overrides:

- "커밋 메시지는 영어로"
- "Write commit message in Korean"

If no explicit override exists, infer input language and choose:

- Korean input -> `.ko.md`
- Otherwise -> `.md`

## Instruction File Selection Rules

After language resolution, select exactly one instruction file:

- Korean -> `references/git-commit-instructions.ko.md`
- English -> `references/git-commit-instructions.md`

If the selected file is missing, unreadable, or multiple matching files exist, stop and ask the user for resolution before committing.

## Safety Checks

- If commit scope is empty, stop and report "No changes to commit."
- If detected scope includes unrelated changes, stop and ask for scope confirmation.
- If commit message cannot satisfy instruction constraints, revise message before commit.
- Never invent change intent not supported by the staged diff.

## Procedure

1. Confirm requested mode and determine commit scope.
2. Resolve instruction language using the priority rules.
3. Load exactly one matching instruction file.
4. Read staged context (`git diff --cached --name-status` and `git diff --cached --stat`).
5. Draft commit message that matches instruction constraints and actual diff.
6. Run `git commit` for the prepared scope.
7. Share commit result and final scope summary.

## References

- `references/git-commit-instructions.ko.md`
- `references/git-commit-instructions.md`
