---
name: ics-historian-attack
description: "Ics Ics Historian Attack."
domain: cybersecurity
---

|
| OT Historian | Database server (OSIsoft PI, Ignition, Wonderware) storing time-series process data from SCADA/DCS systems |
| Pivot Point | Historian's position between IT and OT networks makes it a prime target for attackers to move between zones |
| Data Replay Attack | Feeding historical data to an HMI to mask real-time process manipulation (Stuxnet technique) |
| OSIsoft PI | Most widely deployed OT historian, used by 65% of Global 500 process companies |
| Ignition | Inductive Automation SCADA platform with historian module, increasingly targeted due to Python scripting capabilities |
| CVE-2025-0921 | Ignition SCADA privileged file system vulnerability allowing escalation through malicious project files |

## Output Format

```
HISTORIAN ATTACK DETECTION REPORT
====================================
Historian: [type and hostname]
Date: YYYY-MM-DD

CONNECTION ANALYSIS:
  Authorized Clients: [count]
  Unauthorized Clients Detected: [count with IPs]

DATA INTEGRITY:
  Tags Checked: [count]
  Integrity Issues: [count]
  Flatline Detections: [count]
  Data Gaps: [count]

LATERAL MOVEMENT INDICATORS:
  Outbound PLC Connections: [found/not found]
  Unauthorized Processes: [found/not found]
  Anomalous Authentication: [found/not found]
```
