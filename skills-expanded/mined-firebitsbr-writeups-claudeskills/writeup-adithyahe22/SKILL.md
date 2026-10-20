<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-adithyahe22
description: CTF writeups and security challenges by adithyaHE22.
---

# Writeups by adithyaHE22

Source repository: `/repos/adithyaHE22`

## Repository Index

- Bug-Bounty-Report/README.md

## Writeup Content


### File: Bug-Bounty-Report/README.md

# Bug-Bounty-Report
This repository contains a detailed web security assessment conducted as part of a responsible disclosure exercise. The report includes real-world vulnerabilities discovered on lankaecity.com and eshop.lk, following a structured manual penetration testing methodology.

## What’s Included
Each section of the report documents:

  - Vulnerability title & technical description
  - Reconnaissance and information-gathering process
  - Tools used during discovery
  - Step-by-step reproduction (PoC)
  - Screenshots & evidence
  - Impact analysis
  - Affected components/pages
  - Recommended mitigation strategies
  - Ethical testing and responsible disclosure notes

## Vulnerabilities Covered
The assessment includes three critical client-side vulnerabilities

    - Reflected Cross-Site Scripting (XSS)
    - Cross-Site Request Forgery (CSRF)
    - Clickjacking (UI Redressing)
		
These findings demonstrate how missing input validation, absent anti-CSRF protections, and lack of framing restrictions expose users to significant risk.

## Tools Used
During reconnaissance, enumeration, and exploitation, the following tools were used:
  - Burp Suite
  - Nmap
  - Nikto
  - Sublist3r
  - Amass
  - Dirsearch
  - WhatWeb
  - Wafw00f
  - Browser Developer Tools

## Methodology
The assessment followed an organized penetration testing workflow:

  - Reconnaissance
  - Scanning & enumeration
  - Vulnerability analysis
  - Manual exploitation with PoC
  - Reporting & remediation guidance

## Ethical Statement
All testing was non-destructive, educational, and conducted under strict ethical guidelines.
No data was modified, stolen, or misused.
Findings are intended for responsible disclosure and academic learning.

# Peer Review Score - 84 / 100

