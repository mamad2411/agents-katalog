---
name: ga
description: Kick off a new feature or fix in a parallel clone with Pi working autonomously. Takes a problem description, generates a concise branch name, runs ga to set up the worktree, and sends a crafted prompt to the new Pi session.
user-invocable: true
---

# ga - Start a New Task

Kick off a new parallel development task. Creates a clone, branch, tmux session, and starts Pi with a crafted prompt.

## Steps

1. **Get the task description** from the user's message. If unclear, ask what they want to build or fix.

2. **Generate a concise branch name** from the description:
   - Use lowercase kebab-case
   - Max 3-4 words, abbreviate aggressively
   - Prefix with `fix-` for bug fixes
   - Examples:
     - "the login button doesn't work on mobile" → `fix-mobile-login-btn`
     - "add a dark mode toggle to settings" → `dark-mode-toggle`
     - "search results are slow when filtering by date" → `fix-search-date-perf`
     - "implement rate limiting on the API" → `api-rate-limit`
     - "the sidebar collapses when resizing" → `fix-sidebar-resize`
     - "add webhook support for deployments" → `deploy-webhooks`

3. **Build the prompt** that Pi will receive in the new session. The prompt MUST follow this structure:

   ```
   <Clear description of the problem or feature>

   <Any relevant context: file paths, error messages, specific behavior>

   When you're done, run /create-draft-pr to commit, push, and open a draft PR.
   ```

   Keep the prompt direct and actionable. Don't over-explain. Include specific file paths or error details if the user mentioned them.

4. **Pick the harness**. Default is `pi`, so omit the flag for normal use. If the user's message explicitly asks for Claude Code (e.g. "use claude", "with claude", "claude harness"), pass `--harness c`.

5. **Run `ga` with the branch name, prompt, and base branch**. The `ga` function accepts a second argument for the prompt and a third for the base branch, which skips the fzf picker:
   ```bash
   ga <branch-name> "<prompt>" main
   # or explicitly with Claude Code:
   ga --harness c <branch-name> "<prompt>" main
   ```
   If `ga` is not found, source `~/.zshrc` first and then run it again, since in some environments `ga` is defined as a shell function rather than an executable.

6. **Report back** to the user with the branch name and tmux session name so they can attach:
   ```
   Started: <session-name>
   Branch: <branch-prefix>/<branch-name>
   Attach: tmux a -t <session-name>
   ```

## Rules

- Branch names must be short. 3-4 words max. Abbreviate (`btn`, `auth`, `cfg`, `nav`, `perf`, `err`, `msg`, `req`, `res`, `fmt`, `val`, `tmpl`, `env`, `deps`).
- Always include the `/create-draft-pr` instruction in the prompt.
- The prompt should be a single clear message, not a multi-step plan. Let Pi figure out the implementation.
- If the user provides file paths or error messages, include them verbatim in the prompt.
- Don't over-specify. Trust Pi to explore the codebase and find the right approach.
