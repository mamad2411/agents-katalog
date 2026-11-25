---
name: hermes-integration
description: >
  Self-improving agent integration via Hermes Agent. Creates skills from experience,
  improves them during use, and delivers CoreMind decisions via Telegram/Discord/Slack.
  Available as MCP server (hermes) for conversation management and skill orchestration.
  Use for multi-platform delivery, closed learning loops, and cron-scheduled tasks.
license: MIT
metadata:
  author: <your-name>
  version: "1.0.0"
  mcp_servers:
    - hermes
tags: [self-improving, multi-platform, skills, automation, mcp]
created: 2026-04-04
---

# Hermes Agent Integration

## Overview

Hermes Agent (Nous Research) is a self-improving personal AI agent with a closed
learning loop: use → skill creation → improvement → re-use. It's connected as an
MCP server (`hermes`) providing conversation management across platforms.

## MCP Server Tools (available after Claude Code restart)

The `hermes` MCP server exposes 10 tools:

| Tool | Purpose |
|------|---------|
| conversations_list | List active conversations across all platforms |
| conversation_get | Get details of a specific conversation |
| messages_read | Read message history from a conversation |
| messages_send | Send a message to a platform (Telegram, Discord, Slack, etc.) |
| events_poll | Poll for new events across platforms |
| events_wait | Wait for a specific event (blocking) |
| attachments_fetch | Fetch message attachments |
| permissions_list_open | List pending approval requests |
| permissions_respond | Approve or deny a permission request |
| channels_list | List available communication channels |

## When to Use

- **Multi-platform delivery**: Send CoreMind decisions to Telegram, Discord, or Slack
- **Self-improving skills**: Let Hermes create and refine skills from experience
- **Cron scheduling**: Schedule recurring tasks via `hermes cron`
- **Cross-session memory**: Hermes maintains its own user model (Honcho dialectic)
- **RL training data**: Generate trajectory data for fine-tuning models (Atropos)

## Integration with /plan

When `/plan` routes an AI or meta task:

1. Check if Hermes has created skills relevant to the current task
2. Use Hermes MCP to deliver status updates to configured platforms
3. For long-running autonomous tasks, schedule Hermes cron for periodic check-ins

## Integration with Council

When `/council` is invoked:

1. Council decisions can be delivered to Telegram/Discord via Hermes MCP `messages_send`
2. Hermes user model provides additional context about user preferences

## Quick Commands

```bash
# Interactive chat
source ~/.hermes/hermes-agent/.venv/bin/activate && hermes chat

# Check status of all components
hermes status

# List created skills
hermes skills list

# Set up Telegram delivery
hermes gateway add telegram

# Schedule a cron task
hermes cron add "0 9 * * *" "Check portfolio and send summary to Telegram"

# MCP server mode (used by Claude Code)
hermes mcp serve
```

## Agent Binding

Best-fit agents for Hermes integration:
- **ai-engineer** (L2): Manages self-improving skill loops
- **prompt-engineer** (L3): Optimizes Hermes skill prompts
- **workflow-optimizer** (L5): Integrates Hermes into automation pipelines
- **pm-agent** (L0): Uses Hermes for cross-platform status delivery
