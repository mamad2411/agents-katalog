---
name: across-bridge
description: "Use when comparing Across API quotes, inspecting exact_input versus min_output, or reconciling transfer status, destination actions and refunds."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.5.0"
---

# Across bridge

Return an exact Across route plan or a transfer settlement ledger. Current API access requires a Bearer API key from the Across dashboard. The legacy `integratorId` is not sent. Installing a skill supplies neither a key nor permission to transfer.

## Quote the requested amount semantics

Collect origin and destination chain ids, token addresses, decimals, depositor, recipient, amount and objective. Current quotes are `POST /v1/quotes` on `https://api.across.to`, as described in [reads](references/reads.md). The Swap API (`/swap/*`), suggested-fees and deposit-status routes are deprecated. Discover supported chains and tokens with `GET /v1/capabilities` rather than assuming old routes remain active.

For `amountType` `exact_input`, `origin.amount` is the input-token budget in base units. For `min_output` or `exact_output`, `destination.amount` is the output amount; compare the returned required input with the user's budget. Preserve `orderId`, `expiresAt`, `destination.amount`, `destination.minAmount`, `maxFee`, `nextActions` and refund fields. `maxFee.bps` is basis points of total value loss, not a fraction: `100` is 1%. Do not send legacy `slippage` (`0.005` or `auto`) or append an app fee the user did not set.

## Inspect source and destination effects

Decode each `nextActions` entry by `kind`. An `approve_token` spender is separate from a later `send_transaction` target. For destination actions inspect ultimate recipient, target, token amount, downstream calldata and refund behavior. Delivery to a handler does not prove the final beneficiary received the requested asset or shares. Inspect dynamic-balance actions against the actual destination inventory instead of using a stale estimated amount.

Return unsigned source prerequisites and destination expectations. A wallet-capable MCP tool is not a read merely because the server also has quote tools; inspect the tool's effects and preserve the user's existing signing boundary.

## Track one transfer

Persist the quote `orderId`. Query `GET /v1/transfers/{orderId}`, retain fill and refund references, and inspect destination actions separately from `status.state`. A 404 shortly after submission is not proof of failure. A list response can contain multiple transfers; disambiguate rather than selecting the first.

A completed source receipt is incomplete delivery. Completion needs `status.state` `completed`, the correct destination token, recipient and amount and, if requested, a successful downstream action. `completed` with reason `filled_destination_action_failed` means the bridge finished and the destination action did not. On pending, failed action, refund or timeout retain the same `orderId` and do not open a second transfer to repair the first.

## Worked result

Synthetic `min_output` request asks for 1,000 USDC on Base; returned source requirement is 1,004 USDC and budget is 1,002. Report route over budget and leave it unsigned. Separately, `status.state` `completed` with reason `filled_destination_action_failed` and zero vault shares is `bridge completed; vault objective unmet`; reconcile fallback tokens and refund before proposing any remedy.

## Sources and limits

Primary documentation and source reviewed 2026-11-11; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
