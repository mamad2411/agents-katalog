---
name: galleon-defi-lending
description: "Use when researching lending markets, planning supply, borrow, repay or withdrawals, or monitoring liquidation risk across Aave, Morpho, Compound, Euler, Spark, Kamino and Save."
license: MIT
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# DeFi lending

Use the provider's maintained SDK, API, contracts or documented MCP for the selected deployment. This skill supplies operational judgment; it does not supply a wallet, signer, runtime adapter or authority to transact.

Read [providers](references/providers.md) for the chosen protocol and version. Read [workflows](references/workflows.md) for position planning, monitoring and evaluation cases. Keep unrelated provider manuals out of context.

## Start with the requested task

Use supplied preferences and compatible tools for this request; ask only for missing terms that change its result. Public research needs no wallet. Preferences and tool access never grant financial authority.

## Workflow

1. Identify the requested operation, chain ID, protocol version, market/pool/spoke or vault, collateral and debt token addresses, account/subaccount, amount and recipient. Resolve deployments from official sources. A token ticker or familiar frontend name is insufficient.
2. Read current balances, accrued debt, oracle values and units, collateral configuration, liquidity, caps, rates, fees and pause state. Record block/time and data provenance. Distinguish indexed discovery from fresh transaction state; missing or stale risk data is a blocker for execution planning.
3. Explain the proposed post-state: supplied assets, debt, withdrawable liquidity, interest exposure and distance to liquidation. Stress collateral and debt prices separately. Compare variable rates, fixed-term quotes, reward assumptions and rollover costs on a common basis. A maximum borrow amount is not a recommended amount.
4. For a requested transaction, use the official builder to prepare the complete unsigned sequence, including approvals/permits and any batch or flash-loan legs. Decode spender, amounts, recipients, chain, expiry and authority. Simulate the final sequence against current state. An error warning or unknown permission must be resolved before presenting it for signing.
5. Preserve the user's existing authorization scope. Research or preparation alone does not authorize signatures, debt, token allowances, delegation or transfers. Obtain any missing authorization for the concrete plan, then use the user's chosen signer; never request seed phrases or expose keys in prompts or logs.
6. Track separately: prepared, authorized, signed, submitted, confirmed, and reconciled. A signature, transaction hash, successful approval, or indexed position alone is not proof that all intended legs completed. Verify receipt and onchain balances/debt, then wait for indexer reconciliation. On timeout, inspect the known hash/nonce before considering a retry.

## Decision record

Return the target identity and block/time, tool/version actually used, rate basis and costs, pre/post-position risk, approvals and signer scope, simulation result, transaction state, and unresolved questions. Label documentation-only guidance or untested tooling honestly. Do not install/connect an MCP, enable broad tools, or open a leveraged position merely because a skill lists it.

Prefer adding collateral or repaying within authorized limits over assuming an unapproved refinance, bridge or asset sale. Monitoring alerts must state what changed and what action is proposed; scheduling and automated execution require their own explicit scope.


## Worked comparison

Synthetic observations below illustrate the decision; they are not live quotes or receipts.

**Request:** Compare a 30-day supply of 10,000 USDC. Use my existing providers and exclude rewards.

**Available evidence:** Fresh supplied observations: market A base APR 5%, total entry/exit cost 8 USDC; B base APR 4.5%, cost 2 USDC. Both meet the supplied liquidity and risk constraints. Simple interest, ACT/365; rates may change.

**Read sequence:** Read market identity, base rate methodology, liquidity and total costs at aligned observation times. Apply the requested horizon before ranking headline rates.

**Completed answer:** A: 10,000 × 0.05 × 30/365 - 8 = 33.10 USDC. B: 10,000 × 0.045 × 30/365 - 2 = 34.99 USDC. B leads by 1.89 USDC at unchanged rates. Recommend B for this comparison; this is an estimate, with no transaction prepared.

**Changed evidence:** B now lacks a fresh liquidity read; A is unchanged.

**Useful response:** Keep both rate calculations, mark B liquidity unverified, and request that one read through an available compatible tool before recommending executable allocation.

Fetch a missing observation through an existing compatible read tool when available; otherwise return the supported partial result and exact gap. Reconcile an uncertain write through its original identity before considering a retry.

## Focused protocol procedures

For a named protocol task, load its focused skill when installed. Discover it by name; this comparison workflow remains usable without sibling files.

- `galleon-aave-position`: checking an Aave V3 health factor, sizing a borrow, or planning a repay and collateral withdrawal; use for eMode and isolation constraints, not Aave V4.
- `galleon-morpho-market`: evaluating a specific Morpho Blue market or Morpho vault allocation, oracle, LLTV, borrow liquidity or exit risk.
- `galleon-compound-borrow`: planning a Compound III Comet base-asset borrow, repayment or collateral withdrawal and checking baseBorrowMin and collateral factors.
- `galleon-aave-v4`: Inspect Aave V4 Hub/Spoke positions, preview exact actions, and reconcile unsigned execution plans.
- `galleon-euler-lending`: inspecting an Euler V2 EVK borrow, repay or collateral withdrawal, including EVC subaccounts, collateral enablement and controller risk.
- `galleon-sparklend-position`: reviewing a SparkLend Pool supply, borrow, repay or collateral withdrawal; distinguish Spark Isolated Markets and savings vaults.
- `galleon-kamino-lending`: inspecting a Kamino Borrow obligation on Solana, its market, reserve liquidity, borrow factors, elevation group and post-action risk.
- `galleon-save-lending`: reviewing a Save (formerly Solend) lending market, reserve or obligation, including WAD debt, collateral exchange rates and split transactions.
