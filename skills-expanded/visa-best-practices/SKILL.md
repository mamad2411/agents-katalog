---
name: visa-best-practices
description: >
  Best practices and integration guide for Visa developer APIs and payment protocols — covers 
  platform setup, authentication, encryption, and product-specific workflows.
  Trigger keywords: VDP, Visa Developer Platform, VIC, Visa Intelligent Commerce, MPP,
  Machine Payments Protocol, X-Pay Token, Two-Way SSL, Mutual TLS, MLE, JWE,
  MCP integration, HTTP 402, network tokens, Visa Developer, Visa MLE.
---

# Visa Developer Platform Integration Guide

## Routing — What Are You Working On?

| If the user is asking about... | Read this reference |
|--------------------------------|---------------------|
| Authentication (X-Pay Token, Two-Way SSL, Mutual TLS) | [references/vdp-integration.md](references/vdp-integration.md) |
| Message Level Encryption (MLE/JWE) | [references/vdp-integration.md](references/vdp-integration.md) |
| Environment URLs (Sandbox, Cert, Production) | [references/vdp-integration.md](references/vdp-integration.md) |
| Credential management & certificate rotation | [references/vdp-integration.md](references/vdp-integration.md) |
| Code examples & starter kit (llms.txt) | [references/vdp-integration.md](references/vdp-integration.md) |
| VIC workflows (card enrollment, purchase instructions) | [references/visa-intelligent-commerce.md](references/visa-intelligent-commerce.md) |
| VIC payment credentials & agent commerce | [references/visa-intelligent-commerce.md](references/visa-intelligent-commerce.md) |
| MPP card charge (HTTP 402, network tokens) | [references/machine-payments-protocol.md](references/machine-payments-protocol.md) |
| MPP Client/Server Enablers | [references/machine-payments-protocol.md](references/machine-payments-protocol.md) |

## Quick Decision: Which Auth Method?

- **X-Pay Token** — Use for most integrations. Simpler setup, HMAC-based.
- **Two-Way SSL (Mutual TLS)** — Use when required by specific APIs or for higher-security environments.

Both are documented in [references/vdp-integration.md](references/vdp-integration.md).

## Quick Decision: MCP vs Direct API?

- **MCP-based** — Building an AI agent or LLM-powered application? Use MCP (StreamableHTTP transport).
- **Direct REST API** — Traditional backend service? Use direct API calls with X-Pay auth + MLE.

## Official Documentation Entry Points

| Resource | URL |
|----------|-----|
| Developer Center | https://developer.visa.com |
| VIC Capabilities | https://developer.visa.com/capabilities/visa-intelligent-commerce |

For all documentation links (auth guides, MLE guide, quick start), see [references/vdp-integration.md](references/vdp-integration.md).

## Product-Specific Guides

### Visa Intelligent Commerce (VIC)

For VIC integration (card enrollment, purchase instructions, payment credentials, agent commerce workflows), see:

**[references/visa-intelligent-commerce.md](references/visa-intelligent-commerce.md)**

### Machine Payments Protocol (MPP)

For MPP card charge integration (HTTP 402 payment challenges, encrypted network token credentials, Client Enabler interface, receipts), see:

**[references/machine-payments-protocol.md](references/machine-payments-protocol.md)**
