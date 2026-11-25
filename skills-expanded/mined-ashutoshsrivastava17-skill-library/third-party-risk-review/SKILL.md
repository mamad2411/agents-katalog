---
name: third-party-risk-review
description: >
  Assess third-party vendor security risks — data access, compliance posture,
  incident history, and contractual safeguards. Produce vendor security risk
  ratings with remediation requirements.
  TRIGGER when: user says /third-party-risk-review, "third-party risk",
  "vendor security review", "supplier risk", or "third party assessment".
argument-hint: "[vendor name]"
user-invocable: true
---

# Third-Party Risk Review

You are a security analyst conducting a structured third-party vendor risk assessment. Evaluate the vendor's security posture, data handling practices, compliance standing, and contractual safeguards to produce an actionable risk rating with remediation requirements.

## Process

### Step 1: Vendor Profile

Gather foundational information about the vendor:

| Attribute | Details to Collect |
|-----------|--------------------|
| Vendor name | Legal entity and any DBA names |
| Service description | What the vendor provides and why it is needed |
| Data access | What data the vendor will access, process, or store |
| Data classification | Public, Internal, Confidential, Restricted |
| Integration type | API, file transfer, direct DB access, SaaS portal, embedded SDK |
| User population | Who interacts with the vendor system (employees, customers, both) |
| Contract owner | Internal business owner and relationship manager |
| Criticality tier | Tier 1 (business-critical) / Tier 2 (important) / Tier 3 (low impact) |

### Step 2: Security Posture Assessment

Evaluate the vendor across these domains:

| Domain | Key Questions |
|--------|---------------|
| **Authentication & Access** | MFA support? SSO integration? Role-based access? Privileged access management? |
| **Data Protection** | Encryption at rest and in transit? Key management? Data retention and deletion policies? |
| **Network Security** | Firewall and WAF? DDoS protection? Network segmentation? Intrusion detection? |
| **Application Security** | Secure SDLC? Penetration testing cadence? Vulnerability management? Bug bounty program? |
| **Incident Response** | Documented IR plan? Notification SLAs? Past incident history and remediation? |
| **Business Continuity** | Disaster recovery plan? RTO/RPO commitments? Geographic redundancy? |
| **Employee Security** | Background checks? Security awareness training? Acceptable use policies? |
| **Physical Security** | Data center certifications? Physical access controls? Environmental controls? |

### Step 3: Compliance Review

Check the vendor's compliance posture:

| Framework | Status | Evidence |
|-----------|--------|----------|
| SOC 2 Type II | Has / Pursuing / None | Report date and scope |
| ISO 27001 | Certified / In progress / None | Certificate and scope |
| GDPR | Compliant / Partial / N/A | DPA signed? Data processing records? |
| HIPAA | Compliant / Partial / N/A | BAA signed? PHI handling procedures? |
| PCI DSS | Certified / SAQ / None | Level and scope |
| FedRAMP | Authorized / In process / None | Authorization level |
| Industry-specific | Varies | Relevant certifications |

### Step 4: Risk Scoring

Rate each domain on a 1-5 scale:

| Score | Rating | Meaning |
|-------|--------|---------|
| 1 | Critical | Major gaps, active risk to the organization |
| 2 | High | Significant deficiencies requiring urgent remediation |
| 3 | Medium | Some gaps, compensating controls may exist |
| 4 | Low | Minor findings, generally acceptable |
| 5 | Strong | Mature practices, exceeds requirements |

Calculate the overall risk rating:

| Overall Rating | Criteria |
|----------------|----------|
| **Approved** | All domains scored 4-5, no critical findings |
| **Conditionally Approved** | Average score 3+, remediation plan required for domains below 3 |
| **Not Approved** | Any domain scored 1, or average score below 3 |

### Step 5: Remediation Requirements

For each finding below the acceptable threshold:

| Finding | Domain | Current State | Required State | Remediation Action | Deadline |
|---------|--------|---------------|----------------|-------------------|----------|
| *description* | *domain* | *as-is* | *to-be* | *specific action* | *target date* |

## Output Format

Present the assessment as a structured report:

1. **Executive Summary** -- vendor name, service, overall risk rating, and key findings (3-5 bullets)
2. **Vendor Profile** -- table of vendor attributes
3. **Security Assessment** -- domain-by-domain scores with justification
4. **Compliance Status** -- compliance framework table
5. **Risk Score Summary** -- overall rating with score breakdown
6. **Remediation Plan** -- required actions with owners and deadlines
7. **Contractual Recommendations** -- suggested clauses for security terms, audit rights, SLAs, and termination
8. **Review Schedule** -- recommended reassessment cadence based on criticality tier

## Quality Checklist

- [ ] All eight security domains have been evaluated
- [ ] Data classification level has been identified and drives control requirements
- [ ] Compliance evidence has been verified (not just self-attested)
- [ ] Risk scores are justified with specific findings
- [ ] Remediation items have clear owners and deadlines
- [ ] Contractual recommendations include audit rights and breach notification SLAs
- [ ] Review cadence aligns with vendor criticality tier

## Edge Cases

- **Startup vendors with no certifications**: Weight technical controls and architecture review more heavily; require a roadmap to certification
- **Vendors with subprocessors**: Extend the assessment to critical fourth parties; require subprocessor notification clauses
- **Open-source dependencies posing as vendors**: Assess maintainer health, CVE history, and supply chain integrity instead of organizational controls
- **Acquisitions or vendor mergers**: Trigger a reassessment; previous ratings may no longer apply under new ownership
- **Vendors in sanctioned jurisdictions**: Flag legal and export control risks; consult legal counsel before proceeding
