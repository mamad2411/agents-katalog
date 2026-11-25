---
name: code-review
description: Review code for correctness, style, and maintainability. Use when the user asks for a code review, PR review, or feedback on changes.
---

# Code Review

When the user asks for a code review, follow this process.

## Checklist

- [ ] **Correctness** — Logic is sound and edge cases are handled.
- [ ] **Security** — No obvious issues (e.g. injection, hardcoded secrets, missing validation).
- [ ] **Style** — Matches project conventions and is readable.
- [ ] **Structure** — Functions/classes are focused; duplication is minimized.
- [ ] **Tests** — Changes that affect behavior have or deserve tests.

## Output format

Group feedback by severity:

- **Critical** — Must fix before merge (bugs, security).
- **Suggestion** — Should consider (readability, performance, patterns).
- **Nice to have** — Optional improvements.

Keep feedback actionable: point to files/lines and suggest concrete changes where helpful.

## Scope

- If the user points to specific files or a diff, focus there.
- If they say "review my changes", use git (e.g. `git diff`) to determine scope when appropriate.
