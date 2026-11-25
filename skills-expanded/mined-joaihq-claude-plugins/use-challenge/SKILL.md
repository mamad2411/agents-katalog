---
name: use-challenge
description: Use the Challenge JoAi app plugin when the task needs Challenge tools or workflows.
---

# Challenge

Connect Challenge to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Challenge tools available in this app.
- Explain what setup or authentication Challenge needs before I run an action.
- Use Challenge to help me with the task I describe next.

## Action Inventory

- `challenge-accept` (contract) — Match the stake and bet that the challenger will fail. If they skip — you take it.
- `challenge-create` (contract) — Commit to something and stake tokens on it. If you prove it — you keep your stake. If you skip — the challenger takes it.
- `challenge-list` (query) — Browse open challenges waiting for someone to take the bet.
- `challenge-resolve` (contract) — Mark a challenge as succeeded or failed after verification. Owner only.
- `challenge-view` (query) — See the details, stake, and status of a challenge.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
