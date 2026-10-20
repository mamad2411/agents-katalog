---
name: cloud-azure-defender
description: "Cloud Azure Defender."
domain: cybersecurity
---

|
| Microsoft Defender for Cloud | Azure-native security platform providing CSPM and cloud workload protection (CWP) across Azure, hybrid, and multi-cloud environments |
| Secure Score | Numerical measure of an organization's security posture based on the percentage of security recommendations that have been implemented |
| Security Recommendation | Actionable guidance from Defender for Cloud to improve security posture, prioritized by severity and secure score impact |
| Defender Plan | Workload-specific protection tier (Servers, Containers, SQL, Storage, etc.) that enables advanced threat detection for specific resource types |
| Just-In-Time VM Access | Feature that reduces attack surface by blocking management ports (SSH/RDP) by default and granting time-limited access on request |
| Adaptive Application Controls | Machine-learning-based allowlisting that recommends which applications should be allowed to run on VMs |

## Tools & Systems

- **Microsoft Defender for Cloud**: Central security platform with CSPM, CWP, and regulatory compliance capabilities
- **Azure Policy**: Governance service used by Defender for Cloud to evaluate and enforce security configurations
- **Log Analytics Workspace**: Backend data store for security telemetry collected by Defender agents
- **Azure Logic Apps**: Workflow automation for incident response triggered by Defender alerts
- **Azure Arc**: Extends Defender for Cloud protection to hybrid and multi-cloud servers and Kubernetes clusters

## Common Scenarios

### Scenario: Rolling Out Defender for Cloud Across a Multi-Subscription Enterprise

**Context**: An enterprise with 20 Azure subscriptions needs to enable Defender for Cloud with server, container, and SQL protection while establishing a compliance baseline against CIS Azure 2.0.

**Approach**:
1. Enable the CSPM plan (CloudPosture) across all subscriptions using Azure Policy initiative
2. Enable Defender for Servers P2, Containers, and SQL on production subscriptions
3. Configure auto-provisioning to deploy Log Analytics agents to all VMs
4. Enable CIS Azure 2.0 and PCI DSS 4.0 compliance standards
5. Create security contacts and configure alert notifications to the SOC team
6. Set up workflow automation for High severity alerts via Logic Apps
7. Enable JIT VM access for all production servers to eliminate persistent SSH/RDP exposure
8. Create a weekly Secure Score report for executive stakeholders

**Pitfalls**: Defender for Servers P2 costs per server per hour. For environments with many VMs, costs can escalate quickly. Use Defender for Servers P1 for development subscriptions and P2 only for production. Auto-provisioning of agents may conflict with existing agent deployments managed by SCCM or other tools.

## Output Format

```
Microsoft Defender for Cloud Deployment Report
=================================================
Organization: Acme Corp
Subscriptions: 20 (12 production, 8 non-production)
Deployment Date: 2026-02-23

DEFENDER PLANS ENABLED:
  CloudPosture (CSPM):     20 / 20 subscriptions
  Servers P2:              12 / 20 (production only)
  Containers:              12 / 20 (production only)
  SQL:                     12 / 20 (production only)
  Storage:                 20 / 20 all subscriptions
  Key Vault:               20 / 20 all subscriptions

SECURE SCORE:
  Current: 62% (baseline)
  Target: 80% within 90 days

COMPLIANCE STATUS (CIS Azure 2.0):
  Compliant controls:        78 / 142 (55%)
  Non-compliant controls:    52 / 142
  Not applicable:            12 / 142

RECOMMENDATIONS:
  Critical:    8 recommendations affecting 34 resources
  High:       24 recommendations affecting 89 resources
  Medium:     56 recommendations affecting 234 resources
  Low:        34 recommendations affecting 112 resources

SECURITY ALERTS (Last 7 Days):
  High severity:    3
  Medium severity:  12
  Low severity:     28
```
