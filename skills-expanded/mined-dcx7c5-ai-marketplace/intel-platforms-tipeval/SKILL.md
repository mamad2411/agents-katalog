---
name: intel-platforms-tipeval
description: "Intel Platforms Tipeval."
domain: cybersecurity
---

--|
| **TIP** | Threat Intelligence Platform — software for collecting, processing, analyzing, and disseminating cyber threat intelligence |
| **TAXII Server** | Component of a TIP that serves STIX bundles to consuming systems on request |
| **TC Exchange** | ThreatConnect's commercial marketplace for pre-built feed integrations and app connectors |
| **Multi-tenancy** | TIP capability to serve multiple organizational units or customers with isolated data environments |
| **Deduplication** | Process of identifying and merging duplicate indicators within a TIP to reduce analyst noise |

## Tools & Systems

- **MISP**: Open-source TIP used by 6,000+ organizations; strongest ISAC/government community integration
- **OpenCTI**: Modern open-source TIP with native STIX 2.1 and graph-based analysis
- **ThreatConnect**: Enterprise commercial TIP with lifecycle management and SOAR playbook integration
- **Anomali ThreatStream**: Commercial TIP with strong Splunk ecosystem integration
- **EclecticIQ**: Commercial TIP with ATT&CK-centric workflow design

## Common Pitfalls

- **Selecting TIP before defining requirements**: Technology selection before use case definition leads to expensive mismatches.
- **Underestimating administration burden**: MISP and OpenCTI require dedicated admin time (minimum 0.25 FTE); budget accordingly.
- **Ignoring data migration costs**: Moving historical intelligence from one TIP to another is costly and often impractical for legacy systems.
- **Not testing SIEM integration in PoC**: TIP value depends heavily on downstream integration quality; always test SIEM/SOAR connectivity during evaluation.
