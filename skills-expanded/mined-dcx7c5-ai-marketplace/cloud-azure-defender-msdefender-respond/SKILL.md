---
name: cloud-azure-defender-msdefender-respond
description: "Cloud Azure Defender Msdefender Respond."
domain: cybersecurity
---

|
| Secure Score | A numerical measure of an organization's security posture based on the percentage of implemented security recommendations, scored per subscription and aggregated at the management group level |
| Cloud Security Graph | A graph database mapping relationships between cloud resources, identities, network exposure, and vulnerabilities to identify exploitable attack paths |
| Attack Path Analysis | Visualization of multi-step attack chains an adversary could follow from an entry point to a high-value target, prioritized by real-world exploitability |
| Just-In-Time Access | Security control that blocks management ports by default and opens them temporarily upon approved request, reducing the VM attack surface |
| Adaptive Application Controls | Machine-learning-based allowlisting that recommends which applications should run on VMs and alerts on deviations |
| Defender CSPM | Enhanced cloud security posture management plan providing agentless scanning, attack path analysis, and cloud security graph capabilities |
| Security Connector | Integration point connecting AWS or GCP environments to Defender for Cloud for multi-cloud posture management |

## Tools & Systems

- **Microsoft Defender for Cloud**: Core CNAPP platform providing CSPM, CWP, and threat protection across Azure, AWS, and GCP
- **Azure Resource Graph**: Query engine for exploring cloud security graph data and attack paths at scale
- **Azure Logic Apps**: Workflow automation platform for building remediation playbooks triggered by Defender alerts
- **Microsoft Defender Portal**: Unified security operations console integrating Defender for Cloud with XDR, Sentinel, and threat intelligence
- **Azure Policy**: Governance engine for enforcing Defender for Cloud recommendations as compliance requirements

## Common Scenarios

### Scenario: Internet-Exposed SQL Server with Known Vulnerability

**Context**: Defender for Cloud identifies an Azure SQL Server with a public endpoint, an unpatched critical CVE, and a service principal with database owner permissions that also has access to a Key Vault containing production encryption keys.

**Approach**:
1. Review the attack path in the cloud security graph showing: Internet -> SQL Server (CVE) -> Service Principal -> Key Vault
2. Immediately restrict the SQL Server firewall to private endpoints only
3. Apply the SQL Server security patch through Azure Update Management
4. Rotate the service principal credentials and scope its permissions to only the required database operations
5. Add a Key Vault access policy requiring the service principal to authenticate via managed identity rather than secret-based credentials
6. Verify the attack path is resolved in Defender CSPM within 24 hours

**Pitfalls**: Focusing on the SQL vulnerability alone misses the lateral movement path to Key Vault. Restricting the endpoint without updating application connection strings causes an outage.

## Output Format

```
Microsoft Defender for Cloud Security Report
=============================================
Tenant: acme-corp.onmicrosoft.com
Subscriptions Monitored: 12
Report Date: 2025-02-23

SECURE SCORE: 72/100

DEFENDER PLANS STATUS:
  Servers (P2):     ENABLED - 156 VMs covered
  Containers:       ENABLED - 8 AKS clusters covered
  Storage:          ENABLED - 342 storage accounts, malware scanning active
  Databases:        ENABLED - 23 SQL servers, 5 Cosmos DB accounts
  Key Vault:        ENABLED - 18 vaults monitored
  AWS Connector:    ENABLED - 3 accounts connected
  GCP Connector:    ENABLED - 2 projects connected

CRITICAL ATTACK PATHS:
  [AP-001] Internet -> VM (RDP open) -> Managed Identity -> Storage (PII data)
    Risk: Critical | Affected Resources: 3 | Remediation: Close RDP, restrict MI scope
  [AP-002] Internet -> App Service (SQLi vuln) -> SQL DB -> Service Principal -> Key Vault
    Risk: Critical | Affected Resources: 5 | Remediation: Patch app, private endpoint

ALERT SUMMARY (Last 30 Days):
  Critical: 5 | High: 23 | Medium: 67 | Low: 134
  Top Alert Types:
    - Suspicious login activity (18)
    - Malware detected in storage (7)
    - Anomalous resource deployment (12)
```
