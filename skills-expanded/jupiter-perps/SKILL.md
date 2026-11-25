---
name: jupiter-perps
description: "Use when inspecting Jupiter Perpetuals position and PositionRequest accounts, borrowing fees, triggers or pending close evidence on Solana."
license: MIT
compatibility: "Read-only protocol APIs or RPC through existing configured tools. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.2.1"
---

# Jupiter perps

Return a Jupiter Perps account/position assessment using the deployed program's exact account schema. The official Perps overview still labels its REST API a work in progress; do not invent a live `/perps/order` API or infer support from the Swap API.

## Resolve position identity

Collect cluster, owner, side, custody and collateral-custody accounts, Position address and any request signature. Resolve the official program and verified current account layout. Read the Position, relevant Custody and PositionRequest accounts at a recorded slot through configured Solana RPC or an existing supported official tool.

Position identity includes side and both custody identities; do not combine different collateral assets because they share a token symbol. `sizeUsd` and `collateralUsd` are distinct raw USD-scaled amounts; token collateralDelta uses its mint decimals. A zero `sizeUsd` is a closed position, but historical realized proceeds require transaction/history evidence because a closed account's displayed PnL can reset.

## Read costs and contingent actions

Evaluate entry/mark, size, collateral, borrow accumulator and request state. Borrowing costs derive from the difference between custody cumulative interest and the position snapshot using current program math; do not label them interchangeable with signed cross-venue funding.

Read active trigger requests separately from current position exposure. For increases and decreases, inspect side-dependent priceSlippage direction, swap minimum, entirePosition flag and intended size delta. A newly created PositionRequest is an instruction waiting for execution, not a completed close. Its ATA can temporarily hold deposit/withdraw assets.

## Return the unsigned decision

Show position/account identities, slot, leverage assumptions, cost sources, pending requests and missing evidence. Preparation must use the currently supported official UI or a verified program integration; the linked third-party IDL parsing example is community code, not a guaranteed maintained signing service. Keep signing and instruction submission outside research.

If a request disappears, distinguish executed/rejected/closed using its transaction and current Position/ATA balances; do not infer fill from disappearance alone. On timeout reconcile the original signature before retrying. Unsupported API, stale custody data or unknown program version remains a named capability gap.

## Worked result

Synthetic Position sizeUsd is 5,000,000,000 at six decimals: $5,000 exposure. A full-close request exists with executed=false and current size unchanged. Report $5,000 observed exposure and pending close. An eventual zero-size reread plus successful close receipt and returned collateral establish completion; a request creation signature alone does not.

## Sources and limits

Primary documentation and source reviewed 2026-10-25; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) ship with this skill. Recheck supported deployments and schemas before a consequential handoff. Research adds no permission to trade, transfer, vote or change account authority.
