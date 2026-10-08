# Cursor Rules for FloripaTalks Project

## Commit Message Generation

When generating commit messages, follow the Conventional Commits specification:

**Format**: `<type>: <subject>`

**Types**:
- `feature` (or `ft`): New feature
- `hotfix` (or `hf`): Critical bug fix in production
- `fix` (or `fx`): Bug fix
- `bugfix` (or `bf`): Bug fix (alternative to fix)
- `chore` (or `ch`): Maintenance (deps, config, etc)

**Rules**:
- Subject: Maximum 50 characters, imperative mood, lowercase
- Body: Optional, wrap at 72 chars per line, maximum 300 characters total
- Footer: Optional, for breaking changes or issue references
- Style: Imperative mood ("add feature" not "added feature")
- Language: English only
- Keep messages concise and focused

**Examples**:
- `feature: add HTMX infinite scroll`
- `ft: add HTMX infinite scroll`
- `hotfix: resolve critical database connection issue`
- `hf: resolve critical database connection issue`
- `fix: resolve static files warning`
- `fx: resolve static files warning`
- `bugfix: resolve static files warning`
- `bf: resolve static files warning`
- `chore: update Django to 6.0`
- `ch: update Django to 6.0`

**Important**:
- Total message length (including subject and body) MUST NOT exceed 300 characters
- Use the prefix format consistently
- Be specific but concise
- All commit messages MUST be in English

## Code Quality Checks

**MANDATORY**: Before finalizing any code changes, ALWAYS run quality checks to catch errors early:

1. **Run linting and formatting checks**: Use `just check` or `just check-fix` to run all pre-commit checks
2. **Verify E402 compliance**: All module-level imports MUST be at the top of the file (E402 rule)
3. **Run tests**: Ensure all tests pass before considering code complete
4. **Check pre-commit hooks**: Run `just pre-commit-staged` to verify all hooks pass

**Process**:
- After writing code, ALWAYS run `just check` to verify linting and formatting
- If errors are found, run `just check-fix` to auto-fix issues, then verify with `just check` again
- Only consider code complete when all checks pass

**Rationale**: Catching errors during development prevents failed pre-commit hooks and ensures code quality standards are met before commits.
