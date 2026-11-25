---
name: galleon-symbiotic-withdrawals
description: "Use when reviewing a Symbiotic vault withdrawal or claim, including epoch timing, active versus queued stake, slashing exposure and claimer ownership."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Symbiotic vault withdrawals

## Resolve the vault contract

Identify chain, vault/version, collateral, depositor, claimer, amount/unit and requested epoch. Read the verified deployment rather than assuming all curator vaults share settings. This workflow concerns vault collateral; rewards and network middleware are distinct. A network's Relay integration is not a cross-chain swap route.

Read vault `collateral()`, `epochDuration()`, `currentEpoch()`, active stake/shares, `activeBalanceOf(account)`, delegator, slasher and deposit access/limits where relevant. Match these functions to the vault's deployed version. Record block timestamp and epoch origin/boundaries. Read delegator allocations, network/operator opt-ins, slash/veto policy and pending penalties before presenting restaking exposure.

## Track the actual withdrawal

For the selected claimer and epoch, read `withdrawalsOf(epoch, claimer)` and `isWithdrawalsClaimed(epoch, claimer)` from the version-matched interface. Preserve the `Withdraw` event's claimer, active shares burned and withdrawal shares minted. A withdrawal can be requested for a different claimer; depositor identity alone does not prove claim authority.

1. An assets request uses `withdraw(claimer, amount)`; a share request uses `redeem(claimer, shares)`. Both queue collateral instead of transferring it immediately.
2. In the reviewed V1 implementation, a request during epoch k is recorded under withdrawal epoch k+1. Preserve that stored epoch when calling `withdrawalsOf` or `claim`; passing the request epoch k is wrong. It becomes claimable only after epoch k+1 ends. Read actual boundaries; the wait is generally between one and two epoch durations, not one duration after request.
3. Queued collateral remains slashable until its eligibility boundary. Re-read the epoch's remaining assets and shares after a penalty; do not promise the initially requested amount.
4. Prepare `claim(recipient, epoch)` or the supported batch-claim variant only for eligible, unclaimed epochs and the actual claimer. Simulate from that account with the exact recipient.

## Worked decision

Synthetic epoch length is 7 days and epoch k begins at day 0. A request at day 2 becomes eligible at day 14, a 12-day wait. At day 9 it is still queued, although 7 days have elapsed since request. If a queued 100-unit request now maps to 97 units after a slash, use 97 for the current claim estimate. Do not label 100 as a guaranteed receivable.

If `AlreadyClaimed`, `InvalidEpoch`, insufficient claim or an ownership mismatch occurs, inspect the matching claim event and current receiver balance. Do not request withdrawal again merely because a claim receipt was not indexed. If the curator changes an epoch setting, resolve version-specific current semantics before reusing an earlier countdown.

## Complete with evidence

Return vault/collateral identity, block/time, active and queued quantities, actual claimer, request/claim epoch, eligibility boundary, slash exposure and supported amount. This skill supplies research or unsigned calls, never financial authority. After separately authorized execution, confirm claim receipt, epoch claim state and collateral receipt at the intended recipient. Resolve an uncertain hash/nonce before retrying.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
