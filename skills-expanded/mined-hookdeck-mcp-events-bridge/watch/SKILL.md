---
name: watch
description: Watch for events from the MCP Events bridge in the background, such as GitHub issues, comments, pull requests, reviews, pushes, releases and workflow runs, inbound email, or other webhooks, and tell the user as each one happens. Use when the user asks to watch, follow or monitor events, to be told when something happens in a repository or inbox, to stop watching, or what is being watched. Needs the bridge's Claude Code plugin, mcp-events-bridge.
allowed-tools: Bash(events-bridge watches *)
---

# Watch MCP Events bridge events

This plugin runs a monitor for the whole session that follows this project's watch list. Each watch is an event type name and its arguments. When an event happens, you get a monitor notification, and you should tell the user about it, briefly, without being asked.

## Before you start: is the plugin installed?

This skill is part of the bridge's Claude Code plugin, `mcp-events-bridge`. The plugin provides everything this skill uses: the `events-bridge` command, the `events-bridge` MCP server, and the monitor that tells you about events.

`npx skills add hookdeck/mcp-events-bridge` can install this skill without the plugin. Then the shell can't find `events-bridge` (`command not found` or `No such file or directory`, exit code 127). If that happens, stop: don't retry, and don't look for another way to run the commands. Tell the user the plugin isn't installed, and what they can do:

- **No bridge yet:** set one up first. The `mcp-events-bridge` skill (`npx skills add hookdeck/mcp-events-bridge --skill mcp-events-bridge`) or the [README](https://github.com/hookdeck/mcp-events-bridge#readme) walks through it.
- **In Claude Code:** install the plugin with `/plugin install mcp-events-bridge --marketplace hookdeck/mcp-events-bridge` (Claude Code 2.1.275 or later). It asks for the bridge's MCP endpoint and secret. Then start a new session. See the [Claude Code guide](https://github.com/hookdeck/mcp-events-bridge/blob/main/skills/mcp-events-bridge/references/claude-code.md).
- **In another agent:** use the bridge's `wait_for_event` and `poll_events` MCP tools, which wait for events while you work on a request. If you can run a command in the background and act on its output, `npx @hookdeck/mcp-events-bridge watch <event...>` prints one JSON line per event. It reads the bridge's MCP endpoint from `BRIDGE_MCP_URL` and its secret from `BRIDGE_MCP_SECRET`.

## Find event types and their arguments

Call the `events-bridge` MCP server's `list_sources` tool (`list_providers` on a bridge before 0.6.0). Each source's `events` lists its event types: each one's `name` (such as `github.issue_comment` or `resend.email.received`), `description`, and `inputSchema`, which describes the arguments it takes (for GitHub: `repository` as owner/name, `actions` as a list, `sender`). A bridge before 0.10.0 lists only the names. Either way, `watches add` checks the arguments (`--filter key=value`) with the bridge and says which one is wrong.

## Add, remove and list watches

Run these exactly as shown, one watch per event name:

```sh
events-bridge watches add <event name> --filter <key>=<value> --store "${CLAUDE_PLUGIN_DATA}" --project "${CLAUDE_PROJECT_DIR}"
events-bridge watches remove <event name> --store "${CLAUDE_PLUGIN_DATA}" --project "${CLAUDE_PROJECT_DIR}"
events-bridge watches remove --all --store "${CLAUDE_PLUGIN_DATA}" --project "${CLAUDE_PROJECT_DIR}"
events-bridge watches list --store "${CLAUDE_PLUGIN_DATA}" --project "${CLAUDE_PROJECT_DIR}"
```

- `--filter` is repeatable. A list value is JSON: `--filter 'actions=["opened","closed"]'`.
- `add` checks the name and arguments with the bridge, and says why if they're wrong. `remove` without `--filter` removes every watch for that event name.
- The monitor picks up a change within a few seconds. A new watch starts from now. Don't start a watch with the Monitor tool yourself: the plugin's monitor already runs.
- Watches belong to this project and last between sessions. When a session starts, events that happened since the last session arrive first (up to 24 hours old).

To show past events instead, use the MCP server's `list_events` and `get_event` tools.

## When an event arrives

Each notification line is one event as JSON: `{"eventId", "name", "timestamp", "data"}`. Tell the user what happened in a sentence or two, with its link (`data.url`) when there is one.

Long lines are cut short in notifications. If a field looks cut off, read the whole event with the MCP server's `get_event` tool (its `name` and `eventId`, which are at the start of the line), and don't mention that you did.

A line like `{"problem": "..."}` means something is wrong. Tell the user:

- `stopped watching: ...` with a `watch`: that watch can't run (for example, the event no longer exists). Suggest removing it.
- `this watch keeps failing, still retrying: ...` with a `watch`: the bridge answers, but not for that watch (for example, its source isn't set up). It's still retried.
- `can't reach the bridge, still retrying: ...`: events will arrive once the bridge is reachable again. If it says `no MCP URL yet`, the plugin's MCP URL isn't set: the user sets it with `/plugin configure mcp-events-bridge@hookdeck`, then starts a new session.
