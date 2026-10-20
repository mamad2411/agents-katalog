---
name: sui-onchain-agent-payment-gateway
description: Applies Sui's September 2026 on-chain agent payment infrastructure — scoped spend accounts with delegate keys, per-payment caps, expirations, and RefundVault recovery, settling in USDC before the upstream service call with MPP and x402 compatibility and MCP-sponsored gas — to design secure autonomous machine-to-machine payment infrastructure. Use when building on-chain agent payment gateways, designing scoped delegate-key spend models, or benchmarking chain-level agent-payment architectures (Sui vs Solana vs Base). NOT for testnet deployment readiness claims or for fiat settlement flows.
---

# Sui On-Chain Agent Payment Gateway

## Overview
Sui's September 2026 launch of on-chain payment infrastructure for autonomous machine-to-machine commerce — agents **discover, pay for, and access APIs without manual approval or API keys**, with settlement in USDC **on-chain before the upstream service call is executed**, ensuring verified on-chain payment. Uses an on-chain spend account model with scoped delegate keys.

## When to Use
- Building on-chain agent payment gateways with strict budget limits and verified settlement
- Designing scoped delegate-key risk management for agent wallets (compromised key cannot drain the wallet)
- Benchmarking chain-level agent-payment infrastructure across Sui/Solana/Base
- Structuring refundable agent transactions for failed service delivery
- NOT as mainnet production-readiness evidence (currently Sui testnet, USDC settlement, mainnet pending hardening)
- NOT for fiat or card-network settlement (out of scope)

## Core Process / Workflow
1. **Grant scoped on-chain access**: owners grant agents scoped access to specific assets and services — grants define **allowed services, total budgets, per-payment caps, and expiration dates, all enforced on-chain at settlement**.
2. **Settle on-chain before the service call**: payment finalization via digest visible on Suiscan; only then is the upstream service call executed — settlement-before-delivery as the atomicity pattern.
3. **Support both MPP and x402** standards for compatibility with emerging machine payment protocols.
4. **Eliminate hidden fees via MCP-sponsored gas**: sponsored gas through the MCP ensures the agent's cost remains exactly equal to the service price.
5. **Bound the blast radius with scoped delegate keys**: the agent acts only as a delegated signer on the owner's spend account — a compromised key cannot drain the entire wallet, only the pre-defined grant permissions.
6. **Recover funds via RefundVault**: if service delivery fails within a specified decision window, the agent can reclaim funds from the vault before they release to the seller.
7. **Verify settlement on Suiscan** (the digest-visible explorer).

## Key Evidence
- Settlement occurs **on-chain before the upstream service call** — the atomicity guarantee is the architectural differentiator vs HTTP-402-then-settle patterns.
- Scoped delegate keys are the risk-management layer: **compromised key = limited grant permissions, not full wallet drain**.
- RefundVault = refundable offers with a decision window — the refund path missing from most per-request payment rails.
- Currently **Sui testnet with USDC settlement; mainnet pending further transaction-path hardening** — deployability caveat is load-bearing.
- Strategic position: Sui's object-centric data model + Mysticeti upgrade (390ms consensus latency) positions it for high-throughput, low-latency agent payments — distinct from Solana's PoH clock-based approach.

## Pairs with
`app-onchain-agent-payments` (new this run — the commercial-relationship protocol), `agentic-payment-protocol-convergence-2026`, `x402-production-checklist`, `agent-pay-card-network-integration`, `agent-settlement-protocol-asp-2026`, `erc8004-empirical-trust-reality-check-2026`

## A-Tech Alignment
- **Open source**: chain-level open infrastructure; MCP/x402 protocol composability is open-standard alignment.
- **Data privacy**: scoped delegate keys = the programmable-consent surface; a compromised agent key cannot reach the whole wallet — structural blast-radius containment.
- **Financial freedom**: sub-cent settlement + exact-cost MCP-sponsored gas = no hidden fees for the solo builder's agent fleet.
- **Practical**: the grant-parameters checklist (allowed services / total budget / per-payment cap / expiration) is the deployable scope template.

*Source: ainvest news, Sept 1, 2026 (Sui testnet launch announcement).*