---
name: identity-rbac-identity
description: "Identity Rbac Identity."
domain: cybersecurity
---

|
| **Joiner-Mover-Leaver (JML)** | Core identity lifecycle transitions covering employee onboarding (joiner), role/department changes (mover), and offboarding (leaver) |
| **Birthright Access** | Baseline entitlements automatically provisioned based on job code, department, or location without requiring an access request |
| **Role Mining** | Analysis of existing access patterns to derive role definitions by identifying common entitlement groupings across similar job functions |
| **Orphaned Account** | Application account that no longer has a corresponding active identity in the authoritative HR source, representing a security risk |
| **Authoritative Source** | System of record (typically HR) that serves as the single source of truth for identity attributes and employment status |
| **Access Request Workflow** | Self-service process enabling users to request additional entitlements with risk-based approval routing |

## Tools & Systems

- **SailPoint IdentityIQ/IdentityNow**: Enterprise IGA platform for lifecycle management, access certifications, and automated provisioning
- **Saviynt Enterprise Identity Cloud**: Cloud-native IGA with identity warehouse, access governance, and application access management
- **Microsoft Entra ID Governance**: Identity governance capabilities including lifecycle workflows, access reviews, and entitlement management
- **One Identity Manager**: IGA solution with business role management, attestation, and IT shop for access requests

## Common Scenarios

### Scenario: Building JML Process for 10,000-Employee Organization

**Context**: Rapidly growing company has no automated identity lifecycle. IT manually creates accounts, taking 3-5 days for new hires. Terminated employees retain access for weeks. Audit found 2,300 orphaned accounts across 45 applications.

**Approach**:
1. Integrate Workday as authoritative source with daily delta sync to IGA platform
2. Mine existing access patterns to define birthright roles for the top 20 job codes (covering 80% of employees)
3. Implement pre-hire provisioning triggered 7 days before start date for AD, email, and birthright apps
4. Build termination workflow that disables all access within 1 hour of HR status change
5. Create mover workflow that recalculates roles when job code or department changes
6. Deploy self-service access request portal with risk-based approval chains
7. Run orphaned account detection to identify and remediate the 2,300 existing orphans
8. Schedule quarterly access certifications to prevent access accumulation

**Pitfalls**:
- Not defining a single authoritative source leads to conflicting identity data from multiple HR systems
- Mining roles without business validation creates technical roles that do not align with organizational structure
- Automating termination without grace period for knowledge transfer frustrates business managers
- Not handling contractor and vendor identities that exist outside the HR system

## Output Format

```
IDENTITY GOVERNANCE LIFECYCLE REPORT
=======================================
Authoritative Source:   Workday
IGA Platform:          SailPoint IdentityIQ
Total Identities:      10,247
Active Employees:      9,834
Contractors:           413

LIFECYCLE AUTOMATION
Joiner (Pre-Hire) SLA:     Target: 0 days | Actual: 0.2 days avg
Mover Processing SLA:      Target: 1 day  | Actual: 0.8 days avg
Leaver Disablement SLA:    Target: 1 hour | Actual: 0.5 hours avg

PROVISIONING METRICS (Last 30 Days)
New Hires Provisioned:     187
  Auto-Provisioned:        174 (93.0%)
  Manual Intervention:     13 (7.0%)
Role Changes Processed:    89
Terminations Processed:    43
  Within 1-Hour SLA:       41 (95.3%)

ROLE GOVERNANCE
Defined Roles:             127
Birthright Roles:          48
Average Entitlements/Role: 12.3
Role Overlap > 70%:        8 pairs (consolidation recommended)

ORPHANED ACCOUNTS
Detected:                  23
  Critical:                2 (privileged accounts)
  High:                    8
  Medium:                  13
Remediated (30 days):      19
Outstanding:               4

ACCESS REQUESTS
Submitted:                 342
Auto-Approved (Birthright):87 (25.4%)
Approved:                  231 (67.5%)
Denied:                    24 (7.0%)
Average Approval Time:     6.2 hours
SOD Violations Flagged:    12
```
