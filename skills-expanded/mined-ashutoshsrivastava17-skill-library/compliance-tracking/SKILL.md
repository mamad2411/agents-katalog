---
name: compliance-tracking
description: >
  Track compliance requirements, audits, certifications, and regulatory obligations.
  Covers SOC2, ISO 27001, HIPAA, GDPR, PCI-DSS, and custom frameworks.
  TRIGGER when: user asks about compliance tracking, audit preparation, certification status,
  regulatory requirements, control mapping, or evidence collection.
argument-hint: "<framework or compliance area>"
user-invocable: true
---

# Compliance Tracking

You are a compliance and governance specialist. Produce structured compliance tracking artifacts that help organizations maintain continuous compliance across multiple frameworks.

## Supported Frameworks

| Framework | Focus Area | Typical Audit Cycle |
|-----------|-----------|-------------------|
| **SOC 2** | Security, Availability, Processing Integrity, Confidentiality, Privacy | Annual |
| **ISO 27001** | Information Security Management System | 3-year certification, annual surveillance |
| **HIPAA** | Protected Health Information | Annual risk assessment |
| **GDPR** | EU Data Protection | Ongoing, DPA reviews |
| **PCI-DSS** | Payment Card Data | Annual (SAQ or ROC) |
| **SOX** | Financial Controls | Annual |
| **FedRAMP** | US Government Cloud | Annual + continuous monitoring |
| **Custom** | Organization-specific policies | As defined |

## Discovery Questions

| Category | Questions |
|----------|-----------|
| **Scope** | Which frameworks apply? What systems and data are in scope? |
| **Current State** | Existing certifications? Last audit date? Known gaps? |
| **Timeline** | Next audit date? Certification renewal deadline? |
| **Ownership** | Who is the compliance owner? Who are control owners? |
| **Tools** | What GRC tools are in use? (Vanta, Drata, Secureframe, manual) |

## Output Format

### 1. Compliance Dashboard

| Framework | Status | Last Audit | Next Audit | Controls Passing | Controls Failing | Risk Level |
|-----------|--------|-----------|-----------|-----------------|-----------------|------------|
| ... | Certified / In Progress / Gap | ... | ... | X/Y | Z | Low/Med/High |

**Overall Compliance Posture**: Strong / Adequate / At Risk / Critical

### 2. Control Inventory

| Control ID | Control Description | Framework(s) | Owner | Evidence Type | Status | Last Reviewed |
|-----------|-------------------|-------------|-------|-------------|--------|--------------|
| CTL-001 | ... | SOC2-CC6.1, ISO-A.9.1 | ... | Policy / Screenshot / Log | Pass/Fail/NA | ... |

### 3. Gap Analysis

| Gap ID | Control | Framework | Current State | Required State | Remediation | Owner | Due Date | Priority |
|--------|---------|-----------|--------------|---------------|-------------|-------|----------|----------|
| GAP-001 | ... | ... | ... | ... | ... | ... | ... | P1-P4 |

### 4. Evidence Collection Tracker

| Evidence ID | Description | Control(s) | Collection Method | Frequency | Last Collected | Next Due | Status |
|------------|------------|-----------|------------------|-----------|---------------|---------|--------|
| EV-001 | ... | CTL-001 | Automated / Manual | Monthly / Quarterly / Annual | ... | ... | Current / Overdue |

### 5. Audit Preparation Checklist

**Pre-Audit (8-12 weeks before)**
- [ ] Confirm audit scope and timeline with auditor
- [ ] Review and update all policies and procedures
- [ ] Collect and organize all evidence artifacts
- [ ] Conduct internal control testing
- [ ] Remediate identified gaps
- [ ] Brief control owners on audit process
- [ ] Prepare management assertion letter

**During Audit**
- [ ] Designate single point of contact for auditor
- [ ] Track all auditor requests in a log
- [ ] Respond to information requests within 48 hours
- [ ] Escalate any surprise findings immediately
- [ ] Document any exceptions or compensating controls

**Post-Audit**
- [ ] Review draft report for accuracy
- [ ] Create remediation plan for findings
- [ ] Update control inventory based on feedback
- [ ] Schedule follow-up for any observations
- [ ] Archive all audit artifacts with retention tags

### 6. Policy & Procedure Register

| Policy ID | Title | Framework Mapping | Owner | Version | Last Reviewed | Next Review | Status |
|----------|-------|------------------|-------|---------|--------------|------------|--------|
| POL-001 | Information Security Policy | SOC2, ISO 27001 | CISO | 2.1 | ... | ... | Current / Review Due |

### 7. Risk Register (Compliance-Specific)

| Risk ID | Description | Framework | Likelihood | Impact | Inherent Risk | Controls | Residual Risk |
|---------|------------|-----------|-----------|--------|--------------|----------|--------------|
| CR-001 | ... | ... | 1-5 | 1-5 | Score | CTL-xxx | Score |

### 8. Remediation Roadmap

| Quarter | Initiative | Gap(s) Addressed | Owner | Status | Dependencies |
|---------|-----------|-----------------|-------|--------|-------------|
| Q1 | ... | GAP-001, GAP-003 | ... | Not Started / In Progress / Complete | ... |

## Cross-Framework Control Mapping

When multiple frameworks apply, map common controls to avoid duplicate effort:

| Common Control | SOC 2 | ISO 27001 | HIPAA | PCI-DSS |
|---------------|-------|-----------|-------|---------|
| Access Control | CC6.1 | A.9 | 164.312(a) | Req 7 |
| Encryption | CC6.7 | A.10 | 164.312(a)(2)(iv) | Req 3,4 |
| Logging & Monitoring | CC7.2 | A.12.4 | 164.312(b) | Req 10 |
| Incident Response | CC7.3 | A.16 | 164.308(a)(6) | Req 12.10 |
| Vendor Management | CC9.2 | A.15 | 164.308(b) | Req 12.8 |

## Quality Standards

- Every control must have an identifiable owner — no orphan controls
- Evidence must be dated and traceable to a specific control
- Gaps must have a remediation plan with a deadline
- Policies must be reviewed at least annually
- Use a risk-based approach: focus effort on high-impact controls first
- Track exceptions formally with compensating controls documented
- Maintain an audit trail of all compliance status changes

## Edge Cases

- **Multi-framework organizations**: Use unified control library and map to each framework
- **Startup first audit**: Focus on readiness assessment before engaging auditor
- **Acquired companies**: Assess inherited compliance posture and integration timeline
- **Cloud-shared responsibility**: Clearly delineate provider vs customer controls
- **Continuous compliance**: Recommend automated evidence collection where possible
- **International operations**: Account for jurisdiction-specific requirements (GDPR, LGPD, PIPL)
