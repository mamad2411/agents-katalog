---
name: galleon-defi-derivatives
description: Assess perpetuals, options and funding-rate derivatives, prepare bounded exposure plans, and reconcile order and margin state. Use when comparing GMX, Velocity (formerly Drift), Derive, Jupiter Perps or Boros, planning hedges, monitoring positions or recovering orders.
license: MIT
compatibility: Portable Agent Skills instructions. Live work needs official venue data and optional user-authorized wallet tooling. No signer, provider or runtime is installed by this skill.
metadata:
  author: Galleon Labs
  version: "0.2.1"
---

# DeFi derivatives

Translate a market or hedge request into explicit exposure, collateral requirements and venue-specific order evidence. Reuse official tooling; keep research, planning and authorized execution distinct.

## Start with the requested task

Use supplied preferences and compatible tools for this request; ask only for missing terms that change its result. Public research needs no wallet. Preferences and tool access never grant financial authority.

## Select the product and tools

Read [providers](references/providers.md) for GMX, Velocity (formerly Drift), Derive, Jupiter and Boros, their official integration surfaces and version gaps. Read [workflows](references/workflows.md) for risk planning and order reconciliation. [Evaluation cases](references/evaluation.md) provide bounded fixture scenarios.

For Hyperliquid, use the installed `hyperliquid-analyze`, `hyperliquid-plan`, `hyperliquid-execute` or `hyperliquid-monitor` skill when available. This pack provides the cross-venue comparison and handoff; it does not reproduce Hyperliquid signing or nonce rules. No other pack is required for the general workflow here.

## Define the exposure

Identify network, protocol version, exact instrument/market, expiry, payoff denomination, collateral, margin mode, owner, subaccount and signer role. An ETH perpetual, an ETH option and an ETH funding-rate contract are different exposures. Do not normalize them into a single token price or label annualized funding as guaranteed yield.

Obtain fresh oracle/mark/index prices, order book or available capacity, current positions and orders, balances, margin requirements and accrued funding/borrow costs. State the observation time and source. Missing account data prevents a personalized risk or execution-ready claim; public market analysis can still proceed.

## Build a bounded plan

Use the user's existing risk budget and approved terms. Specify size in both native venue units and economic notional, side, order type, limit/acceptable price, maximum slippage, collateral change, leverage/margin mode, expiry, reduce-only intent, fee recipients and maximum costs. Stress adverse price, funding, volatility and exit liquidity; calculate combined exposure across existing orders and positions, not just the new order. A stop order may trigger without filling.

For options include premium, contract multiplier, settlement asset, exercise/expiry model and uncovered short liability. For funding-rate hedges include settlement period, rate convention, maturity, collateral and basis mismatch against the exposure being hedged. A hedge across venues creates separate liquidation and settlement risks.

## Authorize and reconcile

Use the official builder within the user's established execution boundary. A delegated key with limited withdrawals can still lose trading collateral. Granting or renewing delegation, changing margin mode, depositing and withdrawing are distinct financial actions; none is incidental setup. Never handle a key, create an agent wallet, insert a fee recipient or authorize a trade from this skill's presence.

Before manual changes to a managed account, read [account control](references/account-control.md) to reconcile active bots, open orders and an authorized handoff.

Follow [the venue lifecycle](references/workflows.md): persist operation identity; separate prepared, submitted, created/resting, partially filled, executed, cancelled and unknown states; reconcile authoritative fills and account changes. Resolve unknown outcomes before retries. A keeper-created order, relayer acceptance or successful transport response is not a completed trade. Cancel and replace can race with fills; reread both before calculating remaining size.

## Deliver

Return the market answer, comparison or proposed ticket with exact instrument and account identity, exposure, downside constraints, costs, source times, supported capabilities and material gaps. For monitoring, report position/order/margin changes with trigger conditions and a bounded next action. Creating a schedule, starting continuous trading or changing an existing automation requires the user's actual request; the skill does not start a background service.

## Worked comparison

Synthetic observations below illustrate the decision; they are not live quotes or receipts.

**Request:** Calculate an incremental ETH hedge using my existing venue; target zero delta. Analysis only.

**Available evidence:** Spot +10 ETH, filled linear ETH perp -3 ETH, live unfilled sell order -2 ETH. Contract multiplier 1 ETH, no other exposure. Assume the resting order fills for target planning and separately report current filled exposure.

**Read sequence:** Read exact contract multiplier, filled positions, open orders and spot units; calculate current and contingent delta separately.

**Completed answer:** Filled exposure is +7 ETH. If the resting sell fills, projected exposure is +5 ETH; an additional 5 ETH short targets zero projected delta. If that order does not fill, the additional hedge leaves +2 ETH. Recheck/cancel-or-account-for the resting order before preparing an executable order.

**Changed evidence:** The open-order read times out after a prior submission.

**Useful response:** Report +7 ETH filled exposure only, mark contingent exposure unknown and reconcile the existing order before computing a new executable size.

Fetch a missing observation through an existing compatible read tool when available; otherwise return the supported partial result and exact gap. Reconcile an uncertain write through its original identity before considering a retry.

## Focused protocol procedures

For a named protocol task, load its focused skill when installed. Discover it by name; this comparison workflow remains usable without sibling files.

- `gmx-position`: reviewing a GMX perpetual position or order through SDK v2, including market capacity, fees, keeper execution and request-id reconciliation.
- `derive-options`: reviewing Derive v3 option instruments, premium and margin scenarios, or reconciling subaccount orders, fills and session scope.
- `velocity-position`: inspecting Velocity Exchange Solana positions and margin or distinguishing paused legacy Drift accounts from the new Velocity deployment.
- `pendle-boros`: reviewing Boros funding-rate derivatives, implied versus realized rates, margin and delegated-agent scope before any trading action.
- `jupiter-perps`: inspecting Jupiter Perpetuals position and PositionRequest accounts, borrowing fees, triggers or pending close evidence on Solana.
