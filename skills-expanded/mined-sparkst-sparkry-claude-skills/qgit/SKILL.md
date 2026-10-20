---
name: QGIT - Git Release Management
description: Run quality gates (lint, typecheck, test), stage changes, generate Conventional Commit message, commit, and push to remote
version: 1.0.0
agents: [release-manager]
tools: [quality-gate-checker.py]
references: [conventional-commits.md, quality-gates.md]
claude_tools: Read, Grep, Glob, Bash
trigger: QGIT
---

# QGIT Skill

## Purpose

Automated git release management with quality gate enforcement:
1. Run pre-commit quality gates (lint, typecheck, test)
2. Stage changes
3. Generate Conventional Commit message
4. Commit with co-author attribution
5. Push to remote repository

**Use QGIT when**:
- Ready to commit and push changes
- Want to ensure quality gates pass before commit
- Need a well-formatted Conventional Commit message

**Do NOT use QGIT for**:
- Destructive git operations (force push, hard reset)
- Skipping quality gates (use manual git commands if necessary)

---

## Workflow

### Phase 1: Quality Gate Checks

**Agent**: release-manager

**Actions**:
1. Run `npm run lint` (ESLint, Prettier)
2. Run `npm run typecheck` (TypeScript)
3. Run `npm run test` (All tests)
4. Run edge function dependency checks (if applicable)
5. Run custom quality gates from `.qgit.json` (if configured)

**Tools**: Bash, quality-gate-checker.py

**Blockers**: Any failing gate blocks the commit

**Output**: Quality gate report

---

### Phase 2: Change Analysis

**Agent**: release-manager

**Actions**:
1. Run `git status` to see untracked and modified files
2. Run `git diff` to see staged and unstaged changes
3. Run `git log -5` to see recent commit style
4. Analyze changes to determine commit type (feat, fix, refactor, etc.)

**Tools**: Bash (git commands)

**Output**: Change summary

---

### Phase 3: Commit Message Generation

**Agent**: release-manager

**Actions**:
1. Determine commit type based on changes
2. Extract scope from changed files (e.g., "auth", "api", "ui")
3. Write concise description (<50 chars)
4. Add body if needed (explain "why", not "what")
5. Add footer with REQ IDs (if applicable)
6. Add co-author attribution

**Format**: Conventional Commits (https://www.conventionalcommits.org)

**Output**: Commit message

---

### Phase 4: Stage and Commit

**Agent**: release-manager

**Actions**:
1. Stage relevant files (`git add <files>`)
2. Commit with generated message
3. Verify commit succeeded

**Tools**: Bash (git commands)

**Safety**: Never stage `.env`, `credentials.json`, or other secrets

**Output**: Commit hash

---

### Phase 5: Push

**Agent**: release-manager

**Actions**:
1. Push to remote repository (`git push`)
2. Verify push succeeded

**Tools**: Bash (git commands)

**Safety**: Never force push to main/master unless explicitly requested

**Output**: Push confirmation

---

## Input

**From User**:
- Basic: `QGIT`
- With custom message: `QGIT --message="fix(auth): resolve token expiry bug"`
- Skip specific gate: `QGIT --skip-lint` (use sparingly)
- Dry run: `QGIT --dry-run` (show what would happen, don't commit)

**From Environment**:
- Git status and diff
- Package.json scripts (lint, typecheck, test)
- `.qgit.json` configuration (if exists)
- `requirements/requirements.lock.md` (for REQ IDs)

---

## Output

### Quality Gate Report

```
Quality Gate Report
===================

✅ Lint: PASSED (0 errors, 0 warnings)
✅ Typecheck: PASSED (0 errors)
✅ Test: PASSED (42 tests, 0 failures)
✅ Edge Functions: PASSED (all dependencies @2.50.2)

All gates passed. Proceeding with commit.
```

### Commit Message

```
feat(auth): add OAuth provider support

Implement Google and GitHub OAuth providers with PKCE flow.
Includes token refresh logic and session management.

REQ-42, REQ-43

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Commit and Push Confirmation

```
Staged files:
  src/auth/oauth.ts
  src/auth/providers/google.ts
  src/auth/providers/github.ts
  src/auth/__tests__/oauth.spec.ts

Commit: a3f8c2e feat(auth): add OAuth provider support
Push: origin/main (success)
```

---

## Quality Gates

### Default Gates (MUST PASS)

1. **Lint** (`npm run lint`)
   - ESLint rules
   - Prettier formatting
   - No errors or warnings

2. **Typecheck** (`npm run typecheck`)
   - TypeScript compilation
   - No type errors

3. **Test** (`npm run test`)
   - All tests pass
   - No failing test suites

4. **Edge Functions** (if applicable)
   - Dependency version consistency
   - Function exists in `supabase/functions/`
   - Smoke test passes

### Custom Gates

Add custom gates in `.qgit.json`:

```json
{
  "quality_gates": [
    {
      "name": "Security Scan",
      "command": "npm audit --production",
      "required": true
    },
    {
      "name": "Bundle Size",
      "command": "npm run build && du -sh dist",
      "required": false
    }
  ]
}
```

---

## Conventional Commits Format

Based on: https://www.conventionalcommits.org

### Structure

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **refactor**: Code refactoring (no behavior change)
- **perf**: Performance improvement
- **test**: Add or update tests
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **chore**: Build process, dependencies, tooling
- **ci**: CI/CD configuration changes
- **revert**: Revert previous commit

### Scope

Scope is optional but recommended. Use the primary domain affected:
- `auth` - Authentication/authorization
- `api` - API endpoints
- `ui` - UI components
- `core` - Core domain logic
- `db` - Database/migrations

### Description

- Max 50 characters
- Lowercase, no period at end
- Imperative mood ("add", not "added" or "adds")

### Body

- Explain "why", not "what" (code shows "what")
- Wrap at 72 characters
- Separate from description with blank line

### Footer

- Reference REQ IDs: `REQ-42, REQ-43`
- Breaking changes: `BREAKING CHANGE: <description>`
- Close issues: `Closes #123`

### Examples

**Simple Feature**:
```
feat(auth): add password reset flow

REQ-43

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Bug Fix with Context**:
```
fix(api): resolve race condition in token refresh

Token refresh logic was not thread-safe, causing intermittent
401 errors under high concurrency. Added mutex lock.

REQ-45

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

**Breaking Change**:
```
feat(auth): migrate from sessions to JWT tokens

BREAKING CHANGE: Session storage is no longer supported.
Existing sessions will be invalidated on upgrade.

Migration guide: See docs/migration/v2.0.0.md

REQ-46

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## Configuration

### Default Settings

- **Quality Gates**: lint, typecheck, test
- **Auto-stage**: Modified and new files (excludes .env, credentials.json)
- **Auto-push**: true
- **Commit Format**: Conventional Commits
- **Co-author**: Claude Opus 4.5

### Custom Configuration

Create `.qgit.json` in project root:

```json
{
  "quality_gates": [
    {
      "name": "Lint",
      "command": "npm run lint",
      "required": true
    },
    {
      "name": "Typecheck",
      "command": "npm run typecheck",
      "required": true
    },
    {
      "name": "Test",
      "command": "npm run test",
      "required": true
    }
  ],
  "auto_stage": true,
  "auto_push": true,
  "commit_format": "conventional",
  "exclude_patterns": [".env", "*.key", "credentials.json"],
  "require_req_ids": false,
  "max_description_length": 50,
  "max_body_line_length": 72
}
```

---

## Examples

### Example 1: Simple Feature Commit

**Scenario**: Implemented OAuth authentication

**Command**:
```bash
QGIT
```

**Actions**:
1. Run quality gates ✅ All pass
2. Analyze changes: Added files in `src/auth/`
3. Generate commit message: `feat(auth): add OAuth provider support`
4. Stage files: `src/auth/oauth.ts`, `src/auth/providers/*.ts`, `src/auth/__tests__/*.spec.ts`
5. Commit: `a3f8c2e`
6. Push: `origin/main`

**Estimated Effort**: 0.05 SP (automated)

---

### Example 2: Bug Fix with Custom Message

**Scenario**: Fixed token refresh bug, want custom description

**Command**:
```bash
QGIT --message="fix(api): resolve token refresh race condition"
```

**Actions**:
1. Run quality gates ✅ All pass
2. Use provided message (validate Conventional Commits format)
3. Add body and footer automatically
4. Stage files
5. Commit
6. Push

**Estimated Effort**: 0.05 SP (automated)

---

### Example 3: Quality Gate Failure

**Scenario**: Tests are failing

**Command**:
```bash
QGIT
```

**Actions**:
1. Run quality gates ❌ Test fails
2. Display failing test output
3. Block commit
4. Recommend: Fix tests, then retry

**Output**:
```
Quality Gate Report
===================

✅ Lint: PASSED
✅ Typecheck: PASSED
❌ Test: FAILED (2 tests failed)

Failing tests:
  - src/auth/__tests__/oauth.spec.ts:42 REQ-42 — OAuth flow
  - src/auth/__tests__/oauth.spec.ts:58 REQ-43 — Token refresh

Fix failing tests before committing.
```

**Estimated Effort**: N/A (blocked)

---

### Example 4: Dry Run

**Scenario**: Want to see what QGIT would do without committing

**Command**:
```bash
QGIT --dry-run
```

**Actions**:
1. Run quality gates ✅ All pass
2. Analyze changes
3. Generate commit message
4. Display what would be staged
5. **Skip commit and push**

**Output**:
```
Dry Run Mode
============

Quality gates: ✅ All passed

Would stage:
  src/auth/oauth.ts
  src/auth/providers/google.ts
  src/auth/__tests__/oauth.spec.ts

Would commit with message:
  feat(auth): add OAuth provider support

  REQ-42, REQ-43

  Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

Would push to: origin/main

(No changes made - dry run only)
```

**Estimated Effort**: 0.05 SP (automated)

---

## Integration with Other QShortcuts

### With QCODE (Implementation)

```bash
# 1. Implement feature
QCODE

# 2. Verify implementation
npm run test

# 3. Commit and push
QGIT
```

---

### With QDOC (Documentation)

```bash
# 1. Implement feature
QCODE

# 2. Update docs
QDOC

# 3. Commit all changes (code + docs)
QGIT
```

---

### With QCHECK (Code Review)

```bash
# 1. Implement feature
QCODE

# 2. Code review
QCHECK

# 3. Fix issues from review
QCODE

# 4. Commit and push
QGIT
```

---

## Safety Features

### Git Safety Protocol

**NEVER**:
- Update git config
- Run destructive commands (force push, hard reset, clean -f, checkout .)
- Skip hooks (--no-verify, --no-gpg-sign)
- Force push to main/master
- Commit secrets (.env, credentials.json)

**ALWAYS**:
- Run quality gates before commit
- Generate Conventional Commit messages
- Add co-author attribution
- Verify push success

### Secret Detection

QGIT automatically excludes files matching these patterns:
- `.env`, `.env.*`
- `*.key`, `*.pem`, `*.p12`
- `credentials.json`
- `secrets.yaml`

To customize, add to `.qgit.json`:
```json
{
  "exclude_patterns": [".env", "*.key", "api-keys.json"]
}
```

---

## Troubleshooting

### Issue: Quality Gate Failing

**Problem**: `npm run test` fails

**Solution**: Fix failing tests
```bash
npm run test  # See specific failures
# Fix issues
npm run test  # Verify green
QGIT          # Retry commit
```

---

### Issue: Commit Message Too Long

**Problem**: Generated commit description >50 chars

**Solution**: Shorten description manually
```bash
QGIT --message="feat(auth): add OAuth support"
```

---

### Issue: Want to Skip Quality Gate

**Problem**: Need to commit despite failing lint (edge case)

**Solution**: Use manual git commands (QGIT is opinionated about quality)
```bash
git add .
git commit -m "wip: work in progress"
git push
```

**Note**: Only do this for WIP branches, never main/master.

---

### Issue: Push Rejected (Non-Fast-Forward)

**Problem**: Remote has changes not in local

**Solution**: Pull and rebase, then retry
```bash
git pull --rebase
npm run test  # Verify tests still pass
QGIT          # Retry push
```

---

## Story Point Estimation

| Action | Effort (SP) |
|--------|-------------|
| QGIT (all gates pass) | 0.05 |
| QGIT (gates fail, fix issues) | 0.1-0.5 (depends on fixes) |
| QGIT --dry-run | 0.05 |

**Baseline**: QGIT is automated and should take ~30 seconds when gates pass.

---

## Tools

### quality-gate-checker.py

Python script that runs quality gates and reports results.

**Usage**:
```bash
python tools/quality-gate-checker.py
```

**Output**: JSON with gate results
```json
{
  "lint": {"status": "pass", "errors": 0},
  "typecheck": {"status": "pass", "errors": 0},
  "test": {"status": "fail", "errors": 2, "details": "..."}
}
```

---

## References

See `references/` directory:
- `conventional-commits.md` - Conventional Commits specification and examples
- `quality-gates.md` - Quality gate configuration and troubleshooting

---

## Best Practices

### 1. Commit Frequently

**❌ Don't**: Commit once per day with 500 lines changed
✅ **Do**: Commit after each logical unit of work (1-3 REQs)

---

### 2. Write Descriptive Messages

**❌ Don't**: `fix: bug fix`
✅ **Do**: `fix(auth): resolve race condition in token refresh`

---

### 3. Keep Commits Focused

**❌ Don't**: Mix features and bug fixes in one commit
✅ **Do**: Separate commits for different change types

---

### 4. Reference REQs

**❌ Don't**: `feat: add feature`
✅ **Do**: `feat(auth): add OAuth support\n\nREQ-42, REQ-43`

---

## Contributing

For issues or enhancements to QGIT skill:
- **Email**: skills@sparkry.ai
- **License**: MIT
