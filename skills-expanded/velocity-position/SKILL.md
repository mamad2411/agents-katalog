---
name: velocity-position
description: "Use when inspecting Velocity Exchange Solana positions and margin or distinguishing paused legacy Drift accounts from the new Velocity deployment."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.2.1"
---

# Velocity position

Return a deployment-specific Velocity position assessment. Official migration guidance says the original Drift program is paused; Velocity has a new program, new account layouts and no transferred onchain state. A legacy Drift address is not a Velocity balance.

## Verify program and source generation

Collect cluster, RPC, public owner/subaccount and market. Resolve the current Velocity program ID and SDK version from official deployment/source records, then verify the onchain account owner. Use `@velocity-exchange/sdk` with its matching account layout. Do not decode a Velocity account with archived Drift types because a discriminator happens to match.

If the user supplied a Drift account, identify its original program and observed legacy state first. Report migration as unresolved unless actual new-program account evidence exists. Do not describe a program rename as automatic asset migration or create new funded accounts as setup.

## Read fresh subscriptions and risk

Use the existing read client or version-matched account decoding in [reads](references/reads.md). SDK `subscribe()` can return false; check it explicitly. Record slot, market/oracle freshness and subscription health, then read positions, collateral, orders and margin with official SDK math. A connected RPC with a failed subscription is not current market evidence.

Keep BN integer precision for quote, base, price and funding calculations; convert only for display. Separate oracle price, vAMM bid/ask and order-book depth. Evaluate stale oracle, open-order margin, funding, liquidation and reduce-only behavior under the deployed program's actual limits.

## Return and reconcile

An unsigned plan names program, subaccount, market index, side, base amount, limit, reduce-only flag, fees and margin before/after. SDK methods such as `placePerpOrder` send transactions; do not invoke them as read checks. Current delegate/Swift permissions must be inspected rather than assumed harmless.

For an existing signature inspect confirmation, transaction errors, fills and resulting position/orders. An accepted order can be resting. On timeout query the original signature and account before another send. Close subscriptions when the bounded read finishes; do not leave a polling service running.

## Worked result

Synthetic legacy Drift account shows 5 SOL exposure; the same owner has no discovered Velocity user account. Report legacy 5 SOL and no verified Velocity exposure. If a new-program subscription returns false, report failed data readiness, not zero positions or permission to initialize a wallet.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
