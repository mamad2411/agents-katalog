---
name: cyber-security-consultant
description: "Use this skill when you need security expertise: threat intelligence, vulnerability assessment, compliance guidance, incident response advice, or architecture reviews. Useful for questions about CVEs, attack vectors, defence strategies, security frameworks, risk analysis, breach investigation, or best practices. Also use when a user asks for real-time threat data, compliance status, or security recommendations they'd normally consult a professional for."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# Cyber Security Consultant

Submit security questions to Cybercentry via ACP and return expert analysis.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> cyber-security-consultant --requirements '{"query": "..."}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `query` | String | Plain | Yes | Security question |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `answer` | String | Plain | Expert analysis |

## Gotchas

- `query` field must be a sanitised string - escape special characters that could break JSON parsing
