---
name: conventional-commits
description: Generates correct conventional commit messages from a diff, file list, or change description. Use when the user says "write a commit message", "generate a commit", "what should I name this commit", "help me commit this", or pastes a git diff or list of changed files. Also apply when the user asks to squash, split, or rewrite existing commit messages.
---

# Conventional Commits

Generates commit messages that follow the Conventional Commits standard.
Analyzes the change, picks the right type and scope, writes a clear
description, and adds a body or footer only when necessary.

---

## Required Details

Collect or infer before writing. Ask if missing.

| Detail | Example |
|---|---|
| **What changed** | Diff, file list, or plain description |
| **Why (if not obvious)** | Bug fix, new feature, refactor |
| **Breaking change?** | Yes / No |
| **Issue reference?** | `#123`, `PROJ-456`, or none |

---

## Instructions

### Step 1 — Pick the type

| Type | When to use |
|---|---|
| `feat` | New feature or behavior visible to the user |
| `fix` | Bug fix |
| `refactor` | Code change with no behavior change |
| `perf` | Performance improvement |
| `test` | Adding or fixing tests |
| `docs` | Documentation only |
| `style` | Formatting, whitespace — no logic change |
| `chore` | Build, deps, config, tooling |
| `ci` | CI/CD pipeline changes |
| `revert` | Reverts a previous commit |

### Step 2 — Pick the scope (optional but recommended)

Scope = the area of the codebase affected. Keep it short and lowercase.

```
feat(auth): ...
fix(api): ...
refactor(db): ...
chore(deps): ...
```

Use no scope only if the change is truly cross-cutting.

### Step 3 — Write the subject line

Format: `type(scope): description`

Rules:
- Lowercase after the colon
- No period at the end
- Max 72 characters
- Imperative mood: "add", "fix", "remove" — not "added", "fixes", "removed"

```
✅ feat(auth): add Google OAuth2 login
✅ fix(api): handle null user in /me endpoint
✅ chore(deps): upgrade Next.js to 15.1.0

❌ Added Google login
❌ Fixed the bug with the user endpoint.
❌ FEAT: Add Google OAuth2 Login
```

### Step 4 — Add body only if the subject isn't enough

Add a body when:
- The **why** is not obvious from the subject
- The change involves a non-trivial approach worth explaining
- Multiple unrelated things changed (consider splitting instead)

```
refactor(db): replace raw SQL with Drizzle ORM

Replaces manual pg queries with Drizzle for type safety and
easier migrations. No behavior change — all queries produce
identical results.
```

### Step 5 — Add footer for breaking changes or issue refs

```
feat(api): change user ID format from integer to UUID

BREAKING CHANGE: user IDs are now UUIDs. Clients must update
any hardcoded integer ID assumptions.

Closes #234
```

---

## Non-Negotiable Acceptance Criteria

Do not deliver the commit message unless ALL of these are true:

- [ ] Type is one of the allowed values — no custom types
- [ ] Subject line is lowercase after the colon
- [ ] Subject line has no trailing period
- [ ] Subject line is under 72 characters
- [ ] Imperative mood: "add" not "added", "fix" not "fixed"
- [ ] Breaking changes are in the footer with `BREAKING CHANGE:` prefix
- [ ] Body and footer are separated from subject by a blank line

---

## Output Format

~~~
## Commit Message

```
[subject line]

[body — only if needed]

[footer — only if breaking change or issue ref]
```

## Notes
- [if the change should be split into multiple commits, say so here]
- [if scope was inferred, mention it]
~~~