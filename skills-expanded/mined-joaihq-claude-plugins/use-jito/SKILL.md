---
name: use-jito
description: Use the Jito JoAi app plugin when the task needs Jito tools or workflows.
---

# Jito

Connect Jito to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Jito tools available in this app.
- Explain what setup or authentication Jito needs before I run an action.
- Use Jito to help me with the task I describe next.

## Action Inventory

- `jito-liquid-stake` (contract) — Stake SOL to secure the network and earn rewards using Jito Liquid Staking. Receive JitoSOL tokens in return.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
