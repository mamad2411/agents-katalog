<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-abduu-chaker
description: CTF writeups and security challenges by abduu-chaker.
---

# Writeups by abduu-chaker

Source repository: `/repos/abduu-chaker`

## Repository Index

- recon-toolkit/README.md

## Writeup Content


### File: recon-toolkit/README.md

# Recon & API Security Toolkit  
**Developed by Abduu-chaker**  
GitHub: https://github.com/abduu-chaker


   Recon & API Pentesting Toolkit by Abduu-chaker


##  Overview

This toolkit provides a set of essential tools for **Bug Bounty**, **Pentesting**, and **Reconnaissance**.

It includes:

- Subdomain Enumeration  
- API Security Testing Tool  
- Port Scanning  
- Report Generation (TXT/JSON soon)  
- Modular structure ready to expand  

Perfect for beginners & professionals who want a clean and fast workflow.


#  Project Structure

recon-toolkit/

"" subdomain_enum.py       __ # Subdomain enumeration tool

"" api_security_tool.py   __  # Full API testing tool

"" port_scanner.py      __  # Basic port scanner

"" README.md           __   # Project documentation

"" requirements.txt     __   # Dependencies



#  Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/abduu-chaker/recon-toolkit
cd recon-toolkit
````

### 2️⃣ Install requirements

```bash
pip install -r requirements.txt
```

#  Tools Included

## 1️⃣ Subdomain Enumerator

Simple and efficient brute-force subdomain scanner.

### Run:

```bash
python subdomain_enum.py
```


## 2️⃣ API Security Tester (Pro)

Supports:

* GET / POST / PUT / DELETE / PATCH
* JSON Body
* Pretty JSON output
* Built‑in User-Agent: “API Tester | Abduu-chaker”
* Error handling
* Status code & header display

### Run:

```bash
python api_security_tool.py
```


## 3️⃣ Port Scanner (basic)

Scans common ports of a target host.

### Run:

```bash
python port_scanner.py
```

#  Requirements

```
requests
```

Install using:

```bash
pip install -r requirements.txt
```

#  Author

**Developed by Abduu-chaker**
GitHub → [https://github.com/abduu-chaker](https://github.com/abduu-chaker)

If you want to contribute, open a **Pull Request**.


#  License

MIT License — Free to use & modify.


#  Support the Project

Leave a star on the repo if you like the work!


#  Notes

More modules coming soon:

* Directory brute‑forcing
* Banner grabbing
* WAF detection
* Automating recon workflow



