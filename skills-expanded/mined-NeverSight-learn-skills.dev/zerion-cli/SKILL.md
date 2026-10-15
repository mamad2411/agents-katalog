---
name: zerion-cli
description: "Install, configure, and troubleshoot the Zerion CLI for crypto wallet data. Use when setting up authentication, checking CLI status, or debugging connection issues. For actual wallet queries, use the wallet-analysis skill."
compatibility: "Requires Node.js >= 20."
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

# Zerion CLI

Setup, authentication, and troubleshooting for zerion-cli.

**For wallet analysis, use the `wallet-analysis` skill instead.**

## Installation

```bash
# Run without installing (recommended)
npx zerion-cli --help

# Or install globally
npm install -g zerion-cli
```

Requires Node.js 20 or later.

## Authentication

### Option A: API key (recommended for production)

```bash
export ZERION_API_KEY="zk_dev_..."
```

Get yours at [dashboard.zerion.io](https://dashboard.zerion.io).

- Dev keys start with `zk_dev_`
- Rate limits: 120 requests/minute, 5,000 requests/day
- Auth method: HTTP Basic Auth (key as username, empty password)

### Option B: x402 pay-per-call (no signup)

No API key needed. Pay $0.01 USDC per request via the [x402 protocol](https://www.x402.org/). Supports EVM (Base) and Solana.

**Single key** — format is auto-detected:

```bash
export WALLET_PRIVATE_KEY="0x..."    # EVM (Base) — 0x-prefixed hex
export WALLET_PRIVATE_KEY="5C1y..."  # Solana — base58 encoded keypair
```

**Both chains simultaneously:**

```bash
export EVM_PRIVATE_KEY="0x..."
export SOLANA_PRIVATE_KEY="5C1y..."
export ZERION_X402_PREFER_SOLANA=true  # optional: prefer Solana when both are set

# Per-command flag
zerion-cli wallet analyze <address> --x402

# Or set globally via environment
export ZERION_X402=true
```

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ZERION_API_KEY` | Yes (unless x402) | API key from dashboard.zerion.io |
| `WALLET_PRIVATE_KEY` | Yes (for x402, single key) | Auto-detected: 0x-hex for EVM/Base, base58 for Solana |
| `EVM_PRIVATE_KEY` | No | EVM private key for x402; overrides `WALLET_PRIVATE_KEY` for EVM |
| `SOLANA_PRIVATE_KEY` | No | Solana base58 keypair for x402; overrides `WALLET_PRIVATE_KEY` for Solana |
| `ZERION_X402` | No | Set to `true` to enable x402 pay-per-call globally |
| `ZERION_X402_PREFER_SOLANA` | No | Set to `true` to prefer Solana when both keys are configured |
| `ZERION_API_BASE` | No | Override API base URL (default: `https://api.zerion.io/v1`) |

## CLI help

```bash
zerion-cli --help
```

Returns JSON with all available commands, env vars, and x402 info.

## Available commands

```
zerion-cli wallet analyze <address>       # Full wallet analysis
zerion-cli wallet portfolio <address>     # Portfolio overview
zerion-cli wallet positions <address>     # Token + DeFi positions
zerion-cli wallet transactions <address>  # Transaction history
zerion-cli wallet pnl <address>           # Profit and loss
zerion-cli chains list                    # Supported chains
```

All commands accept `--x402` for pay-per-call auth.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `missing_api_key` | No `ZERION_API_KEY` set | Set the env var or use `--x402` |
| `unsupported_chain` | Invalid `--chain` value | Run `zerion-cli chains list` for valid IDs |
| `api_error` status 401 | Invalid API key | Check key at dashboard.zerion.io |
| `api_error` status 429 | Rate limited | Wait, reduce request frequency, or use x402 |
| `api_error` status 400 | Invalid address or ENS resolution failed | Retry with a valid 0x hex address |
| `unexpected_error` | `WALLET_PRIVATE_KEY` missing in x402 mode | Export the private key or disable x402 |
| `unexpected_error` | Node.js version too old | Requires Node.js >= 20 |

## Resources

- API docs: [developers.zerion.io](https://developers.zerion.io)
- Dashboard: [dashboard.zerion.io](https://dashboard.zerion.io)
- x402 protocol: [x402.org](https://www.x402.org/)
- Source: [github.com/zeriontech/zerion-ai](https://github.com/zeriontech/zerion-ai)
