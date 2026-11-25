---
name: lbamm-clob
description: Generate integration code for the LBAMM CLOBTransferHandler -- on-chain limit order book with maker deposits, FIFO order filling, and price-linked lists. Generates Foundry scripts for maker flows (deposit, open/close orders, withdraw) and taker flows (filling orders through AMM swaps). Use this skill whenever the user asks about LBAMM CLOB, on-chain order books, limit orders on LBAMM, maker/taker flows, CLOB deposits, or filling CLOB orders.
user-invocable: true
disable-model-invocation: true
argument-hint: "[description of CLOB integration]"
---

# LBAMM CLOB Integration Generator

Generate complete integration code for the LBAMM on-chain Central Limit Order Book (CLOB). The CLOBTransferHandler allows makers to deposit tokens and place limit orders at specific prices. Takers fill orders by executing AMM swaps with the CLOB as the transfer handler.

## Project Setup

Before generating code, check the user's project is configured:
1. **Foundry**: `foundry.toml` must exist. If not: `forge init`
2. **LBAMM Core**: `lib/lbamm-core/` must exist. If not: `forge install limitbreakinc/lbamm-core`
3. **LBAMM Hooks and Handlers**: `lib/lbamm-hooks-and-handlers/` must exist. If not: `forge install limitbreakinc/lbamm-hooks-and-handlers`
4. **Remappings**: `remappings.txt` needs both `@limitbreak/lbamm-core/=lib/lbamm-core/` and `@limitbreak/lbamm-hooks-and-handlers/=lib/lbamm-hooks-and-handlers/`. Append if missing.
5. **Local testing**: LBAMM is in audit and not yet on public networks. For local testing, use `lbamm-examples` -- see `lbamm-protocol/references/local-dev.md`. Generated scripts should read addresses from environment variables (`vm.envAddress`) so they work with the local Anvil deployment.

## Instructions

1. **Parse requirements** from `$ARGUMENTS` -- determine what kind of CLOB integration the user needs (maker-side, taker-side, or both)

2. **Resolve ambiguities before generating** -- if $ARGUMENTS doesn't specify token/pool addresses, which side (maker vs taker vs both), or order parameters (prices, amounts), ask in a single message. If clear, proceed.

3. **Determine the flow:**
   - **Maker flow**: Deposit tokens, open orders at specific prices, close orders, withdraw balances
   - **Taker flow**: Fill CLOB orders by executing AMM swaps with the CLOB handler as transfer handler
   - **Quotor**: Query order book state (current price, input remaining at a price level)

4. **Generate complete integration code** covering:

   **For Maker flows:**
   - `depositToken()` -- transfer tokens to the CLOB for order placement
   - `openOrder()` -- place a limit order at a specific `sqrtPriceX96` with a group key
   - `closeOrder()` -- cancel an unfilled/partially filled order and reclaim tokens
   - `withdrawToken()` -- withdraw deposited balance back to the maker
   - Group key generation via `generateGroupKey(hook, minimumOrderBase, minimumOrderScale)`
   - `HooksExtraData` construction for token hooks and CLOB hooks
   - Price hint optimization for efficient linked-list insertion

   **For Taker flows:**
   - `FillParams` struct encoding with `groupKey`, `maxOutputSlippage`, and `hookData`
   - `transferData` encoding using `bytes.concat` (NOT `abi.encode`)
   - `swapOrder.recipient` must be set to the CLOB handler address (the handler collects output tokens)
   - Only input-based swaps (`amountSpecified >= 0`) -- output-based swaps revert
   - Understanding that excess output is refunded to the executor via the `afterSwapRefund` callback

5. **Handle price calculations:**
   - Orders use `sqrtPriceX96` format: `sqrtPriceX96 = sqrt(amountOut / amountIn) * 2^96`
   - Output calculation: `amountOut = mulDivRoundingUp(mulDivRoundingUp(amountIn, sqrtPriceX96, Q96), sqrtPriceX96, Q96)`
   - Price bounds: `MIN_SQRT_RATIO` to `MAX_SQRT_RATIO`

6. **Handle edge cases:**
   - `openOrder()` auto-collects via `transferFrom` if maker's deposited balance is insufficient
   - Order amounts are capped at `uint128.max`
   - Minimum order size enforced by `minimumOrderBase * 10^minimumOrderScale`
   - Maximum order scale is 72
   - Maker balances for filled orders are credited during fill, not transferred immediately
   - Makers withdraw filled output tokens via `withdrawToken()` after their orders fill

## Reference Files

- `references/clob-reference.md` -- Complete data structures, maker/taker flows, quotor, hook system, events, error reference, end-to-end examples
- Handler architecture: `lbamm-handler-protocol`
- Protocol knowledge: `lbamm-protocol`

## Common Mistakes

- Setting `swapOrder.recipient` to an address other than the CLOB handler -- it must be `address(this)` (the handler address)
- Using output-based swaps (`amountSpecified < 0`) -- the CLOB only supports input-based swaps
- Using `abi.encode(address, bytes)` for transferData instead of `bytes.concat` -- the AMM reads raw bytes, not ABI-encoded
- Confusing `groupKey` with `orderBookKey` -- the group key is a packed `bytes32` of `(hook, minimumOrderBase, minimumOrderScale)`, while the order book key hashes `(tokenIn, tokenOut, groupKey)` together
- Forgetting that excess output goes to the executor (taker), not to makers -- makers get credited via `makerTokenBalance` during fills

## Dependencies

```
@limitbreak/lbamm-core/src/interfaces/ILimitBreakAMMTransferHandler.sol
@limitbreak/lbamm-core/src/DataTypes.sol
@limitbreak/lbamm-hooks-and-handlers/src/handlers/clob/CLOBTransferHandler.sol
@limitbreak/lbamm-hooks-and-handlers/src/handlers/clob/DataTypes.sol
@limitbreak/lbamm-hooks-and-handlers/src/handlers/clob/Constants.sol
```

## Related Skills

- **lbamm-handler-protocol** -- Transfer handler architecture and custom handler development
- **lbamm-permit-handler** -- Gasless swap settlement via EIP-712 signed permits (alternative handler)
- **lbamm-integrator** -- Generate router contracts that use handlers via directSwap
- **lbamm-test** -- Generate Foundry test suites for CLOB integration flows
