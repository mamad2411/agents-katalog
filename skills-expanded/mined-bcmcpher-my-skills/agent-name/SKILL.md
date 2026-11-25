---
name: agent-name
description: When should the main Claude instance delegate to this agent? Be specific about the trigger condition and what outcome the agent produces.
tools: Read, Grep, Glob, Bash
model: inherit
permissionMode: default
maxTurns: 20
# isolation: worktree   # Uncomment to run agent in a temporary git worktree (isolated branch).
#                       # Use when the agent will make independent file changes that shouldn't
#                       # affect the main working tree. Worktree is cleaned up automatically
#                       # if no changes are made; otherwise the branch/path is returned.
---

You are a specialized assistant for [PURPOSE].

When invoked:
1. [Step one]
2. [Step two]
3. Return a concise summary of what you did and any output

Always [constraint]. Never [constraint].
