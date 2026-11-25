---
name: private-data-verification
description: "Use this skill when you need Zero-Knowledge Proofs or data integrity validation. User cases: verifying identity claims without exposure, proving login status, creating trustless proof of action, validating sensitive data authenticity, privacy-preserving verification in Web3, or generating cryptographic proof receipts."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# Private Data Verification

Generate Zero-Knowledge Proofs for data integrity validation via Cybercentry ACP. Returns proof_id and proof_url.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> private-data-verification --requirements '{"cpdv_data": "..."}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `cpdv_data` | String | Plain | Yes | Private data for proof generation |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `proof_id` | String | Plain | ZKP verification ID |
| `proof_url` | String | Plain | ZKP verification URL |

## Gotchas

- `cpdv_data` must be a plain string - escape special characters that could break JSON parsing
