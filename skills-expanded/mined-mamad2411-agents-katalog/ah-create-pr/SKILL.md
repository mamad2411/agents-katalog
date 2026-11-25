---
name: ah-create-pr
description: Use this skill to create a GitHub Pull Request when using the "ah" prefix. Use when asked to "ah create pr", "ah create pull request", or "ah pr". Analyzes the current branch, runs quality checks, generates a well-structured PR with summary, changes, tests, and linked issues, then creates it via `gh pr create`.
argument-hint: "base branch, issue number, labels"
---

# Create GitHub Pull Request

Analyze the current branch and create a well-structured GitHub Pull Request. The diff against the base branch is the single source of truth for all PR content.

## Input

- **Base branch** (REQUIRED): The target branch this PR will merge into (e.g., `main`, `develop`). If the user did not provide it, STOP and ask before proceeding. Never assume or default to any branch.
- **Issue number** (optional): The GitHub issue number this PR addresses (e.g., `42`, `#42`). If not provided by the user, do not attempt to infer it from the branch name -- simply omit issue references from the PR.
- **Labels** (optional): Comma-separated list of labels to apply to the PR (e.g., `bug,urgent`, `feature,frontend`). If not provided by the user, auto-detect labels in step 2.
- Current Git branch with unmerged commits
- Git diff against the base branch

## Procedure

### 0. Preparation

Run quality checks to catch issues before creating the PR. If any check fails, report the failure and ask the user how to proceed.

```bash
pnpm preflight
pnpm preflight:build
```

Also compare `.env*` files in the repo root: identify missing keys across them and flag any security risks or naming inconsistencies.

### 1. Gather Context

If the user did not provide a base branch, STOP and ask for it before proceeding.

```bash
BASE_BRANCH=<user-provided base branch>
CURRENT_BRANCH=$(git branch --show-current)

# Full diff against base (primary source of truth)
git diff origin/${BASE_BRANCH}...HEAD --stat
git diff origin/${BASE_BRANCH}...HEAD

# Commit history on this branch
git log origin/${BASE_BRANCH}..HEAD --no-decorate

# Branch tracking status
git status -sb
```

If the user provided an issue number, use it for the PR references. Do not infer issue numbers from the branch name or commit messages.

### 2. Analyze Changed Files

- **Categorize changes** by functional area (features, components, API, config, tests, etc.).
- **Identify patterns** -- look for related changes that form logical blocks (e.g., "Auth flow refactor", "Error handling improvements").
- **Validate scope** -- verify all changes contribute to the same feature/fix. Flag unrelated changes that may need separate PRs.

#### Determine Labels

If the user provided labels, use them as-is. Otherwise, auto-detect labels by analyzing:

1. **Fetch available labels** from the repository:
   ```bash
   gh label list --limit 100 --json name,description
   ```
2. **Match labels** based on the PR content:
   - **PR title type** -- map the commit type (`feat`, `fix`, `refactor`, `docs`, `test`, `perf`, `chore`) to matching labels (e.g., `feat` -> `feature`/`enhancement`, `fix` -> `bug`/`bugfix`, `docs` -> `documentation`)
   - **Changed file paths** -- infer domain labels from directories (e.g., changes in `src/api/` -> `api`/`backend`, changes in `src/components/` -> `frontend`/`ui`, changes in `infra/` -> `infrastructure`)
   - **Diff content** -- detect patterns like security fixes, dependency updates, breaking changes, and match to corresponding labels
3. **Select only labels that exist** in the repository. Never create or suggest labels that do not exist.
4. **Limit to 1-4 labels** -- pick the most relevant ones. Prefer specific labels over generic ones.

### 3. Generate PR Content

#### Summary

- Parse branch name and commit messages to understand the change intent.
- If the user provided an issue number, retrieve its context and write a clear, standalone explanation (2-4 sentences). Never just say "Fixes #XXX" without explaining what the issue was about.

#### Changes

For each logical group of changes, write a bullet point describing:

- What was changed (component/file/feature area)
- Why it was changed (how it contributes to the Summary)
- Brief technical approach if complex

Every significant diff block from `git diff origin/${BASE_BRANCH}...HEAD` must be represented. The diff is the single source of truth. Explicitly note if any changes seem unrelated to the main purpose.

Do not link to files or code snippets in the Changes section.

Example format:

```markdown
- **Added new help-circle icon** (`src/icons/help-circle.svg`)
  - Consistent with existing icon style (24x24 SVG with animated strokes)
  - Question mark in circle design for FAQ functionality

- **Modified AppLayout sidebar menu** (`src/layouts/AppLayout/index.tsx`)
  - Replaced contact button with FAQ link that opens in a new tab
  - Added `rel="noopener noreferrer"` for security best practices
```

#### Tests

- List which existing tests should be affected based on the changes.
- Identify whether new functionality requires new tests and whether they are included.
- Check for `.test.ts`, `.spec.ts`, or test-related changes in the diff.
- Flag if new functionality lacks test coverage.
- Include manual testing steps if relevant.

Example format:

```markdown
- **Manual Testing Required**: Verify the fix works by:
  1. Step one
  2. Step two
  3. Step three
- **Automated Tests**: Description of test coverage status
```

#### GH (GitHub References)

If the user provided an issue number, include closing keywords with proper syntax: `Fixes #123`, `Closes #456`, `Resolves #789`. If no issue number was provided, omit this section entirely from the PR body.

### 4. Create Pull Request

**Title format**: `<type>: <brief description>` -- keep under 70 characters.

- Types: `feat`, `fix`, `refactor`, `chore`, `test`, `docs`, `perf`
- For monorepos, prefix with app name: `app-name/feat: description`
- Extract from the first commit if it already follows this format.

**Draft mode**: Create as draft if any of these apply:

- TODOs identified in commit messages
- Tests missing for new features
- Scope seems too large (>20 files changed)

Push the branch to the remote if it has not been pushed yet or is behind:

```bash
git push -u origin ${CURRENT_BRANCH}
```

Then create the PR (include `--label` flags for each determined label):

```bash
gh pr create \
  --base "${BASE_BRANCH}" \
  --head "${CURRENT_BRANCH}" \
  --title "<type>: <brief description>" \
  --label "<label1>" --label "<label2>" \
  --body "$(cat <<'EOF'
## Summary

<2-4 sentence explanation of what this PR does and why>

## Changes

<bullet points from step 3>

## Tests

<test coverage details from step 3>

## GH

<closing keywords from step 3>
EOF
)"
```

Omit `--label` flags entirely if no labels were determined.

### 5. Report to User

After creating the PR, provide:

1. **PR URL** -- direct link to the created pull request
2. **Summary** -- brief recap of what was included
3. **Labels** -- list the labels applied and briefly explain why each was chosen (or note that none were applicable)
4. **Action Items** -- any TODOs or follow-ups identified
5. **Review Checklist** -- quick reminders for self-review before requesting reviewers

## Validation Checks

Before submitting the PR, verify:

- All applicable sections are populated (Summary, Changes, Tests, and GH if an issue was provided)
- No placeholder text like "TODO" or "TBD" remains (unless in explicit TODO checkboxes)
- If an issue number was provided, closing keywords are correctly formatted
- Changes align with branch name and commit messages
- Test coverage is addressed (present or explicitly noted as TODO)

## Error Handling

- If no base branch was provided, STOP and ask the user for it
- If no commits exist ahead of the base branch, abort and inform user
- If diff is empty, check for unstaged changes and prompt user

## Best Practices

- **Atomic PRs**: Warn if scope seems too broad (suggest splitting if >30 files or multiple unrelated features)
- **Conventional Commits**: Use semantic versioning-friendly titles
- **Self-Review**: Suggest the author review the generated content before requesting reviewers
