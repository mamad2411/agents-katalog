---
name: jupiter-swap
description: "Use when quoting Jupiter Swap v2 on Solana, inspecting immutable order transactions, or reconciling managed execution and token-account deltas."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.4.1"
---

# Jupiter swap

Produce a Jupiter quote or a Solana swap outcome. Choose the v2 `/order` path for an assembled transaction or `/build` for custom instructions; their routing and landing responsibilities differ.

## Quote without wallet authority

Collect input/output mint addresses, mint decimals, raw input amount, desired recipient and optional public taker. Use [reads](references/reads.md). Current docs allow quote-only `/order` without a key or taker, at lower limits. An API key can raise limits; discovering the docs MCP does not establish a trading connection.

Without taker, expect a quote and null transaction. Adding taker can construct an assembled transaction. Inspect router, fee basis, price impact, input/output amounts, slippage, request ID and expiry information. Track SOL gas/rent and any extra payer separately from SPL token spend.

## Inspect the transaction boundary

For `/order` + `/execute`, keep the returned transaction immutable. Resolve all lookup-table addresses, instructions, writable accounts, token mints, destination accounts, signers, compute budget and priority fees before a wallet handoff. Do not append instructions to an RFQ/managed transaction. If custom composition is needed, choose `/build` and re-evaluate its route and self-managed landing path.

Signing, `/execute` and transaction submission are financial actions. Return unsigned terms for planning. A quote refresh, changed payer, mint or amount invalidates the previous transaction/approval review. Do not insert a referral fee.

## Reconcile managed landing

Preserve request ID and original transaction signature. Inspect execution response and Solana confirmation/transaction meta, including errors and pre/post token balances at the exact destination token account. Wallet SOL changes include fees/rent and are not the swap output. A signature or HTTP success alone is insufficient.

On blockhash expiry or timeout, query the original signature before rebuilding; an order may have landed despite a lost response. Report a partial observation or missing archival data rather than inventing a fill. Use bounded backoff for keyless rate limits.

## Worked result

Synthetic quote for 0.1 SOL has no taker and `transaction: null`. Return the price estimate only, with no signing requirement. Later an execution endpoint returns a signature, but meta has an error and USDC delta is zero: report failed execution and actual SOL fee, not successful delivery because a signature exists.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
