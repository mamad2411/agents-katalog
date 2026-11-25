---
name: use-solana
description: Use the Solana JoAi app plugin when the task needs Solana tools or workflows.
---

# Solana

Connect Solana to Claude, Cursor, and ChatGPT through JoAi's hosted MCP app server.

If a specific task was given, identify the relevant MCP tool and call it immediately — no preamble.

If invoked with no task, call the authenticate tool first (if present), then list the available actions concisely so the user can pick one.

Never ask "what would you like to do?" — either act on the task or show the menu.

## Example Prompts

- List the Solana tools available in this app.
- Explain what setup or authentication Solana needs before I run an action.
- Use Solana to help me with the task I describe next.

## Action Inventory

- `solana-account-info` (collect) — Retrieve detailed Solana account data via the Solana JSON RPC API. Check lamport balance, SOL balance, owner program, and executable status for a wallet address. Ideal for wallet status checks, balance tracking, and account inspection on the Solana blockchain.
- `solana-account-nfts` (collect) — Discover NFTs owned by a Solana wallet using the Solana JSON RPC API. Filters SPL token accounts to NFT-like assets (0 decimals, amount > 0) to provide a quick NFT overview.
- `solana-account-tokens` (collect) — List SPL token accounts for a Solana wallet using the Solana JSON RPC API. See token mints, balances, and decimals to track your token portfolio on the Solana blockchain.
- `solana-account-transaction-count` (collect) — Count recent transaction signatures for a Solana wallet using the Solana JSON RPC API. Uses getSignaturesForAddress with a configurable limit to estimate recent activity.
- `solana-account-transactions` (collect) — Retrieve recent transaction signatures for a Solana wallet via the Solana JSON RPC API. Inspect signatures, slots, and block times to track wallet activity on the Solana blockchain.
- `solana-burn-tokens` (contract) — Burn (destroy) SPL tokens from your token account using the Solana Token Program. Permanently removes tokens from circulation by reducing the supply.
- `solana-revoke-delegate` (contract) — Revoke a delegate's approval to spend tokens from your token account using the Solana Token Program. Removes any previously granted spending permission.
- `solana-transfer-spl-token` (transfer) — Transfer an SPL token to another address on Solana. Supports any SPL token by specifying the mint address. Automatically creates the recipient's associated token account if needed.

## Usage Notes

- Every listed action becomes an MCP tool when the app server is connected.
- Prefer the generated provider plugin when one is available, and fall back to the raw MCP URL otherwise.

## Auth Notes

- Some actions require provider credentials or OAuth on first use.
