---
name: follow-create-codex-plugin
description: Create a Codex plugin with manifest, skills, MCP servers, app wiring, and marketplace publishing
argument-hint: "[scope]"
related:
  - ask-me
  - deep-review-codebase
  - follow-create-plugins
  - follow-create-sdk
  - follow-harness-engineering
  - search
  - update-devin-global-skills
  - update-devin
  - report

---
## Goal

Build a Codex (ChatGPT Work / OpenAI Codex) plugin that can be installed and used in ChatGPT or Codex, with manifest, skills, MCP servers, app wiring, and lifecycle hooks

## Scope

Used to create a Codex plugin from scratch to extend ChatGPT Work and Codex with custom skills, MCP tools, and apps

- Format: portable Agent Plugins — root `plugin.json` + `mcp.json` + `skills/` + `extensions.com.openai`; `.codex-plugin/plugin.json` is a compatibility fallback — always confirm the latest schema via `/deep-research` + `/follow-best-practice` (Codex CLI 0.x may break — no version pins in this file, per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before building

1. Run `/deep-review-codebase` to summarize the tech stack in use
2. Run `/deep-review-codebase` to review tech stack, dependencies, and library design (create codex plugin)
3. Record the rationale for the chosen stack and libraries for future reference (create codex plugin)

### 2. Gather Requirements

> Goal: understand the plugin's purpose and components

1. Ask the user for the plugin name, goal, target users, and use case
2. Identify the needed components:
   - `skills/<name>/SKILL.md` for reusable workflows (auto-discovered from root `skills/`)
   - root `mcp.json` for bundled MCP servers (portable schema — specify transport `type`)
   - `.app.json` for a registered app/MCP connection (`plugin_asdk_app...` ID)
   - `hooks/hooks.json` for lifecycle events (default discovery — override via `extensions.com.openai.hooks`)
   - `assets/` for icons, logo, screenshots
3. If unclear → use `/ask-me` to pick components

### 3. Create Plugin Structure

> Goal: build the directory structure per the portable Agent Plugins convention

1. Create a root directory named after the plugin — or use `@plugin-creator` (ChatGPT Work) / `$plugin-creator` (Codex CLI) to scaffold the `.codex-plugin/plugin.json` compat layout
2. Create root `plugin.json` with `"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"`, `name` (kebab-case), `version`, `description`, `author`, `license`, `keywords`, `homepage`, `repository`
3. Create `skills/` if there are skills (no need to declare the `skills` field — auto-discovered)
4. Create `mcp.json` if there is a bundled MCP server (declare `"$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"` and a transport `type` such as `streamable-http`)
5. Create `.app.json` when connecting to a registered MCP server/app
6. Add `extensions.com.openai` in the root manifest for `apps`, `hooks`, `interface` — if using `.codex-plugin/plugin.json` (compat), declare `apps`/`hooks`/`interface` there instead (never use both — the inline extension overrides the whole overlay, it does not merge)

### 4. Implement Components

> Goal: build each component per convention

1. For `skills/`: create `skills/<name>/SKILL.md` per `/update-devin-global-skills`
2. For `mcp.json`: declare named entries in `mcpServers` with transport `type` (`streamable-http` + `url` for remote)
3. For `.app.json`: reference the `plugin_asdk_app...` ID registered in ChatGPT developer mode
4. Define `interface` under `extensions.com.openai` for `displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `capabilities`, `defaultPrompt`, `brandColor`, `composerIcon`, `logo`, `screenshots`
5. For hooks: create `hooks/hooks.json` (discovered by default) or point a path via `extensions.com.openai.hooks` — hook commands receive env `PLUGIN_ROOT` and `PLUGIN_DATA`

### 5. Register And Test

> Goal: verify the plugin in ChatGPT/Codex

1. Open ChatGPT → Settings → Security and login → Developer mode; if there is an MCP server → register at chatgpt.com/plugins, then copy the `plugin_asdk_app...` ID
2. Create a local marketplace: repo → `$REPO_ROOT/.agents/plugins/marketplace.json`, personal → `~/.agents/plugins/marketplace.json` (entries must have `source.path` starting with `./`, `policy.installation`, `policy.authentication`, `category`)
3. Or use `codex plugin marketplace add <source>` (GitHub shorthand, git URL, or local path; `list`/`upgrade`/`remove` to manage)
4. Restart the ChatGPT desktop app → install the plugin from the Plugins Directory (choose the marketplace source)
5. Enable/disable per repo via `.codex/config.toml` `[plugins."name@marketplace"] enabled = true`
6. Open a Work chat, type `@` to select the plugin, and test the tools/skills

### 6. Document And Distribute

> Goal: the plugin is ready to share

1. Create `README.md` describing purpose, components, setup, and usage
2. Update `AGENTS.md` if the plugin is part of the project's skills
3. Create `.gitignore` for sensitive files
4. If publishing → follow the OpenAI plugin marketplace / workspace marketplace guidelines

## Rules

- Use the directory layout from `### 3` — portable `plugin.json`, `mcp.json`, `skills/` live at the plugin root only; `.mcp.json` (dotfile, no `type`) is a legacy format — never rename it into `mcp.json`
- The `plugin.json` manifest must have `$schema` (agent-plugins 1.0.0), `name`, `description`; `version`/`author` recommended
- Paths in `extensions.com.openai` must start with `./`, relative to the plugin root, and stay within the root
- Never hardcode secrets or credentials in plugin files
- Use environment variables for API keys and app IDs
- Create only the components actually used
- Use the `SKILL.md` format per `/update-devin-global-skills`
- Plugin-bundled hooks are non-managed — Codex skips them until the user trusts the hook definition

- Use /deep-review-codebase if needed
- Use /follow-create-sdk if needed
- Use /search-skills if needed
- Use /report if needed
- Use /follow-create-plugins if needed


## Expected Outcome

- A Codex plugin with a portable `plugin.json` (or `.codex-plugin/plugin.json` compat) and all chosen components in place
- The plugin installs via a local/personal marketplace in the ChatGPT desktop app or Codex
- Skills/MCP tools work as designed
- Has a `README.md` and is ready to distribute

## Guide

- `/deep-research` + `/follow-best-practice` — latest official docs/schema (no pins in this file)
- `/update-devin-global-skills` — SKILL.md format
- `/update-devin-global-subagents` — AGENT.md format
- `/follow-harness-engineering` — hooks, agents, lifecycle
- `/follow-create-claude-plugin` — if the plugin should later be ported to Claude
