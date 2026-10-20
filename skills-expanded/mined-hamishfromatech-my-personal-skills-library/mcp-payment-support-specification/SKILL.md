---
name: mcp-payment-support-specification
description: Implements the SEP-2007 MCP Payment Support specification for standardized, protocol-level payment of MCP tool invocations. Use when building paid MCP servers, designing agent-to-agent payment flows, monetizing open-source AI tools via MCP, or implementing X402/Stripe payment integration for AI agents.
---

# MCP Payment Support Specification (SEP-2007)

## Overview

SEP-2007 adds a standardized payment framework to the Model Context Protocol (MCP), enabling MCP servers to charge for tool invocations. The specification defines a protocol-agnostic framework supporting multiple payment methods (X402 for blockchain/on-chain, Stripe for fiat, and a metered mode for usage tracking without real-time payment).

This skill implements the specification for A-Tech's open-source, privacy-first AI tools. It enables direct monetization of MCP servers — the protocol layer where A-Coder, Be Practical, and Builder's Club tools can generate revenue without compromising user privacy or data sovereignty.

## Why This Matters for A-Tech

- **Open-source AI**: The spec is open and protocol-agnostic; any MCP server can implement it
- **Data privacy**: Payment data is minimized and routed through payment providers, not stored by the MCP server
- **Financial freedom**: Enables direct agent-to-agent revenue streams and per-tool monetization
- **Practical implementation**: X402 (on-chain, USDC) and Stripe (fiat) examples are documented; backward-compatible with existing MCP implementations

## Core Specification

### 1. Capability Declaration

Servers that support payments MAY declare the `payment` capability during initialization:

```json
{
  "capabilities": {
    "payment": {
      "protocols": ["x402", "stripe", "metered"]
    }
  }
}
```

Declaring the capability is OPTIONAL. Servers MUST include payment information in tool definitions regardless of whether they declare the capability.

### 2. Tool-Based Payment Discovery

Payment information is included directly in tool definitions returned by `tools/list`. This provides:
- **Transparent pricing**: LLMs and clients see costs upfront for each tool
- **Per-tool pricing**: Different tools can have different payment requirements
- **Multiple payment options**: Each tool can accept multiple protocols
- **Intelligent decision-making**: LLMs can factor cost into tool selection

Example `tools/list` response:

```json
{
  "tools": [
    {
      "name": "get_premium_weather",
      "description": "Get detailed weather analysis ($0.01)",
      "inputSchema": {
        "type": "object",
        "properties": {
          "location": { "type": "string" }
        }
      },
      "payment": [
        {
          "protocol": "x402",
          "paymentRequired": {
            "scheme": "exact",
            "network": "eip155:84532",
            "amount": "10000",
            "asset": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
            "payTo": "0x209693Bc6afc0C5328bA36FaF03C514EF312287C",
            "maxTimeoutSeconds": 60,
            "extra": { "name": "USDC", "version": "2" }
          }
        }
      ]
    }
  ]
}
```

### 3. Payment Challenge Flow

When payment is required, servers MUST return error code `-32402` with protocol-specific payment information. The `-32402` response is the authoritative source of truth for pricing (supports dynamic pricing based on arguments).

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32402,
    "message": "Payment Required",
    "data": {
      "payment": [
        {
          "protocol": "x402",
          "paymentRequired": { /* same structure as tools/list */ }
        }
      ]
    }
  }
}
```

### 4. Payment Request Processing

Clients include payment authorization in the `payment` field when retrying the tool invocation:

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_premium_weather",
    "arguments": { "location": "New York" },
    "payment": {
      "protocol": "x402",
      "paymentInput": {
        "authorization": {
          "x402Version": 2,
          "resource": {
            "url": "mcp://tool/get_premium_weather",
            "description": "Premium weather data tool",
            "mimeType": "application/json"
          },
          "accepted": { /* payment terms */ },
          "payload": {
            "signature": "0x...",
            "authorization": { /* EIP-3009 auth */ }
          }
        }
      }
    }
  }
}
```

### 5. Payment Verification and Settlement

Servers MUST:
1. Parse payment authorization from the `payment` field
2. Verify via protocol-specific payment providers (X402 facilitator, Stripe API)
3. Execute the tool only after authorization is verified
4. Settle payment via payment provider
5. Return tool result with payment confirmation

Successful response:

```json
{
  "result": {
    "content": [{ "type": "text", "text": "The weather is 72°F." }],
    "isError": false,
    "payment": {
      "protocol": "x402",
      "paymentOutput": {
        "result": {
          "success": true,
          "transaction": "0x1234...",
          "network": "eip155:84532",
          "payer": "0x14cE..."
        }
      }
    }
  }
}
```

## Payment Protocols

### X402 (On-Chain, Recommended for Crypto)

- **Authorization flow**: Client signs authorization (not a completed payment); server settles via facilitator
- **Networks**: EVM (Ethereum, Base, Arbitrum) and Solana
- **Asset**: USDC recommended for price stability
- **Security**: Cryptographic signatures, time-limited challenges, facilitator mediation
- **Facilitator endpoints**: `/verify`, `/settle`, `/supported`

### Stripe (Fiat, Recommended for Enterprise)

```json
{
  "payment": [{
    "protocol": "stripe",
    "paymentRequired": {
      "amount": 500,
      "currency": "usd",
      "description": "Premium weather analysis",
      "paymentMethods": ["card", "us_bank_account"]
    }
  }]
}
```

Stripe uses a two-phase intent model (create intent → confirm with payment method). For sub-dollar payments, prepaid credit balances are recommended to avoid per-call Stripe fees.

### Metered (Usage Tracking Without Payment)

For servers that want usage tracking and budget enforcement before adding real-time payment collection. The `tools/list` payment field carries cost information for LLM visibility, but billing happens out of band (monthly invoice, prepaid balance, free tier).

## Security Requirements

- Use secure communication channels (HTTPS for HTTP transport)
- Integrate only with trusted, protocol-compliant payment providers
- Verify all payment authorizations through designated providers
- Maintain comprehensive audit logs of payment activities
- Protect user privacy: collect only necessary payment info, minimize local storage
- Use MCP-specific URI schemes: `mcp://tool/{tool_name}`, `mcp://resource/{resource_name}`

## Server-Side Production Patterns

From production deployments (438 paid tools, 132 providers):

1. **Escrow-before-call ordering**: Payment challenge must resolve BEFORE the upstream API call, not after. Pipeline: `AUTH → IDEMPOTENCY → SCHEMA → ESCROW → PROVIDER_CALL → ESCROW_FINALIZE → LEDGER_WRITE`
2. **Atomic escrow finalize + ledger write**: Run in a single database transaction to prevent revenue leaks and double-charging
3. **Orphaned escrow reconciliation**: 60-second loop auto-refunds orphaned holds; recommended `escrow_ttl` of 30–120s
4. **Cache hit billing**: Cached results skip escrow stages; use `cached: true` in receipt; may apply lower price tier
5. **Idempotency**: MUST for payment-enabled servers; retried requests with same key return cached result + original receipt

## Client Implementation

MCP clients SHOULD provide a payment hook interface:

```typescript
interface PaymentHooks {
  onPaymentRequested(toolName: string, paymentOptions: PaymentOption[]): Promise<PaymentSelection>;
  onPaymentError(toolName: string, protocol: string, error: unknown): Promise<void>;
  onPaymentSuccess(toolName: string, protocol: string, paymentResult: unknown): Promise<void>;
}
```

This allows client builders to integrate preferred payment methods without modifying the core MCP client.

## A-Tech Applications

### A-Coder (Developer Tool)
- **Premium tools**: Charge for advanced code analysis, security scanning, or AI-powered refactoring via X402 micro-payments (0.001–0.01 USDC per call)
- **Metered mode**: Track usage for free-tier limits; upgrade to paid via Stripe prepaid balance
- **Privacy-first**: On-premise MCP server; payment data never touches A-Tech infrastructure

### Be Practical (Learning Platform)
- **Pay-per-lesson**: MCP tools that generate personalized learning content; charge per lesson via Stripe
- **Premium playbooks**: Gated MCP tools for advanced frameworks; X402 for crypto-native learners

### Builder's Club (Community Marketplace)
- **Tool marketplace**: Community-built MCP tools with per-call pricing; A-Tech takes a revenue share
- **Reputation-based pricing**: Tools from verified contributors can charge premium rates
- **Open-source monetization**: Enables contributors to earn from their open-source MCP tools directly

## Current Status

- **SEP-2007**: Draft specification, closed June 2026 for dormancy (can be revived with sponsor support)
- **X402**: Mature, production-deployed (Coinbase Payments MCP, Giskard, 438+ paid tools in production)
- **Stripe integration**: Validated via production implementations (mcp-billing library)
- **MCP ecosystem**: 97M+ monthly SDK downloads; broad industry backing

## References

- SEP-2007 PR: https://github.com/modelcontextprotocol/modelcontextprotocol/pull/2007
- X402 Protocol Spec v2: https://github.com/coinbase/x402/blob/main/specs/x402-specification-v2.md
- Coinbase Payments MCP: https://docs.cdp.coinbase.com/x402/mcp-server
- mcp-billing (Stripe reference): https://pypi.org/project/mcp-billing/
- MCP Specification: https://modelcontextprotocol.io/specification/2025-11-25