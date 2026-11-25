---
name: galleon-rocket-pool-reth
description: "Use when valuing Rocket Pool rETH or comparing native ETH redemption with a secondary-market exit, without starting validator or Smartnode operation."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Rocket Pool rETH entry and exit

## Choose the retail route

Resolve chain, exact rETH deployment, holder, amount and desired ETH receiver. Retail rETH ownership does not imply operating a validator or running Smartnode. A bridged rETH token is not automatically burnable for native ETH on that chain. Resolve current RocketStorage contract entries and verified implementation before using a source ABI.

## Read accounting and exit liquidity

Read rETH `balanceOf(holder)`, decimals, `getEthValue(rawReth)`, `getRethValue(rawEth)`, `getExchangeRate()` and `getTotalCollateral()` at one block. The exchange rate measures accounting ETH backing per rETH; it is neither a guaranteed market sale price nor 1:1 token parity. `getTotalCollateral` includes eligible deposit-pool excess as implemented; reading only the token contract's ETH balance can understate available native redemption cash.

For entry, identify current deposit-pool contract, pause/deposit limits and current mint quote. Compare a native deposit with a same-size secondary-market quote using actual fees, price impact, recipient and minimum output. Do not assume a direct deposit route is open or best merely because rETH trades.

For native exit, compare the exact `getEthValue(amount)` with current total collateral and simulate `burn(amount)` from the holder using the matched deployed ABI. The reviewed direct burn transfers ETH to `msg.sender`; it has no receiver argument. A different receiver requires a separately reviewed route or follow-on transfer. Review any deployment-specific transfer/deposit restrictions and native-ETH receiving behavior. Do not insert an ERC20 allowance or router into a direct burn merely by habit.

## Compare like-for-like outcomes

1. Quote all routes for the same raw rETH amount at compatible times.
2. Show native accounting ETH, feasible native liquidity, DEX minimum ETH after fees and expected gas separately.
3. If native cash is insufficient, mark the burn unavailable at that state. A market sale may remain possible, but it requires a distinct approved route and minimum output.
4. If acquisition is requested, express the received rETH and its accounting ETH separately. Never turn a stated ETH spending cap into an rETH token amount without conversion.

## Worked decision

Synthetic 10 rETH has accounting value 11.2 ETH. Native redemption cash is 8 ETH, so the full burn cannot execute now. A DEX quote returns minimum 10.9 ETH and estimated gas 0.01 ETH: net minimum 10.89 ETH,0.31 ETH below accounting value. Return that difference and the unavailable native route; do not sell automatically or claim the protocol owes immediate 11.2 ETH liquidity.

If quotes expire, pool state changes or `burn` simulation reverts, retain the failed route and refresh the exact size. Do not split an action to evade a live restriction without a newly evaluated plan.

## Evidence and completion

Return chain/deployment, block, raw rETH, accounting ETH, total native collateral, quote expiry/minimum/gas and requested decision. This procedure prepares research or unsigned calls. After separately authorized execution, confirm receipt and actual rETH decrease/ETH receipt, accounting for gas and receiver identity. Reconcile the original hash/nonce before any uncertain retry.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
