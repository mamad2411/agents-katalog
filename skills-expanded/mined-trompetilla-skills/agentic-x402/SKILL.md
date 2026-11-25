---
name: agentic-x402
description: Make x402 payments to access gated APIs and content. Fetch paid resources, check wallet balance, and create payment links. Use when encountering 402 Payment Required responses or when the user wants to pay for web resources with crypto.
license: MIT
compatibility: Requires Node.js 20+, network access to x402 facilitators and EVM chains
metadata:
  author: monemetrics
  version: "0.1.0"
allowed-tools: Bash(x402:*) Bash(npm:*) Read
---

# x402 Agent Skill

Pay for x402-gated APIs and content using USDC on Base. This skill enables agents to autonomously make crypto payments when accessing paid web resources.

## Quick Reference

| Command | Description |
|---------|-------------|
| `x402 balance` | Check USDC and ETH balances |
| `x402 pay <url>` | Pay for a gated resource |
| `x402 fetch <url>` | Fetch with auto-payment |
| `x402 create-link` | Create payment link (seller) |
| `x402 link-info <addr>` | Get payment link details |

## Setup

1. Install dependencies:
```bash
cd {baseDir} && npm install
```

2. Configure wallet (create `.env` in working directory):
```bash
EVM_PRIVATE_KEY=0x...your_private_key...
X402_NETWORK=mainnet  # or testnet
```

3. Verify setup:
```bash
x402 balance
```

## Paying for Resources

### When you encounter HTTP 402 Payment Required

Use `x402 pay` to make the payment and access the content:

```bash
x402 pay https://api.example.com/paid-endpoint
```

The command will:
1. Check payment requirements
2. Verify amount is within limits
3. Process the payment
4. Return the gated content

### Automatic payment with fetch

Use `x402 fetch` for seamless payment handling:

```bash
x402 fetch https://api.example.com/data --json
```

This wraps fetch with x402 payment handling - if the resource requires payment, it's handled automatically.

### Payment limits

By default, payments are limited to $10 USD. Override with `--max`:

```bash
x402 pay https://expensive-api.com/data --max 50
```

Or set globally:
```bash
export X402_MAX_PAYMENT_USD=25
```

### Dry run

Preview payment without executing:

```bash
x402 pay https://api.example.com/data --dry-run
```

## Creating Payment Links (Seller)

Create payment links to monetize your own content using x402-links-server:

### Setup for link creation

Add to `.env`:
```bash
X402_LINKS_API_URL=https://your-x402-links-server.com
X402_LINKS_API_KEY=your_api_key
```

### Create a link

Gate a URL:
```bash
x402 create-link --name "Premium API" --price 1.00 --url https://api.example.com/premium
```

Gate text content:
```bash
x402 create-link --name "Secret" --price 0.50 --text "The secret message..."
```

With webhook notification:
```bash
x402 create-link --name "Guide" --price 5.00 --url https://mysite.com/guide --webhook https://mysite.com/payment-hook
```

### Get link info

```bash
x402 link-info 0x1234...5678
x402 link-info https://21.cash/pay/0x1234...5678
```

## Command Reference

### x402 balance

Check wallet balances.

```bash
x402 balance [--json] [--full]
```

Options:
- `--json`: Output as JSON
- `--full`: Show full addresses

### x402 pay

Pay for an x402-gated resource.

```bash
x402 pay <url> [options]
```

Options:
- `--method <METHOD>`: HTTP method (default: GET)
- `--body <JSON>`: Request body for POST/PUT
- `--max <USD>`: Maximum payment limit
- `--dry-run`: Preview without paying

### x402 fetch

Fetch with automatic payment.

```bash
x402 fetch <url> [options]
```

Options:
- `--method <METHOD>`: HTTP method (default: GET)
- `--body <JSON>`: Request body
- `--json`: Output JSON only (for piping)
- `--raw`: Output raw response body

### x402 create-link

Create a payment link.

```bash
x402 create-link --name <name> --price <usd> [options]
```

Required:
- `--name <name>`: Link name
- `--price <usd>`: Price in USD (e.g., "5.00")

Content (one required):
- `--url <url>`: URL to gate
- `--text <content>`: Text to gate

Options:
- `--desc <text>`: Description
- `--webhook <url>`: Webhook for notifications
- `--json`: Output as JSON

### x402 link-info

Get payment link details.

```bash
x402 link-info <router-address> [--json]
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EVM_PRIVATE_KEY` | Wallet private key | Required |
| `X402_NETWORK` | `mainnet` or `testnet` | `mainnet` |
| `X402_MAX_PAYMENT_USD` | Max payment limit | `10` |
| `X402_FACILITATOR_URL` | Custom facilitator | Auto |
| `X402_LINKS_API_URL` | x402-links-server URL | - |
| `X402_LINKS_API_KEY` | API key for links | - |
| `X402_VERBOSE` | Enable debug logging | `0` |

## Supported Networks

| Network | Chain ID | CAIP-2 ID |
|---------|----------|-----------|
| Base Mainnet | 8453 | eip155:8453 |
| Base Sepolia | 84532 | eip155:84532 |

## Payment Token

All payments use **USDC** (USD Coin) on the selected network.

- Base Mainnet: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Base Sepolia: `0x036CbD53842c5426634e7929541eC2318f3dCF7e`

## How x402 Works

1. Client requests a resource
2. Server responds with `402 Payment Required` + payment details
3. Client signs a payment authorization (USDC transfer)
4. Client retries request with payment signature
5. Server verifies payment via facilitator
6. Server settles payment on-chain
7. Server returns the gated content

The x402 protocol is gasless for buyers - the facilitator sponsors gas fees.

## Troubleshooting

### "Missing required environment variable: EVM_PRIVATE_KEY"

Set your wallet private key:
```bash
export EVM_PRIVATE_KEY=0x...
```

Or create a `.env` file in your working directory.

### "Payment exceeds max limit"

Increase the limit:
```bash
x402 pay https://... --max 50
```

### Low balance warnings

Fund your wallet with:
- **USDC** for payments
- **ETH** for gas (small amount, ~0.001 ETH)

### Network mismatch

Ensure your wallet has funds on the correct network:
- `X402_NETWORK=mainnet` → Base mainnet
- `X402_NETWORK=testnet` → Base Sepolia

## Security Notes

- Never share your private key
- Start with testnet to verify setup
- Set reasonable payment limits
- Review payment amounts before confirming

## Links

- [x402 Protocol Docs](https://docs.x402.org/)
- [x402 GitHub](https://github.com/coinbase/x402)
- [Base Network](https://base.org/)
