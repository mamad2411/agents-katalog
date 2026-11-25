---
name: ics-sector-oil-gas-assess
description: "Ics Sector Oil Gas Assess."
domain: cybersecurity
---

|
| API 1164 | American Petroleum Institute standard for Pipeline SCADA Security providing a risk-based framework for cybersecurity of pipeline control systems |
| TSA Pipeline Security Directives | Mandatory cybersecurity requirements issued by TSA for pipeline operators including SD-01 (reporting) and SD-02 (implementation) |
| Custody Transfer | Transfer of ownership of petroleum products between parties, requiring metering system integrity to prevent financial fraud |
| DCS | Distributed Control System used in refineries for continuous process control with redundant controllers and operator stations |
| Remote Terminal Unit (RTU) | Field device at remote pipeline sites that collects sensor data and executes control commands, communicating via radio/satellite |
| Safety Integrity Level (SIL) | IEC 61511 rating for safety instrumented functions, with SIL 1-4 defining probability of failure on demand |
| HAZOP | Hazard and Operability Study identifying potential hazards in process design; cybersecurity should be integrated with HAZOP results |

## Tools & Systems

- **Dragos Platform**: OT cybersecurity platform with specific detection for oil and gas threat groups (XENOTIME, KAMACITE, ERYTHRITE)
- **Claroty xDome**: Comprehensive asset discovery and vulnerability management for oil and gas OT environments
- **Nozomi Guardian**: Network monitoring with support for pipeline protocols (DNP3, Modbus, IEC 60870-5-104)
- **Honeywell Forge Cybersecurity**: OT security platform designed for Honeywell DCS environments common in refineries

## Output Format

```
Oil & Gas Cybersecurity Assessment Report
==========================================
Facility: [Name]
Segment: Upstream / Midstream / Downstream
Date: YYYY-MM-DD
Standards: API 1164, TSA SD-02, IEC 62443

FINDINGS:
  Critical: [N]  High: [N]  Medium: [N]  Low: [N]

COMPLIANCE STATUS:
  TSA SD-02: [N]% compliant
  API 1164: [N]% compliant
  IEC 62443: [N]% compliant
```
