---
name: intel-analysis-general-overview
description: "Intel Analysis General Overview."
domain: cybersecurity
---

--|
| **PIR** | Priority Intelligence Requirement — specific, actionable question driving intelligence collection and analysis |
| **Intelligence Lifecycle** | Six-phase iterative process: Planning → Collection → Processing → Analysis → Dissemination → Feedback |
| **Strategic Intelligence** | Long-term threat trend analysis for executive decision-making; time horizon 6–24 months |
| **Operational Intelligence** | Campaign-level analysis for security program decisions; time horizon 1–6 months |
| **Tactical Intelligence** | Specific IOCs and TTPs for immediate detection and blocking; time horizon hours to days |
| **FIRST CTI-SIG** | Forum of Incident Response and Security Teams — CTI Special Interest Group maturity model |

## Tools & Systems

- **ThreatConnect**: TIP with built-in intelligence lifecycle workflows, PIR tracking, and stakeholder reporting dashboards
- **MISP**: Open-source TIP supporting intelligence lifecycle from collection through sharing
- **OpenCTI**: Graph-based CTI platform with workflow management for intelligence products
- **Recorded Future**: Commercial platform with structured intelligence reports aligned to the intelligence lifecycle

## Common Pitfalls

- **Collection without direction**: Ingesting every available feed without PIRs produces data overload and no actionable intelligence.
- **Missing feedback loops**: Without structured feedback, CTI teams produce reports that don't meet stakeholder needs and lose organizational relevance.
- **Tactical-only focus**: Overemphasis on IOC sharing neglects strategic intelligence that informs security investment and risk decisions.
- **No metrics program**: Cannot demonstrate CTI program value without tracking detection contributions, true positive rates, and stakeholder satisfaction.
- **Underfunded collection**: PIRs cannot be answered without appropriate collection sources; document and escalate gaps rather than producing low-confidence estimates.
