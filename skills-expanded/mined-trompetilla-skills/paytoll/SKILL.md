---
name: paytoll
description: DeFi intelligence, crypto utilities, and LLM access via x402 micro-payments on Base. Query Aave markets, yields, positions, token prices, ENS names, wallet validation, and AI models — all paid per-call in USDC with no API keys.
metadata: {"mcpServers":{"paytoll":{"command":"npx","args":["-y","paytoll-mcp"],"env":{"PAYTOLL_API_URL":"https://api.paytoll.io","PRIVATE_KEY":"${PRIVATE_KEY}"}}}}
requires.env: ["PRIVATE_KEY"]
requires.bins: ["node"]
---

# PayToll

You have access to DeFi intelligence, crypto utilities, and LLM tools via the PayToll MCP server. Each tool call costs a small amount of USDC on the Base network, paid automatically from the user's configured wallet. No API keys or subscriptions needed — payment is the auth.

## Setup Requirements

The user must have:
- A wallet private key set as `PRIVATE_KEY` in their environment
- USDC on the Base network in that wallet (for tool call payments)
- A small amount of ETH on Base (for gas fees)

## Available Tools

### Aave DeFi Intelligence

Use these tools when the user asks about DeFi yields, borrowing, lending, or Aave positions.

**`aave-best-yield`** ($0.01/call)
Find the best supply APY for a given asset across all Aave v3 deployments and chains.
- Use when: "What's the best yield for USDC?", "Where should I supply ETH for the highest APY?"
- Input: `asset` (e.g., "USDC", "ETH", "WBTC")

**`aave-best-borrow`** ($0.01/call)
Find the lowest borrow APR for an asset across all Aave v3 markets.
- Use when: "Cheapest place to borrow DAI?", "What's the lowest ETH borrow rate?"
- Input: `asset` (e.g., "USDC", "ETH", "DAI")

**`aave-markets`** ($0.005/call)
Get comprehensive data for all Aave v3 markets including supply/borrow rates, TVL, and utilization.
- Use when: "Show me all Aave markets", "Overview of DeFi lending rates", "What assets can I supply on Aave?"

**`aave-health-factor`** ($0.005/call)
Calculate a user's health factor on Aave — indicates how close a position is to liquidation.
- Use when: "What's my health factor?", "Am I at risk of liquidation?", "Check health for 0x..."
- Input: `address` (Ethereum address)

**`aave-user-positions`** ($0.01/call)
Get a user's complete supply and borrow positions on Aave across chains.
- Use when: "What are my Aave positions?", "Show my DeFi portfolio", "What am I supplying/borrowing?"
- Input: `address` (Ethereum address)

### Crypto Utilities

Use these tools for token prices, ENS resolution, and address validation.

**`crypto-price`** ($0.001/call)
Get current token prices from CoinGecko.
- Use when: "Price of ETH?", "How much is BTC worth?", "What's the USDC price?"
- Input: `token` (e.g., "ethereum", "bitcoin", "solana")

**`ens-lookup`** ($0.001/call)
Resolve ENS names to Ethereum addresses.
- Use when: "What address is vitalik.eth?", "Resolve myname.eth"
- Input: `name` (e.g., "vitalik.eth")

**`wallet-validator`** ($0.0005/call)
Validate whether a string is a valid wallet address (supports Ethereum, Bitcoin, Solana).
- Use when: "Is this a valid address?", "Check if 0x... is valid"
- Input: `address`, `chain` (optional)

### Aave Transactions

Use these tools when the user wants to generate transaction data for Aave operations.

**`aave-supply`** ($0.01/call)
Generate supply transaction data for depositing assets into Aave.
- Use when: "Supply 100 USDC to Aave", "Deposit ETH into Aave"
- Input: `asset`, `amount`, `address`

**`aave-borrow`** ($0.01/call)
Generate borrow transaction data for borrowing assets from Aave.
- Use when: "Borrow 50 DAI from Aave", "Take a USDC loan on Aave"
- Input: `asset`, `amount`, `address`

**`aave-repay`** ($0.01/call)
Generate repay transaction data for paying back Aave loans.
- Use when: "Repay my DAI loan", "Pay back 100 USDC on Aave"
- Input: `asset`, `amount`, `address`

**`aave-withdraw`** ($0.01/call)
Generate withdraw transaction data for removing assets from Aave.
- Use when: "Withdraw my USDC from Aave", "Pull out my ETH supply"
- Input: `asset`, `amount`, `address`

### LLM Proxy

Use these tools when the user wants to query AI models through PayToll.

**`llm-openai`** ($0.01/call)
Query OpenAI GPT models.
- Use when: "Ask GPT...", "Use OpenAI to..."
- Input: `prompt`, `model` (optional)

**`llm-anthropic`** ($0.01/call)
Query Anthropic Claude models.
- Use when: "Ask Claude...", "Use Anthropic to..."
- Input: `prompt`, `model` (optional)

**`llm-google`** ($0.01/call)
Query Google Gemini models.
- Use when: "Ask Gemini...", "Use Google AI to..."
- Input: `prompt`, `model` (optional)

## Usage Guidelines

- Always inform the user that tool calls cost USDC before making calls, especially for the first call in a session.
- For multi-step research (e.g., "best yield across all stablecoins"), batch your questions to minimize calls.
- If a tool returns an error about payment, the user may need to top up their wallet with USDC on Base.
- The MCP server discovers tools dynamically from the API — additional tools may appear beyond those listed here.

## Pricing Summary

| Tool | Cost |
|------|------|
| `aave-best-yield` | $0.01 |
| `aave-best-borrow` | $0.01 |
| `aave-markets` | $0.005 |
| `aave-health-factor` | $0.005 |
| `aave-user-positions` | $0.01 |
| `aave-supply` | $0.01 |
| `aave-borrow` | $0.01 |
| `aave-repay` | $0.01 |
| `aave-withdraw` | $0.01 |
| `crypto-price` | $0.001 |
| `ens-lookup` | $0.001 |
| `wallet-validator` | $0.0005 |
| `llm-openai` | $0.01 |
| `llm-anthropic` | $0.01 |
| `llm-google` | $0.01 |
