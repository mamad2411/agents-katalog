---
name: setup
description: Configure Riven Analyst after installation in Claude Code. Use when the player needs an external vision endpoint, bounded web research, an installation scope, or one-time Riven MCP permissions.
---

# Riven Analyst Setup

Finish setup with one configuration decision and one permission confirmation. Never ask the
player to paste an API key into chat or write one into a repository file.

## Workflow

1. Identify the host, then confirm the install scope. Use `user` for all projects, `local` for this player on the current
   project, and `project` only when the repository should share the plugin configuration.
2. Configure the external OpenAI-compatible vision endpoint, model, Provider label, and API key.
3. On Claude Code, use Claude's native Riven Analyst plugin configuration dialog or the bundled
   `mcp-server/vision-config.html` helper. On Codex, use the host's
   MCP environment configuration for the documented `RIVEN_VISION_*` variables. Do not collect the key in prose.
   The current Claude project directory is the image root for the MCP vision adapter. For a screenshot
   elsewhere, let the host read that one folder temporarily or copy the screenshot into the project;
   do not create a persistent plugin directory setting or request a whole-drive grant.
4. Choose whether bounded web research is enabled. Explain that it is used only when the trusted
   local sample does not answer the current identity or recommendation question.
5. On Claude Code, preview the permission update with `scripts/configure_permissions.py --dry-run`. Show
   the target settings file and added rules, then ask for one confirmation. The narrowly scoped rules
   cover the Riven MCP tools, read-only access to this installed plugin's bundled references, and the
   selected web policy. After confirmation run the same command with `--apply`.
   Codex plugin MCP permissions do not use this Claude settings script.
6. Ask Claude Code to `/reload-plugins`, or start a new Codex task, after configuration changes. Report the chosen modes and
   permission scope without printing secrets.

## Permission command

Run the bundled script with the selected values:

```text
uv run --project "${CLAUDE_PLUGIN_ROOT}" --locked --no-dev python "${CLAUDE_PLUGIN_ROOT}/skills/setup/scripts/configure_permissions.py" --scope <user|local|project> --web-research <enabled|disabled> --dry-run
```

Replace `--dry-run` with `--apply` only after the player confirms. The script is idempotent and
adds only explicit read-only Riven tools plus optional web rules. Do not use a server-wide MCP
wildcard or `--dangerously-skip-permissions`.

Do not add a health-check ceremony. If setup fails, state the specific configuration field or
settings file that needs attention.
