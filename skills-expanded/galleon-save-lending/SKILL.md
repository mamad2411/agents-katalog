---
name: galleon-save-lending
description: "Use when reviewing a Save (formerly Solend) lending market, reserve or obligation, including WAD debt, collateral exchange rates and split transactions."
license: MIT
compatibility: "Official read APIs, SDKs or chain RPC; provider access stays in the user's environment. No signer required for research."
metadata:
  version: "0.4.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# Save lending on Solana

## Resolve Save identity

Identify cluster, wallet, lending program, specific market, reserve and obligation. Save retains Solend-named SDK and program interfaces. Do not treat the old integration guide's one-market wording as a current deployment inventory. Discover live markets and verify program ownership and mint identities before applying an example.

Use the maintained `solendprotocol/public` repository for `@solendprotocol/solend-sdk`; the older standalone SDK repository is read-only. Pin a reviewed release and follow its matching types. A symbol lookup is only a candidate: validate reserve address, liquidity mint, decimals and oracle accounts before computing amounts.

## Collect the lending state

The official SDK documents `SolendMarket.initialize(connection, environment, marketPublicKey)`, `loadReserves()`, `refreshAll()` and `fetchObligationByWallet(wallet)`. Await the version's asynchronous methods and inspect returned failures. Retain RPC slot and API timestamps. Cross-check cached/API prices with current reserve and oracle accounts for a proposed transaction.

Read reserve available liquidity, borrowed amount, collateral mint supply/exchange rate, rate curve, fees, supply/borrow limits and configuration. Read obligation collateral entries, borrowed amounts, accrued interest and risk-adjusted limits. WAD-valued fields use fixed-point scaling; do not treat `borrowedAmountWads` as native token units or convert through an imprecise JavaScript Number.

## Decide and prepare

1. Convert receipt collateral to underlying with that reserve's current exchange rate. Value each asset using accepted oracle units.
2. Compute debt after accrual and the proposed change, borrow capacity and liquidation exposure. Stress both prices and rates. Rewards are separate from borrowing cost and do not reduce liquidation debt.
3. Compare the requested withdrawal with reserve cash and remaining collateral requirements. A large total deposit does not guarantee immediate liquidity.
4. Use the SDK's current action builder for an unsigned sequence. Preserve setup, refresh, lending and cleanup transactions in order. Inspect token accounts, program IDs, fee payer and any delegation; do not invoke `sendTransactions` during research.
5. Simulate each transaction with state dependencies respected. If account setup succeeds but lending fails, report the partial state rather than calling the whole action complete.

## Worked decision and failure handling

Synthetic reserve deposits are 1,000,000 USDC equivalent, borrowing 990,000 and available underlying 10,000. A requested 25,000 withdrawal exceeds current cash even if the obligation has enough collateral. The supported upper bound is at most 10,000 before fees, constraints and changing state; do not promise a 25,000 exit. For a six-decimal token, a borrowed value of 5,000,000,000 × 10^18 WAD-scaled native units represents 5,000 USDC, not 5,000,000,000 USDC.

For an uncertain Solana send, inspect the original signature, status and last-valid-block-height before replacing. A retry can duplicate an action across a split sequence. Do not reuse another market's parameters or infer success from a created associated token account.

## Completion

Deliver market/reserve/obligation identity, slot, underlying and receipt units, accrued debt, caps, cash, stress and the precise unsigned sequence or missing prerequisite. Financial execution requires its own authority. Confirm actual signature outcomes and reread the obligation plus receiver balance before reporting repayment, borrowing or withdrawal complete.

Read [current official sources and interface limits](references/sources.md) for the selected deployment. This independently installable workflow was reviewed on 2026-10-25; live amounts, access and contract configuration must be refreshed at use time.
