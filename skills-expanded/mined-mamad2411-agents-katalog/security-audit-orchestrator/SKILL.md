---
name: security-audit-orchestrator
description: "Orchestrates a comprehensive security audit lifecycle: from threat modeling and requirement extraction to automated scanning (SAST, CodeQL) and deep-dive manual research (malware analysis, memory forensics, and reverse engineering). Keywords: security-audit, threat-modeling, sa_scan, codeql, malware-analysis, memory-forensics, reverse-engineering."
version: 1
created: "2024-05-22"
updated: "2024-05-22"
---

# Security Audit Orchestrator - End-to-End Vulnerability Research

This skill orchestrates a multi-layered security audit designed to identify, analyze, and mitigate vulnerabilities across the entire software stack. It combines automated high-speed scanning with deep-dive manual forensics.

## When to Use
Use this skill for:
- Full security audits of new repositories or production systems.
- Investigating specific security incidents or reports.
- Performing deep-dive analysis on suspicious binaries or memory dumps.
- Establishing a security baseline for a new product.

## The Orchestrated Workflow
This skill executes the following phases in sequence:

### Phase 1: Strategic Threat Modeling
1. **Threat Modeling**: Invoke `threat-modeling-expert` to identify trust boundaries and potential attack vectors.
2. **STRIDE Analysis**: Use `stride-analysis-patterns` to systematically categorize threats.
3. **Requirement Extraction**: Invoke `security-requirement-extraction` to turn identified threats into actionable security requirements.

### Phase 2: Automated Scanning
4. **SAST Scanning**: Invoke `security-scanning-security-sast` for rapid codebase vulnerability detection.
5. **CodeQL Analysis**: Invoke `codeql` for deep interprocedural data flow and taint tracking.
6. **Dependency Audit**: Use `security-scanning-security-dependencies` to identify supply chain risks.

### Phase 3: Deep-Dive Forensics & Manual Review
7. **Malware Analysis**: If suspicious binaries are found, invoke `malware-analyst` for triage.
8. **Memory Forensics**: Invoke `memory-forensics` to analyze memory dumps and artifact extraction.
9. **Reverse Engineering**: Use `reverse-engineer` for disassembly and protocol extraction on complex targets.

### Phase 4: Reporting & Mitigation
10. **Vulnerability Reporting**: Invoke `vuln-report` to compile all findings into a professional, actionable report.
11. **Mitigation Mapping**: Use `threat-mitigation-mapping` to prioritize and assign fixes.

## Freedom Calibration & Constraints
- **Constraint Level: High**
  - **Rigidity**: The sequence of scanning BEFORE deep-dive forensics is mandatory to prioritize findings.
  - **Freedom**: The specific analysis depth is left to the user (e.g., "quick scan" vs. "full forensic investigation").

## Critical Anti-Patterns (NEVER List)
| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** skip threat modeling | Starting with scanning without understanding the trust boundaries leads to noise. | Always perform threat modeling first. |
| **NEVER** ignore dependency risks | Automated scans often miss supply chain issues; always check dependencies. | Use `security-scanning-security-dependencies` in every audit. |
| **NEVER** report without mitigation | A vulnerability report without a remediation path is useless to developers. | Always use `vuln-report` and `threat-mitigation-mapping`. |

## Verification
1. A comprehensive threat model is documented.
2. SAST and CodeQL scans are completed and reviewed.
3. Deep-dive forensics (if needed) are performed on high-risk targets.
4. A final vulnerability report with prioritization is produced.
