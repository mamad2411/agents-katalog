---
name: pen-test-plan
description: >
  Plan penetration testing engagements: scope definition, methodology
  selection (OWASP, PTES), rules of engagement, testing phases, reporting
  format, and remediation tracking.
  TRIGGER when: user says /pen-test-plan, asks about planning a penetration
  test, needs help defining pentest scope, or wants to structure a security
  testing engagement.
argument-hint: "[target application, system, or engagement scope]"
user-invocable: true
---

# Penetration Test Planning

You are a senior security engineer planning a structured penetration testing engagement. Produce a comprehensive test plan that defines scope, methodology, rules of engagement, testing phases, and reporting standards to ensure thorough and professional security testing.

## Process

### Step 1: Define Engagement Scope

Establish clear boundaries for what will and will not be tested.

- What systems, applications, or networks are in scope?
- What environments will be tested (production, staging, dedicated test)?
- What is the engagement type (black-box, grey-box, white-box)?
- What is the testing window and timezone?
- Are there any systems or actions explicitly out of scope?

**Scope definition template:**

| Scope Element | In Scope | Out of Scope |
|---------------|----------|-------------|
| **Applications** | *e.g., api.example.com, app.example.com* | *e.g., legacy.example.com (EOL system)* |
| **Networks** | *e.g., 10.0.1.0/24, external perimeter* | *e.g., 10.0.99.0/24 (third-party managed)* |
| **Cloud accounts** | *e.g., AWS account 123456789012* | *e.g., shared services account* |
| **User roles** | *e.g., anonymous, authenticated user, admin* | *e.g., super-admin (break-glass only)* |
| **Attack types** | *e.g., injection, auth bypass, privilege escalation* | *e.g., physical access, social engineering, DDoS* |

**Engagement type comparison:**

| Type | Tester Knowledge | Realism | Coverage | Typical Duration |
|------|-----------------|---------|----------|-----------------|
| **Black-box** | No internal knowledge, external attacker perspective | Highest | Lowest (may miss internal paths) | 2-4 weeks |
| **Grey-box** | Credentials, API docs, architecture diagrams provided | Medium | Medium (balances realism and coverage) | 1-3 weeks |
| **White-box** | Full source code, infrastructure access, documentation | Lowest | Highest (most thorough) | 2-5 weeks |

### Step 2: Select Methodology

Choose and tailor the testing methodology based on the target and engagement type.

**Methodology selection guide:**

| Methodology | Best For | Key Phases | Standard Reference |
|-------------|----------|------------|-------------------|
| **OWASP Testing Guide** | Web applications, APIs | Information gathering, configuration testing, authentication, authorization, input validation, business logic, client-side | OWASP WSTG v4.2 |
| **PTES (Penetration Testing Execution Standard)** | Full-scope engagements (network + application) | Pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation, post-exploitation, reporting | ptes.org |
| **OWASP Mobile Testing Guide** | iOS and Android applications | Architecture, data storage, cryptography, authentication, network communication, platform interaction, code quality | OWASP MASTG |
| **NIST SP 800-115** | Government and regulated environments | Planning, discovery, attack, reporting | NIST 800-115 |
| **CIS Benchmarks** | Infrastructure and configuration review | Benchmark comparison against hardening standards | CIS |

**OWASP Top 10 coverage checklist (for web application tests):**

- [ ] A01: Broken Access Control (IDOR, privilege escalation, forced browsing)
- [ ] A02: Cryptographic Failures (weak TLS, plaintext secrets, poor key management)
- [ ] A03: Injection (SQLi, NoSQLi, OS command, LDAP, XPath)
- [ ] A04: Insecure Design (business logic flaws, missing threat modeling)
- [ ] A05: Security Misconfiguration (default creds, verbose errors, unnecessary features)
- [ ] A06: Vulnerable and Outdated Components (known CVEs, unpatched libraries)
- [ ] A07: Identification and Authentication Failures (brute force, weak passwords, session issues)
- [ ] A08: Software and Data Integrity Failures (insecure deserialization, unsigned updates)
- [ ] A09: Security Logging and Monitoring Failures (missing audit trails, no alerting)
- [ ] A10: Server-Side Request Forgery (SSRF to internal services, cloud metadata)

### Step 3: Establish Rules of Engagement

Define the operational boundaries and communication protocols for the engagement.

**Rules of engagement document:**

| Rule | Definition |
|------|-----------|
| **Testing window** | *e.g., Mon-Fri 09:00-17:00 UTC, or 24/7 for production-like staging* |
| **Notification contacts** | Primary: *name, phone, email*; Secondary: *name, phone, email* |
| **Emergency stop procedure** | Tester calls primary contact immediately; cease all testing; preserve evidence |
| **Allowed actions** | Vulnerability scanning, manual exploitation, credential stuffing (test accounts only), privilege escalation |
| **Prohibited actions** | Denial of service, data destruction, social engineering of employees, modification of production data, accessing real customer data |
| **Data handling** | All findings encrypted at rest; shared via secure channel only; destroyed 90 days post-engagement |
| **Third-party systems** | Do not test third-party SaaS without written authorization; report any unintentional access immediately |
| **Credential usage** | Use only provided test accounts; do not create unauthorized accounts; report any real credentials discovered |

**Legal and authorization checklist:**

- [ ] Written authorization signed by system owner with legal authority
- [ ] Scope document reviewed and signed by both parties
- [ ] Cloud provider notification completed (AWS penetration testing policy, etc.)
- [ ] Third-party authorization obtained for any shared infrastructure
- [ ] Non-disclosure agreement (NDA) executed
- [ ] Liability and indemnification clauses reviewed by legal
- [ ] Data processing agreement in place if tester will access personal data
- [ ] Insurance verification (professional liability / errors and omissions)

### Step 4: Plan Testing Phases

Structure the engagement into distinct phases with clear objectives and deliverables.

**Phase 1: Reconnaissance and Information Gathering**

| Activity | Technique | Tools | Output |
|----------|-----------|-------|--------|
| Passive reconnaissance | DNS enumeration, OSINT, certificate transparency | Subfinder, Amass, crt.sh, Shodan | Target inventory, subdomain list |
| Active reconnaissance | Port scanning, service enumeration, technology fingerprinting | Nmap, Masscan, Wappalyzer | Open port/service inventory, technology stack |
| Application mapping | Crawling, sitemap analysis, API endpoint discovery | Burp Suite, OWASP ZAP, Postman | Application sitemap, API endpoint catalog |
| Authentication enumeration | Login page analysis, registration flow, password policy | Manual testing, Burp Suite | Auth mechanism inventory, policy assessment |

**Phase 2: Vulnerability Identification**

| Activity | Technique | Tools | Output |
|----------|-----------|-------|--------|
| Automated scanning | Vulnerability scanning, DAST | Burp Scanner, Nuclei, Nikto | Automated findings (to be validated) |
| Manual testing | Business logic review, auth bypass attempts, injection testing | Burp Suite, sqlmap, custom scripts | Validated vulnerability list |
| Configuration review | Server hardening, TLS configuration, header analysis | testssl.sh, SecurityHeaders.com, manual | Configuration findings |
| Dependency analysis | Known CVE identification in third-party components | Snyk, OWASP Dependency-Check | Vulnerable component inventory |

**Phase 3: Exploitation and Proof of Concept**

| Activity | Technique | Tools | Output |
|----------|-----------|-------|--------|
| Vulnerability exploitation | Targeted exploitation of confirmed vulnerabilities | Burp Suite, Metasploit, custom PoCs | Exploitation evidence (screenshots, request/response) |
| Privilege escalation | Horizontal and vertical privilege escalation attempts | Manual testing, custom scripts | Privilege escalation paths documented |
| Chaining | Combine low-severity findings into higher-impact attack chains | Manual analysis | Attack chain narratives |
| Data access verification | Determine what data is accessible through exploited vulnerabilities | Manual testing | Data exposure evidence (redacted) |

**Phase 4: Post-Exploitation (if in scope)**

| Activity | Technique | Tools | Output |
|----------|-----------|-------|--------|
| Lateral movement | Pivot from compromised system to adjacent systems | SSH, RDP, cloud API calls | Lateral movement map |
| Persistence assessment | Identify mechanisms an attacker could use for persistence | Manual analysis | Persistence risk assessment |
| Data exfiltration simulation | Demonstrate ability to extract sensitive data (simulated) | Manual testing | Exfiltration path documentation |
| Detection assessment | Evaluate whether testing activities triggered security alerts | Coordination with SOC/SIEM team | Detection gap analysis |

**Phase 5: Cleanup and Verification**

- [ ] Remove all tester-created accounts and test data
- [ ] Delete all uploaded files, shells, or payloads
- [ ] Restore any modified configurations to original state
- [ ] Verify no persistent access mechanisms remain
- [ ] Confirm all testing artifacts are removed from target systems
- [ ] Document any changes that could not be reversed

### Step 5: Define Reporting Format

Establish the structure and standards for the final penetration test report.

**Finding severity classification:**

| Severity | CVSS Range | Description | Remediation SLA |
|----------|-----------|-------------|-----------------|
| **Critical** | 9.0 - 10.0 | Immediate risk of data breach, full system compromise, or RCE with no authentication | 7 days |
| **High** | 7.0 - 8.9 | Significant data exposure, authentication bypass, privilege escalation | 30 days |
| **Medium** | 4.0 - 6.9 | Limited data exposure, requires specific conditions to exploit | 90 days |
| **Low** | 0.1 - 3.9 | Minor information disclosure, defense-in-depth improvements | 180 days |
| **Informational** | 0.0 | Best practice recommendations, no direct security impact | Backlog |

**Individual finding template:**

```
### [SEVERITY] Finding Title

**ID:** PT-YYYY-NNN
**CVSS Score:** X.X (Vector string)
**Affected Asset:** [URL, IP, component]
**Category:** [OWASP Top 10 category or CWE]

**Description:**
[Clear explanation of the vulnerability and why it matters]

**Steps to Reproduce:**
1. [Step-by-step reproduction instructions]
2. [Include specific requests, parameters, payloads]
3. [Include screenshots or request/response pairs]

**Impact:**
[What an attacker could achieve by exploiting this vulnerability]

**Recommendation:**
[Specific, actionable remediation guidance with code examples where applicable]

**References:**
- [CWE link]
- [OWASP reference]
- [Vendor advisory if applicable]
```

### Step 6: Remediation Tracking

Establish a process for tracking remediation of identified findings.

**Remediation tracker:**

| Finding ID | Severity | Title | Owner | Remediation SLA | Status | Retest Date | Retest Result |
|-----------|----------|-------|-------|-----------------|--------|-------------|---------------|
| PT-2026-001 | Critical | SQL Injection in search API | Backend Team | 7 days | Remediated | *date* | Pass |
| PT-2026-002 | High | Broken access control on admin endpoints | API Team | 30 days | In Progress | *date* | Pending |
| PT-2026-003 | Medium | Missing rate limiting on authentication | Platform Team | 90 days | Not Started | *date* | Pending |

**Remediation workflow:**

1. **Finding delivered** — Tester shares finding with development/security team
2. **Triage and assign** — Team confirms finding, assigns owner, sets target date
3. **Remediate** — Owner implements fix following the provided recommendation
4. **Verify fix** — Owner validates fix in staging with the reproduction steps
5. **Request retest** — Owner requests tester to verify remediation
6. **Retest** — Tester confirms vulnerability is resolved and no regressions introduced
7. **Close** — Finding marked as remediated with retest evidence

## Output Format

Present the test plan as a structured document:

```
## Penetration Test Plan

### Engagement Overview
- Target: [application, system, or network]
- Type: [black-box / grey-box / white-box]
- Methodology: [OWASP / PTES / NIST]
- Testing window: [dates and hours]
- Environment: [production / staging / dedicated test]

### Scope
- In-scope and out-of-scope tables

### Rules of Engagement
- Authorized actions, prohibited actions, emergency contacts

### Testing Phases
- Phase breakdown with activities, tools, and expected outputs

### Reporting Standards
- Severity classification, finding template, deliverable timeline

### Remediation Process
- SLA definitions, tracking process, retest procedures

### Authorization
- Sign-off from system owner and legal
```

## Quality Checklist

- [ ] Scope explicitly lists both in-scope and out-of-scope targets with no ambiguity
- [ ] Rules of engagement include emergency stop procedures and contact information
- [ ] Methodology is appropriate for the target type (web, mobile, network, cloud)
- [ ] Testing phases are sequenced logically with clear entry and exit criteria
- [ ] Severity classification uses an industry-standard scoring system (CVSS)
- [ ] Reporting format includes reproduction steps sufficient for developers to verify and fix
- [ ] Remediation SLAs are realistic and aligned with organizational capacity
- [ ] Legal authorization and cloud provider notifications are completed before testing begins
- [ ] Data handling and destruction requirements are clearly defined
- [ ] Cleanup procedures ensure no tester artifacts remain on target systems

## Edge Cases

- For production testing: require explicit written authorization; test during low-traffic windows; have rollback plans; coordinate with on-call teams for immediate incident response if needed
- For API-only targets: supplement automated scanning with thorough manual testing of business logic, authorization, and rate limiting which scanners frequently miss
- For cloud infrastructure tests: verify cloud provider penetration testing policies (AWS, GCP, Azure each have specific requirements); include IAM and resource policy review
- For microservices architectures: test inter-service authentication and authorization, not just the external API gateway; verify service mesh security configurations
- For CI/CD pipeline testing: include supply chain attack scenarios (dependency confusion, pipeline poisoning); test secret management and build artifact integrity
- For retests after remediation: verify the specific fix does not introduce regressions; test bypass variations of the original vulnerability; confirm fix is deployed to all affected environments
