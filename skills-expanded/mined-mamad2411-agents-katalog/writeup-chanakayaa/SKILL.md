<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-chanakayaa
description: CTF writeups and security challenges by chanakayaa.
---

# Writeups by chanakayaa

Source repository: `/repos/chanakayaa`

## Repository Index

- r3c0n_engin3/Installation_Guide.md
- r3c0n_engin3/README.md

## Writeup Content


### File: r3c0n_engin3/README.md

### 🚀 ReconEngine v9.2 – Pentest Recon & Intelligence Framework

**ReconEngine** is an advanced, modular **reconnaissance and intelligence automation framework** designed for **penetration testers, SOC teams, red teams, and auditors**. It performs deep attack surface discovery and produces **interactive, executive-ready HTML reports** with expandable modules and raw terminal-style evidence.

---

## 🔐 Key Features

### 🔍 Comprehensive Reconnaissance

* ASN mapping & WHOIS intelligence
* Passive + active subdomain enumeration
* DNS resolution & IP discovery
* Live host detection
* CDN & origin identification
* WAF detection
* TLS / SSL configuration analysis

### 🧠 Technology & Exposure Analysis

* Technology fingerprinting via **Httpx**
* Deep fingerprinting via **WhatWeb**
* Authentication & API surface mapping
* Historical URL discovery (Wayback / GAU)
* Google dork generation
* Email & OSINT harvesting

### 🛡 Security Misconfiguration Detection

* Missing / weak HTTP security headers
* TLS weaknesses
* Server & framework exposure
* WAF presence and behavior insights

### 🔎 Scanning & Enumeration

* Automated Nmap scanning
* Structured scan artifacts (normal, XML, grepable)
* Organized results per engagement

---

## 📊 Advanced Reporting Engine

ReconEngine includes a **dedicated report generator** that creates a fully interactive HTML report:

* Executive summary for management
* Expandable module-wise sections
* Intelligent summaries per module (not filenames)
* Terminal-style **“View Raw Data”** evidence
* Offline-safe (no CDN / JS frameworks)
* Audit-friendly and compliance-ready

---

## 📁 Output Structure

```text
results/
└── target_timestamp/
    ├── recon/
    │   ├── subdomains.txt
    │   ├── alive_domains.txt
    │   ├── technologies_httpx.txt
    │   ├── whatweb_tech.txt
    │   ├── security_headers_raw.json
    │   └── ...
    ├── scans/
    │   ├── nmap.nmap
    │   ├── nmap.xml
    │   └── nmap.gnmap
    └── reports/
        └── detailed_report.html
```

---

## ▶️ Usage

### Run Recon

```bash
python3 main.py -t example.com --crawl --dirs
```

### Generate Report

```bash
python3 report.py results/example.com_YYYYMMDD_HHMMSS
```


## ⚠️ Disclaimer

> ReconEngine is intended **only for authorized security testing**.
> The author is not responsible for misuse or illegal activities.

---

---

## 👤 Author

**Pushkar Singh**
Security Researcher | Pentester | 



### File: r3c0n_engin3/Installation_Guide.md

# 🛠 Installation Guide

ReconEngine requires several open-source reconnaissance tools.
To simplify installation, a **`setup.sh` script** is provided that installs and configures all dependencies automatically.

> ⚠️ **Root access is required only for installation**, not for running the framework.

---

## 📋 System Requirements

* **OS:** Kali Linux / Ubuntu (22.04+ recommended)
* **Python:** 3.9+
* **Privileges:** Root access (for setup only)
* **Internet:** Required during installation

---

## 📦 Installation Steps

### 1️⃣ Clone the Repository

```bash
git clone git@github.com:chanakayaa/r3c0n_engin3.git
cd ReconEngine
```

---

### 2️⃣ Run Setup Script (Required – as Root)

The setup script installs all required tools and dependencies.

```bash
sudo chmod +x *
sudo ./setup.sh
```

🔹 This will install:

* Python dependencies
* `httpx`
* `subfinder`
* `assetfinder`
* `amass`
* `dnsx`
* `asnmap`
* `wafw00f`
* `whatweb`
* `sslscan`
* `katana`
* `feroxbuster`
* `theHarvester`
* `nmap`
* Other supporting utilities

⏳ Installation may take several minutes depending on network speed.

---

### 3️⃣ Verify Installation

After setup completes, you should be able to run:

```bash
httpx -h
whatweb -h
nmap --version
```

If these commands work, setup is successful ✅

---

## 🚀 Running ReconEngine

### 4️⃣ Run Recon (Normal User)

> ❗ **Do NOT run recon as root unless required for specific scans**

```bash
python3 main.py -t example.com --crawl --dirs
```

📂 Output will be generated under:

```text
results/example.com_TIMESTAMP/
```

---

## 📊 Generate the Detailed Report

### 5️⃣ Generate HTML Report (After Recon Completes)

Once recon finishes, generate the interactive report:

```bash
python3 report.py results/example.com_TIMESTAMP
```

---

### 6️⃣ View the Report

Open the report in a browser:

```bash
firefox results/example.com_TIMESTAMP/reports/detailed_report.html
```

The report includes:

* Executive summary
* Expandable module-wise results
* Terminal-style raw evidence
* Scan outputs

---

## 🧹 Optional: Re-run Setup

If tools are missing or broken, re-run:

```bash
sudo ./setup.sh
```

---

## ⚠️ Important Notes

* **Authorized testing only**
* Some tools may rate-limit or behave differently on corporate networks
* Use VPN / lab environment when required
* ASNMAP would require one API Key so set the key before running the script
* Run ASNMAP it would guide you to get the FreeAPI Key

---

## 🧠 Tip (Best Practice)

```bash
# Install once as root
sudo ./
setup.sh

# Use as normal user
python3 
main.py
 -t 
target.com
python3 
report.py
 results/target_TIMESTAMP
```

---

## 🛑 Disclaimer

> ReconEngine is intended **only for authorized security testing**.
> The author is not responsible for misuse or illegal activity.



