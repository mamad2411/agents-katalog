---
name: agent-plugin-setup
description: Initialize a VS Code agent plugin with directory structure, plugin.json manifest, and workspace configuration for multi-tool compatibility.
---

# Agent Plugin Setup

## Specialization

Bootstrap a new VS Code agent plugin with a properly structured directory hierarchy and manifest configuration. This is the first step before authoring any agent functionality.

## Supporting Activities

- Create directory structure following VS Code plugin conventions.
- Generate `plugin.json` manifest with required and optional metadata fields.
- Configure optional paths for skills, agents, hooks, and MCP servers.
- Validate manifest schema against official specifications.
- Generate workspace-level or user-level agent configuration if needed.

## Workflow

1. **Define plugin identity**: Obtain kebab-case name (lowercase letters, numbers, hyphens only; max 64 characters), version, author info.
2. **Choose plugin format**: Confirm Copilot format (`plugin.json` at root) unless targeting Claude or OpenPlugin ecosystems.
3. **Initialize directory scaffold**:
   ```
   my-plugin/
     plugin.json                # Plugin manifest (required)
     skills/                    # Skill directory (optional)
     agents/                    # Agent directory (optional)
     hooks.json                 # Hook config (optional)
     .mcp.json                  # MCP server defs (optional)
     scripts/                   # Hook scripts (optional)
     .gitignore
     README.md
   ```
4. **Author `plugin.json`** with metadata:
   - Required: `name` (kebab-case, no slashes or colons)
   - Optional: `description`, `version` (semver), `author` (name, email, url), `skills`, `agents`, `hooks`, `mcpServers`
5. **Validate manifest** using the official [plugin.json schema](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson).
6. **Create placeholder files** for each component (skills/, agents/, .mcp.json) if planned.
7. **Initialize version control**: Create `.gitignore` with `node_modules/`, `.env`, build artifacts.
8. **Add README** with plugin purpose, installation instructions, and minimal example.

## Inputs

- Plugin name, description, and version (semver).
- Author name, email (optional), URL (optional).
- List of components to scaffold: skills, agents, hooks, MCP servers.
- Target path for plugin directory.
- Optional: Cross-tool compatibility requirement (Claude, OpenPlugin, Copilot, or multi-tool).

## Required Outputs

- Complete directory scaffold on disk.
- Valid `plugin.json` manifest.
- Optional component directories (skills/, agents/, .mcp.json) if specified.
- README.md with installation and usage guidance.
- .gitignore for source control.
- Success confirmation: plugin loads in VS Code without manifest errors.

## Done Criteria

- Directory structure follows VS Code plugin conventions.
- `plugin.json` validates against official schema.
- `name` field uses only lowercase letters, numbers, hyphens (no slashes, colons, or namespace prefixes).
- `version` uses semantic versioning (MAJOR.MINOR.PATCH).
- Placeholder directories created for each component type.
- README includes plugin description and example usage.
- Plugin is discoverable in VS Code with `Chat: List Plugins` or equivalent.
- Version control is configured (`.gitignore` present, not in tree).

## Validation Checklist

- [ ] Plugin name is kebab-case and max 64 characters.
- [ ] `plugin.json` is at plugin root (Copilot format) or `.plugin/plugin.json` (OpenPlugin format).
- [ ] `description` is clear and max 1024 characters.
- [ ] `version` follows semver (e.g., 1.0.0, 0.2.1-beta).
- [ ] `author.name` is required; `email` and `url` are optional.
- [ ] `skills`, `agents`, `hooks`, `mcpServers` paths are relative to plugin root.
- [ ] No hardcoded secrets or credentials in any file.
- [ ] README includes minimal working example (e.g., `/run-tests` slash command if applicable).
- [ ] `.gitignore` includes `node_modules/`, `.env`, build outputs.
- [ ] Plugin loads without errors in VS Code via `Chat: Install Plugin From Source`.

## References

- [VS Code Agent Plugins Documentation](https://code.visualstudio.com/docs/copilot/customization/agent-plugins)
- [plugin.json Schema Reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#pluginjson)
- [Cross-tool Compatibility Guide](https://code.visualstudio.com/docs/copilot/customization/agent-plugins#_cross-tool-compatibility)
- [GitHub Copilot CLI Plugin Reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference)

## Trigger Conditions

Invoke this skill when any of the following is true:

- A new agent plugin is being created from scratch.
- Plugin directory structure must be scaffolded with manifest initialization.
- A plugin is being prepared for distribution (Marketplace, GitHub, private registry).
- Cross-tool compatibility (VS Code, Copilot CLI, Claude Code) must be enabled from the start.
