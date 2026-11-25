<!-- SAGARITHM:START - DO NOT EDIT DIRECTLY -->
---
id: "security.secure-development"
name: "Secure Development & Vulnerability Prevention"
version: "1.2.0"
domain: "security"
description: "Implement defense-in-depth controls, input validation at system boundaries, secret isolation, STRIDE threat mitigation, and SSRF/timing defenses."
triggers:
  - "Handling user input, authentication, or authorization"
  - "Writing database queries, shell executions, or file operations"
  - "Introducing external dependencies or handling credentials"
  - "Processing webhooks, outgoing HTTP requests, or cryptography"
prerequisites:
  - "quality.coding-standards"
risk_profile: "critical"
---

# Secure Development & Vulnerability Prevention

## Overview
This skill guides AI agents and engineers in constructing software that resists malicious exploitation. Security is not an afterthought; it is built into every architectural boundary, input schema, cryptographic comparison, and database query.

## Core Directives
1. **Never Commit Secrets**: Prevent API keys, tokens, or credentials from entering git history. Use environment configuration.
2. **Validate at the Perimeter**: Parse and validate all external payloads using strict schemas before business logic processing.
3. **Prevent Injection by Default**: Use parameterized queries for databases and structured argument arrays for process executions.
4. **Enforce Least Privilege**: Run processes and queries with the minimal permissions necessary.
5. **Mitigate Timing Attacks**: Always use constant-time comparison functions when evaluating tokens, signatures, or HMACs.
6. **Defend Against SSRF**: Validate resolved IP addresses of external URLs to block internal network access and cloud metadata exploitation.

## 🛑 Anti-Rationalization Matrix

| Agent Excuse / Shortcut | Security Reality | Mandatory Action |
|---|---|---|
| *"I'll hardcode the API key temporarily for local testing."* | Temporary keys get committed accidentally, triggering irreversible credential exposure. | Always load secrets from environment variables or `.env.local`. |
| *"This input comes from an internal source, so validation is redundant."* | Internal boundaries erode over time, leading to lateral privilege escalation. | Validate all inputs with strict schemas at module boundaries. |
| *"Using string concatenation for this SQL/Command is safe here."* | String concatenation is the root cause of SQL injection and command injection flaws. | Strictly use parameterized statements and structured argument arrays. |

## Detailed Guidance
- [OWASP Defense in Depth Guidelines](references/owasp-defense-in-depth.md)
- [STRIDE Threat Modeling & Advanced Attack Defense](references/threat-modeling-and-stride.md)
- [Input Validation & Secret Isolation Examples](examples/input-validation-and-secrets.md)
- [Advanced Defensive Security Patterns](examples/advanced-security-patterns.md)
- [Security Audit Checklist](checklists/security-audit-checklist.md)
<!-- SAGARITHM:END -->
