---
name: last7days
description: "Review the last 7 days of git repository activity. Surfaces trends, risks, and actionable insights from commits, PRs, and issues. Produces a structured weekly report with priority-ranked findings. Triggers: 'review this week', 'what happened in the last 7 days', 'weekly review', 'last week\\'s activity'."
alwaysAllow: ["Bash", "Read", "Glob", "Grep"]
---

# last7days: 7-Day Repo Activity Review

Review the last 7 days of activity in a repo. Surface trends, risks, and actionable insights grounded in real data from git history, GitHub PRs, issues, and code patterns.

<objective>
Produce a concise, data-grounded weekly activity report covering commits, PRs, issues, and code health signals over the last 7 days. Every insight must cite a specific artifact (commit hash, file path, PR number). Degrade gracefully when GitHub CLI is unavailable.
</objective>

## Prerequisites

- **git** >= 2.12 (for `--date=short` and portable relative dates)
- **gh** >= 2.0 (for `--json reviewDecision` on PRs); if older, omit `reviewDecision` from JSON fields
- **Python 3** (optional, portable date fallback for `gh` search queries)

Check versions: `git --version` and `gh --version`

## 1. Setup

<review_target> #$ARGUMENTS </review_target>

(`$ARGUMENTS` is replaced at runtime with whatever the user typed after the skill name.)

Parse the target:
- **Empty** → use current branch in current directory
- **Branch name** → analyze that branch (verify it exists with `git rev-parse --verify`)
- **Path** → verify directory exists, `cd` to worktree
- **GitHub URL** → parse owner/repo, use `gh` CLI

Examples: `last7days` (current branch), `last7days main` (branch), `last7days /path/to/worktree` (path), `last7days https://github.com/owner/repo` (remote). Ambiguous input: try as branch first (`git rev-parse --verify`), then as directory (`test -d`), then report "cannot resolve target."

Detect environment:
- Check if inside a git repo: `git rev-parse --is-inside-work-tree`
- Resolve branch name (handles detached HEAD):
  ```bash
  BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD)
  ```
- Check if `gh` is available and authenticated: `gh auth status 2>&1`
- Set `HAS_GH=true/false` for graceful degradation
- If `HAS_GH=true`, compute the YYYY-MM-DD date for GitHub search queries (portable):
  ```bash
  SINCE_DATE=$(python3 -c "from datetime import date, timedelta; print((date.today()-timedelta(7)).isoformat())")
  ```

Use git's portable relative dates everywhere (no platform-specific `date` commands):
```
--since="7 days ago"
```

**If not a git repo, stop and tell the user.** If `gh` is unavailable, continue with git-only analysis and note that PR/issue data is skipped.

## 2. Data Collection

Run these commands sequentially. Check each for empty output before proceeding.

### 2a. Git Analysis (always available)

**Commits:**
```bash
git log --since="7 days ago" --all --no-merges --format="%H|%an|%ae|%ad|%s" --date=short
```
If empty → report "No commits in the last 7 days" and check `git log -1 --format="%ad" --date=relative` to show when last activity was. Stop here if no commits.

**Diff stats** (only if commits exist):
```bash
OLDEST=$(git log --since="7 days ago" --all --format="%H" --reverse | head -1)
CURRENT=$(git rev-parse HEAD)
if [ -z "$OLDEST" ] || [ "$OLDEST" = "$CURRENT" ]; then
  echo "Insufficient commit range for diff stats — skipping"
else
  git diff "$OLDEST".."$CURRENT" --stat
  git diff "$OLDEST".."$CURRENT" --numstat | head -100
fi
```

**Hotspots** (files changed most often):
```bash
git log --since="7 days ago" --all --name-only --format="" | sort | uniq -c | sort -rn | head -20
```

**Branches:**
```bash
git for-each-ref --sort=-committerdate --format='%(refname:short)|%(committerdate:short)|%(authorname)|%(subject)' refs/heads/
```

**Patterns** — scan recent commit messages:
```bash
git log --since="7 days ago" --all --oneline --no-merges | grep -iE "revert|hotfix|fix bug|WIP|hack|temp|workaround"
```

Check for TODO/FIXME additions:
```bash
git diff "$OLDEST".."$CURRENT" | grep -E "^\+[^+]" | grep -iE "TODO|FIXME" | head -20
```

### 2b. GitHub Analysis (only if HAS_GH=true)

**PRs:**
```bash
gh pr list --state all --limit 100 --search "created:>=$SINCE_DATE" --json number,title,state,author,createdAt,mergedAt,additions,deletions,changedFiles,reviewDecision,labels
```

**Issues:**
```bash
gh issue list --state all --limit 100 --search "updated:>=$SINCE_DATE" --json number,title,state,author,createdAt,closedAt,labels,assignees
```
Filter in analysis: include issues where `createdAt >= $SINCE_DATE` OR `closedAt >= $SINCE_DATE`. This avoids duplicate queries and deduplicates naturally by issue number.

**Releases** (note any releases in the window for the report header):
```bash
gh release list --limit 5
```

If output is exactly 100 items, warn the user that results may be truncated. If any `gh` command fails, log the error and continue with remaining data. Don't abort the whole review.

## 3. Analysis

Synthesize findings across all collected data. Focus on:

- **Velocity** — commit/PR/issue rates, any spikes or dropoffs by day
- **Risk signals** — files changed 3+ times (instability), large unreviewed PRs, revert/hotfix patterns, stale PRs open > 3 days
- **Focus areas** — which parts of the codebase got attention, concentrated vs scattered changes
- **Team dynamics** (multi-author only) — review bottlenecks, knowledge silos (files only one person touches)
- **Patterns** — new TODOs accumulating, dependency changes, config churn

Cross-reference signals: high-churn file with no corresponding test file changes (`*_test.*`, `*.test.*`, `*.spec.*`) in the same window = elevated risk. Multiple reverts in same area = instability. Stale PR + high additions = blocked large change.

## 4. Report

Adapt the report structure to actual findings. **Skip sections that have no data.** For a single-author repo, skip contributor breakdown. For repos with no PRs, skip PR activity.

Core structure:

**Header:**
```
## 7-Day Review: [repo-name] ([branch])
Period: [start_date] → [end_date]
```

**Story of the week** — 2-3 sentences summarizing what happened. Ground it in specifics.

**Key metrics** — table with commits, PRs (opened/merged), issues (opened/closed), lines added/removed, active contributors, files changed. Only include rows where data exists.

**Findings by priority:**
- **Red — Needs Attention:** items requiring action (security concerns, blocking PRs, instability patterns). Include specific file paths, commit hashes, PR numbers.
- **Yellow — Worth Watching:** emerging trends that could become problems. Include current data points.
- **Blue — Highlights:** positive signals worth noting.

**Code hotspots** — top 5-10 most-changed files with change count and authors.

**PR activity** (if HAS_GH) — merged, open, and stale PRs with titles and age.

**Actionable next steps** — 3-5 concrete actions derived from findings.

### Example Output

```markdown
## 7-Day Review: vesper (main)
Period: 2026-02-16 → 2026-02-23

Authentication refactoring dominated this week. Two hotfix commits suggest instability
in the login flow (a1b2c3d, e4f5g6h). One PR (#42) remains open for 5 days with +320 lines.

| Metric | Value |
|--------|-------|
| Commits | 14 |
| PRs merged | 3 |
| PRs open | 2 |
| Lines +/- | +847 / -312 |
| Files changed | 18 |

### Red — Needs Attention
- `src/auth/login.ts` changed 5 times by 2 authors; includes 2 reverts (a1b2c3d, e4f5g6h)
- PR #42 open 5 days, +320 lines, no review decision

### Yellow — Worth Watching
- 3 new TODOs added in `src/api/client.ts`

### Blue — Highlights
- Session isolation refactor merged cleanly (PR #40, #41)

### Code Hotspots
| File | Changes | Authors |
|------|---------|---------|
| src/auth/login.ts | 5 | alice, bob |
| src/api/client.ts | 3 | alice |

### Actionable Next Steps
1. Review and stabilize `src/auth/login.ts` — 2 reverts indicate unresolved issues
2. Review stale PR #42 — 5 days without review decision
3. Address 3 new TODOs in `src/api/client.ts`
```

## 5. Todo Creation (Optional)

If Red items exist, **ask the user** whether to create todo files.

If user confirms, create todo files manually:
- Naming: `{NNN}-pending-{priority}-{description}.md` where `{NNN}` is a sequential integer (001, 002, ...) for this review session
- Priority: `p1` for Red items, `p2` for Yellow items
- Tags: `weekly-review` plus relevant tags (e.g., `security`, `instability`, `stale-pr`)
- Include: problem statement, evidence from analysis (commit hashes, file paths, PR numbers), recommended action

Do not auto-create todos without user confirmation.

## Rules

- Ground every insight in data — commit hashes, file paths, author names, PR numbers, dates. No speculative claims.
- Prioritize signal over noise — surface what matters, not every commit.
- Report objective metrics without judgment — focus on code health, not developer rankings.
- Degrade gracefully — work with whatever data is available (git-only, no PRs, no issues).
- If the repo has no activity in 7 days, say so and show when last activity occurred. Don't produce an empty report.

## Anti-Patterns

- **Do not use `--all` when a specific branch was requested.** `--all` includes remote-tracking refs and will mix unrelated branches into the review.
- **Do not interpret high churn as individual failure.** Report facts; let the user draw conclusions.
- **Do not run `git diff HEAD~N..HEAD` as a shortcut.** It ignores the 7-day window and breaks for repos with fewer than N commits.
- **Do not skip empty-output checks.** Running `uniq -c | sort -rn` on empty input produces no output and no error — the report silently drops the hotspots section.
- **Do not assume `gh` output is complete.** Default limit is 30 results; always use `--limit 100` and warn if output hits the cap.
- **Do not assume "last 7 days" means the current calendar week.** Always use a rolling 168-hour window from now.

## Success Criteria

- [ ] All data collection commands ran (or were explicitly skipped with a noted reason)
- [ ] Report header includes repo name, branch, and exact date range
- [ ] "Story of the week" cites at least one specific commit hash, file, or PR number
- [ ] Key metrics table has no empty rows (omit rows with no data)
- [ ] Every Red finding includes a specific artifact (file path, commit hash, or PR number)
- [ ] Actionable next steps are concrete commands or decisions, not vague recommendations
- [ ] If no activity in 7 days, report explicitly states this and shows last activity date
- [ ] If gh was unavailable, report notes "PR/issue data not available"

## Next Steps

- Generate release notes from this period: `skill: ship-notes`
- Compile agent-optimized changelog: `skill: agent-changelog`
- Persist Red findings in your preferred issue or todo tracker
