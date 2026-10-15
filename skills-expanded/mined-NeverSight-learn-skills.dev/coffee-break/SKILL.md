---
name: coffee-break
description: Park mid-arc session state and work in progress. Routes to /reflect first if memory work is pending.
---

# Coffee Break

Park work, print resume instructions. Heaviness check first — if memory consolidation is pending, route to /reflect.

## 1. Heaviness check (route to /reflect if any fires)

- New `feedback_*.md` or `project_*.md` in `~/.claude/projects/<slug>/memory/` with mtime > `$SESSION_DIR` directory mtime (≈ session-start on CC; on Codex, skip this signal with logged reason `no $SESSION_DIR`)
- `ai-workspace/MEMORY.md` modified in-branch (`git status` non-empty OR commits since fork)
- If unsure, ask user: is the branch task complete or paused? If complete, fire.

Any fire → use /reflect

## 2. Park

0. Note what team position you are in, if any (e.g. swe1, architect, tmp)
1. Refresh `.branch-context.md` (Finished / Open / Next action / Resumes as)
2. Commit if changed (skip silently if `no-commit-primary-worktree.sh` blocks — surface the block to user)
3. Push if ahead of upstream

## 3. Respond
1. Print:
   ```
   Parked: <branch> @ <sha>
   Self-resume: /clear then /position <position> --resume
   ```
