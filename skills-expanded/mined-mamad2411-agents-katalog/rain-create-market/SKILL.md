---
name: rain-create-market
description: "Create prediction markets on the Rain protocol (Arbitrum One) using @buidlrrr/rain-sdk. Use when: building market creation flows, deploying new prediction markets, setting up initial liquidity, configuring market options/probabilities, or any task involving Rain's buildCreateMarketTx method."
---

# Rain — Create Market

Create prediction markets on Arbitrum One using `@buidlrrr/rain-sdk`.

```bash
npm install @buidlrrr/rain-sdk  # peer dep: viem ^2.0.0
```

## How It Works

`buildCreateMarketTx` returns an array of unsigned transactions. The first may be a token approval, the second is the market creation. Execute them sequentially — the caller signs and sends.

```ts
import { Rain } from '@buidlrrr/rain-sdk';

const rain = new Rain({ environment: 'production' });

const txs = await rain.buildCreateMarketTx({
  marketQuestion: 'Will ETH hit $10k by end of 2026?',
  marketOptions: ['Yes', 'No', 'Unlikely'],
  marketTags: ['crypto'],
  marketDescription: 'ETH price prediction',
  isPublic: true,
  isPublicPoolResolverAi: false,
  creator: walletAddress,
  startTime: BigInt(Math.floor(Date.now() / 1000) + 3600),     // 1h from now
  endTime: BigInt(Math.floor(Date.now() / 1000) + 604800),     // 1 week from now
  no_of_options: 3n,
  inputAmountWei: 100_000_000n,   // 100 USDT initial liquidity
  barValues: [34, 33, 33],        // initial probability distribution (%)
  baseToken: '0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9', // USDT on Arbitrum
  tokenDecimals: 6,
});

for (const tx of txs) {
  const hash = await walletClient.sendTransaction({ ...tx, chain: arbitrum });
  await publicClient.waitForTransactionReceipt({ hash });
}
```

## Validation Rules

| Field | Rule |
|-------|------|
| `marketOptions` | 3–26 items, no empty strings |
| `marketTags` | 1–3 items, no empty strings |
| `no_of_options` | Must match `marketOptions.length` |
| `startTime` | Must be < `endTime` |
| `inputAmountWei` | Min 10 tokens (e.g., `10_000_000n` for 6-decimal USDT) |
| `barValues` | Array of integers summing to ~100, length matches options |

Throws on validation failure.

## Resolution (Admin/Resolver Only)

After a market ends, the resolver closes it and picks the winner:

```ts
// Combined close + choose winner
const txs = await rain.buildResolveMarketTx({
  marketId: '698c8f116e985bbfacc7fc01',
  winningOption: 1,  // 1-indexed (not 0)
});

for (const tx of txs) {
  await walletClient.sendTransaction({ ...tx, chain: arbitrum });
}
```

Or step by step:

```ts
const closeTx = await rain.buildCloseMarketTx({ marketId: '...' });
const winnerTx = await rain.buildChooseWinnerTx({ marketId: '...', winningOption: 1 });
```

## Key Conventions

- All tx builders return `{ to, data, value? }` — the SDK never sends transactions
- Prices: `bigint` in 1e18 scale (e.g., `650000000000000000n` = 0.65 = 65%)
- Token amounts: base token wei (USDT = 6 decimals, so `10_000_000n` = 10 USDT)
- `winningOption` is **1-indexed** in resolve/chooseWinner. Everything else is 0-indexed.
- USDT on Arbitrum: `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9`

## Environments

| Env | API | Factory |
|-----|-----|---------|
| `production` | `prod-api.rain.one` | `0xccCB3C03D9355B01883779EF15C1Be09cf3623F1` |
| `stage` | `stg-api.rain.one` | `0x6109c9f28FE3Ad84c51368f7Ef2d487ca020c561` |
| `development` | `dev-api.rain.one` | `0x148DA7F2039B2B00633AC2ab566f59C8a4C86313` |
