---
name: galleon-spark-savings
description: "Use when reviewing sUSDS or Spark Savings Vaults V2 shares, idle liquidity, PSM conversion or request-based large exits; exclude SparkLend borrowing."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Spark and Sky savings exits

## Identify savings implementation

Resolve chain, vault/token, underlying, owner and requested assets or shares. Mainnet sUSDS, Spark V2 spUSDC/spUSDT vaults, cross-chain receipt tokens and SparkLend spTokens are different. Match the exact official deployment and ABI; a similar symbol does not establish ERC-4626 redemption support on that chain.

Read `asset()`, decimals, `balanceOf(owner)`, `totalAssets()`, `totalSupply()`, `convertToAssets(shares)`, owner exit limits and actual underlying liquidity. For Spark V2 also inspect the rate accumulator (`vsr` and current share-value state) and role/configuration that permits liquidity deployment. Accounting growth can continue while assets are deployed outside the vault; it does not prove available cash.

## Select an exit route

1. Quote exact shares/assets with the matched implementation. Spark V2 previews may revert when liquidity is insufficient; use conversion for accounting value plus actual liquidity and limits, not a failed preview as proof of zero assets.
2. For immediate exit, simulate exact `withdraw` or `redeem` with owner and receiver. For any PSM conversion, read current supported assets, decimal conversions, fee parameters and rate limits. Do not assume every stablecoin route is currently free or 1:1 after costs.
3. If the requested amount exceeds idle liquidity, check whether official Savings Vault Intents supports this vault/network. Treat an intent as a request with shares, deadline, allowance and fulfillment conditions, not a reserved payout.
4. Read the latest request for that owner/vault. A replacement supersedes an earlier request; absence of a cancellation event is not proof the old request remains active. All-or-nothing fulfillment differs from a partial ERC-4626 withdrawal.
5. Inspect relayer/contract identity, share allowance and receiver. Do not approve unlimited spending, post an intent or switch output asset during a read-only liquidity assessment.

## Worked decision

Synthetic shares convert to 20,000 USDC, but current immediate limit/cash supports 6,000. A requested 10,000 exit has at most 6,000 immediate support and a 4,000 shortfall. A 10,000 intent must be evaluated as its complete requested amount; do not claim the relayer automatically fills 4,000 or guarantees a completion time. If a later intent replaces it, the earlier deadline is irrelevant.

If a bridged token lacks local redemption, return the actual bridge/native route needed, with separate settlement evidence. If a preview reverts, preserve the revert and liquidity read; do not substitute accounting assets as withdrawable assets.

## Deliver and reconcile

Return implementation, chain/block, share value, underlying cash/limits, rate assumption, conversion costs and latest intent state. A variable savings rate is not a guaranteed fixed return. Financial authority is separate from this research. After an authorized exit, verify exact receipt or intent fulfillment and recipient balance, resolving the original hash/request before retrying.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
