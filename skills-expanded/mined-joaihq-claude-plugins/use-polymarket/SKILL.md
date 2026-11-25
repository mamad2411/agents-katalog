---
name: use-polymarket
description: Use the Polymarket JoAi app plugin when the task needs Polymarket tools or workflows.
---

# Polymarket

Connect Polymarket to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Polymarket tools available in this app.
- Explain what setup or authentication Polymarket needs before I run an action.
- Use Polymarket to help me with the task I describe next.

## Action Inventory

- `polymarket-buy-shares` (collect) — Buy shares in a prediction market on Polymarket. Purchase 'Yes' or 'No' shares for a specific market outcome using the CLOB API.
- `polymarket-claim-winnings` (contract) — Claim your winnings from a resolved prediction market on Polymarket. Exchange winning shares for USDC using the Conditional Token Framework.
- `polymarket-create-market` (collect) — Create a new prediction market on Polymarket. Define the market question, outcomes, and resolution criteria using the Gamma API.
- `polymarket-get-active-predictions` (collect) — Retrieve the latest active prediction markets from Polymarket showing current predictions, volumes, and end dates.
- `polymarket-get-collection-id` (query) — Calculate the collection ID from parent collection, condition ID, and index set using the Conditional Token Framework.
- `polymarket-get-condition-info` (query, query) — Retrieve information about a prediction market condition including outcome slot count and condition details from the Conditional Token Framework.
- `polymarket-get-latest-markets` (collect) — Retrieve the latest active prediction markets from Polymarket using the Data API.
- `polymarket-get-position-balance` (query) — Retrieve the balance of a specific position (shares) for a user in a prediction market from the Conditional Token Framework.
- `polymarket-get-position-id` (query) — Calculate the position ID from collateral token address and collection ID using the Conditional Token Framework.
- `polymarket-resolve-market` (collect) — Resolve a prediction market by setting the winning outcome. Only authorized resolvers can resolve markets using the Gamma API.
- `polymarket-sell-shares` (collect) — Sell your shares in a prediction market on Polymarket. Exchange your position shares for USDC using the CLOB API.
- `polymarket-view-latest-predictions` (collect) — View the latest active prediction markets on Polymarket with current prices, volumes, and end dates. See what people are predicting right now.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
