---
name: update-pull-request
description: Update an existing pull request's title and description to accurately reflect the implemented changes. Use this skill when asked to update, refresh, or rewrite a PR title or description, sync a PR with the latest changes, or when the PR description no longer matches the implementation.
license: MIT
---

# Update Pull Request

This skill teaches how to update an existing pull request's title and description so they accurately reflect the implemented changes.

## When to Use This Skill

- A PR description is outdated or no longer matches the implementation
- You want to sync the PR title and description with the latest changes on the branch
- Addressing reviewer feedback about unclear PR descriptions
- After significant changes to the branch that alter the scope or intent

## PR Conventions

All PR title rules, validation requirements, and description templates follow the same conventions as creating PRs. See [create-pull-request skill](../create-pull-request/SKILL.md) for complete details.

### Title Format

```text
<type>(<scope>): <gitmoji> <subject>
```

- **Format**: `<type>(<scope>): <gitmoji> <subject>` (max 128 chars)
- **Subject**: Imperative mood, lowercase after gitmoji, no period
- **Gitmoji**: Must match the type (✨ feat, 🐛 fix, 📝 docs, ♻️ refactor, 🔧 chore, ⬆️ dependencies, etc.)

### Description Template

```markdown
## 🌰 Summary

<!-- Brief description of what this PR does (1-2 sentences) -->

## 📝 Details

- <!-- List of specific changes made -->

## 🧪 Testing

1. <!-- How to manually verify these changes work correctly -->

## 🔗 Related

- <!-- Link any relevant documentation or related resources like internal documentation, GitHub issues/pull requests -->
```

## Workflow

### Step 1 — Identify the Active Pull Request

Determine the current branch and locate its open PR:

```bash
git rev-parse --abbrev-ref HEAD
gh pr view --json number,title,body,baseRefName
```

If no PR exists, inform the user and suggest using the **create-pull-request** skill instead.

### Step 2 — Gather the Full Diff

Get the complete set of changes between the base branch and HEAD:

```bash
git log origin/main..HEAD --oneline
git diff origin/main..HEAD --stat
git diff origin/main..HEAD
```

For large diffs, also review individual commits to understand intent:

```bash
git log origin/main..HEAD --format="%h %s"
```

### Step 3 — Analyze Changes

From the diff, determine:

1. **Primary type** — What kind of change is this? (`feat`, `fix`, `refactor`, `docs`, `chore`, etc.)
2. **Scope** — Which project(s) or category is affected?
3. **Gitmoji** — Which emoji matches the type?
4. **Summary** — A 1-2 sentence description of the overall purpose
5. **Detailed changes** — A complete bulleted list of every meaningful modification
6. **Testing strategy** — Relevant `nx` commands and manual verification steps
7. **Affected projects** — Which Nx projects are touched (for testing commands)

### Step 4 — Discover Related Issues and Documentation

Search for issues and documentation that may be related to this PR:

- Parse the branch name for issue numbers (e.g., `feat/lexico-fix-123` → `#123`)
- Scan commit messages for issue references
- Search for open issues matching keywords: `gh issue list --search "<keywords>"`
- Look for relevant documentation links: AGENTS.md, SKILL.md, planning files, or external library docs referenced in the changes

Use appropriate linking keywords:

| Keyword           | Effect                      |
| ----------------- | --------------------------- |
| `Closes #N`       | Closes issue when PR merges |
| `Fixes #N`        | Closes issue when PR merges |
| `Resolves #N`     | Closes issue when PR merges |
| `Related to #N`   | Links without closing       |

If no related issues or documentation are found, omit the Related section content.

### Step 5 — Generate Updated Title

Compose a new title following `<type>(<scope>): <gitmoji> <subject>`:

- Keep the subject concise (aim for < 50 chars after emoji)
- Use imperative mood ("add", "fix", "update", not "added", "fixes", "updates")
- Lowercase after gitmoji, no trailing period
- Total length must not exceed 128 characters

### Step 6 — Generate Updated Description

Write the description using **only facts derived from the diff**. Do not speculate or include aspirational content.

Use the PR template as the structure:

<!-- pr-template-start -->

```markdown
## 🌰 Summary

<!-- Brief description of what this PR does (1-2 sentences) -->

## 📝 Details

- <!-- List of specific changes made -->

## 🧪 Testing

1. <!-- How to manually verify these changes work correctly -->

## 🔗 Related

- <!-- Link any relevant documentation or related resources like internal documentation, GitHub issues/pull requests -->
```

<!-- pr-template-end -->

Fill each section based on **only facts derived from the diff**:

- **Summary**: Synthesize the overall purpose from the actual changes
- **Details**: One bullet per meaningful change, present tense, specific file/component names
- **Testing**: Include `nx run <project>:<target>` commands for affected projects, plus manual steps
- **Related**: Include discovered issue links and relevant documentation links, or omit section if none found

### Step 7 — Update the Pull Request

Use the `gh` CLI to apply the changes:

```bash
gh pr edit <PR_NUMBER> \
  --title "<type>(<scope>): <gitmoji> <subject>" \
  --body "<generated description>"
```

### Step 8 — Verify

After updating, confirm the PR was updated successfully:

```bash
gh pr view <PR_NUMBER>
```

Report the updated title and a brief confirmation to the user.

## Quality Checklist

Before submitting the update, verify:

- [ ] Title follows `<type>(<scope>): <gitmoji> <subject>` format (max 128 chars)
- [ ] Subject uses imperative mood and lowercase after gitmoji
- [ ] Summary accurately reflects the diff (no speculative content)
- [ ] Details list covers all meaningful changes from the diff
- [ ] Testing section includes relevant `nx` commands for affected projects
- [ ] Related issues use correct linking keywords and documentation links are included where relevant
- [ ] Description uses present tense ("Add", "Update", "Remove")

## Error Recovery

If the PR update fails:

```bash
# Check GitHub CLI auth
gh auth status

# Retry the update
gh pr edit <PR_NUMBER> \
  --title "<type>(<scope>): <gitmoji> <subject>" \
  --body "<generated description>"
```

## Resources

- [create-pull-request skill](../create-pull-request/SKILL.md) — Full PR conventions and creation workflow
- [commit-code skill](../commit-code/SKILL.md) — Types, scopes, and gitmoji reference
