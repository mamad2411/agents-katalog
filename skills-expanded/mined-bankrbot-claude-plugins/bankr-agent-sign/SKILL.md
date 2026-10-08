---
name: Bankr Agent - Sign & Submit API
description: This skill should be used when the user asks to "sign a message", "sign typed data", "sign a transaction", "submit a transaction", "submit raw transaction", "personal_sign", "EIP-712", "eth_signTypedData", "eth_signTransaction", or any direct signing or transaction submission operation. Covers the synchronous /agent/sign and /agent/submit endpoints.
version: 1.0.0
---

# Sign & Submit API

Synchronous endpoints for signing messages and submitting transactions directly — no polling required.

## Overview

| Endpoint | Purpose | Returns |
|----------|---------|---------|
| `POST /agent/sign` | Sign messages, typed data, or transactions | Signature |
| `POST /agent/submit` | Submit raw transactions to chain | Transaction hash |

Unlike `/agent/prompt` (async with job polling), these endpoints return immediately.

## POST /agent/sign

Sign data without broadcasting to the network.

### Signature Types

| Type | Use Case |
|------|----------|
| `personal_sign` | Sign plain text messages (auth, verification) |
| `eth_signTypedData_v4` | Sign EIP-712 typed data (permits, orders) |
| `eth_signTransaction` | Sign transactions for later broadcast |

### Prompt Examples

**Sign a message:**
- "Sign this message: Hello World"
- "Sign in to MyApp with nonce abc123"

**Sign typed data (EIP-712 permit):**
- "Sign this EIP-712 permit for USDC approval"

**Sign a transaction without broadcasting:**
- "Sign this transaction but don't send it"

### Success Response

```json
{
  "success": true,
  "signature": "0x...",
  "signer": "0xYourWalletAddress",
  "signatureType": "personal_sign"
}
```

### Common Errors

| Status | Error | Cause |
|--------|-------|-------|
| 400 | Missing required field | Missing message, typedData, or transaction |
| 401 | Authentication required | Missing or invalid API key |
| 403 | Read-only API key | Key lacks write permissions |

## POST /agent/submit

Submit raw transactions directly to the blockchain.

### Transaction Fields

| Field | Required | Description |
|-------|----------|-------------|
| `to` | Yes | Destination address |
| `chainId` | Yes | Chain ID (8453=Base, 1=Ethereum, 137=Polygon) |
| `value` | No | Value in wei (as string) |
| `data` | No | Calldata (hex string) |
| `gas` | No | Gas limit |
| `waitForConfirmation` | No | Wait for on-chain confirmation (default: true) |

### Prompt Examples

**Submit a raw transaction:**
- "Submit this transaction on Base: {to: 0x..., data: 0x..., value: 0}"

**Simple ETH transfer:**
- "Submit a transfer of 1 ETH to 0x..."

### Success Response

With confirmation:
```json
{
  "success": true,
  "transactionHash": "0x...",
  "status": "success",
  "blockNumber": "12345678",
  "gasUsed": "21000",
  "signer": "0xYourWalletAddress",
  "chainId": 8453
}
```

### Transaction Status Values

| Status | Description |
|--------|-------------|
| `success` | Confirmed and succeeded |
| `reverted` | Confirmed but reverted |
| `pending` | Submitted, not yet confirmed |

## Use Cases

- **Authentication**: Sign messages to verify wallet ownership
- **Gasless approvals**: Sign EIP-2612 permits without gas
- **Pre-built transactions**: Submit calldata from external tools
- **Multi-step workflows**: Execute approve + swap in sequence

## Comparison with /agent/prompt

| Feature | /agent/prompt | /agent/sign | /agent/submit |
|---------|---------------|-------------|---------------|
| Input | Natural language | Structured data | Transaction object |
| Response | Async (job ID) | Sync (signature) | Sync (tx hash) |
| Executes on-chain | Via AI agent | No | Yes |
| Best for | General queries | Auth, permits | Raw transactions |

## Security Notes

- `/agent/submit` executes immediately with **no confirmation prompt**
- Validate all transaction parameters before submission
- Use `waitForConfirmation: true` for important transactions
- Read-only API keys cannot use these endpoints (403)
