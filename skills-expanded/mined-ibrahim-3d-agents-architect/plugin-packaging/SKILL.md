---
name: plugin-packaging
description: Package a collection of skills/agents/commands/hooks as a distributable Claude Code plugin. Use when the user asks to "package this as a plugin", "create a plugin.json", "build a marketplace entry", "make this installable", "publish my plugin", "plugin manifest", "validate my plugin", or when bundling work for others to install via /plugin marketplace add. Covers plugin.json schema, marketplace.json, CLAUDE_PLUGIN_ROOT, userConfig, and validation.
---

# Plugin Packaging

Claude Code plugins are directory bundles installable via `claude plugin install <name>@<marketplace>` or `/plugin marketplace add <git-url-or-path>`.

## Required layout

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json          # manifest (only required file for a manifest-driven plugin)
│   └── marketplace.json     # if you're shipping a marketplace in this repo
├── skills/<name>/SKILL.md
├── commands/<ns>/<cmd>.md
├── agents/<agent>.md
├── hooks/hooks.json         # optional
├── .mcp.json                # optional
├── scripts/                 # helpers invoked by hooks/agents
├── bin/                     # binaries added to PATH inside the plugin sandbox
├── README.md
├── LICENSE
└── CHANGELOG.md
```

**Critical**: components must live at the plugin root, not inside `.claude-plugin/`.

## plugin.json minimum

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "…",
  "author": {"name": "…", "email": "…"},
  "license": "MIT"
}
```

If you follow default layout, Claude Code auto-discovers skills/agents/commands/hooks/MCPs. Only set `"skills"`, `"commands"`, `"agents"` keys if you use custom paths.

## Path substitution

- `${CLAUDE_PLUGIN_ROOT}` — absolute path to the plugin (changes on update; don't write persistent files here).
- `${CLAUDE_PLUGIN_DATA}` — `~/.claude/plugins/data/<id>/`, persists across updates. Use for caches, `node_modules`, venvs, generated state.

Use these in hook commands, MCP configs, and `@`-imports inside commands/agents/skills.

## marketplace.json

```json
{
  "name": "my-marketplace",
  "owner": {"name": "…"},
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./",
      "description": "…",
      "version": "0.1.0"
    }
  ]
}
```

`source` can be a local path or a git URL. Users install via `/plugin marketplace add <path-or-url>` then `claude plugin install my-plugin@my-marketplace`.

## userConfig (prompted at install)

```json
{
  "userConfig": {
    "api_token": {"description": "Your API token", "sensitive": true},
    "workspace_id": {"description": "Workspace ID", "sensitive": false}
  }
}
```

Non-sensitive values are substitutable as `${user_config.KEY}`; sensitive go to keychain. Exported as `CLAUDE_PLUGIN_OPTION_<KEY>` to subprocesses.

## Security constraints for plugin-shipped agents

`hooks`, `mcpServers`, `permissionMode` are NOT permitted in plugin agent frontmatter. Keep these at the plugin level only.

## Validation

```bash
claude plugin validate ./my-plugin
# or inside Claude Code:
/plugin validate
```

Checks manifest syntax, frontmatter on skills/agents/commands, hooks.json schema.

## Versioning

SemVer. Bump `version` in `plugin.json` on every public change — Claude Code caches by version; unchanged version = users don't see updates. Maintain `CHANGELOG.md`.

## References

- @../../agents-architect/references/plugin-manifest.md — full field reference
- @../../agents-architect/templates/plugin.json.template
- @../../agents-architect/templates/marketplace.json.template

## Output

When packaging:

1. Create `.claude-plugin/plugin.json` + optionally `marketplace.json`.
2. Verify layout (components at root, not in `.claude-plugin/`).
3. Run `claude plugin validate` and fix errors.
4. Write CHANGELOG entry + bump version.
5. Produce install instructions for README.
