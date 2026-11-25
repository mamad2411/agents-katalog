---
name: wallet-verification
description: "Use this skill when you need blockchain forensics for wallet addresses. User cases: investigating wallet funding sources, screening sanctions compliance, detecting money laundering patterns, identifying bot automation, assessing wallet trustworthiness, evaluating counterparty risk, or gate-checking wallets in automated systems."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# Wallet Verification

Blockchain forensics for wallet addresses via Cybercentry ACP. Traces funding chains across 30+ EVM chains.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> wallet-verification --requirements '{"wallet_address": "0x..."}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `wallet_address` | String | Plain | Yes | EVM wallet address with `0x` prefix |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `report` | String | Plain | Forensics report |

## Gotchas

- `wallet_address` must include the `0x` prefix for EVM addresses
