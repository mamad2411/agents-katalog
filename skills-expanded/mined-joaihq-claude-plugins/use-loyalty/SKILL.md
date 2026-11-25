---
name: use-loyalty
description: Use the Loyalty JoAi app plugin when the task needs Loyalty tools or workflows.
---

# Loyalty

Connect Loyalty to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Loyalty tools available in this app.
- Explain what setup or authentication Loyalty needs before I run an action.
- Use Loyalty to help me with the task I describe next.

## Action Inventory

- `loyalty-configure` (contract) — Set up your stamp-based loyalty program — rewards, Google review incentive, and reminder frequency.
- `loyalty-create` (contract) — Register your loyalty program on-chain. Uses your team slug as the unique identifier.
- `loyalty-redeem` (query, contract) — Redeem a customer's loyalty reward and reset their stamps.
- `loyalty-register` (query, collect, contract) — Register your loyalty card and start earning stamps towards free rewards.
- `loyalty-remind` (query, query) — Check for customers who haven't visited recently and send them a reminder.
- `loyalty-review` (query) — Rate us on Google and get a discount on your next visit.
- `loyalty-setup` (compute) — Program NFC cards for your loyalty program. All cards get the same agent URL — the NFC chip's hardware ID is the unique card identity.
- `loyalty-stamp` (query, contract) — Scan a customer's loyalty card to add a stamp and track their reward progress. Automatically shows the current stamp count and notifies when a reward is ready to be redeemed.
- `loyalty-status` (query) — Check your stamp progress and available rewards.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
