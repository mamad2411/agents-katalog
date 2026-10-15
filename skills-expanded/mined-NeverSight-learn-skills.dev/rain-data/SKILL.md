---
name: rain-data
description: "Query data from the Rain prediction-markets protocol (Arbitrum One) using @buidlrrr/rain-sdk. Use when: fetching market listings, prices, volume, liquidity, positions, portfolio values, transaction history, price charts (OHLCV), P&L analytics, leaderboards, protocol stats, or subscribing to live WebSocket price/event feeds from Rain."
---

# Rain — Data

Query markets, prices, positions, analytics, and live feeds from Rain using `@buidlrrr/rain-sdk`.

```bash
npm install @buidlrrr/rain-sdk  # peer dep: viem ^2.0.0
```

## Setup

```ts
import { Rain } from '@buidlrrr/rain-sdk';

// Minimal — market queries and on-chain reads
const rain = new Rain({ environment: 'production' });

// Full — adds tx history, price charts, analytics, and live feeds
const rain = new Rain({
  environment: 'production',
  subgraphApiKey: 'YOUR_GRAPH_KEY',   // needed for: getTransactions, getPriceHistory, getPnL, getLeaderboard
  wsRpcUrl: 'wss://arb-mainnet.g.alchemy.com/v2/KEY', // needed for: subscribeToMarketEvents, subscribePriceUpdates
});
```

## Markets

```ts
// Browse markets
const markets = await rain.getPublicMarkets({
  limit: 10,
  sortBy: 'Liquidity',  // 'Liquidity' | 'Volumn' | 'latest'
  status: 'Live',        // 'Live' | 'New' | 'WaitingForResult' | 'Closed' | 'Trading' | ...
});
// → [{ id, title, totalVolume, status, contractAddress }]

// Full details (API + on-chain)
const details = await rain.getMarketDetails(markets[0].id);
// → { id, title, status, contractAddress, options, startTime, endTime,
//    allFunds, totalLiquidity, winner, baseToken, baseTokenDecimals, ... }

// Current option prices from AMM
const prices = await rain.getMarketPrices(marketId);
// → [{ choiceIndex, optionName, currentPrice }]  — currentPrice in 1e18

// Volume
const vol = await rain.getMarketVolume(marketId);
// → { totalVolume, optionVolumes: [{ choiceIndex, volume }] }

// Liquidity + order book edges
const liq = await rain.getMarketLiquidity(marketId);
// → { totalLiquidity, optionLiquidity: [{ totalFunds, firstBuyOrderPrice, firstSellOrderPrice }] }

// ID ↔ address lookups
const addr = await rain.getMarketAddress(marketId);
const id = await rain.getMarketId(contractAddress);
```

## Positions & Portfolio

```ts
// All positions across all markets
const positions = await rain.getPositions(walletAddress);
// → { markets: [{ marketId, title, options: [{ shares, sharesInEscrow, currentPrice }], dynamicPayout }] }

// Single market position
const pos = await rain.getPositionByMarket(walletAddress, marketId);

// LP position
const lp = await rain.getLPPosition(walletAddress, marketId);
// → { userLiquidity, totalLiquidity, poolShareBps }

// Portfolio value (token balances + position values)
const portfolio = await rain.getPortfolioValue({
  address: walletAddress,
  tokenAddresses: ['0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9'], // USDT
});
// → { tokenBalances, positions, totalPositionValue }

// Token balances for any address
const bal = await rain.getSmartAccountBalance({
  address: walletAddress,
  tokenAddresses: ['0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9'],
});
```

## Transaction History (requires subgraph)

```ts
// Wallet tx history
const txs = await rain.getTransactions({
  address: walletAddress,
  first: 20,
  orderDirection: 'desc',
  types: ['buy', 'limit_buy_placed'],  // optional filter
});
// types: 'buy' | 'limit_buy_placed' | 'limit_sell_placed' | 'limit_buy_filled' |
//        'limit_sell_filled' | 'cancel_buy' | 'cancel_sell' | 'add_liquidity' | 'claim'

// Decode single tx
const details = await rain.getTransactionDetails({ transactionHash: '0x...' });

// All trades on a market
const trades = await rain.getMarketTransactions({ marketAddress: '0x...', first: 50 });

// User's trades on a market
const history = await rain.getTradeHistory({ address: '0x...', marketAddress: '0x...' });
```

## Analytics (requires subgraph)

```ts
// OHLCV price candles
const candles = await rain.getPriceHistory({
  marketId: '...',
  optionIndex: 0,
  interval: '1h',  // '1m' | '5m' | '15m' | '1h' | '4h' | '1d' | '1w'
});
// → { candles: [{ timestamp, open, high, low, close, volume, trades }] }

// P&L (per-market or aggregate)
const pnl = await rain.getPnL({ address: '0x...' });
// → { totalRealizedPnL, totalUnrealizedPnL, totalPnL, markets: [...], formatted }

// Leaderboard
const leaders = await rain.getLeaderboard({
  timeframe: '7d',  // '24h' | '7d' | '30d' | 'all-time'
  sortBy: 'volume',
  limit: 10,
});

// Protocol stats
const stats = await rain.getProtocolStats();
// → { tvl, totalVolume, activeMarkets, totalMarkets, uniqueTraders }
```

## Live WebSocket Feeds (requires wsRpcUrl)

```ts
// Live market events (trades, orders, claims)
const unsub = rain.subscribeToMarketEvents({
  marketAddress: '0x...',
  eventNames: ['EnterOption', 'PlaceBuyOrder'],  // optional filter
  onEvent: (event) => console.log(event.eventName, event.args),
  onError: (err) => console.error(err),
});

// Live price updates (fires after each trade)
const unsub2 = rain.subscribePriceUpdates({
  marketAddress: '0x...',
  onPriceUpdate: (update) => console.log(update.prices),
  onError: (err) => console.error(err),
});

// Cleanup
unsub();
unsub2();
await rain.destroyWebSocket();
```

Event names: `EnterOption`, `PlaceBuyOrder`, `PlaceSellOrder`, `ExecuteBuyOrder`, `ExecuteSellOrder`, `CancelBuyOrder`, `CancelSellOrder`, `Sync`, `Claim`, `ChooseWinner`, `ClosePool`

## Key Conventions

- Prices: `bigint` in 1e18 scale (`650000000000000000n` = 0.65 = 65% implied probability)
- Token amounts: base token wei (USDT = 6 decimals, `10_000_000n` = 10 USDT)
- Option indices: 0-indexed
- Market IDs: MongoDB-style strings (e.g., `'698c8f116e985bbfacc7fc01'`)
- Timestamps: unix seconds as `bigint`
- Methods requiring subgraph throw if `subgraphUrl`/`subgraphApiKey` not configured
- USDT on Arbitrum: `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9`
