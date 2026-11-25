---
name: secure-coding
description: Defensive security guidance for code — input validation, secrets handling, auth, common vulnerability classes (OWASP Top 10).
category: security
aliases:
- security-coding
- appsec
- owasp
- vulnerability
triggers:
- check this code for security issues
- check code for security
- security check
- is this code secure
- security review
- secure coding
- OWASP
- check for vulnerabilities
- prevent SQL injection
- prevent XSS
keywords:
- security
- secure
- owasp
- xss
- sql
- injection
- vulnerability
- validate
- sanitize
- auth
dependencies: []
risk: medium
version: 1.0.0
source: custom
enabled: true
author: Mr-Nobody-Anonymous
tags:
- coding
- owasp
- secure
- security
- xss
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Secure Coding

## Purpose

Identify and prevent security defects in code: input validation, output encoding, secrets
handling, authentication / authorization, and the OWASP Top 10.

## When to Use

- User asks if code is secure
- User is implementing auth, payments, PII handling
- Reviewing a security-sensitive change

## When NOT to Use

- The user wants a full penetration test (recommend a security professional)
- The user wants infrastructure / cloud security (route to `security-audit`)

## Capabilities

- Identify common vulnerability classes
- Suggest specific fixes
- Map to OWASP / CWE references

## Coverage

- Injection (SQL, command, LDAP)
- XSS / CSRF
- AuthN / AuthZ flaws
- Secrets in code / logs
- Insecure deserialization
- SSRF, path traversal
- Dependency CVEs

## Safety

- This is a defensive skill — never offensive
- For real vulnerabilities, suggest reporting via responsible disclosure

## Source

Custom skill, written for this library. References OWASP Top 10 and CWE.

## Notes

Pairs with `code-review`, `dependency-audit`, `secret-detection`.

## Inputs

- The user's goal and desired output.
- Relevant source material, constraints, and environment details.
- Acceptance criteria when available.

## Workflow

1. Confirm the goal, scope, and constraints.
2. Inspect the available context before acting.
3. Apply the skill-specific guidance in this document.
4. Verify the result and report limitations or next steps.

## Tools

- No mandatory tool unless declared in frontmatter.
- Use only project-approved tools and documented optional dependencies.

## Examples

Requests that should activate this skill include: "is this code secure"; "security review"; "secure coding".
