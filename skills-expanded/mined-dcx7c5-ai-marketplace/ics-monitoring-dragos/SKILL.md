---
name: ics-monitoring-dragos
description: "Ics Ics Monitoring Dragos."
domain: cybersecurity
---

|
| Dragos Platform | Purpose-built OT cybersecurity platform with asset visibility, threat detection, and vulnerability management for ICS environments |
| Knowledge Pack | Dragos threat intelligence update containing detection analytics for new threats, malware, and vulnerability exploits specific to ICS |
| SiteStore | Dragos central management server aggregating data from all deployed sensors across a site |
| VOLTZITE | Dragos-tracked threat group targeting energy sector OT environments, exfiltrating GIS data and ICS network diagrams |
| PIPEDREAM/INCONTROLLER | Modular ICS attack framework developed by CHERNOVITE, targeting Schneider/OMRON PLCs and OPC UA servers |
| Neighborhood Keeper | Dragos community defense program sharing anonymized threat data across participating OT environments |

## Common Scenarios

### Scenario: Detecting VOLTZITE Reconnaissance in Energy Utility

**Context**: A Dragos sensor deployed at an electric utility detects unusual OPC UA browsing activity and exfiltration of device configuration data from an engineering workstation.

**Approach**:
1. Review the Dragos notification for MITRE ATT&CK ICS technique mapping
2. Identify the source host performing OPC UA browsing (check if it is an authorized engineering workstation)
3. Check Dragos threat intelligence correlation for VOLTZITE TTPs
4. Examine the scope of data accessed (GIS data, network diagrams, ICS configuration files)
5. Isolate the compromised workstation from the OT network
6. Check for lateral movement indicators to other OT systems
7. Engage Dragos Professional Services if threat group attribution is confirmed
8. Report to CISA as a critical infrastructure cyber incident

**Pitfalls**: Do not ignore OPC UA browsing alerts as false positives -- VOLTZITE specifically uses this technique for pre-positioning. Ensure Dragos Knowledge Packs are current to detect the latest VOLTZITE indicators. Do not reimage the compromised workstation before collecting forensic evidence.

## Output Format

```
DRAGOS OT MONITORING DEPLOYMENT REPORT
==========================================
Site: [Site Name]
Date: YYYY-MM-DD

SENSOR DEPLOYMENT:
  Total Sensors: [count]
  Operational: [count]
  Coverage: [percentage of OT segments monitored]

ASSET VISIBILITY:
  Total OT Assets: [count]
  PLCs: [count] | HMIs: [count] | Network Devices: [count]
  Protocols: [list]

THREAT DETECTION:
  Active Threat Groups Relevant: [count]
  Detection Analytics Loaded: [count]
  Alerts (Last 30 Days): [count by severity]

SIEM INTEGRATION:
  Status: [Connected/Disconnected]
  Events Forwarded (Last 24h): [count]
```
