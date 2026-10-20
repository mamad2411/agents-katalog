<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hairyankle
description: CTF writeups and security challenges by HairyAnkle.
---

# Writeups by HairyAnkle

Source repository: `/repos/HairyAnkle`

## Repository Index

- reconforge-cli/README.md
- vulnlab-webapp/README.md
- vulnlab-webapp/patches/README.md
- vulnlab-webapp/reports/README.md
- vulnlab-webapp/reports/TEMPLATE.md
- vulnlab-webapp/tests-security/README.md

## Writeup Content


### File: reconforge-cli/README.md

# ReconForge CLI — Modular Pentest Recon Pipeline

A CLI-based reconnaissance toolkit for **authorized security testing**.

> ⚠️ Authorized use only. Run this tool only on systems you own or where you have explicit written permission.

## What is implemented now

### Core
- ✅ Target intake: domain / CIDR / list file / scope file (`targets`, `run`)
- ✅ Subdomain collection with pluggable sources (`common`, `wordlist`)
- ✅ DNS resolve + dedup
- ✅ Live host probing (HTTP/HTTPS) + titles/status
- ✅ Port scanning (top or full) + simple rate control
- ✅ Service parsing + inventory summary (`ports/inventory.json`)
- ✅ Markdown + JSON report generation

### Optional
- ✅ Endpoint directory discovery with wordlist (`webdirs`)
- ⏳ Tech fingerprint hints
- ⏳ Endpoint crawl + URL extraction
- ⏳ Screenshots integration (`gowitness`/`aquatone`)
- ⏳ Caching
- ⏳ Resume support

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e . --no-build-isolation
python3 -m reconforge --help
```

## Commands

- `targets` build `scope/in_scope.txt` and `scope/out_of_scope.txt`
- `subdomains` collect/resolve subdomains
- `alive` probe HTTP/HTTPS and print terminal output
- `ports` scan top/full ports and output inventory
- `webdirs` brute-force directories from a wordlist
- `report` generate and print Markdown report
- `run` full pipeline

## Examples

### 1) Build scope inputs

```bash
python3 -m reconforge targets --domain example.com --cidr 10.10.10.0/30 --list targets.txt --scope scope.txt --out runs/example
```

`scope.txt` format supports:
- `+value` include
- `-value` exclude
- `value` include

### 2) Subdomains with pluggable sources

```bash
python3 -m reconforge subdomains \
  --domain example.com \
  --sources common,wordlist \
  --wordlist wordlists/subs.txt \
  --out runs/example
```

### 3) Alive + ports + webdirs

```bash
python3 -m reconforge alive --input runs/example/subdomains/resolved.txt --out runs/example
python3 -m reconforge ports --input runs/example/alive/alive.txt --out runs/example --top 10 --rate 200
python3 -m reconforge webdirs --input runs/example/alive/alive.txt --wordlist wordlists/common.txt --out runs/example
python3 -m reconforge report --input runs/example
```

### 4) One-shot run

```bash
python3 -m reconforge run \
  --domain example.com \
  --sources common,wordlist \
  --sub-wordlist wordlists/subs.txt \
  --web-wordlist wordlists/common.txt \
  --top 10 --rate 200 \
  --out runs/example
```

## Output files

- `scope/in_scope.txt`, `scope/out_of_scope.txt`
- `subdomains/all.txt`, `resolved.txt`, `failed.txt`, `sources.json`
- `alive/alive.txt`, `alive/alive.json`, `web/titles.txt`
- `ports/services.txt`, `ports/ports.json`, `ports/inventory.json`
- `web/endpoints.txt`, `web/directories.json`
- `report/report.md`, `report/summary.json`



### File: vulnlab-webapp/README.md

# VulnLab Web App (Build → Break → Fix)

A local-first security learning project: build a realistic mini web app, introduce vulnerabilities in controlled commits, then patch and document them.

## Finalized Stack

- **Python 3.12**
- **Flask**
- **SQLite**
- **Docker / Docker Compose**

## Current App Modules

- Authentication (register/login/logout)
- User profile (bio + avatar upload)
- Notes CRUD (access-controlled)
- Basic admin panel

## Quick Start

### Docker (recommended)

```bash
docker compose up --build
```

Then open: `http://localhost:5000`

### Local Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app run.py init-db
flask --app run.py create-admin
flask --app run.py seed-lab
python run.py
```

Then open: `http://localhost:5000`

## Default Workflow

1. Initialize/run the app.
2. Register users and create baseline data.
3. Add a vulnerability scenario in a dedicated change.
4. Write a report in `reports/` with PoC + impact + remediation.
5. Patch and add regression checks in `tests-security/`.

## Repository Layout

```text
.
├── app/                    # Flask app source
├── docker/                 # Dockerfile
├── reports/                # vulnerability write-ups
├── patches/                # optional patch notes
├── tests-security/         # regression/security checks
├── screenshots/            # PoC screenshots
├── docker-compose.yml
├── requirements.txt
└── run.py
```

## Disclaimer

Intentionally vulnerable variants should be used **only** in local labs or authorized environments.



### File: vulnlab-webapp/patches/README.md

# Patch Notes

Use this directory for optional patch notes or diff snippets that summarize how vulnerabilities were fixed.



### File: vulnlab-webapp/reports/README.md

# Vulnerability Reports

Store one markdown file per finding (for example: `IDOR.md`, `Stored-XSS.md`).

Recommended sections:
- Title / Summary
- Affected endpoint(s)
- Severity
- Steps to reproduce
- Impact
- Recommendation
- Patch summary
- References



### File: vulnlab-webapp/tests-security/README.md

# Security Regression Checks

Add regression checks here as vulnerabilities are patched.

Examples:
- access control checks for IDOR regressions
- output encoding checks for stored XSS regressions
- CSRF enforcement checks for state-changing routes



### File: vulnlab-webapp/reports/TEMPLATE.md

# <Finding Title>

## Summary

## Affected Endpoints

## Severity

## Steps to Reproduce

## Impact

## Recommendation

## Patch Summary

## References

