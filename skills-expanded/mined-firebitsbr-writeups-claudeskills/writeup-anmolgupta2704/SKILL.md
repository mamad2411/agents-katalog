<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-anmolgupta2704
description: CTF writeups and security challenges by anmolgupta2704.
---

# Writeups by anmolgupta2704

Source repository: `/repos/anmolgupta2704`

## Repository Index

- ReconX/README.md
- ReconX/venv/Lib/site-packages/idna-3.10.dist-info/LICENSE.md
- ReconX/venv/Lib/site-packages/soupsieve-2.7.dist-info/licenses/LICENSE.md
- ReconX/venv/Lib/site-packages/playwright/driver/README.md
- ReconX/venv/Lib/site-packages/playwright/driver/package/README.md

## Writeup Content


### File: ReconX/README.md

# ReconX – Automated Information Gathering & Network Reconnaissance Toolkit

ReconX is an advanced reconnaissance and information gathering tool for penetration testers and security researchers.
It combines OSINT, subdomain enumeration, port scanning, web audits, screenshots, and reporting into a single framework.

⚠️ Disclaimer: **This tool is for educational and authorized penetration testing only. Do NOT scan targets without explicit written permission. Unauthorized usage is illegal.**
<img width="1000" height="500" alt="image" src="https://github.com/user-attachments/assets/c7f92c02-3ad2-4450-abea-2d628ef2f9e2" />


## ✨ Features

🔍 Google Dorking – Automates search engine dorks to find sensitive files & directories
🌍 OSINT Gathering – WHOIS lookup, DNS records, Shodan integration
🌐 Subdomain Enumeration – Finds live subdomains via crt.sh & APIs
📡 Network Scanning – Scans IP ranges, discovers open ports & services (Nmap/Scapy)
🧪 Web Security Audit – Detects missing HTTP headers, weak SSL/TLS configs
📸 Screenshots – Captures live screenshots of discovered domains using Playwright
⚠️ Risk Scoring – Calculates overall security risk based on findings
📑 Report Generation – Exports HTML / PDF / JSON professional reports

## New in v2
- Risk Score (0–100) with transparent breakdown
- Web Security Audit: security headers + TLS version + cert expiry check
- Auto-screenshots of live subdomains/pages (Playwright)

## Folder Structure

```bash
ReconX/
├── core/
│   ├── google_dorker.py
│   ├── osint_module.py
│   ├── network_scanner.py
│   ├── subdomain_enum.py
│   ├── vuln_suggester.py
│   ├── report_generator.py
│   ├── security_audit.py        
│   ├── risk_scorer.py           
│   └── screenshotter.py         
├── templates/
│   └── report_template.html     
├── reports/
├── app.py                     
├── requirements.txt         
└── README.md          
```
## Install
1️⃣ Clone Repo
```bash
git clone https://github.com/your-username/ReconX.git
cd ReconX
```
2️⃣ Setup Virtual Environment (Windows Example)
```bash
python -m venv venv
venv\Scripts\activate
```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
4️⃣ Install Playwright Browsers (for screenshots)
```bash
playwright install
```

🚀 Usage

Basic syntax:
```bash
python app.py --confirm --domain <target.com> [options]
```
### Example Commands:
1.Scan a single domain:
```bash
python app.py --confirm --domain scanme.nmap.org --osint --subdomains --web-audit --ports
```
2. Scan local network range:
```bash
python app.py --confirm --cidr 192.168.1.0/24 --network-scan
```
3. Full scan with reporting:
```bash
python app.py --confirm --domain example.com --osint --subdomains --network-scan --web-audit --screenshots --risk-score --pdf
```
### Sample Output

Reports are saved in the reports/ folder:
1.report.html → Interactive web report
2.report.pdf → Printable version
3.report.json → Machine-readable format

Example:
```bash
{
  "meta": {
    "domain": "scanme.nmap.org",
    "timestamp": "2025-08-23T10:30Z",
    "tool": "ReconX v2.0"
  },
  "findings": {
    "subdomains": ["dev.target.com", "mail.target.com"],
    "open_ports": ["80/tcp", "22/tcp"],
    "headers": ["Missing X-Frame-Options", "Weak SSL"]
  },
  "risk_score": 72
}
```
### ⚡ Key Advantages Over Other Tools

| Feature            | Nmap | theHarvester | Sublist3r | Recon-ng | ReconX ✅ |
| ------------------ | ---- | ------------ | --------- | -------- | -------- |
| Subdomain Enum     | ❌    | ✅            | ✅         | ✅        | ✅        |
| OSINT + WHOIS/DNS  | ❌    | ✅            | ❌         | ✅        | ✅        |
| Port Scanning      | ✅    | ❌            | ❌         | ❌        | ✅        |
| Web Security Audit | ❌    | ❌            | ❌         | ❌        | ✅        |
| Screenshots        | ❌    | ❌            | ❌         | ❌        | ✅        |
| Risk Scoring       | ❌    | ❌            | ❌         | ❌        | ✅        |
| Report Generation  | ❌    | ❌            | ❌         | ❌        | ✅        |


         





### File: ReconX/venv/Lib/site-packages/playwright/driver/README.md

win_amd64.whl driver package


### File: ReconX/venv/Lib/site-packages/playwright/driver/package/README.md

# playwright-core

This package contains the no-browser flavor of [Playwright](http://github.com/microsoft/playwright).



### File: ReconX/venv/Lib/site-packages/idna-3.10.dist-info/LICENSE.md

BSD 3-Clause License

Copyright (c) 2013-2024, Kim Davies and contributors.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.



### File: ReconX/venv/Lib/site-packages/soupsieve-2.7.dist-info/licenses/LICENSE.md

MIT License

Copyright (c) 2018 - 2025 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

