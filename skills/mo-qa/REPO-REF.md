# Repo Referensi: momentic-ai/skills

Repo: https://github.com/momentic-ai/skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/momentic-ai_skills
API: curl "localhost:27126/repos/readme?name=momentic-ai_skills"
Dibuat: 2026-09-16

## Cuplikan README
# momentic-ai/skills

Source: https://github.com/momentic-ai/skills
Fetched: 2026-09-16

## README
# Momentic Agent Skills

Agent skills for [Momentic](https://momentic.ai), an end-to-end testing platform
for web and mobile apps.

The skills teach a coding agent how to write Momentic tests, run them, and fix
them when they break. The package also wires up the local Momentic MCP servers,
which are what let the agent drive a real browser or device while it works.

## Installation

### Momentic CLI (recommended)

The `momentic`, `momentic-mobile`, and `mo` CLIs ship these skills. Each CLI
installs the shared skills plus the one for its platform, with no network
fetch:

```shell
npx momentic skills
npx momentic-mobile skills
mo skills
```

Each command detects the coding agents on your machine and asks which ones to
set up. Pass `--yes` to skip the prompt. After you upgrade a CLI, it asks once
to reinstall the skills so they match the new version. `momentic init` and the
setup wizard offer the same step. See
[Skills](https://momentic.ai/docs/coding-agents/skills).

Use the options below if you want the plugin form, or a skill the CLIs do not
bundle (`momentic-result-classification`).

### Claude Code

Add this repository as a Claude Code marketplace, then install the Momentic
plugin:

```shell
/plugin marketplace add momentic-ai/skills
/plugin install momentic@momentic
```

The plugin installs all the skills and registers the local Momentic MCP servers.
Run `/mcp` in Claude Code to see which ones started.

### Cursor

Install the Momentic plugin from the Cursor Marketplace. Search for
**Momentic** under **Customize → Plugins**.

### Devin

Install the Devin plugin from this repository. It includes all the skills and
the local Momentic MCP servers.

### Other agents

Install the skills with the `skills` CLI if you do not use a Momentic CLI:

```shell
npx skills add momentic-ai/skills
```

This repository is also an Agent Plugins v1 package. The manifest is at
[`plugin.json`](plugin.json).

## MCP servers

The skills call MCP tools that run tests, inspect live pages, and splice steps
back into your YAML files. Those tools come from the Momentic CLIs over stdio, so
the servers run on your machine next to your project:

```json
{
  "mcpServers": {
    "momentic": {
      "command": "npx",
      "args": ["-y", "momentic", "mcp"]
    },
    "momentic-mobile": {
      "command": "npx",
      "args": ["-y", "momentic-mobile", "mcp"]
    }
  }
}
```

That is what `.mcp
