---
name: follow-enter-dot
description: Handle the "." trigger: check state, then choose continue, commit/push, suggest, ship, or ask-me
argument-hint: "[scope]"
related:
  - continue
  - idea
  - idea-features
  - follow-your-suggestion
  - git-commit
  - git-push
  - git-commit-and-push
  - ship
  - dont-ask-me
  - ask-me
  - suggest-next-action
  - report-progress
  - report
  - save-to-todo-md

---

## Goal

Handle the `.` trigger from the user by inspecting the current state, then choosing the appropriate action: continue work, commit/push finished work, suggest next steps, ship the work, generate feature ideas, or ask the user

## Scope

Use when the user sends a message containing only `.` or uses `.` as a trigger to perform the next action based on the current state

## Execute

### 1. Read Current State

> Goal: know the current state before deciding

1. Check the current todo list (if any) — if a `[scope]` argument is given, limit the state check to that scope
2. Check open files, recent changes, git status
3. Check the user's latest message and context
4. Check whether this session has used `/ship` in `dont-ask-me` mode or `/dont-ask-me` — if so, keep `dont-ask-me` mode for every subsequent decision (replace `/ask-me` with `/follow-your-suggestion` + safe default)
5. Run `/report-progress` to summarize the current status

### 2. Determine Next Action

> Goal: choose the appropriate action

Choose by order of items 1-8 — the first item that matches the state wins

1. If there is pending work or unfinished todos → run `/continue`
2. If there are uncommitted changes whose work is done and validation passed → run `/git-commit-and-push` (commit + push + resolve CI/CD); if only a commit is needed without pushing → run `/git-commit`
3. If committed but there are still unpushed commits → run `/git-push`
4. If the work is ready to ship and validation passed → run `/ship` then follow with `/suggest-next-action`; but if the session is in `dont-ask-me` mode → run `/ship` in `dont-ask-me` mode
5. If guidance on direction or next steps is needed → run `/suggest-next-action` or `/follow-your-suggestion`
6. If the context indicates a need for feature ideas or brainstorming (e.g. previous messages mention "ideas", "features", or the user asks open-ended questions about features) → run `/idea-features`
7. If the context is unclear or needs an answer from the user → run `/ask-me`; but if the session is in `dont-ask-me` mode → run `/follow-your-suggestion` with a safe default instead
8. If the user indicates a specific intent (e.g. ship, continue, commit, push, ask) → do what the user wants

### 3. Execute Action

> Goal: carry out the chosen action

1. `/continue` — finish the pending work
2. `/git-commit-and-push` — commit + push finished work with CI/CD resolution
3. `/git-commit` — commit changes only (no push) when appropriate
4. `/git-push` — push the pending commits
5. `/ship` — deliver finished work, then run `/suggest-next-action` to recommend the next action
6. `/ship` (dont-ask-me mode) — ship without asking the user when the session is in `dont-ask-me` mode
7. `/suggest-next-action` — recommend the next step
8. `/idea-features` — generate feature ideas in chat when the context is about ideas
9. `/follow-your-suggestion` — follow the previously analyzed suggestion
10. `/ask-me` — ask the user when context is insufficient (except in `dont-ask-me` mode, where you use `/follow-your-suggestion` instead)
11. If the chosen action cannot be done (blocked, missing dependencies, or too risky) → run `/save-to-todo-md` to record the pending work first, then skip to the next action

### 4. Report

> Goal: summarize the action taken

1. Report the chosen action
2. Report the state that led to choosing that action
3. If committed/pushed → report the commit hash and remote state
4. If shipped → report the result summary
5. If continuing → report the next step taken

## Rules

- `.` is a trigger, not a full command
- Always check the state before deciding
- If the work is not finished → run `/continue` before `/git-commit-and-push` or `/ship`
- If commit/push or ship is needed → validation must pass first
- Never commit/push changes that are unfinished or failed validation
- If the session is in `dont-ask-me` mode → run `/ship` in `dont-ask-me` mode and keep the mode (replace `/ask-me` with `/follow-your-suggestion`)
- If the context is unclear → run `/ask-me` (except in `dont-ask-me` mode)
- Do not make risky changes without user confirmation (except in `dont-ask-me` mode, where you choose a safe default and report)
- Anything not yet doable → run `/save-to-todo-md` first, then skip; never leave pending work unrecorded

## Expected Outcome

- The user gets the action appropriate for the state
- Pending work is continued until complete
- Finished, validated work is committed/pushed via `/git-commit-and-push`, `/git-commit`, or `/git-push`
- Ready work is shipped per the standard, followed by `/suggest-next-action`, or shipped in `dont-ask-me` mode when the session is in that mode
- Feature ideas are generated with `/idea-features` when the context indicates
- Unclear context is asked about before starting, or decided with a safe default when in `dont-ask-me` mode
- Work that cannot be done yet is recorded in `/save-to-todo-md` before skipping, never silently lost
