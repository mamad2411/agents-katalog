---
name: identity-pam-delinea
description: "Identity Pam Delinea."
domain: cybersecurity
---

|
| **Privileged Access Management (PAM)** | Security framework for controlling, monitoring, and auditing elevated access to critical systems and data through credential vaulting and session management |
| **Secret** | A stored credential or sensitive data item in the vault, including passwords, SSH keys, API tokens, and certificates |
| **Remote Password Changing (RPC)** | Automated mechanism that connects to target systems to rotate passwords according to defined policies without manual intervention |
| **Heartbeat** | Periodic check that validates stored credentials against target systems to ensure vault contents remain synchronized and functional |
| **Dual Control** | Security mechanism requiring approval from a second authorized user before granting access to highly sensitive secrets |
| **Discovery** | Automated scanning of infrastructure to identify privileged accounts, service accounts, and dependencies across Active Directory, servers, and network devices |
| **Session Recording** | Capture of complete privileged session activity including video, keystrokes, and application usage for audit and forensic review |

## Tools & Systems

- **Delinea Secret Server**: Enterprise PAM solution providing credential vaulting, password rotation, session recording, and privileged access workflows
- **Delinea Distributed Engine**: Agent deployed in network segments to enable password changing and discovery across firewalled environments
- **Secret Server REST API**: RESTful API for programmatic secret management, automation, and integration with DevOps pipelines
- **Secret Server SDK**: .NET and PowerShell SDKs for application-level integration with Secret Server vault

## Common Scenarios

### Scenario: Migrating Shared Admin Credentials to Vault

**Context**: An organization stores 500+ shared administrator credentials in Excel spreadsheets and password-protected documents. Auditors flagged this as a critical finding requiring remediation within 90 days.

**Approach**:
1. Deploy Secret Server with SQL Server backend and configure HTTPS access
2. Design folder hierarchy mirroring the organizational structure (by department, system type, environment)
3. Create secret templates matching the credential types in use (Windows, Linux, database, network device)
4. Import existing credentials via CSV import or PowerShell bulk creation
5. Configure discovery to find undocumented privileged accounts across AD and local systems
6. Enable Remote Password Changing starting with non-production accounts to validate rotation
7. Roll out session launchers to replace direct RDP/SSH connections
8. Gradually enable dual control for Tier-0 accounts (Domain Admins, root accounts)
9. Configure SIEM integration and compliance reporting for audit evidence

**Pitfalls**:
- Not identifying all service account dependencies before enabling password rotation (causes service outages)
- Enabling RPC for production accounts without testing in non-production first
- Setting rotation intervals too short for service accounts that require coordinated restarts
- Not configuring Distributed Engines for network segments separated by firewalls

## Output Format

```
DELINEA SECRET SERVER PAM DEPLOYMENT REPORT
=============================================
Environment:       Hybrid (On-Premises + Azure)
Version:           Secret Server 11.6
Deployment Mode:   On-Premises (High Availability)

VAULT STATISTICS
Total Secrets:           1,247
  Windows Credentials:   523
  Linux/SSH Keys:        312
  Database Accounts:     198
  Network Devices:       87
  Cloud API Keys:        127

PASSWORD ROTATION STATUS
Auto-Change Enabled:     1,089 / 1,247 (87.3%)
Rotation Compliant:      1,056 / 1,089 (97.0%)
Heartbeat Healthy:       1,198 / 1,247 (96.1%)
Failed Rotations (30d):  12

SESSION MANAGEMENT
Active Sessions:         23
Recorded Sessions (30d): 4,567
Average Session Length:  22 minutes
Approval Requests (30d): 189 (174 approved, 15 denied)

DISCOVERY RESULTS
Scanned Systems:         2,340
Discovered Accounts:     3,891
Onboarded to Vault:      1,247 (32.1%)
Pending Review:          892

COMPLIANCE
SOX Controls Met:        12/12
PCI-DSS Requirements:    8/8
Password Age Violations: 3 (remediation in progress)
```
