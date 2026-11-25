<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-exorcist1234
description: CTF writeups and security challenges by Exorcist1234.
---

# Writeups by Exorcist1234

Source repository: `/repos/Exorcist1234`

## Repository Index

- web-pentest-reports/README.md
- web-pentest-reports/tools/security-headers-visualizer/README.md

## Writeup Content


### File: web-pentest-reports/README.md

# Web Application Security Writeups — Exorcist

This repository contains detailed writeups from web application penetration tests, bug bounty programs, security assessments, and CTF challenges.

---

## Contact

📧 Email: [Excorcist_sec@proton.me](mailto:Excorcist_sec@proton.me)  
🔗 GitHub: https://github.com/Exorcist1234

---

## Contents

### Bug Bounty and Security Assessments

- [User Enumeration Vulnerability (Out-of-Scope)](./bounty/report-user-enumeration.pdf)
- [Other Bug Bounty](./bug-bounty/)

### Labs and Exercises

- [OWASP Juice Shop](./labs/report-juice-shop.pdf) 
- [Other Labs](./labs/)

### Tools

- [Security Headers Visualizer](./tools/security-headers-visualizer/)
  - A Python-based tool that scans websites for common security headers (CSP, HSTS, X-Frame-Options, Referrer-Policy, Permissions-Policy) and generates a clear, color-coded report.
  - Designed for educational purposes and penetration testing labs.
  - Includes example reports and screenshots in the repository.

### CTF Writeups


---

## Disclaimer

Reports are provided for educational and professional reference.  
Sensitive information has been redacted or anonymized to respect confidentiality and disclosure policies.

---

## About me

I focus on web application security through penetration testing and responsible vulnerability disclosure.  
This repository reflects my experience and approach in web security.

---



### File: web-pentest-reports/tools/security-headers-visualizer/README.md

Security Headers Visualizer

A small Python script that checks a website for important security headers and shows them in a clear, color-coded table

It checks for headers like Content-Security-Policy (CSP), Strict-Transport-Security (HSTS), X-Frame-Options, Referrer-Policy and Permissions-Policy. The script shows which headers are present and which are missing, works with HTTPS and HTTP, and can be run directly from the console

To use it, first clone the repository with git clone https://github.com/Exorcist1234/web-pentest-reports.git then go to the script folder with cd web-pentest-reports/tools/security-headers-visualizer/src. Install the dependencies by running pip install requests rich. Run the script with python "Security Headers Visualizer.py" and enter the website URL to see the table with the headers

Screenshots of the script in action are in the examples/ folder, there are two images included

Use this script only on websites where you have permission to test or on your own labs
Important

Use only on websites where you have permission to test, or on your own labs.

