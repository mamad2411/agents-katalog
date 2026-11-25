---
name: session-wrap
description: End-of-session documentation - summarize accomplishments and lessons
allowed-tools: Bash, Read, Write, Glob
disable-model-invocation: true
---

# Session Wrap-Up

Document the current session's accomplishments and lessons learned.

## Instructions

### 1. Gather Session Data

```bash
# Commits made this session (last 24 hours or since session start)
git log --since="8 hours ago" --oneline

# Files changed
git diff --stat HEAD~5 2>/dev/null || git diff --stat

# Current branch and status
git branch --show-current
git status --short
```

### 2. Create Session Summary

Create a file at `docs/sessions/YYYY-MM-DD-session.md`:

```markdown
# Session Summary - YYYY-MM-DD

## Accomplishments

- [Major accomplishment 1]
- [Major accomplishment 2]
- [...]

## PRs Created/Merged

- PR #X: [title] - [status]

## Commits

- [commit hash] [message]
- [...]

## Blockers Encountered

- [Blocker 1] - [resolution or status]

## Next Steps

- [ ] [Next task 1]
- [ ] [Next task 2]
```

### 3. Create Lessons Learned (if applicable)

If you encountered something worth documenting, create `docs/sessions/YYYY-MM-DD-lessons.md`:

```markdown
# Lessons Learned - YYYY-MM-DD

## What Worked Well

- [Pattern or approach that was effective]

## What Didn't Work

- [Approach that failed and why]

## Key Insights

- [Insight that would help future sessions]

## Knowledge Updates Needed

- [ ] Update `knowledge/[skill]/SKILL.md` with [insight]
```

### 4. Commit Documentation

```bash
git add docs/sessions/
git commit -m "docs: session wrap-up for YYYY-MM-DD"
```

## Output

Summarize what was documented and any recommendations for the next session.
