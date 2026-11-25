<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-adi52303
description: CTF writeups and security challenges by adi52303.
---

# Writeups by adi52303

Source repository: `/repos/adi52303`

## Repository Index

- Recon-Scanner/readme.md

## Writeup Content


### File: Recon-Scanner/readme.md

# 🕵️ Recon Scanner v1.0

A Python-based reconnaissance tool for ethical hacking and penetration testing.  
This tool automates the process of:
- WHOIS Lookup
- DNS Record Enumeration
- Subdomain Brute-Forcing
- Basic Port Scanning

It is designed for **ethical use** and **cybersecurity training** only.

---

## Features
- **WHOIS Lookup** – Get registrar, creation, and expiry details of the target.
- **DNS Enumeration** – Find A, MX, and NS records.
- **Subdomain Brute Force** – Identify possible subdomains using a wordlist.
- **Basic Port Scan** – Check for common open ports and associated services.
- **Professional Report Generation** – Saves results to `/reports` in pentest-style format.

---

## Project Structure
RECON_SCANNER/
│
├── recon_scanner.py # Main script
├── wordlists/
│ └── subdomains.txt # Subdomain brute-force wordlist
├── reports/ # Auto-generated scan reports
└── README.md # Project documentation

## Install Dependencies
pip install requests python-whois dnspython


## Usage
Run the script and enter the target domain or IP:

python recon_scanner.py
