<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-devanshubajaj07
description: CTF writeups and security challenges by DevanshuBajaj07.
---

# Writeups by DevanshuBajaj07

Source repository: `/repos/DevanshuBajaj07`

## Repository Index

- Phishy/README.md

## Writeup Content


### File: Phishy/README.md


# 🛡️ Python Penetration Testing Framework

A modular and extensible penetration testing framework built in Python. It performs reconnaissance, vulnerability scanning, simulated exploits, and generates detailed multi-format reports (TXT, PDF, JSON, HTML).

---

## 📦 Features

- 🌐 **Reconnaissance**
  - DNS & IP resolution
  - HTTP header inspection
  - `robots.txt` discovery
  - WHOIS domain lookup

- 🔍 **Scanning**
  - Port and service discovery using Nmap
  - Simulated vulnerability detection for known services (CVE-like)

- 💥 **Exploitation (Simulated)**
  - Weak login credential testing (via dynamic wordlist)
  - SQL Injection simulation
  - XSS Injection detection
  - File upload form detection

- 📝 **Reporting**
  - Multiple report formats:
    - ✅ Text (.txt)
    - ✅ HTML (.html)
  - Severity-based filtering for HTML
  - Auto-timestamped metadata

---

## 🛠️ Installation

### ✅ Requirements

- Python 3.7+
- pip
- `nmap` installed on your system and accessible via command line
- Internet access for scans

### 📥 Install Python Dependencies

```bash
pip install requests python-whois reportlab
```

> Make sure `nmap` is installed and in your system PATH:
- Linux: `sudo apt install nmap`
- macOS: `brew install nmap`
- Windows: [Download Nmap](https://nmap.org/download.html)

---

## 🚀 Usage

Run the tool via terminal:

```bash
python main.py 
```

You will see an interactive menu like this:

```
Enter target URL (e.g., http://testphp.vulnweb.com):

Select Scan Option:
1. Full Scan
2. Reconnaissance Only
3. Vulnerability Scan Only
4. Exploitation Only
5. Exit
```

Choose your desired scan mode, and the tool will start scanning the given target.

---

## 🔑 Credential Brute Force Testing

The brute-force login module now loads credentials dynamically from a file named `creds.txt`.

- Each line should be in the format: `username:password`
- A sample file is provided, and you can customize it as needed.

```
admin:admin
root:toor
guest:1234
admin:password
...
```

Place `creds.txt` in the same folder as your script before running.

---

## 📂 Report Outputs

After scanning, the following files will be created in the working directory:

| File                | Format  | Purpose                     |
|---------------------|---------|-----------------------------|
| `pentest_report.txt`  | TXT     | Raw, plain-text report      |
| `pentest_report.html` | HTML    | Stylish browser-viewable    |

---

## 📁 Project Structure

```
.
├── main.py           # Entry point CLI menu
├── recon.py          # Reconnaissance logic
├── scanner.py        # Port/CVE scan logic
├── exploit.py        # Simulated attack checks
├── reporter.py       # Multi-format reporting system
├── creds.txt         # Credential wordlist for brute-force login
├── README.md         # You're reading it!
```

---

## ⚠️ Disclaimer

This tool is for **educational and authorized testing purposes only**.  
Do not scan or attack systems without **explicit permission**. Unauthorized usage is illegal and unethical.

---

## 🧠 Author Notes

This project was built to demonstrate how basic penetration testing tools can be created in Python.  
PRs, suggestions, and ethical hackers welcome!

---


