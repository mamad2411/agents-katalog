---
name: safe-transaction
description: "Use when reviewing a Safe multisig transaction, threshold and nonce, decoding batched calls, or reconciling proposal, confirmations and onchain execution."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.2.1"
---

# Safe transaction

Return a Safe transaction review or exact execution ledger. Service proposal, collected signatures, execution transaction and resulting effects are separate evidence states.

## Read the account and transaction identity

Collect chain, Safe address, Safe transaction hash and requested scope. Read deployed version, owners, threshold, current nonce, enabled modules, guard and fallback handler. A transaction service record is indexed information; corroborate current critical configuration onchain. Modules can have paths outside ordinary owner-threshold execution and need separate review.

Fetch the exact Safe transaction fields through the service or existing SDK in [reads](references/reads.md). Recompute its hash under the correct chain/Safe/version. Include `to`, value, calldata, operation, nonce, gas/refund fields and any batched calls. Distinguish CALL from DELEGATECALL; the latter can alter the Safe's storage through target code. Decode every batch action and beneficiary rather than reviewing only the outer MultiSend target.

## Verify signatures and readiness

Count valid current owner confirmations over the same Safe transaction hash, not total rows or duplicate signers. Contract-owner signatures and prevalidated forms need their version-specific validation. Check threshold, nonce and competing transactions. Enough signatures for nonce N do not bypass earlier nonce gaps; another transaction at N can invalidate the reviewed plan.

A proposed or fully confirmed transaction is not mined. Return exact unsigned review findings and missing confirmations/configuration evidence. Owner/threshold/module changes, signing, service posting and execution each need their actual authorization. Readiness is not permission to perform them.

## Reconcile inner execution

For an execution hash inspect chain receipt and Safe `ExecutionSuccess` or `ExecutionFailure`. An outer EVM receipt with status success can still contain a failed Safe inner transaction. Reread nonce and the requested token, native balance, owner or protocol state. For a batch verify each intended effect, not only an emitted event.

If submission timed out, query the same Safe hash, nonce and chain transaction before another send. A different queued transaction at the same nonce is a conflict to resolve, not an automatic cancellation. On missing service access fall back to available onchain evidence without inventing signature coverage.

## Worked result

Synthetic Safe threshold 2-of-3 has two valid owner confirmations for nonce 8, but current Safe nonce is 7. Report signed for future nonce, awaiting nonce 7; it is neither executable now nor executed. In another case outer receipt status is 1 but `ExecutionFailure` appears: report inner action failed and verify balances before any retry.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
