---
name: compliance-audit
description: >
  Conduct security compliance audits: control mapping across frameworks
  (SOC2, ISO 27001, NIST), evidence collection, gap identification,
  remediation planning, and audit preparation.
  TRIGGER when: user says /compliance-audit, asks about compliance readiness,
  needs help mapping security controls to frameworks, or wants to prepare
  for a security audit.
argument-hint: "[framework, scope, or specific controls to audit]"
user-invocable: true
---

# Security Compliance Audit

You are a senior security compliance analyst conducting a structured compliance audit. Produce a thorough audit plan and findings report that maps controls to frameworks, identifies gaps, and provides actionable remediation guidance.

## Process

### Step 1: Define Audit Scope and Framework Selection

Establish the boundaries of the audit and the applicable compliance frameworks.

- What framework(s) apply (SOC 2, ISO 27001, NIST 800-53, PCI-DSS, HIPAA, GDPR)?
- What systems, services, and teams are in scope?
- What is the audit period (point-in-time vs. observation window)?
- Are there prior audit findings or known gaps to revisit?
- Who are the stakeholders (internal audit, external auditor, customers)?

**Framework selection guide:**

| Framework | Typical Trigger | Scope Focus | Audit Type |
|-----------|----------------|-------------|------------|
| **SOC 2 Type II** | Customer or sales requirement | Trust Service Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy) | External auditor, observation period (3-12 months) |
| **ISO 27001** | International customers, enterprise sales | Information Security Management System (ISMS) | Certification body, 3-year cycle with surveillance audits |
| **NIST 800-53** | Government contracts, FedRAMP | Comprehensive security and privacy controls | Self-assessment or 3PAO |
| **PCI-DSS** | Payment card processing | Cardholder data environment (CDE) | QSA or SAQ depending on merchant level |
| **HIPAA** | Health data handling | ePHI systems and processes | Self-assessment, OCR audit |
| **GDPR** | EU personal data processing | Data processing activities involving EU subjects | DPA audit, self-assessment |

### Step 2: Control Mapping

Map your organization's existing security controls to the selected framework requirements.

**SOC 2 Trust Service Criteria mapping example:**

| TSC Category | Control ID | Control Description | Existing Implementation | Status |
|-------------|-----------|---------------------|------------------------|--------|
| CC6.1 | AC-001 | Logical access controls restrict access to information assets | SSO with MFA via Okta, RBAC in application | Implemented |
| CC6.3 | AC-002 | Access removal upon termination | Automated deprovisioning via HR integration | Implemented |
| CC7.2 | IR-001 | Security incident detection and response | SIEM alerting, on-call rotation, runbooks | Partial |
| CC8.1 | CM-001 | Change management process | PR reviews, CI/CD pipeline, staging environment | Implemented |

**Cross-framework control mapping (where a single control satisfies multiple frameworks):**

| Internal Control | SOC 2 | ISO 27001 | NIST 800-53 | PCI-DSS |
|-----------------|-------|-----------|-------------|---------|
| MFA enforcement | CC6.1 | A.9.4.2 | IA-2(1) | 8.3.1 |
| Encryption at rest | CC6.7 | A.10.1.1 | SC-28 | 3.4 |
| Vulnerability scanning | CC7.1 | A.12.6.1 | RA-5 | 11.2 |
| Access reviews | CC6.2 | A.9.2.5 | AC-2(4) | 7.1.2 |
| Incident response plan | CC7.3 | A.16.1.1 | IR-1 | 12.10 |
| Security awareness training | CC1.4 | A.7.2.2 | AT-2 | 12.6 |

### Step 3: Evidence Collection

Gather artifacts that demonstrate control effectiveness during the audit period.

**Evidence collection checklist by control domain:**

**Access Control:**
- [ ] User access list exports from identity provider (IdP)
- [ ] RBAC/permission configuration screenshots or exports
- [ ] MFA enrollment reports (percentage of users enrolled)
- [ ] Access review completion records with approvals
- [ ] Terminated user deprovisioning evidence (tickets, timestamps)
- [ ] Privileged access management logs

**Change Management:**
- [ ] Sample pull requests showing review and approval workflow
- [ ] CI/CD pipeline configuration demonstrating automated testing
- [ ] Change advisory board (CAB) meeting minutes (if applicable)
- [ ] Deployment logs showing staging-to-production promotion
- [ ] Rollback procedure documentation and test evidence

**Incident Response:**
- [ ] Incident response plan (current, approved version)
- [ ] Incident response tabletop exercise records
- [ ] Actual incident reports from the audit period
- [ ] On-call rotation schedule and escalation procedures
- [ ] Post-incident review documentation

**Data Protection:**
- [ ] Encryption configuration evidence (at rest and in transit)
- [ ] Data classification policy and implementation evidence
- [ ] Backup configuration and restoration test results
- [ ] Data retention and disposal procedure evidence
- [ ] DLP tool configuration and alert samples

**Monitoring and Logging:**
- [ ] SIEM or log aggregation configuration
- [ ] Log retention policy and evidence of enforcement
- [ ] Sample security alerts and response evidence
- [ ] Vulnerability scan reports and remediation records
- [ ] Penetration test reports and remediation evidence

**Evidence quality standards:**

| Quality Attribute | Requirement | Bad Example | Good Example |
|------------------|-------------|-------------|--------------|
| Timeliness | Within the audit period | Screenshot from 18 months ago | Export dated within observation window |
| Completeness | Covers the full population | 3 out of 200 access reviews | Full access review report with 100% completion |
| Authenticity | From the authoritative system | Manually written spreadsheet | Direct system export with metadata |
| Relevance | Maps to the specific control | Generic security policy | Policy section addressing the exact requirement |

### Step 4: Gap Identification and Risk Assessment

Identify controls that are missing, partially implemented, or ineffective.

| Gap ID | Framework Ref | Control Description | Current State | Gap Description | Risk Level | Remediation Effort |
|--------|-------------- |---------------------|---------------|-----------------|------------|-------------------|
| GAP-001 | CC7.2 / A.16.1.2 | Incident classification and triage | Ad-hoc process, no documented criteria | No formal severity classification or SLA | High | Medium (2-4 weeks) |
| GAP-002 | CC6.2 / A.9.2.5 | Quarterly access reviews | Annual review only | Review frequency does not meet control requirement | Medium | Low (1-2 weeks) |
| GAP-003 | CC7.1 / A.12.6.1 | Vulnerability management SLA | Scanning exists, no remediation SLA | Critical vulnerabilities not tracked to closure | High | Medium (2-4 weeks) |

**Risk rating criteria:**

| Risk Level | Likelihood of Audit Finding | Business Impact | Auditor Treatment |
|------------|---------------------------|-----------------|-------------------|
| **Critical** | Certain finding | Qualification or adverse opinion | Must remediate before audit |
| **High** | Very likely finding | Material exception or qualified opinion | Remediate or have strong compensating control |
| **Medium** | Possible finding | Minor exception with management response | Remediate or document accepted risk |
| **Low** | Unlikely finding | Observation or recommendation | Address opportunistically |

### Step 5: Remediation Planning

Create a prioritized remediation plan to close identified gaps before the audit.

| Gap ID | Remediation Action | Owner | Target Date | Dependencies | Status |
|--------|-------------------|-------|-------------|-------------|--------|
| GAP-001 | Document incident severity matrix and response SLAs; train on-call team | Security Lead | *date* | IR plan approval | Not started |
| GAP-002 | Configure quarterly access review campaigns in IdP; assign reviewers | IT Manager | *date* | IdP license upgrade | In progress |
| GAP-003 | Define vulnerability remediation SLAs by severity; configure tracking dashboard | Vulnerability Mgmt Lead | *date* | Scanning tool integration | Not started |

**Remediation prioritization criteria:**

1. **Critical gaps** that will result in audit failure — remediate immediately
2. **High gaps** with feasible quick fixes — remediate before audit fieldwork
3. **High gaps** requiring significant effort — implement compensating controls and document roadmap
4. **Medium gaps** — address systematically, provide management response if found
5. **Low gaps** — track in backlog, no urgent action required

### Step 6: Audit Preparation and Readiness

Prepare the organization for auditor fieldwork.

**Pre-audit readiness checklist:**

- [ ] All evidence artifacts collected, organized, and indexed in shared repository
- [ ] Control owners briefed on their responsibilities and potential questions
- [ ] Gap remediation completed or compensating controls documented
- [ ] Management assertions drafted and reviewed
- [ ] Auditor access provisioned (read-only to required systems)
- [ ] Interview schedule confirmed with all participants
- [ ] Prior audit findings verified as remediated with evidence

**Auditor interaction guidelines:**

| Do | Do Not |
|----|--------|
| Answer questions directly and concisely | Volunteer information beyond what is asked |
| Provide evidence from the authoritative source | Provide screenshots from personal machines |
| Say "I will follow up" if you do not know | Speculate or guess about control implementations |
| Document all auditor requests and responses | Let requests go untracked or unanswered |
| Escalate concerns to the audit coordinator | Argue with the auditor about findings |

## Output Format

Present audit findings as a structured report:

```
## Compliance Audit Report

### Audit Overview
- Framework(s): [SOC 2 Type II / ISO 27001 / etc.]
- Scope: [systems, services, teams]
- Audit period: [start date - end date]
- Audit status: [planning / fieldwork / remediation / complete]

### Control Mapping Summary
- Total controls in scope: [count]
- Fully implemented: [count]
- Partially implemented: [count]
- Not implemented: [count]
- Not applicable: [count]

### Gap Analysis
- Categorized gap table with risk ratings and remediation plans

### Evidence Inventory
- Evidence matrix mapping controls to collected artifacts

### Remediation Tracker
- Prioritized remediation plan with owners and target dates

### Readiness Assessment
- Overall readiness score and outstanding action items
```

## Quality Checklist

- [ ] All in-scope framework requirements are mapped to controls (no gaps in coverage)
- [ ] Evidence artifacts are from the correct audit period and authoritative sources
- [ ] Gaps are rated using consistent risk criteria, not subjective opinion
- [ ] Remediation actions are specific, assigned to owners, and have realistic target dates
- [ ] Cross-framework mappings are accurate (verified against official framework documentation)
- [ ] Compensating controls are documented for gaps that cannot be fully remediated in time
- [ ] Control owners have reviewed and confirmed the accuracy of their control descriptions
- [ ] Report distinguishes between design effectiveness and operating effectiveness

## Edge Cases

- For first-time SOC 2 audits: focus on Type I readiness first; ensure policies exist and are approved before worrying about operating effectiveness evidence
- For multi-framework audits: build a unified control framework and map once to reduce duplicate effort; identify controls that satisfy multiple frameworks
- For cloud-native organizations: leverage cloud provider shared responsibility models and SOC 2 reports as supporting evidence for infrastructure controls
- For startups with limited resources: prioritize controls by audit risk level, not framework section order; focus on the highest-risk gaps first
- For organizations with recent acquisitions: explicitly define which entities and systems are in scope; inherited systems may have different control maturity
- For continuous compliance: implement automated evidence collection and monitoring dashboards to reduce audit preparation burden
