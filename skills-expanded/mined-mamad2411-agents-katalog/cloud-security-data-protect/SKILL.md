---
name: cloud-security-data-protect
description: "Cloud Security Data Protect."
domain: cybersecurity
---

|
| S3 Data Events | CloudTrail object-level logging that captures GetObject, PutObject, DeleteObject, and CopyObject API calls with request details |
| GuardDuty S3 Protection | Threat detection feature analyzing CloudTrail S3 data events to identify anomalous access patterns and exfiltration attempts |
| Amazon Macie | Data security service that discovers and classifies sensitive data in S3 and generates findings for data exposure risks |
| VPC Endpoint Policy | Access control policy on an S3 VPC endpoint that restricts which buckets and actions can be accessed through the endpoint |
| Data Exfiltration | Unauthorized transfer of data from an organization's S3 storage to an external location controlled by an attacker |
| Anomalous Behavior Detection | Machine learning-based identification of S3 access patterns that deviate from established baselines for a principal |

## Tools & Systems

- **AWS CloudTrail**: Audit logging of S3 object-level operations for forensic analysis and anomaly detection
- **Amazon GuardDuty**: ML-based threat detection with S3-specific finding types for exfiltration and unauthorized access
- **Amazon Macie**: Sensitive data discovery and classification for correlating access anomalies with data sensitivity
- **Amazon Athena**: SQL query engine for analyzing CloudTrail logs at scale to identify bulk download patterns
- **CloudWatch Logs Insights**: Real-time log analysis for building detection queries against CloudTrail data

## Common Scenarios

### Scenario: Compromised IAM Credentials Used for Bulk S3 Data Download

**Context**: GuardDuty reports an `Exfiltration:S3/ObjectRead.Unusual` finding indicating that a developer's access key is downloading thousands of objects from a sensitive data bucket at 3 AM from an IP address in a foreign country.

**Approach**:
1. Immediately deactivate the compromised access key
2. Query CloudTrail for all S3 actions by the compromised principal in the last 72 hours
3. Identify which buckets and objects were accessed using Athena queries
4. Cross-reference accessed objects with Macie classifications to assess data sensitivity
5. Check for CopyObject calls to external accounts (cross-account exfiltration)
6. Review how the credentials were compromised (TruffleHog scan, phishing investigation)
7. Implement VPC endpoint policies to restrict future S3 access to approved network paths

**Pitfalls**: CloudTrail S3 data events can generate massive log volume. Use Athena with partitioned tables rather than CloudWatch Logs Insights for queries spanning more than 24 hours. GuardDuty baseline learning requires 7-14 days, so new accounts may generate false positives for normal access patterns.

## Output Format

```
S3 Data Exfiltration Investigation Report
============================================
Account: 123456789012
Detection Source: GuardDuty Exfiltration:S3/ObjectRead.Unusual
Investigation Date: 2026-02-23

INCIDENT TIMELINE:
  2026-02-23 02:47 UTC - First anomalous GetObject from 185.x.x.x
  2026-02-23 02:47-04:12 UTC - 12,847 GetObject requests
  2026-02-23 04:15 UTC - GuardDuty finding generated
  2026-02-23 04:20 UTC - PagerDuty alert received by SOC
  2026-02-23 04:25 UTC - Access key deactivated

COMPROMISED PRINCIPAL:
  ARN: arn:aws:iam::123456789012:user/developer-jane
  Access Key: AKIA...WXYZ
  Source IP: 185.x.x.x (Tor exit node)

DATA IMPACT ASSESSMENT:
  Buckets accessed: 3
  Objects downloaded: 12,847
  Total data volume: 4.7 GB
  Sensitive data types: PII (SSN, email), Financial (credit card)
  Macie severity: CRITICAL

CONTAINMENT ACTIONS:
  [x] Access key deactivated
  [x] User password reset and MFA re-enrolled
  [x] VPC endpoint policy applied to sensitive buckets
  [x] Bucket policy restricting to VPC-only access
  [x] TruffleHog scan initiated on developer repositories
```
