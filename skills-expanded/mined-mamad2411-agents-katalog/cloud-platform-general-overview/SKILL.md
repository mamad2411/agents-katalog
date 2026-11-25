---
name: cloud-platform-general-overview
description: "Cloud Platform General Overview."
domain: cybersecurity
---

|
| CSPM | Cloud Security Posture Management, the practice of continuously monitoring cloud infrastructure for misconfigurations and compliance violations |
| Configuration Drift | Unintended changes to cloud resource configurations that deviate from the approved security baseline over time |
| Security Baseline | A documented set of minimum security configuration requirements that all cloud resources must meet |
| Compliance Framework | A structured set of security controls and requirements (CIS, SOC 2, PCI DSS, NIST) against which cloud configurations are evaluated |
| Finding Severity | Risk classification of a misconfiguration based on exploitability and potential impact (Critical, High, Medium, Low, Informational) |
| Auto-Remediation | Automated corrective action that restores a non-compliant resource to its required configuration without manual intervention |

## Tools & Systems

- **Prowler**: Open-source multi-cloud security assessment tool with 300+ checks aligned to CIS, PCI DSS, HIPAA, and NIST
- **ScoutSuite**: Multi-cloud security auditing tool producing risk-scored HTML reports from API-collected configuration data
- **AWS Security Hub**: AWS-native CSPM with aggregated findings and compliance standard evaluation
- **Microsoft Defender for Cloud**: Azure-native CSPM with secure score, regulatory compliance, and workload protection
- **GCP Security Command Center**: GCP-native security platform with asset inventory, vulnerability scanning, and compliance monitoring

## Common Scenarios

### Scenario: Establishing CSPM for a Multi-Cloud Enterprise

**Context**: An enterprise runs production workloads across AWS (primary), Azure (identity and Microsoft services), and GCP (data analytics). The security team needs unified posture visibility.

**Approach**:
1. Enable cloud-native CSPM in each provider: Security Hub, Defender for Cloud, SCC
2. Deploy Prowler scans as daily scheduled jobs in each environment via CI/CD pipelines
3. Normalize and aggregate findings into a central data lake using the aggregation script
4. Build dashboards in Grafana or Kibana showing posture scores by cloud, account, and severity
5. Configure auto-remediation for known-good fixes (public access blocks, encryption enablement)
6. Route CRITICAL findings to PagerDuty for immediate response and HIGH findings to Jira tickets
7. Produce weekly compliance reports for executive stakeholders showing trend data

**Pitfalls**: Running CSPM tools with overly broad permissions creates a high-value target. Use dedicated service accounts with read-only permissions and rotate credentials regularly. Different CSPM tools may report the same misconfiguration differently, so deduplication logic must account for varying resource ID formats and finding titles across tools.

## Output Format

```
Cloud Security Posture Management Dashboard
==============================================
Organization: Acme Corp
Assessment Date: 2026-02-23
Environments: AWS (12 accounts), Azure (8 subscriptions), GCP (5 projects)

POSTURE SCORES:
  AWS:   82/100  (+3 from last week)
  Azure: 76/100  (-1 from last week)
  GCP:   79/100  (+5 from last week)
  Overall: 79/100

FINDINGS BY SEVERITY:
  Critical:  18 (AWS: 7, Azure: 8, GCP: 3)
  High:      67 (AWS: 28, Azure: 24, GCP: 15)
  Medium:   234 (AWS: 98, Azure: 87, GCP: 49)
  Low:      412 (AWS: 178, Azure: 134, GCP: 100)

TOP FAILING CATEGORIES:
  1. IAM overly permissive policies     (43 findings)
  2. Encryption not enabled at rest      (38 findings)
  3. Public network exposure             (29 findings)
  4. Logging and monitoring gaps         (24 findings)
  5. Unused credentials and keys         (19 findings)

AUTO-REMEDIATION (Last 7 Days):
  Findings auto-remediated:  34
  Manual remediation pending: 51
  Exceptions approved:        8
```
