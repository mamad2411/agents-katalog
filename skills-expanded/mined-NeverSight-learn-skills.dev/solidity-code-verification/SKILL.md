---
name: solidity-code-verification
description: "Use this skill when you need security analysis of Solidity smart contract code. User cases: auditing Solidity contracts, identifying re-entrancy bugs, detecting access control issues, reviewing unsafe external calls, evaluating code before deployment, gate-checking contracts in transaction pipelines, or performing security assessments."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# Solidity Code Verification

Analyse Solidity code for vulnerabilities via Cybercentry ACP. Returns High/Medium/Low/Informational risk level.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> solidity-code-verification --requirements '{"solidity_code": "..."}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `solidity_code` | String | Plain | Yes | Solidity source code to analyse |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `job_id` | String | Plain | Job ID |
| `overall_risk` | String | Plain | Risk level (Informational, Low, Medium, or High) |

## Gotchas

- Escape double quotes and newlines in Solidity code for valid JSON
- For multi-file contracts, concatenate all files into a single string
- Execution time typically < 2 minutes but can take up to 5 minutes
