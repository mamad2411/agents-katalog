---
name: pi-agent-hermes-tool
description: "Hermes-native tool plugin for controlling pi --mode rpc sessions with full lifecycle management"
version: 1.0.0
author: Dustin Chadwick (@ShaggyD)
license: MIT
tags: [hermes, pi-agent, rpc, tool-plugin, session-management]
---

# Pi Agent - Hermes Tool Plugin

Native Hermes tool plugin for controlling `pi --mode rpc` sessions. Provides the `pi_agent` tool within Hermes for full session lifecycle management.

## Problem

Running pi in RPC mode from within Hermes meant manually launching subprocesses, managing session files, reading JSON event streams, and handling auth failures. Every session required wiring up stdin/stdout, tracking session state yourself, and reconnecting when things broke. There was no reusable, tested interface.

## Built

A Hermes tool plugin (`tools/pi_agent_tool.py`) with a companion test suite that wraps the entire pi RPC protocol. Provides a single `pi_agent` tool with these actions:

- **start** - Launch a new pi RPC session in a project directory
- **resume** - Reconnect to an existing session file
- **send** - Send a message or command to the active session
- **poll** - Fetch new events since last check
- **wait** - Block until the session completes its turn
- **stop** - Terminate a session cleanly
- **list** - View active sessions

## Outcome

No more manual process management or raw JSON line parsing. Pi RPC sessions are as easy to use as any other Hermes tool. Sessions survive restarts, auth reconnects, and network interruptions without losing context. The test suite validates against the actual pi protocol so edge cases and auth failures are handled cleanly.

## Installation

This plugin is registered in the Hermes agent's tool configuration. Ensure the `pi_agent_tool.py` file is accessible from the Hermes tools directory.

```bash
# Copy the tool file to Hermes tools directory
cp tools/pi_agent_tool.py ~/.hermes/tools/

# The pi CLI must be installed and on PATH
pi --version
```

## Files

| File | Purpose |
|------|---------|
| `tools/pi_agent_tool.py` | Main Hermes tool plugin for pi RPC |
| `tools/test_pi_agent_tool.py` | Test suite against the pi protocol |
| `scripts/pi_agent_client.py` | Helper client for pi RPC communication |

## Usage

```bash
# Start a session
pi_agent action=start workdir=/path/to/project

# Send a message
pi_agent action=send session_id=abc message="build the feature"

# Wait for completion
pi_agent action=wait session_id=abc timeout=120

# Stop when done
pi_agent action=stop session_id=abc
```

## See Also

- [pi-agent (autonomous-agents)](../../autonomous-agents/pi-agent/) - Skill docs for pi RPC patterns
