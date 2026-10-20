<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aenoshrajora
description: CTF writeups and security challenges by aenoshrajora.
---

# Writeups by aenoshrajora

Source repository: `/repos/aenoshrajora`

## Repository Index

- recon-pipeline/README.md

## Writeup Content


### File: recon-pipeline/README.md

# Full-Scale Recon Automation Pipeline

A modular **Python-based reconnaissance framework** designed for red teaming, penetration testing, and bug bounty engagements. Automates subdomain enumeration, DNS resolution, port scanning, web fingerprinting, directory brute-forcing, screenshots, and vulnerability intelligence. Includes detailed logs, customizable wordlists, timestamped reports, and optional Slack/Discord notifications.


## 🚀 Features

- **Automated Subdomain Discovery:** Uses `subfinder` and `amass` to enumerate all subdomains.  
- **DNS Resolution:** Filters live hosts for accurate targeting.  
- **Port Scanning:** Fast scan with Masscan + detailed Nmap service/version scan.  
- **Web Technology Fingerprinting:** Detects web servers, frameworks, CMS, and other tech stacks.  
- **Directory Bruteforcing:** Discover hidden endpoints using customizable wordlists.  
- **Web Screenshotting:** Capture visual snapshots of live hosts with `gowitness`.  
- **Vulnerability Intelligence:** Banner/version gathering with placeholders for CVE matching.  
- **Notifications:** Optional Slack/Discord alerts when recon completes.  
- **Structured Reports:** Timestamped folders with JSON, text, and screenshots per target.  
- **Modular & Extensible:** Easy to add new tools or API integrations (Shodan, Censys, etc.).  


## Folder Structure
```yaml
recon-pipeline/
├─ targets/ # Target domains/IPs (one per line)
├─ wordlists/ # Directory brute-force wordlists
├─ reports/ # Timestamped recon reports per target
├─ logs/ # Runtime logs for debugging
├─ recon/
│ ├─ main.py # Orchestrates the pipeline
│ ├─ config.py # Configuration (threads, tool paths, webhooks)
│ ├─ modules/ # Modular scripts for each recon step
│ └─ utils/ # Notification scripts
```

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/aenoshrajora/recon-pipeline.git
cd recon-pipeline/recon
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure required tools are installed:

```bash
subfinder
amass
masscan
nmap
httpx
ffuf
gowitness
dnsx
```

4. Configure config.py:

Set thread count, output directories, wordlists, and optional Slack/Discord webhooks.

## Usage

1. Add targets to targets/targets.txt:
```lua
example.com
testsite.local
```
2. Run the pipeline:
```bash
python3 main.py
```
3. Check reports/ for timestamped folders containing all outputs:

```bash
reports/example.com_20250907_2100/
├─ all_subs.txt
├─ live_subs.txt
├─ masscan.txt
├─ nmap.txt
├─ web_hosts.txt
├─ ffuf_example.com.json
├─ screenshots/
└─ vuln_intel.txt
```

## Extensibility
* Integrate Shodan/Censys APIs for external intelligence.
* Add automated CVE matching using Nmap scripts or Python CVE APIs.
* Create a web dashboard to visualize results in real-time.
* Containerize the pipeline using Docker for portability.

## Legal Disclaimer
This tool is intended for authorized penetration testing, bug bounty programs, and educational purposes only. Use it responsibly and ensure you have explicit permission for all targets. The author is not responsible for any misuse.

## Contributing

* Contributions are welcome! Please:
* Fork the repo
* Create a branch (feature-name)
* Commit your changes
* Open a pull request

## Contact
* Author: [Aenosh Rajora](https://www.linkedin.com/in/aenosh-rajora/)

Star this repo if you find it useful!
