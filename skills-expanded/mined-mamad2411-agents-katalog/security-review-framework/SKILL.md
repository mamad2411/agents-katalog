---
name: security-review-framework
description: >-
  Threat modeling and security review checklist for applications, infrastructure,
  and processes. Identifies attack vectors, data flows, and compliance gaps
  before production deployment.
when-to-use: >-
  Use when designing new systems, reviewing architecture changes, onboarding new
  data sources, or preparing for security audit. Also use to guide penetration
  testing scope and validate remediation.
categories:
  - security
  - risk-management
  - compliance
---

# Security Review Framework

Structured approach to identifying and remediating security risks. Covers application security, infrastructure security, data protection, and incident response.

## Threat Model Template

For each new system or major change, complete:

### 1. Asset Inventory
What are we protecting?
- [ ] Customer/user data (PII, financial data, health info?)
- [ ] Application code and configurations
- [ ] Infrastructure (databases, APIs, networks)
- [ ] Intellectual property (algorithms, trade secrets)
- [ ] Compliance/audit data (logs, access records)

**Classification**: [Public | Internal | Confidential | Restricted]

### 2. Data Flow Diagram
- [ ] Draw or describe: How data flows through system
- [ ] Identify trust boundaries (where data crosses from trusted to untrusted)
- [ ] Mark storage points (databases, caches, logs)
- [ ] Mark external integrations (APIs, third-party services)

### 3. Threat Identification

#### Authentication & Identity
- [ ] Weak passwords/MFA missing?
- [ ] Over-privileged service accounts?
- [ ] No session invalidation on logout?
- [ ] API keys exposed in logs/configs?

#### Authorization & Access Control
- [ ] Horizontal privilege escalation (users access others' data)?
- [ ] Vertical privilege escalation (non-admin becomes admin)?
- [ ] No role-based access control (RBAC)?
- [ ] Overly broad permissions?

#### Data Protection
- [ ] Unencrypted data at rest (databases, backups)?
- [ ] Unencrypted data in transit (HTTPS enforced)?
- [ ] Sensitive data logged unencrypted?
- [ ] Backup encryption missing?
- [ ] Key management insecure?

#### Network Security
- [ ] Public endpoints that should be private?
- [ ] No network segmentation (VPC/subnet isolation)?
- [ ] DDoS protection missing?
- [ ] WAF/IDS not configured?

#### API Security
- [ ] No rate limiting / brute force protection?
- [ ] SQL injection / command injection possible?
- [ ] Missing input validation?
- [ ] XXE (XML External Entity) possible?
- [ ] CORS overly permissive?

#### Third-Party Risks
- [ ] Unvetted dependencies (known vulnerabilities)?
- [ ] Supply chain attack surface (compromised packages)?
- [ ] Vendor access to production systems?
- [ ] No incident response from vendor?

#### Incident Response
- [ ] No way to detect breach?
- [ ] Logs not protected (attacker can cover tracks)?
- [ ] No backup restoration procedure?
- [ ] Incident response plan missing?

### 4. Risk Assessment

For each threat identified:

| Threat | Impact | Likelihood | Risk | Mitigation |
| --- | --- | --- | --- | --- |
| Weak passwords | High (account compromise) | High | **Critical** | Enforce MFA, min complexity |
| Unencrypted database | Critical (data breach) | Medium | **High** | Enable encryption at rest |
| No rate limiting | Medium (brute force) | High | **High** | Add rate limiting, monitoring |

### 5. Mitigation Plan

For each high/critical risk:
- [ ] **What** — Specific control (e.g., "Enable database encryption")
- [ ] **Who** — Team responsible
- [ ] **When** — Timeline (critical < 1 week, high < 1 month)
- [ ] **How verify** — How to confirm mitigation is working

---

## Security Checklist

Use for code review, infrastructure review, or pre-deployment assessment.

### Application Code
- [ ] No hardcoded secrets (password, API keys, tokens)
- [ ] Input validation on all user input
- [ ] Output encoding prevents XSS (HTML, JSON, SQL contexts)
- [ ] No SQL injection (parameterized queries or ORM)
- [ ] Authentication enforced (no unauthenticated endpoints with sensitive data)
- [ ] Authorization checks (permission verification, not just authentication)
- [ ] CSRF protection (state-changing requests use tokens)
- [ ] Secure password hashing (bcrypt, Argon2, not MD5/SHA1)
- [ ] Session security (httpOnly cookies, secure flag, SameSite)
- [ ] Dependency scanning enabled (known vulnerabilities checked)
- [ ] Error handling doesn't leak information (no stack traces in response)

### API Security
- [ ] Rate limiting implemented
- [ ] API authentication required (JWT, OAuth, mTLS)
- [ ] API authorization enforced
- [ ] Request size limits (prevent DoS)
- [ ] CORS not overly permissive
- [ ] API versioning clear (preventing breaking changes)
- [ ] Deprecated endpoints have sunset timeline

### Infrastructure Security
- [ ] Network segmentation (VPCs, subnets, security groups)
- [ ] Public endpoints restricted (no unnecessary exposure)
- [ ] Private endpoints for internal services
- [ ] WAF/DDoS protection for public endpoints
- [ ] VPN/bastion host for admin access
- [ ] Database access restricted (no public endpoint)
- [ ] Backup encryption enabled
- [ ] Backup stored in separate account/region
- [ ] Log aggregation to tamper-proof location
- [ ] Secrets encrypted (vault, not environment variables)

### Cloud Configuration
- [ ] IAM least-privilege (minimal permissions per role)
- [ ] MFA required for console access
- [ ] CloudTrail/Activity Log enabled
- [ ] Bucket/blob ACLs block public read
- [ ] VPC flow logs enabled
- [ ] KMS key policies prevent deletion
- [ ] Reserved capacity not publicly shared

### Compliance & Audit
- [ ] Privacy policy documents data processing
- [ ] Data retention policy enforced
- [ ] Audit logging captures: who, what, when, where
- [ ] Audit logs retention meets compliance requirement
- [ ] Access logs for sensitive data (data access tracking)
- [ ] Change logs for sensitive configs
- [ ] Incident response plan documented
- [ ] Security incident escalation path clear

---

## Vulnerability Assessment

When a vulnerability is discovered:

### Immediate (< 24 hours)
- [ ] Assess blast radius (how many users/systems affected?)
- [ ] Determine exploitability (how hard to exploit?)
- [ ] Check for active exploitation (review logs)
- [ ] Disable affected feature if critical
- [ ] Create incident ticket

### Short-term (< 1 week)
- [ ] Develop fix
- [ ] Test fix thoroughly
- [ ] Deploy to staging
- [ ] Peer review
- [ ] Deploy to production

### Follow-up
- [ ] Root cause analysis (why did we miss this?)
- [ ] Implement controls to catch this class of bug (SAST, linting, etc.)
- [ ] Update threat model
- [ ] Post-incident review with team

---

## Compliance Checklist

### GDPR (if processing EU personal data)
- [ ] Privacy policy describes data processing
- [ ] Consent collected for data processing
- [ ] Data minimization enforced (collect only necessary)
- [ ] Data retention policy defined and enforced
- [ ] Right to deletion implemented ("right to be forgotten")
- [ ] Data subject access request process documented
- [ ] Data Processing Agreement (DPA) with vendors
- [ ] Data breach notification procedure defined
- [ ] No data transfers to non-GDPR countries (or adequacy decision exists)

### SOC 2 Type II
- [ ] All changes logged (change log)
- [ ] Access controls documented
- [ ] Segregation of duties (dev ≠ prod access)
- [ ] Encryption for data at rest and in transit
- [ ] Security incident procedure
- [ ] Disaster recovery tested
- [ ] Backup tested (can restore?)
- [ ] Access log retention (min 90 days)

### HIPAA (if handling health data)
- [ ] HIPAA Business Associate Agreement (BAA) signed
- [ ] Encryption for PII (data at rest and in transit)
- [ ] Access controls and audit logs
- [ ] Breach notification procedure
- [ ] Workforce security training
- [ ] Physical security (data center access)
- [ ] Encryption of data in transit (TLS 1.2+)

### PCI DSS (if handling payment card data)
- [ ] No storage of CVV/CVC
- [ ] No storage of full magnetic stripe
- [ ] Tokenization of card numbers
- [ ] Encryption of transmission (TLS)
- [ ] Secure key management
- [ ] Regular security testing (penetration test, scanning)
- [ ] Compliance certification maintained

---

## Security Review Approval Checklist

✅ **Approve when:**
- Threat model completed and reviewed
- All high/critical risks mitigated
- Compliance requirements met
- Security testing passed
- Incident response plan in place

⚠️ **Request changes when:**
- Medium risks without mitigation timeline
- Secrets handling insecure
- Documentation missing
- Encryption missing from sensitive data

❌ **Block when:**
- Critical vulnerabilities unmitigated
- No authentication/authorization
- No audit logging
- Hardcoded secrets
- Known vulnerable dependencies unpatched
