---
name: sast-patterns
description: Static Application Security Testing patterns, OWASP Top 10 checklist, language-specific vulnerability patterns, Semgrep rule writing guide, and CI/CD integration. Grok-native with Production Contract, hooks, compound, palace.
when-to-use: When scanning code for security vulnerabilities, writing custom SAST rules, setting up CI/CD security gates, or before production deploy. Use with security-reviewer agent.
---

# SAST Patterns Skill (Grok Port)

Reusable patterns for static security analysis. Focus on high-signal OWASP, common vulns, and Grok integration for preflight/compound.

## Core Patterns (Condensed from OWASP Top 10 + common)

### A01 Broken Access Control
- Missing authz on endpoints.
- IDOR without ownership.
- Detect: endpoints without middleware checks.

### A03 Injection
- SQL: string concat vs parameterized.
- Command: unsanitized exec.
- Detect: user input to sinks without sanitizers.

### A02/A07 Crypto & Auth Failures
- Hardcoded secrets.
- Weak hashes (MD5).
- Plaintext creds.
- Detect: regex for keys/passwords, no MFA patterns.

### A05 Misconfig
- Debug in prod.
- Missing headers (helmet, etc.).
- Verbose errors.

**Semgrep quick:**
```yaml
rules:
- id: sql-injection
  pattern: $DB.query("..." + $INPUT)
  message: "Potential SQLi"
  severity: ERROR
```

## Grok Integration (Production Contract)
- Use with security-reviewer / compliance-expert agents.
- Fire on_compliance_check / on_security_audit hooks.
- Pre-Flight: run sast before heavy changes or deploys.
- Ledger for security findings in audits.
- Handoff: include severity, exploit path, fix + test.
- Friction: record vulns found → compound for better patterns or linter rules.
- Palace: store recurring vuln decisions (e.g. "always use prepared stmts").
- Compound: promote good sast rules to skills or agent prompts.
- Claim-verif: always read_file before claiming "no vuln".

## When to Activate
- In preflight for security-relevant tasks.
- After code changes (pair with linter_friction).
- In swarm Phase 3 review.
- Before release (shipper + verifier).

## Resources (Grok)
- Semgrep p/owasp-top-ten, p/secrets.
- Integrate with tldr for large code scans.
- See security-review skill, preflight, compound-learnings.

Prioritize executable guards over exhaustive lists. SAST is signal, not proof — always manual verify + test.
