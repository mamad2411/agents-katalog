# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is your project repository with an AI workspace layer built in. Your files (code, documents, resources, whatever you're working on) live here, and Claude tracks progress, decisions, and goals automatically alongside them.

This is a **starter** — Ace Level 1. It ships with the minimum scaffolding to get a small team or solo operator working with Claude on day one. Larger systems (multi-project portfolios, custom hooks, MCP-driven analytics) layer on top of this once you outgrow the basics.

## Workspace Structure

| Path | Purpose |
|------|---------|
| `CLAUDE.md` | This file — workspace context Claude reads on every session |
| `README.md` | Public-facing intro and quick start |
| `tasks-inbox.md` | Open list of work not yet tied to an initiative |
| `goals/` | YAML OKR system (created by `goals-onboarding`) |
| `goals-schema.md` | Reference spec for the OKR YAML format |
| `.claude/agents/` | Installed AI agents |
| `.claude/hooks/` | Python hooks (session-init, prompt-check) |
| `.claude/rules/` | Always-active behavioral rules |
| `.claude/settings.json` | Permission mode and hook wiring |
| `.vscode/` | Recommended VS Code extensions and workspace settings |
| `logs/temp/` | Real-time work capture (consolidated into session logs) |
| `logs/archive/` | Processed temp logs (excluded from search) |
| `level1.code-workspace` | VS Code workspace file — open this instead of `code .` |

## Project Locations

| Project | Location | Description |
|---------|----------|-------------|
| (this workspace) | `.` | Your work goes here. Add additional projects via `start-here` if you grow into a multi-repo setup. |

_If you add additional repos later, `start-here` will register them here and create tracking folders._

## Session Role

When working in this repo, Claude should:
- Help with project work (code, documents, planning, whatever the user needs)
- Track work automatically through temp logs and session logs
- Keep status and goals files updated as work progresses
- Surface active priorities and blockers when asked "what's the status"

## Reporting Structure

For each project (or for this single workspace):
- `status.md` — current priorities, active workstreams, blockers
- `goals/` — YAML OKR system (annual objectives, quarterly KRs, initiatives, tasks-inbox)
- `tasks-inbox.md` (root) — actionable items not yet tied to an initiative
- `logs/session-log-{YYYY-MM}.md` — monthly summary (consolidated by `session-logger`)

## Agents

Installed agents live in `.claude/agents/`. Read `.claude/agents/manifest.json` for the full inventory and which are default vs optional.

| Agent | Purpose | Trigger |
|-------|---------|---------|
| `system-overview` | Tour of how Ace works (philosophy + recap of Alfred's deck) before diving in | "intro", "how does this work", "explain the system" |
| `start-here` | First-run setup walk-through | "start here", "set me up" |
| `vscode-setup` | Configure VS Code: extensions, layout, permission layers | "set up VS Code" |
| `session-logger` | Consolidate temp logs into session logs | "consolidate my logs" |
| `workspace-sync` | Git operations through natural language | "save my work", "sync" |
| `status-reporter` | Project dashboard | "what's the status" |
| `calendar-audit` | Review calendar events, log outcomes (needs Google Workspace MCP) | "check my calendar" |
| `goals-onboarding` | Set up OKR YAML structure | "set up goals" |
| `goals-weekly-review` | Weekly KR actuals + CEO narrative email | "weekly review" |

## MCP Integrations

MCP servers are configured in `~/.claude.json` under the `mcpServers` key. The level-1 starter only requires one if you want calendar features:

| Server | Used By | Status |
|--------|---------|--------|
| Google Workspace | `calendar-audit` | Not set up — `start-here` walks you through it if you select calendar-audit |

## Temp Logging

**Every chat must log work as it happens.**

1. After completing any significant task or milestone, append an entry to a temp log file
2. File path: `logs/temp/{project}-{username}-{YYYY-MM-DD}.md`
   - `{username}` is the GitHub username (detected via `gh api user --jq '.login'`)
   - `{project}` defaults to `workspace` for single-project workspaces
3. Session-logger consolidates these into the official session log on demand or end of day

### Temp Log Format

```markdown
## HH:MM - [Brief description]
- What was done
- Key decisions or context
- Any blockers or next steps
```

## Working Guidelines

- Always read existing files before making modifications
- When updating documents, preserve existing information unless explicitly asked to remove it
- Use consistent formatting within document types
- Date-stamp entries where temporal context matters
- Never modify code without explicit permission from the user

## Permission Mode

This workspace ships with `defaultMode: bypassPermissions` in `.claude/settings.json` — Claude runs without confirmation prompts inside this repo. Review changes via `git diff` before pushing.

To switch to per-prompt confirmations, edit `.claude/settings.json` and remove the `defaultMode` line, or set it to `"default"`. See `vscode-setup` for the full breakdown of permission layers (Claude in VS Code vs Claude in terminal).

## Adding New Projects

When you have additional repos or projects to bring in:
1. Tell Claude — "I want to add a project at `~/code/my-app`"
2. Claude (via `start-here`) deploys workspace components into that repo (`.claude/`, a tailored CLAUDE.md)
3. Adds it to the Project Locations table here
4. Creates a tracking folder for it (status, goals, session log)
5. Updates the temp log project mapping above

This is how level-1 grows into a multi-project portfolio without ceremony.
