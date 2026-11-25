---
name: circle-cctp
description: "Use when tracking a Circle CCTP USDC burn, attestation and destination mint, including domain IDs, finality and failed-mint recovery."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.4.1"
---

# Circle CCTP

Produce a burn-to-mint ledger for one Circle CCTP transfer. This workflow covers native USDC CCTP; token swaps, Circle Gateway and CCTP for other configured assets require their own contracts and terms.

## Establish version and message identity

Collect source hash, source/destination chains and domains, USDC contracts, raw amount, depositor and encoded mint recipient. Domain IDs are CCTP identifiers, not EVM chain IDs. Resolve CCTP version, supported domains, contract addresses and finality from current Circle sources. Never combine a V1 burn with a V2 receive path.

For planning, inspect burn allowance, max fee, requested finality, destination caller restriction and recipient encoding. Fast-transfer fees, forwarding-service fees and destination gas are separate costs. Return unsigned terms; do not burn, sign an authorization or enable forwarding to test readiness.

## Read burn and attestation

Confirm source receipt, actual burn event and emitted message. Save message bytes/hash and source domain before waiting. Query Circle's current message endpoint in [reads](references/reads.md), matching the correct message if a source transaction emitted several. An attestation can remain pending until the required source finality; a successful source receipt is not a destination balance.

Verify the returned source/destination domains, token, recipient, amount and finality against the saved intent. Pending or rate-limited retrieval gets bounded backoff; do not poll indefinitely or switch to a new burn.

## Reconcile mint or recovery

For a completed transfer inspect destination `receiveMessage` receipt/events and actual USDC credit to the encoded recipient. Check used-message/nonce state with the deployed version's ABI. A forwarding service's accepted status is weaker than that proof.

If mint submission failed, diagnose destination gas, caller restriction, attestation/finality and already-used state for the original message. Retry only the appropriate receive/recovery step within separately authorized scope after reconciling existing attempts. Never repeat the source burn as a remedy. On consumed-message state with missing local data, find the original mint rather than calling it lost funds.

## Worked result

Synthetic source burns 1,000 USDC and finality is sufficient; attestation exists, destination receive reverted for insufficient gas and no mint occurred. Report source burned/attested, destination unminted, and original-message gas recovery. A second burn would create a second transfer rather than repair the first.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
