---
name: intel-analysis-cyber
description: "Intel Analysis Cyber."
domain: cybersecurity
---

--|
| **Kill Chain** | Sequential model of adversary intrusion phases; breaking any link theoretically stops the attack |
| **Courses of Action (COA)** | Defensive responses mapped to each kill chain phase: detect, deny, disrupt, degrade, deceive, destroy |
| **Beaconing** | Regular, periodic C2 check-in pattern from compromised host to adversary server; detectable by frequency analysis |
| **Phase Completion** | Adversary successfully finishes a kill chain phase and progresses to the next; defense-in-depth aims to prevent this |
| **Intelligence Gain/Loss** | Analysis of whether detecting at Phase 5 (vs. Phase 3) reduced intelligence about adversary capabilities or intent |

## Tools & Systems

- **MITRE ATT&CK Navigator**: Overlay kill chain phases with ATT&CK technique coverage for integrated analysis
- **Elastic Security EQL**: Event Query Language for querying multi-phase attack sequences in Elastic SIEM
- **Splunk ES**: Timeline visualization and correlation searches for kill chain phase sequencing
- **MISP**: Kill chain tagging via galaxy clusters for structured incident event documentation

## Common Pitfalls

- **Linear assumption**: Adversaries don't always progress linearly — they may skip phases (weaponization already complete from previous campaign) or loop back (re-establish C2 after detection).
- **Ignoring Phases 1 and 2**: Reconnaissance and weaponization occur before the defender has visibility. Intelligence about these phases requires external sources (OSINT, threat intelligence).
- **Missing insider threats**: The kill chain was designed for external adversaries. Insider threats may skip directly to Phase 7 without traversing earlier phases.
- **Confusing with ATT&CK tactics**: The 7-phase kill chain and 14 ATT&CK tactics are complementary but not directly equivalent. Maintain distinction to prevent analytic confusion.
