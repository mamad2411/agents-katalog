---
name: doomsday
description: This skill should be used when the user asks to "end session", "shutdown", "wrap up", "prepare handoff", "save everything", "doomsday protocol", or is finishing a coding session and needs to preserve context for next time.
---

# End of Session Shutdown Protocol (Doomsday Prep)

**Role:** Paranoid Lead Architect and Project Manager.

**Objective:** Secure project state, update all documentation, and prepare a comprehensive handoff. Treat this as if the server is about to be wiped and rebuild must happen from these files alone.

## Phase 1: Execution & File Integrity

1. **Force Save:** Ensure every code block, text buffer, or conceptual change discussed is written to its respective file. Leave nothing in "memory" only.
2. **File Creation:** If new files were discussed but not generated, generate them now.

## Phase 2: Documentation Synchronization

Update the following `.md` files immediately. Create them if they do not exist:

### A. Update `README.md`
- Reflect the current state of the application
- Update installation or usage instructions if dependencies changed
- Add a "Recent Changes" section summarizing this session's work

### B. Update/Create `PROJECT_STATUS.md`
- **Current Phase:** Where exactly are we? (Dev, Testing, Refactoring)
- **Completed:** Bullet points of everything achieved this session
- **In Progress:** What is half-baked? (Mark clearly to avoid deploying broken code)
- **Blockers:** Any bugs or issues that couldn't be solved today

### C. Update User/Dev Docs
- If API endpoints changed, update API documentation
- If UI logic changed, update user guides

## Phase 3: The Brain Dump (Context Preservation)

Create `SESSION_HANDOFF_[DATE].md` (or append to `CHANGELOG.md`). Include:

1. **The "Why":** Briefly explain *why* specific architectural decisions were made today
2. **The "Gotchas":** Note weird bugs or workarounds that might be forgotten
3. **Next Actions:** Strictly prioritized list of exactly what to do first next session

## Phase 4: Version Control

1. Generate a comprehensive **Git Commit Message** formatted as:
   - `feat/fix/chore: [Summary]`
   - `[Bulleted list of detailed changes]`
   - End the message with the attribution line `Co-Authored-By: Claude Code <noreply@anthropic.com>`
2. **Ask the user: "Commit and push now?"** Do not end the session while this question is open. On **yes**: stage (`git add -A`), commit, and push, then verify with `git status -sb` (clean and in sync with origin) and report the commit hash. On **no**: record in the handoff's "Next Actions" that the commit is prepared but NOT run — never leave this implicit — and do not run git.

## Final Output Format

```
✅ FILE SYNC STATUS: [Report on files saved/updated]
📄 DOCS UPDATED: [List of .md files touched]
🔖 COMMIT: [pushed hash / or "prepared, not run — commit is queued for next session"]
🚀 NEXT SESSION TRIGGER: [The one command or task to run first next time]
```

Execute immediately. Go.
