---
name: update
description: >
  End-of-session wrap-up — capture progress, update tasks, save context for next session.
  TRIGGER when: user says "wrap up", "end of day", "save progress", "update",
  "done for today", "session summary", or is finishing a work session.
argument-hint: "[topic or area to summarize]"
user-invocable: true
---

# Session Update / Wrap-Up

Capture everything that happened during the work session so the next session starts with full context. This is the counterpart to `/start`.

## Execution Flow

### Phase 1 — Gather Session Activity (run in parallel)

#### 1a. Git Activity

- `git log --oneline --since="8 hours ago"` — commits made this session
- `git diff --stat` — unstaged changes
- `git diff --cached --stat` — staged but uncommitted changes
- `git stash list` — any stashed work
- `git branch -vv` — current branch and tracking status
- Note the current branch name and whether it has unpushed commits.

#### 1b. GitHub Activity (skip gracefully if `gh` unavailable)

- `gh pr list --author @me --state open` — your open PRs and their CI status
- `gh pr list --search "reviewed-by:@me"` — PRs you reviewed today
- Check if any PRs are ready to merge (approved + CI passing).

#### 1c. Task State

- Read `~/.claude/tasks/TASKS.md` if it exists.
- Identify tasks that were `in-progress` at session start.
- Cross-reference with git activity to infer which tasks were worked on.

#### 1d. Memory State

- Read `~/.claude/memory/MEMORY.md` if it exists.
- Note any memories that may be stale or need updating based on today's work.

### Phase 2 — Analyze and Classify

Categorize the session's work:

1. **Completed**: Tasks finished, PRs merged, issues closed.
2. **Progressed**: Tasks/PRs that moved forward but aren't done.
3. **Created**: New branches, PRs, tasks, or issues opened.
4. **Blocked**: Anything that hit a wall — note the specific blocker.
5. **Discovered**: New information, decisions, or context that emerged.

### Phase 3 — Update Systems

#### Update Tasks

For each task that was worked on:
1. Update `status` if it changed (todo -> in-progress, in-progress -> done).
2. Set `updated: {today}`.
3. Add a timestamped note under `## Notes` summarizing progress.
4. Set `completed: {today}` if done.
5. Update `TASKS.md` index to reflect current state.

#### Save New Memories (only if warranted)

Evaluate whether any session context should be persisted. **Save only what is:**
- Non-obvious (not in code, commits, or task files)
- Useful for future sessions (not just today)
- Decision context ("we chose X because Y" — the "because Y" part)

**Do NOT save:**
- What code was changed (that's in git)
- Task status updates (that's in task files)
- Anything that will be stale by next session

If saving, follow the `/memory-management` save protocol.

#### Flag Uncommitted Work

If there are uncommitted changes:
- Warn the user with the list of modified files.
- Ask if they want to commit, stash, or leave as-is.
- Do NOT commit or stash without explicit confirmation.

### Phase 4 — Present Summary

Output a structured wrap-up:

```
## Session Summary — {date}

### Completed
- Merged PR #123: "Add auth middleware"
- Closed TASK-005: "Migrate user table"

### In Progress
- PR #125: "Add rate limiting" — CI passing, awaiting review
- TASK-008: branch `feature/rate-limit` — 3 uncommitted files

### Blocked
- TASK-006: "Deploy auth service" — waiting on staging environment access

### Decisions & Context Saved
- Saved memory: "Auth service uses JWT with 15min expiry — compliance requirement"

### For Next Session
- Review PR #130 from @teammate (requested 2 days ago)
- TASK-008 needs tests before opening PR
- Merge freeze starts 2026-04-10 — finish open PRs before then

### Uncommitted Work
- `src/middleware/rate-limit.ts` (modified)
- `tests/rate-limit.test.ts` (new)
> Action needed: commit, stash, or leave?
```

### Phase 5 — Handoff

Ask the user:

1. "Anything else to capture before wrapping up?"
2. If they mention something, save it as a memory or task as appropriate.
3. End with a brief "you're all set" confirmation.

## Edge Cases

- **No activity**: If no git commits, task changes, or PR activity, acknowledge a light session. Don't fabricate activity.
- **Multiple repos**: Only summarize the current working directory. If memories reference other projects, note them under "For Next Session."
- **First session**: If no task or memory system exists yet, offer to set them up using `/task-management` and `/memory-management`.
- **Long sessions**: If git log shows > 20 commits, group by branch or feature area rather than listing each one.

## Output Standards

- Use the same formatting conventions as `/start` for consistency.
- Show dates in relative + absolute form.
- Keep the summary under 50 lines unless the user asks for detail.
- Bold section headers and key action items.

## Quality Checklist

- [ ] Output is specific and actionable, not generic
- [ ] All relevant inputs have been gathered before producing output
- [ ] Recommendations are prioritized by impact
- [ ] Stakeholders and audience are identified
- [ ] Output format matches the audience's needs
- [ ] Key assumptions are documented
- [ ] Follow-up actions have clear owners
