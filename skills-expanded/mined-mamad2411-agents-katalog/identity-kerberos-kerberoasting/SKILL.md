---
name: identity-kerberos-kerberoasting
description: "Identity Kerberos Kerberoasting."
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

1. **Scenario 1**: Rubeus kerberoast targeting all SPN accounts
2. **Scenario 2**: GetUserSPNs.py from Impacket requesting RC4 tickets
3. **Scenario 3**: Targeted kerberoast against high-privilege service accounts
4. **Scenario 4**: AS-REP roasting accounts without pre-authentication

## Output Format

```
Hunt ID: TH-DETECT-[DATE]-[SEQ]
Technique: T1558.003
Host: [Hostname]
User: [Account context]
Evidence: [Log entries, process trees, network data]
Risk Level: [Critical/High/Medium/Low]
Confidence: [High/Medium/Low]
Recommended Action: [Containment, investigation, monitoring]
```
