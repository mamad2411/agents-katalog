---
name: identity-ntlm-passthehash
description: "Identity Ntlm Passthehash."
domain: cybersecurity
---

|
| CrowdStrike Falcon | EDR telemetry and threat detection |
| Microsoft Defender for Endpoint | Advanced hunting with KQL |
| Splunk Enterprise | SIEM log analysis with SPL queries |
| Elastic Security | Detection rules and investigation timeline |
| Sysmon | Detailed Windows event monitoring |
| Velociraptor | Endpoint artifact collection and hunting |
| Sigma Rules | Cross-platform detection rule format |

## Common Scenarios

1. **Scenario 1**: Mimikatz sekurlsa::pth with stolen NTLM hash
2. **Scenario 2**: Impacket psexec.py remote execution with hash
3. **Scenario 3**: CrackMapExec hash spraying across hosts
4. **Scenario 4**: WMI lateral movement via pass-the-hash

## Output Format

```
Hunt ID: TH-DETECT-[DATE]-[SEQ]
Technique: T1550.002
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```
