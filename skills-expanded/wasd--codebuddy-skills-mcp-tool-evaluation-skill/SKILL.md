---
name: mcp-tool-evaluation
description: Evaluate MCP servers and tool integrations for project use. Use when considering MCP Registry, filesystem/git/fetch/memory servers, Godot MCP, Playwright MCP, or new external tools.
license: MIT
compatibility: agent-skills
metadata:
  source: project-adapted from official MCP registry/reference server guidance and project security rules
---

# MCP Tool Evaluation

Use this skill before adding or recommending an MCP server or external tool integration.

## Evaluate Fit

- Does it solve an actual current project workflow gap?
- Is a built-in tool or existing `tools/*.py` script already enough?
- Does it work on Windows PowerShell and this repo layout?
- Does it require secrets, credentials, browsers, network access, or long-running daemons?
- Should config be project-level or user-level?

## Source Preference

- Official MCP Registry entries.
- Official/reference MCP servers for fetch, filesystem, git, memory, sequential thinking, and time.
- Mature community servers only after checking license, maintenance, install command, and permissions.
- Game-specific tools like Godot MCP are useful, but local paths such as `GODOT_PATH` should usually stay user-level.

## Security Rules

- Do not commit API tokens or personal paths.
- Avoid project-level MCP config that grants broad filesystem or network access by default.
- Prefer read-only/research servers unless the task explicitly needs writes.
- Document why the server is needed and how to disable it.

## Project Recommendations

- Godot MCP: useful for editor/scene operations, but keep local executable paths in user config.
- Fetch/search MCP: useful only if existing `webfetch` is insufficient.
- Git/filesystem MCP: usually redundant because OpenCode already has repo tools.
- Memory MCP: evaluate carefully; project already has explicit AI memory files.

## Output

Return one of: install now, user-level only, document for later, reject.
Include reason, config scope, expected commands, validation, and rollback path.
