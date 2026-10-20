---
name: gateway-slash-commands
description: "Handle Hermes slash commands in Discord/Telegram/gateway messaging contexts — recognize known commands from COMMAND_REGISTRY and implement their intent using available tools."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [gateway, slash-commands, hermes-agent, command-handling, discord, telegram]
    triggers: [slash-command, /sessions, /resume, /status, /new, /model, /undo, /retry, /compress]
    related_skills: [debugging-hermes-tui-commands]
---

# Gateway Slash Command Handling

## When to Use

The user types what looks like a Hermes slash command (e.g. `/sessions`, `/resume`, `/status`, `/new`, `/model`) in a gateway context — Discord, Telegram, or any messaging platform. Your default should NOT be to treat it as free-form chat. Check if it's a known Hermes command and implement its intent with your available tools.

## Core Pattern

When you see user input starting with `/`:

1. **Check if it's a known command.** The canonical source is `COMMAND_REGISTRY` in `hermes_cli/commands.py` at the Hermes Agent codebase. Commands are defined as `CommandDef(name, description, category, ...)` entries. The `resolve_command()` function maps aliases to canonical names.

2. **Check if you can implement it with tools.** Many commands have tool-based equivalents:
   - `/sessions` — use `session_search()` to browse/query sessions
   - `/resume <id>` — use `session_search(session_id=...)` to scroll into it
   - `/status` — use `session_search()` browse shape or memory recall for session info
   - `/search <query>` — use `session_search(query=...)`

3. **Implement the command's intent.** Map the command to the closest tool behavior. Format output clearly, mirroring the CLI presentation where appropriate.

4. **Tell the user how to proceed.** If your tool can only do part of what the CLI command does, explain the next step (e.g. "Use `/resume <id>` to continue").

## Command Map (Known Mappings)

### `/sessions` — Browse and resume previous sessions

**Definition:** `CommandDef("sessions", "Browse and resume previous sessions", "Session")`

**Gateway implementation:**
1. Call `session_search()` with no arguments (browse shape) to get recent sessions
2. Format as a table: #, Title, Preview, Source, Message count
3. Tell user to use `/resume <session_id>` to continue a session
4. For searches: `session_search(query="<term>")` with limit=5-10 to find specific sessions
5. To scroll into a session: `session_search(session_id="<id>", around_message_id=<id>)`

**CLI reference behavior** (from `cli.py:_show_recent_sessions`):
- Uses `session_db.list_sessions_rich()` with source="cli", exclude_sources=["tool"]
- Formats as: `# | Title (32ch) | Preview (38ch) | Last Active (13ch) | ID`
- Shows up to 10 sessions by default
- Prompts: "Use /resume <number>, /resume <session id>, or /resume <session title> to continue."

**Pitfalls:**
- The current session is excluded from the list (filtered out by ID match)
- Session IDs shown are the canonical ID, not a number — the CLI supports /resume <number> by position but the gateway must use session_id strings

### `/resume <id>` — Continue a previous session

**Definition:** `CommandDef("resume", "Resume a previously-named session", "Session", args_hint="[name]")`

**Gateway implementation:**
- Use `session_search(session_id="<id>")` with around_message_id to scroll into it
- Show the recent messages to give context
- Let the user know they can continue the conversation

### `/status` — Show session info

**Definition:** `CommandDef("status", "Show session info", "Session")`

**Gateway implementation:**
- Current session ID, source, message count from conversation context
- Can supplement with `session_search()` for current session details

### `/new` — Start a new session

**Definition:** `CommandDef("new", "Start a new session (fresh session ID + history)", "Session", aliases=("reset",), args_hint="[name]")`

**Gateway implementation:**
- This is handled by the Hermes gateway infrastructure — the agent's session ID changes
- In agent context, acknowledge the intent and note the fresh start

## Commands That Are CLI-only (no direct gateway mapping)

These commands are marked `cli_only=True` and cannot be implemented in gateway:
- `/clear` — Clear screen (terminal behavior)
- `/history` — Show conversation history (TUI renders this)
- `/save` — Save conversation
- `/redraw` — Force UI repaint
- `/handoff` — Hand off to messaging platform
- `/snapshot` — Config/state snapshots

For these, acknowledge the command exists but explain it's CLI-only, or offer to do a manual equivalent.

## General Principles

1. **When in doubt, assume the user expects the command to work.** A repeated command (typed 2+ times) is a strong signal your first response missed the mark.
2. **Don't treat `/command` text as a query or question.** The user is executing a command, not asking a question about the command.
3. **Check the registry.** Always verify the command's canonical name, aliases, and category before responding. The regex-ish `resolve_command()` from `hermes_cli/commands.py` is the ground truth.
4. **Graceful degradation.** If you can only implement part of the command's functionality, do what you can and explain the gap.

## Pitfalls

- Don't ignore a known command — if you see `/sessions`, `/resume`, `/status`, etc. in user input, treat them as commands first
- Don't treat `/command` as free-form text to chat about — the user wants the command executed
- Don't say "I don't have that command" — check the registry first; many commands map to tools you already have
- Don't explain what the command does in the abstract — execute it
- Session IDs from `session_search()` are strings like `"20260529_083351_70d3746a"` — use them directly, not as positions

## Verification

After implementing a command:
1. Did you call a tool to produce the output? (session_search for /sessions, etc.)
2. Is the output formatted clearly (table, columns, scannable)?
3. Did you tell the user how to take the next step? (/resume for /sessions, etc.)
4. If you got it wrong and the user repeats the command, try a different approach — dig into the codebase if needed
