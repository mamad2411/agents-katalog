---
name: follow-create-devin-plugin
description: Create a Devin CLI plugin bundling skills, rules, agents, hooks, and MCP servers
argument-hint: "[plugin-name]"
related:
  - follow-create-sdk
  - update-devin-global-skills
  - update-devin
  - deep-review-codebase
  - ship
  - update-references

---
## Goal

Create a Devin CLI plugin that bundles skills, rules, agents, hooks, and MCP servers per the Devin CLI plugins documentation standard

## Scope

Use for creating a new plugin or improving an existing one so it can be installed and shared via GitHub repo, git URL, or local folder

- Devin CLI is not published on npm (the `devin` npm package = unrelated stub) — check the version with `devin --version`; always confirm the latest docs/format with `/deep-research` + `/follow-best-practice` (per `/update-devin-global-skills`)

## Execute

### 1. Review Tech Stack

> Goal: verify the tech stack before creating

1. Run `/deep-research` + `/follow-best-practice` to confirm the plugin format and latest docs at https://docs.devin.ai , then run `/deep-review-codebase` to summarize the tech stack
2. Record the rationale for the chosen stack and libraries for future reference (create devin plugins)
3. Record the rationale for the chosen stack and libraries for future reference (create devin plugins)

### 2. Plan Plugin Scope

> Goal: plan what the plugin does

1. Identify the problem the plugin solves or the gap it fills
2. Give the plugin a unique, meaningful name
3. Decide which skill types the plugin bundles: review, setup, architecture, tools
4. Identify target consumers: project, team, or public
5. Check that the name doesn't duplicate already installed plugins

### 3. Create Plugin Directory

> Goal: create the plugin structure

1. Create the root directory `<plugin-name>/`
2. Create `.devin-plugin/plugin.json` for the manifest
3. Create `skills/` and the sub-skills per `/update-devin-global-skills`
4. Create `AGENTS.md` if always-on rules are wanted
5. Create `rules/` if triggered rules are wanted
6. Create `agents/` if custom subagents are wanted
7. Create `hooks.json` if lifecycle hooks are wanted
8. Create `.mcp.json` (or `mcp_config.json`, which is equally supported) if MCP servers are wanted

### 4. Write Plugin Manifest

> Goal: write `.devin-plugin/plugin.json`

1. Set a unique `name` (required) as the namespace for `/<name>:<skill>`
2. Set `version` per semantic versioning
3. Set a concise `description`
4. Set `author` in the `{ name, email }` form
5. Add `homepage`, `repository`, `license`, `keywords` if available
6. Specify the `skills` path if the skill directories aren't in the default `skills/`
7. Specify `mcpServers` if there are MCP servers
8. Specify `requiredPlugins`, `optionalPlugins`, `forbiddenPlugins` per the governance policy

### 5. Create Skills

> Goal: create skills inside the plugin

1. Follow `/update-devin-global-skills` for each skill
2. Place `SKILL.md` at `skills/<skill-name>/SKILL.md`
3. Check that skill names are unique within the plugin
4. Test invocation with `/<plugin-name>:<skill-name>`

### 6. Add Rules And Agents

> Goal: add rules and custom subagents if needed

1. Write `AGENTS.md` as an always-on rule if wanted
2. Create `rules/<rule-name>.md` for triggered rules with a `trigger` frontmatter
3. Create `agents/<agent-name>.md` or `agents/<agent-name>/AGENT.md` for custom subagents
4. Note that agents load only in local Devin agents (CLI and Devin Desktop)

### 7. Add Hooks And MCP

> Goal: add lifecycle hooks and MCP servers

1. Create `hooks.json` for lifecycle hooks if needed
2. Create `.mcp.json` for MCP servers with an `mcpServers` map (`mcp_config.json` is still supported, but `.mcp.json` is the current convention)
3. Check that MCP servers don't expose secrets in the plugin repository

### 8. Test Plugin Locally

> Goal: test the plugin before publishing

1. Run `devin plugins install ./<plugin-name>` from the local path
2. Run `devin plugins list` to confirm the installation succeeded
3. Run `devin plugins info <plugin-name>` to see skills and dependencies
4. Test invoking a skill with `/<plugin-name>:<skill-name>`
5. Edit a skill and retest without `update`, since the local plugin is linked

### 9. Publish And Manage

> Goal: publish the plugin and manage versions

1. Push the plugin repository to GitHub or a git host
2. Install from remote with `devin plugins install owner/repo`
3. Run `devin plugins update <plugin-name>` when there are changes
4. Run `devin plugins remove <plugin-name>` to uninstall
5. Run `devin plugins prune` to clean up requirements from removed repos and unused plugin content
6. Run `/update-references` if any project references the plugin

### 10. Ship

> Goal: deliver the work

1. Run `/ship`
2. If `ship` fails → report the status

## Rules

### 1. Plugin Structure

- `.devin-plugin/plugin.json` is required and must have a unique `name`
- `skills/` holds skill files per `/update-devin-global-skills`
- `AGENTS.md` optional for always-on rules
- `rules/` optional for triggered rules
- `agents/` optional for custom subagents (local only)
- `hooks.json` optional for lifecycle hooks
- `.mcp.json` (or `mcp_config.json`) optional for MCP servers
- Devin also supports other plugin formats with manifest precedence `.devin-plugin/plugin.json` > `.claude-plugin/plugin.json` > root `plugin.json` (Agent Plugins 1.0.0 spec)

### 2. Manifest Fields

- `name` must be unique among installed plugins
- `version` uses semantic versioning
- `description` is concise
- `author` uses `{ name, email }`
- `requiredPlugins` for dependencies that must be auto-installed
- `optionalPlugins` for allow-list endorsements
- `forbiddenPlugins` for the deny-list and glob patterns
- `skills` specifies a path if not under `skills/`
- `mcpServers` specifies a path or an inline map

### 3. Dependency Governance

- deny wins: a plugin is blocked if anyone forbids it
- self-override: a plugin's own manifest is exempt from its own forbidden list
- no cross-scope re-permitting: one plugin can't override another plugin's forbidden list
- if a required plugin is blocked, the whole plugin install fails

### 4. Safety And Security

- never put secrets or credentials in `mcp_config.json` or skill files
- don't use `*` in `forbiddenPlugins` without declaring the needed `optionalPlugins` or `requiredPlugins`
- review skill permissions before bundling them into the plugin
- local path dependencies must be trusted paths

### 5. Versioning And Release

- use semantic versioning in `plugin.json`
- update `version` on breaking changes
- declare `license` when publishing publicly
- maintain backward compatibility unless a major version bump is justified

- Use /follow-create-sdk when needed
- Use /update-devin-global-subagents when needed

## Expected Outcome

- The plugin directory is created correctly per the Devin CLI spec
- `plugin.json` is valid and has a unique `name`
- Skills work and are invoked with `/<plugin>:<skill>`
- Rules, agents, hooks, MCP are declared correctly (if present)
- The plugin installs from both local and remote sources
- Dependencies and governance are clear

