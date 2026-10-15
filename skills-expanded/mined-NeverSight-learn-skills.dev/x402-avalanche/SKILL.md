---
name: x402-avalanche
description: Implement and operate HTTP 402 payments with x402 on Avalanche (Fuji/Mainnet), including facilitator integration, X-PAYMENT/X-PAYMENT-RESPONSE headers, EIP-712/EIP-3009 security, and flows for APIs or AI agents. Use it when the user mentions x402, "Payment Required", micropayments, USDC on Avalanche, "facilitator", "X-PAYMENT", "AI agents paying for APIs", or wants to monetize endpoints with pay-per-use.
---

# x402 on Avalanche

## Skill objective
This skill guides any developer to implement `pay-per-use` payments with `x402` using `HTTP 402 Payment Required` and on-chain settlement on Avalanche, focusing on fast and secure integration.

## When to activate it
Activate this skill if the task includes any of these cases:
- Protect HTTP endpoints with per-request payment.
- Implement `X-PAYMENT` and automatic client retries.
- Monetize APIs with `USDC` on `avalanche-fuji` or `avalanche-c-chain`.
- Choose or configure a `facilitator` (Thirdweb, PayAI, Ultravioleta, x402-rs).
- Design autonomous payments for AI agents.

## Recommended workflow

### 1) Define payment model
1. Choose scheme:
   - `exact`: fixed amount per request (recommended to start).
   - `upto`: maximum amount and variable charge based on actual usage (useful for LLM/token pricing).
2. Define price in token base units (USDC = 6 decimals).
3. Define target network:
   - Development: `avalanche-fuji`
   - Production: `avalanche-c-chain`

If you need pricing examples and AI/content/API use cases, read `references/use-cases-and-economics.md`.

### 2) Prepare network and wallet
1. Configure RPC and USDC contract addresses.
2. Fund test wallet with USDC from faucet (Fuji).
3. Configure project environment variables (RPC, receiving wallet, facilitator credentials).

For exact network parameters, addresses, and setup checklist, read `references/network-and-setup.md`.

### 3) Integrate protected endpoint (server)
1. In the endpoint:
   - If no valid payment, respond `402` with `accepts[]`.
   - If valid payment, settle and respond `200` with the resource.
2. Maintain consistency in:
   - `resource`, `network`, `asset`, `payTo`, `maxAmountRequired`.
3. Include `X-PAYMENT-RESPONSE` when confirming settlement.

For exact structure of `402`, `X-PAYMENT`, and `X-PAYMENT-RESPONSE`, read `references/protocol-and-headers.md`.

### 4) Implement paying client
1. Make normal request.
2. If you receive `402`, select option from `accepts`.
3. Generate `EIP-3009` authorization and `EIP-712` signature.
4. Retry request with `X-PAYMENT` (base64 JSON).
5. Process `X-PAYMENT-RESPONSE` and save transaction hash.

If you need cryptographic details and signature fields, read `references/security-and-settlement.md`.

### 5) Choose facilitator
Select based on priority:
- **Thirdweb**: enterprise stack and mature SDKs.
- **PayAI**: AI/agent-first cases.
- **Ultravioleta DAO**: gasless approach and decentralized governance.
- **x402-rs**: self-hosted, high performance in Rust.

For decision matrix and integration by provider, read `references/facilitators.md`.

### 6) Security and mandatory validations
Always validate:
- EIP-712 signature.
- Unique nonce (anti-replay).
- Time window (`validAfter`/`validBefore`).
- Correct `network`.
- Correct `asset`.
- Expected `payTo`.
- Minimum required amount.

Also, store `txHash`/receipt for idempotency and auditing.

Complete checklist and hardening patterns in `references/security-and-settlement.md`.

### 7) End-to-end testing
1. Request without payment -> should return `402`.
2. Request with valid `X-PAYMENT` -> should return `200`.
3. Verify tx on-chain in facilitator explorer/dashboard.
4. Simulate failures:
   - invalid signature
   - repeated nonce
   - expired authorization
   - insufficient amount
5. Confirm that the server responds with clear error and allows correct retry.

### 8) Extension to AI agents
1. Use agent wallet separate from main wallet.
2. Define budget and limits.
3. Apply `exact` for fixed calls or `upto` for variable costs by tokens.
4. Implement remaining balance withdrawal and risk controls.

AI patterns guide in `references/ai-agent-patterns.md`.

## Operational conventions
- Always use amounts as strings in token base units.
- Don't rely only on facilitator webhooks: verify on-chain.
- Avoid session logic for payment; favor stateless/idempotent flow.
- Test first on Fuji and then promote to C-Chain.

## Skill references
- `references/network-and-setup.md`: Avalanche configuration, wallets, faucets, env.
- `references/protocol-and-headers.md`: x402 protocol HTTP contract.
- `references/facilitators.md`: comparison and selection guide.
- `references/security-and-settlement.md`: EIP-712/EIP-3009 security and settlement.
- `references/ai-agent-patterns.md`: autonomous agent patterns and token-based chat.
- `references/use-cases-and-economics.md`: business context, traditional friction, and micropayment viability.
