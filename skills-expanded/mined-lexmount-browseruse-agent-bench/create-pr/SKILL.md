---
name: create-pr
description: Create GitHub pull requests for browseruse-bench with clear conventional-commit style titles and a review-ready body.
allowed-tools: Bash(git:*), Bash(gh:*), Read, Grep, Glob
---

# Create Pull Request

Create a draft GitHub pull request for this repository using `gh`.

## Prerequisites

1. `gh` is installed and authenticated.
2. Your branch is pushed to origin.
3. You are in the repository root.

## PR Title Format

Use conventional commit style:

```
<type>(<scope>): <summary>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `perf`: Performance improvement
- `refactor`: Refactor without behavior change
- `docs`: Documentation only
- `test`: Tests only
- `build`: Build/dependency changes
- `ci`: CI workflow/config changes
- `chore`: Maintenance tasks

### Scope Suggestions

- `core`
- `cli`
- `agents`
- `benchmarks`
- `docs`
- `skills`

### Summary Rules

- Imperative present tense (for example: `Add`, `Fix`, `Refactor`)
- Start with capital letter
- No trailing period
- Keep it specific and concise

## Workflow

1. Inspect local changes:

```bash
git status
git diff --stat
git log origin/main..HEAD --oneline
```

2. Decide title components:
- Type
- Scope
- Summary

3. Push branch if needed:

```bash
git push -u origin HEAD
```

4. Create draft PR:

```bash
gh pr create \
  --draft \
  --base main \
  --title "<type>(<scope>): <summary>" \
  --body "$(cat <<'PRBODY'
## Summary

- What changed
- Why it changed

## Testing

- [ ] `uv run ruff check .`
- [ ] `uv run pytest`

## Related

- Optional: `closes #<issue-number>`
PRBODY
)"
```

## Body Guidelines

- `Summary`: explain behavior change and key files touched.
- `Testing`: list commands actually run.
- `Related`: reference GitHub issues when available.

## Examples

```text
fix(cli): Propagate skills command exit code
```

```text
docs(benchmarks): Correct LexBench split filenames
```

```text
refactor(agents): Guard duplicate agent registration names
```

## Validation Checklist

- Title follows `<type>(<scope>): <summary>`.
- Summary accurately reflects the patch.
- Testing section contains real commands/results.
- Related issue links are included when relevant.
