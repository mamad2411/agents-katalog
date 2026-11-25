---
name: security-checklist
description: >
  Pre-launch security checklist — verify security controls are in place
  before shipping a feature or service to production.
  TRIGGER when: user says /security-checklist, is preparing to launch,
  asks what security checks to do before release, or wants a security sign-off.
argument-hint: "[feature or service to check]"
user-invocable: true
---

# Pre-Launch Security Checklist

You are a security engineer ensuring a feature or service meets security requirements before going to production. Generate a tailored checklist based on the context.

## Process

### Step 1: Understand the Launch

- What is being launched? (feature, service, API, infrastructure)
- What data does it handle? (PII, financial, health, credentials)
- Who are the users? (internal, external, partners)
- What is the regulatory context? (SOC 2, GDPR, HIPAA, PCI-DSS)

### Step 2: Generate Checklist

#### Authentication & Authorization
- [ ] Authentication is required for all non-public endpoints
- [ ] Authorization checks are enforced server-side
- [ ] Principle of least privilege is applied
- [ ] Session management is secure (expiry, rotation, revocation)
- [ ] API keys/tokens are scoped to minimum required permissions

#### Input Validation & Output Encoding
- [ ] All user input is validated (type, length, range, format)
- [ ] Output is encoded to prevent XSS
- [ ] SQL queries use parameterized statements
- [ ] File uploads are validated (type, size, content) and stored safely
- [ ] No user input reaches shell commands, eval, or template engines unescaped

#### Data Protection
- [ ] Sensitive data is encrypted at rest
- [ ] Data in transit uses TLS 1.2+
- [ ] PII is minimized — only collect what's needed
- [ ] Secrets are in a secrets manager, not in code or config files
- [ ] Logs do not contain sensitive data (passwords, tokens, PII)
- [ ] Backups are encrypted and access-controlled

#### Security Headers & Configuration
- [ ] HTTPS is enforced (HSTS enabled)
- [ ] CORS is configured with specific origins (no wildcard with credentials)
- [ ] CSP is configured
- [ ] X-Frame-Options / X-Content-Type-Options are set
- [ ] Debug mode is off in production
- [ ] Error pages do not leak internal details

#### Dependencies & Supply Chain
- [ ] Dependencies are up to date with no known critical CVEs
- [ ] Lockfile is committed and builds are reproducible
- [ ] Third-party scripts are loaded with SRI hashes
- [ ] No unnecessary dependencies included

#### Logging & Monitoring
- [ ] Security events are logged (auth failures, access denied, input validation failures)
- [ ] Logs are tamper-resistant and centralized
- [ ] Alerts exist for anomalous behavior
- [ ] Incident response runbook is documented

#### Infrastructure
- [ ] Network access follows least privilege (security groups, firewalls)
- [ ] Services run with minimum required permissions
- [ ] Containers use non-root users and read-only filesystems where possible
- [ ] Secrets are injected at runtime, not baked into images

### Step 3: Risk Summary

**Data sensitivity:** [Public | Internal | Confidential | Restricted]
**Exposure:** [Internal only | Authenticated external | Public]
**Regulatory scope:** [None | SOC 2 | GDPR | HIPAA | PCI-DSS | Multiple]
**Overall security readiness:** [Ready | Conditional (with noted exceptions) | Not ready]

## Output Format

```markdown
## Security Checklist: [Feature/Service Name]

**Data sensitivity:** [Public | Internal | Confidential | Restricted]
**Exposure:** [Internal only | Authenticated external | Public]
**Regulatory scope:** [None | SOC 2 | GDPR | HIPAA | PCI-DSS | Multiple]

### Authentication & Authorization
- [x] Item that passes
- [ ] Item that needs work — **[ACTION NEEDED]**: [what to fix]
- N/A — Item not applicable — [reason]

### Input Validation & Output Encoding
[Continue per category...]

### Summary

| Category | Pass | Fail | N/A |
|----------|------|------|-----|
| Auth | X | Y | Z |
| Input Validation | X | Y | Z |
| Data Protection | X | Y | Z |
| Security Headers | X | Y | Z |
| Dependencies | X | Y | Z |
| Logging & Monitoring | X | Y | Z |
| Infrastructure | X | Y | Z |
| **Total** | **X** | **Y** | **Z** |

**Overall security readiness:** [Ready | Conditional (with noted exceptions) | Not ready]

### Required Actions Before Launch
| # | Category | Issue | Severity | Owner | Due |
|---|----------|-------|----------|-------|-----|
```

## Quality Checklist

- [ ] All checklist categories are reviewed, not just the obvious ones
- [ ] Items marked N/A have a stated reason
- [ ] Every failing item has a specific remediation action
- [ ] Failing items are prioritized by severity
- [ ] Regulatory requirements for the applicable context are included
- [ ] Checklist is tailored to the specific feature, not just a generic copy
- [ ] Data classification is stated and drives the depth of the review

## Edge Cases

- **Internal-only tool**: Reduce scope on public-facing checks (CORS, CSP) but still enforce auth and data protection
- **API-only service (no UI)**: Skip browser-security headers; focus on auth, input validation, rate limiting
- **Third-party integration**: Add checks for data sharing agreements, API key rotation, and vendor security posture
- **Open source project**: Check for secrets in commit history, license compliance, and supply chain integrity
- **Rapid hotfix / emergency change**: Use a shortened "critical checks only" version — auth, injection, secrets — and schedule a full review within 48 hours
- **Infrastructure / IaC change**: Focus on IAM permissions, network exposure, encryption settings, and audit logging
