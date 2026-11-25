---
name: eyebot-tradebot
description: High-performance trading and swap execution engine
version: 1.2.0
author: ILL4NE
metadata:
  chains: [base, ethereum, polygon, arbitrum]
  category: trading
---

# TradeBot 📈

**Intelligent Trade Execution**

Execute swaps with best-route aggregation across 400+ liquidity sources. Supports limit orders, DCA strategies, and MEV protection.

## Features

- **Route Aggregation**: Best prices across all DEXs
- **MEV Protection**: Private transactions to avoid frontrunning
- **Limit Orders**: Set target prices for automatic execution
- **DCA Engine**: Dollar-cost averaging strategies
- **Multi-Hop**: Complex routing for optimal rates

## Capabilities

| Function | Description |
|----------|-------------|
| Swap | Instant token swaps |
| Limit Order | Price-triggered execution |
| DCA | Scheduled recurring buys |
| Quote | Get best rate preview |
| History | Track all trades |

## Supported Aggregators

- 1inch
- OpenOcean
- 0x Protocol
- Paraswap
- Native DEX routing

## Usage

```bash
# Instant swap
eyebot tradebot swap ETH USDC 0.5

# Set limit order
eyebot tradebot limit BUY ETH 0.5 --price 2000

# Start DCA
eyebot tradebot dca ETH 100 --interval daily
```

## Support
Telegram: @ILL4NE
