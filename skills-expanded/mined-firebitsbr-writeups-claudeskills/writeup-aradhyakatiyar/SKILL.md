<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aradhyakatiyar
description: CTF writeups and security challenges by AradhyaKatiyar.
---

# Writeups by AradhyaKatiyar

Source repository: `/repos/AradhyaKatiyar`

## Repository Index

- Vulnerability-Scanner/README.md

## Writeup Content


### File: Vulnerability-Scanner/README.md

# Vulnerability Scanner (Kali-friendly, safe-by-default)

This is a **learning project** that scans only systems you own (or have explicit permission). It does:
- Async **port scanning** on common ports
- **Banner grabbing** for basic service fingerprinting
- **HTTP security header** checks
- **TLS version** support checks (detects deprecated TLS 1.0/1.1)
- Writes **report.json** and **report.html**

> ⚠️ **Safety**: By default, the scanner **refuses to scan non-private addresses** (public internet) unless you pass `--allow-external`. For your coursework/projects, stick to `localhost` and Docker containers.

---

## 1) Setup on Kali (one-time)
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip docker.io docker-compose-plugin
```

## 2) Create and activate a virtual environment
```bash
cd vulnscanner
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> When you're done working: `deactivate`

## 3) Start a **safe local test lab** (optional but recommended)
This uses Docker to spin up two local targets:
- `insecure_web` (Python simple HTTP server on **:8000**) → no TLS, no security headers
- `juice_shop` (OWASP Juice Shop on **:3000**) → intentionally vulnerable app for learning

```bash
sudo docker compose up -d
# wait a few seconds, then you can visit:
# http://localhost:8000 and http://localhost:3000
```

Stop the lab later with:
```bash
sudo docker compose down
```

## 4) Run the scanner (examples)

Scan the sample targets from `targets.txt`:
```bash
source .venv/bin/activate     # if not already active
python scanner.py --hosts-file targets.txt --ports common --output report
```

Scan localhost with a port range (1..1024) and slower concurrency (extra safe):
```bash
python scanner.py --hosts localhost --ports 1-1024 --concurrency 50 --timeout 1.5 --output localhost_report
```

> The tool writes `report.json` and `report.html`. Open the HTML in your browser.

## 5) Legal & ethical
Only scan machines you own or are **explicitly authorized** to test. Your ISP/organization may have policies and IDS/IPS. Keep scans to your lab (localhost/Docker).

## 6) How it works (high level)
- Async TCP connect to ports → mark **open/closed**, try to **read a banner**
- If a web service is found (HTTP/HTTPS), it fetches `/` and checks for:
  - **HSTS**, **CSP**, **X-Content-Type-Options**, **X-Frame-Options**, **Referrer-Policy**
- For HTTPS ports, attempts TLS handshakes restricted to **1.0 / 1.1 / 1.2 / 1.3** to see what's supported
- Findings are aggregated into a simple HTML and JSON report

## 7) Customize
- Change the port set with `--ports` (e.g., `1-1024` or `22,80,443`)
- Add/remove targets in `targets.txt`
- Tweak concurrency/timeouts to be gentler on targets

## 8) Troubleshooting
- `ModuleNotFoundError: aiohttp` → run `pip install -r requirements.txt` inside the virtualenv
- Permission denied on Docker → add your user to `docker` group or prefix with `sudo`
- HTML shows no issues but ports are open → the scanner is lightweight; use Nmap for deeper fingerprinting if permitted

Happy (and responsible) hacking! 🛡️

