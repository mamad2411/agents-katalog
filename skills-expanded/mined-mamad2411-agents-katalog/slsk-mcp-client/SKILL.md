---
name: slsk-mcp-client
description: Wraps the Slsk MCP server (MCPMarket) with safety rules, rate limits, and session logging for Soulseek access.
category: media
tags: [media, soulseek, mcp, acquisition]
agents: [opencode, freebuff, antigravity, codex]
---

# slsk-mcp-client

## Purpose

Behavioral wrapper around the Slsk MCP server (MCPMarket). Provides safety, etiquette, and logging rules on top of the MCP action layer.

## Invocation

**OpenCode / Codex:** `Invoke slsk-mcp-client`
**Freebuff:** `/skill slsk-mcp-client`

Requires: Slsk MCP server configured at `mcp/slsk-mcp.json`.

## Rules

- Always invoke `soulseek-network-orienter` first for etiquette context.
- Rate-limit searches: max 1 search per 10 seconds; no automated loops.
- Only queue downloads explicitly approved by the user.
- Log every download session to `obsidian-music-journal`.
- Tokens and credentials must be in `mcp/slsk-mcp.json`, never in prompts.

## MCP Action Layer

This skill wraps `mcp/slsk-mcp.json` which connects to the Slsk MCP server from MCPMarket.
- Source: https://mcpmarket.com (search "Slsk")
- Capabilities: authenticate, search Soulseek, queue downloads, monitor transfers.

## Inputs

- Search query (artist, release, label, scene keyword)
- User-approved download targets
- MCP config at `mcp/slsk-mcp.json`

## Outputs

- Queued downloads in slskd or Soulseek client
- Session log written to `obsidian-music-journal`

## Safety

- Never automate mass downloads; each download requires explicit user approval.
- Credentials stay in `mcp/slsk-mcp.json` — never exposed in prompts or logs.
- Always invoke `soulseek-network-orienter` before searching.

## Failure Modes

- MCP server unreachable — check `mcp/slsk-mcp.json` config and Slsk MCP server status.
- Rate limit hit — pause searches for 30 seconds before retrying.
- Download queue stalled — check slskd transfer queue; surface to user.

## Companion Skills

- `soulseek-network-orienter` — etiquette (invoke first)
- `slskd-media-acquisition` — alternative via slskd API
- `obsidian-music-journal` — session logging
