---
name: lcx-liberty-swap
description: "Use when quoting an LCX Liberty DEX swap on an EVM chain, comparing its after-gas floor with other providers, or building and checking its unsigned same-chain or cross-chain transaction."
license: MIT
compatibility: "Read-only protocol API through existing configured tools. Needs LCX_API_KEY in the environment. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.5.0"
---

# LCX Liberty DEX swap

Return a quote comparison or an exact unsigned LCX Liberty DEX swap plan. LCX Liberty DEX is a non-custodial EVM aggregator that routes through its own pool index and router contract. A quote, a build and a fill are different facts.

## Check access first

Every request needs the user's own key, read from `LCX_API_KEY` and sent as `Authorization: Bearer $LCX_API_KEY`. Before the first request, check that `LCX_API_KEY` is set. If it is missing, stop and report: `LCX_API_KEY is not set. Create a key at https://dex.lcx.com/dashboard and export LCX_API_KEY before using lcx-liberty-swap.` Do not ask the user to paste the key into the conversation, never write it to a file, a query string or a log, and do not create an account on the user's behalf.

A request without a key returns 401 `API_KEY_REQUIRED`; a present key that does not resolve returns 401 `INVALID_API_KEY` and is never served anonymously. A key pinned to other origins or IPs returns 403. Only `/health` and `/ready` answer without a key.

## Read the exact swap

Collect chain ID, sell and buy token addresses, raw sell amount, taker, recipient and the user's slippage or loss limit. Read the chain's row in `GET /v1/chains`: `available`, `degraded` and `routerDeployed` decide whether a quote can become a transaction, `router` is the contract the handoff must target, and `nativeIsToken` decides how the gas coin is named. Where `nativeIsToken` is false the native coin is the zero address. Where it is true (Arc, whose gas coin is USDC) there is no native placeholder: name the coin by its token contract address, resolved with `GET /v1/tokens`, and sell it like any ERC-20, with an approval and a `value` of 0. Price with `POST /v1/quote` as shown in [reads](references/reads.md). `amountIn` is an integer string in the sell token's base units; `slippageBps` defaults to 50 and is capped at 2000.

Inspect `output.amount`, `output.minimumAmount`, `gasEstimateWei`, `gasFeeUSD`, `priceImpactPct`, `routes`, `venues`, `blockNumber`, `expiresAt` and `stale`. A missing `priceImpactPct` means one side cannot be priced from the index: warn instead of proceeding. `stale: true` will not build, and a `degraded` chain quotes but refuses builds. `no_route`, `insufficient_liquidity`, `transfer_tax` and `transfer_blocked` are concrete gaps, not weaker quotes.

## Compare on one unit

Compare providers for the same chain, tokens, raw amount and recipient within one block window, on the guaranteed minimum rather than the headline output:

1. Convert each provider's guaranteed minimum to whole units of the same output token: raw amount / 10^decimals, with that token's own decimals (LCX responses name each side's). LCX's figure is `output.minimumAmount`, or `endToEndMinOut` for a cross-chain journey. Different output tokens, or one symbol at different contracts, need a dated price for each, and the comparison is incomplete without it.
2. Subtract only costs the user pays separately from the output, converted to that unit at a stated price: swap gas, plus approval gas when an approval is still needed. LCX's `gasEstimateWei` and `gasFeeUSD` cover the swap only and exclude the approval; `null` means unknown, never zero.
3. Do not subtract a fee the output already carries: a bridge or relay fee taken before delivery is inside `endToEndMinOut`, and an integrator fee in the quote's fee block is taken from the output. Count each cost once.

Report each provider's net figure with its prices, gas and block. If gas, approval or price data is missing for any side, name it and call the comparison incomplete instead of ranking.

## Build and bind

`POST /v1/build` takes the `quoteId`, the `recipient` and the same `slippageBps` the quote used; a different value returns `slippage_mismatch` rather than being clamped. It returns `swap` (`chainId`, `to`, `data`, `value`), `minAmountOut`, `deadline`, `routerDeployed` and a `simulation` block. The floor comes from the output the user was shown, not from a fresh price: if the market has fallen below it the build is refused with `price_moved`. A `quoteId` lives 120 seconds; on `QUOTE_EXPIRED` re-quote and show the new price. Building twice from one `quoteId` is safe.

Matching addresses alone do not bind a build to the request. Re-read `GET /v1/chains` at handoff time and stop unless every check in [handoff](references/handoff.md) holds:

- `swap.chainId` is the requested chain, `routerDeployed` is true, and `swap.to`, the quote's `spender` and the chain's live `router` are one address. A `to` that equals `spender` but not `router` is a stop.
- `swap.value` equals the amount sold when selling the native coin and is 0 otherwise, including every sale on a `nativeIsToken` chain.
- `swap.data` decodes against one of the router's five swap entrypoints, and its sell and buy tokens, amount sold, recipient, minimum output (at least the quote's `minimumAmount` and the user's own limit) and future deadline match the reviewed request and quote, with the maker-leg and integrator rules satisfied.

Never keep a router address list: the live `/v1/chains` row is the source. On any mismatch, report the failed check and re-quote; never edit calldata.

Approve only that router, for the finite sell amount, after checking `GET /v1/allowance`. Native input needs no approval (`nativeIn: true`). `simulation.status` `ok` with `deliveredVsQuotedBps` near zero supports the plan but is not a fill. An ERC-20 build made before approval returns `status` `skipped` with `why` `awaiting_allowance`: report the simulation as not yet run, then rebuild and rerun the checks after the approval receipt. Never request an integrator; a decoded integrator other than the zero address is a stop.

## Cross chains

Add `toChainId` and `recipient` to the quote. The answer is a journey: read `shape`, `legs`, `endToEndMinOut`, `endToEndOut`, `etaSec` and `expiresAt`. `endToEndMinOut` is the floor for the whole journey; the last leg's `minOut` is not. Each bridge leg is a short-lived offer, so read `expiresAt` instead of assuming 120 seconds. `bridge_too_small` and `bridge_too_large` carry the limit in their message, and refused options come back in `rejected` with a reason.

The build returns one `transactionRequest` on the source chain and an `approval.target`, the cross router, which can differ from the quote's spender: approve the build's target. Stop unless `transactionRequest.chainId` is the source chain, `approval.amount` equals the amount sold, the build is for the recipient the quote was priced for and `endToEndMinOut` meets the user's limit. No published ABI or live address source covers the cross router, so report its target and calldata as not independently decoded rather than as a bound handoff. A confirmed source transaction is not delivery. Poll `tracking.status` (`/v1/bridge/transfers/{transferId}`) and never send a second transfer to repair a pending one.

## Resolve the result

A quote, simulation or broadcast is not a fill. For a submitted swap read the receipt and the buy-token delta at the recipient against `minAmountOut`. On timeout keep the original hash and inspect it before any retry. On 401 report missing or invalid access. On 429 wait as the response instructs rather than switching keys. `store_unavailable` (503) means the chain's index is behind its freshness window: retry later instead of forcing a build.

## Worked result

Synthetic quote sells 0.01 ETH on Base for USDC: `output.amount` 18.226954 USDC, `minimumAmount` 18.135819 at 50 bps, `gasFeeUSD` 0.004, `nativeIn` true, `spender` R. `/v1/chains` for 8453 shows `routerDeployed` true, `nativeIsToken` false and `router` R. The build returns `swap.chainId` 8453, `swap.to` R, `value` 10000000000000000, and `swapSplit` calldata selling exactly that amount of the zero address for USDC to the requested recipient with `minAmountOut` 18135819 and a deadline five minutes out; simulation is `ok` 1 bp under quoted. Return an unsigned handoff with no approval step, an 18.135819-USDC floor and 18.131819 USDC net of gas at USDC = $1. Had `swap.to` and `spender` both been S while the chain's `router` is R, or the decoded recipient differed, return no handoff and re-quote. After `expiresAt` the build answers `QUOTE_EXPIRED`: re-quote and show the new price.

## Sources and limits

Primary documentation reviewed 2026-11-17. Response shapes were checked against the live API without a key and a non-production instance; no account authorization, signing or financial action was tested. [Read recipes and current primary sources](references/reads.md) and the [handoff check](references/handoff.md) ship with this skill. Recheck supported chains and schemas before a consequential handoff. Research adds no permission to trade, transfer or change account authority.
