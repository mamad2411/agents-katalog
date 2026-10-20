---
name: start-hermes-dev-agents
description: "QUICK-START: Launch the 5 Hermes Dev Team agents (dev-lead, skills-lead, integration-lead, qa-lead, docs-lead) on Spacebar. For the full class-level guide including channel creation, profile wiring, and SOUL.md patterns, load `self-hosted-communication-server` instead."
version: 1.2.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes dev team, spacebar, gateway, agents]
    triggers: [hermes dev team, spacebar-gateway, start-agents, dev-lead, skills-lead, integration-lead, qa-lead, docs-lead]
    related_skills: [self-hosted-communication-server, agent-fleet-deploy]
    note: "OVERLAPS with self-hosted-communication-server. Consolidation candidate — absorbed pattern into that skill's references/hermes dev team.md"
---

# Start Hermes Dev Team Agents on Spacebar

> **⚠️ This skill overlaps with `self-hosted-communication-server`.**
> The full build + launch workflow is documented there. This skill is a quick-start card for relaunching the existing 5 agents.

## Prerequisites

- Profiles exist at `~/AppData/Local/hermes/profiles/{dev-lead,skills-lead,integration-lead,qa-lead,docs-lead}/`
- Each has `config.yaml`, `.env` (with `DISCORD_BOT_TOKEN`), `.env.spacebar` (with channel), `SOUL.md`
- Spacebar running at `wss://discy.your-domain.example/`
- **Spacebar-specific config** applied (see `self-hosted-communication-server/references/spacebar-gateway-config.md`):
  - `discord.auto_thread: false` in config.yaml or `DISCORD_AUTO_THREAD=false` in .env
  - `GATEWAY_ALLOW_ALL_USERS=true` in .env (or your user ID in `DISCORD_ALLOWED_USERS`)

## Launch (Recommended: Fleet Manager)

The Fleet Manager is the recommended production deployment — bulletproof auto-restart, health checking, and rotating logs:

```bash
# Start with the fleet manager (all 5 bots in one process):
${HERMES_HOME}/hermes-agent/venv/Scripts/python.exe \
  ${MY_REPOS}/agent-fleet/scripts/spacebar-fleet-manager.py
```

Or double-click `start-spacebar-fleet.bat` in the agent-fleet repo.

The fleet manager handles: subprocess launch, 15s watchdog, auto-restart with exponential backoff, REST health checks, rotating log to `~/.hermes/logs/fleet-manager.log`.

## Launch (Manual — per bot)

```bash
cd ${MY_REPOS}/agent-fleet/scripts && \
source ${MY_REPOS}/agent-fleet/.env.spacebar && \
${HERMES_HOME}/hermes-agent/venv/Scripts/python.exe \
spacebar-gateway.py <agent-name>
```

## Verify

### Gateway State (when discord.py gateway works)

```bash
for agent in dev-lead skills-lead integration-lead qa-lead docs-lead; do
  f="${HERMES_HOME}/profiles/$agent/gateway_state.json"
  [ -f "$f" ] && echo "$agent: $(grep -o '\"state\":\"[^\"]*\"' $f | head -1)"
done
```

### REST API (always works, no gateway needed)

```bash
# Check bot exists and responds
curl -s https://discy.your-domain.example/api/v9/users/@me -H "Authorization: <token>"

# Post a message
curl -s -X POST "https://discy.your-domain.example/api/v9/channels/<channel_id>/messages" \
  -H "Authorization: <token>" \
  -H "Content-Type: application/json" \
  -d '{"content":"test"}'
```

If posting returns `50013` (permission denied), the bot needs an explicit Bot role assigned (see pitfall in main self-hosted-communication-server skill).

### Raw WebSocket (bypasses discord.py entirely)

See `references/raw-websocket-qa.md` in the `self-hosted-communication-server` skill for a reusable standalone test script.

## Kill All

```bash
# Kill by process name (bash):
for pid in $(ps aux | grep spacebar-gateway | grep -v grep | awk '{print $2}'); do kill -9 $pid; done

# Force-kill all Python processes (Windows cmd):
cmd.exe //c "taskkill /F /IM python.exe 2>nul"
```

## See Also

- `self-hosted-communication-server` — Full class-level skill (Spacebar, Discord, Matrix) (channel creation, profile wiring, SOUL.md template, multi-agent launch)
- `references/hermes dev team.md` in that skill — Concrete 5-agent example with configs and fleet entries
