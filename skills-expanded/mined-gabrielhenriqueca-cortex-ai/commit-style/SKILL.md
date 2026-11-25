# Commit Style Skill

This skill enforces Conventional Commits with high-quality commit messages and anti-pattern detection.

## Conventional Commits Format

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types

| Type | When to use |
|---|---|
| `feat` | New feature for the user |
| `fix` | Bug fix for the user |
| `refactor` | Code change that is neither a fix nor a feature |
| `perf` | Performance improvement |
| `test` | Adding or correcting tests |
| `docs` | Documentation changes only |
| `chore` | Build process, tooling, dependency updates |
| `ci` | CI/CD configuration changes |
| `revert` | Revert a previous commit |

### Rules

1. Subject line ≤ 72 characters
2. Imperative mood in subject: "add feature" not "added feature" or "adds feature"
3. No period at the end of subject line
4. Scope is optional but recommended: the module, component, or layer changed
5. Body explains **why**, not **what** — the diff shows what
6. Breaking changes: add `!` after type/scope AND `BREAKING CHANGE:` footer

## Good vs Bad Examples

### Good commits

```
feat(auth): add OAuth2 PKCE flow for mobile clients

PKCE is required for public clients that cannot store a client secret.
The previous implicit flow was deprecated in RFC 8252.

Closes #142
```

```
fix(pipeline): handle null values in user_id join key

Spark's default inner join silently drops rows with null keys.
Changed to LEFT JOIN with explicit null filter and quarantine step.
```

```
refactor(orders): extract tax calculation to dedicated service

Tax logic was duplicated in 3 places and had diverged. Now a single
TaxCalculationService is the source of truth.
```

```
perf(query): add composite index on (tenant_id, created_at)

Query planner was doing a full scan on the events table (12M rows).
EXPLAIN ANALYZE confirmed this index reduces the scan to 1.2k rows.
```

### Bad commits (and why)

```
# BAD — no type, no scope, vague
fix stuff

# BAD — describes what, not why
add index to events table

# BAD — past tense
added OAuth flow

# BAD — too long, non-imperative, no type
I updated the authentication module to support the new OAuth2 PKCE flow as required by mobile clients

# BAD — redundant comment in commit body
# Changed tax calculation
tax_amount = price * rate  # calculate tax
```

## Detecting Bad Commit Patterns

Flag these when reviewing commit history or helping write commits:

- Commits that mention specific line numbers ("fix line 42")
- Commits that reference internal variable names ("rename `tmp` to `data`")
- Commits with "WIP", "temp", "fix", "update", "changes" as the entire message
- Commits that mix multiple unrelated changes
- Commits that include debug code, commented-out code, or `print()` statements

## Breaking Change Example

```
feat(api)!: remove /v1/users/search endpoint

BREAKING CHANGE: /v1/users/search is removed. Use /v2/users?q= instead.
The v1 endpoint was deprecated in 0.8.0 and is incompatible with the
new search infrastructure.

Migration guide: docs/migrations/v1-v2-search.md
```
