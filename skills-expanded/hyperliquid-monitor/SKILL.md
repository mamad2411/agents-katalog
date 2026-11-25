---
name: hyperliquid-monitor
description: "Reconcile a Hyperliquid account, position, order, fill, funding stream, liquidation buffer, or watch from current exchange data. Use when the user asks what is open, whether protection exists, whether an order filled, how close liquidation is, what changed, or to watch and alert on a condition. Read-only; not for placing, changing, or canceling orders."
license: MIT
compatibility: "Requires read-only Hyperliquid API access and the user account address. The bundled funding script needs Node.js 20 or newer."
metadata:
  version: "0.4.2"
  protocol: "hyperliquid"
---

# Hyperliquid monitor

Reconstruct current exchange state and distinguish safe, triggered, and unavailable observations.

## Tools and resources

Read [the tool contract](references/official-tools.md) only when selecting or verifying a capability. Resolve scripts and references from this skill's directory. Related skills are optional handoffs; their absence is not permission to invent state or bypass a prerequisite.

## Task

Reconcile one requested public user account from read-only tools and report positions, protection, timestamps and gaps. A failed read is unavailable, never an empty healthy account.

## Task handling

Reuse the requested account or position identity, then verify it from current reads. Ask only for missing identity or monitoring constraints; never substitute another account. Finish unaffected checks when a source fails and mark the affected result unavailable. Report the current state, material changes, and next required read concisely, retaining the output contract.

## Workflow

1. Bind the network, user account address, account abstraction mode, DEX, markets, observation time, freshness bound, and requested condition.
2. Read [authoritative state](references/authoritative-state.md). Query the account or subaccount being monitored, never the API wallet address.
3. Reconcile positions, balances, open orders, trigger details, order status, fills, funding, ledger updates, fee tier, and action budget. Under unified or portfolio margin, include spot clearinghouse and borrow/lend state.
4. Check every open position against [protection and incidents](references/protection-and-incidents.md). Match stop side, reduce-only state, trigger, size, and position-tied status.
5. Normalize funding by its stated interval. Use `node scripts/funding.mjs --help` for arithmetic. Preserve funding signs from the account's perspective.
6. For continuous work, use [stream discipline](references/stream-discipline.md). Snapshot first, deduplicate, heartbeat, detect gaps, and reconcile after reconnect.
7. Evaluate the condition as exactly one of `triggered`, `not-triggered`, or `unavailable`. A failed, empty, stale, partial, or gapped read is unavailable.
8. Emit [the monitor contract](references/output-contract.md). Alerts state facts and open a plan; they never act.

## Hard rules

- `frontendOpenOrders` or an equivalent detailed stream is required to prove trigger and reduce-only properties.
- Order response text is not final state. Use order status, open orders, fills, and position state together.
- `liquidationPx` is a live estimate. Cross, unified, and portfolio modes couple risk across positions and balances.
- The first fills message on a subscription may be a snapshot. Do not alert on it as new activity.
- An open candle changes until close. Label intrabar signals.
- WebSocket reconnect without backfill creates an unknown interval.
- A scheduled cancel can remove protective stops. It is not a position-aware safety system.

## Boundary

Do not place, modify, cancel, close, change leverage, transfer, or submit any exchange action. State the exact next read or unsigned action needed. Route a requested action to `hyperliquid-plan` or `hyperliquid-execute`.
