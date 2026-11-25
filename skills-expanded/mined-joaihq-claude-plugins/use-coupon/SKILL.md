---
name: use-coupon
description: Use the Coupon JoAi app plugin when the task needs Coupon tools or workflows.
---

# Coupon

Connect Coupon to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Coupon tools available in this app.
- Explain what setup or authentication Coupon needs before I run an action.
- Use Coupon to help me with the task I describe next.

## Action Inventory

- `coupon-browse` (collect) — Browse available discount coupons and claim one to your wallet.
- `coupon-claim` (contract) — Claim a discount coupon to your wallet. The coupon is sent as an SFT that you hold until you redeem it.
- `coupon-create` (collect, contract) — Create a discount coupon as an SFT in your collection. Customers can claim and hold the coupon in their wallet, then redeem it at checkout. All details are stored on-chain.
- `coupon-create-collection` (contract) — Create an SFT collection on the blockchain for your discount coupons. Each collection groups all coupons for a brand or campaign. Requires 0.05 EGLD for the ESDT issuance fee.
- `coupon-list` (query) — View all discount coupons you have created on-chain.
- `coupon-manage` (collect) — View and manage your discount coupons — revoke, check status.
- `coupon-redeem` (collect, contract) — Redeem a coupon SFT from your wallet at checkout. Send the coupon token to the contract — it gets burned and the discount is returned.
- `coupon-revoke` (contract) — Permanently deactivate a coupon. Remaining SFTs are burned and customers can no longer claim or redeem it.
- `coupon-view` (query) — Look up a coupon by code — see the discount, usage count, expiry, and status.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
