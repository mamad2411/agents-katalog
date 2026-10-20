---
name: identity-rbac-entitlement
description: "Identity Rbac Entitlement."
domain: cybersecurity
---

|
| **Certification Campaign** | An organized review process where designated certifiers validate whether users should retain their current access entitlements across one or more applications |
| **Access Review** | Individual review unit within a campaign where a certifier examines and makes approve/revoke decisions on specific user entitlements |
| **Entitlement** | A specific permission, group membership, role, or access right granted to an identity on a target application |
| **Certifier** | The reviewer responsible for making access decisions, typically a manager, application owner, or data owner |
| **Revocation** | Decision to remove an entitlement from a user, triggering a provisioning request to the target application for access removal |
| **SOD Violation** | Separation of Duties conflict where a user holds entitlements from two or more conflicting access groups that create a segregation risk |
| **Remediation** | Automated or manual process of removing revoked access from target systems following certification decisions |

## Tools & Systems

- **SailPoint IdentityIQ**: Enterprise identity governance platform providing access certifications, lifecycle management, and compliance reporting
- **IdentityIQ Compliance Manager**: Module for running certification campaigns, tracking reviewer progress, and generating compliance evidence
- **SailPoint REST API**: Programmatic interface for automating certification campaigns, querying status, and extracting audit data
- **IdentityIQ Report Builder**: Built-in reporting engine for generating access review statistics, SOD violation summaries, and trend analysis

## Common Scenarios

### Scenario: SOX Compliance Quarterly Access Review

**Context**: A publicly traded company must demonstrate quarterly access reviews for all financial applications per SOX Section 404. The previous manual review process took 6 weeks and produced inconsistent results.

**Approach**:
1. Define application scope: SAP ERP, Oracle Financials, banking platforms, and treasury systems
2. Configure manager certifications with 30-day active period for general access review
3. Create targeted entitlement certifications for privileged financial roles with application owner as certifier
4. Enable SOD policy checks to flag AP/AR, GL posting/approval, and user admin/transaction conflicts
5. Configure automatic reminders at 7, 14, and 21 days with escalation to compliance team at day 25
6. Set default-revoke for items not reviewed by campaign end to enforce completion accountability
7. Generate signed certification reports with decision audit trail for external auditors
8. Track revocation completion to ensure all denied access is actually removed from target systems

**Pitfalls**:
- Not pre-populating entitlement descriptions causes certifiers to approve everything they do not understand
- Setting campaigns too short (under 21 days) results in rubber-stamping and low-quality reviews
- Not validating that revocations are actually provisioned to target systems (approve on paper, still active in system)
- Missing service accounts from review scope when they have access to financial systems

## Output Format

```
ACCESS CERTIFICATION CAMPAIGN REPORT
=======================================
Campaign:          Q1-2026 Manager Access Review
Type:              Manager Certification
Period:            2026-01-15 to 2026-02-14
Status:            COMPLETED

COVERAGE
Identities Reviewed:    2,847
Applications In Scope:  34
Total Entitlements:     18,392

DECISION SUMMARY
Approved:              16,841 (91.6%)
Revoked:                1,203 (6.5%)
Mitigated:                 198 (1.1%)
Delegated:                 150 (0.8%)

REVOCATION STATUS
Provisioned:            1,089 / 1,203 (90.5%)
Pending:                   87
Failed:                    27 (manual work items created)

SOD VIOLATIONS
Flagged:                   43
Remediated:                31
Compensating Controls:     12

CERTIFIER COMPLIANCE
On-Time Completion:     89.3%
Required Escalation:    14 certifiers
Average Review Time:    3.2 minutes per item

SIGN-OFF
Campaign Signed:        2026-02-14 by compliance-admin
Audit Evidence:         Exported to /reports/Q1-2026-cert-evidence.pdf
```
