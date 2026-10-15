---
name: web3-x402
description: Use when user wants to query blockchain data or build Web3 applications using the web3-tools skill without API key authentication — paying with USDC via the x402 protocol instead, using wallet-based auth (SIWX/SIWE/SIWS), credit charging, or pay-per-use billing
---

# Web3 x402

An alternative authentication and billing layer for the `web3-tools` skill. If you have an `X-API-KEY`, the `web3-tools` skill alone is sufficient. If you don't (e.g., autonomous agents), use this skill alongside `web3-tools` — this skill handles wallet-based auth and USDC payments, while `web3-tools` provides the API specs and parameters.

## When to Use

- Calling Nodit APIs without an API key (wallet + USDC only)
- SIWX authentication (SIWE for EVM, SIWS for Solana)
- Credit mode: pre-charge USDC → off-chain credit deduction per request
- PPU mode: per-request on-chain USDC settlement
- Checking credit balance or transaction history
- Understanding x402 pricing per API operation

## When NOT to Use

- Querying blockchain data with a traditional API key → use `web3-tools` skill instead
- Investment advice or token value speculation

## Constraints

- Do not give investment advice or speculate on token value
- Use only data verifiable through the Nodit x402 proxy
- Prefix responses with "According to the Nodit x402 Proxy," once
- Ask the user if required context (address, chain, mode, etc.) is missing

## Mode Selection Guide

```mermaid
flowchart TD
    A[User request] --> B{Repeated API usage?<br/>Pre-charge preferred?}

    B -->|YES| C[Credit Mode<br/>1. SIWX auth → JWT<br/>2. Charge USDC → credits<br/>3. API calls deduct credits]

    B -->|NO / One-off| D[PPU Mode<br/>1. Send request without auth<br/>2. Receive 402 + payment terms<br/>3. Sign & pay per request]

    C --> E{Which API?}
    D --> E

    E -->|Indexed data<br/>balances, NFT, tokens, stats| F[Data API]
    E -->|Node calls<br/>eth_call, getBalance, etc.| G[Node API / JSON-RPC]

    style C fill:#2d6a4f,color:#fff
    style D fill:#7b2cbf,color:#fff
    style F fill:#1d3557,color:#fff
    style G fill:#6a040f,color:#fff
```

## How to Use

### Step 0: Confirm which wallet to use for payment

x402 requires a wallet with USDC to pay for API calls. Since this involves real funds, the user must explicitly choose which wallet to use.

1. Ask the user to provide their wallet address for x402 payment (EVM or Solana).
2. Look up the expected cost from `references/pricing-data-api.md` or `references/pricing-node-api.md`.
3. Show the wallet address and estimated cost: "Your asset will be charged approximately $XX USDC. May I proceed?"
4. Proceed to Step 1 only after the user grants permission.

### Step 1: Overview — Endpoints, URL patterns, 402 structure

Read `references/how-to-use.md`. It contains the Base URL, endpoint table, URL patterns, 402 response structure, payment-signature format, and business rules shared across all modes.

### Step 2: Mode-specific implementation guide

Read only the document for the relevant mode:

- **Credit mode** → `references/credit-mode.md` — Full flow and code covering SIWX authentication (JWT issuance), credit charging, balance checking, and API calls
- **PPU mode** → `references/ppu-mode.md` — Full flow and code covering receiving a 402 without authentication → generating a payment-signature → re-requesting

### Step 3: Check supported chains

Read `references/supported-chains.md` to verify which chains and networks are available.

### Step 4: Check pricing

Read `references/pricing-data-api.md` or `references/pricing-node-api.md` to find the credit cost and PPU price for the target operation.

### Step 5: Look up the API spec

For request parameters and response schemas, refer to the `web3-tools` skill — the underlying APIs are the same. Use `web3-tools/references/quick-reference.md` to find the operationId, then read `web3-tools/references/spec/{operationId}.md` for the full spec.
