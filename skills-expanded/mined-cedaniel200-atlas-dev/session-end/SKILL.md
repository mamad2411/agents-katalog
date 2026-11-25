---
name: session-end
description: "Session close checklist: tests, final commit, clean state and a summary for the next session."
license: MIT
---

# Session end

## Steps (in order)

1. **Full tests** with the command declared in `AGENTS.md` → green.
2. **Final commit** if changes remain: conventional commit + role byline.
3. **Push** the working branch.
4. **Clean state**: `git status` without pending changes (or only inside the feature worktree).
5. **Summary**: what was done, what remains, relevant files.

## Checklist

- [ ] Tests green
- [ ] Incremental commits (not one giant commit)
- [ ] Role byline on agent commits
- [ ] No open QA or review findings
- [ ] Default branch clean; work lives in its branch/worktree
- [ ] Summary written for the next session

## Persistent memory (if configured)

Store the session summary with the project's memory tool. If there is no memory configured, the
summary goes to the chat and to the commit or PR description.
