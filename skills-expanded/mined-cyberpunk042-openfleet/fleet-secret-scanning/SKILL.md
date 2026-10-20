---
name: fleet-secret-scanning
description: How DevSecOps scans for leaked credentials and secrets — patterns to detect, git history scanning, response protocol. Maps to sec_secret_scan group call and secret-detector sub-agent.
---

# Secret Scanning — DevSecOps Credential Detection

A single leaked API key can compromise an entire system. Your job is to find exposed credentials BEFORE they reach production — in code, config, commit history, and environment files.

## What to Scan For

| Pattern | Example | Risk |
|---------|---------|------|
| API keys | `AKIAIOSFODNN7EXAMPLE` (AWS), `sk-...` (OpenAI) | Service compromise |
| Tokens | `ghp_...` (GitHub PAT), `xoxb-...` (Slack) | Account takeover |
| Passwords | `password = "hunter2"`, connection strings with creds | Database/service access |
| Private keys | `-----BEGIN RSA PRIVATE KEY-----` | Identity theft |
| Connection strings | `postgresql://user:pass@host/db` | Database access |
| JWT secrets | `JWT_SECRET=mysecretkey` | Token forgery |

## Scanning Tools

### secret-detector sub-agent
```
Agent: secret-detector
Prompt: "Scan fleet/infra/ and config/ for exposed credentials, 
        API keys, tokens, and secret patterns. Check .env.example 
        for real values that shouldn't be there."
```

### semgrep MCP (pattern-based)
Semgrep has rules for secret detection across 30+ languages.

### Git history scanning
Secrets removed from HEAD may still exist in git history:
```bash
git log --all -p | grep -i "password\|secret\|token\|api_key\|private_key"
```

## Your sec_secret_scan Group Call

`sec_secret_scan()` prepares the scanning context:
1. Identifies files likely to contain secrets (.env, config/*, credentials/*)
2. Checks .gitignore coverage for sensitive files
3. Reports findings with specific file:line references

## Response Protocol

When a secret is found:

### In Code (not yet committed)
1. Remove the secret
2. Move to .env (gitignored) or secrets manager
3. Verify .gitignore covers the sensitive file

### In Git History
1. **CRITICAL** — the secret is exposed even if removed from HEAD
2. Rotate the credential immediately (new key, revoke old)
3. Post: `fleet_alert(severity="critical", category="security", details="Exposed {type} in git history")`
4. Create task to clean history if needed (git filter-branch or BFG)

### In .env.example
1. Replace real values with placeholders: `API_KEY=your-api-key-here`
2. Verify .env (with real values) is gitignored

## CRON Integration

Your **secret-scan** CRON runs weekly:
1. Scan all project files for secret patterns
2. Check .gitignore coverage
3. Report findings to board memory [security, secrets]
4. For any match: alert + investigation

## False Positives

Not every match is a real secret:
- Documentation mentioning "set your API_KEY to..." → false positive
- Test fixtures with fake values → false positive (verify they're fake)
- Base64-encoded data that looks like keys → check context

When in doubt, treat it as real until verified otherwise. The cost of a false negative (missed real secret) is much higher than the cost of a false positive (investigated harmless string).
