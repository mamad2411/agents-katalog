# Quill Mission Inbox — OpenClaw Skill

## What This Skill Does

Automatically syncs every significant OpenClaw session into the **Quill Mission Inbox** at `https://your-quill-domain/missions`.
After completing a task or conversation on any channel (Telegram, WhatsApp, Slack, Discord, Signal, iMessage, Matrix…), OpenClaw calls the Quill ingest API so all your agent activity appears in one place.

This skill also connects OpenClaw to the Quill MCP server so it can *read* your mission history and open Quill chats directly.

---

## Setup (2 minutes)

### 1. Generate a Quill API Key

1. Open your Quill dashboard → **Settings → API Keys**
2. Click **Generate new key** → copy the key (shown once)
3. Set environment variables:
   ```bash
   # ~/.bashrc, ~/.zshrc, or .env in your OpenClaw workspace
   export QUILL_API_KEY="qak_your_key_here"
   export QUILL_BASE_URL="https://your-quill-domain.vercel.app"
   ```

### 2. Install the Skill

```bash
mkdir -p ~/.openclaw/workspace/skills/quill-inbox
cp SKILL.md ~/.openclaw/workspace/skills/quill-inbox/SKILL.md
```

Or install directly from the Quill MCP endpoint once connected.

### 3. Add Quill as an MCP Server in OpenClaw

Open **OpenClaw → Settings → MCPs** and add:

| Field | Value |
|-------|-------|
| Name | Quill Inbox |
| URL | `https://your-quill-domain.vercel.app/api/agent/mcp` |
| Auth type | Bearer |
| Token | `qak_your_key_here` |

Or via the OpenClaw config file:

```json
// ~/.openclaw/config.json
{
  "mcpServers": [
    {
      "name": "quill",
      "url": "${QUILL_BASE_URL}/api/agent/mcp",
      "auth": "Bearer ${QUILL_API_KEY}",
      "description": "Quill Mission Inbox"
    }
  ]
}
```

---

## Behavior (When OpenClaw Should Trigger This Skill)

**ALWAYS call `send_session` when:**

- A multi-turn conversation ends or has been idle for > 5 minutes
- A task is marked done, completed, or resolved
- A file, document, or code artefact is delivered
- A scheduled or automated workflow finishes
- The user says "save", "log", "remember", or "archive this"

**DO NOT call for:**
- Single-message exchanges with no notable output
- Internal reasoning / chain-of-thought steps
- Health checks or ping messages

---

## API Reference

### Option A — MCP Tool Call (if MCP server is configured)

When Quill is added as an MCP server, OpenClaw can call:

```typescript
// OpenClaw will call this automatically during session completion
await mcp.callTool("quill", "send_session", {
  title: "Summary of what was accomplished",
  source: "openclaw",
  summary: "Detailed session description",
  sourceId: session.id,              // optional
  externalUrl: session.deepLink,     // optional
  metadata: {
    channel: session.channel,        // e.g. "telegram", "slack"
    contact: session.contact,
  },
});
```

### Option B — Webhook / Direct HTTP (no MCP needed)

Add a webhook in **OpenClaw → Automations → Webhooks**:

| Field | Value |
|-------|-------|
| Trigger | Session completed |
| URL | `${QUILL_BASE_URL}/api/missions/ingest` |
| Method | POST |
| Headers | `Authorization: Bearer ${QUILL_API_KEY}` |
| Body template | See below |

**Webhook body template:**
```json
{
  "title": "{{session.title}}",
  "source": "openclaw",
  "summary": "{{session.summary}}",
  "sourceId": "{{session.id}}",
  "externalUrl": "{{session.deepLink}}",
  "metadata": {
    "channel": "{{session.channel}}",
    "contact": "{{session.contact}}"
  }
}
```

### Option C — CLI (ad hoc)

```bash
curl -X POST "${QUILL_BASE_URL}/api/missions/ingest" \
  -H "Authorization: Bearer ${QUILL_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Task completed",
    "source": "openclaw",
    "summary": "What was done"
  }'
```

---

## Reading Missions Back (MCP Tools Available)

When connected via MCP, OpenClaw can call:

| Tool | What it does |
|------|-------------|
| `list_missions` | List all sessions (Quill + external agents), filter by `source` |
| `send_session` | Push a session into the inbox |
| `get_mission` | Get details for a specific mission by ID |
| `new_chat_url` | Get the URL to open a new Quill chat |

---

## sessions_send Integration (OpenClaw native)

If you want to send tasks *from* Quill to OpenClaw via the OpenClaw gateway:

1. Set `OPENCLAW_GATEWAY_URL=http://localhost:18789` in your Quill `.env.local`
2. Use the Quill delegate API:
   ```bash
   curl -X POST https://your-quill-domain/api/agent/delegate \
     -H "Cookie: <your-session>" \
     -d '{"agent":"openclaw","task":"Summarise my emails from today"}'
   ```
3. OpenClaw will receive the task via `POST /sessions/send` and process it on your behalf.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `QUILL_API_KEY` not set | Set env var or check Settings → API Keys |
| 401 Unauthorized | Regenerate key — shown once only |
| MCP tool not found | Confirm Quill MCP server URL is correct and gateway is running |
| Sessions not appearing | Confirm `source` is one of: `openclaw telegram gmail notion slack hermes agent custom` |
| Webhook not firing | Check OpenClaw Automations → Webhook logs for errors |

---

## ACP Integration (Advanced)

Both OpenClaw and Quill support the [Agent Communication Protocol (ACP)](https://acp.dev).
OpenClaw discovers peers via `docs.acp.md`. To register Quill as an ACP peer, add to your ACP registry:

```json
{
  "peers": [
    {
      "id": "quill-inbox",
      "endpoint": "${QUILL_BASE_URL}/api/agent/mcp",
      "auth": "Bearer ${QUILL_API_KEY}",
      "capabilities": ["missions.list", "missions.create", "missions.get"]
    }
  ]
}
```
