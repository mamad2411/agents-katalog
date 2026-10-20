---
name: intel-threat-actor-profile-hunt
description: "Intel Threat Actor Profile Hunt."
domain: cybersecurity
---

--|
| **Finished Intelligence** | Analyzed, contextualized intelligence product ready for consumption by decision-makers; distinct from raw collected data |
| **Key Judgment** | Primary analytical conclusion of a report; clearly stated in opening paragraph |
| **TLP** | Traffic Light Protocol — FIRST-standard classification system for controlling intelligence sharing scope |
| **ICD 203** | Intelligence Community Directive 203 — US government standard for analytic standards including confidence language |
| **Flash Report** | Urgent, time-sensitive intelligence notification for imminent threats; prioritizes speed over depth |
| **Intelligence Gap** | Area where collection is insufficient to answer a PIR; should be explicitly documented in reports |

## Tools & Systems

- **ThreatConnect Reports**: Built-in report templates with ATT&CK mapping, IOC tables, and stakeholder distribution controls
- **Recorded Future**: Pre-built intelligence report templates with automated sourcing from proprietary datasets
- **OpenCTI Reports**: STIX-based report objects with linked entities for structured finished intelligence
- **Microsoft Word/Confluence**: Common report delivery formats; use organization-approved templates with TLP headers

## Common Pitfalls

- **Writing for analysts instead of the audience**: Technical detail appropriate for SOC analysts overwhelms executives. Maintain strict audience segmentation.
- **Omitting confidence levels**: Statements presented without confidence qualifiers appear as established facts when they may be low-confidence assessments.
- **Intelligence without recommendations**: Reports that describe threats without prescribing actions leave stakeholders without direction.
- **Stale intelligence**: Publishing a report on a threat campaign that was resolved 2 weeks ago creates alarm without utility. Include freshness dating on all claims.
- **Over-classification**: Applying TLP:RED to information that could be TLP:GREEN impedes community sharing and limits defensive value across the sector.
