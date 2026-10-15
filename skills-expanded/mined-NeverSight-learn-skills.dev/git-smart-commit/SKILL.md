---
name: git-smart-commit
description: "Analyze git changes and generate semantic, meaningful commit messages"
trigger: ["commit", "git commit", "commit message", "semantic commit", "conventional commit"]
---

# Git Smart Commit Skill

This skill analyzes your git changes and generates meaningful, semantic commit messages following Conventional Commits specification.

## Objective

Analyze staged and unstaged changes in a git repository, understand the intent and impact of the changes, and generate clear, semantic commit messages that follow best practices.

## Execution Steps

### 1. Check Git Repository Status

```bash
# Check if we're in a git repository
git rev-parse --is-inside-work-tree

# Get status of changes
git status --short

# View detailed diff of changes
git diff HEAD
```

**Understand:**
- Are there staged changes? Unstaged changes?
- How many files are affected?
- What types of changes (new files, modifications, deletions)?

### 2. Analyze the Changes

Read the actual diff to understand what changed:

```bash
# See staged changes
git diff --cached

# See all changes (staged + unstaged)
git diff HEAD

# Show file names and change statistics
git diff --stat HEAD
```

**Categorize changes by:**
- **Type:** feat, fix, docs, style, refactor, test, chore, perf, ci, build
- **Scope:** Component, module, or feature affected
- **Breaking changes:** API changes, removed features
- **Impact:** User-facing vs internal changes

### 3. Determine Commit Type

Use Conventional Commits specification:

| Type | When to Use | Examples |
|------|-------------|----------|
| **feat** | New feature for users | Add user profile page, Add dark mode |
| **fix** | Bug fix | Fix login error, Resolve memory leak |
| **docs** | Documentation only | Update README, Add API docs |
| **style** | Formatting, whitespace | Format code, Fix indentation |
| **refactor** | Code restructuring | Extract helper function, Simplify logic |
| **test** | Adding or fixing tests | Add unit tests, Fix flaky E2E test |
| **chore** | Maintenance tasks | Update dependencies, Configure build |
| **perf** | Performance improvement | Optimize query, Reduce bundle size |
| **ci** | CI/CD changes | Update GitHub Actions, Add deploy step |
| **build** | Build system changes | Update webpack config, Add Vite plugin |
| **revert** | Reverting previous commit | Revert "Add feature X" |

### 4. Identify Scope

The scope provides context about what part of the codebase changed:

**Examples:**
- `feat(auth):` Changes to authentication
- `fix(api):` Bug fix in API layer
- `docs(readme):` README updates
- `style(header):` Header component styling
- `refactor(utils):` Utility function refactoring

**Scope guidelines:**
- Keep it short (1-2 words)
- Be specific but not overly detailed
- Use consistent names (refer to existing commits)
- Optional for small projects

### 5. Craft the Commit Message

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Subject line (required):**
- Limit to 50-72 characters
- Use imperative mood ("Add feature" not "Added feature")
- Don't end with a period
- Capitalize first letter
- Be specific and descriptive

**Body (optional but recommended):**
- Explain the "why" and "what", not "how"
- Wrap at 72 characters
- Separate from subject with blank line
- Can include multiple paragraphs

**Footer (optional):**
- Breaking changes: `BREAKING CHANGE: description`
- Issue references: `Fixes #123`, `Closes #456`
- Co-authors: `Co-authored-by: Name <email>`

### 6. Examples of Good Commit Messages

#### Simple Feature
```
feat(auth): add password reset functionality

Users can now reset their password via email. Added reset token
generation, email sending, and password update endpoints.

Closes #234
```

#### Bug Fix
```
fix(cart): prevent duplicate items being added

Fixed race condition where rapid clicks on "Add to Cart" button
would create duplicate items. Added debouncing and loading state.

Fixes #456
```

#### Breaking Change
```
feat(api)!: migrate to v2 authentication

BREAKING CHANGE: Auth endpoints now require API key in header
instead of query parameter. Update all clients to use
Authorization: Bearer <token> header.

Migration guide: docs/migration-v2.md
```

#### Refactor
```
refactor(utils): extract date formatting logic

Moved date formatting functions to separate utils file to
improve reusability and testability. No functional changes.
```

#### Documentation
```
docs(contributing): add code review guidelines

Added section on code review best practices and expectations
for reviewers and authors.
```

#### Chore
```
chore(deps): update dependencies to latest versions

Updated React to 18.3, TypeScript to 5.3, and Vite to 5.0.
All tests passing.
```

### 7. Stage Changes (if needed)

If there are unstaged changes:

```bash
# Stage all changes
git add .

# Stage specific files
git add src/components/Login.tsx src/utils/auth.ts

# Stage interactively (choose what to include)
git add -p
```

**Best practice:** Keep commits focused on a single logical change

### 8. Create the Commit

```bash
# Create commit with generated message
git commit -m "feat(auth): add password reset functionality" \
           -m "Users can now reset their password via email. Added reset token
generation, email sending, and password update endpoints." \
           -m "Closes #234"

# Or use editor for multi-line message
git commit
# Opens editor with message template
```

### 9. Verify Commit

```bash
# View the commit you just created
git log -1 --pretty=full

# See the diff in the commit
git show HEAD
```

### 10. Report Summary

```
✅ Commit Created

Type: feat
Scope: auth
Subject: add password reset functionality

Files changed: 4
- src/api/auth.ts (new endpoints)
- src/components/PasswordReset.tsx (new component)
- src/utils/email.ts (email sending)
- tests/auth.test.ts (new tests)

Commit SHA: abc1234
Message:
---
feat(auth): add password reset functionality

Users can now reset their password via email. Added reset token
generation, email sending, and password update endpoints.

Closes #234
---
```

## Commit Message Best Practices

### DO:
- ✅ Use present tense imperative ("Add feature" not "Added feature")
- ✅ Be specific ("Fix login error on mobile" not "Fix bug")
- ✅ Reference issues/tickets
- ✅ Explain the "why" in the body
- ✅ Keep subject line under 72 characters
- ✅ Use conventional commit types
- ✅ Include breaking change notices

### DON'T:
- ❌ Generic messages ("Fix stuff", "Update code", "WIP")
- ❌ Commit unrelated changes together
- ❌ Use past tense ("Added", "Fixed")
- ❌ End subject with period
- ❌ Include file names in subject (visible in diff)
- ❌ Commit without understanding what changed

## Handling Different Scenarios

### Multiple Unrelated Changes
**Don't:** Commit everything together
```
git commit -m "Fix login, update README, refactor utils"
```

**Do:** Create separate commits
```bash
git add src/auth/Login.tsx
git commit -m "fix(auth): resolve login error on mobile"

git add README.md
git commit -m "docs: update installation instructions"

git add src/utils/
git commit -m "refactor(utils): extract common helpers"
```

### Work in Progress
```bash
# If you must commit incomplete work
git commit -m "wip: partial implementation of user search"

# Later, before pushing, squash or amend
git commit --amend  # Edit last commit
git rebase -i HEAD~3  # Interactive rebase to squash
```

### Emergency Hotfix
```
fix(api)!: patch critical security vulnerability

SECURITY: Fixed SQL injection vulnerability in user search endpoint.
All installations should update immediately.

CVE-2024-12345
```

### Merge Commits
```
# Let git generate merge commit message, or customize:
Merge branch 'feature/user-profile' into main

Brings in user profile functionality including avatar upload,
bio editing, and profile visibility settings.

Closes #123, #124, #125
```

## Conventional Commit Type Reference

```
feat:     New feature
fix:      Bug fix
docs:     Documentation changes
style:    Code style (formatting, semicolons, etc.)
refactor: Code refactoring (no feature change)
perf:     Performance improvement
test:     Adding/updating tests
build:    Build system changes
ci:       CI/CD changes
chore:    Maintenance, dependencies, tooling
revert:   Revert previous commit
```

**With breaking changes:** Add `!` after type/scope: `feat!:` or `feat(api)!:`

## Tools & Integrations

### Commitizen
For interactive commit message generation:
```bash
npm install -g commitizen
cz  # Instead of git commit
```

### Commitlint
To enforce commit message format:
```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# .commitlintrc.json
{
  "extends": ["@commitlint/config-conventional"]
}
```

### Husky
To validate commits before they're created:
```bash
npm install --save-dev husky
npx husky add .husky/commit-msg 'npx commitlint --edit $1'
```

## Success Criteria

- Commit message follows Conventional Commits format
- Subject line is clear and descriptive (< 72 chars)
- Commit includes only related changes
- Breaking changes are clearly marked
- Relevant issues are referenced
- Body explains the "why" when necessary
- Message would be helpful in 6 months

## Common Pitfalls

❌ **Too vague:** "Update files"
✅ **Specific:** "feat(ui): add responsive navigation menu"

❌ **Too detailed:** "Fix bug in handleUserLogin function line 45 where useState wasn't updating properly"
✅ **Right level:** "fix(auth): resolve state update issue in login handler"

❌ **Past tense:** "Added new feature"
✅ **Imperative:** "Add new feature"

❌ **Multiple unrelated changes:** "Fix bug, add feature, update docs"
✅ **Focused:** Create 3 separate commits

## Usage Examples

### Basic Usage
```
"Analyze my changes and create a smart commit message"
```

### After Feature Development
```
"I just finished implementing user profile editing. Generate a commit message."
```

### Bug Fix
```
"I fixed the checkout bug. Help me write a proper commit message."
```

### Before Push
```
"Review my staged changes and suggest a commit message that follows best practices"
```

## Notes

- This skill reads git diffs but doesn't commit automatically - it generates the message for review
- Always review generated messages to ensure accuracy
- Consider setting up commit message hooks to enforce standards across your team
- Good commit messages are documentation - invest time in writing them well
- Use `git log` to see team's commit patterns and maintain consistency
