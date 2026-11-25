---
name: handover-writer
description: Use when approaching context limits (70%+ usage), switching tasks mid-stream, ending a session with incomplete work, or when the user says "write a handover", "save progress", "I need to stop", or "context is getting full". Also use proactively when you detect that context compression has started occurring.
---

# Handover Writer

## Overview

Generate a structured handover document that enables a fresh session to continue work seamlessly. The handover captures everything a new session needs: what was done, what remains, critical context, and exact next steps. A good handover eliminates the "where was I?" problem entirely.

## When to Use

- Context usage at 70%+ (system will block edits soon)
- User says "save progress", "write handover", "wrap up"
- Switching from one task to another mid-session
- Before `/clear` command
- Any time incomplete work needs to survive a session boundary

## Process

### Step 1: Gather State

Collect all relevant information:

```bash
# Current branch and changes
git status
git log --oneline -5
git diff --stat

# Worktree info (if applicable)
git worktree list
```

Read the current task list (if any) and note completed vs pending items.

### Step 2: Write the Handover Document

Save to `docs/handovers/YYYY-MM-DD-<task-slug>.md`:

```markdown
# Handover: [Task Name]

**Date**: YYYY-MM-DD
**Branch**: `[branch-name]`
**Worktree**: `[path or N/A]`
**Last Commit**: `[hash]` — [message]
**Completion**: [X]%

## What Was Done

- [Completed item 1 with specific details]
- [Completed item 2]
- [Files modified: list key files]

## What Remains

1. **[Next task]** — [specific details, file paths, line numbers]
2. **[Following task]** — [details]
3. **[Final task]** — [details]

## Critical Context

- [Decision made during session and WHY]
- [Gotcha discovered that future session must know]
- [Dependency or ordering constraint]

## Files Modified

| File | Change |
|------|--------|
| `path/to/file.js` | [what changed] |
| `path/to/other.js` | [what changed] |

## Uncommitted Changes

[If any — describe what's staged, what's unstaged, and whether it's safe to commit]

## Test Status

- Unit tests: [passing/failing — which ones]
- E2E tests: [passing/failing/not run]

## How to Continue

1. Read this handover
2. `cd [worktree-path]` or `git checkout [branch]`
3. [Exact first command or action to take]
4. [Second action]

## Related Vault Memories

- Recall: `search_vault(query="[topic]")` for related context
- Key decisions stored via `/vault-capture`
```

### Step 3: Update MEMORY.md

Update the "Resume Point" section in MEMORY.md with:
- Task name and completion percentage
- Branch and worktree path
- Last commit hash
- Reference to this handover doc
- Brief remaining work summary

### Step 4: Save to Obsidian Vault

If the work involves important decisions, gotchas, or patterns worth preserving:
- `/vault-capture` with key findings (type="issue" for gotchas, type="decision" for decisions)
- Vault handles relations via tags/links automatically

### Step 5: Commit the Handover

```bash
git add docs/handovers/YYYY-MM-DD-<task-slug>.md
git commit -m "docs: add handover for [task name]"
```

## Quality Criteria

A good handover must pass this test: **Could a brand new Claude session read ONLY this document and the referenced files and continue the work without asking clarifying questions?**

Checklist:
- [ ] Specific file paths (not "the component" — which component?)
- [ ] Specific line numbers for remaining edits
- [ ] Exact git commands to get to the right state
- [ ] WHY decisions were made, not just WHAT
- [ ] Test status with specific test names if failing
- [ ] No jargon without explanation

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Vague remaining work ("finish the feature") | List exact files, functions, line numbers |
| Missing decision rationale | Always explain WHY, not just WHAT |
| Forgetting uncommitted changes | Always run git status and include results |
| Not updating MEMORY.md | Resume point must be updated too |
| Writing handover too late (90%+ context) | Start at 70%, don't wait |
