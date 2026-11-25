---
name: galleon-ethena-susde
description: "Use when reviewing Ethena sUSDe share value, USDe unstaking cooldown, silo claim or restrictions; distinguish issuer mint/redeem and campaign locks."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Ethena sUSDe staking and cooldown

## Resolve token and operation

Identify chain, exact sUSDe deployment, owner, underlying USDe, requested amount/unit and exit receiver. sUSDe staking, direct issuer mint/redeem and separately locked campaigns are different products. Buying USDe or holding sUSDe does not establish issuer whitelist eligibility or redeem USDe directly for dollars.

Read the verified current implementation and ABI. Historical audit repositories contain older signatures; the reviewed public StakedUSDeV2 source uses `cooldownAssets(assets)` and `cooldownShares(shares)` without an owner argument. Match deployed code before encoding; do not combine old signatures with current addresses.

## Read share and cooldown state

Read `asset()`, decimals, owner `balanceOf`, `convertToAssets`, `previewRedeem`/`previewWithdraw`, owner limits, `cooldownDuration()`, `cooldowns(owner)` and `silo()`. Inspect applicable restricted-staker roles and pause/access conditions through the current interface. Keep wallet shares, assets already moved into the silo and USDe received by the wallet separate.

1. If cooldown is nonzero, ordinary `withdraw`/`redeem` are not the supported exit path for the reviewed V2 contract. Prepare the exact assets- or shares-denominated cooldown operation and simulate it.
2. Record the actual cooldown end and underlying amount after request. A new request can extend the combined cooldown end while accumulating underlying; show that effect before preparing another request.
3. At claim time evaluate `unstake(receiver)` using current request state and deployment semantics. A configurable duration of zero can affect existing claims in the reviewed source; read current code/state rather than recomputing eligibility from an old UI countdown.
4. A secondary-market sale is another route with price impact, minimum output, fees and a separate authority decision. A cooldown estimate is not a market-sale quote.

## Worked decision

Synthetic 1,000 shares convert to 1,080 USDe. Requesting 600 shares moves an estimated 648 USDe into cooldown and leaves 400 shares representing 432 USDe at the same rate. Claimable-now remains 0 before eligibility. Do not report 1,080 wallet USDe plus 648 queued. If another request resets the end, update the combined exit schedule instead of keeping the earlier claim date.

Disclose yield observation period and reward-vesting mechanics without promising a fixed rate or redemption value. The USDe risk/issuer structure and the sUSDe contract's restriction powers remain relevant even if a recent price was near one dollar.

## Completion

Return implementation/block, shares/assets, cooldown duration, request end/amount, restriction state and exact next step. A queue receipt is not USDe received. This skill grants no signing, issuer or spending authority. For separately authorized execution, reconcile the original hash then confirm receipt, cooldown/silo state and recipient balance; do not retry an ambiguous request blindly.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
