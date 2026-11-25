---
name: web-application-verification
description: "Use this skill when you need security scanning for websites or dApps. User cases: finding XSS vulnerabilities, identifying insecure APIs, assessing frontend security, evaluating web application vulnerabilities, securing dApp frontends, or performing OWASP compliance checks on web interfaces."
license: MIT
metadata:
  author: Cybercentry
  version: "1.0.0"
---

# Web Application Verification

OWASP security scanning for websites and dApps via Cybercentry ACP. Detects XSS, insecure APIs, and frontend vulnerabilities.

## Workflow

1. Install ACP CLI from https://github.com/Virtual-Protocol/openclaw-acp
2. Run `acp setup` (one-time only)
3. Run `acp browse "Cybercentry"` to find provider wallet
4. Run `acp job create <wallet> web-application-verification --requirements '{"target_url": "https://..."}'`
5. Poll `acp job status <jobId>` until `COMPLETED`

## Requirements Schema

| Parameter | Type | Format | Required | Description |
|-----------|------|--------|----------|-------------|
| `target_url` | String | Plain | Yes | Target URL including protocol (e.g., `https://example.com`) |

## Deliverables

| Field | Type | Format | Description |
|-------|------|--------|-------------|
| `report_url` | String | Plain | Security report URL |

## Gotchas

- `target_url` must include the protocol (`https://` or `http://`)
- URL must be publicly accessible for scanning
