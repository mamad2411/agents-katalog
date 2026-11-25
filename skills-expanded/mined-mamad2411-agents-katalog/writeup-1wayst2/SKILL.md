<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-1wayst2
description: CTF writeups and security challenges by 1wayst2.
---

# Writeups by 1wayst2

Source repository: `/repos/1wayst2`

## Repository Index

- Pentest-Reports/README.md
- Pentest-Reports/references/bibliography.md
- Pentest-Reports/references/mappings.md
- Pentest-Reports/templates/Findings-Template.md
- Pentest-Reports/templates/Industry-Pentest-Report.md
- Pentest-Reports/templates/SMEAC-Lab-Report.md
- Pentest-Reports/reports/hping3-pentest/hping3-SMEAC.md

## Writeup Content


### File: Pentest-Reports/README.md

# Pentest-Reports
Pentesting reports created through my own homelab setup
A clean, opinionated scaffold for organizing penetration testing and lab reports in GitHub.

## What's inside
- **templates/** — SMEAC lab report, industry-style pentest report, and a findings template
- **reports/** — put each engagement or lab here (auto-created by `scripts/new_report.sh`)
- **references/** — bibliography, mappings, and helpful links
- **scripts/** — helper to generate a new report folder structure
- **.gitignore** — ignores common binaries and large evidence artifacts

## Quick start
```bash
# 1) Create a new report folder (YYYY-MM-DD-your-slug)
scripts/new_report.sh 2025-09-07 my-first-lab

# 2) Edit the generated Report.md and add evidence to /Evidence
# 3) Track findings in Findings.md (or CSV/JSON if preferred)
# 4) Commit and push
git add .
git commit -m "Add 2025-09-07 my-first-lab report"
git push origin main
```

## Recommended workflow
1. Duplicate a template from **templates/** as your starting point.
2. Log steps and commands in the SMEAC **Execution** section while testing.
3. Write findings using **templates/Findings-Template.md** (one file per finding).
4. Export evidence (screens, logs, POCs) into the report's **Evidence/** folder.
5. Summarize in **Industry-Pentest-Report.md** style for stakeholders.

## Repo structure
```
pentest-reports-starter/
├─ README.md
├─ templates/
│  ├─ SMEAC-Lab-Report.md
│  ├─ Industry-Pentest-Report.md
│  └─ Findings-Template.md
├─ reports/
│  └─ 2025-09-07-my-first-lab/
│     ├─ Report.md
│     ├─ Findings.md
│     └─ Evidence/ (place screenshots, logs, pcap, etc.)
├─ references/
│  ├─ bibliography.md
│  └─ mappings.md
├─ scripts/
│  └─ new_report.sh
├─ .gitignore
└─ LICENSE
```

---

> Tip: keep sensitive evidence out of public repos. Use private repos or self-hosted Git with proper access control.



### File: Pentest-Reports/references/bibliography.md

# Bibliography
- PTES, NIST 800-115
- MITRE ATT&CK
- OWASP Testing Guide, ASVS
- CVSS v3.1 Specification
- CWE List



### File: Pentest-Reports/references/mappings.md

# Mappings
- **Discovery/Scanning** → ATT&CK Reconnaissance/Resource Development
- **Initial Access** → ATT&CK Initial Access
- **Privilege Escalation/Lateral Movement** → corresponding ATT&CK tactics
- **Reporting** → PTES Post-Engagement, NIST Documentation



### File: Pentest-Reports/reports/hping3-pentest/hping3-SMEAC.md

# SMEAC Lab Report
> Use this for hands-on labs or internal exercises. Keep it concise but evidence-driven.
> Be as descriptive as possible. The more information the better.

## Situation
- **Context/Targets:** Target is going to be a linux machine with the program ufw (uncomplicated firewall) installed, enabled, and running on a basic rules configuration. 
- **Assumptions/Constraints:** 
- **Tools/Images:** Parrot OS VM on my Qemu/KVM network named 1wayst2net using the tool hping3 (add brief network topology and ip addresses when available, ensure network is NAT).
- **Rules of Engagement:** The network 1wayst2net with the target machine will be the attack surface for this penetration test.

## Mission
- **Objective:** The objective of this test is to use hping3 to craft packets specifically for firewall evasion, steps used to prep for this test is going to be a thorough familiarization with the tool hping3.
- **Success Criteria:** Successful completion of the test is when specifically crafted TCP packets are sent and effectively evade strict firewall rules.

## Execution
- **Plan of Attack:** High-level sequence.
- **Timeline/Logbook:** Commands and observations with timestamps.
- **Discovery:** Hosts/services/users.
- **Exploitation:** Steps, payloads, creds.
- **Post-Exploitation:** Loot, persistence, lateral movement.
- **Evidence:** Link files in `Evidence/` with filenames and brief notes.

## Administration & Logistics
- **Resources:** (hardware, network, storage)
- **Data Handling:** classification, retention, and redaction plan.
- **Backup/Recovery:** checkpoints, snapshots.

## Command & Signal
- **Comms/Coordination:** who/when/how.
- **Change Control:** branching/tags for key milestones.

## After Action Review (AAR)
- **What was planned?**
- **What actually happened?**
- **What went well / needs improvement?**
- **Action Items:** owners & due dates.

## References
- Links, CVEs, docs used.



### File: Pentest-Reports/templates/Findings-Template.md

# Finding: <Title>
- **ID:** F-XXX
- **Severity:** Informational | Low | Medium | High | Critical
- **CVSS:** (e.g., 8.8 AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H)
- **CWE:** CWE-XXX
- **Affected Assets:** list
- **Status:** Open | In Progress | Remediated | Accepted

## Description
(What is the issue? Where does it occur? Root cause?)

## Impact
(What could an attacker achieve? Who/what is affected?)

## Evidence
(Embed screenshots or link to files under `Evidence/`)

## Reproduction Steps
(Exact steps/requests/commands with parameters)

## Remediation
(Specific, testable fix; include configuration/code examples if helpful)

## References
(CVEs, vendor docs, writeups)



### File: Pentest-Reports/templates/Industry-Pentest-Report.md

# Penetration Test Report (Industry Format)

## 1. Executive Summary
- **Overall Risk:** Low | Medium | High | Critical
- **Key Findings:** bullet list of top 3–5 issues and business impact
- **Remediation Timeline:** quick wins vs strategic items

## 2. Engagement Overview
- **Client/Environment:** 
- **Scope:** in-scope systems, IPs, applications
- **Out of Scope:**
- **Rules of Engagement:** dates, allowed test windows, accounts provided

## 3. Methodology
- Mapping to **PTES/NIST 800-115** and **ATT&CK** phases
- Tooling and versions, false-positive controls

## 4. Findings Summary
| ID | Title | Severity | Affected Assets | Status |
|---:|-------|:-------:|-----------------|--------|
| F-001 | Example finding | High | app01, db01 | Open |

## 5. Risk Rating
- Severity mapping (e.g., Informational/Low/Medium/High/Critical)
- Optional **CVSS v3.1** rubric and scoring

## 6. Recommendations
- Prioritized, actionable mitigations with owners

## 7. Detailed Findings
(One sub-section per finding; see Findings-Template.md for structure.)

## 8. Appendix
- Evidence index, credentials used, wordlists, payloads, affected versions
- Full tool output if needed (or link to `Evidence/` in the report folder)



### File: Pentest-Reports/templates/SMEAC-Lab-Report.md

# SMEAC Lab Report
> Use this for hands-on labs or internal exercises. Keep it concise but evidence-driven.

## Situation
- **Context/Targets:** (e.g., 10.10.10.0/24 lab on QEMU/Arch)
- **Assumptions/Constraints:** 
- **Tools/Images:** (OS build, kernel, VM topology, versions)
- **Rules of Engagement:** (timebox, scope, no-touch zones)

## Mission
- **Objective:** One sentence describing the goal.
- **Success Criteria:** What proves completion?

## Execution
- **Plan of Attack:** High-level sequence.
- **Timeline/Logbook:** Commands and observations with timestamps.
- **Discovery:** Hosts/services/users.
- **Exploitation:** Steps, payloads, creds.
- **Post-Exploitation:** Loot, persistence, lateral movement.
- **Evidence:** Link files in `Evidence/` with filenames and brief notes.

## Administration & Logistics
- **Resources:** (hardware, network, storage)
- **Data Handling:** classification, retention, and redaction plan.
- **Backup/Recovery:** checkpoints, snapshots.

## Command & Signal
- **Comms/Coordination:** who/when/how.
- **Change Control:** branching/tags for key milestones.

## After Action Review (AAR)
- **What was planned?**
- **What actually happened?**
- **What went well / needs improvement?**
- **Action Items:** owners & due dates.

## References
- Links, CVEs, docs used.

