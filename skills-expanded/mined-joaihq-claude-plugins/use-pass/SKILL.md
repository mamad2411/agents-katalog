---
name: use-pass
description: Use the Pass JoAi app plugin when the task needs Pass tools or workflows.
---

# Pass

Connect Pass to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Pass tools available in this app.
- Explain what setup or authentication Pass needs before I run an action.
- Use Pass to help me with the task I describe next.

## Action Inventory

- `pass-generate` (collect) — Generate a mobile wallet pass for Apple Wallet or Google Wallet from an existing coupon or loyalty card. The pass appears directly on the customer's phone.
- `pass-update` (collect) — Push updated data to an existing mobile wallet pass. Changes appear on the customer's phone within about a minute.
- `pass-void` (collect) — Permanently expire a wallet pass so it no longer appears active on the customer's device. Use this when a coupon is revoked or a loyalty card is cancelled.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
