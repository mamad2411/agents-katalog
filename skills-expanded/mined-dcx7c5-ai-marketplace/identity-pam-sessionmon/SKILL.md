---
name: identity-pam-sessionmon
description: "Identity Pam Sessionmon."
domain: cybersecurity
---

|
| **PSM (Privileged Session Manager)** | CyberArk component that acts as a proxy/jump server, recording all privileged sessions in video and text format |
| **PSMP (PSM for SSH Proxy)** | Linux-based PSM proxy specifically for SSH, SCP, and SFTP sessions |
| **Connection Component** | CyberArk configuration that defines how PSM launches client applications (RDP, SSH, SSMS) to connect to target systems |
| **Privileged Threat Analytics (PTA)** | CyberArk module that applies behavioral analytics and risk scoring to recorded sessions to detect anomalous activity |
| **Dual Authorization** | Security control requiring two authorized users to approve a privileged session before it is established |
| **Session Isolation** | Architecture principle where administrators never directly connect to targets; all access is proxied through the PAM system |
| **Keystroke Transcript** | Text log of all keystrokes typed during a recorded session, searchable for audit and forensic purposes |
| **Vaulting** | Storing privileged credentials in an encrypted digital vault so they are never exposed to the end user |

## Verification

- [ ] All privileged access to production targets routes through PSM (direct RDP/SSH is blocked by firewall)
- [ ] Session recordings are being stored in the Vault with encryption and tamper protection
- [ ] Keystroke transcripts are captured and searchable for SSH and RDP sessions
- [ ] PTA rules trigger alerts for high-risk commands (test with a benign trigger pattern)
- [ ] Real-time monitoring dashboard shows active sessions with correct metadata
- [ ] Session recordings play back correctly in PVWA HTML5 player with timeline and transcript
- [ ] Storage estimates are validated and retention policies match compliance requirements
- [ ] Dual authorization is enforced for vendor and high-risk target access
- [ ] Session metadata and alerts are forwarding to SIEM and correlating correctly
- [ ] Auditors can search, review, and annotate sessions through the PVWA interface
- [ ] Terminated sessions leave a complete recording up to the point of termination
