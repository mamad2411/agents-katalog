---
name: intel-mitre-threatmodel
description: "Intel Mitre Threatmodel."
domain: cybersecurity
---

--|
| **MITRE ATT&CK** | Knowledge base of adversary tactics, techniques, and procedures based on real-world observations |
| **TTP** | Tactics, Techniques, and Procedures — the behavioral patterns of adversary groups |
| **ATT&CK Navigator** | Web tool for visualizing ATT&CK matrices as layered heatmaps showing coverage or threat profiles |
| **Gap Analysis** | Process of comparing threat actor TTPs against detection coverage to identify blind spots |
| **Threat-Informed Defense** | Security strategy prioritizing defenses based on actual adversary behaviors rather than theoretical risks |
| **Adversary Emulation** | Controlled simulation of threat actor TTPs to validate detection and response capabilities |

## Tools & Systems

- **MITRE ATT&CK Navigator**: Web-based visualization tool for creating and overlaying ATT&CK technique layers
- **MITRE Caldera**: Automated adversary emulation platform for testing detection coverage at scale
- **Atomic Red Team**: Open-source library of ATT&CK technique tests for security control validation
- **CTID ATT&CK Workbench**: MITRE tool for customizing ATT&CK knowledge base with organizational context
- **Tidal Cyber**: Commercial platform for threat-informed defense planning using ATT&CK framework

## Common Scenarios

- **Annual Threat Assessment**: Map top 5 threat actors to ATT&CK, overlay against detection, produce gap analysis
- **Cloud Migration Planning**: Model cloud-specific threats (T1078.004, T1537) and plan detection coverage
- **M&A Security Assessment**: Threat model the acquired company's environment against relevant threat actors
- **Budget Justification**: Use gap analysis to demonstrate detection blind spots requiring tool investment
- **Purple Team Planning**: Select adversary emulation scenarios based on highest-priority gaps from threat model

## Output Format

```
THREAT MODEL ASSESSMENT — Financial Services Division
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Date:             2024-03-15
Threat Actors:    FIN7, APT38, Lazarus Group
Techniques Total: 87 unique techniques across all actors

DETECTION COVERAGE:
  Covered:     56/87 (64%)
  Gaps:        31/87 (36%)

  Tactic Coverage Breakdown:
    Initial Access:      78%  ████████░░
    Execution:           82%  █████████░
    Persistence:         71%  ████████░░
    Priv Escalation:     65%  ███████░░░
    Defense Evasion:     52%  ██████░░░░  <-- Priority gap
    Credential Access:   58%  ██████░░░░  <-- Priority gap
    Discovery:           45%  █████░░░░░
    Lateral Movement:    61%  ███████░░░
    Collection:          50%  ██████░░░░
    Exfiltration:        55%  ██████░░░░
    C2:                  67%  ███████░░░

TOP PRIORITY GAPS (30-day remediation):
  1. T1055 Process Injection — used by all 3 actors, 0 detections
  2. T1003.006 DCSync — used by FIN7 and Lazarus, 0 detections
  3. T1070.004 File Deletion — evidence destruction, 0 detections

INVESTMENT RECOMMENDATION:
  Closing top 10 gaps requires: 2 detection engineer FTEs, 60 days
  Expected coverage improvement: 64% -> 76%
```
