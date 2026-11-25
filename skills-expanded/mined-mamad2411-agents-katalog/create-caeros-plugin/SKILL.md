---
name: create-caeros-plugin
description: Authoritative guide to scaffolding a Caeros plugin: directory layout, the full plugin.json manifest schema (capabilities, permissions, runtime, interface), skill and slash-command conventions, bundling MCP servers via .mcp.json, and compatibility with other plugin bundle formats. Use whenever creating, reviewing, or debugging a Caeros plugin.
---

# Creating a Caeros Plugin

A Caeros plugin is a directory (usually a git repo, or a folder inside one) containing a manifest plus capability folders. The loader reads the manifest, resolves every declared path safely under the plugin root, then fills in unset capabilities from layout conventions.

## Directory layout

```
my-plugin/
  .caeros-plugin/
    plugin.json          # the manifest (canonical location)
  skills/
    my-skill/
      SKILL.md           # one folder per skill
  commands/
    my-command.md        # one markdown file per slash command
  agents/                # optional sub-agent definitions
  .mcp.json              # optional bundled MCP servers
  hooks/
    hooks.json           # optional lifecycle hooks
  assets/
    logo.svg             # logo, screenshots, etc.
```

Manifest locations are checked in this order; the first hit wins:

1. `.caeros-plugin/plugin.json` (use this for new plugins)
2. `caeros-plugin.json` (bare fallback at the root)
3. `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `.claude-plugin/plugin.json` (compatibility, see below)

## Manifest schema (plugin.json)

Full shape with every supported field:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "One sentence about what the plugin does.",
  "keywords": ["search", "terms"],
  "capabilities": {
    "skills": "./skills",
    "mcpServers": "./.mcp.json",
    "apps": "./apps",
    "agents": "./agents",
    "workflows": "./workflows",
    "tools": "./tools",
    "commands": "./commands",
    "views": "./views",
    "hooks": ["./hooks/hooks.json"],
    "assets": "./assets"
  },
  "permissions": {
    "fs": ["."],
    "network": ["api.example.com"],
    "secrets": ["EXAMPLE_API_KEY"],
    "tools": ["web_*"],
    "exec": false
  },
  "runtime": "local",
  "interface": {
    "displayName": "My Plugin",
    "shortDescription": "Storefront one-liner.",
    "longDescription": "Full storefront description.",
    "developerName": "Your Name",
    "category": "Developer Tools",
    "capabilities": ["Read", "Write", "Interactive"],
    "websiteUrl": "https://example.com",
    "privacyPolicyUrl": "https://example.com/privacy",
    "termsOfServiceUrl": "https://example.com/terms",
    "defaultPrompt": ["try my plugin on this repo"],
    "brandColor": "#1b365d",
    "logo": "./assets/logo.svg",
    "composerIcon": "./assets/logo.svg",
    "screenshots": ["./assets/shot1.png"]
  }
}
```

Field rules, exactly as the loader implements them:

- **name**: falls back to the plugin directory name when unset.
- **capabilities**: each entry is a `./`-relative path (the `./` prefix is added if missing) to a directory or file for that surface. Paths are resolved under the plugin root; anything escaping the root via `..` or an absolute path is silently rejected (resolves to unset). Fields:
  - `skills`: directory of SKILL.md packs
  - `mcpServers`: path to the .mcp.json file
  - `apps`: directory of .app.json connectors
  - `agents`: sub-agent definitions directory
  - `workflows`: workflow scripts directory
  - `tools`: custom tool definitions directory
  - `commands`: slash commands directory
  - `views`: UI mini-apps directory
  - `hooks`: lifecycle hook files, accepts a single string or an array of strings
  - `assets`: logos, screenshots, other static files
- **permissions**: scopes the user grants on install and the runtime enforces at call time:
  - `fs`: filesystem path scopes (list of paths)
  - `network`: allowed hosts/domains (list)
  - `secrets`: secret keys the plugin may read (list)
  - `tools`: tool-name globs the plugin may call (list)
  - `exec`: boolean, whether the plugin may run shell commands
- **runtime**: `"local"` (default, anything unrecognized normalizes to local) or `"cloud"` (executed server-side via the Caeros gateway).
- **interface**: storefront presentation. `defaultPrompt` accepts a single string or an array. `logo`, `composerIcon`, and `screenshots` are `./`-relative paths resolved like capability paths. If every interface field is empty the block is treated as absent.

## Convention defaults (what you can omit)

After parsing, unset capabilities are filled from these conventions when the file or directory exists at the plugin root:

- `skills` defaults to `skills/`
- `commands` defaults to `commands/`
- `agents` defaults to `agents/`
- `mcpServers` defaults to `.mcp.json`, then `mcp.json`
- `hooks` defaults to `hooks/hooks.json`

So a minimal plugin is just a manifest with `name` plus a `skills/` folder. Declare paths explicitly anyway for first-party plugins: it documents intent and survives layout changes.

## Skills

Each skill is `skills/<skill-name>/SKILL.md` with YAML frontmatter:

```markdown
---
name: my-skill
description: What the skill covers and when the agent should load it. Make the "use when" part concrete: it is the trigger.
---

# My Skill

The body is reference material the agent reads when the skill triggers.
```

Keep the body factual and self-contained. Supporting files can live next to SKILL.md inside the skill folder.

## Slash commands

Each command is a markdown (or .txt) file in the commands directory:

```markdown
---
name: my-command
description: Shown in the command palette.
aliases: mc, my-cmd
---

The body is the prompt template the agent runs when the user types /my-command.
User arguments are appended after the body.
```

Parsing rules to know:

- `name` falls back to the filename without extension. Names are sanitized to lowercase `a-z`, `0-9`, `-`, `_`; anything else is stripped.
- `aliases` is a comma (or whitespace) separated list; surrounding brackets and quotes are tolerated.
- Built-in Caeros commands always win: a plugin command whose name or alias collides with a built-in is skipped, as is a duplicate of an earlier plugin's command.
- A command with an empty body is rejected at invocation time, so always ship a real prompt.
- Write bodies as complete, self-contained instructions: scope, steps, safety rails, and output format. Assume no other context.

## Bundled MCP servers (.mcp.json)

Shape:

```json
{
  "mcpServers": {
    "my-api": {
      "transport": "url",
      "url": "https://mcp.example.com/mcp"
    },
    "my-local-tool": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "my-mcp-server"]
    }
  }
}
```

Permission rules:

- A `url` transport server requires a matching host in `permissions.network` (e.g. `"network": ["mcp.example.com"]`), or its calls are blocked.
- A `stdio` transport server spawns a process, so it requires `"exec": true` in `permissions`.

Request the narrowest permissions that make the bundle work; users see and grant them at install.

## Compatibility with other bundle formats

Caeros also loads plugin bundles built for other harnesses unchanged, because their layouts are near-identical (manifest + skills + mcp config). Accepted manifest file names are `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, and `.claude-plugin/plugin.json`, and the convention defaults above (skills/, commands/, agents/, .mcp.json, hooks/hooks.json) mean such bundles work even when their manifests declare no paths at all. Codex-style manifests may also declare `skills`, `mcpServers`, `apps`, and `hooks` as top-level fields instead of inside `capabilities`; that fallback is honored when `capabilities` is absent. When authoring a new plugin, always use the Caeros manifest name and the explicit `capabilities` block.

## Checklist before shipping

1. `python3 -m json.tool .caeros-plugin/plugin.json` parses cleanly (same for .mcp.json if present).
2. Every declared capability path exists and is inside the plugin root.
3. Each SKILL.md has `name` and `description` frontmatter; each command file has a non-empty body.
4. Permissions cover exactly what the bundle needs (network hosts for url MCP servers, exec for stdio ones), nothing more.
5. An original logo at `assets/logo.svg`, referenced from `interface.logo`.
