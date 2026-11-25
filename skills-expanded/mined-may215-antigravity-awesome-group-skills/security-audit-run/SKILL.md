---
name: security-audit-run
description: "Group skill: Comprehensive security audit — threat modeling, SAST, dependency check, auth review, API security, pen testing, secrets check, GDPR, hardening, and compliance report."
risk: high
source: self
---

# 🔒 Security Audit

> **Group Skill** — Orchestrates sub-skills for periodic security reviews and compliance preparation.
> Activate by saying: "Run security audit" or "security review"

## When to Use

- Periodic security review
- Preparing for compliance audit
- After major changes to auth or data flows

## Step-by-Step Workflow

### Step 1: Threat Model
**Skill**: `threat-modeling-expert`
- Identify attack surfaces
- Map trust boundaries
- Prioritize threats

### Step 2: Code SAST
**Skill**: `security-scanning-security-sast`
- Static application security testing
- Identify code-level vulnerabilities
- Review input validation

### Step 3: Dependency Check
**Skill**: `security-scanning-security-dependencies`
- Scan for vulnerable packages
- Review dependency licenses
- Update critical vulnerabilities

### Step 4: Auth Review
**Skill**: `auth-implementation-patterns`
- Validate auth flow
- Check session management
- Review token handling

### Step 5: API Security
**Skill**: `api-security-best-practices`
- OWASP Top 10 checks
- Rate limiting review
- Input sanitization

### Step 6: Pen Test
**Skill**: `web-security-testing` + `ffuf-claude-skill`
- Active vulnerability probing
- Fuzzing endpoints
- Test for common exploits

### Step 7: Secrets Check
**Skill**: `secrets-management` + `zeroize-audit`
- No hardcoded secrets
- Review secret rotation
- Audit secret access logs

### Step 8: GDPR
**Skill**: `gdpr-data-handling` + `privacy-by-design`
- Privacy compliance review
- Data retention policies
- Consent management

### Step 9: Hardening
**Skill**: `security-scanning-security-hardening`
- System configuration review
- Network security rules
- Access control hardening

### Step 10: Report
**Skill**: `security-compliance-compliance-check`
- Generate compliance report
- Document findings
- Create remediation plan

## Completion

Security audit complete with compliance report and remediation plan. 🔒

## Sub-Skills Referenced

1. `threat-modeling-expert`
2. `security-scanning-security-sast`
3. `security-scanning-security-dependencies`
4. `auth-implementation-patterns`
5. `api-security-best-practices`
6. `web-security-testing`
7. `ffuf-claude-skill`
8. `secrets-management`
9. `zeroize-audit`
10. `gdpr-data-handling`
11. `privacy-by-design`
12. `security-scanning-security-hardening`
13. `security-compliance-compliance-check`
