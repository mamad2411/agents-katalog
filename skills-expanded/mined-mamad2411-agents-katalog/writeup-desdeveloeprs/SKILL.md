<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-desdeveloeprs
description: CTF writeups and security challenges by DesDeveloeprs.
---

# Writeups by DesDeveloeprs

Source repository: `/repos/DesDeveloeprs`

## Repository Index

- Pentesting-Reports/README.md

## Writeup Content


### File: Pentesting-Reports/README.md

BRICK PRESS MEDIA INCIDENT RESPONSE
====================================

TryHackMe Challenge Documentation
Author: DesSecurity
Date: 13th OCT 2025

OVERVIEW
--------
This repository contains my complete investigation of the Brick Press Media 
security breach as part of TryHackMe's incident response challenge. The 
scenario involved a compromised web server with cryptocurrency mining 
operations and persistent backdoors.

INVESTIGATION FINDINGS
----------------------
- Initial Access: WordPress Bricks Builder RCE (CVE-2024-25600)
- Persistence: Malicious systemd service (ubuntu.service)
- Backdoor: /lib/NetworkManager/nm-inet-dialog
- Cryptocurrency Miner: Logged in /lib/NetworkManager/inet.conf
- Wallet Address: bc1qyk79fcp9hd5kreprce89tkh4wrtl8avt4l67qa
- Threat Actor: LockBit ransomware group

FILES INCLUDED
--------------
- Incident_Response_Report_v2.pdf
- bricks_rce.dox

SKILLS DEMONSTRATED
-------------------
- Web Application Penetration Testing
- Digital Forensics & Incident Response
- Malware Analysis & Persistence Detection
- Threat Intelligence & Attribution
- Professional Security Reporting

NOTE
----
This was completed as part of TryHackMe's educational platform.
All infrastructure and scenarios are part of the THM environment.

and the payload is a modification from :https://github.com/K3ysTr0K3R/CVE-2024-25600-EXPLOIT
NOT MY TOOL

CONTACT
-------
https://github.com/DesDeveloeprs

