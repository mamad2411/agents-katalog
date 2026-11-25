---
name: galleon-kamino-lending
description: "Use when inspecting a Kamino Borrow obligation on Solana, its market, reserve liquidity, borrow factors, elevation group and post-action risk."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Kamino lending position

## Identify the obligation

Resolve Solana cluster, wallet public key, lending program, market, obligation, deposit mints, debt mints and intended amount. A ticker is insufficient. Kamino Borrow, Earn vaults, fixed-term lending and Multiply have different contracts and risk. Keep this workflow scoped to the discovered Borrow obligation; do not introduce leverage or a standing order for a spot lending request.

Use the official public API to discover `GET https://api.kamino.finance/v2/kamino-market` and `GET /kamino-market/{marketPubkey}/users/{userPubkey}/obligations`. Use `GET /oracles/prices` for discovery of supported observations. Inspect current schemas from the official index rather than inventing fields. Keep response and retrieval times; API discovery is not a current-slot validity check.

## Read and assess

Use a pinned, version-matched `@kamino-finance/klend-sdk` or program account decoder to read market, reserves and obligation at compatible slots. Confirm each account's program owner, underlying mint, token program and decimals. Read accrued debt, collateral exchange rates, risk-adjusted debt, borrow factor per debt asset, liquidation LTV, borrowing limits, reserve liquidity, caps and elevation-group eligibility. Markets are isolated; another market's collateral and cash cannot rescue this obligation's borrowing capacity.

1. Value collateral and liabilities using the protocol's accepted oracles. Retain raw token quantities and scaling; an SPL account balance is not necessarily underlying deposited collateral.
2. Calculate risk-adjusted debt by applying the selected reserve's borrow factor. Compare this with collateral and the applicable borrowing/liquidation limits. Do not report raw debt divided by collateral as the protocol LTV when factors differ.
3. Stress collateral price, debt price and interest growth. For correlated LST/SOL positions, include depeg/basis shocks rather than treating correlation as guaranteed.
4. For an unsigned action, use the current official transaction builder or SDK. Inspect every instruction, address lookup table, writable account, mint, receiver and fee payer. Verify refresh/oracle instructions and simulation at a recent slot. Rebuild an expired blockhash only after resolving whether the original signature landed.

## Worked decision

Synthetic collateral value is 20,000, raw debt 10,000 and borrow factor 1.2. Risk-adjusted LTV is 60%, not 50%. A 20% collateral decline makes it 75%. At a 70% liquidation LTV, the stressed position breaches the limit. Increasing collateral in another Kamino market changes none of these figures. Rate, cap and cash reads remain necessary before an executable borrow plan.

If an oracle or reserve is stale, the elevation group rejects a mint, or simulation reports stale obligation state, refresh through the official builder and rerun the exact plan. Do not remove risk checks or use a lower factor from another reserve.

## Return evidence

Return program/market/obligation identities, slots, mint scales, factors, liquidity, risk calculations and a decision with remaining reads. This is research or unsigned planning; no signer is needed. After separately authorized execution, verify signature status at the chosen commitment and reread obligation and recipient token account. A submitted signature or explorer listing alone is not a settled borrow or repayment.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
