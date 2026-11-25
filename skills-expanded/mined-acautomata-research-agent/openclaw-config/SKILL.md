---
name: openclaw-config
description: Complete OpenClaw agent and configuration management. Use when the user wants to create new agents, configure Telegram bots, set up message routing with bindings, manage multi-agent configurations, list current setup, or troubleshoot routing issues. Handles agent creation, binding management, and configuration based on official OpenClaw documentation.
---

# OpenClaw Config

Complete agent and configuration management for OpenClaw, with automatic binding setup and progressive documentation.

## Quick Start

### Create a new agent (one command)

```bash
python3 scripts/create_agent.py <agent-id> <agent-name> <bot-token> [workspace-path]
```

This automatically:
- ✅ Adds Telegram bot account
- ✅ Registers agent
- ✅ Configures binding (routing)
- ✅ Backs up configuration

Example:
```bash
python3 scripts/create_agent.py project-manager "项目管理助手" "YOUR_TELEGRAM_BOT_TOKEN"
```

**See [agent-creation.md](references/agent-creation.md) for complete agent creation guide.**

### Add a binding (routing rule)

```bash
python3 scripts/add_binding.py <agent-id> <channel> <account-id>
```

Example:
```bash
python3 scripts/add_binding.py project-manager telegram project-manager
```

For peer-specific routing (specific user/group/channel):
```bash
python3 scripts/add_binding.py family whatsapp personal --peer-kind group --peer-id "120363999@g.us"
```

**See [binding-management.md](references/binding-management.md) for complete binding guide.**

### View configuration

```bash
python3 scripts/list_config.py
```

Shows agents, bindings, and channel accounts.

## Core Concepts

### Agents
Isolated "brains" with their own workspace, sessions, and configuration.

### Bindings
Route messages to agents based on channel, account, and optionally peer (user/group/channel).

**Priority:** Peer > Guild > Team > Account > Channel > Default

### Channels
Communication platforms: telegram, whatsapp, discord, slack, etc.

## Common Workflows

### Create a complete agent setup

```bash
# 1. Create agent with automatic binding
python3 scripts/create_agent.py my-agent "My Assistant" "bot-token"

# 2. Create workspace
mkdir -p ~/.openclaw/workspace/my-agent

# 3. Add configuration files (use templates in assets/)
cp assets/SOUL.md.template ~/.openclaw/workspace/my-agent/SOUL.md
cp assets/AGENTS.md.template ~/.openclaw/workspace/my-agent/AGENTS.md
cp assets/USER.md.template ~/.openclaw/workspace/my-agent/USER.md

# 4. Edit templates (replace {{placeholders}})

# 5. Restart
openclaw gateway restart
```

### Route specific group to dedicated agent

```bash
# Add peer-specific binding (higher priority)
python3 scripts/add_binding.py family whatsapp personal --peer-kind group --peer-id "120363999@g.us"

# Add account-level binding (lower priority, catches everything else)
python3 scripts/add_binding.py main whatsapp personal
```

### Multiple Telegram bots → Multiple agents

```bash
python3 scripts/create_agent.py main "Main Assistant" "token1"
python3 scripts/create_agent.py work "Work Assistant" "token2"
python3 scripts/create_agent.py family "Family Assistant" "token3"
```

Each bot automatically routes to its agent.

## Official CLI Commands

OpenClaw provides built-in commands:

```bash
# Agent management
openclaw agents list
openclaw agents add <id> --workspace <path>
openclaw agents set-identity --agent <id> --name "Name"

# Configuration
openclaw config get agents.defaults.workspace
openclaw config set agents.list[0].workspace "/path"

# Gateway
openclaw gateway restart
openclaw gateway logs

# Diagnostics
openclaw doctor
```

**See [cli-reference.md](references/cli-reference.md) for complete CLI guide.**

## Configuration Templates

Templates in `assets/` directory:
- `SOUL.md.template` - Agent personality and behavior
- `AGENTS.md.template` - Agent role and responsibilities
- `USER.md.template` - User information and preferences

Replace placeholders:
- `{{agent_name}}` - Agent display name
- `{{agent_purpose}}` - Agent's main purpose
- `{{workspace_path}}` - Workspace directory path

## Troubleshooting

**Agent not responding:**
1. Check binding: `python3 scripts/list_config.py --bindings`
2. Verify agent exists: `python3 scripts/list_config.py --agents`
3. Check logs: `openclaw gateway logs`
4. Run diagnostics: `openclaw doctor`
5. Restart: `openclaw gateway restart`

**Config validation error:**
- Restore backup: `cp ~/.openclaw/openclaw.json.backup-* ~/.openclaw/openclaw.json`
- Run diagnostics: `openclaw doctor --fix`

**Wrong agent responding:**
- Check binding priority (peer > account > channel)
- Ensure more specific bindings come first
- Verify account IDs match

## Progressive Documentation

This skill uses progressive disclosure for efficient context usage:

**Core workflow (this file):**
- Quick start commands
- Common patterns
- Basic troubleshooting

**Detailed guides (references/):**
- [agent-creation.md](references/agent-creation.md) - Complete agent creation process
- [binding-management.md](references/binding-management.md) - Routing rules and scenarios
- [config-guide.md](references/config-guide.md) - Configuration schema and examples
- [cli-reference.md](references/cli-reference.md) - OpenClaw CLI commands

**When to read detailed guides:**
- **agent-creation.md** - When creating your first agent or troubleshooting creation
- **binding-management.md** - When setting up complex routing or debugging routing issues
- **config-guide.md** - When manually editing configuration or understanding structure
- **cli-reference.md** - When using OpenClaw CLI commands or automation

## Important Notes

### ❌ Don't use these fields (they don't exist)
- `agents.list[].channels`
- `channels.telegram.accounts[].agent`

### ✅ Use bindings instead
```json
{
  "bindings": [
    {
      "agentId": "project-manager",
      "match": {
        "channel": "telegram",
        "accountId": "project-manager"
      }
    }
  ]
}
```

### Configuration Validation
OpenClaw uses strict validation:
- Unknown keys → startup failure
- Type errors → rejected
- Invalid values → prevented

Always run `openclaw doctor` after manual config changes.

## Reference

Official OpenClaw documentation:
- Multi-agent: `docs/zh-CN/concepts/multi-agent.md`
- Configuration: `docs/zh-CN/gateway/configuration.md`
- Telegram: `docs/zh-CN/channels/telegram.md`
- CLI: `docs/zh-CN/cli/`

All paths relative to: `~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/`
