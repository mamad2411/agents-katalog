---
name: ics-sector-power-grid-assess
description: "Ics Sector Power Grid Assess."
domain: cybersecurity
---

|
| IEC 61850 | International standard for communication networks and systems in substations, using GOOSE for protection signaling and MMS for SCADA data |
| GOOSE | Generic Object Oriented Substation Event - multicast protocol for fast peer-to-peer protection signaling between IEDs (< 4ms trip time) |
| MMS | Manufacturing Message Specification - client/server protocol for reading/writing IED data and operating circuit breakers |
| IEC 62351 | Security standard series for power system communication protocols providing authentication and encryption for IEC 61850, DNP3, and IEC 104 |
| ICCP/TASE.2 | Inter-Control Center Communications Protocol for data exchange between control centers of different utilities |
| Synchrophasor (PMU) | Phasor Measurement Unit providing time-synchronized voltage/current measurements at 30-60 samples/second for wide-area monitoring |

## Tools & Systems

- **Dragos Platform**: OT security platform with specific threat intelligence on power grid-targeting groups (ELECTRUM, KAMACITE)
- **SEL-3620 Ethernet Security Gateway**: Substation security device providing encryption, access control, and intrusion detection
- **GRIDsure**: Power grid cybersecurity assessment framework by Idaho National Laboratory
- **Wireshark with IEC 61850 Dissector**: Protocol analysis for GOOSE and MMS traffic in substations

## Output Format

```
Power Grid Cybersecurity Assessment Report
=============================================
Facility: [Name and Type]
NERC Registration: [Entity ID]
BES Impact Rating: [High/Medium/Low]

SUBSTATION FINDINGS: [N]
EMS/SCADA FINDINGS: [N]
COMMUNICATION FINDINGS: [N]

NERC CIP COMPLIANCE:
  CIP-002: [Status]
  CIP-005: [Status]
  CIP-007: [Status]
```
