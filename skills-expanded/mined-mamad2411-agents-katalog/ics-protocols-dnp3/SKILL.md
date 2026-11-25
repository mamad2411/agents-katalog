---
name: ics-protocols-dnp3
description: "Ics Ics Protocols Dnp3."
domain: cybersecurity
---

|
| DNP3 | Distributed Network Protocol version 3, the predominant SCADA protocol in the energy sector for communication between masters and outstations |
| Outstation | DNP3 slave device (typically an RTU or IED) that responds to master station polls and commands |
| Select-Before-Operate | DNP3 safety mechanism requiring a Select command before an Operate, preventing accidental control actions |
| Cold Restart (FC 0x0D) | DNP3 command that fully restarts an outstation, resetting all configuration -- a high-risk denial-of-service operation |
| DNP3 Secure Authentication | Optional DNP3 extension (SA v5) adding HMAC-based authentication to prevent command spoofing |
| PIPEDREAM | ICS attack framework with DNP3 capabilities for manipulating outstations and performing firmware updates |

## Output Format

```
DNP3 ANOMALY DETECTION REPORT
================================
Analysis Period: [start] to [end]
Monitoring Point: [substation/segment]

TRAFFIC SUMMARY:
  DNP3 Packets: [count]
  Unique Master-Outstation Pairs: [count]
  Control Commands: [count]
  File Operations: [count]

ALERTS:
  [CRITICAL] Unauthorized DNP3 master [IP]
  [CRITICAL] Cold restart command to outstation [addr]
  [HIGH] Unexpected control command from [IP]

RECOMMENDATIONS:
  1. Deploy DNP3 Secure Authentication (SA v5)
  2. Block unauthorized sources at firewall
  3. Enable DNP3 DPI on industrial firewall
```
