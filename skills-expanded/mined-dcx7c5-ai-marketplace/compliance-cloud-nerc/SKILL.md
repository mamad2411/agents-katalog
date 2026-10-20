---
name: compliance-cloud-nerc
description: "Compliance Cloud Nerc."
domain: cybersecurity
---

|
| BES Cyber System | Group of one or more BES Cyber Assets that perform a reliability function for the Bulk Electric System |
| Electronic Security Perimeter (ESP) | Logical border surrounding a network containing BES Cyber Systems, with all traffic flowing through Electronic Access Points |
| Electronic Access Point (EAP) | Interface on the ESP boundary that controls traffic flowing in and out of the ESP |
| Intermediate System | System used for remote access that prevents direct connectivity to BES Cyber Assets (jump server) |
| Transient Cyber Asset | Device that is directly connected to a BES Cyber System for less than 30 consecutive calendar days (laptops, USB drives) |
| NERC Glossary | Official definitions used in CIP standards; precise terminology required for compliance |

## Tools & Systems

- **Tripwire Enterprise**: Configuration compliance monitoring and file integrity monitoring for CIP-010 baseline management
- **Splunk with CIP Content Pack**: SIEM with pre-built CIP-007 security event monitoring dashboards and alerts
- **Carbon Black App Control**: Application allowlisting for HMI stations and BES cyber assets (CIP-007 R3)
- **Trellix/McAfee ePO**: Endpoint protection with OT-optimized scanning policies for BES cyber assets

## Output Format

```
NERC CIP Compliance Assessment Report
=======================================
Entity: [Registered Entity Name]
Date: YYYY-MM-DD
Standards: CIP-002 through CIP-014

BES CYBER SYSTEM CATEGORIZATION:
  High Impact: [N] systems
  Medium Impact: [N] systems
  Low Impact: [N] systems

COMPLIANCE STATUS BY STANDARD:
  CIP-002: [Compliant/Partial/Non-Compliant]
  CIP-005: [Status] - [N] gaps identified
  CIP-007: [Status] - [N] gaps identified
  CIP-010: [Status] - [N] gaps identified
  CIP-013: [Status] - [N] gaps identified
```
