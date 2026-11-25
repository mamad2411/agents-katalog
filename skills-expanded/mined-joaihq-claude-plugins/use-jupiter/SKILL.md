---
name: use-jupiter
description: Use the Jupiter JoAi app plugin when the task needs Jupiter tools or workflows.
---

# Jupiter

Connect Jupiter to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Jupiter tools available in this app.
- Explain what setup or authentication Jupiter needs before I run an action.
- Use Jupiter to help me with the task I describe next.

## Action Inventory

- `jupiter-swap-quote` (collect) — Get the best swap quote from Jupiter DEX aggregator on Solana. Compares routes across multiple liquidity sources to find the optimal price for your token swap.
- `jupiter-token-price` (collect) — Retrieve the current USD price of any Solana token using the Jupiter Price API. Returns price, decimals, 24h price change, and liquidity data.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
