---
name: follow-create-claude-plugin
description: Build a Claude Code plugin with manifest, skills, agents, hooks, and MCP servers
argument-hint: "[scope]"
related:
  - follow-create-sdk
  - update-devin-global-skills
  - update-devin
  - ask-me
  - search
  - follow-harness-engineering
  - deep-review-codebase

---

## Goal

Build a Claude Code plugin that can be installed and used with Claude Code, with a manifest, skills, agents, hooks, MCP servers, and slash commands following Claude's conventions

## Scope

For building a Claude Code plugin from scratch to extend Claude with custom skills, agents, hooks, MCP servers, or slash commands

- Supported components: skills, agents, hooks, commands, MCP (`.mcp.json`), LSP (`.lsp.json`), monitors (`monitors/monitors.json`), `bin/`, `settings.json` — always confirm the latest schema/docs with `/deep-research` + `/follow-best-practice` (never pinned in this file — per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: Verify the tech stack before building

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest plugin schema, then run `/deep-review-codebase` to summarize the tech stack
2. Record the reasons for choosing the stack/components as a reference for the next step (create claude plugin)

### 2. Gather Requirements

> Goal: Understand the plugin's purpose and components

1. Ask the user for the plugin name, goals, target users, and use case
2. Identify the needed components:
   - `skills/` for knowledge or user-initiated actions (preferred — invoked as `/plugin-name:skill-name`)
   - `agents/` for autonomous tasks
   - `hooks/` for event-driven automation (`hooks/hooks.json` + handler scripts)
   - `commands/` for slash commands (legacy — use `skills/` for new plugins)
   - `mcpServers` in `.mcp.json` for external service integration
   - `.lsp.json` for LSP servers (code intelligence)
   - `monitors/monitors.json` for background monitors (watch logs/files, then notify Claude)
   - `bin/` for executables added to the Bash tool's PATH
   - `settings.json` for default settings (`agent`, `subagentStatusLine`)
3. If unclear → use `/ask-me` to pick components

### 3. Create Plugin Structure

> Goal: Create the directory structure per Claude plugin conventions

1. Create a root directory named after the plugin — or run `claude plugin init <name>` to scaffold into `~/.claude/skills/<name>` (auto-loaded as `<name>@skills-dir`)
2. Create the `.claude-plugin/plugin.json` manifest with `name` (kebab-case, serves as the namespace) and `description`; `version`/`author` are optional but recommended
3. Create directories per the chosen components: `skills/`, `agents/`, `commands/`, `hooks/`, `monitors/`, `bin/`, `scripts/` — every component lives at the plugin root and must not be inside `.claude-plugin/` (which holds only `plugin.json`)
4. Create `.mcp.json`, `.lsp.json`, or `settings.json` at the root if those components exist
5. Use `${CLAUDE_PLUGIN_ROOT}` for portable paths in the manifest
6. If the plugin has a single skill → `SKILL.md` may sit at the root (its frontmatter `name` becomes the invocation name)

### 4. Implement Components

> Goal: Build each component per convention

1. For `skills/`: create `skills/<name>/SKILL.md` as a sub-unit per `/update-devin-global-skills` (use `$ARGUMENTS` to receive input)
2. For `agents/`: create `.md` agent definitions per the `/update-devin-global-subagents` standard
3. For `hooks/`: create `hooks.json` and handler scripts per hook types (pre/post tool use, stop, etc.)
4. For `commands/`: create `.md` files with frontmatter and instructions
5. For `mcpServers`: specify server name, transport, command, args, and env in `.mcp.json`
6. For `.lsp.json`: specify `command`, `args`, and `extensionToLanguage` per language key
7. For `monitors/`: create a `monitors.json` array with `name`, `command`, and `description` — each stdout line is delivered as a notification

### 5. Validate And Test

> Goal: Verify the plugin before use

1. Run `claude --plugin-dir <plugin-path>` to load the plugin in Claude Code (supports a directory, `.zip` archive, or folder-of-plugins; use `--plugin-url` for a hosted zip)
2. Run `/reload-plugins` in the session to pick up changes without restarting
3. Test skills via `/plugin-name:skill-name` and check the `/plugin` manager Errors tab
4. Run `claude plugin validate <plugin-path>` before submitting/distributing (`--strict` to fail on warnings)
5. Verify `plugin.json` has `name` (kebab-case — serves as the `/plugin-name:skill-name` namespace) and `description`; if `version` is set, users only receive updates when it is bumped
6. If there are agents/hooks → run `/deep-validate` on each agent `.md`/`hooks.json`

### 6. Document And Distribute

> Goal: Make the plugin ready to share

1. Create `README.md` describing purpose, components, setup, and usage
2. Update `AGENTS.md` if the plugin is part of the project's skills
3. Create `.gitignore` for sensitive files
4. To publish → for a marketplace use a `.claude-plugin/marketplace.json` catalog; public submissions go through the claude.ai admin-settings directory form or platform.claude.com/plugins/submit (approved plugins pin the commit SHA)

## Rules

- Follow the directory layout in `### 3` — every component at the plugin root, `.claude-plugin/` holds only `plugin.json`
- The `plugin.json` manifest must have `name`, `description`, and `version`
- Never hardcode secrets or credentials in plugin files
- Use environment variables for API keys and sensitive paths
- Create only the directories actually used
- Follow the `SKILL.md` format in `/update-devin-global-skills`

- Use /follow-create-sdk if needed
- Use /search-skills if needed
- Use /deep-review-codebase if needed

## Expected Outcome

- A Claude Code plugin with `plugin.json` and all chosen components in place
- The plugin loads in Claude Code via `--plugin-dir`
- Skills/agents/hooks/commands work as designed
- A `README.md` exists and the plugin is ready to distribute

## Guide

- `/deep-research` + `/follow-best-practice` — latest official docs/schema (never pinned in this file)
- `/update-devin-global-skills` — SKILL.md format
- `/update-devin-global-subagents` — AGENT.md format
- `/follow-harness-engineering` — hooks, agents, lifecycle
