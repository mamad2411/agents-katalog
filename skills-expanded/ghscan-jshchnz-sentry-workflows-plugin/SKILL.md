---
name: install-routines
description: Print the two ready-to-paste Claude Routine prompts (and matching `/schedule` commands) that wire the Sentry fix-issue and groom-stale workflows into cloud routines. Use when the user says "set up Sentry routines", "schedule Sentry workflows", or "how do I run this on a schedule".
---

# install-routines

The Sentry workflow skills run locally in Claude Code. To run them on a schedule, in CI, or in response to GitHub events, copy them into Claude Routines (cloud-hosted autonomous sessions).

This skill prints the two routine prompts and the `/schedule` commands you can run from any Claude Code CLI session.

## Prerequisites — verify these first

Before printing anything, check and report status of:

1. **Sentry connector on claude.ai.** Visit `https://claude.ai/customize/connectors`. The Sentry connector must be enabled so cloud routines can call the same `mcp__sentry__*` tools the plugin uses locally.
2. **GitHub connected.** Cloud routines need GitHub access to clone the target repo and open PRs. Run `/web-setup` if not already connected.
3. **The `jshchnz/sentry-workflows-plugin` repo (or a fork) is the one you want routines to clone**, so the skill bodies live in `.claude/skills/` of the cloned repo. If your routine should run inside *your own* application repo, copy `plugin/skills/` into your repo's `.claude/skills/` directory first and commit it.

## Print routine prompts

Print the contents of:

- `${CLAUDE_PLUGIN_ROOT}/routines/fix-issue.routine.md`
- `${CLAUDE_PLUGIN_ROOT}/routines/groom-stale.routine.md`

in fenced code blocks, prefixed by a short note: "These prompts are self-contained — they reference the Sentry MCP by tool name. Paste them into the **Instructions** box at https://claude.ai/code/routines, or use `/schedule` from the CLI as shown below."

## Scheduling

The web UI at https://claude.ai/code/routines is the easier path: paste the routine prompt, pick a repo, choose a schedule from a form.

If you prefer the CLI, the `/schedule` skill creates and manages cloud routines for you. After printing the routine prompts above, also print this guidance:

> "Run `/schedule` in any Claude Code session. The skill is conversational — say something like *'schedule the fix-issue Sentry routine weekdays at 9am'* and paste the routine prompt when it asks. For groom-stale, use *'weekly on Monday at 8am'*. The skill resolves the schedule into a cron expression and confirms before creating the routine."

Equivalent cron expressions, if you're managing routines yourself:

- `fix-issue`: `0 9 * * 1-5` (weekdays at 09:00)
- `groom-stale`: `0 8 * * 1` (Mondays at 08:00)

## GitHub-trigger variant

For users who want `fix-issue` to react to a `pull_request.opened` event (e.g. a labeled issue triggers an auto-fix attempt), print this variant of the fix-issue routine:

> "Set the GitHub trigger to `pull_request.opened` with label filter `sentry-fix`. The routine prompt remains identical — Claude will look at the Sentry issue ID in the PR body."

## Hard rules

- Never write to the user's filesystem from this skill — it is read + print only.
- Do not generate API tokens or write to `claude.ai/code/routines` programmatically. The user must create routines through the official UI or `/schedule`.
