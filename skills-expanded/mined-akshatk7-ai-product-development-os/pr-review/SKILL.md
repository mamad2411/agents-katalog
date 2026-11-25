---
name: pr-review
description: Review a GitHub pull request using the team's learned review patterns. Use when the user wants to review a PR, asks for PR feedback, or says "review PR".
alwaysApply: false
---

# Team PR Reviewer

Reviews pull requests against your team's collective review patterns. These patterns are extracted from real review comments by senior engineers — encoding the team's quality bar into a repeatable skill.

## Trigger

"review PR [url]" or "review this PR"

## Pre-Run

1. Read `.claude/skills/pr-review/gotchas.md` (if it exists)
2. Read `.claude/skills/pr-review/runs.log` (if it exists)

## Input

The user provides a GitHub PR URL (e.g., `https://github.com/org/repo/pull/123`).

## Step 1: Fetch PR Context

```bash
# Get PR metadata
gh pr view <PR_NUMBER> --repo <OWNER/REPO> --json title,body,author,files,additions,deletions,baseRefName,headRefName

# Get the full diff
gh pr diff <PR_NUMBER> --repo <OWNER/REPO>

# Get existing review comments (avoid duplicating feedback)
gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments --jq '.[].body'
```

## Step 2: Analyze Against Review Patterns

Review EVERY changed file in the diff. For each file, check against ALL patterns below. Customize these patterns based on your team's actual review history.

### Pattern 1: Safety & Rollback
- **Feature flags**: New behavior changes in hot paths should have a feature flag for quick rollback.
- **Default values**: Verify defaults are the safe choice. If a field can't be determined, what's the safer assumption?
- **Fallback behavior**: When removing feature flags, confirm the current rollout state. Can the flag stay as a killswitch?

### Pattern 2: Code Hygiene & DRY
- **Duplicated logic**: Same logic in multiple files? Suggest a helper function.
- **Dead code**: Flag commented-out code, excessive inline comments, or auto-generated noise.
- **Naming clarity**: Variable/method names should clearly convey purpose. Flag ambiguous names.
- **Unnecessary indirection**: If a value is used in one place, reference it directly instead of creating a companion variable.

### Pattern 3: Operational Readiness
- **Alerts and dashboards**: When changing metric names or adding services, check if alerts/dashboards need updating.
- **Observability**: For new code paths, suggest counter metrics to track usage and detect misuse.
- **Debug logging**: For new queries, API calls, or data flows, suggest feature-flagged logging.

### Pattern 4: Scope & PR Focus
- **Overloaded PRs**: If a PR mixes a core change with a refactor, suggest splitting.
- **Follow-up items**: When something should change later, verify it's tracked as a ticket.

### Pattern 5: Edge Cases & Null Safety
- **Null/empty checks**: When accessing collections or nullable fields, verify bounds.
- **Permission edge cases**: Check behavior for different user roles and permission levels.
- **Time-based edge cases**: Check behavior around boundaries (midnight, DST, timezone differences).

### Pattern 6: Query & Performance Safety
- **Unbounded queries**: Flag SELECT queries without LIMIT or proper filtering.
- **Function overhead in queries**: Applying functions (LOWER, TRIM) in WHERE clauses can prevent index usage.
- **API call proliferation**: When adding external calls to a hot path, check how many already exist.

### Pattern 7: Design Patterns & Extensibility
- **Factory/registry patterns**: When code branches on type enums, suggest a registry map.
- **Completeness of mappings**: When mapping some enum values, ask about unmapped ones.
- **Runtime config vs hardcoding**: Values that might change should be configurable, not hardcoded.

### Pattern 8: API Consistency
- **Mixed field types**: Flag inconsistent use of types in API definitions.
- **Naming alignment**: Verify endpoint names in PR description match the code.

## Step 3: Output Review

Structure feedback as:

1. **Summary** — 1-2 sentences on what the PR does and overall assessment
2. **Must-fix** — Issues that should block merge (safety, correctness, performance)
3. **Should-fix** — Improvements that significantly help but aren't blockers
4. **Nits** — Style, naming, minor suggestions

For each item, reference the specific file and line, the pattern it violates, and a concrete suggestion.

## Post-Run

Append to `.claude/skills/pr-review/runs.log`:
```
[date] | [PR URL] | [files reviewed] | [issues found] | [patterns triggered]
```

If you discover a new team-specific pattern during this review, add it to the patterns list above.
