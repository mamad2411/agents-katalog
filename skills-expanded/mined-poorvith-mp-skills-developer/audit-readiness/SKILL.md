---
name: audit-readiness
last_reviewed: 2026-09-06
group: Security
description: >-
  Prepare for SOC 2, ISO 27001, HIPAA or PCI-DSS: control mapping, gap analysis and evidence. Use
  when preparing evidence and technical controls for SOC 2 or ISO 27001.
---

# Audit Readiness

Technical compliance is an engineering operational discipline, not a legal exercise. Auditors evaluate inspectable technical artifacts: continuous audit logs, automated configuration policies, branch protection rules, encrypted storage configurations, and role-based access controls (RBAC).

## 1. Multi-Framework Technical Control Specifications

### A. SOC 2 Type II (Trust Services Criteria)
- **CC6.1 / CC6.3 (Logical Access & MFA)**: Single Sign-On (SSO) enforced via Okta or Google Workspace; mandatory hardware/TOTP MFA; automated deprovisioning via SCIM within 24 hours of employee departure.
- **CC6.6 / CC6.8 (Network & Endpoint Protection)**: Mobile Device Management (MDM via Jamf/Kandji) enforcing FileVault/BitLocker full-disk encryption and automated OS patching; infrastructure deployed strictly in private VPC subnets.
- **CC7.2 / CC7.3 (Change Management)**: GitHub branch protection enforcing mandatory peer reviews, passing CI/CD pipelines, and linear commit histories on production branches. No direct commits to `main`.
- **CC8.1 (Vulnerability & Patch Management)**: Automated dependency scanning (Dependabot/Snyk) running in CI; critical CVEs patched within 7 days, high within 30 days.

### B. ISO/IEC 27001:2022 (Annex A Controls)
- **Control A.5.15 (Access Control)**: Formal quarterly user access reviews (UAR) of GitHub, AWS, and production database permissions with signed audit sign-offs.
- **Control A.8.8 (Management of Technical Vulnerabilities)**: Continuous infrastructure vulnerability scanning via AWS Inspector or Trivy, tracked in Jira/Linear with SLA burn-down charts.
- **Control A.8.20 / A.8.24 (Network Security & Cryptography)**: TLS 1.3 enforced for public endpoints; TLS 1.2 minimum; cipher suites restricted to forward-secret AEAD ciphers; AES-256 for EBS, S3, and RDS storage volumes.

### C. HIPAA Security Rule (45 CFR Part 164)
- **Business Associate Agreements (BAA)**: Signed BAAs executed with all cloud service providers and SaaS platforms touching electronic Protected Health Information (ePHI).
- **Technical Safeguards (§ 164.312)**:
  - *Access Control*: Unique user IDs, automatic session timeout after 15 minutes of inactivity.
  - *Audit Controls*: Centralized immutable audit trails capturing every read, write, and export event containing ePHI, retained for 6 years.
  - *Transmission Security*: Field-level encryption or dedicated cryptographic isolation for database columns storing patient identifiers.

### D. PCI-DSS v4.0 (Cardholder Data Environment)
- **Scope Reduction via Tokenization**: Offload payment form collection to hosted iframes/SDKs (Stripe Elements, Adyen Drop-in, Braintree Hosted Fields). Primary Account Numbers (PAN) must NEVER hit application memory or backend servers, qualifying for Self-Assessment Questionnaire (SAQ) A.
- **Requirement 10 (Logging & Monitoring)**: Centralized SIEM logging (Datadog/Elasticsearch) with real-time alerting on unauthorized access attempts and file integrity monitoring (FIM) on CDE nodes.
- **Requirement 11 (Vulnerability Testing)**: Quarterly vulnerability scans by an Approved Scanning Vendor (ASV) and annual third-party penetration testing.

## 2. Automated Evidence Collection Matrix

| Framework Requirement | Inspectable Technical Evidence | Automated Extraction Command / Method |
|---|---|---|
| SOC 2 CC7.2 (Branch Protection) | GitHub Branch Protection API JSON | `gh api repos/{owner}/{repo}/branches/main/protection` |
| SOC 2 CC6.1 (MFA Enforcement) | IdP user directory export showing MFA status | `GET /api/v1/users?filter=status eq "ACTIVE"` (Okta API) |
| ISO 27001 A.8.24 (Encryption at Rest) | AWS Config / Terraform compliance report | `aws rds describe-db-instances --query 'DBInstances[?StorageEncrypted==false]'` |
| HIPAA § 164.312 (Audit Logging) | CloudTrail S3 bucket retention & MFA delete | `aws s3api get-bucket-versioning --bucket audit-logs` |
| PCI-DSS Req 11.3 (ASV Scanning) | Signed external ASV vulnerability PDF report | Quarterly automated schedule via Qualys / Tenable |

## Critical Rules
1. Never generate manual compliance policies that contradict automated CI/CD configurations; policies must reflect real engineering workflows.
2. Maintain evidence as code: export infrastructure states, commit hashes, and access logs programmatically rather than manually taking screenshots.
3. Every external service handling user data must have a verified DPA or BAA on file before engineering wires the integration.

## Verification Checklist
- [ ] Technical controls mapped to relevant framework clauses (SOC 2 CC series, ISO 27001 Annex A, HIPAA § 164, PCI-DSS v4).
- [ ] Branch protection rules active on all production repositories requiring peer approval.
- [ ] Centralized logging captures security-relevant events with tamper-proof retention.
- [ ] Database volumes and object stores verified encrypted with AES-256 / KMS.
- [ ] Quarterly access review and vulnerability management cadence documented with owners.

## Anti-Patterns
- NEVER use shared admin credentials or root accounts for day-to-day engineering tasks.
- NEVER allow production database access without temporary, audited bastion/teleport sessions and justifiable ticket IDs.
- NEVER store raw unencrypted credit card data (PAN) or patient health data (ePHI) in general application log files.
