---
name: chrome-live-session
description: Attach to the user's existing Chrome session through the official Chrome DevTools MCP server for live tab inspection, debugging, and interaction.
---

# Chrome Live Session

Use this when the user explicitly wants you to inspect, debug, or interact with a page that is already open in Chrome.

## What it is

This skill tells the agent to prefer the user's already-open Chrome session over launching a fresh browser.

## Why it matters

Using the live session preserves:

- active logins
- cookies
- existing navigation state
- tabs the user has already prepared

## Safety rules

- Only use this after the user clearly asks for browser inspection or interaction.
- Be careful with unrelated tabs and personal data.
- Narrate major actions before making impactful page changes.
- Prefer the minimum number of interactions needed.

## Setup expectation

This skill assumes the client has a `chrome-devtools` MCP server configured with the official server and `--autoConnect`.

## Recommended flow

1. Connect to the live Chrome session.
2. Start with inspection before mutation.
3. Use snapshots, console, and network tools first.
4. Click/type only after confirming the intended target.
