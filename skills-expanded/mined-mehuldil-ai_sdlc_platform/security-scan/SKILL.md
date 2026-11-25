---
name: security-scan
description: Full security pass (deps, AppSec, stability) — for secrets-only use shared/secrets-detector first
model: sonnet-4-6
token_budget: {input: 8000, output: 4000}
---

# Security Scan Skill

Comprehensive security validation covering secrets detection, vulnerability scanning, and crash prevention.

**Shared reference:** [security-scan-dimensions-reference.md](../shared/security-scan-dimensions-reference.md) — atomic split with `secrets-detector` and unified P0–P3 rubric.

## Security Dimensions

### 1. Secrets & Credential Detection
- API keys, tokens, passwords
- Database credentials, connection strings
- Private keys and certificates
- Sensitive environment variables
- Tools: TruffleHog, git-secrets

### 2. Data Protection & Compliance
- HTTPS enforcement (all APIs)
- Encryption at rest
- PII handling (GDPR compliance)
- Secure storage (Keychain, Keystore)
- Token management and logout on expiry

### 3. Dependency Vulnerabilities (OWASP Top 10)
- npm audit findings
- Critical/High/Moderate/Low severity
- Available patches
- Abandoned packages (2+ year old)

### 4. Application Security Audit (9 Categories)
1. Authentication (OAuth2, JWT, MFA)
2. Authorization (Role-based, isolation)
3. Data Protection (Encryption, PII, GDPR)
4. Communication (TLS/SSL, cert pinning)
5. Storage (Keychain, Keystore, encryption)
6. Input Validation (XSS, injection prevention)
7. Cryptography (Strong algorithms, key mgmt)
8. Third-Party (SDK security, compliance)
9. Deployment (Code signing, anti-tampering)

### 5. Crash Prevention & Stability
- Null/Undefined safety
- Async issues (race conditions, unhandled promises)
- Error handling (missing try-catch)
- Resource leaks (memory, listeners)
- Type mismatches (runtime errors)
- Edge cases (boundaries, empty arrays)

## Scanning Process

1. **Secrets Detection**: Scan patterns, git history
2. **Data Protection Review**: HTTPS, encryption, PII, storage, tokens
3. **Dependency Audit**: npm audit, security check
4. **Input Validation Check**: XSS, injection, sanitization
5. **Crash Risk Analysis**: Null/undefined, async, errors, resources
6. **Full AppSec Audit**: All 9 categories

## Vulnerability Analysis Tools

- TruffleHog, git-secrets (credential detection)
- TypeScript strict mode
- ESLint security plugins
- Semgrep rules
- OWASP Mobile Top 10 checklist
- MobSF (Mobile Security Framework)
- Burp Suite (proxy analysis)

## Security Scan Report

Documents:
- Secrets Detection (status, findings)
- Data Protection (HTTPS, encryption, PII, storage, tokens)
- Vulnerability Scan (critical, high, moderate, low counts)
- Crash Risk Analysis (by category)
- AppSec Audit (9 categories status)
- Issues Found (by severity)
- Security Decision (APPROVE/WARN/BLOCK)

## Guardrails

- Fail: Exposed secrets (P0)
- Fail: Memory leaks/crash patterns
- Fail: Critical vulnerabilities
- Flag: Unencrypted storage (P1)
- Warn: Unvalidated inputs (P2)
- Require: Dependency security updates
- Null Safety: All optionals handled
- Async: All promises tracked
- Errors: Try-catch around risky ops
- Resources: Proper cleanup

## Triggers

Use when:
- PR security validation required
- Before code review
- Before release
- Suspicious code pattern detected
- Dependency update needed

---
