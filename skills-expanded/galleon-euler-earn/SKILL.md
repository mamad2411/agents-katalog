---
name: galleon-euler-earn
description: "Use when evaluating an EulerEarn strategy vault, curator allocation, fees, share position or withdrawal queue; distinguish direct EVK borrowing vaults."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# EulerEarn vault allocation and exit

## Resolve Earn identity

Identify chain, vault, owner, underlying asset, amount/unit and desired entry, comparison or exit. Use official Euler metadata and the version-matched `@eulerxyz/euler-v2-sdk` read services. `vaultMetaService.fetchVault(chainId, vault)` can distinguish supported vault types; confirm this is EulerEarn rather than a direct EVK lending vault. Query failures or unknown types are unresolved, not a reason to guess an ABI.

## Read allocation and liquidity

Use Euler's Data API V3 or metadata to discover allocations, curator labels and historical observations. Cross-check current state with version-matched lenses/direct contract calls. Capture `asset()`, share/asset decimals, owner `balanceOf`, `totalAssets`, `totalSupply`, standard conversions, `maxWithdraw(owner)`/`maxRedeem(owner)` and exact action previews where supported.

Read the vault's actual withdrawal queue, strategy allocations, caps, fees, role holders and pending configuration/timelock changes through its current interface. Avoid copying a queue method from another ERC-4626 protocol. A listing badge or curator name does not establish liquidity, audited configuration or deposit safety.

## Reach the requested decision

1. Convert the owner's shares to accounting assets at a recorded block. Do not add shares, their underlying value and strategy allocations as three independent assets.
2. Compare requested exit against owner-specific limits and each strategy's reachable liquidity through the actual queue. Record total allocation separately from available cash.
3. Attribute yield and losses to selected allocations, fees and observation window. Incentives and performance fees need distinct lines; displayed APY is not a fixed forward return.
4. Inspect whether a deposit changes concentration or enters a pending curator/configuration transition. Report those risks without changing allocation or management roles.
5. Prepare through the official supported SDK or exact ERC-4626 interface, simulate full approval/action sequence and disclose state overrides. Do not introduce custom strategy-management calls for a retail entry or exit.

## Worked decision

Synthetic 1,000 shares convert to 1,100 underlying units. Two strategies account for 700 and 400 units, but the owner-specific exit limit is 300. A 500-unit withdrawal has only 300 currently supported and 200 unsupported. The accounting 1100 does not show that every strategy can return funds now. A proposed curator change does not automatically improve the limit; refresh after it is actually executed.

If metadata and onchain asset identities conflict, stop amount preparation and resolve the deployment. If indexed withdrawal liquidity is old, keep it as historical context and obtain current limits/queue evidence. A simulation failure is not repaired by bypassing the queue.

## Completion and recovery

Return vault type/address, block, owner shares, accounting assets, queue/allocation, current limits, fees and concrete entry/exit decision. This procedure performs research or unsigned planning only. After separately authorized execution, reconcile hash/nonce then confirm receipt, share change and actual underlying receipt; indexed portfolio disappearance alone is insufficient.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
