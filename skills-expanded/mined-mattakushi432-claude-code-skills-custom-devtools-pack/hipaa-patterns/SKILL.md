---
name: hipaa-patterns
description: "When to activate: HIPAA, PHI, protected health information, healthcare data, covered entity, business associate, BAA, health records, medical data, ePHI"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: compliance
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# HIPAA Compliance Patterns

> **Disclaimer**: This is informational only and does not constitute legal or compliance advice. Engage qualified HIPAA counsel and compliance experts for your specific situation.

## Who Must Comply

### Covered Entities (CEs)
- Health plans (insurance, HMOs, employer-sponsored)
- Healthcare clearinghouses
- Healthcare providers who transmit health info electronically

### Business Associates (BAs)
Any person/entity that performs functions on behalf of a CE that involve creating, receiving, maintaining, or transmitting PHI.

**Examples**: EHR vendors, cloud storage providers, billing companies, coding services, IT support with PHI access, analytics firms processing health data, lawyers reviewing medical records.

**Sub-Business Associates**: BAs that engage subcontractors who access PHI must have BAAs with them too.

## Protected Health Information (PHI)

Individually identifiable health information related to:
- Past, present, or future physical or mental health
- Healthcare provision
- Payment for healthcare

### 18 HIPAA Identifiers
1. Names
2. Geographic data (smaller than state, including zip codes)
3. Dates (except year) related to individual
4. Phone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers
14. Web URLs
15. IP addresses
16. Biometric identifiers (fingerprints, voice)
17. Full-face photos
18. Any other unique identifying number or code

**ePHI**: Electronic PHI — same definition, applies to Security Rule.

### De-Identification Methods
- **Expert determination**: Statistical expert certifies very small re-identification risk
- **Safe harbor**: Remove all 18 identifiers AND no actual knowledge of re-identification

## HIPAA Rules

### Privacy Rule
Controls use and disclosure of PHI.

**Permitted Uses Without Authorization**:
- Treatment, payment, healthcare operations (TPO)
- Public health activities
- Victims of abuse/neglect
- Health oversight activities
- Judicial/administrative proceedings
- Law enforcement (limited)
- Research (with IRB waiver or de-identification)
- Serious threat to health/safety

**Minimum Necessary Standard**:
- Disclose only the minimum PHI necessary for the purpose
- Implement policies for routine disclosures
- Review non-routine requests individually

**Patient Rights**:
- [ ] Access their PHI (within 30 days, extendable to 60)
- [ ] Request amendment
- [ ] Accounting of disclosures
- [ ] Request restrictions (must honor if CE doesn't need for TPO and patient pays out-of-pocket)
- [ ] Request confidential communications
- [ ] Complain to CE and HHS

### Security Rule
Applies to ePHI only.

#### Administrative Safeguards
- [ ] Security officer designated
- [ ] Workforce training on security policies
- [ ] Access management procedures (granting, modifying, terminating)
- [ ] Security incident response procedures
- [ ] Contingency plan (BCP/DR)
- [ ] Evaluation of security measures (annual risk analysis)
- [ ] Business Associate contracts

#### Physical Safeguards
- [ ] Facility access controls (badge, key, visitor log)
- [ ] Workstation use policies (screen locks, clean desk)
- [ ] Workstation security (physical security of devices)
- [ ] Device and media controls (encryption, disposal, reuse procedures)

#### Technical Safeguards
- [ ] Access controls (unique user IDs, emergency access procedure, auto-logoff, encryption/decryption)
- [ ] Audit controls (hardware and software activity logs)
- [ ] Integrity controls (authentication mechanisms, checksums)
- [ ] Transmission security (encryption in transit, TLS 1.2+)

### Breach Notification Rule

**Breach Definition**: Impermissible use/disclosure of unsecured PHI that compromises privacy or security.

**Unsecured PHI**: PHI not rendered unusable, unreadable, or indecipherable through encryption or destruction.

#### Risk Assessment (4 Factors)
1. Nature and extent of PHI involved (identifiers + likelihood of re-identification)
2. Who used or accessed the PHI
3. Whether PHI was actually acquired or viewed
4. Extent to which risk has been mitigated

Low probability of compromise → not a breach (document assessment).

#### Notification Timeline
- **Individuals**: Within 60 days of discovery
- **HHS**: 
  - 500+ affected: Simultaneously with individual notification
  - <500 affected: Annual log, submitted within 60 days of calendar year end
- **Media**: 500+ residents of a state/jurisdiction → notify prominent media outlets

#### Notification Content
- Description of the breach
- Types of PHI involved
- Steps individuals should take to protect themselves
- CE's steps to investigate and mitigate
- Contact information

## Business Associate Agreements (BAAs)

**Required before** sharing PHI with any BA.

### Mandatory BAA Elements
- [ ] Permitted uses and disclosures of PHI
- [ ] Prohibition on non-permitted uses/disclosures
- [ ] Appropriate safeguards requirement
- [ ] Reporting breaches to CE
- [ ] Compliance with minimum necessary standard
- [ ] Making PHI available for patient access requests
- [ ] Subcontractor requirements (flow-down)
- [ ] Return or destroy PHI at termination
- [ ] Government access for compliance purposes

### BAA with Cloud Providers
AWS, GCP, Azure, and many SaaS vendors offer standard BAAs. Request from their sales/legal team. Note:
- IaaS providers operate under "conduit" or full BA model depending on access
- Review what the BAA covers (region, services)
- Some services may be excluded from BAA coverage

## Technical Implementation Checklist

### Encryption
- [ ] Data at rest: AES-256 minimum
- [ ] Data in transit: TLS 1.2+ (prefer TLS 1.3)
- [ ] Key management: Hardware security modules (HSM) for critical keys
- [ ] Device encryption: Full-disk encryption on all laptops/mobile devices
- [ ] Backup encryption: Same standards as production

### Access Control
- [ ] Unique user accounts (no shared accounts)
- [ ] MFA for all remote access
- [ ] Role-based access control (RBAC)
- [ ] Automatic session timeout (15–30 minutes)
- [ ] Privileged access management (PAM) for admin accounts
- [ ] Access review quarterly minimum

### Audit Logging
- [ ] All access to PHI logged (read and write)
- [ ] Login/logout events
- [ ] Failed authentication attempts
- [ ] Configuration changes
- [ ] Log integrity protection (tamper-evident)
- [ ] Retention: 6 years minimum
- [ ] Regular log review procedures

### Vulnerability Management
- [ ] Monthly vulnerability scanning
- [ ] Annual penetration testing
- [ ] Patch management SLA (critical: 30 days, high: 60 days)
- [ ] Third-party component inventory (SBOMs)

## Risk Analysis Requirements

HIPAA requires a documented, thorough, accurate, organization-wide risk analysis:

1. **Scope**: All ePHI created, received, maintained, or transmitted
2. **Threat identification**: Natural, human, environmental
3. **Vulnerability identification**: Technical, physical, administrative
4. **Control assessment**: Current security measures
5. **Likelihood determination**: Probability of threat exploiting vulnerability
6. **Impact determination**: Magnitude of harm if PHI compromised
7. **Risk level**: Combination of likelihood and impact
8. **Risk treatment**: Accept, mitigate, transfer, avoid
9. **Documentation**: Written, retained 6 years
10. **Review**: Annual or on significant change

## Common HIPAA Violations and Penalties

| Tier | Culpability | Per Violation | Annual Cap |
|------|-------------|---------------|------------|
| 1 | Unknowing | $100–$50,000 | $25,000 |
| 2 | Reasonable cause | $1,000–$50,000 | $100,000 |
| 3 | Willful neglect, corrected | $10,000–$50,000 | $250,000 |
| 4 | Willful neglect, uncorrected | $50,000 | $1,500,000 |

State AGs can also bring civil actions. Criminal penalties apply for knowing violations.

## Quick Compliance Checklist

- [ ] Covered entity / BA determination completed
- [ ] Privacy policies and procedures documented
- [ ] Security policies and procedures documented
- [ ] Notice of Privacy Practices (NPP) published
- [ ] BAAs signed with all business associates
- [ ] Workforce training completed and documented
- [ ] Security officer designated
- [ ] Risk analysis completed and documented
- [ ] Audit logs enabled and retained 6 years
- [ ] Encryption implemented (at rest and in transit)
- [ ] Breach response procedure documented and tested
- [ ] Patient rights request procedures implemented
- [ ] Annual policy review scheduled
