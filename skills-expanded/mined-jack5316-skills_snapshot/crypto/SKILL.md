---
name: crypto
description: Fetch and analyze cryptocurrency market data using CoinGecko API. Use when user asks for crypto prices, market data, or /crypto.
---

# Crypto Market Skill

Fetches real-time cryptocurrency market data from CoinGecko (free API, no key needed) and creates a comprehensive digest with AI-powered analysis.

## Usage

```bash
python3 _scripts/crypto_market.py
```

With custom cryptos:
```bash
python3 _scripts/crypto_market.py --cryptos bitcoin ethereum solana
```

## Default Cryptos

bitcoin, ethereum, solana, cardano, polkadot

## Output

`Sources/Crypto Market Digest - YYYY-MM-DD.md` (market overview, table, AI analysis with [[wikilinks]])
