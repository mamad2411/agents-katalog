---
name: secrets-handling
description: >
  Use when working with API keys, credentials, tokens, certificates, or any sensitive
  configuration. This skill provides procedures for securely handling secrets throughout
  their lifecycle - from identification to storage, usage, rotation, and revocation.
---

# Secrets Handling

## Overview
This skill defines how to handle secrets (API keys, passwords, tokens, certificates, credentials) when they appear in work products, configurations, or communications. Improper secrets handling is a critical security risk that can compromise systems and data. Treat ALL secrets as sensitive.

## When to Use
- When configuring any service that requires authentication
- When working with environment variables or configuration files
- When creating documentation that references secure systems
- When integrating with external APIs or services
- When reviewing code or configuration that may contain secrets
- When setting up CI/CD pipelines with deployment credentials
- **Don't use when:** Working only with public, non-sensitive information

## Core Procedures

### Step 1: Identify Secrets
Recognize these as secrets requiring special handling:
- API keys and access tokens
- Database connection strings with credentials
- Passwords, passphrases, and PINs
- SSL/TLS certificates and private keys
- OAuth client secrets and refresh tokens
- SSH keys and deployment credentials
- Webhook secrets and signing keys
- Encryption keys and initialization vectors
- Personal identifiable information (PII)
- Financial data, account numbers

### Step 2: Secret Classification
Classify each secret by sensitivity:

| Level | Description | Examples |
|-------|-------------|---------|
| CRITICAL | Full system access, production data | Prod DB passwords, root keys |
| HIGH | Service-level access, staging systems | API keys, staging credentials |
| MEDIUM | Limited scope, non-critical systems | Test tokens, sandbox keys |
| LOW | Public or near-public information | API documentation, public certs |

### Step 3: Secure Usage

#### NEVER DO:
- Hardcode secrets in source code, configuration files, or documentation
- Pass secrets in URLs or query parameters
- Log secrets to console, log files, or monitoring systems
- Share secrets in plain text communications
- Store secrets in environment files committed to repositories
- Include secrets in handoff packages or deliverables

#### ALWAYS DO:
- Use secret management systems (env vars from secure vaults)
- Reference secrets by identifier, not by value
- Use placeholders in documentation: `[API_KEY]` or `${SECRET_NAME}`
- Access secrets through established secure channels only
- Rotate secrets regularly and after any potential exposure

### Step 4: Document Secrets Safely
When documentation must reference secrets:
```
# Configuration
DATABASE_URL=postgresql://user:${DB_PASSWORD}@host:5432/db
API_KEY=${MY_SERVICE_API_KEY}

# Setup (do NOT include actual values)
Required secrets:
- DB_PASSWORD: PostgreSQL database password (from vault: db/prod/password)
- MY_SERVICE_API_KEY: API key from MyService dashboard (from vault: integrations/myservice/key)
```

### Step 5: Secret Detection in Deliverables
Before delivering any work:
- [ ] Scan all files for patterns matching: `password`, `secret`, `key`, `token`, `credential`
- [ ] Check for common secret formats: base64 strings, hex strings, connection strings
- [ ] Verify no test fixtures contain real credentials (use mock values only)
- [ ] Confirm documentation uses placeholders, not actual values
- [ ] Run secrets detection tools if available

### Step 6: Exposure Response
If you discover exposed secrets:
1. **IMMEDIATELY** flag the exposure and identify the affected secret(s)
2. Notify the security team (Guardian, Sentinel, Gatekeeper) or company CEO
3. Do NOT share the exposed secret further
4. Document the incident (what, where, when) for security team investigation
5. Recommend secret rotation be performed immediately

## Quality Checklist
- [ ] No secrets present in source code, documentation, or deliverables
- [ ] All secret references use secure vault or environment variable patterns
- [ ] Documentation uses placeholders with setup instructions
- [ ] Secret classification is documented if applicable
- [ ] Secret detection scan was performed on all files
- [ ] Any discovered exposures are flagged and reported

## Error Handling
- **Error:** Secret accidentally exposed in communication
  **Response:** IMMEDIATELY revoke and rotate the secret, notify security team
- **Error:** Work requires a secret you don't have access to
  **Response:** Request secret through proper channel (security/infrastructure team), never ask another agent for it
- **Error:** Found hardcoded secret in existing codebase
  **Response:** Flag as security issue, fix with proper secret management, report to security agent
- **Error:** Secret has expired or is invalid
  **Response:** Request renewal through proper channel, document expiration for monitoring

## Cross-Team Integration
**Related Skills:** data-privacy-check, threat-modeling, audit-trail-management, incident-response
**Used By:** ALL agents (especially backend engineers, infrastructure, database, integrators)