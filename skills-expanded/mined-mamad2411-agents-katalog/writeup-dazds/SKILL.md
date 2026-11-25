<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dazds
description: CTF writeups and security challenges by DAZDS.
---

# Writeups by DAZDS

Source repository: `/repos/DAZDS`

## Repository Index

- bugbounty-framework/docs/CHANGELOG.md
- bugbounty-framework/docs/INTEGRATIONS.md
- bugbounty-framework/docs/README.md
- bugbounty-framework/docs/SETUP.md

## Writeup Content


### File: bugbounty-framework/docs/README.md

# DAZ Sentinel – Bug Bounty Framework

An advanced modular bug bounty and penetration testing framework by **DAZDS**.

## Features

- Automated reconnaissance (subdomain, IP, HTTP, WHOIS)
- Vulnerability scanning (CVE, port, service)
- Exploitation modules
- Report generator with CVE/CWE mapping
- Integrated SecLists database
- Modular and customizable



### File: bugbounty-framework/docs/CHANGELOG.md

# Changelog

## v1.0 – Initial Release

- Setup script with environment validation
- Modules: recon, portscan, vulnscan, exploit, fuzz, intel_report, report
- Integrated SecLists
- Logging of environment state



### File: bugbounty-framework/docs/INTEGRATIONS.md

# Integrated Projects

## SecLists
- Source: https://github.com/danielmiessler/SecLists
- License: MIT
- Integrated into `config/SecLists/`
- Auto-updated during setup
- Used by recon, fuzzing and grep modules



### File: bugbounty-framework/docs/SETUP.md

# Setup Instructions – DAZ Sentinel Bug Bounty Framework

This document explains how to install and use the DAZ Sentinel framework.

## 📦 Requirements

- OS: Kali Linux, Parrot OS, Ubuntu (preferred)
- Internet access
- `git`, `curl`, `jq`, `golang`

## ⚙️ Setup Steps

```bash
# Step 1: Clone the repository
git clone https://github.com/DAZDS/bugbounty-framework.git
cd bugbounty-framework

# Step 2: Run setup script
chmod +x setup.sh
./setup.sh
```

## 🧪 What setup.sh does:

- Installs tools: `amass`, `ffuf`, `gobuster`, `httpx`, `gau`, `waybackurls`, etc.
- Creates structure: `modules/`, `output/`, `config/`, `reports/`
- Clones and integrates SecLists
- Logs system environment in `output/env-check.txt`

## ✅ Run modules

Each module is inside the `modules/` directory and can be executed independently:

```bash
bash modules/recon.sh target.com
bash modules/vulnscan.sh target.com
bash modules/report.sh target.com
```

You can also run all steps:

```bash
bash run_all.sh target.com
```

## 📤 Push changes to GitHub

Use `push.sh` to commit and upload changes:

```bash
bash push.sh
```

