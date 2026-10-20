---
name: ics-architecture-purdue-configure
description: "| | Purdue Model (PERA) | Hierarchical reference architecture organizing industrial networks into levels 0-5 based on function and trust | | Level 3."
domain: cybersecurity
---

|
| Purdue Model (PERA) | Hierarchical reference architecture organizing industrial networks into levels 0-5 based on function and trust |
| Level 3.5 DMZ | Demilitarized zone between IT (Level 4) and OT (Level 3), where all cross-boundary data exchange occurs |
| Defense in Depth | Layered security approach requiring attackers to breach multiple boundaries to reach critical control systems |
| Data Diode | Hardware-enforced unidirectional communication device ensuring data flows only from OT to IT, never reverse |
| Zone | Logical grouping of assets sharing common security requirements as defined by IEC 62443 |
| Conduit | Controlled communication path between zones with defined security policies |

## Common Scenarios

### Scenario: Flat OT Network Remediation

**Context**: An audit reveals that enterprise IT systems can directly communicate with PLCs on the control network. There is no DMZ and no firewall between IT and OT.

**Approach**:
1. Perform full traffic analysis to identify all legitimate data flows crossing IT/OT boundary
2. Design DMZ architecture with historian replica, jump server, and patch staging
3. Deploy industrial firewall between IT and DMZ (north firewall) and between DMZ and OT (south firewall)
4. Migrate data flows one at a time: start with historian replication through DMZ
5. Implement jump server for remote access, deprecating direct RDP to OT systems
6. Block direct IT-to-OT traffic on the north firewall after all flows migrate through DMZ
7. Validate with penetration test from IT network confirming no direct path to Level 1 controllers

**Pitfalls**: Do not cut over all traffic simultaneously -- migrate flow by flow with rollback plans. Legacy OT systems may use protocols that cannot traverse firewalls doing DPI; test thoroughly in a lab first. Never deploy the DMZ during active production without an agreed maintenance window.

## Output Format

```
PURDUE MODEL SEGMENTATION REPORT
====================================
Assessment Date: YYYY-MM-DD
Facility: [Plant Name]

CURRENT STATE:
  Network Type: [Flat/Partially segmented/Fully segmented]
  IT-OT Boundary: [None/Firewall/DMZ with dual firewall]
  Direct IT-to-PLC paths: [count]

RECOMMENDED ARCHITECTURE:
  Level 0-1: VLAN 110 (Control Network)
  Level 2:   VLAN 120 (Supervisory Network)
  Level 3:   VLAN 130 (Operations Network)
  Level 3.5: VLAN 150 (IT/OT DMZ)
  Level 4-5: VLAN 200+ (Enterprise)

DMZ COMPONENTS:
  - Historian Replica Server
  - Jump Server (MFA-enabled)
  - Patch Staging Server
  - AV Relay Server

FIREWALL RULES: [count] rules generated
MIGRATION STEPS: [count] phases planned
```
