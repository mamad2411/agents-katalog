---
name: revert-position
description: "Use when inspecting a Revert-indexed LP position or preparing a Revert unsigned liquidity action, including custody, quote digests and approval-phase rebuilds."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.7.1"
---

# Revert position

Return a position assessment or a bounded unsigned Revert plan. Revert is an optional provider; do not move a normal LP task into Revert custody without a user-selected reason.

## Inspect the actual capability

Collect public account, network, protocol and position identity. On an existing Revert MCP connection discover the current schemas, call `get_protocol_capabilities` for the selected venue and `get_chain_status` for freshness. Then use `get_positions(account=...)` and `get_position_details` with that exact identity. Preserve pagination and observation age. A venue supported for reads may not support unsigned construction.

Separate directly owned NFTs, gauge custody and Revert Lend collateral. Read principal, collectible fees, debt and owner independently. If this is only a PnL question, report available cash-flow coverage and indexed/chain differences; do not call a prepare tool or `confirm_transaction` as a diagnostic.

## Prepare only the requested action

Use a current advertised `prepare_create_position`, `prepare_increase_liquidity`, `prepare_withdraw_liquidity` or `prepare_move_range` matching the user's action. Preserve the returned plan phase, digest, chain, owner, recipient, deadline, expiry, amount bounds, route fees and transaction list. Range moves need canonical price orientation and usable ticks from the exact pool.

An approval-phase response is not the final executable plan. After a separately authorized finite approval is mined, invoke the same prepare action again to obtain fresh balances and the ready-plan digest. Do not reuse the approval digest or manually add estimated fees to a provider's protected inventory. Consolidating withdrawal output can add a swap; show that extra action and its limit.

## Reconcile custody and outcome

Borrow, collateralize, leverage, automation and staking change permissions or risk. They are separate actions, not incidental prerequisites for ordinary liquidity research. Website handoff tools open a UI; they do not execute a plan.

For an authorized execution, retain original transaction hash and ready digest. Revert's `confirm_transaction` changes provider accounting and belongs only after the mined receipt in an authorized flow. Independently verify resulting owner/custody, position amount, token deltas and debt. Pending or unknown execution remains unresolved; do not send again. On stale indexer, absent capability or unsupported custody, identify the gap and retain direct-RPC/UI alternatives.

## Worked result

Synthetic increase: phase `approval_required`, finite 500-USDC allowance request, digest A. Approval receipt later succeeds. Return `approval confirmed; liquidity increase not yet prepared`, re-run the prepare action and review new ready digest B before any liquidity send. A failed indexer read cannot turn that into either an empty position or permission to create another position.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
