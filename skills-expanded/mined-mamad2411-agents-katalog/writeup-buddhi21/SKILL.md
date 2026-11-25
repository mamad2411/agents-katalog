<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-buddhi21
description: CTF writeups and security challenges by Buddhi21.
---

# Writeups by Buddhi21

Source repository: `/repos/Buddhi21`

## Repository Index

- Bug-Bounty-Report/README.md

## Writeup Content


### File: Bug-Bounty-Report/README.md

# Bug Bounty Report - Responsible Disclosure

This repository documents a **focused web security assessment conducted on a single authorized domain**, resulting in the identification of **two security misconfigurations**.  
The assessment was performed in accordance with ethical hacking practices and responsible disclosure guidelines.

This work demonstrates hands-on experience in **web application security testing**, vulnerability analysis, and professional reporting aligned with bug bounty standards and academic evaluation.

## Scope of Assessment

- **Target:** Single authorized domain  
- **Assessment Type:** Web security configuration review  
- **Testing Method:** Manual analysis supported by security testing tools  

## Vulnerabilities Identified

The following vulnerabilities were confirmed:

1. **Missing Anti-Clickjacking Header**  
   - Absence of `X-Frame-Options` or equivalent frame protection  
   - Application susceptible to clickjacking attacks  

2. **Missing Content Security Policy (CSP) Header**  
   - No `Content-Security-Policy` header defined  
   - Increased risk of XSS and content injection attacks  

## What the Report Includes

- Executive Summary  
- Methodology  
  - Tools Utilized  
  - Testing Approach  
- Vulnerability Description  
- Vulnerability Discovery Process  
- Severity Rating  
- Proof of Concept (PoC)  
- Exploitation  
  - Demonstration of steps an attacker could take to exploit the vulnerability  
- Impact Assessment  
- Recommended Remediation Steps  
- Responsible Disclosure Notes  

## Tools and Technologies Used

- Burp Suite  
- OWASP ZAP  
- PortSwigger Web Security Labs  
- Nmap  
- Nikto  
- Amass  
- Sublist3r  
- Browser Developer Tools  

## Standards & Best Practices Referenced

- OWASP Secure Headers Project  
- OWASP Top 10  
- General Web Security Best Practices  

## Academic Evaluation

- **Assessment Score:** 87 / 100  

> All testing was conducted strictly within permitted scope and followed responsible disclosure principles.  
> No exploitation beyond proof-of-concept validation was performed.

## Disclaimer

This repository is intended strictly for **educational and ethical security research purposes**.  
The author does not support or encourage unauthorized testing or misuse of the information provided.

> ⚠️ GitHub may not render PDF files inline.  
> Please download the PDF to view the full report.


