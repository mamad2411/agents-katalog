---
name: use-xexchange
description: Use the xExchange JoAi app plugin when the task needs xExchange tools or workflows.
---

# xExchange

Connect xExchange to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the xExchange tools available in this app.
- Explain what setup or authentication xExchange needs before I run an action.
- Use xExchange to help me with the task I describe next.

## Action Inventory

- `xexchange-swap-ash-to-wegld` (contract) — Swap ASH to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-busd-to-wegld` (contract) — Swap BUSD to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-crt-to-wegld` (contract) — Swap CRT to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-egld-to-mex` (contract) — Swap WEGLD to MEX tokens on xExchange. Exchange WEGLD for MEX in the EGLD/MEX liquidity pair with slippage protection.
- `xexchange-swap-emr-to-usdc` (contract) — Swap EMR to USDC tokens on xExchange Devnet.
- `xexchange-swap-emr-to-wegld` (contract) — Swap EMR to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-htm-to-usdc` (contract) — Swap HTM to USDC tokens on xExchange Devnet.
- `xexchange-swap-htm-to-wegld` (contract) — Swap HTM to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-itheum-to-wegld` (contract) — Swap ITHEUM to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-kwak-to-wegld` (contract) — Swap KWAK to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-legld-to-wegld` (contract) — Swap LEGLD to WEGLD tokens on xExchange Devnet.
- `xexchange-swap-lxoxno-to-xoxno` (contract) — Swap LXOXNO to XOXNO tokens on xExchange Devnet.
- ...and 33 more actions exposed by the hosted MCP app server.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
