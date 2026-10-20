<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-4ykutg
description: CTF writeups and security challenges by 4ykutG.
---

# Writeups by 4ykutG

Source repository: `/repos/4ykutG`

## Repository Index

- PentestPilot/readme.md

## Writeup Content


### File: PentestPilot/readme.md

#  PentestPilot

**PentestPilot** is an automated web vulnerability reconnaissance tool that helps penetration testers quickly identify common security issues such as SQL Injection, XSS, missing security headers, exposed directories, and subdomains.  
Modular, customizable, and lightweight — your one-command reconnaissance co-pilot.

---

##  Disclaimer

This project is intended **solely for educational, research, and authorized penetration testing purposes**.  
Any unauthorized use of this tool against systems without explicit permission is **strictly prohibited** and may violate local, national, or international laws.

The developer assumes **no responsibility** for any misuse, damage, or legal consequences resulting from the use of this software.

Use responsibly. You are solely accountable for your actions.


##  Features

- ✅ SQL Injection Testing
- ✅ XSS (Reflected) Detection
- ✅ HTTP Security Headers Analysis
- ✅ Directory Brute-Force Discovery
- ✅ Subdomain Enumeration
- ✅ Modular architecture (easy to expand)
- ✅ CLI support for targeted scans
- ✅ Custom payload file support

---

##  Setup

```bash
git clone https://github.com/4ykutG/PentestPilot.git
cd PentestPilot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
##  usage

python webapp.py

