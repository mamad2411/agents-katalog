---
name: derive-options
description: "Use when reviewing Derive v3 option instruments, premium and margin scenarios, or reconciling subaccount orders, fills and session scope."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.2.1"
---

# Derive options

Produce an option-specific Derive v3 decision with premium, Greeks, margin and expiry evidence. Do not combine v2 authentication or instrument formats with the current v3 API.

## Identify the contract and portfolio

Collect exact instrument_name, side, quantity, public/subaccount identity, collateral and objective. Resolve the market's risk universe, option strike/type, exact expiry timestamp and settlement asset. Names encode an eight-digit expiry date, but the actual expiry time can vary by market; read `option_details.expiry` rather than applying a universal UTC hour.

Use the current public ticker and dry-run APIs in [reads](references/reads.md), or existing properly scoped account reads. Record mark/index, bid/ask sizes, Greeks, fee quote and observation time. A mark is a valuation input, not executable depth. Keep decimal strings until calculation boundaries.

## Model premium and margin

Separate premium paid/received, fees and notional. A fully paid long option's premium exposure differs from a short option's collateral and potentially large loss. Evaluate spot/volatility/time scenarios with the venue's matched margin manager and risk universe. The public margin simulation returns net margin; positive is headroom. It excludes open-order margin, so include pending-order obligations from account evidence before claiming account readiness.

A dry-run `public/order_quote` is an estimate, not a trade. For a requested unsigned order, show subaccount, exact instrument, amount, direction, limit, max fee, reduce-only/time-in-force and expiry. Session creation or Trade/Admin scope changes are distinct authority actions; never create keys for research.

## Reconcile lifecycle

Retain order ID, nonce and subaccount; read current order, trades, positions and settlement history. Partial fills change Greeks and margin while unfilled quantity can remain live. Cancellation can race a fill. At expiry distinguish stale displayed positions from actual settlement and balance changes.

On auth, version, instrument or risk-universe mismatch report the exact gap. After ambiguous submit query original order/nonce before another signed action. Do not assume a session metadata edit revoked onchain permission.

## Worked result

Synthetic long call: quantity 2, premium 120 each, fee 3 total. Initial premium cost is 243 settlement units; it is not the strike notional. Public simulation returns +500 net initial margin, but open orders require 600 additional margin. Report the missing 100 headroom after those obligations and avoid calling the account ready from public simulation alone.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
