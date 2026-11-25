---
name: standup
description: >
  Generate a standup update from recent git commits, GitHub activity,
  and project context. Summarize what was done, what is in progress,
  and what is blocked.
  TRIGGER when: user says /standup, asks for a standup update, daily
  status, or wants to summarize recent work activity.
argument-hint: "[optional: time range like 'since yesterday' or 'this week']"
user-invocable: true
---

# Standup Update Generator

You help engineers generate clear, concise standup updates from their recent activity. The update should be useful to teammates, not just a log dump.

## Process

### Step 1: Gather Activity Data

Collect information from available sources:

**Git Activity:**
- Run `git log --oneline --since="yesterday" --author="$(git config user.name)"` (adjust timeframe as needed)
- Run `git log --oneline --since="yesterday"` if author is unclear
- Check `git branch` for current working branch
- Check `git diff --stat` for uncommitted work in progress

**GitHub Activity (if gh CLI available):**
- Run `gh pr list --author=@me --state=all --limit=10` for recent PRs
- Run `gh pr list --search="reviewed-by:@me"` for reviews done
- Run `gh issue list --assignee=@me` for assigned issues

**Other Context:**
- Ask the user about meetings, design work, or non-code activities
- Ask about blockers or dependencies

### Step 2: Categorize Activity

Group work into:

| Category | Description |
|----------|-------------|
| **Completed** | Merged PRs, closed issues, finished tasks |
| **In Progress** | Open PRs, active branches, partially done work |
| **Blocked** | Waiting on review, external dependency, decision needed |
| **Planned** | What you intend to work on today |

### Step 3: Generate Update

#### Standard Format

```
**Yesterday / Since [date]:**
- [Completed] Merged PR #123: Add user authentication flow
- [Completed] Fixed bug in payment processing (issue #456)
- [In Progress] Working on search indexing optimization (PR #789 — 80% done)
- [Review] Reviewed PR #101: Database migration for user preferences

**Today:**
- Continue search indexing optimization
- Start API rate limiting implementation
- Team sync on Q2 roadmap at 2pm

**Blockers:**
- Waiting on DevOps for staging environment access (asked Monday)
- Need design review on notification preferences UI
```

#### Compact Format (for Slack/chat)

```
*Done:* Shipped auth flow (#123), fixed payment bug (#456)
*Doing:* Search indexing (PR #789, ~80%)
*Blocked:* Staging access from DevOps
```

#### Detailed Format (for async/weekly updates)

```markdown
## Standup — [Name] — [Date]

### Completed
- **[PR #123] Add user authentication flow**
  - Implemented OAuth2 with Google and GitHub providers
  - Added session management with Redis-backed tokens
  - 95% test coverage on auth module

### In Progress
- **[PR #789] Search indexing optimization**
  - Reduced index build time from 45s to 12s
  - Still need to handle incremental updates
  - ETA: Tomorrow

### Blocked
- **Staging environment access**
  - Requested from DevOps on Monday, followed up Wednesday
  - Blocking end-to-end testing of auth flow
  - Escalation: Will ping DevOps manager if not resolved by EOD

### Notes
- Out of office Friday afternoon
- Sprint review moved to 3pm Thursday
```

## Writing Standards

**Good standup updates:**
- Lead with impact, not activity ("Shipped feature X" not "Wrote code")
- Include PR/issue numbers for traceability
- Quantify progress when possible (80% done, 3 of 5 endpoints complete)
- Be specific about blockers — what is blocked, by whom, since when
- Keep it scannable — teammates should get the gist in 10 seconds

**Avoid:**
- Vague statements ("worked on stuff", "made progress")
- Exhaustive commit-by-commit logs
- Over-explaining technical details (link to the PR instead)
- Listing meetings as accomplishments (unless they produced decisions)

## Time Ranges

| User Says | Git Log Since |
|-----------|--------------|
| "standup" / "daily" | Yesterday / last working day |
| "weekly" / "this week" | Monday / last 7 days |
| "since [date]" | The specified date |
| "sprint update" | Sprint start date |

If the user runs this on Monday, "yesterday" should cover Friday (and the weekend if there was weekend work).

## Edge Cases

- If no git activity found, ask if the work was in a different repo or non-code work
- If the user has many repos, ask which one(s) to check
- If commit messages are cryptic, try to infer intent from branch names and PR titles
- For managers or leads, include team coordination activities (reviews, unblocking, planning)
- If the user works across multiple projects, group by project

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
