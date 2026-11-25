---
name: commit
description: >
  Generates a conventional commit (feat/fix/refactor/docs/chore) with a clear, lowercase message based on staged or unstaged changes.
argument-hint: "[optional: commit scope or message hint]"
model: haiku
effort: low
user-invocable: true
---

## Instructions

1. Run `git diff --staged` to see staged changes. If nothing is staged, run `git diff` to see unstaged changes and stage them with `git add` (specific files, not `-A`).
2. Analyze the diff and determine the commit type:
   - `feat:` — new feature or functionality
   - `fix:` — bug fix or correction
   - `refactor:` — code restructuring without behavior change
   - `docs:` — documentation only
   - `chore:` — tooling, deps, config changes
3. Write a concise, lowercase conventional commit message (no period at end). Focus on the "what" in a single line.
4. Commit using:

```
git commit -m "$(cat <<'EOF'
type: message here

EOF
)"
```

5. Do NOT push unless explicitly asked.
6. Show the commit hash and message after committing.

## Style Rules

- Always lowercase after the type prefix
- No trailing period
- Keep under 72 characters
- Single line — no multi-line body unless the change is complex
- Examples from this repo:
  - `fix: simplify user authentication fallback rendering and improve loading skeleton styles`
  - `feat: add motion-plus dependency and remove setup script for auth token injection`
  - `refactor: remove unused SignIn import from DemoState component`
