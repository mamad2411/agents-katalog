---
name: context-save
description: Save working context, git state, decisions, and remaining work so a future Codex session can resume cleanly.
---

# Context Save

Use this skill when the user asks to save progress, save state, checkpoint the work, or preserve context for later.

Upstream GStack renamed this from `checkpoint` because some hosts use checkpoint as a native rewind command. In this repo, `checkpoint` remains as a compatibility skill, while `context-save` is the current upstream-aligned name.

## Workflow

1. Capture repository state:
   - current branch
   - `git status --short`
   - recent commits relevant to the task
   - files changed by the current session
2. Capture working memory:
   - user goal
   - decisions made
   - blockers or assumptions
   - exact next steps
3. Prefer durable local artifacts:
   - use `reports` when the output is a timestamped report
   - use `capture` or `brain-ops` when the output should become brain memory
   - use `checkpoint` only as the legacy compatibility path
4. Keep the saved context concise enough for a future session to read quickly.

## Guardrails

- Do not claim work is committed, pushed, or installed unless that actually happened.
- Do not include secrets or credentials.
- Do not overwrite a prior saved context without preserving what changed.
