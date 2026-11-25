<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-advaith-s-dev
description: CTF writeups and security challenges by ADVAITH-S-DEV.
---

# Writeups by ADVAITH-S-DEV

Source repository: `/repos/ADVAITH-S-DEV`

## Repository Index

- Basic_pentesting_1-Report-/README.md

## Writeup Content


### File: Basic_pentesting_1-Report-/README.md

# Basic_pentesting_1(Report)


## Project Overview

This repository contains all deliverables for the penetration test of the “Basic Pentesting: 1” VM from VulnHub. The objective was to:

- Discover target IP using netdiscover  
- Scan open ports & services with Nmap  
- Enumerate web vulnerabilities using Nikto  
- Brute-force credentials with Hydra  
- Exploit ProFTPD via Metasploit and obtain a reverse shell  

Machine Download & Setup Instructions:  
🔗 https://www.vulnhub.com/entry/basic-pentesting-1,216/ :contentReference[oaicite:1]{index=1}  

---

## Prerequisites

- Kali Linux (VirtualBox or VMware)  
- Installed tools: `nmap`, `nikto`, `hydra`, `msfconsole`  
- Host-only network configured  

---

## Setup & Installation

1. **Download & Import VM**  
   - Download the “Basic Pentesting: 1” ZIP from VulnHub.  
   - Extract and import the `.vmdk` into VirtualBox as a new Linux (Ubuntu 64-bit) VM.  
2. **Network Configuration**  
   - Adapter 1 → Host-Only Adapter  
   - Ensure your Kali VM is on the same host-only network.  

---
## Report Structure

All findings are documented in `BasicPentest1_Report.pdf`, which includes:

- **Cover Page**
- **Executive Summary**
- **Reconnaissance & Scanning**
- **Enumeration**
- **Exploitation & Post-Exploitation**
- **Lessons Learned**
- **Suggestions for Defense**

## License

This project is for educational purposes only. No license is granted for malicious use.


