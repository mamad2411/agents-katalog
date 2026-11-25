---
name: chains
description: "List blockchain networks supported by Zerion. Use when validating chain names, checking supported networks, or looking up chain metadata before querying wallet data."
compatibility: "Requires zerion-cli (`npx zerion-cli` or `npm install -g zerion-cli`). Set ZERION_API_KEY or use --x402 for pay-per-call."
license: MIT
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins:
        - zerion-cli
    install:
      - kind: node
        package: "zerion-cli"
        bins: [zerion-cli]
    homepage: https://github.com/zeriontech/zerion-ai
---

# Chains

List supported blockchain networks using zerion-cli.

## Setup check

```bash
which zerion-cli || npm install -g zerion-cli
```

## Command

```bash
zerion-cli chains list [--x402]
```

Returns the full chain catalog with IDs and metadata.

## When to use

- User asks "what chains does Zerion support?"
- You need the current chain catalog before choosing a `--chain` value
- Looking up chain metadata (name, type, support level)

## Quick reference (common chain IDs)

These are the chain IDs currently accepted by the wallet commands in this repo:

| Chain | ID |
|-------|----|
| Ethereum | `ethereum` |
| Base | `base` |
| Arbitrum | `arbitrum` |
| Optimism | `optimism` |
| Polygon | `polygon` |
| BNB Chain | `bsc` |
| Avalanche | `avalanche` |
| Gnosis | `gnosis` |
| Scroll | `scroll` |
| Linea | `linea` |
| zkSync | `zksync` |
| Solana | `solana` |
| Zora | `zora` |
| Blast | `blast` |

`zerion-cli chains list` may return a broader catalog. For `wallet positions`, `wallet transactions`, and `wallet analyze`, use the IDs above unless the CLI validator is expanded.

## Using with wallet commands

```bash
# Positions on a specific chain
zerion-cli wallet positions <address> --chain ethereum

# Transactions on a specific chain
zerion-cli wallet transactions <address> --chain base

# Full analysis filtered to one chain
zerion-cli wallet analyze <address> --chain arbitrum
```
