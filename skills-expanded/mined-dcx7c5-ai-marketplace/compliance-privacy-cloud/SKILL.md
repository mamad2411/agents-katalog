---
name: compliance-privacy-cloud
description: "Compliance Privacy Cloud."
domain: cybersecurity
---

|
| Data Loss Prevention | Security controls and technologies that detect and prevent unauthorized disclosure of sensitive data from cloud environments |
| Amazon Macie | AWS service using machine learning to discover, classify, and protect sensitive data stored in S3 buckets |
| Google Cloud DLP | GCP API for inspecting, classifying, and de-identifying sensitive data across Cloud Storage, BigQuery, and Datastore |
| Data De-identification | Transforming sensitive data using masking, tokenization, encryption, or redaction to remove identifying characteristics while preserving utility |
| Sensitivity Label | Classification tag applied to data (Confidential, Highly Confidential) that triggers DLP policy enforcement and access controls |
| Custom Data Identifier | Organization-specific pattern (regex or keyword) added to DLP services to detect proprietary sensitive data formats |

## Tools & Systems

- **Amazon Macie**: ML-powered sensitive data discovery and classification for S3 with automated finding generation
- **Google Cloud DLP API**: Programmable API for inspecting, classifying, de-identifying, and redacting sensitive data
- **Microsoft Purview**: Data governance platform with sensitivity labeling, auto-classification, and DLP policy enforcement
- **Azure Information Protection**: Data classification and labeling service integrated with Microsoft 365 and Azure storage
- **Nightfall AI**: Third-party cloud DLP tool supporting scanning across SaaS applications and cloud infrastructure

## Common Scenarios

### Scenario: Discovering PII in an Unprotected S3 Data Lake

**Context**: A compliance audit reveals that the analytics team's S3 data lake contains customer PII (names, emails, SSNs) in CSV files without encryption or access controls. The organization must classify all data and implement DLP controls.

**Approach**:
1. Enable Macie and create a one-time classification job against the data lake bucket
2. Review Macie findings to identify which objects contain PII and what types
3. Create custom data identifiers for organization-specific formats (employee IDs, account numbers)
4. Implement a weekly scheduled Macie job for ongoing discovery
5. Build a data pipeline gate that scans new data before promotion to the data lake
6. Apply de-identification transforms (masking SSNs, tokenizing emails) for analytics use cases
7. Configure S3 bucket policies to restrict access to classified data to authorized roles only

**Pitfalls**: Macie charges per GB scanned. Large data lakes can generate significant costs. Use scoping rules to focus on high-risk object types (CSV, JSON, Parquet) and exclude known-safe formats (compressed archives, binary files). De-identification must preserve data utility for analytics while removing re-identification risk.

## Output Format

```
Cloud DLP Compliance Report
==============================
Organization: Acme Corp
Scan Period: 2026-02-01 to 2026-02-23
Environments: AWS (12 buckets), GCP (3 datasets), Azure (5 storage accounts)

DATA DISCOVERY SUMMARY:
  Total objects/records scanned:    2,847,000
  Objects with sensitive data:        45,200 (1.6%)
  Unique sensitivity categories:      8

SENSITIVE DATA FINDINGS:
  PII (names, emails, phone):       23,400 objects
  Financial (credit cards, bank):     8,700 objects
  Health (PHI, medical records):      3,200 objects
  Credentials (API keys, tokens):     1,400 objects
  Government ID (SSN, passport):      5,800 objects
  Custom (employee ID, account):      2,700 objects

FINDINGS BY SEVERITY:
  Critical:    1,400 (exposed credentials)
  High:       14,200 (unprotected PII/PHI)
  Medium:     18,600 (standard PII)
  Low:        11,000 (non-sensitive patterns)

PROTECTION STATUS:
  Data with encryption at rest:       78%
  Data with access controls:          65%
  Data with sensitivity labels:       12%
  Pipeline data with DLP gates:       30%

REMEDIATION ACTIONS:
  Objects quarantined:                1,400
  De-identification applied:          8,200
  Access controls tightened:         14,200
  Sensitivity labels applied:        45,200
```
