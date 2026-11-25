---
name: discord-tool
description: >-
  Discord integration tool. Sends and receives messages, performs searches, lists guilds and channels, and manages reactions.
  Use when: Use when: you need to send messages on Discord, list channels, search within a server, react to messages, or check threads.
tags: [communication, discord, external]
---


# Discord Tool

An external tool for sending and receiving Discord messages, searching, listing servers/channels, and managing reactions.

## How to Invoke

**Bash**: Run with `animaworks-tool discord <サブコマンド> [引数]`

## List of Actions

### guilds — List Servers
```bash
animaworks-tool discord guilds
```

### channels — List Channels
```bash
animaworks-tool discord channels GUILD_ID
```
- `GUILD_ID`: Snowflake ID of the target guild (server) (required)

### send — Send Message
```bash
animaworks-tool discord send CHANNEL_ID MESSAGE [--reply-to MESSAGE_ID]
```
- `CHANNEL_ID`: Snowflake ID of the destination text channel
- `--reply-to`: Optional. Reply-to message ID

### messages — Fetch Messages
```bash
animaworks-tool discord messages CHANNEL_ID [-n 20]
```

### search — Search Messages
```bash
animaworks-tool discord search KEYWORD [-c CHANNEL_ID] [-n 50]
```

### react — Add Reaction (MCP only, not available in CLI)
- Adds an emoji reaction. **MCP only**. Not available in the CLI.

## CLI Usage

```bash
animaworks-tool discord guilds
animaworks-tool discord channels GUILD_ID
animaworks-tool discord send CHANNEL_ID MESSAGE [--reply-to MESSAGE_ID]
animaworks-tool discord messages CHANNEL_ID [-n 20]
animaworks-tool discord search KEYWORD [-c CHANNEL_ID] [-n 50]
```

## Notes

- The Discord Bot Token must be pre-configured in credentials
- To get a channel ID, right-click in Discord's developer mode and select "Copy ID"
- Messages have a 2000-character limit
- Guild IDs, channel IDs, and message IDs are all numeric strings (Snowflake IDs)
- The bot needs the required permissions (Send Messages, Read Message History, Add Reactions, View Channels)
