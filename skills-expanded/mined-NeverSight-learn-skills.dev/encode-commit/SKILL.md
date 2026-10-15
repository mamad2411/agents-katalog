---
name: encode-commit
description: >
  Ultra-compressed commit message generator. Cuts noise from commit messages while preserving intent and reasoning. Conventional Commits format. Subject ≤50 chars, body only when "why" isn't obvious. Triggers: "/encode-commit". Auto-triggers when staging changes.
---

Write commit messages terse and exact. Conventional Commits format. No fluff. Why over what.

## Rules

**Subject line:**
- `<type>(<scope>): <imperative summary>` — `<scope>` optional
- Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `chore`, `build`, `ci`, `style`, `revert`
- Imperative mood: "add", "fix", "remove" — not "added", "adds", "adding"
- ≤50 chars when possible, hard cap 72; no trailing period

**Body (only if needed):**
- Skip when subject is self-explanatory
- Always include for: non-obvious *why*, breaking changes, migrations, reverts, security fixes — never compress these to subject-only

**What NEVER goes in:**
- "I", "we", "now", "currently" — the diff says what
- AI attribution ("Generated with Claude Code") or emoji
- Encoding symbols (`→ ∴ ∀ ⊥ ∃ §`) — write the English word instead
- Plan/spec identifiers (`F1`, `T77`, `V77`, `R28`) — expand into what it stood for: PLAN.md is blanked each cycle and SPEC.md rows get pruned, so only the commit message survives to explain the change

## Example

Diff: new endpoint for user profile with body explaining the why
- bad: "feat: add a new endpoint to get user profile information from the database"
- good:
  ```
  feat(api): add GET /users/:id/profile

  Mobile client needs profile data without the full user payload
  to reduce LTE bandwidth on cold-launch screens.

  Closes #128
  ```

## Boundaries

Only generates the commit message. Does not run `git commit`, stage files, or amend. "stop encode-commit" or "normal mode": revert to verbose style.
