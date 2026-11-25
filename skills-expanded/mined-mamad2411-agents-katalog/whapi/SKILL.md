---
name: whapi
description: >
  WHAPI.cloud WhatsApp API guide for AI agents. Use this skill when building
  WhatsApp bots, automations, CRM integrations, or broadcast systems with WHAPI.
  Prevents the most common AI mistakes: wrong Chat ID format, wrong message type,
  polling instead of webhooks, and hallucinated parameters.
license: MIT
metadata:
  author: whapi
  version: "1.0.0"
  organization: WHAPI.cloud
  date: April 2026
  abstract: >
    Practical guide for AI agents working with the WHAPI WhatsApp API and its MCP
    server. Covers Chat ID formats, message type selection, webhook setup, groups,
    channels/newsletters, communities, and ready-made integration patterns. Each
    reference file includes correct and incorrect examples to prevent hallucinations
    and common mistakes.
---

# WHAPI.cloud WhatsApp API — Agent Skill

Practical guide for AI agents building WhatsApp integrations via WHAPI.cloud.
Contains rules across 7 categories, prioritized to prevent the most frequent
mistakes and cover the most-used API features.

## Prerequisites — MCP Setup Check

Before starting any task, verify that the `whapi-mcp` MCP server is available:

1. Attempt to call the `checkHealth` tool.
2. If it responds successfully — proceed.
3. If the tool is not found — the MCP server is not installed.
   Guide the user through installation: `references/core-mcp-setup.md`.
4. If the tool returns 404 ("Channel not found") — the token is invalid or the channel
   does not exist. Guide the user: `references/core-mcp-setup.md` section
   "Token is Missing or Invalid".
5. If the tool responds, check `status.text` in the response:

| status.text  | Meaning                        | Action                                                                      |
|--------------|--------------------------------|-----------------------------------------------------------------------------|
| `AUTH`       | Connected and operational      | Proceed                                                                     |
| `QR`         | Waiting for QR code scan       | Open the channel dashboard and scan the QR code to pair                    |
| `INIT`       | Server initialization          | Wait 40-50 seconds; if persists, contact WHAPI support                      |
| `LAUNCH`     | Connecting to WhatsApp account | Wait a few seconds; if persists, contact WHAPI support                      |
| `STOP`       | Channel deactivated            | Check subscription status at [panel.whapi.cloud/dashboard](https://panel.whapi.cloud/dashboard) |
| `SYNC_ERROR` | Sync failure                   | Log out the channel and reconnect it; GET requests will fail until resolved |

For `QR` pairing: `references/core-mcp-setup.md` section "Where to Get Your API Token".

## When to Apply

Reference these guidelines when:
- Setting up the WHAPI MCP in Cursor, Claude Desktop, or any MCP-compatible client
- Sending messages (text, media, interactive, polls)
- Receiving incoming messages via webhooks
- Managing groups, channels (newsletters), or communities
- Building bots, broadcast systems, or CRM integrations
- Troubleshooting unexpected API behavior

## API Coverage and MCP Fallback

This skill covers the most-used operations and prevents the most common mistakes.
It does NOT document every WHAPI endpoint.

**If the operation you need is not described in any reference file:**
1. Check available MCP tools — `whapi-mcp` exposes all API methods directly.
2. Apply `core-chat-id.md` rules for Chat ID format regardless of the endpoint.
3. Apply `core-auth.md` rules for authentication regardless of the endpoint.
4. Use ONLY parameter names from the MCP tool schema — do NOT invent parameters.
5. Validate against the [WHAPI API Reference](https://whapi.readme.io/reference) if unsure.

The MCP is the source of truth for available methods. The skill is the source of truth
for correct usage patterns and anti-hallucination rules.

## Rule Categories by Priority

| Priority | Category     | Impact    | Prefix          |
|----------|--------------|-----------|-----------------|
| 1        | Core Concepts | CRITICAL | `core-`         |
| 2        | Messaging     | CRITICAL | `msg-`          |
| 3        | Receiving     | CRITICAL | `recv-`         |
| 4        | Groups        | HIGH     | `groups-`       |
| 5        | Channels      | HIGH     | `channels-`     |
| 6        | Communities   | MEDIUM   | `communities-`  |
| 7        | Patterns      | HIGH     | `pattern-`      |

## How to Use

Read individual reference files for detailed explanations and code examples:

```
1. references/core-mcp-setup.md      ← install and configure the MCP first
2. references/core-chat-id.md        ← understand Chat ID formats (most common error)
3. references/core-auth.md           ← authenticate direct REST calls
4. references/msg-type-selection.md  ← choose the right send tool
5. references/recv-webhooks.md       ← set up receiving messages
```

Each reference file contains:
- Why this matters (1-2 sentences)
- Incorrect example with explanation
- Correct example with explanation
- Anti-hallucination checklist (parameters that do NOT exist)
- WHAPI-specific notes

## References

- https://whapi.readme.io/reference — Full API Reference
- https://support.whapi.cloud/help-desk — Documentation & FAQ
- https://support.whapi.cloud/help-desk/faq/chat-id.-what-is-it-and-how-to-get-it
- https://support.whapi.cloud/help-desk/integrations/mcp-model-context-protocol
