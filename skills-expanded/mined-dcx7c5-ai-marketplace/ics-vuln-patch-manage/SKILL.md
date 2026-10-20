---
name: ics-vuln-patch-manage
description: "Ics Ics Vuln Patch Manage."
domain: cybersecurity
---

|
| Compensating Control | Alternative security measure applied when a patch cannot be deployed, such as firewall rules, IPS signatures, or network isolation |
| Vendor Compatibility | Confirmation from the OT vendor that a patch (especially OS patches) is compatible with their control system software |
| Maintenance Window | Scheduled period for system modifications, aligned with process shutdowns or reduced-risk operational periods |
| Virtual Patching | Deploying IDS/IPS rules to detect and block exploitation attempts for known vulnerabilities without modifying the target system |
| Evaluation Deadline | NERC CIP-007-6 requires patch evaluation within 35 calendar days of availability |
| Turnaround | Major scheduled shutdown of a process unit for maintenance, providing opportunity for extensive OT patching |

## Tools & Systems

- **WSUS/SCCM**: Microsoft patch management for Windows-based OT systems (HMIs, historians, engineering workstations)
- **Siemens ProductCERT**: Siemens security advisory service for industrial products
- **Claroty xDome**: OT vulnerability management with patch availability tracking and risk scoring
- **Tripwire Enterprise**: Configuration monitoring detecting unauthorized changes and tracking patch status

## Output Format

```
OT Patch Management Report
============================
Reporting Period: YYYY-MM to YYYY-MM

PATCH STATUS:
  Identified: [N]
  Evaluating: [N]
  Testing: [N]
  Deployed: [N]
  Deferred: [N]

COMPLIANCE:
  Evaluated within 35 days: [N]/[N] (CIP-007-6 R2)
  Deployed or mitigated: [N]/[N]
  Deferred with compensating controls: [N]
```
