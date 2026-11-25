---
name: pieces-mcp
description: "Connect ArgentOS to Pieces long-term memory via MCP. Query past activity, create durable memories, and search across devices using PiecesOS."
metadata:
  argent:
    emoji: 🧩
    homepage: https://pieces.app
    requires:
      bins:
        - curl
        - npm
    install:
      - id: mcp-remote
        kind: npm-global
        package: mcp-remote@0.1.38
        bins:
          - mcp-remote
        label: Install mcp-remote (MCP bridge)
---

# Pieces MCP Skill for ArgentOS

Connect ArgentOS to Pieces long-term memory via MCP. Pieces captures ambient context (browser, clipboard, meetings, code) across devices. This skill teaches you how to wire it into ArgentOS so you can query that memory and create durable summaries.

## When to Use This Skill

Trigger when:

- The human mentions **Pieces**, **PiecesOS**, or **long-term memory**
- They want cross-device memory: "What did I work on today?"
- They say "Hook up to my Pieces" or "Ask Pieces"
- You see an HTTPS tunnel URL for a Pieces MCP server

## Architecture

Three components:

1. **PiecesOS MCP server** — runs on the human's machine with Long-Term Memory (LTM) enabled. Exposed via HTTPS tunnel.
2. **ArgentOS gateway** — this machine. Connects to the Pieces MCP server via `gateway.mcp.servers` config.
3. **Bridge: mcp-remote** — npm package that connects to the remote `/mcp` endpoint and exposes it locally as a stdio MCP server.

> **Important:** This integration is MCP-only. Always use `/mcp`, never `/sse`.

## Setup Guide

### Step 1: Confirm PiecesOS Is Running

Ask the human to confirm:

> "Make sure PiecesOS is installed and running on your machine (or remote machine), and that Long-Term Memory (LTM) is enabled in the Pieces Desktop App."

### Step 2: Get the Tunnel URL

The human needs to expose PiecesOS's MCP server via HTTPS:

**For ngrok:**

> "On the machine running PiecesOS, run:
>
> ```bash
> ngrok http 39300
> ```
>
> Paste the HTTPS forwarding URL here (e.g., `https://abc123.ngrok-free.dev`)."

**For custom tunnels:** Any HTTPS URL that forwards to `localhost:39300` works.

### Step 3: Verify the MCP Endpoint

Construct the MCP URL:

```
MCP_URL = <tunnel_url>/model_context_protocol/2025-03-26/mcp
```

Quick sanity check:

```bash
curl -i "<MCP_URL>"
```

**Expected:** HTTP 400 with `"mcp-session-id header or sessionId query parameter is required"`. This means the server is alive and ready.

If you get 404, 502, or timeout — the tunnel is down. Ask the human to check PiecesOS and the tunnel.

### Step 4: Configure ArgentOS

Add the Pieces MCP server to `~/.argentos/argent.json` under `gateway.mcp.servers`:

```json
{
  "gateway": {
    "mcp": {
      "servers": {
        "pieces": {
          "command": "mcp-remote",
          "args": ["<MCP_URL>"]
        }
      }
    }
  }
}
```

**Example with ngrok:**

```json
{
  "gateway": {
    "mcp": {
      "servers": {
        "pieces": {
          "command": "mcp-remote",
          "args": ["https://abc123.ngrok-free.dev/model_context_protocol/2025-03-26/mcp"]
        }
      }
    }
  }
}
```

### Step 5: Install mcp-remote

```bash
npm install -g mcp-remote@0.1.38
```

### Step 6: Restart the Gateway

```bash
argent gateway restart
```

The Pieces MCP tools are now available to all agent sessions.

## Available Tools

Once connected, three Pieces tools become available:

### ask_pieces_ltm

Query long-term memory with a natural language question:

```json
{
  "name": "ask_pieces_ltm",
  "arguments": {
    "question": "What did I work on today?",
    "chat_llm": "gpt-4"
  }
}
```

Returns `summaries[]` and `events[]` as structured JSON. Parse this and synthesize a natural language answer for the human.

**Use for:**
- "What did I work on today / this week?"
- "What did we discuss in the standup?"
- "What debugging steps did I try last time?"

**When you answer, attribute it:**
> "According to your Pieces long-term memory, ..."

### create_pieces_memory

Write a durable memory:

```json
{
  "name": "create_pieces_memory",
  "arguments": {
    "summary_description": "Profile: Jason — MSP Owner",
    "summary": "# Profile: Jason\n\n## Role\nMSP owner, AI developer\n\n## Current Focus\nArgentOS development",
    "project": "ArgentOS"
  }
}
```

**Use for:**
- Human profile (name, role, preferences)
- Decision summaries
- Debugging recaps
- Project milestones

### Full-Text Search Tools

Search tools (names vary by PiecesOS version) provide keyword-based search across all captured context.

## Troubleshooting

### MCP URL returns 404/502/timeout

- Confirm PiecesOS is running on the remote machine
- Confirm the tunnel is active (`ngrok` may have restarted)
- Ask the human for a fresh tunnel URL

### Tools not appearing after gateway restart

1. Check `~/.argentos/argent.json` has the `gateway.mcp.servers.pieces` entry
2. Verify `mcp-remote` is installed: `mcp-remote --help`
3. Test the MCP URL directly with curl (Step 3)
4. Check gateway logs: `grep pieces /tmp/argent/argent-*.log`

### ask_pieces_ltm times out or gives vague answers

Narrow the query:
- Add time: "What did I work on **this morning**?"
- Add topic: "What have I done on **the website project**?"
- Add context: "What debugging steps did I try for **the login bug**?"

### Raw JSON responses

This is normal. Pieces returns structured JSON with `summaries[]` and `events[]`. You (the agent) parse it and synthesize a natural language answer. The raw JSON is not an error.

## Direct Testing (Debugging Only)

If MCPorter/mcp-remote isn't working, test the MCP server directly:

Create `init.json`:

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "0.1.0",
    "capabilities": {},
    "clientInfo": { "name": "argentos-agent", "version": "1.0" }
  },
  "id": "1"
}
```

```bash
curl -i -X POST "<MCP_URL>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: init-001" \
  --data-binary @init.json
```

Extract the `mcp-session-id` from the **response headers** (13-digit timestamp like `1774202062499`). Use that for all subsequent requests.

> **Common mistakes:** Use `--data-binary @file.json` (not inline `-d`), use string IDs (`"id": "1"` not `"id": 1`), always include both `Content-Type` and `Accept` headers.
