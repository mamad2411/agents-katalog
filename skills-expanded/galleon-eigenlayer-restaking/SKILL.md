---
name: galleon-eigenlayer-restaking
description: "Use when reviewing EigenLayer liquid-token restaking, strategy shares, delegation/slashing exposure or queued withdrawal completion; exclude native EigenPod setup."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# EigenLayer LST restaking and withdrawal

## Identify the restaking position

Resolve chain, staker, token, StrategyManager strategy, DelegationManager deployment and requested operation. This procedure covers liquid-token strategies. Native EigenPod withdrawal credentials, validator exits and proofs need an explicitly scoped native-restaking workflow; do not introduce them for an LST request.

Match release, deployed proxy implementation and ABI through EigenCloud's compatibility/deployment records. An old method name is not evidence for a current signature. Official prose and source revisions have differed on withdrawal delays; read the actual request and deployed parameters rather than promising a universal day count.

## Collect shares and slash exposure

Read `StrategyManager.getDeposits(staker)` for strategies/deposit shares and `DelegationManager.getWithdrawableShares(staker, strategies)` for current withdrawable shares after scaling/slashing. Read each strategy's `underlyingToken()` and `sharesToUnderlyingView(withdrawableShares)` for a read-only current conversion. Deposit shares and withdrawable shares are different quantities; convert the latter for current exit estimates. Read `DelegationManager.delegatedTo(staker)`, allocation/slashing exposure, pause state and any deposit restrictions. Do not count strategy shares as underlying token units or assume deposits avoid existing operator-set exposure.

For deposit preparation, verify exact strategy/token pairing, token decimals, amount and allowance to StrategyManager. `depositIntoStrategy` and any delegation step are distinct. A request to value a position does not authorize deposits, operator changes or approvals.

## Queue and complete correctly

1. For post-slashing-release requests, read `getQueuedWithdrawalRoots(staker)` and `getQueuedWithdrawal(root)`; retain the returned withdrawal struct and its separately returned current shares. Older requests need their release-specific events/interface. Preserve staker, withdrawer, strategies, scaled shares, nonce and start block.
2. Separate active shares, queued shares, claimable underlying and already completed amounts. Slashing and conversion changes can reduce realizable proceeds.
3. Read `minWithdrawalDelayBlocks()` and compare the stored start block with the current block, then check allocation-dependent restrictions and pause flags. Simulate `completeQueuedWithdrawal(withdrawal, tokens, receiveAsTokens)` with the returned struct and one token entry per strategy. The reviewed interface sends tokens to the caller/withdrawer; an arbitrary receiver requires a separate reviewed transfer.
4. Queueing and completing are separate transactions. Completion into tokens differs from restaking as shares. Inspect the receiver and do not silently choose a different form.
5. After completion, confirm the exact withdrawal root is no longer pending and verify receiver token changes. A queue event is only proof that a request exists.

## Worked decision

Synthetic current withdrawable shares, after the appropriate scaling/slashing read, total 100 and convert to 105 LST units. A queued request with 80 current withdrawable shares estimates 84 units before future slashing/conversion changes; 20 active withdrawable shares estimate 21. The eligibility read says the request is not ready, so claimable-now is 0, not 84. Report 105 current estimated exposure split into 21 active and 84 queued, without adding the queued amount a second time to the total.

If an old UI countdown expires but the completion simulation is paused or ineligible, retain the authoritative failure. If send status is uncertain, reconcile the original hash/nonce and withdrawal root before another queue or complete operation.

## Return the decision

Include release/deployment, block, operator/allocation exposure, share and underlying units, withdrawal identity, eligibility and exact next supported action. Keep unsigned plans separate from financial authority. Research never requests keys or changes validator withdrawal credentials. Successful execution requires receipt plus root/position and recipient-state rereads.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
