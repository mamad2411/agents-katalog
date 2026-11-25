---
name: galleon-defi-staking
description: "Use when planning liquid staking, wrapping, restaking, delegation or queued exit claims for Lido, Rocket Pool, EigenLayer and Symbiotic."
license: MIT
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# DeFi staking and restaking

Use maintained official interfaces for the selected deployment. This skill guides liquid-staking and restaking positions, not validator installation or custody. It includes no signer or automatic transaction runner.

Read the selected protocol in [providers](references/providers.md); use [workflows](references/workflows.md) for exits, accounting and evaluation cases.

## Start with the requested task

Use supplied preferences and compatible tools for this request; ask only for missing terms that change its result. Public research needs no wallet. Preferences and tool access never grant financial authority.

## Workflow

1. Identify chain, deployment/version, input token, receipt token, account, recipient and intended action. Separate buying an LST on a market, staking through its issuer, wrapping, restaking, and operating a validator. These create different claims and exit paths.
2. Read the exchange rate or rebasing shares, actual protocol liquidity, deposit limits, fees, pauses, current queue/epoch/cooldown state and pending request ownership. Restaking additionally requires the chosen vault/operator/network, allocation and slashing terms. A points campaign is not a promised monetary return.
3. Compare the complete lifecycle. Show principal denomination, expected receipts, yield methodology, underlying exposure, available exit routes, expected delay and loss/slashing exposure during that delay. Quote a secondary-market exit separately with price impact; never call it a protocol redemption at par.
4. Prepare the requested unsigned operation with official SDK/contracts and simulate it. Review token/spender/amount, recipient, permit deadlines, delegate/operator authority and any withdrawal credentials. Creating an EigenPod or changing validator withdrawal credentials is materially different from restaking an LST and needs specifically scoped authorization.
5. Use existing authorization only within its scope. Research or exit estimates do not authorize staking, token approvals, delegation, restaking or signing. Present the concrete plan for any missing authorization, and use the selected signer without ingesting secrets.
6. Reconcile each stage independently: preparation, authorization, signature, submission, receipt, resulting position, pending exit, claimable exit, final claim. Save request IDs, epoch or eligible block, current owner and claim recipient. A request receipt is not funds returned; an indexer's countdown is not proof of claimability. Check authoritative state before claiming or retrying an uncertain transaction.

## Report

Return chain/version and source time, underlying versus receipt units, available liquidity, current queue state and ownership, operator/curator/slashing exposure where relevant, unsigned plan and approval scope, and the verified lifecycle stage. Report a delay as an estimate unless a current contract condition proves eligibility.

Do not auto-install/connect tools, import wallet secrets, select an operator, extend authority, or schedule claims merely because these capabilities are documented. Use native harness scheduling only when monitoring is requested, with explicit targets and actionable alerts.


## Worked comparison

Synthetic observations below illustrate the decision; they are not live quotes or receipts.

**Request:** I need ETH within 24 hours. Compare exiting 10 receipt tokens.

**Available evidence:** Verified synthetic receipt exchange rate 1.2 ETH per token; redemption gives 12 ETH before 0.01 ETH cost, earliest queue completion 3 days. Current executable market quote gives 11.95 ETH net of all costs within one hour.

**Read sequence:** Read receipt conversion, queue conditions, and executable quote for the exact receipt amount; compare net underlying units and earliest usable time.

**Completed answer:** Queue exit estimates 11.99 ETH in at least 3 days; market exit quotes 11.95 ETH within an hour. The market route meets the deadline at a 0.04 ETH cost relative to queued redemption. Quote expiry and final settlement still apply.

**Changed evidence:** The DEX quote expires before preparation and a fresh quote is unavailable.

**Useful response:** Preserve the queue estimate and missed deadline. Mark the market outcome unavailable until requoted; do not reuse the expired price or claim a timely exit is available.

Fetch a missing observation through an existing compatible read tool when available; otherwise return the supported partial result and exact gap. Reconcile an uncertain write through its original identity before considering a retry.

## Focused protocol procedures

For a named protocol task, load its focused skill when installed. Discover it by name; this comparison workflow remains usable without sibling files.

- `galleon-lido-withdrawals`: requesting or claiming Lido stETH or wstETH withdrawals, reconciling unstETH NFTs, or comparing the native queue with a secondary-market exit.
- `galleon-rocket-pool-reth`: valuing Rocket Pool rETH or comparing native ETH redemption with a secondary-market exit, without starting validator or Smartnode operation.
- `galleon-eigenlayer-restaking`: reviewing EigenLayer liquid-token restaking, strategy shares, delegation/slashing exposure or queued withdrawal completion; exclude native EigenPod setup.
- `galleon-symbiotic-withdrawals`: reviewing a Symbiotic vault withdrawal or claim, including epoch timing, active versus queued stake, slashing exposure and claimer ownership.
