---
name: solana-token-verification
description: "Use this skill when you need to verify Solana token contracts for security. User cases: checking Solana token legitimacy, scanning for rug pulls, detecting hidden taxes, assessing liquidity risks, analysing holder distribution, evaluating tokens before investment, or gate-checking Solana tokens in automated pipelines."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# Solana Token Verification

Verify Solana token contracts for security risks via Cybercentry ACP with Rust Scan AI detection.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> solana-token-verification --requirements '{"contract_address": "..."}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `contract_address` | String | Plain | Yes | Solana contract address (e.g., `Gx5dX1pM5aCQn8wtXEmEHSUia3W57Jq7qdu7kKsHvirt`) |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `scan_url` | String | Plain | Scan URL |

## Gotchas

- Solana addresses are base58-encoded, not hex - do not add `0x` prefix
- Address is typically 32-44 characters long
