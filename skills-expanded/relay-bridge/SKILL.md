---
name: relay-bridge
description: "Use when preparing a Relay quote or tracking a cross-chain request through source confirmation, destination execution, delay or refund."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.4.1"
---

# Relay bridge

Produce a route comparison or reconcile a single Relay request. Start recovery from its request ID and source hash, not a replacement quote.

## Read a versioned quote

Collect source/destination chains, exact currency identities, raw input or output amount, user, recipient and trade type. Use current `/quote/v2` in [reads](references/reads.md); the old `/quote` is deprecated. Current `/quote/v2` requires a valid `x-api-key` from private configuration; respect the configured app limits. On 401/403 report missing access without changing account or payment scope.

Preserve top-level requestId and all steps/items. A quote can require signatures, approvals and transactions on different chains; inspect each item kind and exact payer before handoff. Verify returned amount bounds, route, gas, relayer/application fees and expected duration. Keep native gas additional to input separate from fees already included in output.

## Review every step

For transaction items decode chainId, sender, target, value and data. For signature items inspect typed domain, spender, amount, nonce and expiry. Verify the ultimate destination recipient rather than only the intermediate depositor. Deposit-address and permit flows have different lifecycle identities; use their current documented request checks instead of inventing a generic transaction.

Quote terms are not signing authority. Return the ordered unsigned steps, expiry and limits. If a changed amount or recipient alters the quote, rebuild the entire bound plan. Do not insert app fees or skip a failed prerequisite.

## Track delivery or refund

Query current status v3 with the same requestId. Retain source hashes and destination/refund hashes separately. `delayed`, `pending`, `submitted`, refund or failure labels require different evidence; destination submission is not final success. Read actual destination receipt and beneficiary token deltas against the accepted minimum.

For a refund identify chain, recipient, currency and net amount. A refunded source obligation is not payment at the destination. If the status endpoint is delayed or unknown, use original onchain evidence and a bounded next-check time; never repair uncertainty by another deposit.

## Worked result

Synthetic 1,000-USDC request has a source-confirmed deposit and Relay status delayed; no destination hash exists. Report funds in transit, the same requestId and the missing destination stage. If a later 997-USDC refund reaches the origin owner, report refunded with 3-USDC cost, while the intended recipient remains unpaid.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
