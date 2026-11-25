---
name: secrets-detector
description: Atomic skill — detect secrets, credentials, and sensitive strings in code and config (invoke before broader security-scan)
model: sonnet-4-6
token_budget: {input: 4000, output: 2000}
---

# Secrets Detector (Atomic)

**Single responsibility:** find exposed secrets and credential material.  
**Does not:** OWASP AppSec audit, dependency CVEs, crash analysis — use `security-scan` for the full pass.

## Scope

- API keys, tokens, passwords in source and env samples
- Private keys, certificates, connection strings
- High-entropy strings that match secret patterns
- Recommend: TruffleHog, git-secrets, repo policy

## Delegation

- `security-scan` (frontend/backend) should **start with or reference** this skill for the secrets slice to avoid duplicating detection logic in prompts.

## Output

- List of findings with file path, line, severity (P0 exposed secret → block)
- Remediation: rotate credential, move to vault/Keychain, remove from history
