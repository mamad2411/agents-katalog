---
name: context-preservation
description: Prevent AI context loss — maintain full project awareness across sessions and within long runs
triggers: [context lost, forgot, token, session, memory, remember, pick up where]
---

# SKILL: Context Preservation

## Purpose
AI has limited memory. Every session ends, context resets, tokens burn.
This skill prevents the #1 productivity killer: losing context.

## The Context Loss Problem
```
Session ends → Context gone
Tokens fill up → Compaction degrades quality
New session → AI asks questions already answered
Mid-task compact → Loses file paths, variable names, state
```

## The Solution: External Memory System

### Layer 1: CONTEXT_STATE.md (session-to-session)
Update this file at the END of every response that changes state:
```markdown
# Context State — Updated: [timestamp]

## What we are building
[Project name, type, one-line description]

## Current phase
[Phase name] → [Status: active/blocked/complete]

## Active task RIGHT NOW
[Exact task, exact file being worked on]

## Completed this session
- [task]: [result]

## Next actions (in order)
1. [most critical]
2. [second]
3. [third]

## Key decisions
- [decision]: [reason]

## Blockers
- [blocker]: [what unblocks it]

## Files being worked on
- [path]: [status/what is happening]

## Stack confirmed
[Stack choices locked in]
```

### Layer 2: PROGRESS.md (cross-session history)
Never overwrite. Always append:
```markdown
## [Date]
- Completed: [list]
- In progress: [list]
- Blocked by: [list]
- Next session start: [exact first task]
```

### Layer 3: ARCHITECTURE_DECISIONS.md (why decisions were made)
Any significant choice goes here immediately:
```markdown
## [YYYY-MM-DD] [Decision title]
Context: [what situation]
Decision: [what was decided]
Reason: [why]
Alternatives: [what was rejected and why]
```

### Layer 4: Git as memory
Commit after every meaningful unit of work:
```bash
git commit -m "feat(auth): add JWT login endpoint"
git commit -m "chore: update context state — completed auth, starting dashboard"
```

## Session Start Protocol (run automatically)
```
1. Read docs/CONTEXT_STATE.md → know current state
2. Read docs/PROGRESS.md → know history
3. git log --oneline -10 → see recent work
4. Read docs/ARCHITECTURE_DECISIONS.md → know why things are built as they are
5. Identify: what is the EXACT next action?
6. Begin — do not ask questions already answered in these files
```

## When to Compact Context (/compact)
✅ After research phase completes, before implementation starts
✅ After a complete milestone, before starting the next
✅ Context is above 50% used
✅ After debugging session

❌ NEVER compact mid-implementation
❌ NEVER compact during TDD RED phase
❌ NEVER compact before saving state to docs/

## Anti-Patterns to Avoid
```
✗ Starting a session without reading CONTEXT_STATE.md
✗ Asking questions already answered in PROGRESS.md
✗ Compacting context without saving state first
✗ Not committing before ending a session
✗ Keeping all context only in the chat window
✗ Using more than 10 MCP servers (eats context window)
```

## Quality checks
- [ ] CONTEXT_STATE.md exists and is current
- [ ] PROGRESS.md updated at end of every session
- [ ] Commits made after every meaningful change
- [ ] Architecture decisions documented
- [ ] Session start reads context before doing anything
