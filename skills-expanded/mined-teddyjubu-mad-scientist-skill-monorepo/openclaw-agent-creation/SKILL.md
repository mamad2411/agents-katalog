---

name: openclaw-agent-creation
description: Create a new OpenClaw subagent workspace with full file structure, modeled after existing agents. Use this when the user wants to add a new named AI agent to their team.

---
When the user wants to create a new AI agent on their team, follow this workflow.

## What This Skill Does

This skill Create a new OpenClaw subagent workspace with full file structure, modeled after existing agents. Use this when the user wants to add a new named AI agent to their team.

## Step 1: Check Existing State

**Check if the agent is already registered in openclaw.json:**

```bash
python3 -c "
import json
with open('/root/.openclaw/.openclaw/openclaw.json') as f:
    config = json.load(f)
agents = config.get('agents', {}).get('list', [])
matches = [a for a in agents if a['id'] == '<agent-id>']
print(json.dumps(matches, indent=2))
"
```

**Check if workspace directory exists:**

```bash
ls -la /root/.openclaw/workspace/agents/<agent-id>/ 2>/dev/null || echo "Directory does not exist"
```

**Check existing agents for reference:**

```bash
ls /root/.openclaw/workspace/agents/
```

## Step 2: Create Workspace Directory Structure

```bash
mkdir -p /root/.openclaw/workspace/agents/<agent-id>/{memory,scripts,data/.learnings,logs}
touch /root/.openclaw/workspace/agents/<agent-id>/.openclaw/config.json
```

## Step 3: Create Required Files

Every agent needs these files (model after existing agents like Bob or Mark):

| File | Purpose |
|------|---------|
| `IDENTITY.md` | Name, role, specialty, emoji |
| `AGENTS.md` | System rules, capabilities, workflows, tools, guardrails, delivery protocol |
| `SOUL.md` | Personality, voice, workflow philosophy, signature move |
| `TOOLS.md` | Toolkit description, command patterns, evaluation frameworks |
| `USER.md` | What the agent knows about Charles, his businesses, expectations |
| `QUICK_START.md` | First-run guide for the agent |
| `HEARTBEAT.md` | Status tracker |
| `README.md` | Full overview for humans |

## Step 4: Register in openclaw.json (if not already there)

The agent entry goes in `agents.list`:

```json
{
  "id": "<agent-id>",
  "name": "<Agent Name>",
  "workspace": "/root/.openclaw/workspace/agents/<agent-id>",
  "model": "openrouter/anthropic/claude-sonnet-4-5"
}
```

**CRITICAL PATH NOTE:** Existing configs may show `/data/.openclaw/workspace/agents/<agent-id>` as the workspace path, but the actual filesystem uses `/root/.openclaw/workspace/agents/<agent-id>`. `/data` does not exist on this machine. If the config references `/data/`, it should be updated to `/root/` or a symlink created:

```bash
ln -sf /root/.openclaw /data/.openclaw 2>/dev/null
```

## Step 5: Add Telegram Account (if needed)

In `channels.telegram.accounts`:

```json
"<agent-id>": {
  "enabled": true,
  "dmPolicy": "allowlist",
  "botToken": "<bot-token>",
  "allowFrom": ["<user-telegram-id>"],
  "groupPolicy": "disabled",
  "streaming": "partial"
}
```

## Step 6: Add Binding

In `bindings`:

```json
{
  "agentId": "<agent-id>",
  "match": {
    "channel": "telegram",
    "accountId": "<agent-id>"
  }
}
```

## Step 7: Add Spawn Allowlist (optional)

If the main agent should be able to spawn this new agent, add it to the main agent's `subagents.allowAgents`:

```json
"subagents": {
  "allowAgents": ["main", "mark", "eric", "michael", "bob", "<agent-id>"]
}
```

## Step 8: Verify

```bash
# Verify directory exists
ls -la /root/.openclaw/workspace/agents/<agent-id>/

# Verify config is valid JSON
python3 -c "import json; json.load(open('/root/.openclaw/.openclaw/openclaw.json')); print('Config OK')"

# Verify all required files exist
for f in IDENTITY.md AGENTS.md SOUL.md TOOLS.md USER.md QUICK_START.md HEARTBEAT.md README.md; do
  [ -f "/root/.openclaw/workspace/agents/<agent-id>/$f" ] || echo "MISSING: $f"
done
```

## Existing Agents Reference

- **bob** 🏘️ — Property Intelligence & Outreach
- **eric** 🎬 — Video Creation & Social Media
- **mark** 🎨 — Design & Graphics
- **michael** 🎨 — REI Content & Community Events
- **tammie** 👩‍💼 — HR & Hiring Automation

## Pitfalls

- **Path mismatch:** Config may reference `/data/.openclaw/` but the real path is `/root/.openclaw/`. Always verify with `ls`. The symlinks `/data/.openclaw` may or may not exist.
- **OpenClaw CLI not in PATH:** Even when OpenClaw processes are running (gateway, TUI), the `openclaw` CLI binary may NOT be in `$PATH`. This happens on linuxbrew installs where the path isn't exported. Test with `which openclaw` first. If not found, try: `export PATH="/data/linuxbrew/.linuxbrew/bin:$PATH"` or find it: `find / -name 'openclaw' -type f -executable 2>/dev/null`. CLI commands like `openclaw doctor` or `openclaw tui` will fail silently without it.
- **TUI already running:** If another session has `openclaw tui` attached, you can't launch a second instance. Check with `ps aux | grep openclaw-tui`. You can still interact via the gateway HTTP API on port 18789 (health at `/health`, webhook endpoints at `/hooks/...`).
- **Agent already registered but no workspace:** This happens — the config entry exists but the directory was never created. Create it without modifying config.
- **Don't copy API keys between agents:** Each agent may need its own credentials. Reference the correct skill/secrets for the new agent's role.
- **Main agent allowlist:** If the new agent should be spawnable by the main agent, remember to add it to `subagents.allowAgents` in the main agent's config entry.
- **Gateway API auth:** The gateway exposes an internal API. Get the hooks token from `openclaw.json` (`hooks.token`). Port 18789 serves the web UI; 18791 is the authenticated API.
