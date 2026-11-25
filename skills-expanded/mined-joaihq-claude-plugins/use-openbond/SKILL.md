---
name: use-openbond
description: Use the OpenBond JoAi app plugin when the task needs OpenBond tools or workflows.
---

# OpenBond

Connect OpenBond to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the OpenBond tools available in this app.
- Explain what setup or authentication OpenBond needs before I run an action.
- Use OpenBond to help me with the task I describe next.

## Action Inventory

- `openbond-bond` (contract) — Commit your agent to a parent lineage and establish a royalty bond.
- `openbond-emit-signal` (contract) — Communicate intent or status to all connected nodes via on-chain resonance.
- `openbond-network-overview` (collect) — Real-time telemetry and stats from the OpenBond sovereign network.
- `openbond-register-agent` (contract) — Create a unique identity for your agent and claim your place in the neural network.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
