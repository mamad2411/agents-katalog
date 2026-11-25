---
name: cloud-azure-sentinel
description: "Cloud Azure Sentinel."
domain: cybersecurity
---

|
| KQL | Kusto Query Language, the primary query language for Microsoft Sentinel used to search, analyze, and visualize security data |
| Analytics Rule | Detection logic in Sentinel that evaluates log data on a schedule and creates incidents when conditions match |
| SOAR Playbook | Automated workflow triggered by incidents that performs response actions such as blocking accounts, enriching alerts, or notifying teams |
| Data Connector | Integration module that ingests security logs from cloud services, identity providers, and third-party tools into Sentinel |
| Sentinel Data Lake | Petabyte-scale storage layer providing long-term log retention with KQL and SQL query interfaces for advanced hunting |
| Workbook | Interactive dashboard in Sentinel displaying visualizations of security data, trends, and operational metrics |
| Watchlist | Reference data tables in Sentinel used to enrich alerts with context such as VIP user lists or approved IP ranges |
| Fusion Detection | Machine learning-powered correlation engine that automatically detects multi-stage attacks across data sources |

## Tools & Systems

- **Microsoft Sentinel**: Cloud-native SIEM/SOAR platform built on Azure Log Analytics with AI-powered threat detection
- **Azure Logic Apps**: Low-code automation platform for building SOAR playbooks triggered by Sentinel incidents
- **Microsoft Threat Intelligence**: Integrated threat feeds providing IP, domain, and URL indicators for matching against security logs
- **Azure Data Explorer**: High-performance analytics engine underlying Sentinel KQL queries for large-scale data exploration
- **MITRE ATT&CK Navigator**: Framework for mapping Sentinel detection rules to adversary tactics and techniques

## Common Scenarios

### Scenario: Detecting Cross-Cloud Credential Theft Campaign

**Context**: An attacker compromises an Azure AD account through phishing, then uses the account to access AWS resources via federated identity. Sentinel needs to correlate the Azure sign-in anomaly with unusual AWS API activity.

**Approach**:
1. Create an analytics rule detecting Azure AD impossible travel or anomalous sign-in risk
2. Write a KQL query correlating the compromised Azure AD identity with AWS CloudTrail AssumeRoleWithSAML events
3. Build a Fusion detection rule that links Azure AD risk events with subsequent AWS privilege escalation activity
4. Deploy a SOAR playbook that automatically disables the Azure AD account and revokes AWS STS sessions
5. Create a workbook showing the timeline from initial compromise through lateral movement to AWS
6. Run a hunting query across the data lake to check for similar patterns affecting other accounts

**Pitfalls**: Not correlating identity across cloud providers misses the full attack chain. Setting analytics rule frequency too low (e.g., 24 hours) allows attackers hours of undetected access.

## Output Format

```
Microsoft Sentinel SOC Operations Report
==========================================
Workspace: sentinel-workspace
Data Sources: 14 connectors active
Report Period: 2025-02-01 to 2025-02-23

DATA INGESTION:
  Azure AD Sign-in Logs:     2.3 TB (23 days)
  AWS CloudTrail:            1.8 TB (23 days)
  Azure Activity:            0.9 TB (23 days)
  Defender for Cloud Alerts: 45 GB (23 days)
  Total Ingestion:           5.1 TB

DETECTION SUMMARY:
  Active Analytics Rules: 87
  Incidents Created: 234
    Critical: 8 | High: 34 | Medium: 89 | Low: 103
  Mean Time to Detect (MTTD): 4.2 minutes
  Mean Time to Respond (MTTR): 18 minutes

TOP INCIDENT TYPES:
  Impossible Travel Detected:          42 incidents
  AWS Unauthorized API Call Pattern:   28 incidents
  Mass File Deletion in S3:            3 incidents
  Suspicious Azure AD App Registration: 12 incidents

AUTOMATION:
  Playbooks Executed: 156
  Accounts Auto-Disabled: 23
  Incidents Auto-Enriched: 198
  False Positive Rate: 12%
```
