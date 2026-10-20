---
name: ics-access-remote-configure
description: "Ics Ics Access Remote Configure."
domain: cybersecurity
---

|
| Intermediate System | System in the DMZ that terminates external connections and brokers new connections to OT, preventing direct network access per CIP-005 |
| Jump Server | Hardened bastion host in the DMZ used for remote access sessions to OT systems with session recording and access controls |
| Session Recording | Capture of all remote access session activity (screen, keystrokes, commands) for security audit and incident investigation |
| Privileged Access Management (PAM) | System for vaulting credentials, controlling access, and auditing privileged sessions to critical OT systems |
| Co-Attendance | Requirement for an OT operator to monitor vendor remote access sessions in real time |
| Time-Limited Access | Vendor accounts enabled only for specific maintenance windows and automatically disabled after the window closes |

## Tools & Systems

- **CyberArk Privileged Access Security**: Enterprise PAM with session management, credential vaulting, and recording for OT remote access
- **BeyondTrust Privileged Remote Access**: Purpose-built remote access solution with session recording and granular access policies
- **Claroty Secure Remote Access (SRA)**: OT-specific remote access solution with protocol-aware session controls
- **Duo Security**: MFA provider supporting push notifications, hardware tokens, and biometrics for OT access verification

## Output Format

```
OT Remote Access Security Report
===================================
Active Sessions: [N]
Pending Approval: [N]
Sessions Today: [N]

MFA COMPLIANCE:
  All sessions MFA verified: [Yes/No]
  Sessions without MFA: [N]

VENDOR ACCESS:
  Active vendor sessions: [N]
  Co-attended: [N]
  Recorded: [N]
```
