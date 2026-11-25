<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-coelhino
description: CTF writeups and security challenges by coelhino.
---

# Writeups by coelhino

Source repository: `/repos/coelhino`

## Repository Index

- c03lh1n0/README.md

## Writeup Content


### File: c03lh1n0/README.md

# c03lh1n0 - Automated WebApp Pentesting

## Overview
c03lh1n0 is a powerful command-line interface (CLI) tool designed to automate the most common penetration testing tasks for web applications. It combines multiple industry-standard tools (Nmap, Nikto, SQLMap, OWASP Zap, Dirb) to scan a web application, extract vulnerabilities, and generate a `.docx` report with results organized by severity.

### Key Features:
- **Automated Scanning**: Run multiple web app pentesting tools like Nmap, Nikto, SQLMap, OWASP Zap, and Dirb with a single command.
- **Multi-threading**: Scans run in parallel for faster results.
- **Interactive CLI**: Choose specific tools to run or scan using all tools.
- **Comprehensive Reporting**: Generates a `.docx` report organized by severity levels (High, Medium, Low).

  
### Tools Used:
1. **Nmap**: Network mapping and service version detection.
2. **Nikto**: Web server vulnerability scanner.
3. **SQLMap**: SQL injection vulnerability scanner.
4. **OWASP Zap**: Automated web app vulnerability scanner.
5. **Dirb**: Directory brute-forcing.

---

## Requirements
### Software:
- Python 3.x
- Unix-based OS (Linux or Mac recommended) or Windows Subsystem for Linux (WSL).
- Installed versions of the pentesting tools:
  - Nmap
  - Nikto
  - SQLMap
  - OWASP Zap
  - Dirb
## Installation
```
git clone https://github.com/coelhino/c03lh1n0.git
```
```
cd c03lh1n0
```
## Usage
```
python c03lh1n0.py http://example.com
```
### Python Libraries:
Install the necessary Python packages using `pip`:
```bash
pip install python-docx art

