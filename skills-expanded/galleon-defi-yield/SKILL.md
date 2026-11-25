---
name: galleon-defi-yield
description: "Use when comparing savings and strategy vaults, planning deposits or exits, or evaluating principal/yield tokens and maturity across Pendle, Yearn, Spark, Morpho, Euler and Ethena."
license: MIT
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# DeFi yield positions

Use official builders and data sources. This skill adds a common decision process for vault shares, savings tokens and tokenized yield; it is not a yield optimizer with trading authority.

Read [providers](references/providers.md) for the chosen product and version. Read [workflows](references/workflows.md) for vault mechanics, maturity/exit plans and evaluation cases.

## Start with the requested task

Use supplied preferences and compatible tools for this request; ask only for missing terms that change its result. Public research needs no wallet. Preferences and tool access never grant financial authority.

## Workflow

1. Resolve chain, contract/version, underlying asset, share token, accounting asset, owner and recipient. For Pendle resolve SY, PT, YT, market and exact maturity together. A familiar token symbol does not prove a vault's origin or supported redemption route.
2. Read current assets/shares, conversion and preview values, owner-specific limits, liquidity, fees, queue/cooldown status, strategy allocation, curator/admin powers and rate provenance. Keep APY observation period, compounding, fees, rewards and points separate. Missing yield is unknown, not zero; historical rates are not guaranteed future returns.
3. Compare net outcomes over the user's actual horizon. Distinguish assets from shares and accounting principal from raw receipt tokens. A vault's assets under management are not immediately withdrawable cash. Show early-exit price risk, maturity, underlying loss exposure and each claim step.
4. Prepare the selected unsigned deposit, mint, withdrawal, redemption, claim or market trade with an official interface. Set concrete slippage/minimum-output and loss tolerances appropriate to that interface; a loss tolerance is not necessarily a price-slippage tolerance. Review approvals, recipients, shares/assets, deadlines and final simulation.
5. Respect existing authorization, obtaining any missing approval for the concrete transaction plan. Research, comparison and simulation do not authorize signatures, allowances, asset movement, borrowing or automatic compounding. Use the selected signer without exposing credentials.
6. Track prepared, authorized, signed, submitted, receipt-confirmed and position-reconciled states separately. For queued exits add requested, claimable and claimed. For maturity distinguish redeemable principal from received output. Investigate existing transaction hashes and request IDs before retrying; an indexer's lag is not failure.

## Output

Show asset identity, observation block/time, APY methodology, underlying/strategy and governance exposure, net horizon comparison, liquidity and exit route, explicit transaction limits and approval scope, and what was actually verified. Label official documentation separately from tooling tested in the current environment.

Do not connect/install services or enable broad tools automatically. Use official provider skills when building an integration instead of copying their SDK logic. Borrowing against a vault or PT introduces lending risk and requires a separate position analysis; Boros margin trades are derivatives, not passive vault deposits.


## Worked comparison

Synthetic observations below illustrate the decision; they are not live quotes or receipts.

**Request:** Compare 10,000 USDC for 30 days, excluding incentives. I must withdraw on day 30.

**Available evidence:** Vault base APR 6%, simple ACT/365, 10 USDC total costs; withdrawal available at day 30. PT matures day 90 and advertises 8% implied yield; no day-30 executable exit quote or depth supplied.

**Read sequence:** Read asset/share units, base return basis, withdrawal conditions and all costs; for PT read maturity and a horizon-matched early-exit quote.

**Completed answer:** Vault estimate: 10,000 × 0.06 × 30/365 - 10 = 39.32 USDC net interest. PT maturity yield cannot establish day-30 proceeds. Prefer the vault among evidenced options; its variable rate remains an assumption.

**Changed evidence:** Vault withdrawals become queued past day 30 and PT still has no early-exit quote.

**Useful response:** Neither option now has evidenced liquidity by the deadline. Retain the economic estimate but withdraw the liquidity recommendation and identify each missing exit condition.

Fetch a missing observation through an existing compatible read tool when available; otherwise return the supported partial result and exact gap. Reconcile an uncertain write through its original identity before considering a retry.

## Focused protocol procedures

For a named protocol task, load its focused skill when installed. Discover it by name; this comparison workflow remains usable without sibling files.

- `galleon-pendle-maturity`: evaluating a Pendle PT or YT trade, comparing hold-to-maturity with an early exit, or redeeming a matured position.
- `galleon-vault-exit`: checking how much can leave an ERC4626 vault, reconciling pending and claimable ERC7540 redemptions, or choosing withdraw versus redeem under liquidity and fee constraints.
- `galleon-yearn-vault`: reviewing a Yearn V2 or V3 vault, strategy allocation, share value, withdrawal queue or explicit loss tolerance before an entry or exit.
- `galleon-spark-savings`: reviewing sUSDS or Spark Savings Vaults V2 shares, idle liquidity, PSM conversion or request-based large exits; exclude SparkLend borrowing.
- `galleon-euler-earn`: evaluating an EulerEarn strategy vault, curator allocation, fees, share position or withdrawal queue; distinguish direct EVK borrowing vaults.
- `galleon-ethena-susde`: reviewing Ethena sUSDe share value, USDe unstaking cooldown, silo claim or restrictions; distinguish issuer mint/redeem and campaign locks.
