---
name: codex-code-review
description: Use Codex CLI for AI-powered code review. Triggers on "codex review", "review with codex", "code review pr", or when user wants AI code review before PR/merge.
version: 1.0.0
---

# Codex Code Review

Leverage OpenAI's Codex CLI for comprehensive, AI-powered code review that catches bugs, security issues, and code quality problems.

## Prerequisites

- Codex CLI installed (`npm install -g @openai/codex`)
- OpenAI API key configured (`OPENAI_API_KEY` environment variable)
- Git repository with changes to review

## Quick Commands

### Interactive CLI Review

```bash
# Start Codex CLI
codex

# Then type /review to access review presets
```

### Review Modes

| Mode | Use When |
|------|----------|
| **Branch comparison** | Before opening a PR, to catch issues early |
| **Uncommitted changes** | Before committing, to review staged/unstaged files |
| **Commit review** | To analyze a specific commit's changes |
| **Custom instructions** | To focus on specific concerns (security, accessibility, etc.) |

## Workflow: Local Code Review

### Step 1: Review Before Commit

```bash
# Start interactive session
codex

# Review uncommitted changes
/review
# Select: "Review uncommitted changes"
```

### Step 2: Review Before PR

```bash
codex

# Review against base branch
/review
# Select: "Review against a base branch"
# Choose your target branch (e.g., main)
```

### Step 3: Focused Review

```bash
codex

/review
# Select: "Custom review instructions"
# Enter: "Focus on security vulnerabilities and SQL injection"
```

## Workflow: GitHub Integration

### Setup (One-time)

1. Configure Codex cloud at https://codex.openai.com
2. Navigate to Settings → Repositories
3. Enable "Code review" for your repository
4. (Optional) Enable "Automatic reviews" for all new PRs

### Manual PR Review

Comment on any pull request:
```
@codex review
```

Codex will react with 👀 and post a standard GitHub code review.

### Focused PR Review

```
@codex review for security regressions
@codex review focusing on performance implications
@codex review checking error handling
```

### AGENTS.md Configuration

Create `AGENTS.md` in your repository root:

```markdown
# Review Guidelines

## Security
- Check for SQL injection vulnerabilities
- Verify input sanitization
- Review authentication/authorization logic

## Code Quality
- Ensure functions have single responsibility
- Check for proper error handling
- Verify test coverage for new code

## Performance
- Review database queries for N+1 issues
- Check for unnecessary re-renders in React components
```

## Workflow: CI/CD Integration

### GitHub Action

```yaml
name: Codex Code Review
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: openai/codex-action@v1
        with:
          prompt-file: .github/codex-review-prompt.md
          sandbox: read-only
          safety-strategy: drop-sudo
          output-file: review-findings.json
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}

      - name: Post Review Comments
        uses: actions/github-script@v7
        with:
          script: |
            const findings = require('./review-findings.json');
            // Post inline comments based on findings
```

### Review Prompt Template

Create `.github/codex-review-prompt.md`:

```markdown
Review this pull request for:
1. Security vulnerabilities (OWASP Top 10)
2. Logic errors and edge cases
3. Performance issues
4. Code maintainability
5. Test coverage gaps

Focus on issues that impact correctness, performance, security,
maintainability, or developer experience.

Provide exact file paths and line numbers for all findings.
Rate confidence for each finding (high/medium/low).
```

## Examples

### Example: Quick Pre-commit Review

**Input:**
```
Review my changes before I commit
```

**Output:**
```bash
# Start Codex and run review
codex
/review
# Select: "Review uncommitted changes"

# Codex analyzes staged/unstaged files and reports:
# - P0: SQL injection risk in user_service.py:45
# - P1: Missing null check in api/handlers.py:123
# - P2: Consider extracting duplicate logic in utils.py
```

### Example: Security-focused PR Review

**Input:**
```
Do a security review of PR #42
```

**Output:**
```
# Comment on GitHub PR:
@codex review for security vulnerabilities

# Codex responds with GitHub code review:
# 🔴 P0: Unsanitized user input passed to shell command (cmd.py:78)
# 🟠 P1: JWT token stored in localStorage (auth.js:34)
# 🟡 P2: Missing rate limiting on login endpoint (routes.py:56)
```

### Example: CI/CD Integration Setup

**Input:**
```
Set up automatic code review in GitHub Actions
```

**Output:**
1. Create `.github/workflows/codex-review.yml` with `openai/codex-action@v1`
2. Add `OPENAI_API_KEY` to repository secrets
3. Create `.github/codex-review-prompt.md` with review criteria
4. PRs now get automatic Codex reviews on open/sync

### Example: Custom Review Focus

**Input:**
```
Review this code focusing on React performance
```

**Output:**
```bash
codex
/review
# Select: "Custom review instructions"
# Enter: "Focus on React performance: unnecessary re-renders, missing memo/useMemo/useCallback, large bundle imports"

# Codex reports:
# - P1: Component re-renders on every parent update, wrap with React.memo
# - P1: Expensive computation in render, move to useMemo
# - P2: Importing entire lodash, use lodash-es with tree shaking
```

## Tips

### Tip 1: Combine Review Modes

Run multiple review types for comprehensive coverage:
```bash
# First: check uncommitted changes
/review → "Review uncommitted changes"

# Then: compare against main for full PR scope
/review → "Review against a base branch" → main
```

### Tip 2: Create Project-specific AGENTS.md

Tailor reviews to your stack:
```markdown
# Review Guidelines

## Our Stack: Next.js + Prisma + tRPC
- Check for missing Prisma transaction wrapping
- Verify tRPC input validation with Zod
- Review Next.js data fetching patterns (SSR vs CSR)
- Flag any `any` types in TypeScript
```

### Tip 3: Use Structured Output for Metrics

Track code quality over time:
```bash
codex exec --output-schema review-schema.json "Review src/" > findings.json
# Parse findings.json to track P0/P1 counts per sprint
```

### Tip 4: Review Before and After Refactoring

```bash
# Before refactor: baseline
git stash
codex → /review → "Review against main"
# Note: 3 P1 issues

# After refactor: verify improvement
git stash pop
codex → /review → "Review against main"
# Confirm: 0 P1 issues, no new problems introduced
```

### Tip 5: Exclude Generated Files

Add to AGENTS.md to reduce noise:
```markdown
## Exclusions
- Ignore files matching: *.generated.ts, *.min.js, dist/*, coverage/*
- Skip lock files: package-lock.json, yarn.lock, pnpm-lock.yaml
```

## Best Practices

### 1. Use Appropriate Review Mode

| Situation | Recommended Mode |
|-----------|-----------------|
| Pre-commit check | Uncommitted changes |
| Pre-PR validation | Branch comparison |
| Post-merge audit | Commit review |
| Security audit | Custom with security focus |

### 2. Configure Severity Levels

Default GitHub integration shows only P0 (critical) and P1 (high) issues. Adjust in AGENTS.md:

```markdown
# Review Guidelines

## Severity Configuration
- Show P0, P1, and P2 issues
- Ignore style-only findings
```

### 3. Combine with Claude Code

For optimal workflow:
1. **Claude Code**: Fast implementation and iteration
2. **Codex**: Thorough code review before merge

```bash
# Implement with Claude
claude "Add user authentication feature"

# Review with Codex before PR
codex
/review
```

### 4. Model Selection

For critical reviews, use the strongest model:

```bash
# In codex config (~/.codex/config.json)
{
  "review_model": "gpt-5.2-codex"
}
```

## Structured Output Schema

For CI/CD integration with inline comments:

```json
{
  "type": "object",
  "properties": {
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "title": { "type": "string" },
          "body": { "type": "string" },
          "confidence": { "type": "number" },
          "priority": { "enum": ["P0", "P1", "P2", "P3"] },
          "file": { "type": "string" },
          "start_line": { "type": "integer" },
          "end_line": { "type": "integer" }
        }
      }
    },
    "verdict": {
      "type": "object",
      "properties": {
        "status": { "enum": ["approved", "changes_requested"] },
        "explanation": { "type": "string" },
        "confidence": { "type": "number" }
      }
    }
  }
}
```

## Troubleshooting

### "Review model not available"

Ensure your API key has access to the review model:
```bash
export OPENAI_API_KEY="sk-..."
codex models list
```

### GitHub Integration Not Working

1. Verify Codex cloud is configured
2. Check repository has code review enabled
3. Ensure `@codex` has repository access

### Review Too Noisy

1. Increase severity threshold in AGENTS.md
2. Add exclusion patterns for generated files
3. Use focused review instructions

## References

- [Codex CLI Features](https://developers.openai.com/codex/cli/features/)
- [Codex GitHub Integration](https://developers.openai.com/codex/integrations/github/)
- [Codex GitHub Action](https://developers.openai.com/codex/github-action/)
- [Build Code Review with Codex SDK](https://cookbook.openai.com/examples/codex/build_code_review_with_codex_sdk)
