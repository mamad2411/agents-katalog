---
name: security-auditor
description: Audit software architectures, source code, dependencies, and configuration for vulnerabilities, injection vectors, and secret leaks. Enforces threat modeling and static analysis (Semgrep/Trivy).
---

# Security Auditor Skill

## Purpose
Directs comprehensive application security audits, dependency supply chain reviews, and threat modeling.

## When to Use
- Auditing codebases for OWASP Top 10 vulnerabilities (SQLi, command injection, SSRF, path traversal).
- Performing automated static analysis using Semgrep and container scanning using Trivy.
- Enforcing least-privilege permissions and secret zero-leakage policies.

## Engineering Workflow
1. **Threat Modeling**: Identify attack surfaces, trust boundaries, and untrusted input paths.
2. **Static Analysis**:
   - Run `semgrep scan --config auto`
   - Run `cargo audit` / `npm audit` / `pip-audit`
3. **Verification**:
   - Verify zero hardcoded tokens or API keys via secret scanners.
   - Confirm defense-in-depth sanitization on all user input.

