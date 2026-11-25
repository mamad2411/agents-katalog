---
name: pendle-boros
description: "Use when reviewing Boros funding-rate derivatives, implied versus realized rates, margin and delegated-agent scope before any trading action."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.2.1"
---

# Pendle Boros

Produce a Boros rate-exposure assessment or reconcile one order. Boros funding-rate instruments are distinct from Pendle PT/YT tokens and from the underlying venue's perpetual position.

## Read the market and rate convention

Collect exact Boros market ID, expiry, rate underlying, side, notional, collateral/account and comparison objective. Use existing official data tools or API/SDK in [reads](references/reads.md). Resolve the funding-rate symbol and annualization/unit convention before comparing prices. Preserve remaining term, order-book depth, mark rate, actual funding observations and margin mode.

Separate implied fixed-rate exposure from realized floating funding. Use the official SDK's tick/rate and contract-size math; raw ticks are not annual percentages. Identify whether a proposed position receives or pays fixed/floating under the actual market convention instead of assigning a side from the word long alone.

## Model bounded scenarios

Compare rate paths over the same term and notional, then include fees, funding settlement, margin calls and gas treasury charges. A hedge across venues retains separate margin pools and liquidation risks. A favorable fixed-versus-floating spread does not guarantee profit or eliminate funding volatility.

Return an unsigned market/side/size/limit/expiry plan, account mode and risk evidence. The official local Boros MCP can sign with stored delegated keys and uses browser callbacks for owner actions. Adding it, setting up an agent or topping up gas is not a read-only prerequisite. Select only discovered read tools for research; keep credentials inside the user's existing trusted wallet setup.

## Track order and account state

Retain order ID and transaction identity. Reconcile actual fills, remaining orders, entered markets, collateral and settlement history. Agent approval needs the correct root account, unexpired status and bounded scope; existence of an address alone proves none of those. Do not create or revoke an agent without authorization.

On an ambiguous response inspect original order/chain events before another call; delegated tools may have signed without a browser prompt. On unavailable methods or mixed SDK generations report the gap rather than improvising an execution adapter.

## Worked result

Synthetic $10,000 rate exposure for 30/365 year: fixed 8% versus realized average 10% differs by about $16.44 before fees, under an explicitly stated linear simple-rate model. This is scenario arithmetic, not protocol settlement math or a guaranteed hedge. Report separate margin requirements and use official math for an executable plan.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
