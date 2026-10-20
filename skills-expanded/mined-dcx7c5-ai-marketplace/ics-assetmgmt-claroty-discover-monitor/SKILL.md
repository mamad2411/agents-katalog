---
name: ics-assetmgmt-claroty-discover-monitor
description: "Ics Ics Assetmgmt Claroty Discover Monitor."
domain: cybersecurity
---

|
| Passive Monitoring | Observing mirrored network traffic via SPAN/TAP without injecting packets, safe for all OT devices |
| Active Querying | Sending native protocol requests to extract detailed device information; requires careful scheduling |
| Claroty Edge | Claroty's safe active discovery collector that uses native industrial protocols rather than IT scanning |
| Purdue Level | Hierarchical classification of industrial network assets from Level 0 (physical process) to Level 5 (enterprise) |
| Shadow OT Device | Asset connected to the OT network that is not documented in the asset management system |
| xDome | Claroty's SaaS-based cyber-physical systems protection platform providing visibility, risk management, and threat detection |

## Common Scenarios

### Scenario: Brownfield Factory Asset Discovery

**Context**: A manufacturing plant with 20 years of equipment additions needs a complete OT asset inventory for an IEC 62443 risk assessment. No accurate asset records exist.

**Approach**:
1. Deploy Claroty sensors on SPAN ports at each major network segment (control, supervisory, DMZ)
2. Allow passive monitoring for 2-4 weeks to capture all regular communication patterns
3. Schedule Claroty Edge active queries during a planned maintenance window
4. Export discovered inventory and categorize assets by Purdue level, vendor, and criticality
5. Cross-reference against any existing documentation (P&ID diagrams, network drawings)
6. Identify shadow devices and initiate a review process with plant operations
7. Feed validated inventory into IEC 62443 zone and conduit risk assessment

**Pitfalls**: Do not rush active discovery before passive monitoring has captured baseline traffic patterns. Never use IT vulnerability scanners (Nessus active scans) directly against PLCs or RTUs -- this can crash legacy controllers. Always exclude Safety Instrumented Systems (SIS) from active queries.

## Output Format

```
ICS ASSET DISCOVERY REPORT
============================
Date: YYYY-MM-DD
Platform: Claroty xDome
Site: [Site Name]

DISCOVERY SUMMARY:
  Total Assets Discovered: [count]
  New Assets (not in CMDB): [count]
  High-Risk Assets: [count]

PURDUE LEVEL DISTRIBUTION:
  Level 0 (Process): [count] assets
  Level 1 (Control): [count] assets
  Level 2 (Supervisory): [count] assets
  Level 3 (Operations): [count] assets
  Level 3.5 (DMZ): [count] assets
  Level 4-5 (Enterprise): [count] assets

TOP VENDORS:
  1. [Vendor] - [count] devices
  2. [Vendor] - [count] devices

CRITICAL FINDINGS:
  - [Shadow device description]
  - [End-of-life firmware finding]
  - [Unencrypted protocol concern]
```
