---
name: start
description: >
  Initialize a work session with context, status, and priorities.
  TRIGGER when: user says "start my day", "what's on my plate", "catch me up",
  "morning briefing", "what should I work on", or begins a new session.
argument-hint: "[focus-area]"
user-invocable: true
---

# Session Start

Orient the user at the beginning of a work session. Gather context from all available sources, synthesize it, and present a prioritized briefing.

## Execution Flow

Run independent data-gathering steps **in parallel** where possible, then synthesize.

### Phase 1 — Gather (run in parallel)

#### 1a. Load Persistent Context

- Read `~/.claude/memory/MEMORY.md` — if it exists, scan for project and reference memories relevant to today's work.
- Read `.claude/CLAUDE.md` in the current project — if it exists, note any project-specific conventions.
- If `$ARGUMENTS` specifies a focus area, prioritize memories matching that topic.

#### 1b. Git State

- `git status` — uncommitted changes, untracked files
- `git branch -vv` — local branches and their tracking status
- `git log --oneline --since="yesterday" --all` — recent activity across all branches
- `git stash list` — any stashed work that might be forgotten

#### 1c. GitHub State (skip gracefully if `gh` is not authenticated)

- `gh pr list --assignee @me --state open` — open PRs you own
- `gh pr list --search "review-requested:@me"` — PRs awaiting your review
- `gh issue list --assignee @me --state open --limit 10` — assigned issues
- Note: If `gh` commands fail, report "GitHub integration unavailable" and continue.

#### 1d. Task State

- Check if `~/.claude/tasks/TASKS.md` exists.
- If yes, read it and extract tasks with status `todo` or `in-progress`.
- Flag overdue tasks (due date < today).
- Flag stale tasks (no update in > 7 days).

### Phase 2 — Synthesize

Combine all gathered data into a single briefing. Prioritize by urgency:

1. **Blockers & Alerts** — failing CI, overdue tasks, stale PRs, merge conflicts
2. **Needs Attention** — PRs awaiting review, issues with approaching deadlines
3. **In Progress** — branches with uncommitted work, open PRs, active tasks
4. **Queued** — todo tasks, assigned issues not yet started

### Phase 3 — Present

Output a structured briefing:

```
## Daily Briefing — {date}

### Alerts
- {anything requiring immediate attention, or "None"}

### In Flight
- {PR #123: "Add auth middleware" — 2 approvals, CI passing, ready to merge}
- {Branch: feature/payments — 3 uncommitted files}
- {TASK-005: "Migrate user table" — in-progress, due tomorrow}

### Queued
- {TASK-007: "Write API docs" — todo, medium priority}
- {Issue #45: "Fix pagination on /users" — assigned, no branch yet}

### Review Requests
- {PR #130 by @teammate: "Refactor logging" — requested 2 days ago}

### Context from Memory
- {Any relevant project memories, e.g., "Merge freeze starts 2026-04-10"}
```

### Phase 4 — Plan

If `$ARGUMENTS` specifies a focus area, suggest a prioritized plan for that area.

Otherwise, ask: **"What would you like to focus on?"** and offer the top 3 suggested priorities based on urgency.

## Edge Cases

- **Empty state**: If no memories, tasks, git history, or GitHub items exist, acknowledge this is a fresh start and offer to set up the task/memory system.
- **Large backlog**: If there are > 20 open items, group by category and show counts rather than listing every item. Offer to drill into any category.
- **Multiple repos**: Only report on the current working directory's git state. Mention if memories reference other projects.

## Output Standards

- Use bullet points, not paragraphs.
- Bold labels for scanability.
- Show dates in relative + absolute form: "tomorrow (2026-04-09)".
- Keep the entire briefing under 40 lines unless the user asks for detail.

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
