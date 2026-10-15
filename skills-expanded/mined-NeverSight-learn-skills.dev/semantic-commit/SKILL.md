---
name: semantic-commit
description: Create a git commit using the Conventional Commits specification (v1.0.0).
---

# Semantic Commit

## Trigger

When the user says "commit", "semantic commit", "conventional commit", or `/semantic-commit`.

## Instructions

You are a commit message specialist following the [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

### Step 1: Analyze Changes

Run these commands in parallel to understand the current state:

```bash
git status
git diff --staged
git diff
git log --oneline -5
```

If nothing is staged, ask the user which files to stage, or suggest staging all modified files.

### Step 2: Compose the Commit Message

Follow this format strictly:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

#### Types

| Type       | When to use                                      |
|------------|--------------------------------------------------|
| `feat`     | A new feature (SemVer MINOR)                     |
| `fix`      | A bug fix (SemVer PATCH)                         |
| `docs`     | Documentation only changes                       |
| `style`    | Formatting, missing semicolons, etc. (no logic)  |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf`     | Performance improvement                          |
| `test`     | Adding or correcting tests                       |
| `build`    | Build system or external dependency changes      |
| `ci`       | CI configuration changes                         |
| `chore`    | Other changes that don't modify src or test files|
| `revert`   | Reverts a previous commit                        |

#### Rules

- **type** is mandatory and lowercase.
- **scope** is optional, a noun in parentheses describing the affected area: `feat(auth): ...`
- **description** starts lowercase, no period at the end, imperative mood ("add" not "added").
- **body** is optional, separated by a blank line. Explain *what* and *why*, not *how*.
- **BREAKING CHANGE**: Indicate with `!` after type/scope OR as a footer `BREAKING CHANGE: ...`. Correlates with SemVer MAJOR.
- **footer** format: `Token: value` or `Token #value`. Use `Refs`, `Closes`, `BREAKING CHANGE`, etc.

### Step 3: Confirm and Commit

1. Present the proposed commit message to the user.
2. Wait for user approval or edits.
3. Stage files if needed, then commit using a HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
<commit message here>

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

4. Run `git status` after committing to verify success.

### Examples

```
feat(api): add user registration endpoint

Implement POST /api/users with email validation and password hashing.

Closes #42
```

```
fix(parser): handle empty input gracefully

Previously the parser would throw on empty strings.
Now it returns an empty result object.
```

```
refactor!: drop support for Node 14

BREAKING CHANGE: minimum Node version is now 18.
```

```
docs: update README with deployment instructions
```

```
chore(deps): bump axios from 0.21 to 1.6
```
