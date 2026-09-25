# Repo Referensi: railwayapp/railway-skills

Repo: https://github.com/railwayapp/railway-skills
Ref lokal: /Users/chaali0324/.agents/repo-refs/railwayapp_railway-skills
API: curl "localhost:27126/repos/readme?name=railwayapp_railway-skills"
Dibuat: 2026-09-16

## Cuplikan README
# railwayapp/railway-skills

Source: https://github.com/railwayapp/railway-skills
Fetched: 2026-09-16

## README
# Railway Skills

Agent skills for [Railway](https://railway.com), following the [Agent Skills](https://agentskills.io) format. 

This repository also includes Railway plugin packaging for ChatGPT, OpenAI Codex,
Claude Code, Grok Build, and Cursor. Each plugin package includes the
`use-railway` Agent Skill and Railway's hosted MCP server. Railway is also
available as a connector for Claude.


## Railway agent setup

To install the Railway CLI and configure agent support, run:

```bash
curl -fsSL agents.railway.com | sh
```

This installs the Railway CLI and skills, configures the Railway MCP server for
detected tools, and checks Railway authentication. If you are not authenticated,
run:

```bash
railway login
```

If the Railway CLI is already installed, configure agent support directly:

```bash
railway setup agent
```

## Installing Railway integrations

### ChatGPT and OpenAI Codex

Install the official [Railway plugin for ChatGPT and
Codex](https://chatgpt.com/plugins/plugin_asdk_app_6a502589384081919c5decf93496c9d1)
from the shared plugin directory. The plugin includes the `use-railway` skill
and Railway's hosted MCP server. Connect your Railway account when prompted,
then start a new chat or task to use the plugin.

To install the version published by this repository directly, add this GitHub
repository as a Codex marketplace:

1. Open Codex.
2. Select **Plugins** in the sidebar.
3. Open the **More** dropdown.
4. Click **Add more**.
5. Enter [`railwayapp/railway-skills`](https://github.com/railwayapp/railway-skills) as the marketplace source.

- Plugin manifest: [`plugins/railway/.codex-plugin/plugin.json`](plugins/railway/.codex-plugin/plugin.json)
- Marketplace: [`.agents/plugins/marketplace.json`](.agents/plugins/marketplace.json)

### Claude

Add the official [Railway connector for
Claude](https://claude.ai/directory/connectors/railway) from Claude's connector
directory. The connector uses Railway's hosted MCP server and OAuth, so it
doesn't require the Railway CLI.

For terminal-based workflows with Railway's agent skill and hooks, install the
Claude Code plugin.

### Claude Code

The official Anthropic marketplace is available in Claude Code by default.
Install Railway and reload plugins:

```text
/plugin install railway@claude-plugins-official
/reload-plugins
```

You can also run `/plugin` and select the **Discover** tab to browse 
