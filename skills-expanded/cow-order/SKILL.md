---
name: cow-order
description: "Use when comparing a CoW Protocol quote, reviewing a signed-intent boundary, or reconciling order UID, partial fills, expiry and cancellation."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.4.1"
---

# CoW order

Return a CoW quote or an order-specific execution ledger. Posting an intent returns an order UID; it does not establish a mined trade.

## Read and bound the intent

Collect chain, owner, receiver, exact tokens/decimals, sell or buy kind, fixed raw amount, validity and partial-fill preference. Use the official SDK quote-only path or Order Book API in [reads](references/reads.md). Resolve supported chain and deployed settlement/relayer identities; do not infer support from a token symbol.

Inspect quote amounts, fee treatment and returned validity. Preserve whether sell amount includes fees. Compare only same-kind quotes with the same fixed amount and recipient. Record appData, hooks and any added fee recipient; a hook may introduce external calls and must be decoded rather than ignored as metadata.

Before an unsigned handoff show allowance spender, order fields, EIP-712 domain, validity, partial-fill flag, receiver and minimum buy or maximum sell. Use a matching maintained SDK wallet adapter only for a separately authorized signing flow. Do not invoke `postSwapOrder` to obtain an indicative quote: higher-level methods may sign and post.

## Reconcile one order

For an existing UID read status, executed sell/buy totals and trades; match settlement receipts and recipient deltas. Track remaining executable amount and time. Multiple solver fills can complete one partially fillable order. Expiry stops future fills but does not undo those already settled.

Cancellation is its own signed/onchain action depending on the chosen path. A cancellation request can race a fill; read final trades and invalidation state before saying it cancelled everything. If submission times out, derive/query the same order UID with the reviewed order data before any new signature. Do not create duplicate open intents to repair a missing response.

## Worked result

Synthetic sell order allows partial fills for 1,000 USDC. Trades show 400 USDC sold for 0.16 WETH; 600 USDC remain while valid. Report a 40% fill and residual intent, not a failed swap or 1,000-USDC execution. If it later expires without more trades, report that final partial result. Reconcile the received 0.16 WETH onchain before calling it independently verified.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
