---
name: security-doc
description: |
  Generate a complete SECURITY.md file for any software project. Use whenever the user asks to create, write, generate, or draft a SECURITY.md — a comprehensive security documentation covering threat models, security controls, authentication, authorization, data protection, compliance requirements, and security best practices.

  This skill triggers when users need to document: security architecture, threat models, security controls, compliance requirements (GDPR, HIPAA, SOC 2), authentication/authorization design, data protection strategies, vulnerability management, incident response, or "how is this system secured".

  Do NOT trigger for general architecture docs (use Architecture.md), single-feature security (include in Design.md), or code-level security reviews.

---

# SECURITY.md Author Skill

You are a security architect documenting the security posture and controls of a software system.

## Philosophy

A SECURITY.md answers: **"How is this system protected from threats?"**

It covers:
- **Threat Model** - What are we protecting against?
- **Security Controls** - What protections are in place?
- **Authentication & Authorization** - Who can access what?
- **Data Protection** - How is sensitive data secured?
- **Compliance** - What regulations/standards do we meet?
- **Incident Response** - What happens when something goes wrong?

The audience is **security engineers, auditors, compliance teams, and technical stakeholders** who need to understand and verify the system's security. This document is critical for security audits, compliance certifications, and incident response.

## Structure

A SECURITY.md has **10 core sections**:

1. **Security Overview** - Posture and strategy summary
2. **Threat Model** - Assets, threats, and attack vectors
3. **Authentication** - How users prove identity
4. **Authorization** - Access control and permissions
5. **Data Protection** - Encryption and data security
6. **Network Security** - Infrastructure and network controls
7. **Application Security** - Code-level protections
8. **Compliance & Standards** - Regulatory requirements
9. **Monitoring & Incident Response** - Detection and response
10. **Security Operations** - Ongoing security practices

## Workflow: Interview → Draft → Validate

### Step 1: Interview the User

Gather security context before writing:

**Required context:**
- **What's the system?** (type, purpose, users)
- **What data is sensitive?** (PII, financial, health, secrets)
- **What are the threats?** (external attackers, insider threats, data breaches)
- **Any compliance requirements?** (GDPR, HIPAA, PCI-DSS, SOC 2, ISO 27001)
- **Current security state?** (documenting existing or designing new)

**Optional but helpful:**
- **User types?** (public users, employees, admins, partners)
- **Deployment environment?** (cloud, on-prem, hybrid)
- **Previous incidents?** (learn from past breaches)
- **Risk tolerance?** (startup vs bank vs healthcare)

If sparse info, make reasonable security-first assumptions and note them.

### Step 2: Build the Document Structure

```markdown
# [System Name] - Security Documentation

**Version:** 1.0
**Last Updated:** [Date]
**Classification:** [Confidential | Internal | Public]
**Owner:** Security Team
**Status:** [Current | Under Review | Needs Update]

---

## 1. Security Overview

### Security Posture
[2-3 paragraphs describing the overall security approach and maturity level]

Our security strategy follows a **defense-in-depth** approach with multiple layers of protection. We implement security controls at the network, infrastructure, application, and data layers to ensure comprehensive protection against threats.

### Security Objectives
1. **Confidentiality** - Protect sensitive data from unauthorized access
2. **Integrity** - Ensure data accuracy and prevent tampering
3. **Availability** - Maintain system uptime and resilience against attacks
4. **Compliance** - Meet regulatory requirements (GDPR, SOC 2, etc.)

### Risk Classification
- **System Criticality:** [Critical | High | Medium | Low]
- **Data Sensitivity:** [Highly Sensitive | Sensitive | Internal | Public]
- **Attack Surface:** [Internet-facing | Internal | Hybrid]
- **User Base:** [Public | Enterprise | Internal]

### Security Standards Followed
- OWASP Top 10 (web application security)
- CIS Benchmarks (infrastructure hardening)
- NIST Cybersecurity Framework
- [Industry-specific standards: PCI-DSS, HIPAA, etc.]

---

## 2. Threat Model

### Assets

#### Critical Assets
1. **User Data**
   - Type: PII (names, emails, addresses), authentication credentials
   - Storage: PostgreSQL database (encrypted at rest)
   - Access: Application servers only, admin read-only
   - Impact if compromised: High - privacy violation, regulatory fines

2. **API Keys & Secrets**
   - Type: Third-party API keys, database credentials, encryption keys
   - Storage: AWS Secrets Manager (rotated every 90 days)
   - Access: Application runtime only, no human access
   - Impact if compromised: Critical - full system compromise

3. **Source Code & IP**
   - Type: Proprietary algorithms, business logic
   - Storage: GitHub private repositories
   - Access: Engineers with 2FA, no external contractors
   - Impact if compromised: Medium - competitive disadvantage

4. **Financial Data**
   - Type: Payment information, transaction history
   - Storage: Stripe (PCI-DSS compliant third party)
   - Access: We never store credit card numbers (tokenized)
   - Impact if compromised: Critical - financial fraud, regulatory penalties

### Threat Actors

#### External Attackers
- **Motivation:** Financial gain, data theft, disruption
- **Capabilities:** Automated scanning, known exploits, social engineering
- **Likelihood:** High (internet-facing application)
- **Mitigations:** WAF, rate limiting, security updates, monitoring

#### Insider Threats
- **Motivation:** Malicious intent, negligence, compromised credentials
- **Capabilities:** Legitimate access, knowledge of systems
- **Likelihood:** Low (small trusted team, background checks)
- **Mitigations:** Least privilege, audit logging, access reviews

#### Supply Chain Attacks
- **Motivation:** Compromise through dependencies/vendors
- **Capabilities:** Malicious packages, compromised updates
- **Likelihood:** Medium (many npm/pip dependencies)
- **Mitigations:** Dependency scanning, SRI hashes, vendor assessments

### Attack Vectors

| Attack Vector | Likelihood | Impact | Mitigation |
|---------------|------------|--------|------------|
| SQL Injection | Medium | High | Parameterized queries, ORM, WAF |
| XSS (Cross-Site Scripting) | Medium | Medium | Input sanitization, CSP headers |
| CSRF | Low | Medium | CSRF tokens, SameSite cookies |
| Credential Stuffing | High | High | Rate limiting, MFA, breach detection |
| DDoS | Medium | High | CDN, rate limiting, auto-scaling |
| API Abuse | High | Medium | API keys, rate limits, quotas |
| Phishing | High | High | Security awareness training, 2FA |
| Insider Data Theft | Low | Critical | Access logs, DLP, least privilege |

### Trust Boundaries

```
┌─────────────────────────────────────────────────┐
│             Untrusted Zone                      │
│  • Internet users                               │
│  • Third-party services                         │
└────────────────┬────────────────────────────────┘
                 │ TLS, Auth, Rate Limiting
┌────────────────▼────────────────────────────────┐
│             DMZ / Edge Layer                    │
│  • Load Balancer                                │
│  • WAF                                          │
│  • API Gateway                                  │
└────────────────┬────────────────────────────────┘
                 │ Authentication Required
┌────────────────▼────────────────────────────────┐
│          Application Layer (Private Subnet)     │
│  • Application Servers                          │
│  • Business Logic                               │
└────────────────┬────────────────────────────────┘
                 │ Service Accounts Only
┌────────────────▼────────────────────────────────┐
│          Data Layer (Isolated Subnet)           │
│  • Databases                                    │
│  • No Internet Access                           │
└─────────────────────────────────────────────────┘
```

---

## 3. Authentication

### User Authentication

#### Authentication Methods
- **Primary:** Email + Password with bcrypt hashing (cost factor 12)
- **MFA (Multi-Factor Auth):** TOTP (Google Authenticator, Authy) - required for admins
- **SSO:** OAuth 2.0 / OIDC (Google, Microsoft, Okta) - enterprise customers
- **API Keys:** SHA-256 hashed, prefix-scoped, user-generated

#### Password Policy
- Minimum length: 12 characters
- Complexity: Must include uppercase, lowercase, number, special character
- No common passwords (checked against breach database)
- Password expiry: 90 days for admins, optional for users
- Password history: Cannot reuse last 5 passwords
- Lockout: 5 failed attempts = 15-minute lockout

#### Session Management
- **Session Tokens:** JWT (JSON Web Tokens)
- **Token Lifetime:** Access token 15 minutes, refresh token 7 days
- **Storage:** Refresh tokens stored in HTTP-only, Secure, SameSite cookies
- **Invalidation:** Logout revokes refresh token server-side
- **Device Tracking:** Track active sessions, allow user to revoke

#### Account Recovery
- **Password Reset:** Email link with token (1-hour expiry, single-use)
- **Account Lockout Recovery:** Contact support after verification
- **Backup Codes:** 10 single-use codes for MFA recovery

### Service-to-Service Authentication
- **Method:** Mutual TLS (mTLS) for internal services
- **API Gateway:** API keys with scoped permissions
- **Cloud Services:** IAM roles, no long-lived credentials

---

## 4. Authorization

### Access Control Model
**Role-Based Access Control (RBAC)**

### Roles & Permissions

#### User Roles
1. **Public User** (unauthenticated)
   - View public content
   - Register for account

2. **Authenticated User**
   - Create/read/update/delete own resources
   - View shared resources
   - Cannot access admin features

3. **Premium User** (paid tier)
   - All User permissions
   - Access to premium features
   - Higher rate limits

4. **Organization Admin**
   - Manage organization members
   - View organization-wide analytics
   - Configure organization settings

5. **System Admin** (internal staff)
   - Full system access
   - User management
   - System configuration
   - Audit log access

6. **Support Agent** (internal staff)
   - Read-only access to user data
   - Cannot modify financial data
   - All actions logged

### Permission Matrix

| Resource | Public | User | Premium | Org Admin | Sys Admin | Support |
|----------|--------|------|---------|-----------|-----------|---------|
| Public Content | Read | Read | Read | Read | Full | Read |
| User Profile | - | Owner | Owner | Owner | Full | Read |
| Projects | - | Owner | Owner | Team | Full | Read |
| Billing | - | Owner | Owner | Org | Full | Read |
| Analytics | - | Own | Own | Org | Full | - |
| Admin Panel | - | - | - | - | Full | Limited |
| Audit Logs | - | - | - | - | Full | - |

### Authorization Enforcement
- **Application Layer:** Check permissions before every action
- **Database Layer:** Row-level security policies (PostgreSQL RLS)
- **API Gateway:** Scope validation on API keys
- **Frontend:** UI elements hidden based on permissions (defense in depth, not security boundary)

### Principle of Least Privilege
- Default deny (no access unless explicitly granted)
- Time-limited elevated access (admin actions expire after 1 hour)
- Separate accounts for admin vs regular use
- Regular access reviews (quarterly)

---

## 5. Data Protection

### Data Classification

| Classification | Examples | Encryption | Access | Retention |
|----------------|----------|------------|--------|-----------|
| Public | Marketing content, blog posts | No | Anyone | Indefinite |
| Internal | Employee emails, internal docs | In transit | Employees | 7 years |
| Confidential | Customer data, source code | At rest + transit | Need-to-know | Per policy |
| Restricted | Credentials, PII, payment data | At rest + transit + in-use | Minimal | Regulated |

### Encryption

#### Encryption at Rest
- **Database:** AES-256 encryption (AWS RDS encryption enabled)
- **File Storage:** AES-256 (S3 server-side encryption with AWS KMS)
- **Backups:** Encrypted with separate keys
- **Disk Encryption:** Full disk encryption on all servers (LUKS/BitLocker)

#### Encryption in Transit
- **External:** TLS 1.3 only (TLS 1.2 deprecated)
- **Internal:** TLS 1.2+ for service-to-service
- **Certificate Management:** Let's Encrypt auto-renewal, 90-day rotation
- **Perfect Forward Secrecy:** Enabled (ECDHE cipher suites)

#### Key Management
- **Storage:** AWS KMS (Key Management Service)
- **Rotation:** Automatic 1-year rotation for data keys
- **Access:** Keys never leave KMS, services use API to encrypt/decrypt
- **Backup:** Master keys backed up in offline HSM

### Sensitive Data Handling

#### Personally Identifiable Information (PII)
- **Storage:** Encrypted database columns for SSN, DOB, addresses
- **Transmission:** Always over TLS
- **Logging:** PII redacted from application logs
- **Masking:** Display only last 4 digits of SSN, partial email
- **Deletion:** Hard delete within 30 days of account closure (GDPR right to erasure)

#### Secrets & Credentials
- **Application Secrets:** AWS Secrets Manager (auto-rotation every 90 days)
- **API Keys:** Hashed with SHA-256, prefix for identification
- **Database Passwords:** Unique per environment, never in code
- **Encryption Keys:** Hardware Security Module (HSM) backed

#### Payment Data
- **Strategy:** Never store credit card numbers (PCI-DSS Level 1 avoidance)
- **Processor:** Stripe (PCI-DSS compliant)
- **Tokenization:** Store Stripe tokens only, not raw card data
- **Compliance:** PCI-DSS SAQ-A (merchant using fully outsourced solution)

### Data Retention & Deletion

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| User account data | Until account closure + 30 days | Hard delete (overwrite) |
| Transaction logs | 7 years (legal requirement) | Automated purge script |
| Audit logs | 1 year | Archive to cold storage, then delete |
| Backups | 30 days rolling | Encrypted deletion |
| Temporary files | 24 hours | Secure wipe |

---

## 6. Network Security

### Network Architecture

```
                    ┌──────────────┐
                    │   Internet   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  CloudFlare  │
                    │  (DDoS, WAF) │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Load Balancer│
                    │   (AWS ALB)  │
                    └──────┬───────┘
                           │
        ┌──────────────────┴──────────────────┐
        │         VPC (10.0.0.0/16)           │
        │                                     │
        │  ┌──────────────────────────────┐  │
        │  │  Public Subnet (10.0.1.0/24) │  │
        │  │  • NAT Gateway               │  │
        │  │  • Bastion Host              │  │
        │  └──────────────────────────────┘  │
        │                                     │
        │  ┌──────────────────────────────┐  │
        │  │ Private Subnet (10.0.2.0/24) │  │
        │  │  • Application Servers       │  │
        │  │  • No direct internet        │  │
        │  └──────────────────────────────┘  │
        │                                     │
        │  ┌──────────────────────────────┐  │
        │  │Database Subnet (10.0.3.0/24) │  │
        │  │  • RDS (PostgreSQL)          │  │
        │  │  • Redis                     │  │
        │  │  • No internet access        │  │
        │  └──────────────────────────────┘  │
        └─────────────────────────────────────┘
```

### Firewall Rules (Security Groups)

#### Load Balancer
- **Inbound:** 443 (HTTPS) from 0.0.0.0/0, 80 (HTTP redirect)
- **Outbound:** Application servers only

#### Application Servers
- **Inbound:** 8080 from Load Balancer only
- **Outbound:** Database subnet, external APIs (443), NAT gateway

#### Database
- **Inbound:** 5432 from Application Servers only
- **Outbound:** None (isolated)

### DDoS Protection
- **Layer 7:** Cloudflare WAF with rate limiting
- **Layer 4:** AWS Shield Standard (included)
- **Mitigations:** 
  - Auto-scaling to absorb traffic spikes
  - Connection limits per IP
  - Geographic blocking (if needed)

### Web Application Firewall (WAF)
- **Provider:** Cloudflare
- **Rules:**
  - OWASP Core Rule Set (CRS)
  - Rate limiting: 100 requests/minute per IP
  - Bot detection and blocking
  - Geo-blocking: Block high-risk countries (if applicable)
  - Custom rules for known attack patterns

### VPN & Remote Access
- **Employee Access:** AWS VPN with MFA (not direct SSH)
- **Bastion Host:** Jump box for emergency access (heavily logged)
- **SSH Keys:** Ed25519, rotated every 90 days, no password auth

---

## 7. Application Security

### Secure Development Practices

#### Code Security
- **Input Validation:** Whitelist validation for all user input
- **Output Encoding:** Context-aware encoding (HTML, JavaScript, SQL)
- **Parameterized Queries:** No string concatenation in SQL
- **ORM Usage:** SQLAlchemy with bound parameters
- **Avoid Dangerous Functions:** No eval(), exec(), or similar

#### Security Testing
- **SAST (Static Analysis):** Snyk, Semgrep on every commit
- **DAST (Dynamic Analysis):** OWASP ZAP weekly scans
- **Dependency Scanning:** Automated checks for vulnerable libraries
- **Penetration Testing:** Annual third-party pen test

### OWASP Top 10 Mitigations

| Vulnerability | Mitigation |
|---------------|------------|
| **A01: Broken Access Control** | RBAC enforced at every layer, principle of least privilege |
| **A02: Cryptographic Failures** | TLS 1.3, AES-256, proper key management |
| **A03: Injection** | Parameterized queries, input validation, ORM |
| **A04: Insecure Design** | Threat modeling, security reviews, secure defaults |
| **A05: Security Misconfiguration** | Hardened configs, disable defaults, remove unused features |
| **A06: Vulnerable Components** | Dependency scanning, automated updates, version pinning |
| **A07: Auth/Identity Failures** | MFA, strong passwords, session management, rate limiting |
| **A08: Software & Data Integrity** | Code signing, SRI hashes, integrity checks |
| **A09: Logging & Monitoring** | Comprehensive logs, real-time alerts, SIEM integration |
| **A10: SSRF** | Whitelist external URLs, network segmentation |

### Security Headers
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

### API Security
- **Authentication:** JWT with short expiry (15 min)
- **Rate Limiting:** 1000 requests/hour per user, 100 requests/hour per IP
- **Input Validation:** JSON schema validation on all endpoints
- **Output Filtering:** Remove sensitive fields before serialization
- **Versioning:** /api/v1/ to manage breaking changes
- **CORS:** Strict origin whitelist

### Secrets Management
- **No Hardcoded Secrets:** All secrets in environment variables or secret store
- **Secret Scanning:** Automated scans for committed secrets (Gitleaks)
- **Rotation:** Automated 90-day rotation for all credentials
- **Access Logs:** All secret access logged and monitored

---

## 8. Compliance & Standards

### Regulatory Compliance

#### GDPR (General Data Protection Regulation)
**Applicability:** EU citizens' data

**Controls:**
- ✅ **Lawful Basis:** User consent for data processing
- ✅ **Data Minimization:** Collect only necessary data
- ✅ **Right to Access:** Users can download their data (API endpoint)
- ✅ **Right to Erasure:** Account deletion within 30 days
- ✅ **Data Portability:** Export data in JSON format
- ✅ **Privacy by Design:** Security built-in from start
- ✅ **Data Breach Notification:** 72-hour notification procedure
- ✅ **DPO:** Data Protection Officer appointed

#### SOC 2 Type II
**Applicability:** Enterprise customers require audit

**Trust Service Criteria:**
- ✅ **Security:** Access controls, encryption, monitoring
- ✅ **Availability:** 99.9% uptime SLA, redundancy
- ✅ **Confidentiality:** Data segregation, encryption
- ⏳ **Processing Integrity:** Transaction validation (in progress)
- ⏳ **Privacy:** GDPR compliance, privacy policy (in progress)

**Audit Schedule:** Annual audit by external firm

#### HIPAA (if applicable)
**Applicability:** Healthcare data

**Controls:**
- ✅ **Access Controls:** Unique user IDs, automatic logoff
- ✅ **Audit Controls:** Complete audit trail of PHI access
- ✅ **Integrity:** Checksums to detect unauthorized changes
- ✅ **Transmission Security:** TLS 1.3 for all PHI
- ✅ **BAA:** Business Associate Agreements with vendors

### Security Certifications
- [ ] SOC 2 Type II (target: Q4 2026)
- [ ] ISO 27001 (planned: 2027)
- [ ] PCI-DSS Level 1 (not required - using Stripe)

### Third-Party Security
**Vendor Risk Management:**
- Security questionnaire for all vendors handling data
- SOC 2 reports required from critical vendors
- Annual vendor reviews
- Contractual security requirements (DPA, BAA)

---

## 9. Monitoring & Incident Response

### Security Monitoring

#### Logging
**What We Log:**
- Authentication events (login, logout, failed attempts)
- Authorization failures (access denied)
- Data access (who accessed what when)
- System changes (config modifications)
- API calls (endpoint, user, timestamp, response code)
- Security events (WAF blocks, rate limit triggers)

**Log Storage:**
- **Aggregation:** CloudWatch Logs / ELK Stack
- **Retention:** 1 year (compliance requirement)
- **Protection:** Write-once logs, tamper-evident
- **Access:** Security team only, all access logged

#### Security Information and Event Management (SIEM)
- **Tool:** Splunk / Datadog Security Monitoring
- **Use Cases:**
  - Brute force detection (5+ failed logins in 5 minutes)
  - Anomalous access patterns (unusual time/location)
  - Privilege escalation attempts
  - Data exfiltration (large downloads)

#### Alerting
**Real-Time Alerts (PagerDuty):**
- Multiple failed authentication attempts
- Admin privilege usage
- WAF blocking spike
- Database connection from unexpected IP
- Secret access outside business hours

**Daily Digest (Email):**
- Security scan results
- Failed authentication summary
- High-risk user actions

### Vulnerability Management

#### Scanning
- **Dependency Scans:** Snyk on every commit
- **Container Scans:** Docker image vulnerabilities
- **Infrastructure Scans:** AWS Security Hub findings
- **Web App Scans:** OWASP ZAP weekly

#### Patching
- **Critical:** 24 hours
- **High:** 7 days
- **Medium:** 30 days
- **Low:** Next maintenance window

#### Penetration Testing
- **Frequency:** Annual external pen test
- **Scope:** Full system, web app, APIs, infrastructure
- **Remediation:** Critical findings within 30 days

### Incident Response

#### Incident Response Team
- **Incident Commander:** Security Lead
- **Technical Lead:** Engineering Manager
- **Communications:** Product Manager
- **Legal/Compliance:** Legal Counsel

#### Incident Response Process

**1. Detection & Triage (0-15 minutes)**
- Alert received from monitoring
- Severity assessment (P0-P4)
- Incident declared if confirmed

**2. Containment (15-60 minutes)**
- Isolate affected systems
- Revoke compromised credentials
- Block malicious IPs
- Preserve evidence

**3. Investigation (1-4 hours)**
- Root cause analysis
- Scope assessment (what data accessed?)
- Timeline reconstruction
- Impact analysis

**4. Eradication (4-24 hours)**
- Remove malware/backdoors
- Patch vulnerabilities
- Update security rules
- Verify clean state

**5. Recovery (24-48 hours)**
- Restore systems from clean backups
- Monitor for re-compromise
- Gradual traffic restoration

**6. Post-Incident (1 week)**
- Post-mortem document
- Lessons learned
- Process improvements
- Stakeholder communication

#### Incident Severity Levels

| Level | Description | Response Time | Notification |
|-------|-------------|---------------|--------------|
| **P0 (Critical)** | Active breach, data loss, full outage | Immediate | CEO, customers, regulators |
| **P1 (High)** | Partial breach, degraded service | <1 hour | Exec team, affected customers |
| **P2 (Medium)** | Vulnerability, minor impact | <4 hours | Internal team |
| **P3 (Low)** | Security finding, no immediate risk | <24 hours | Security team |

#### Breach Notification
- **GDPR:** 72 hours to notify regulators, immediate for affected users
- **State Laws:** Varies by jurisdiction (California: immediate)
- **Communication Plan:** Pre-drafted templates, legal review, PR coordination

---

## 10. Security Operations

### Security Review Process

#### Code Reviews
- **Security Champion:** One engineer trained in security per team
- **Checklist:** Authentication, authorization, input validation, secrets
- **Approval:** Security-sensitive changes require security team review

#### Architecture Reviews
- **When:** Before new features with security implications
- **Participants:** Security team, architects, relevant engineers
- **Output:** Threat model, security requirements, go/no-go decision

#### Quarterly Security Audits
- Access reviews (remove unused accounts)
- Permission audits (verify least privilege)
- Secret rotation verification
- Compliance checklist review

### Security Training
- **Onboarding:** Security basics for all engineers (4 hours)
- **Annual Training:** Phishing awareness, secure coding
- **Champions Program:** Advanced training for security champions
- **Incident Drills:** Tabletop exercises quarterly

### Bug Bounty Program
- **Platform:** HackerOne / Bugcrowd
- **Scope:** Web application, APIs (not infrastructure)
- **Rewards:** $100-$10,000 based on severity
- **Response SLA:** Triage within 2 business days

### Security Metrics

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Mean Time to Detect (MTTD) | <1 hour | 0.8 hours | ↗️ |
| Mean Time to Respond (MTTR) | <4 hours | 3.2 hours | ↗️ |
| Vulnerability Patching (Critical) | <24 hours | 18 hours | ↗️ |
| Security Training Completion | 100% | 95% | → |
| Failed Auth Rate | <1% | 0.8% | ↗️ |
| Security Incidents (P0-P1) | 0 | 0 | ✅ |

---

## 11. Security Contacts

### Responsible Disclosure
**Security Email:** security@company.com
**PGP Key:** [Link to public key]
**Response SLA:** 48 hours

### Security Team
- **CISO:** [Name] - [email]
- **Security Engineer:** [Name] - [email]
- **Compliance Manager:** [Name] - [email]

### Escalation Path
1. Security team (security@company.com)
2. Engineering Manager
3. CTO
4. CEO (for critical incidents)

---

## 12. Appendix

### Glossary
- **RBAC:** Role-Based Access Control
- **MFA/2FA:** Multi-Factor / Two-Factor Authentication
- **PII:** Personally Identifiable Information
- **WAF:** Web Application Firewall
- **SIEM:** Security Information and Event Management
- **SAST:** Static Application Security Testing
- **DAST:** Dynamic Application Security Testing

### References
- [OWASP Top 10](https://owasp.org/Top10/)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Cloud Security Alliance](https://cloudsecurityalliance.org/)

### Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-07-22 | Security Team | Initial security documentation |

### Review Schedule
- **Frequency:** Quarterly or after major changes
- **Next Review:** 2026-10-22
- **Owner:** Security Team

---

## Maintenance Notes

**This document should be updated when:**
- New security controls are implemented
- Security incidents occur (update lessons learned)
- Compliance requirements change
- New threats emerge
- Architecture changes affect security
- Audit findings require changes

**Document Classification:** Internal - Security Team + Engineering Leadership
