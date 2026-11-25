---
name: galleon-yearn-vault
description: "Use when reviewing a Yearn V2 or V3 vault, strategy allocation, share value, withdrawal queue or explicit loss tolerance before an entry or exit."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Yearn vault deposit and exit review

## Resolve vault version

Identify chain, vault, underlying asset, owner, amount/unit and requested outcome. Use Yearn's official Kong GraphQL service at `https://kong.yearn.fi/api/gql` for discovery, inspecting its schema rather than inventing query fields. Confirm onchain `apiVersion()` and verified implementation; V2 vaults, V3 multi-strategy vaults and standalone TokenizedStrategy contracts differ.

For the selected implementation read asset, decimals, owner share balance, total assets/supply, idle assets, strategy debt/allocation, fees/accountant, profit unlocking, shutdown and deposit/withdrawal limits. Use version-matched standard conversions/previews and strategy queue reads. A share-price increase is not an immediately realizable cash amount.

## Assess entry or exit

1. Keep assets and shares separate. For a V3 exit, compare owner-specific `maxWithdraw`/`maxRedeem` using the exact supported loss and strategy-queue arguments with requested amount.
2. Inspect strategy liquidity and queue order. Total assets include deployed debt; a custom queue can change feasibility. Identify canonical/default queue behavior before quoting an available maximum.
3. State realized-loss tolerance explicitly in basis points. Yearn V3 `withdraw` and `redeem` have different defaults; a zero-loss request must not rely on permissive `redeem` defaults. Inspect the precise overloaded ABI when encoding.
4. Simulate the exact action from owner/caller with chosen receiver, loss bound and queue. Approval/allowance, deposit limit and liquidity are independent prerequisites.
5. For rate comparison, separate base yield, rewards, fees and unrealized/profit-unlocking effects. Report the observation window; do not annualize one harvest as a promise.

## Worked decision

Synthetic 1,000 shares convert to 1,050 USDC accounting value. The owner-specific current withdrawal limit with a 0-bps loss bound is 800 USDC; a requested 1,000-USDC exit is not fully supported. An alternative preview reports 990 at 100-bps allowed loss. Present both as different terms, retain the user's 0-bps bound and request no loss-tolerance expansion automatically. Shares and accounting assets must not be added as separate holdings.

If Kong lags or a strategy changes liquidity, refresh direct contract state and invalidate the earlier executable quote. If a custom queue omits liquid strategies, explain the mismatch and simulate a documented compatible queue rather than claiming the vault has no assets. If simulation reverts, return the failed bound or strategy.

## Evidence and completion

Return version/address, block, shares/assets, limits, allocation/queue, explicit max-loss setting, fees, simulation and requested decision. Research grants no asset approval or deposit authority. Reconcile an uncertain transaction before retrying. After separately authorized execution, require successful receipt, burned/minted shares and actual underlying receiver balance; a vault request or approval does not prove an exit.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
