---
name: rain-trade
description: "Trade on Rain prediction markets (Arbitrum One) using @buidlrrr/rain-sdk. Use when: buying or selling option shares, placing limit orders, canceling orders, adding liquidity, claiming winnings, building trading bots, or any on-chain trading interaction with the Rain protocol."
---

# Rain — Trade

Buy, sell, and manage orders on Rain prediction markets using `@buidlrrr/rain-sdk`.

```bash
npm install @buidlrrr/rain-sdk  # peer dep: viem ^2.0.0
```

All tx builders return `{ to, data, value? }`. The SDK never sends — the caller signs and sends.

## Setup

```ts
import { Rain } from '@buidlrrr/rain-sdk';
const rain = new Rain({ environment: 'production' });
```

## Approve First

Before any trade on a market, approve the market contract to spend your tokens:

```ts
const approveTx = rain.buildApprovalTx({
  tokenAddress: '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9', // USDT
  spender: marketContractAddress,
  amount: 100_000_000n, // optional — defaults to max uint256
});
await walletClient.sendTransaction({ ...approveTx, chain: arbitrum });
```

## Market Buy

Buy shares at the current AMM price:

```ts
const tx = rain.buildBuyOptionRawTx({
  marketContractAddress: '0x...',
  selectedOption: 0n,          // 0-indexed, bigint
  buyAmountInWei: 10_000_000n, // 10 USDT
});
await walletClient.sendTransaction({ ...tx, chain: arbitrum });
```

## Limit Buy

Place a buy order at a target price:

```ts
const tx = rain.buildLimitBuyOptionTx({
  marketContractAddress: '0x...',
  selectedOption: 1,
  pricePerShare: 500000000000000000n, // 0.50 in 1e18
  buyAmountInWei: 10_000_000n,
  tokenDecimals: 6,
});
```

## Sell

Place a sell order for shares you hold:

```ts
const tx = rain.buildSellOptionTx({
  marketContractAddress: '0x...',
  selectedOption: 1,
  pricePerShare: 0.75,     // decimal (0 < price < 1)
  shares: 5_000_000n,
  tokenDecimals: 6,
});
```

## Cancel Orders

```ts
// Cancel buy orders
const tx = rain.buildCancelBuyOrdersTx({
  marketContractAddress: '0x...',
  orders: [{ option: 1, price: 0.5, orderID: 1n }],
});

// Cancel sell orders (same interface)
const tx2 = rain.buildCancelSellOrdersTx({
  marketContractAddress: '0x...',
  orders: [{ option: 1, price: 0.75, orderID: 3n }],
});
```

## Add Liquidity

```ts
const tx = rain.buildAddLiquidityTx({
  marketContractAddress: '0x...',
  liquidityAmountInWei: 100_000_000n, // 100 USDT
});
```

No `removeLiquidity` — LPs recover funds via `buildClaimTx` after resolution.

## Claim Winnings

After a market resolves:

```ts
const tx = await rain.buildClaimTx({
  marketId: '698c8f116e985bbfacc7fc01',
  walletAddress: '0x...',
});
await walletClient.sendTransaction({ ...tx, chain: arbitrum });
```

## Check Positions

```ts
// All positions across all markets
const positions = await rain.getPositions('0x...');
// positions.markets[].options[].shares — shares held
// positions.markets[].dynamicPayout — per-option payout if that option wins

// Single market
const pos = await rain.getPositionByMarket('0x...', 'marketId');

// LP position
const lp = await rain.getLPPosition('0x...', 'marketId');
// lp.userLiquidity, lp.poolShareBps
```

## Smart Account (Gas Sponsored)

```ts
import { RainAA } from '@buidlrrr/rain-sdk';

const rainAA = new RainAA({
  walletClient,
  alchemyApiKey: '...',
  paymasterPolicyId: '...',
  chain: arbitrum,
});

const smartAddr = await rainAA.connect();

// Deposit tokens to smart account
const depositTx = rain.buildDepositToSmartAccountTx({
  tokenAddress: '0x...USDT',
  smartAccountAddress: smartAddr,
  amount: 50_000_000n,
});
await walletClient.sendTransaction({ ...depositTx, chain: arbitrum });

// Send trades from smart account (gas sponsored)
const rawTx = rain.buildBuyOptionRawTx({ ... });
const txHash = await rainAA.sendTransaction(rawTx);

// Withdraw back to EOA
const withdrawTx = rain.buildWithdrawFromSmartAccountTx({
  tokenAddress: '0x...USDT',
  eoaAddress: walletAddress,
  amount: 50_000_000n,
});
```

## Key Conventions

- Prices: `bigint` in 1e18 scale (`650000000000000000n` = 0.65 = 65%)
- Token amounts: base token wei (USDT = 6 decimals, `10_000_000n` = 10 USDT)
- Option indices: 0-indexed everywhere
- Market IDs: MongoDB-style strings (e.g., `'698c8f116e985bbfacc7fc01'`)
- `buildApprovalTx` returns `Error` on invalid input (check `instanceof Error`) — all other builders throw
- Use `publicClient.estimateGas()` before sending to catch reverts early
- Common errors: `InsufficientAmount`, `PoolClosed`, `InvalidOption`, `ERC20InsufficientAllowance`
- USDT on Arbitrum: `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9`
