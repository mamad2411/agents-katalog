---
name: ga-pr
description: Kick off follow-up work on an existing PR in a parallel tmux/agent session. Use when the user asks to work on a PR, continue a branch, address PR feedback, or resolve merge conflicts in the background.
user-invocable: true
---

# ga-pr - Start Follow-up Work on an Existing PR

Kick off an agent task tied to an existing PR or branch. Reuses the existing tmux session/clone for that PR if one already exists.

## Steps

1. **Get the PR or branch and task** from the user's message.
   - Accept a PR number, PR URL, or branch name.
   - If the task is merge-conflict resolution, use `--merge-conflicts`.

2. **Run `ga-pr`**. Default harness is Pi, so omit the harness flag for normal use:
   ```bash
   ga-pr <pr-number-or-url-or-branch> "<task>"
   ```

   For merge conflicts:
   ```bash
   ga-pr --merge-conflicts <pr-number-or-url-or-branch>
   ```

   If the user explicitly asks for Claude Code, pass `--harness c`:
   ```bash
   ga-pr --harness c <pr-number-or-url-or-branch> "<task>"
   ```

3. **Report back** with the session, branch, and attach command printed by the script.

## Behavior

- Resolves PR inputs through `gh pr view`.
- Uses the same session naming convention as `ga`: `<repo>-<branch-slug>`.
- If a matching tmux session already exists, sends the task into that session instead of creating a duplicate.
- If the clone exists but the session does not, starts a new session in the existing clone.
- If neither exists, clones the repo, checks out the PR branch, and starts the agent.

## Rules

- Keep the task concise and direct.
- For conflict resolution, include that the agent should ask before making ambiguous choices.
- Do not use `/create-draft-pr`; this command is for updating an existing PR branch.
