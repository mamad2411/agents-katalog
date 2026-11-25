---
name: orc-gateway
description: "Use when setting up or using ORC's Telegram/Slack gateway: routing messages to live Claude/Codex/Cursor sessions, remote approval and monitoring of agent work, bot commands, or voice messages."
allowed-tools: mcp__orc__context mcp__orc__task_list
---

# ORC Gateway

The gateway bridges messaging platforms (Telegram, Slack) with live AI agent sessions. Approve work, trigger jobs, and chat with agents from your phone.

## Why

Without the gateway, HITL review requires the human at their terminal. The gateway lets you approve tasks, monitor agents, and start new agent sessions from Telegram or Slack. It also receives notifications from the agent loop when tasks need review.

---

## Setup

```bash
orc daemon start       # Starts API + scheduler + gateway
orc gateway status     # Check health
```

Config in `~/.orc/config.json`:

```json
{
  "gateway": {
    "telegram": {
      "enabled": true,
      "token": "BOT_TOKEN",
      "authorized_users": [123456789]
    },
    "slack": {
      "enabled": true,
      "bot_token": "xoxb-...",
      "app_token": "xapp-..."
    }
  }
}
```

---

## Chat Modes

Each chat has a mode: `direct` (ORC commands), `agent:claude`/`agent:codex`/`agent:cursor` (live session), or `job:<name>` (bridge-msg). Switch with `/mode` or `/agent <backend>`.

## HITL Review

Human review gates send notifications; agent reviewer nodes do not page the human
for every round. For a managed flow resolve the declared human outcome through the
dashboard gate or `orc flow resume`. The commands below apply to manual task review:

```
/tasks            # See tasks awaiting review
/task <id>        # View task details and worker summary
/approve <id>     # Approve - task moves to done
/reject <id>      # Request changes - task moves to changes_requested
```

The agent loop automatically resumes workers when tasks move to `changes_requested`.

## Live Agent Sessions

```
/agent claude → type task → Claude responds with streaming output
→ Permission prompts appear as inline keyboard buttons → Tap Allow/Deny
```

## Voice

Telegram voice messages are transcribed and sent to the agent. Responses are converted to TTS voice replies. Configure `speech`/`tts` providers in config (openai, groq, qwen).

---

## Bot Commands (direct mode)

```
/tasks, /task <id>, /approve <id>, /reject <id>    - Task management
/jobs, /run <name>                                   - Job management
/mem [list] [query], /mem show <name>, /mem add     - Project memories
/agent <backend>, /sessions, /session stop           - Agent sessions
/status, /mode, /help                                - Status
```

---

## Common Mistakes

| Mistake                          | Fix                                                          |
| -------------------------------- | ------------------------------------------------------------ |
| No review notifications arriving | Check `authorized_users` includes your Telegram ID           |
| Agent session won't start        | Need `orc daemon start`, not just `orc api`                  |
| Messages going nowhere           | Check `/mode` - may be `direct` when you need `agent:claude` |

---

## Related

- **orc-tasks** skill - task lifecycle, HITL review patterns
- **orc-session** skill - session management for live agent sessions
- Built-in skills: workers spawned via `/agent` or the task loop follow skills like `orc-worker-base` and `orc-coder` - use `skill_list` to discover
