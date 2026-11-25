---
name: commit-jp
description: Create an appropriate git commit from the working tree and session history. Default commit messages are in Japanese unless the repo says otherwise (e.g. AGENTS.md).
metadata:
  author: noblejasper
  version: "1.0.0"
compatibility:
  - codex
  - cursor
---

# Commit

## Purpose

- Produce a commit that reflects the real code changes and session context.
- Follow common git conventions (type prefix, short subject, wrapped body).
- Include both a summary and rationale in the body.
- **Write commit messages in Japanese** by default (if AGENTS.md or similar specifies another language, follow that; Japanese is the default).

## When to Use

- "commitして" (or similar), or when the user asks to commit, prepare a commit message, or finalize staged work.

## Do Not Use When

The user wants push or PR creation as well (use a push skill instead).

## Inputs

- Session history (to infer intent and rationale).
- Actual changes via `git status`, `git diff`, and `git diff --staged`.
- Repository-specific commit rules (see AGENTS.md if present).

## Procedure

1. Read session history and clarify scope, intent, and rationale.
2. Inspect the working tree and staged changes (`git status`, `git diff`, `git diff --staged`).
3. After confirming scope, stage the intended changes (`git add -A`).
4. Validate newly added files. If build artifacts, logs, temp files, or other junk would be committed, confirm with the user before committing.
5. If staging is incomplete or unrelated files are included, fix the index or ask.
6. Choose an appropriate Conventional Commits type and scope for the change (e.g. `feat(scope): ...`, `fix(scope): ...`, `refactor(scope): ...`).
7. **Subject line in Japanese**: imperative mood, ≤72 characters, no trailing period.
8. Body must include:
   - **概要**: what changed (bullets).
   - **理由**: why it changed, tradeoffs (bullets).
   - **テスト**: commands you ran, or `未実行（理由）` with a reason.
9. In Codex, append `Co-authored-by: Codex <codex@openai.com>` as a trailer unless the user says otherwise.
10. Wrap body lines at 72 characters.
11. Write the message with a here-doc or temp file and use `git commit -F <file>` (avoid `-m` with embedded `\n`).
12. Commit only when the message matches the staged changes; otherwise fix the index or message first.

## Output

- One `git commit` that reflects the session and staged diff.

## Template

Types and scopes are examples—adjust to the repo and the change.

```
<type>(<scope>): <short Japanese summary>

概要:
- <what changed>
- <what changed>

理由:
- <why it changed>
- <why it changed>

テスト:
- <commands run> or "未実行（理由）"
```

The section headings **概要**, **理由**, and **テスト** and their bullets are written in Japanese in the final commit message body.
