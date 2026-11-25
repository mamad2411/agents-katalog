---
name: use-oox
description: Use the OOX JoAi app plugin when the task needs OOX tools or workflows.
---

# OOX

Connect OOX to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the OOX tools available in this app.
- Explain what setup or authentication OOX needs before I run an action.
- Use OOX to help me with the task I describe next.

## Action Inventory

- `oox-accept-offer` (contract) — Accept an offer made for your NFT. The NFT will be transferred to the buyer and you will receive the payment.
- `oox-auction-token` (contract) — Create an auction for your NFT or SFT on OOX marketplace. Set minimum and maximum bid prices, deadline, and accepted payment token.
- `oox-bid` (contract) — Place a bid on an active auction. Your bid must be higher than the current highest bid.
- `oox-buy` (contract) — Buy an NFT directly from an auction at the buy-now price (if available).
- `oox-claim-tokens` (contract) — Claim tokens that you have earned from sales or auctions on the marketplace.
- `oox-create-vending-machine` (contract) — Create a vending machine to sell multiple NFTs at a fixed price. Buyers can mint NFTs directly from your machine.
- `oox-end-auction` (contract) — End an active auction. If there are bids, the highest bidder wins. If no bids, the NFT is returned to the seller.
- `oox-get-full-auction-data` (contract) — Retrieve detailed information about an auction including current bid, deadline, and auction details.
- `oox-get-full-offer-data` (contract) — Retrieve detailed information about an offer including payment amount, deadline, and offer details.
- `oox-mint-from-machine` (contract) — Purchase and mint an NFT from a vending machine at the fixed price.
- `oox-modify-auction-price` (contract) — Update the minimum and/or maximum bid price for your active auction.
- `oox-send-offer` (contract) — Send an offer to purchase a specific NFT. The NFT owner can accept your offer.
- ...and 2 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
