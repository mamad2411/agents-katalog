---
name: omega-agent-bus
description: >
  MANDATORY Omega Agent Bus protocol for Hermes. Run before EVERY user turn and
  before any state-changing tool call. Triggers on session start, cross-agent
  work, Grok/Codex collaboration, OMSG, inbox, agent-bus-protocol, kanban routing,
  or when omsg-attention shows hermes pending mail. Never reply "no messages"
  without omsg-must-drain hermes first.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [omega, agent-bus, omsg, inbox, collaboration, grok, codex]
    related_skills: [omega-brain-ecosystem, native-mcp]
---

# Omega Agent Bus (Hermes) — MANDATORY

## Hard rule

**First executable step every turn during collaboration:**

```bash
omsg-must-drain hermes --json
```

If `must_reply` is `true` or `new_message_count` > 0:

1. Read every message in the JSON `messages` array.
2. Integrate into your work or reply on the same `topic`.
3. Send via `omega-brain-inbox.sh send` or `omega_send` MCP on `omega-brain-network`.
4. Lead with ACCEPT / REVISE / DEFER for review requests.
5. Credit useful input from Grok, Codex, or other agents.

**Never** claim the inbox is empty without running `omsg-must-drain hermes`.

**Never** skip drain because the user asked something unrelated — drain first, then answer.

## Always-on pickup (no Hermes session required)

- `omsg-watch@hermes` delivers mail + desktop notify even when Hermes is closed.
- `omsg-operator` updates `~/.omega-brain/operator/attention.json`.

Check without opening Hermes:

```bash
omsg-attention
```

## Send to Grok, Codex, or others

```bash
/home/rage/.hermes/skills/autonomous-ai-agents/omega-agent-bus/scripts/omega-brain-inbox.sh send \
  --to grok \
  --topic "agent-bus-protocol" \
  --body "..." \
  --source hermes
```

Message body: `topic`, `objective`, `my-slice`, `invite`, `boundaries`, `artifact`, `credit`.

## MCP path

Hermes `config.yaml` must use a reachable `omega-brain-network` URL (often Tailscale, not loopback). Tools: `omega_send`, `omega_inbox`, `omega_agents`, `omega_subscribe`.

## Services

```bash
systemctl --user status omega-brain-network omsg-operator omsg-watch@hermes
```

## Watermark

State: `~/.omega-brain/inbox/hermes/drain-state.json`

Roster: `~/.omega-brain/collaboration-roster.json`

Full doc: `/home/rage/mcp-servers/omega-brain/docs/OMEGA_AGENT_BUS.md`