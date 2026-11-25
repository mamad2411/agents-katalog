---
name: create-commit-message
description: "Produce a single ready-to-paste conventional commit message with a `<type>: ` prefix from current git changes, invoke only when explicitly asked to write/draft/create a commit message."
---

# Commit message

## Steps

1. Read staged changes: `git diff --cached`
2. Read unstaged changes: `git diff`
3. Read recent commits for style match: `git log --oneline -10`
4. If both diffs are empty, stop and say "nothing to commit".
5. Read the current branch name (`git branch --show-current`). If it contains an issue/ticket id, reference it per the repo convention visible in `git log`.

## Output format

```
<type>(<optional scope>): <short summary in imperative mood, max 72 chars>

<optional body: what changed and why, wrapped at 72 chars, splitted as bullet items>
```

Where `<type>` is one of: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
If the branch name contains an issue id (e.g. `123` in `feat/123-add-login`), include it the way recent commits in `git log` do (e.g. `(#123)` suffix); omit it otherwise.

## Rules

- Be concise: focus on the "why", not the "what" (the diff shows the what)
- Use imperative mood: "add feature" not "added feature"
- If changes span multiple concerns, suggest splitting into separate commits
- Output only the message, ready to copy-paste
- Message should be for one commit only. **Do not split into more than one commit**
- If quotes are to be used, **use single quotes always**
