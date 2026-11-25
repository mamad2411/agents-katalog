<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-efajtahamidrifat
description: CTF writeups and security challenges by EfajTahamidRifat.
---

# Writeups by EfajTahamidRifat

Source repository: `/repos/EfajTahamidRifat`

## Repository Index

- FRAGLET_THE_ETHICAL_DEMON/README.md

## Writeup Content


### File: FRAGLET_THE_ETHICAL_DEMON/README.md

###############################################################################
# 🕷️  FRAGLET – All-In-One Bug Hunting & Vulnerability Scanner
###############################################################################

FRAG (aka `bug_hunting.sh`) is a PRIVATE high-risk security toolkit created
for **authorized penetration testing and responsible bug bounty research only**.

This repository contains powerful open-source scanners bundled into a single
automated workflow that performs reconnaissance, vulnerability discovery, and
color-coded PDF reporting.

-------------------------------------------------------------------------------
⚠️  LEGAL WARNING – READ BEFORE CLONING OR EXECUTING
-------------------------------------------------------------------------------
FRAGLET is a precision weapon, **not a toy**.  
By downloading or running this code you acknowledge and accept the following:

1. OWNER PERMISSION REQUIRED
   • You must own the target or hold a SIGNED, VERIFIABLE authorization.
   • “Public website” status or verbal consent is NOT valid permission.

2. UNAUTHORIZED USE IS A CRIME
   Running FRAG on systems you do not control may violate:
       - Computer Fraud and Abuse Act (USA)
       - Computer Misuse Act (UK)
       - GDPR / EU Data Protection Laws
       - Local cybercrime statutes in nearly every country
   Penalties can include HEAVY FINES, CIVIL LAWSUITS, EQUIPMENT SEIZURE,
   and MULTI-YEAR PRISON SENTENCES.

3. NO WARRANTY OR LIABILITY
   Author Efaj Tahamid Rifat provides FRAG AS IS with NO WARRANTY and
   accepts ZERO responsibility for:
       - Data loss or service interruption
       - Legal actions or criminal charges
       - Misuse by third parties

4. PRIVATE REPOSITORY STATUS
   • Redistribution, resale, or public forks are strictly forbidden.
   • Legal takedown (DMCA or equivalent) will be enforced if necessary.

5. DATA OWNERSHIP
   • All output remains LOCAL ONLY.
   • You are solely responsible for protecting reports and for ensuring they are
     shared only with authorized parties.

-------------------------------------------------------------------------------
FEATURES
-------------------------------------------------------------------------------
* Environment auto-detection (Termux / Linux / Google Colab)
* Automated installation of all dependencies
* Multi-stage recon & vulnerability scanning
* Color-coded PDF report:
       ✅ Green  → Low Risk
       ⚠️ Yellow → Medium Risk
       🔥 Red    → High Risk
* No credentials collected – everything runs on your machine

-------------------------------------------------------------------------------
TOOLCHAIN
-------------------------------------------------------------------------------
FRAG orchestrates a powerful stack of open-source security tools, including:

Recon:
    Subfinder, Amass, Assetfinder, WhatWeb
Directory/Endpoint Discovery:
    Dirsearch, FFUF, Gobuster
Vulnerability Scanners:
    Nikto, Wapiti, Nmap (vuln scripts), SSLScan
Web App Testing:
    SQLMap, XSStrike, WPScan
Network/Service:
    Masscan, Nmap
Misc:
    Httpx, Waybackurls

Tools may update or change as the project evolves.

-------------------------------------------------------------------------------
INSTALLATION
-------------------------------------------------------------------------------
```bash
git clone https://github.com/<YOUR-USERNAME>/frag.git
cd frag
chmod +x bug_hunting.sh


---

USAGE

./bug_hunting.sh

Interactive sequence: 1. Choose environment (Termux / Linux / Colab) 2. Confirm automatic installation of dependencies 3. Enter the target URL or domain (must be in your legal scope)

Reports are saved to: reports/<target>_report.pdf


---

AUTHORIZED USE CASES

Bug bounty programs with explicit written scope

Penetration testing of systems you own

Research or academic labs with signed authorization


If you do NOT have written authorization, STOP NOW and delete all copies.


---

AUTHOR

Efaj Tahamid Rifat Pentester | Web Developer | Ethical Hacker

“I build tools to close holes—what you do with them is on YOU.”


---

SUPPORT

If FRAG helps secure a system or earn a legitimate bounty, star the repo and responsibly share feedback.

Ignorance of the law is NOT a defense.

