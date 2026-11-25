# CI Skill

## 🌐 Language

> All output documents and user-facing messages must be written in the language specified
> by `crew-config.json → preferences.language`. If not set, default to English.

Analyzes per-repository commit/lint rules and handles workflow automation (branch separation, commits, PRs, merges).

## 🔧 Project Configuration Reference

> **If `crew-config.json` exists, reference it.**
> - `conventions.commitConvention`: Commit message rules
> - `conventions.branchStrategy`: Branch strategy
> - `tools.ci`: CI platform (github-actions, gitlab-ci, etc.)
> - `tools.linter`, `tools.formatter`: Lint/format tools

## Role

1. **Repo Analysis**: Analyze commit rules, lint configuration, CI/CD pipeline
2. **Per-repo Skill Generation**: Create repo-specific rules in the `.claude/` directory
3. **Git Workflow Automation**: Branch creation → Commit → Push → PR → Merge

## Workflow

### Phase 1: Repo Analysis and Skill Generation

When running for the first time on a repo, analyze the following:

```
1. Git Configuration Analysis
   - .gitignore
   - .gitattributes
   - Branch strategy (main/master, develop, etc.)

2. Commit Rule Analysis
   - commitlint.config.js
   - .commitlintrc
   - Recent commit message pattern analysis

3. Lint Configuration Analysis
   - ESLint (.eslintrc.*, eslint.config.js)
   - Prettier (.prettierrc.*)
   - Python (ruff, black, flake8, mypy)
   - pre-commit hooks (.pre-commit-config.yaml)

4. CI/CD Analysis
   - GitHub Actions (.github/workflows/)
   - Test commands (package.json scripts, pytest.ini)
```

### Phase 2: Repo-specific Skill Generation

Save the analysis results as `.claude/repo-rules.md`:

```markdown
# Repository Rules

## Commit Convention
- Type: feat|fix|docs|style|refactor|test|chore
- Format: type(scope): message
- Example: feat(auth): add login API

## Branch Strategy
- Main: main
- Feature: feature/{backlog-keyword}
- Bugfix: bugfix/{issue-id}

## Lint Rules
- ESLint: npm run lint
- Prettier: npm run format
- Pre-commit: npm run lint-staged

## Test Commands
- Unit: npm test
- E2E: npm run test:e2e
- Coverage: npm run test:cov

## CI Checks Required
- Lint pass
- Tests pass
- Build success
```

### Phase 3: Git Workflow Automation

#### At Backlog Start (Orchestrator Integration)
```bash
# 1. Sync to latest state on main branch
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/{backlog-keyword}

# 3. Push branch to remote (set up tracking)
git push -u origin feature/{backlog-keyword}
```

#### At Backlog Completion (Orchestrator Integration)
```bash
# 1. Stage and commit changes
git add .
git commit -m "feat({backlog-keyword}): {description}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

# 2. Push to remote
git push origin feature/{backlog-keyword}

# 3. Create PR
gh pr create --title "feat({backlog-keyword}): {description}" \
  --body "## Summary
- {Changes summary}

## Test Plan
- {Test plan}

🤖 Generated with [Claude Code](https://claude.com/claude-code)"

# 4. Verify CI checks pass
gh pr checks {pr-number} --watch

# 5. Squash Merge
gh pr merge {pr-number} --squash --delete-branch
```

## Command Reference

### Repo Analysis
```bash
# Analyze commit rules
git log --oneline -50 | head -20

# Check lint configuration
cat .eslintrc.* 2>/dev/null || cat eslint.config.* 2>/dev/null
cat .prettierrc.* 2>/dev/null

# Check CI configuration
ls -la .github/workflows/
cat package.json | jq '.scripts'
```

### Branch Management
```bash
# Check current branch
git branch --show-current

# List branches
git branch -a

# Create and switch to branch
git checkout -b feature/{name}

# Delete branch
git branch -d feature/{name}
git push origin --delete feature/{name}
```

### PR Management
```bash
# Create PR
gh pr create --title "title" --body "body"

# List PRs
gh pr list

# Check PR status
gh pr status
gh pr checks {number}

# Merge PR
gh pr merge {number} --squash --delete-branch

# PR comment
gh pr comment {number} --body "message"
```

## Orchestrator Integration

### Backlog Start Hook
```
When the orchestrator starts a backlog:
1. Invoke CI skill
2. Create feature/{backlog-keyword} branch
3. Push to remote
4. Proceed with workflow
```

### Backlog Completion Hook
```
After the orchestrator completes all Phases and PO approves:
1. Invoke CI skill
2. Commit changes (following repo rules)
3. Push
4. Create PR
5. Wait for CI checks
6. Squash Merge to main
7. Delete branch
```

## Usage Examples

```
# Repo analysis and skill generation
"Analyze this repo and generate CI rules"
"Set up commit rules"

# Manual Git operations
"Create a feature branch"
"Commit and create a PR"
"Merge the PR"
```

## Generated Files

```
{project}/.claude/
├── repo-rules.md      # Repo rules document
├── commit-template.md # Commit message template
└── pr-template.md     # PR template
```

## Precautions

1. **No force push**: Do not use the `--force` option
2. **No direct commits to main**: Always use feature branches
3. **CI checks required**: Merge only after all checks pass
4. **Squash Merge**: Use squash for clean history
5. **Branch deletion**: Automatically delete feature branches after merge
