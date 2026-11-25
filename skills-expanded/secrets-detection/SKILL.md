---
name: secrets-detection
description: Scans any codebase or repository for hardcoded secrets — API keys, tokens, passwords, private keys, database URLs, cloud credentials. Use whenever the user wants to check for exposed secrets before making a repo public, before a major commit/push, before deployment, or as part of any broader security audit.
---

# Secrets Detection — Exposed Credential Scanner

A specialized skill for finding any sensitive data hardcoded directly in source instead of environment variables.

## When to use this
- Before making a repository public
- Before any significant commit/push or deployment
- As part of a broader security audit (typically invoked from `code-audit`)

## Patterns to Search For

| Type | Example Patterns |
|---|---|
| Cloud keys | `AKIA[0-9A-Z]{16}` (AWS), GCP service-account JSON, Azure connection strings |
| Public API keys | Stripe (`sk_live_`), SendGrid, Twilio, OpenAI/Anthropic (`sk-`, `sk-ant-`) |
| Tokens | Real-looking JWTs hardcoded as examples, bearer tokens, GitHub PATs (`ghp_`) |
| Private keys | `-----BEGIN PRIVATE KEY-----`, accidentally committed `.pem`/`.key` files |
| Database credentials | Connection strings containing user/password (`postgres://user:pass@host`) |
| Generic passwords | Variables named `password =`, `secret =`, `apiKey =` with a hardcoded string value |

## Methodology
1. Search all source files (not just `.env` — values sometimes get copy-pasted into other files by mistake).
2. Also check configuration files (`config/*.json`, `docker-compose.yml`) and CI/CD pipeline files (`.github/workflows/*.yml`).
3. Check git history, not just the current working tree — a secret removed from current code but still present in a past commit remains fully exposed.
4. Never downgrade a finding to "low severity" just because it looks like a test value — assume the worst by default.

## On Finding a Secret
```
🔴 Exposed Secret Found
Type: [secret type]
Location: file:line
Severity: Critical (always)
Immediate Actions:
  1. Remove the value from code and move it to an environment variable
  2. Rotate this credential immediately from the relevant service's dashboard — if it was ever pushed to version control, treat it as compromised even if later deleted
  3. If the repo was public or exposed for any period, check that service's usage logs for suspicious activity
```

## Rules
- Never stop at just reporting the secret — always push the "rotate immediately" step, since deleting the code reference alone is not sufficient once a secret has touched version control, even briefly.
- Don't display the full secret value in the report if it's long; show only a few leading/trailing characters for identification (`sk-ant-***...***a1b2`) to avoid further exposure.
