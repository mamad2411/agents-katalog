---
name: seclists
description: >
  Use, navigate, and integrate SecLists — the community-curated collection of security
  wordlists and payloads maintained at danielmiessler/SecLists (61k+ stars). Use when
  selecting wordlists for directory bruteforcing, credential spraying, fuzzing, subdomain
  enumeration, or payload injection. Covers directory structure, list selection strategy,
  key files, integration with ffuf/gobuster/hydra/burp/wfuzz, custom list creation,
  and operational best practices for penetration testing engagements.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/danielmiessler/SecLists
---

# seclists Agent Skill

## When to Use This Skill

Use this skill when:
- The user needs to select a wordlist for a specific attack phase
- Performing web content discovery, credential attacks, or fuzzing
- Integrating wordlists into ffuf, gobuster, hydra, burpsuite, wfuzz, or medusa
- Building custom wordlists derived from SecLists content
- The user asks about rockyou.txt, raft lists, common.txt, or directory-list-2.3-*

## What SecLists Does

SecLists is a collection of multiple types of lists used during security assessments. It is not a tool — it is a wordlist repository that feeds into virtually every other offensive security tool. The repository is organized by assessment phase and attack type, making list selection a deliberate, intelligence-driven decision rather than defaulting to a single massive file.

## Installation

```bash
# Kali Linux (pre-installed at /usr/share/seclists or installable via apt)
sudo apt install seclists
ls /usr/share/seclists/

# Clone from GitHub (always get latest)
git clone --depth 1 https://github.com/danielmiessler/SecLists.git /opt/seclists

# Partial clone — only the Discovery subtree (saves disk space)
git clone --depth 1 --filter=blob:none --sparse https://github.com/danielmiessler/SecLists.git /opt/seclists
cd /opt/seclists && git sparse-checkout set Discovery/Web-Content

# Update existing clone
cd /opt/seclists && git pull

# On macOS via Homebrew
brew install seclists
# Installs to: /opt/homebrew/share/seclists/ or /usr/local/share/seclists/

# Docker — use as a volume mount in tool containers
docker run --rm -v /opt/seclists:/seclists ghcr.io/ffuf/ffuf -w /seclists/Discovery/Web-Content/common.txt ...
```

## Core Concepts

### Repository Size and Selectivity

SecLists is large (~1.5 GB full clone). Never use the largest list available by default — match list size to the target's response time, rate limits, and available time window. A 4.6M-line list against a 200ms endpoint takes hours; start small and escalate.

### List Selection Hierarchy

1. **Start small**: common.txt (4,727 entries), best-1050.txt (1,050 entries)
2. **Escalate**: raft-medium-* (~63k entries), directory-list-2.3-medium (~220k entries)
3. **Exhaustive**: directory-list-2.3-big (~1.2M), directory-list-2.3-small for CI checks

### Wordlist Quality Tiers

| Tier | Examples | Use Case |
|------|----------|----------|
| Small/fast | common.txt, best-1050.txt | Quick recon, time-boxed engagements |
| Medium | raft-medium-words.txt, directory-list-2.3-medium.txt | Standard pentest |
| Large | directory-list-2.3-big.txt, rockyou.txt | Targeted, longer-running attacks |
| Specialized | api/api-endpoints.txt, SVNDigger/ | Technology-specific |

## Directory Structure

```
SecLists/
├── Discovery/
│   ├── Web-Content/           # Directory/file bruteforcing
│   │   ├── common.txt                   # 4,727 entries — universal starting point
│   │   ├── best-1050.txt                # 1,050 highest-hit entries
│   │   ├── directory-list-2.3-small.txt
│   │   ├── directory-list-2.3-medium.txt  # ~220k entries — standard pentest
│   │   ├── directory-list-2.3-big.txt
│   │   ├── raft-small-words.txt
│   │   ├── raft-medium-words.txt        # ~63k — good balance
│   │   ├── raft-large-words.txt
│   │   ├── raft-small-directories.txt
│   │   ├── raft-medium-directories.txt
│   │   ├── raft-large-directories.txt
│   │   ├── raft-small-files.txt
│   │   ├── raft-medium-files.txt
│   │   ├── big.txt                      # ~20k — good general list
│   │   ├── burp-parameter-names.txt     # HTTP parameter fuzzing
│   │   ├── api/
│   │   │   └── api-endpoints.txt        # REST API paths
│   │   ├── IIS.fuzz.txt                 # IIS-specific
│   │   ├── Apache.fuzz.txt
│   │   ├── Nginx.fuzz.txt
│   │   └── swagger.txt                  # Swagger/OpenAPI paths
│   ├── DNS/                   # Subdomain enumeration
│   │   ├── subdomains-top1million-5000.txt
│   │   ├── subdomains-top1million-20000.txt
│   │   ├── subdomains-top1million-110000.txt  # Comprehensive
│   │   └── fierce.txt
│   ├── Infrastructure/        # Network recon
│   │   └── nmap-ports-top1000.txt
│   └── SNMP/
│       └── common-snmp-community-strings.txt
├── Fuzzing/                   # Protocol/input fuzzing
│   ├── SQLi/
│   │   ├── quick-SQLi.txt
│   │   └── Generic-SQLi.txt
│   ├── XSS/
│   │   ├── XSS-Jhaddix.txt
│   │   └── XSS-BruteLogic.txt
│   ├── LFI/
│   │   ├── LFI-Jhaddix.txt
│   │   └── LFI-gracefulsecurity-linux.txt
│   ├── SSTI/
│   ├── xxe.txt
│   ├── command-injection-commix.txt
│   ├── fuzz-Bo0oM.txt                   # Generic boundary fuzzing
│   └── special-chars.txt
├── Passwords/                 # Password attacks
│   ├── Leaked-Databases/
│   │   └── rockyou.txt.tar.gz           # 14.3M entries — seminal breach list
│   ├── Common-Credentials/
│   │   ├── top-passwords-shortlist.txt  # 100 entries
│   │   ├── top-20-common-SSH-passwords.txt
│   │   └── 10-million-password-list-top-100.txt
│   ├── Default-Credentials/
│   │   ├── default-passwords.csv
│   │   └── ftp-betterdefaultpasslist.txt
│   └── Malware/
│       └── mirai-botnet.txt             # IoT default creds
├── Usernames/
│   ├── top-usernames-shortlist.txt      # 17 entries — quick spray
│   ├── xato-net-10-million-usernames.txt
│   └── Names/
│       ├── names.txt
│       └── familynames-usa-top1000.txt
├── Miscellaneous/
│   ├── User-Agents/
│   │   └── user-agents.txt
│   └── web-extensions.txt
└── Web-Shells/
    └── laudanum/                        # PHP, ASP, JSP shells
```

## CLI Reference — Integration Examples

### ffuf (Web Content Discovery)

```bash
# Basic directory discovery
ffuf -w /opt/seclists/Discovery/Web-Content/common.txt -u https://target.com/FUZZ

# With file extensions
ffuf -w /opt/seclists/Discovery/Web-Content/raft-medium-words.txt \
     -u https://target.com/FUZZ \
     -e .php,.txt,.html,.bak,.zip,.conf

# Filter by response size/status
ffuf -w /opt/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
     -u https://target.com/FUZZ \
     -mc 200,301,302,403 \
     -fs 1234 \
     -t 40 -rate 100

# Parameter fuzzing
ffuf -w /opt/seclists/Discovery/Web-Content/burp-parameter-names.txt \
     -u https://target.com/page?FUZZ=test \
     -mc 200

# Subdomain enumeration
ffuf -w /opt/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
     -u https://FUZZ.target.com \
     -H "Host: FUZZ.target.com" \
     -mc 200,301,302

# Virtual host discovery
ffuf -w /opt/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
     -u http://10.10.10.10/ \
     -H "Host: FUZZ.target.com" \
     -fs 4242
```

### gobuster

```bash
# Directory mode
gobuster dir -u https://target.com \
  -w /opt/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt \
  -x php,html,txt -t 50 -o gobuster_out.txt

# DNS subdomain mode
gobuster dns -d target.com \
  -w /opt/seclists/Discovery/DNS/subdomains-top1million-20000.txt \
  -t 50

# Vhost mode
gobuster vhost -u http://target.com \
  -w /opt/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
  --append-domain
```

### hydra (Credential Attacks)

```bash
# SSH with SecLists wordlists
hydra -L /opt/seclists/Usernames/top-usernames-shortlist.txt \
      -P /opt/seclists/Passwords/Common-Credentials/10-million-password-list-top-100.txt \
      ssh://10.10.10.10

# Web login with rockyou
hydra -l admin \
      -P /opt/seclists/Passwords/Leaked-Databases/rockyou.txt \
      target.com http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"
```

### SQLMap / Fuzzing

```bash
# Use SecLists SQLi payloads with sqlmap's tamper
sqlmap -u "http://target.com/page?id=1" \
       --sql-query-file=/opt/seclists/Fuzzing/SQLi/Generic-SQLi.txt

# Burp Suite Intruder: load from file
# Positions → Add § markers → Payloads → Load → select SecLists file
```

## Common Workflows

### Web Application Discovery Phase

```bash
# Step 1: Quick sweep — catch low-hanging fruit fast
ffuf -w /opt/seclists/Discovery/Web-Content/best-1050.txt \
     -u https://target.com/FUZZ -mc 200,301,302,403 -t 50

# Step 2: Medium list with extensions based on tech stack
TECH=php  # or asp, jsp, aspx
ffuf -w /opt/seclists/Discovery/Web-Content/raft-medium-words.txt \
     -u https://target.com/FUZZ -e .$TECH,.bak,.conf,.log \
     -mc 200,301,302,403 -t 40 -o step2.json -of json

# Step 3: Recurse into found directories
ffuf -w /opt/seclists/Discovery/Web-Content/common.txt \
     -u https://target.com/admin/FUZZ -mc 200,301,302,403

# Step 4: API endpoint hunting
ffuf -w /opt/seclists/Discovery/Web-Content/api/api-endpoints.txt \
     -u https://target.com/api/FUZZ -mc 200,201,400,401,403
```

### Password Spray Workflow

```bash
# Extract top-100 passwords
head -100 /opt/seclists/Passwords/Leaked-Databases/rockyou.txt > /tmp/top100.txt

# Add company-specific mutations manually or with hashcat rules
# Then spray
hydra -L /opt/seclists/Usernames/xato-net-10-million-usernames.txt \
      -P /tmp/top100.txt \
      -t 4 -W 3 \
      smb://10.10.10.10
```

### Subdomain Enumeration Chain

```bash
# Fast initial — 5k list
ffuf -w /opt/seclists/Discovery/DNS/subdomains-top1million-5000.txt \
     -u https://FUZZ.target.com -mc 200,301 -t 50 -o subs_fast.json -of json

# Full — 110k list piped into httpx for live validation
cat /opt/seclists/Discovery/DNS/subdomains-top1million-110000.txt | \
  sed 's/^/http:\/\//' | sed 's/$/.target.com/' | \
  httpx -silent -mc 200,301,302 -o live_subs.txt
```

## Advanced Techniques

### Building Technology-Targeted Lists

```bash
# Combine Apache-specific + common + PHP files
cat /opt/seclists/Discovery/Web-Content/Apache.fuzz.txt \
    /opt/seclists/Discovery/Web-Content/common.txt \
    <(grep "\.php$" /opt/seclists/Discovery/Web-Content/raft-large-files.txt) \
    | sort -u > /tmp/apache_php_combined.txt
```

### Generating CeWL + SecLists Hybrid Lists

```bash
# Spider target for custom keywords
cewl -d 3 -m 5 -w /tmp/cewl_target.txt https://target.com

# Merge with SecLists passwords
cat /tmp/cewl_target.txt \
    /opt/seclists/Passwords/Common-Credentials/top-passwords-shortlist.txt \
    | sort -u > /tmp/hybrid_passwords.txt
```

### Extracting Specific Entry Types

```bash
# Only .bak and .old files from raft list
grep -E '\.(bak|old|backup|orig)$' \
  /opt/seclists/Discovery/Web-Content/raft-large-files.txt > /tmp/backups.txt

# Only entries without extensions (pure directories)
grep -v '\.' /opt/seclists/Discovery/Web-Content/raft-large-words.txt > /tmp/dirs_only.txt

# Deduplicate merged lists
sort -u /tmp/list1.txt /tmp/list2.txt > /tmp/merged_dedup.txt
```

### Rate-Limited Environments

```bash
# Use smallest list, slow rate, randomize order
shuf /opt/seclists/Discovery/Web-Content/best-1050.txt > /tmp/shuffled.txt
ffuf -w /tmp/shuffled.txt -u https://target.com/FUZZ \
     -rate 10 -p 0.1-0.5 -mc 200,301,302,403
```

### Burp Suite Integration

1. **Intruder**: Payload Sets → Payload type: Simple list → Load → select SecLists file
2. **Extensions (Turbo Intruder)**: Reference SecLists paths directly in Python script
3. **Active Scan**: Configure scan insertion points using SecLists fuzzing payloads

### Using SecLists with wfuzz

```bash
wfuzz -c -w /opt/seclists/Fuzzing/SQLi/quick-SQLi.txt \
      --hc 404 "https://target.com/page?id=FUZZ"

wfuzz -c -w /opt/seclists/Fuzzing/XSS/XSS-Jhaddix.txt \
      -H "Cookie: session=abc123" \
      --hh 1234 "https://target.com/search?q=FUZZ"
```

## Keeping Lists Updated

```bash
# Update the repo
cd /opt/seclists && git pull origin master

# Check what changed recently
git log --oneline -20
git diff HEAD~5 HEAD --name-only

# Symlink Kali's apt-installed copy to your working directory
ln -s /usr/share/seclists /opt/seclists
```

## Troubleshooting

**rockyou.txt is compressed on Kali:**
```bash
gunzip /usr/share/wordlists/rockyou.txt.gz
# or reference SecLists copy directly
find /opt/seclists -name "rockyou*"
```

**List too large — scan takes forever:**
- Limit with `head -n 10000 biglist.txt > /tmp/trimmed.txt`
- Use ffuf's `-rate` and `-t` (threads) to throttle
- Switch to best-1050.txt or common.txt first

**Too many false positives (403s cluttering results):**
```bash
ffuf ... -fc 403    # filter status code
ffuf ... -fs 1234   # filter by size
ffuf ... -fw 42     # filter by word count
ffuf ... -fl 10     # filter by line count
```

**Encoding issues with payload lists:**
```bash
# Convert to UTF-8, strip non-printable
iconv -f latin1 -t utf8 rockyou.txt | strings > rockyou_clean.txt
```

**Git clone too slow / repo too large:**
```bash
# Shallow clone + sparse checkout for only what you need
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/danielmiessler/SecLists.git /opt/seclists
cd /opt/seclists
git sparse-checkout set Discovery/Web-Content Passwords/Leaked-Databases
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
