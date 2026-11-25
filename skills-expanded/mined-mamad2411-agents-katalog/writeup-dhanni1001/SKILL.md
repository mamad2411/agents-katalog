<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dhanni1001
description: CTF writeups and security challenges by dhanni1001.
---

# Writeups by dhanni1001

Source repository: `/repos/dhanni1001`

## Repository Index

- Pentesting-/README.md

## Writeup Content


### File: Pentesting-/README.md

# Pentesting-
Reconnaissance, exploitation, post-exploitation, CVSS scoring, and cleanup are all covered in this expert compilation of penetration testing reports from CTF laboratories and controlled environments. demonstrates useful pentesting techniques, equipment, and lucid technical documentation.

JOHN WICK CTF – Penetration Testing Report
This report presents a structured penetration testing walkthrough of the John Wick CTF machine, demonstrating a methodical approach to enumeration, exploitation, and privilege escalation. The assessment highlights how metadata leakage and misconfigured privileges can lead to full system compromise. The machine reinforces the importance of deep enumeration and careful analysis of seemingly insignificant artifacts.

Key Points:
1)Network scanning and service discovery using Nmap.
2)Web service enumeration and image file analysis.
3)Metadata extraction using ExifTool to uncover usernames.
4)SSH brute-force attack using Hydra with identified wordlists.
5)Successful user access through recovered credentials.
6)Privilege escalation via misconfigured sudo permissions.
7)Root shell obtained using FTP sudo abuse.

This report reflects real-world attack patterns and emphasizes secure configuration and metadata hygiene.

--------------------------------------------------------------------------

LIGHTHOUSE CTF – Vulnerability Exploitation Report
This report documents the exploitation of the Lighthouse CTF machine, focusing on information disclosure, credential recovery, and kernel-level privilege escalation. The assessment demonstrates how multiple low-risk issues can be chained together to achieve complete system compromise. It provides strong insight into Linux enumeration and exploit research techniques.

Key Points:
1)Target reconnaissance and open port discovery with Nmap.
2)Anonymous FTP access for hidden file enumeration.
3)Web directory discovery using robots.txt
4)Extraction of credentials from hidden VeraCrypt volume.
5)Base64 decoding to reveal SSH login details.
6)Initial access gained via SSH authentication.
7)Privilege escalation using the Dirty Pipe vulnerability (CVE-2022-0847)

This report highlights the risks of outdated kernels and weak access controls.

--------------------------------------------------------------------------

SPACEX CTF – Exploitation and Privilege Escalation Report
This report provides a detailed walkthrough of the SpaceX CTF machine, showcasing multiple exploitation techniques and post-exploitation methods. The assessment emphasizes unconventional access vectors, credential harvesting, and lateral user movement within Linux systems.

Key Points:
1)Network scanning and port identification using Nmap.
2)Initial access through Netcat on a non-standard service.
3)Bash shell execution and environment stabilization.
4)Discovery and execution of scripts exposing credentials.
5)SSH login using recovered user credentials.
6)Sensitive data extraction from command history files.
7)User pivoting and privilege escalation through misconfigurations.

This report demonstrates how improper scripting, credential handling, and logging practices can lead to full system compromise.

--------------------------------------------------------------------------

