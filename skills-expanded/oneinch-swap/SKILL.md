---
name: oneinch-swap
description: "Use when quoting a 1inch Classic Swap v6.1 or distinguishing direct calldata, Fusion intents and protected API access."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.4.1"
---

# 1inch swap

Produce a 1inch Classic swap quote or a lifecycle diagnosis. Identify the product first: a Classic transaction and a Fusion signed intent have different submission and settlement paths.

## Quote the selected product

Collect chain, exact src/dst token addresses, decimals, raw input, calling sender (`from`), initiating EOA (`origin`), receiver and cost/slippage limit. Keep `from` and `origin` distinct for contract wallets. For Classic use the protected v6.1 API in [reads](references/reads.md), retaining private Bearer authentication. Public documentation/MCP search does not establish permission or entitlement for protected quote APIs.

Request the quote and verify destination amount, token identities, selected liquidity routes and gas. Use `/approve/spender` and `/approve/allowance` to inspect current spending requirements. A quote does not need a new unlimited approval. For unsigned `/swap` construction include exact sender/receiver and slippage in the documented percentage unit; `1` means 1%, not one basis point.

## Review calldata and intent scope

Check returned transaction `from`, `to`, `value`, data, chain and minimum output against the request. Retain token allowances separately from swap calldata. Resolve the router using current official deployment information. Keep partner fee settings equal between quote and construction, and do not insert a new fee or referrer.

If the requested flow is Fusion/Fusion+, use its official order builder and status interface instead of sending Classic calldata or assuming an offchain signature executed. Decode typed order domain, expiry, receiver, amount bounds and cancellation semantics before an authorized wallet handoff. This skill supplies no signer.

## Reconcile the original action

For Classic, receipt status plus recipient token deltas establishes execution. For an intent, retain the order identity, fills and remaining amount; partial fill or expiry is not full delivery. On ambiguous send query the original transaction/order before creating another. A quote error, unsupported chain, expired quote or access rejection remains an explicit gap; do not disable estimation merely to hide a failing transaction.

## Worked result

Synthetic Classic quote: 1,000 USDC gives 999 DAI estimate; user permits 0.5% slippage. The plan must show the exact constructed minimum and fees, not promise 999 DAI. If the actual mined recipient delta is 998 DAI and meets that minimum, report 998 delivered plus gas. A Fusion order accepted with no fills remains open, regardless of its quote estimate.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
