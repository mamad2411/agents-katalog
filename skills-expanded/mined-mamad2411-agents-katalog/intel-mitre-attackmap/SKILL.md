---
name: intel-mitre-attackmap
description: "--| | **ATT&CK Technique** | Specific adversary method identified by T-number (e."
domain: cybersecurity
---

--|
| **ATT&CK Technique** | Specific adversary method identified by T-number (e.g., T1059 = Command and Scripting Interpreter) |
| **Sub-technique** | More granular variant of a technique (e.g., T1059.001 = PowerShell, T1059.003 = Windows Command Shell) |
| **Tactic** | Adversary goal category in ATT&CK: Initial Access, Execution, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Collection, C&C, Exfiltration, Impact |
| **Data Source** | ATT&CK v10+ component identifying telemetry required to detect a technique (e.g., Process Creation, Network Traffic) |
| **Coverage Score** | Numeric (0–100) representing detection completeness for a technique: 0=blind, 50=logged only, 100=alerted |
| **MITRE D3FEND** | Defensive countermeasure ontology complementing ATT&CK — maps defensive techniques to attack techniques they mitigate |

## Tools & Systems

- **ATT&CK Navigator**: Browser-based heatmap visualization tool for layering coverage scores and annotations on the ATT&CK matrix
- **mitreattack-python**: Official MITRE Python library for programmatic access to ATT&CK STIX data (techniques, groups, software, mitigations)
- **Atomic Red Team**: MITRE-aligned test library providing atomic test cases to validate detection for each technique
- **Sigma**: Detection rule format with ATT&CK tagging support; translatable to Splunk, Sentinel, QRadar, Elastic
- **ATT&CK Workbench**: Self-hosted ATT&CK knowledge base for organizations maintaining custom technique extensions

## Common Pitfalls

- **Over-claiming coverage**: Logging a data source (e.g., process creation events) does not mean the associated technique is detected — a rule must actually fire on malicious patterns.
- **Mapping at tactic level only**: Tagging a rule as "attack.execution" without a specific technique ID prevents granular gap analysis.
- **Ignoring sub-techniques**: Many adversaries use specific sub-techniques. Coverage of T1059 (parent) doesn't imply coverage of T1059.005 (Visual Basic).
- **Static mapping without updates**: ATT&CK releases major versions annually. Coverage maps go stale as techniques are added, revised, or deprecated.
- **Not mapping to adversary groups**: Generic coverage maps don't distinguish between techniques used by APTs targeting your sector vs. commodity malware.
