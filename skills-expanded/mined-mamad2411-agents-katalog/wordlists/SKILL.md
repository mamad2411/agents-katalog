---
name: wordlists
description: SecLists path map, hashcat rules, CeWL usage, and custom wordlist generation for all attack categories
allowed-tools: Bash, Read
---

## SecLists Path Map

Base path: `/usr/share/seclists/`

### Subdomain / DNS Enumeration

```
Discovery/DNS/bitquark-subdomains-top100000.txt        # Top 100k subdomains
Discovery/DNS/subdomains-top1million-110000.txt        # 1M subdomains
Discovery/DNS/shubs-subdomains.txt                      # Alternative quality list
Discovery/DNS/dns-Jhaddix.txt                           # Comprehensive subdomain list
Discovery/DNS/namelist.txt                              # Short, fast list
Discovery/DNS/fierce-hostlist.txt                       # Fierce default list
Discovery/DNS/combined_subdomains.txt                   # Combined mega list
```

### Web Directory / Content Enumeration

```
Discovery/Web-Content/raft-medium-words.txt            # Balanced: 63k entries (RECOMMENDED)
Discovery/Web-Content/raft-large-words.txt             # Large: 119k entries
Discovery/Web-Content/raft-small-words.txt             # Fast: 43k entries
Discovery/Web-Content/directory-list-2.3-medium.txt   # Dirb classic medium
Discovery/Web-Content/directory-list-2.3-big.txt      # Dirb classic big
Discovery/Web-Content/common.txt                        # Quick 4k common paths
Discovery/Web-Content/big.txt                           # 20k common paths
Discovery/Web-Content/raft-medium-directories.txt      # Directories only
Discovery/Web-Content/raft-medium-files.txt            # Files only
Discovery/Web-Content/raft-medium-extensions.txt       # Extension enumeration
Discovery/Web-Content/SVNDigger/all.txt                # SVN/code repos
Discovery/Web-Content/CMS/                             # CMS-specific lists
Discovery/Web-Content/IIS.fuzz.txt                     # IIS-specific
Discovery/Web-Content/nginx.txt                        # Nginx-specific
```

### API Endpoints

```
Discovery/Web-Content/api/api-endpoints.txt            # Common API paths
Discovery/Web-Content/api/api-endpoints-res.txt        # API resource patterns
Discovery/Web-Content/api/api-seen-in-wild.txt         # Wild API endpoints
Discovery/Web-Content/api/objects.txt                  # API object names
Discovery/Web-Content/api/actions.txt                  # API action names
Discovery/Web-Content/api/graphql.txt                  # GraphQL endpoint paths
```

### Passwords by Service

```bash
# SSH brute force
/usr/share/seclists/Passwords/Common-Credentials/10k-most-common.txt
/usr/share/wordlists/rockyou.txt                       # Classic 14M

# HTTP form brute force
/usr/share/seclists/Passwords/Common-Credentials/best1050.txt
/usr/share/seclists/Passwords/Common-Credentials/best110.txt
/usr/share/seclists/Passwords/Leaked-Databases/rockyou-75.txt

# Default credentials (service-specific)
/usr/share/seclists/Passwords/Default-Credentials/default-passwords.csv
/usr/share/seclists/Passwords/Default-Credentials/ftp-betterdefaultpasslist.txt
/usr/share/seclists/Passwords/Default-Credentials/mssql-betterdefaultpasslist.txt
/usr/share/seclists/Passwords/Default-Credentials/mysql-betterdefaultpasslist.txt
/usr/share/seclists/Passwords/Default-Credentials/tomcat-betterdefaultpasslist.txt

# Web application defaults
/usr/share/seclists/Passwords/darkweb2017-top10000.txt
/usr/share/seclists/Passwords/Leaked-Databases/rockyou-10.txt
/usr/share/seclists/Passwords/Leaked-Databases/rockyou-25.txt

# SNMP community strings
/usr/share/seclists/Discovery/SNMP/common-snmp-community-strings.txt
/usr/share/seclists/Discovery/SNMP/snmp.txt

# WPA handshake cracking
/usr/share/wordlists/rockyou.txt                       # Start here
/usr/share/seclists/Passwords/WiFi-WPA/probable-v2-wpa-top4800.txt

# VNC/RDP brute
/usr/share/seclists/Passwords/Common-Credentials/500-worst-passwords.txt

# WordPress xmlrpc brute
/usr/share/seclists/Passwords/Common-Credentials/best1050.txt
```

### Usernames

```
Usernames/top-usernames-shortlist.txt                  # 17 common usernames
Usernames/Names/names.txt                              # First names
Usernames/cirt-default-usernames.txt                   # Device default users
Usernames/CommonAdminBase64.txt                        # Admin base64 encoded
Usernames/mssql-betterdefaultpasslist.txt              # MSSQL defaults
```

### Fuzzing

```
# LFI / Path Traversal
Fuzzing/LFI/LFI-Jhaddix.txt                           # 929 LFI payloads (BEST)
Fuzzing/LFI/LFI-LFISuite-pathtotest-huge.txt          # Huge LFI list
Fuzzing/LFI/LFI-gracefulsecurity-linux.txt            # Linux-specific
Fuzzing/LFI/LFI-gracefulsecurity-windows.txt          # Windows-specific

# XSS
Fuzzing/XSS/XSS-Jhaddix.txt                           # Comprehensive XSS payloads
Fuzzing/XSS/XSS-BruteLogic.txt                        # BruteLogic collection
Fuzzing/XSS/XSS-Bypass-Strings-BruteLogic.txt         # WAF bypass payloads
Fuzzing/XSS/xss-payload-list.txt                      # Extended XSS list

# SQL Injection
Fuzzing/SQLi/Generic-SQLi.txt                          # Generic SQL injection
Fuzzing/SQLi/quick-SQLi.txt                            # Quick test payloads
Fuzzing/SQLi/MySQL-SQLi-Login-Bypass.txt               # MySQL login bypass
Fuzzing/SQLi/MSSQL-Enumeration.fuzzdb.txt             # MSSQL enumeration

# SSTI
Fuzzing/template-engines-expression.txt                # Template injection payloads

# SSRF
Fuzzing/SSRF/SSRF-payloads.txt                        # SSRF bypass payloads

# XXE
Fuzzing/XXE/                                            # XXE payloads directory

# Open Redirect
Fuzzing/open-redirects-payloads.txt                   # Open redirect vectors
```

### IDOR / ID Enumeration

```bash
# Numeric IDs
seq 1 10000                                            # Pipe to ffuf: -w <(seq 1 10000)
seq 1 1000000 | shuf | head -10000                    # Random sample

# UUID generation
python3 -c "import uuid; [print(uuid.uuid4()) for _ in range(1000)]"

# Alphanumeric short IDs
/usr/share/seclists/Fuzzing/alphanumeric-case.txt
```

### Web Backup / Sensitive Files

```
Discovery/Web-Content/sensitive-files.txt              # Sensitive file paths
Discovery/Web-Content/backup-extensions.fuzz.txt      # Backup extensions
Discovery/Web-Content/CGI-Http/apache.txt             # Apache CGI
Discovery/Web-Content/.well-known/                    # .well-known paths
```

## Hashcat Rules

```bash
# Location
/usr/share/hashcat/rules/

# Best overall (start here)
/usr/share/hashcat/rules/best64.rule                   # 64 fast rules
/usr/share/hashcat/rules/d3ad0ne.rule                  # 34k rules
/usr/share/hashcat/rules/rockyou-30000.rule            # rockyou-derived
/usr/share/hashcat/rules/dive.rule                     # Deep coverage

# Combination rules
/usr/share/hashcat/rules/combinator.rule               # Word combination
/usr/share/hashcat/rules/leetspeak.rule                # Leet speak transforms

# Community rules (download separately)
# OneRuleToRuleThemAll: https://github.com/NotSoSecure/password_cracking_rules
# /opt/OneRuleToRuleThemAll.rule                       # 52k rules (BEST community)

# Multiple rules (combine effects)
hashcat -m 1000 hashes.txt wordlist.txt \
  -r /usr/share/hashcat/rules/best64.rule \
  -r /usr/share/hashcat/rules/d3ad0ne.rule

# Generate rule from known password pattern
python3 -c "
# Pattern: Capitalize first, add year + special
# Word: password → Password2024!
print('c')       # capitalize
print('$2$0$2$4') # append 2024
print('$!')      # append !
" > custom.rule
```

## Mask Attack Patterns (hashcat -a 3)

```bash
# Charsets:
# ?l = lowercase a-z
# ?u = uppercase A-Z
# ?d = digit 0-9
# ?s = special chars
# ?a = all printable
# ?b = all 0x00-0xff

# Corporate password patterns (8-12 chars)
?u?l?l?l?l?l?d?d                 # Passw01 style (8 chars)
?u?l?l?l?l?l?l?d?d               # Password01 style (9 chars)
?u?l?l?l?l?d?d?d?d               # Pass0000 style (9 chars)
?u?l?l?l?l?l?l?l?d?d?d?d         # Password0000 (12 chars)
?u?l?l?l?l?l?l?d?d?s             # Password1! (10 chars)

# PINs and numeric
?d?d?d?d                          # 4-digit PIN
?d?d?d?d?d?d                      # 6-digit PIN

# Custom charset example (lowercase + digits)
hashcat -m 0 hashes.txt -a 3 -1 ?l?d '?1?1?1?1?1?1?1?1'
```

## CeWL — Custom Wordlist Generation

```bash
# Basic spider (3 depth, 5 min word length)
cewl $URL -d 3 -m 5 -o evidence/custom_wordlist.txt

# Include lowercase variant
cewl $URL -d 3 -m 5 --lowercase -o evidence/wordlist_lower.txt

# Include email addresses found on site
cewl $URL -d 3 -m 5 -e --email_file evidence/emails.txt -o evidence/wordlist.txt

# With HTTP auth
cewl $URL -d 3 -m 5 -a --auth_type basic --auth_user $USER --auth_pass $PASS -o evidence/wordlist.txt

# Combine CeWL output with rules
hashcat -m 1000 hashes.txt evidence/custom_wordlist.txt \
  -r /usr/share/hashcat/rules/best64.rule
```

## Corporate Password Generator (Python)

```python
#!/usr/bin/env python3
"""Generate corporate password pattern wordlist from company info."""
import itertools, sys

company = sys.argv[1] if len(sys.argv) > 1 else "Company"
year_range = range(2020, 2026)
specials = ['!', '@', '#', '$', '1']

base_words = [
    company, company.lower(), company.upper(),
    company.capitalize(),
    f"{company}Corp", f"{company}Inc",
]

patterns = []
for word in base_words:
    for year in year_range:
        patterns.append(f"{word}{year}")
        for s in specials:
            patterns.append(f"{word}{year}{s}")
            patterns.append(f"{word}{s}{year}")
    for s in specials:
        patterns.append(f"{word}{s}")
        patterns.append(f"{word}{s}1")
        patterns.append(f"{word}1{s}")

for p in set(patterns):
    print(p)
```

## Permutation Generation

```bash
# Create permutations of company terms
python3 /usr/share/seclists/Passwords/permutations.py terms.txt > permuted.txt

# CeWL + permutation
cewl $URL -m 4 -d 2 --lowercase -o base.txt
python3 -c "
with open('base.txt') as f:
    words = [w.strip() for w in f if w.strip()]
for w1 in words:
    for w2 in words:
        if w1 != w2:
            print(f'{w1}{w2}')
            print(f'{w1}_{w2}')
            print(f'{w1}.{w2}')
" > permuted.txt
```

## Service-Specific Wordlist Commands

```bash
# Web directory brute (feroxbuster)
feroxbuster -u $URL \
  -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt \
  -x php,asp,aspx,jsp,txt,bak,zip,env,config,conf,xml,json \
  --filter-status 404,403,400,500 \
  -o evidence/ferox_dirs.txt

# Subdomain brute (ffuf)
ffuf -u http://FUZZ.$DOMAIN \
  -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt \
  -mc 200,301,302 \
  -o evidence/subdomain_brute.json -of json

# SSH brute (hydra)
hydra -L /usr/share/seclists/Usernames/top-usernames-shortlist.txt \
  -P /usr/share/seclists/Passwords/Common-Credentials/best110.txt \
  ssh://$TARGET -t 4 -o evidence/hydra_ssh.txt

# SMB brute (crackmapexec)
crackmapexec smb $TARGET \
  -u /usr/share/seclists/Usernames/top-usernames-shortlist.txt \
  -p /usr/share/seclists/Passwords/Common-Credentials/best1050.txt \
  --continue-on-success 2>&1 | tee evidence/cme_smb.txt

# LFI fuzz (ffuf)
ffuf -u "$URL?file=FUZZ" \
  -w /usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt \
  -mc 200 -fs $BASELINE_SIZE \
  -o evidence/lfi_results.json -of json
```
