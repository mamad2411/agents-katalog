---
name: which-pr
description: Report which PR is being worked on in the current conversation. Use when asked about the current PR context.
---

# Which PR

Report which PR is being worked on in the current conversation.

## Usage

Look through the conversation history for any PR numbers, branch names, worktree
paths, or `gh pr` output that was discussed. Report:

- PR number and title
- URL
- Branch name
- Worktree path (if applicable)

Do NOT run any git or gh commands. The answer must come entirely from
conversation context. This avoids interfering with worktrees or switching
branches in other active sessions.

If no PR has been discussed in this conversation, say so.

Keep the output short and direct.
