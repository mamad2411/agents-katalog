---
name: ics-historian-server
description: "Ics Ics Historian Server."
domain: cybersecurity
---

|
| Process Historian | Server that collects, stores, and serves time-series process data from industrial control systems at high frequency (sub-second to seconds) |
| PI Trust | Legacy OSIsoft PI authentication method based on IP address/hostname; insecure and should be migrated to Windows Integrated Security |
| Data Diode | Hardware-enforced unidirectional gateway ensuring historian data flows only from OT to DMZ, preventing reverse access |
| PI-to-PI Interface | OSIsoft replication mechanism that synchronizes PI data between servers, used for DMZ data mirroring |
| Audit Trail | Historian feature logging all modifications to historical data with before/after values, user identity, and timestamp |
| Tag Security | Per-tag access control in PI determining which users/applications can read or write specific process data points |

## Tools & Systems

- **OSIsoft PI Server**: Industry-leading process historian by AVEVA (formerly OSIsoft) used in 90%+ of large industrial facilities
- **AVEVA Historian**: Time-series database for process data with SQL-like query interface
- **Waterfall Security**: Hardware data diode for unidirectional historian replication
- **PI Vision**: Web-based visualization tool for PI data, deployed in DMZ for enterprise access

## Output Format

```
Historian Security Assessment Report
=====================================
Historian: [Type and Version]
Server: [Hostname/IP]
Network Zone: [Purdue Level]

AUTHENTICATION:
  PI Trust entries: [N] (should be 0)
  Default accounts: [enabled/disabled]
  Windows auth: [enabled/disabled]

NETWORK EXPOSURE:
  Open ports: [list]
  Unnecessary services: [list]

DATA INTEGRITY:
  Audit trail: [enabled/disabled]
  Backup tested: [date]

DMZ REPLICATION:
  Method: [PI-to-PI / Data Diode / VPN]
  Direction: [Unidirectional / Bidirectional]
```
