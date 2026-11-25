# Incident Response & Digital Forensics Skill

This skill enables Claude to guide structured incident response operations aligned with NIST SP 800-61 and SANS PICERL framework.

## Key Capabilities

**IR Playbook Creation** — Generates detailed playbooks for ransomware, phishing, data breaches, and other incident types with role assignments, severity classification, and phase-based checklists.

**Evidence Collection** — Follows order of volatility (memory → disk) with chain of custody documentation. Provides platform-specific commands for Windows and Linux systems.

**Forensic Timelines** — Constructs incident timelines from logs, file system artifacts, and registry data. Normalizes timestamps to UTC and maps activity to the kill chain.

**Memory Forensics** — Interprets Volatility output to identify process injection, hidden processes, network connections, and other malware indicators in RAM.

**Post-Incident Reports** — Produces management-ready reports covering root cause analysis, compliance notification requirements, remediation actions, and lessons learned.

## PICERL Phases

The framework structures response around six phases: Preparation, Identification, Containment, Eradication, Recovery, and Lessons Learned — with defined timelines and task ownership for each.

## Prerequisites

Requires pyyaml, jinja2, pandas, and python-dateutil. Recommended tools include Volatility 3, Autopsy, plaso, KAPE, and Velociraptor.
