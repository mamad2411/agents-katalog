---
name: galleon-sparklend-position
description: "Use when reviewing a SparkLend Pool supply, borrow, repay or collateral withdrawal; distinguish Spark Isolated Markets and savings vaults."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# SparkLend position review

## Resolve the product

Ask for or discover chain, account, asset, amount and requested action. Confirm this is the SparkLend Pool. Spark Isolated Markets use Morpho; sUSDS and Spark Savings Vaults are savings products. Do not map every Spark-branded position onto an Aave SDK deployment. Resolve the current Pool, addresses provider, data provider and oracle from Spark's registry and match their verified interfaces.

## Read one coherent position

Read `Pool.getUserAccountData(account)`, `getUserConfiguration(account)`, `getUserEMode(account)` and `getReserveData(asset)`. Use the matching data provider for `getUserReserveData(asset, account)` and reserve configuration; preserve raw token decimals, oracle base units and WAD health factor. Read the oracle route, current prices, liquidation thresholds, borrowing LTV, debt balances, supply/borrow caps, pause/freeze flags, eMode category and isolation debt ceiling. Verify the actual deployment still supports the requested action; a historical network listing is insufficient.

Read underlying liquidity held by the reserve's aToken separately from total supply. Compare fresh accrued debt, available borrowing capacity and proposed post-state. Never infer withdrawable collateral solely from the wallet's spToken balance.

## Prepare only the requested sequence

- Supply uses `supply(asset, amount, onBehalfOf, referralCode)` with underlying allowance. Check whether first supply automatically enables collateral in the current configuration.
- Borrow uses `borrow(asset, amount, interestRateMode, referralCode, onBehalfOf)`. Check the live rate-mode flag; implemented stable-rate code does not mean a reserve enables stable borrowing. A different debt owner requires explicit credit-delegation evidence.
- Repay uses `repay(asset, amount, interestRateMode, onBehalfOf)`; approval alone does not reduce debt. Repay with aTokens is a different path and requires the same reserve asset.
- Withdrawal uses `withdraw(asset, amount, recipient)`. Simulate its post-withdraw health and liquidity; do not reuse an earlier maximum after prices or accrued debt change.

Use current and shocked prices plus accrued interest over the requested horizon. State the user's health floor separately from the protocol liquidation boundary. Do not change eMode, collateral toggles, debt owner or amount merely to pass a preview.

## Worked decision and recovery

Synthetic weighted liquidation collateral is 12,000 and debt 8,000, so current HF is 1.5. Removing collateral with 2,000 liquidation-weighted value leaves HF 1.25. A user floor of 1.3 fails even though liquidation is not immediate. Report the requested withdrawal as outside that floor. Missing reserve cash remains an independent exit constraint.

If a repayment times out, retain its hash/nonce and inspect receipt plus current debt before constructing a replacement. If Gnosis or another deployment is frozen, distinguish allowed exits from unavailable new supply/borrowing instead of promising full product parity.

## Completion

Return deployment/block, actual Pool product, reserve state, current/proposed/stressed HF, cash, amount scales and failed conditions. An unsigned sequence with simulation is a planning result. Only a separately authorized transaction, successful receipt and state reread establish a changed position; this skill does not grant wallet authority.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
