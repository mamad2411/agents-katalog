---
name: galleon-defi-routing
description: Compare token swaps and cross-chain routes, prepare reviewed transaction handoffs, and track destination delivery or refunds. Use when comparing DEX quotes, selecting bridges, preparing CCTP transfers, investigating stuck transfers, or recovering partial routes.
license: MIT
compatibility: Portable Agent Skills instructions. Live work needs the selected provider's HTTP, MCP or SDK tools; signing stays in the user's trusted wallet. No provider or runtime is installed by this skill.
metadata:
  author: Galleon Labs
  version: "0.4.1"
---

# DeFi routing

Move from an exact asset intent to a comparable quote and, when authorized, a reconciled outcome. A quote, signature, source receipt and destination delivery are different facts.


## Start with the requested task

Use supplied preferences and compatible tools for this request; ask only for missing terms that change its result. Public research needs no wallet. Preferences and tool access never grant financial authority.

## Choose the task

Read [providers](references/providers.md) for official swaps, bridges and CCTP surfaces, access requirements and observed gaps. Read [workflows](references/workflows.md) for transaction sequencing, intent orders, asynchronous recovery and the output record. The [evaluation cases](references/evaluation.md) exercise decision boundaries with fixtures only.

Reuse a suitable connected official tool. Inspect actual schemas and version before relying on a skill or advertised tool list. Documentation MCP supplies reference material; unsigned builders supply proposed calls; signing or submission tools have a separate authority boundary. Do not automatically register a provider, install upstream skills, change accounts, pay for an API request or enable a signer.

## Establish exact intent

Resolve source and destination chain, network, token contract or mint, decimals, amount and exact-in/exact-out mode, sender and final recipient. Tickers and native-token sentinels differ by provider; bridged USDC, native USDC and wrapped assets are separate identities. Confirm the user's slippage, total fee budget, deadline and preferred execution route when those choices affect the result. Preserve already approved unchanged terms.

For comparisons, use the same amount, recipient, route constraints and near-contemporaneous observations. Compare conservative output and all-in costs: approvals, source/destination gas, bridge or solver fees, price impact, protocol/integrator fees and refund costs. An estimated duration is not a finality guarantee. State inaccessible routes instead of silently ranking an incomplete set as the entire market. Compare executable routes rather than preferred quote currencies: any supported quote asset can form a valid leg, including multihop, and an unavailable route is a concrete blocker where a quote symbol is not.

Capital location is not a route constraint. Holdings on another supported chain are deployable through a quoted bridge; count the quote's cost, delivery time and settlement risk as part of the economics instead of treating the holding chain as a blocker. When the destination action needs native gas, quote an owned source asset into the destination native currency delivered to the same account and make that delivery a separately verified prerequisite. A bridge cannot create gas from nothing: the source leg still needs source native gas, so an account with no native gas on any funded chain needs a supported gasless route or a small native deposit, not another quote.

## Prepare and hand off

Validate chain, balances, native gas reserve, token behavior, exact spender and finite allowance, permit domain/deadline, recipient, target, value and calldata. Use the official builder and simulate the exact proposed action when supported. Record unavailable simulation and material uncertainty. Source-chain simulation cannot prove future destination execution.

Separate approvals from swaps or bridge deposits. After approval receipts, obtain a fresh plan if the provider requires rebuilding or quote validity changed. A signature can be an executable off-chain intent even without a gas transaction. Present the final terms before handing the unchanged payload to an existing authorized wallet path. This skill never grants authority to sign, submit, create an account or change permissions. Never add affiliate, referral or builder fees without explicit consent.

## Reconcile before continuing

Persist request/order identity and transaction hashes. On a timeout or lost response, query the original operation before any new write. Continue bounded status reads; exhausted polling means pending or unknown, not failed. Never submit another source transfer to repair a delayed destination leg.

For swaps, require the provider's fill record and matching chain/account state. For bridges, require destination token, amount, recipient and receipt. Report partial output, refund pending, refund received and completion separately; inspect where and in which asset funds arrived. A follow-on swap, lending deposit or retry uses the actual received asset and newly reviewed terms.

## Deliver

Return the selected route or comparison with provider/version, exact identities, amounts, costs, quote expiry, evidence timestamps and unresolved gaps. For a submitted operation, add request ID, source and destination receipts, actual received asset/amount, state and next action. Redact credentials, signed payloads and private evidence. Use the user's installed LP, lending or other skill for the next primitive if available; otherwise return a self-contained handoff rather than silently installing dependencies.

## Worked comparison

Synthetic observations below illustrate the decision; they are not live quotes or receipts.

**Request:** Compare these bridge routes for the same input. Max cost 10 USDC. Use my available tools.

**Available evidence:** Both quotes spend 1,000 USDC and have sufficient destination gas. A minimum net received 994 USDC, including a 4 USDC bridge fee and 2 USDC gas paid from input. B minimum net received 992 USDC, including all costs. Both meet deadline and freshness constraints.

**Read sequence:** Compare exact input, minimum net output, separately paid fees, destination gas and deadlines; normalize included versus additional costs.

**Completed answer:** A has 6 USDC total loss from input, B 8 USDC. Choose A with minimum 994 USDC received; both meet the 10 USDC budget. The nested fee breakdown is already included and is not deducted again. This comparison does not submit a route.

**Changed evidence:** A source receipt succeeds but destination receipt is absent; status is pending and user asks whether to retry.

**Useful response:** Report source confirmed, destination pending, route not reconciled. Track the same bridge message/route identifier and destination balance; do not submit a duplicate route.

Fetch a missing observation through an existing compatible read tool when available; otherwise return the supported partial result and exact gap. Reconcile an uncertain write through its original identity before considering a retry.

## Focused protocol procedures

For a named protocol task, load its focused skill when installed. Discover it by name; this comparison workflow remains usable without sibling files.

- `uniswap-swap`: Quote Uniswap swaps, inspect Permit2 and reconcile AMM or order execution.
- `lifi-cross-chain`: Compare LI.FI quotes and reconcile destination delivery, partial fills and refunds.
- `zerox-swap`: quoting a 0x API v2 swap or inspecting AllowanceHolder, Permit2, issues and minimum-output evidence before an unsigned handoff.
- `oneinch-swap`: quoting a 1inch Classic Swap v6.1 or distinguishing direct calldata, Fusion intents and protected API access.
- `cow-order`: comparing a CoW Protocol quote, reviewing a signed-intent boundary, or reconciling order UID, partial fills, expiry and cancellation.
- `jupiter-swap`: quoting Jupiter Swap v2 on Solana, inspecting immutable order transactions, or reconciling managed execution and token-account deltas.
- `relay-bridge`: preparing a Relay quote or tracking a cross-chain request through source confirmation, destination execution, delay or refund.
- `across-bridge`: comparing Across Swap API routes, inspecting exactInput versus minOutput, or reconciling deposit fills, embedded actions and refunds.
- `circle-cctp`: tracking a Circle CCTP USDC burn, attestation and destination mint, including domain IDs, finality and failed-mint recovery.
