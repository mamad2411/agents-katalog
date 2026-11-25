---
name: zerox-swap
description: "Use when quoting a 0x API v2 swap or inspecting AllowanceHolder, Permit2, issues and minimum-output evidence before an unsigned handoff."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.4.1"
---

# 0x swap

Return a quote comparison or an exact unsigned 0x swap plan. Choose an allowance flow deliberately; do not treat the transaction target as the token spender.

## Read the exact swap

Collect chain ID, sell/buy token addresses and decimals, raw sell amount, public taker, recipient and the user's slippage/cost limit. Use the API v2 AllowanceHolder price and quote endpoints in [reads](references/reads.md). Existing API credentials stay in private environment settings. API access and paid CLI requests are different spending choices; do not enable a payment gateway merely to make a diagnostic pass.

Use `/price` for exploration. A firm `/quote` requires the correct taker and fresh balance/allowance state. Inspect liquidity availability, `issues.balance`, `issues.allowance`, `simulationIncomplete`, route, fee fields, expected `buyAmount` and `minBuyAmount`. Missing liquidity, unsupported token behavior or incomplete simulation is a concrete gap, not a successful quote.

## Bind allowance and transaction

For AllowanceHolder resolve the returned allowance spender against current official deployment records. For Permit2 inspect typed data, amount, nonce, spender, domain and deadline independently. Never approve Settler. Verify `transaction.to`, data, native value and chain against the quoted intent; execution target and approval target can differ.

Return finite allowance needs and an unsigned handoff with exact minimum output, costs, recipient and quote age. After any changed amount, token, chain or approval state, refresh the quote; signatures and calldata are bound to the reviewed terms. Do not inject affiliate fees or a surplus recipient.

## Resolve the result

A quote, successful simulation or send response is not a fill. For a submitted swap inspect the original receipt and sell/buy token deltas at the correct recipient, including actual native gas. On timeout retain the original hash and inspect it before any retry. On 401/403 report missing access; on rate limits respect retry-after rather than changing auth or payment scope.

## Worked result

Synthetic quote sells 100 USDC, expects 0.040 WETH and requires at least 0.0398 WETH. The allowance spender is AllowanceHolder while calldata targets Settler. Return those as separate identities, a 0.0398-WETH floor and finite 100-USDC allowance need. A proposal to approve Settler must be rejected before any wallet handoff.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
