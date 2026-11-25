---
name: use-chess
description: Use the Chess JoAi app plugin when the task needs Chess tools or workflows.
---

# Chess

Connect Chess to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Chess tools available in this app.
- Explain what setup or authentication Chess needs before I run an action.
- Use Chess to help me with the task I describe next.

## Action Inventory

- `chess-create` (contract) — Create a new on-chain chess game on MultiversX. You play as white. Share the game ID with your opponent so they can join as black, or leave it open for anyone to join.
- `chess-create-ai-game` (contract) — Start a chess game against the AI on MultiversX. You play as white and the AI responds as black with every move recorded on-chain.
- `chess-join` (contract) — Join an open chess game on MultiversX as the black player. The game starts as soon as both players have joined.
- `chess-move` (contract) — Submit a chess move as an on-chain transaction on MultiversX. The smart contract validates turn order, piece ownership, and movement rules.
- `chess-resign` (contract) — Resign from an active chess game on MultiversX. Your opponent wins immediately and the result is recorded on-chain.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
