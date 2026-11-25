---
name: galleon-euler-lending
description: "Use when inspecting an Euler V2 EVK borrow, repay or collateral withdrawal, including EVC subaccounts, collateral enablement and controller risk."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Euler V2 lending

## Identify the account and vault

Resolve chain ID, owner, EVC subaccount, collateral vault, borrowing vault, amount/unit and requested operation. EulerEarn allocation vaults are a separate product. Use the current official `@eulerxyz/euler-v2-sdk` release and its deployment resolver; pin the tested version. Do not use the archived legacy Euler SDK or derive subaccount ownership from a ticker.

For a read-only TypeScript client built with `buildEulerSDK`, call `accountService.fetchAccount(chainId, owner, { populateAll: true })` and `vaultMetaService.fetchVault(chainId, vault)`. Inspect `result` and any failures; do not assume a populated account contains every subaccount. Fetch the selected subaccount explicitly through the version-matched service. Record enabled collateral, controller, debt, share balances, oracle unit, rate, cash, caps, hooks and current borrowing/liquidation LTVs.

## Evaluate the requested change

1. Keep collateral assets, vault shares and borrowed assets separate. Read conversions and accrued debt at one block; align oracle quotes to the liability's unit of account.
2. Calculate current, proposed and stressed positions. Use each selected collateral's configured borrow LTV for new risk; liquidation LTV is a separate threshold. A high aggregate dollar value does not make an unenabled collateral usable.
3. Inspect EVC account permissions and enabled controller. Adding an operator or switching controller changes authority or risk, so report the exact required change rather than silently enabling it.
4. Use the SDK's documented plan method for the requested action, preserving all approval steps and EVC batch items. Simulate the complete plan with the exact account. A simulation using state overrides must disclose them; overridden balances or approvals are assumptions, not live prerequisites.
5. Evaluate final batch state. Intermediate collateral/debt values can be transient because EVC defers checks; do not classify each call in isolation as a valid independently sendable action.

## Worked decision

Synthetic collateral is worth 20,000 in the borrow vault's accounting unit. Its borrow LTV is 70%, liquidation LTV 80%, and accrued debt 13,000. A 2,000 borrow would exceed the 14,000 borrow capacity even though 15,000 remains below 16,000 liquidation capacity. Decline that requested size. A 20% collateral decline reduces liquidation capacity to 12,800, already below existing debt; flag the stress exposure independently of the failed new borrow.

If the oracle is stale, controller differs from the expected vault, a hook rejects the action, or cash cannot cover the withdrawal, return the failed prerequisite with the observed value. Do not bypass a hook or choose another controller to force success.

## Deliver and reconcile

Return account/vault identities, block, scales, enabled collateral/controller, both capacities, stress assumptions, available liquidity and the exact missing prerequisite. Planning ends with the unsigned complete batch and simulation evidence. Research grants no signing or operator authority. For separately authorized execution, reconcile the original hash and nonce before any retry, then confirm receipt and reread debt, shares and receiver balances.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
