---
name: windows-privesc
description: Use when escalating privileges on a Windows foothold during a pentest. Enumeration-first, disruption-risk-tagged. Triggers on having a low-priv Windows shell (cmd, PowerShell, evil-winrm, etc.).
---

# Windows Privilege Escalation (Pentest Mode)

Enumeration is read-only and always safe. Tag every execution path with disruption risk before running.

## Enumeration sweep (do this first, always)

Run from the foothold shell. These commands are read-only and safe.

```powershell
# Identity and privileges
whoami /all
net user %username%
net localgroup administrators

# System info
systeminfo
wmic os get Caption,Version,BuildNumber
wmic computersystem get DomainRole   # 4/5 = DC

# Running processes (look for AV, EDR, unusual services)
tasklist /v
Get-Process | Select Name,Path,Id

# Services — look for unquoted paths, writable binaries, weak ACLs
sc query type= all state= all
wmic service get Name,StartName,PathName,StartMode | findstr /i "auto"

# Scheduled tasks — look for writable scripts
schtasks /query /fo LIST /v | findstr /i "task\|run\|user"

# Unquoted service paths (classic)
wmic service get Name,PathName | findstr /v '"' | findstr /i "program files"

# AlwaysInstallElevated (if both keys are 1 → trivial escalation)
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

# Stored credentials
cmdkey /list
reg query HKLM /f password /t REG_SZ /s 2>nul | findstr /i "password"

# Writable directories in PATH
$env:PATH -split ";" | % { icacls $_ 2>$null } | findstr /i "everyone\|builtin\|users.*W"

# Token privileges — look for SeImpersonatePrivilege, SeDebugPrivilege
whoami /priv

# Network shares and connections
net share
net use
netstat -ano | findstr "LISTEN\|ESTABLISHED"
```

For a full automated sweep, use winPEAS if available:

```powershell
.\winPEAS.exe > C:\Users\Public\wp.txt
# then exfil wp.txt for review — do not leave it on the host
```

## Findings by disruption risk

### Disruption: none (preferred — enumerate before executing)

- **AlwaysInstallElevated**: both HKLM + HKCU reg keys set to 1.
  Generate a malicious `.msi` with msfvenom (`-f msi`), run it as the low-priv user.
  Gives `SYSTEM`. Evidence: reg query output + msi execution log.

- **Unquoted service path**: service binary path has spaces and no quotes.
  If you can write to one of the intermediate directories, plant a fake binary.
  Service must restart for the path to be traversed — check start mode.

- **Stored credentials** (`cmdkey /list`): may reveal domain/service creds.
  Use `runas /savecred /user:<domain>\<user> cmd.exe` to consume them.

- **Token impersonation (SeImpersonatePrivilege)**: most common in service
  accounts. Use Potato family (PrintSpoofer, GodPotato, JuicyPotato) depending
  on OS version.

- **Weak service binary ACL**: `icacls <service.exe>` shows write access for
  the current user or a group we're in. Replace binary with payload; trigger
  service restart.

- **Writable service config** (`sc config`): if we can change `binPath=`
  directly, no binary replacement needed. Same caveat: restart required.

- **DLL hijacking**: service loads a DLL by name without a qualified path,
  and we can write to a directory that appears earlier in the search order.
  Plant a malicious DLL; wait for the service to load it.

- **Saved browser credentials**: use LaZagne, SharpWeb, or manual extraction
  if authorized.

### Disruption: low

- **Scheduled task with writable script**: replace the script payload.
  Task runs as SYSTEM or admin. Brief modification of an existing file.

- **Registry autoruns**: writable keys under `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
  if the current user has write access. Executes on next login/reboot.

### Disruption: medium

- **Service binary replacement**: requires stopping and starting the service.
  Brief outage of the service being replaced.

- **DLL side-loading into a running process**: injecting a DLL into a
  live service can crash it if the DLL faults.

### Disruption: high

- **UAC bypass**: many techniques modify registry heuristics that auto-elevate
  certain binaries. Risk is low on modern Windows, but loud — EDR will likely
  alert.

- **Token manipulation** (impersonation of another logged-on user's token):
  may log events and disrupt the impersonated session in edge cases.

### Disruption: dos-likely (operator approval required)

- **Kernel exploits** (PrintNightmare, EternalBlue, HiveNightmare variants):
  crash-prone on some patch levels. Surface but do NOT run without explicit
  per-host operator approval AND ROE `allowed_techniques_with_caveat.kernel_exploit_stable`.

## Active Directory / domain context

These apply when the foothold is domain-joined:

```powershell
# Current domain
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
net group "Domain Admins" /domain

# Kerberoastable accounts
# Prefer running from the attacker box after getting a valid TGT:
# GetUserSPNs.py <domain>/<user>:<pass> -dc-ip <DC> -request
# Hashes go to creds.age via credential_vault hook, not findings.json

# AS-REP roasting (accounts with DONT_REQ_PREAUTH)
# GetNPUsers.py <domain>/ -usersfile users.txt -dc-ip <DC>
```

Credential material discovered during AD attacks must go to `creds.age` via
the operator. The `credential_vault.py` hook will surface a warning when it
detects NTLM hashes or Kerberos tickets in tool output.

## Execution discipline

- **Verify preconditions first.** An unquoted service path only works if you
  can write to the intermediate directory AND trigger a restart. Check both
  before planting anything.
- **One escalation is enough.** Take the safest path that achieves admin/SYSTEM.
  Do not run all three potato exploits to prove they all work.
- **Capture evidence as you go.** Each technique used: command + output showing
  the privilege level before and after (`whoami /all`).
- **Clean up artifacts.** Any binary or DLL planted on the target should be
  noted in the finding's reproduction steps as something to remove during
  remediation, and operator must confirm removal post-engagement.

## What goes in the finding

- The specific misconfiguration (reg key, ACL, service config, etc.)
- Why it grants escalation (path traversal, token abuse, etc.)
- Reproduction steps from the foothold user context
- Evidence refs: `whoami /priv` before, `whoami /all` after escalation
- Remediation: specific configuration fix (e.g. "add quotes to service
  ImagePath", "disable AlwaysInstallElevated", "patch KB…")
- Remediation effort: low for config fixes, medium for patching
