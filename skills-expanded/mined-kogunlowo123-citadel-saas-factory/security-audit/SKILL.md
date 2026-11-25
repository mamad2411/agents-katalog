---
name: security-audit
description: Security audit for code and infrastructure. Auto-invoked on security-related keywords.
allowed-tools: [Read, Grep, Glob]
---

# Security Audit Skill

## When to Invoke
- Keywords: security, vulnerability, CVE, audit, pentest, secrets
- Before deployments to production
- After dependency updates

## Audit Scope
1. **Secrets** — Scan for hardcoded API keys, passwords, tokens
2. **Injection** — SQL injection, command injection, XSS
3. **Authentication** — JWT validation, session management, CSRF
4. **Authorization** — RBAC enforcement, tenant isolation
5. **Dependencies** — Known CVEs in packages
6. **Infrastructure** — Container security, network policies, TLS
7. **Compliance** — GDPR, SOC2, HIPAA requirements

## Tools
- Semgrep (SAST), Trivy (SCA/container), TruffleHog (secrets)
- Falco (runtime), Kyverno (policy), ZAP (DAST)
